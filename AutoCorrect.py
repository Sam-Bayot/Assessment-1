#File: AutoCorrect.py
#Description: This file is used to check if a string is similar to a target string
# and if so, give the distance between the strings
#Author: Sam Bayot
#Last Modified: 19/03/26

import BiClass
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
    def find_changes(self) -> list[dict[str, list[tuple[int, int]]]]:

        #Recursively backtracks through the matrix to get all the possible changes in the string
        def backtrack(x: int, y: int, curr_path: dict[str, list[tuple[int, int]]]) -> None:
            cell_score: int = self.matrix[y][x]
            changes: list[dict[str, list[tuple[int, int]]]] = []
            #Base case when x and y is zero
            if x == 0 and y == 0:
                return [curr_path]
            #Same letter
            if x > 0 and y > 0 and self.matrix[y-1][x-1] == cell_score:
                changes.extend(backtrack(x-1, y-1, curr_path))
            #Replacement
            if x > 0 and y > 0 and self.matrix[y-1][x-1] == cell_score - 1:
                new_path: list[dict[str, list[tuple[int, int]]]] = copy.deepcopy(curr_path)
                new_path["Replacement"].append((x-1, y-1))
                #Calls backtrack again at next position
                changes.extend(backtrack(x-1, y-1, new_path))
            #Insertion
            if y > 0 and self.matrix[y-1][x] == cell_score - 1:
                #Deep copies curr_changes so that no list or dict is a reference
                new_path: list[dict[str, list[tuple[int, int]]]] = copy.deepcopy(curr_path)
                new_path["Insertion"].append((x, y-1))
                changes.extend(backtrack(x, y-1, new_path))
            #Deletion
            if x > 0 and self.matrix[y][x-1] == cell_score - 1:
                new_path: list[dict[str, list[tuple[int, int]]]] = copy.deepcopy(curr_path)
                new_path["Deletion"].append((x-1, y))
                changes.extend(backtrack(x-1, y, new_path))
            return changes
        
        self.change_positions = backtrack(len(self.check_string), len(self.target_string), {"Insertion": [], "Deletion": [], "Replacement": []})
        return self.change_positions
    
#Class for node of a BK tree 
class BKNode:

    def __init__(self, word: str, distance_function: callable) -> None:
        self.word: str = word
        self.distance_function: callable = distance_function
        self.next: dict[int, BKNode] = {}

    #Adds a node to the next dict if the distance isn't used yet, else propogate down the list
    def add_node(self, node: 'BKNode') -> None:
        distance_object: Distance = self.distance_function(self.word.lower(), node.word.lower())
        if distance_object.distance in self.next:
            #If the distance already exists, try to add it to the next node
            self.next[distance_object.distance].add_node(node)
        else:
            self.next[distance_object.distance] = node

    #Gets the nodes within the max distance of the word
    def get_close_nodes(self, word: str, max_distance: int, closest_words: dict[int, list['BKNode', Distance]] = {}) -> dict[int, ['BKNode', Distance]]:
        #Gets the distance bounds
        distance_object: Distance = self.distance_function(word.lower(), self.word.lower())
        if isinstance(distance_object, LevenshteinDistance): distance_object.find_changes()
        left_bound: int = distance_object.distance - max_distance
        right_bound: int = distance_object.distance + max_distance
        #Adds itself if within the max distance
        if distance_object.distance <= max_distance:
            #Creates a new list if distance key doesn't exist yet
            if distance_object.distance in closest_words:
                closest_words[distance_object.distance].append((self, distance_object))
            else:
                closest_words[distance_object.distance] = [(self, distance_object)]
        #Iterates through the tree
        for distance in self.next:
            #Runs the function on the next node if within the bounds
            if distance > left_bound and distance < right_bound:
                self.next[distance].get_close_nodes(word, max_distance, closest_words)
        return closest_words
    
#Calculates the distance between two strings using insertion, deletion and replacement
def levenshtein_distance(check_string: str, target_string: str) -> LevenshteinDistance:
    
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

    #Returns the distance instance
    return LevenshteinDistance(check_string, target_string, distance_matrix[len(target_string)][len(check_string)], distance_matrix)

#Turns a BiList into a BK_Tree
def bi_list_to_BK_tree(bi_list: BiClass.BiList[str]) -> BKNode:
    #Sets the root
    root: BKNode = BKNode(bi_list[0], levenshtein_distance)
    #Adds all the words as nodes into root
    for word in bi_list:
        if word == root.word: continue
        root.add_node(BKNode(word, levenshtein_distance))
    return root

if __name__ == "__main__":
    distance = levenshtein_distance("train", "zain")
    distance.find_changes()
    print(distance.change_positions)

