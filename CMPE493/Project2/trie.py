import os

#
# REFERENCE: https://albertauyeung.github.io/2020/06/15/python-trie.html
#

"""
    Defines the node structure for trie.
    Fields:
        char: Character - The character stored in this node.
        is_word: Boolean - If this node represents the end of a word or not.
        children: Dictionary - The dictionary that stores the child nodes.
            Key: Character
            Value: Node()
"""
class Node():
    def __init__(self,char):
        # character stored in this node
        self.char = char
        # whether this node is a word or not
        self.is_word = False
        # a dictionary that keeps the child nodes
        # dict: keys are characters, values are nodes
        self.children = dict()

"""
    Defines the trie structure.
"""
class Trie(object):
    def __init__(self):
        self.root = Node('')

    # Inserts a node into the trie.
    def insert(self,word):
        current = self.root
        for char in word:
            if char in current.children:
                current = current.children[char]
            else:
                current.children[char] = Node(char)
                current = current.children[char]
        current.is_word = True

    # Returns the output of a query.
    # Arguments:
    #   prefix: String - The string of prefix
    # Returns:
    #   List of words that are stored with that prefix in the trie.
    def query(self,prefix):
        self.query_output = list()
        current = self.root
        # Check if the prefix is in the trie
        for char in prefix:
            if char in current.children:
                current = current.children[char]
            else: # No prefix found!
                return []
        self.dfs(current,prefix)
        return self.query_output

    #
    # Performs dfs algorithm on a given node. The function recursively calls for all
    # children of a node until the currently called node has no children. The function
    # adds the valid words in the path into the query_output list.
    #
    def dfs(self,node,current_word):
        if node.is_word == True:
            self.query_output.append(current_word)
        for child in node.children.values():
            self.dfs(child, current_word+child.char)

"""
    Searches whether a previously saved trie (.pickle) file exists in the given name.
    Arguments:
        file_name: Name of file to be searched.
    Returns:
        Boolean
"""
def search_trie(file_name):
    return os.path.exists(file_name)