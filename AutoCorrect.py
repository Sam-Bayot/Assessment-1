#File: AutoCorrect.py
#Description: This file is used to check if a string is similar to a target string
# and if so, give the distance between the strings
#Author: Sam Bayot
#Last Modified: 19/03/26

import copy

#Class for distance
class Distance:
    def __init__(self, check_string: str, target_string: str, distance: int) -> None:
        self.check_string: str = check_string
        self.target_string: str = target_string
        self.distance: int = distance

#Class for distance and also to find changes to the strings
class LevenshteinDistance(Distance):
    def __init__(self, check_string: str, target_string: str, distance: int, matrix: list[list[int]]) -> None:
        super().__init__(check_string, target_string, distance)
        self.matrix: list[list[int]] = matrix
        self.change_positions: list[dict[str, list[tuple[int, int]]]] = []

    #Gets the insertions, deletions and replacements between the two strings
    def find_changes(self, best_string_transform_distance: float = -1) -> list[dict[str, list[tuple[int, int]]]]:
        INSERTION_ERROR: float = 4
        DELETION_ERROR: float = 4.5
        TRANSPOSITION_ERROR: float = 1.5
        REPLACEMENT_MULTIPLIER: float = 1.1
        #Gets the distance between two letters using the Pythagoras formula
        def get_letter_distance(check_letter: str, target_letter: str):
            #Holds all of the relative positions of the letters on a QWERTY NZ keyboard
            KEY_POSITIONS: dict[str, tuple[int, int]] = {
                "!": (0,0), "@": (0,1), "#": (0,2), "$": (0,3), "%": (0,4), "^": (0,5), "&": (0,6), "*": (0,7), "(": (0,8), ")": (0,9), "_": (0,10), "+": (0,11),
                
                "1": (0,0), "2": (0,1), "3": (0,2), "4": (0,3), "5": (0,4), "6": (0,5), "7": (0,6), "8": (0,7), "9": (0,8), "0": (0,9), "-": (0,10), "=": (0,11),

                                                                                                                                        "{": (1,10), "}": (1,11), "|": (1,12),

                "Q": (1,0), "W": (1,1), "E": (1,2), "R": (1,3), "T": (1,4), "Y": (1,5), "U": (1,6), "I": (1,7), "O": (1,8), "P": (1,9), "[": (1,10), "]": (1,11), "\\": (1,12),

                                                                                                                            ":": (2,9),

                "A": (2,0), "S": (2,1), "D": (2,2), "F": (2,3), "G": (2,4), "H": (2,5), "J": (2,6), "K": (2,7), "L": (2,8), ";": (2,9), "'": (2,10),

                                                                                                    "<": (3,7), ">": (3,8), "?": (3,9),

                "Z": (3,0), "X": (3,1), "C": (3,2), "V": (3,3), "B": (3,4), "N": (3,5), "M": (3,6), ",": (3,7), ".": (3,8), "/": (3,9)
            }
            check_key_position: tuple[int, int] = KEY_POSITIONS.get(check_letter.upper())
            target_key_position: tuple[int, int] = KEY_POSITIONS.get(target_letter.upper())
            #Returns 'DELETION_ERROR' if one of the keys aren't found
            if check_key_position is None or target_key_position is None:
                return DELETION_ERROR
            
            #Returns the distance after using the Pythagoras formula 
            return ((check_key_position[0] - target_key_position[0]) ** 2 + (check_key_position[1] - target_key_position[1]) ** 2) ** 0.5
        
        #Recursively backtracks through the matrix to get all the possible changes in the string
        def backtrack(x: int, y: int, curr_path: dict[str, list[tuple[int, int]]], curr_distance = 0) -> list[dict[str, list[tuple[int, int]]]]:
            #References the variable into the function
            nonlocal best_string_transform_distance
            #Prunes branches where distance is larger than the best distance
            if best_string_transform_distance != -1 and curr_distance >= best_string_transform_distance:
                return []
            cell_score: int = self.matrix[y][x]
            changes: list[dict[str, list[tuple[int, int]]]] = []
            #Base case when x and y is zero
            if x == 0 and y == 0:
                if best_string_transform_distance == -1 or curr_distance < best_string_transform_distance:
                    best_string_transform_distance = curr_distance
                return [copy.deepcopy(curr_path)]
            #Same letter
            if x > 0 and y > 0 and self.matrix[y-1][x-1] == cell_score:
                changes.extend(backtrack(x-1, y-1, curr_path, curr_distance))
            #Transposition
            if x > 1 and y > 1 and self.check_string[x-1] == self.target_string[y-2] and self.check_string[x-2] == self.target_string[y-1] and self.matrix[y-2][x-2] == cell_score - 1:
                curr_path["Transposition"].append((x-2, x-1))
                changes.extend(backtrack(x-2, y-2, curr_path, curr_distance + TRANSPOSITION_ERROR))
                curr_path["Transposition"].pop()
            #Replacement
            if x > 0 and y > 0 and self.matrix[y-1][x-1] == cell_score - 1:
                curr_path["Replacement"].append((x-1, y-1))
                #Calls backtrack again at next position
                changes.extend(backtrack(x-1, y-1, curr_path, curr_distance + (get_letter_distance(self.check_string[x-1], self.target_string[y-1]) * REPLACEMENT_MULTIPLIER)))
                curr_path["Replacement"].pop()
            #Insertion
            if y > 0 and self.matrix[y-1][x] == cell_score - 1:
                curr_path["Insertion"].append((x, y-1))
                changes.extend(backtrack(x, y-1, curr_path, curr_distance + INSERTION_ERROR))
                curr_path["Insertion"].pop()
            #Deletion
            if x > 0 and self.matrix[y][x-1] == cell_score - 1:
                curr_path["Deletion"].append((x-1, y))
                changes.extend(backtrack(x-1, y, curr_path, curr_distance + DELETION_ERROR))
                curr_path["Deletion"].pop()
            return changes
        self.change_positions = backtrack(len(self.check_string), len(self.target_string), {"Insertion": [], "Deletion": [], "Replacement": [], "Transposition": []})
        self.string_transform_distance: float = best_string_transform_distance
        return self.change_positions

