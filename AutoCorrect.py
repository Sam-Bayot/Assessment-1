#File: AutoCorrect.py
#Description: This file is used to check if a string is similar to a target string
# and if so, give the distance between the strings
#Author: Sam Bayot
#Last Modified: 19/03/26

import BiClass

#Class for node of a BK tree
class BKNode:

    def __init__(self, word: str, distance_function: callable):
        self.word: str = word
        self.distance_function: callable = distance_function
        self.next: dict[int, BKNode] = {}

    #Adds a node to the next dict if the distance isn't used yet, else propogate down the list
    def add_node(self, node: 'BKNode'):
        distance: int = self.distance_function(self.word, node.word)
        if distance in self.next:
            #If the distance already exists, try to add it to the next node
            self.next[distance].add_node(node)
        else:
            self.next[distance] = node

    #Gets the nodes within the max distance of the word
    def get_close_nodes(self, word: str, max_distance: int, closest_words: dict[int, list['BKNode']] = {}) -> dict[int, 'BKNode']:
        #Gets the distance bounds
        distance: int = self.distance_function(self.word.lower(), word.lower())
        left_bound: int = distance - max_distance
        right_bound: int = distance + max_distance
        #Adds itself if within the max distance
        if distance <= max_distance:
            #Creates a new list if distance key doesn't exist yet
            if distance in closest_words:
                closest_words[distance].append(self)
            else:
                closest_words[distance] = [self]
        #Iterates through the tree
        for distance in self.next:
            #Runs the function on the next node if within the bounds
            if distance > left_bound and distance < right_bound:
                closest_words = self.next[distance].get_close_nodes(word, max_distance, closest_words)
        return closest_words

#Calculates the distance between two strings using insertion, deletion and replacement
def levenshtein_distance(check_string: str, target_string: str) -> int:
    #Creates the 2D matrix based on the length of both strings
    distance_matrix: list[list[int]] = [[0] * (len(check_string) + 1) for i in range(len(target_string) + 1)]
    for i in range(len(target_string) + 1):
        for j in range(len(check_string) + 1):
            #Sets the first row and column to the letter position
            if i == 0:
                distance_matrix[0][j] = j
                continue
            elif j == 0:
                distance_matrix[i][0] = i
                continue
            #If the letter is equal then set the distance to the previous diagonal distance since no changes are needed
            elif check_string[j-1] == target_string[i-1]:
                distance_matrix[i][j] = distance_matrix[i-1][j-1]
            else:
                #Gets the minimum between insertions, deletions and replacements
                distance_matrix[i][j] = 1 + min(distance_matrix[i-1][j], distance_matrix[i][j-1], distance_matrix[i-1][j-1])

    #Returns the last value in the matrix which is the distance
    return distance_matrix[len(target_string)][len(check_string)]

#Turns a BiList into a BK_Tree
def bi_list_to_BK_tree(bi_list: BiClass.BiList[str]) -> BKNode:
    #Sets the root
    root: BKNode = BKNode(bi_list[0], levenshtein_distance)
    #Adds all the words as nodes into root
    for word in bi_list:
        if word == root.word: continue
        root.add_node(BKNode(word, levenshtein_distance))
    return root