#Class for node of a BK tree 
class BKNode:

    def __init__(self, word: str, distance_function: callable) -> None:
        self.word: str = word
        self.distance_function: callable = distance_function
        self.next: dict[int, BKNode] = {}

    #Adds a node to the next dict if the distance isn't used yet, else propogate down the list
    def add_node(self, node: 'BKNode') -> None:
        distance_object: Distance = self.distance_function(self.word, node.word)
        if distance_object.distance in self.next:
            #If the distance already exists, try to add it to the next node
            self.next[distance_object.distance].add_node(node)
        else:
            self.next[distance_object.distance] = node

    #Gets the nodes within the max distance of the word
    def get_close_nodes(self, word: str, max_distance: int, close_nodes: list[list['BKNode', Distance]] = None, best_string_transform_distance: float = -1) -> list[list['BKNode', Distance]]:
        if close_nodes is None:
            close_nodes = []
        #Gets the distance
        distance_object: Distance = self.distance_function(word, self.word)
        #Gets the distance bounds
        left_bound: int = distance_object.distance - max_distance
        right_bound: int = distance_object.distance + max_distance
        #Adds itself to the close_nodes list if within the max distance
        if distance_object.distance <= max_distance:
            #Runs only if distance_object is an instance of LevenshteinDistance
            if isinstance(distance_object, LevenshteinDistance):
                #Gets the changes and string transform distance
                distance_object.find_changes(best_string_transform_distance)
                if distance_object.string_transform_distance < best_string_transform_distance or best_string_transform_distance == -1:
                    best_string_transform_distance = distance_object.string_transform_distance
            close_nodes.append((self, distance_object))
        #Iterates through the tree
        for distance in self.next:
            #Runs the function on the next node if within the bounds
            if left_bound <= distance <= right_bound:
                self.next[distance].get_close_nodes(word, max_distance, close_nodes, best_string_transform_distance)
        return close_nodes
    
#Calculates the distance between two strings using insertion, deletion and replacement
def levenshtein_distance(check_string: str, target_string: str) -> LevenshteinDistance:
    #Sets both strings to lowercase
    check_string = check_string.lower()
    target_string = target_string.lower()
    #Creates the 2D matrix based on the length of both strings
    distance_matrix: list[list[int]] = [[0] * (len(check_string) + 1) for i in range(len(target_string) + 1)]
    for x in range(len(check_string) + 1):
        for y in range(len(target_string) + 1):
            #Sets the first row and column to the letter position
            if x == 0:
                distance_matrix[y][0] = y
                continue
            elif y == 0:
                distance_matrix[0][x] = x
                continue
            #If the letter is equal then set the distance to the previous diagonal distance since no changes are needed
            elif check_string[x-1] == target_string[y-1]:
                distance_matrix[y][x] = distance_matrix[y-1][x-1]
            else:
                #Gets the minimum between insertions, deletions and replacements
                distance_matrix[y][x] = 1 + min(distance_matrix[y-1][x], distance_matrix[y][x-1], distance_matrix[y-1][x-1])
            #Transposition
            if x > 1 and y > 1 and check_string[x-1] == target_string[y-2] and check_string[x-2] == target_string[y-1]:
                distance_matrix[y][x] = min(distance_matrix[y][x], distance_matrix[y-2][x-2] + 1)

    #Returns the distance instance
    return LevenshteinDistance(check_string, target_string, distance_matrix[len(target_string)][len(check_string)], distance_matrix)

#Gets the closest word based on the list of close nodes
def get_closest_word(close_nodes: list[list['BKNode', Distance]]) -> tuple[str, float]:
    #Initialises the best word and distance
    best_word: str = ""
    smallest_distance: int = -1
    #Iterates over the list and gets the word with the smallest distance
    for node, distance in close_nodes:
        if smallest_distance == -1 or distance.string_transform_distance < smallest_distance:
            smallest_distance = distance.string_transform_distance
            best_word = node.word
    return best_word, smallest_distance

#Turns a list into a BK_Tree
def list_to_BK_tree(list_to_turn: list[str]) -> BKNode:
    #Sets the root
    root: BKNode = BKNode(list_to_turn[0], levenshtein_distance)
    #Adds all the words as nodes into root
    for word in list_to_turn:
        if word == root.word: continue
        root.add_node(BKNode(word, levenshtein_distance))
    return root

if __name__ == "__main__":
    distance = levenshtein_distance("", "two")
    print(distance.find_changes())
    print(distance.string_transform_distance)

