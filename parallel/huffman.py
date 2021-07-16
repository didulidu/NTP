import heapq
import time
from collections import Counter
from multiprocessing import *
import sys
sys.path.append('../../NTP')
from util import calculate_time


"""
Huffman coding tree represented with Node class
For leaf left, right and frequency fields are set to None
Non leaft nodes have char and frequency fields set to None

Codes are generated after tree is built and saved to global dictionary named codes
"""

class Node:
    def __init__(self, left=None, right=None, char=None, frequency=0, code=''):
        """
        Construct a new 'Node' object.

        :param left: The left child (Node)
        :param right: The right child (Node)
        :param char: The character of node (char)
        :param frequency: The frequency of char in document (int)
        :param code: String representation of huffman code, example : '110' (String)
        :return: returns nothing
        """
        self.left = left
        self.right = right
        self.char = char
        self.frequency = frequency
        self.code = code

    def is_leaf(self):
        """
        is_leaf checks if node is has children or no
        :return: true or false weather node is leaf
        """
        return self.left == None and self.right == None

    def __lt__(self, other):
        """
        __lt__ overrides parameter < when comparing to another node
        :return: true if node frequency is less then other node's frequency
        """
        return self.frequency < other.frequency

    def generate_codes(self):
        """
        generate_codes generate huffman code for each node in tree, after tree is built,
        changes attribute code of each node in tree
        all codes are saved to global dict named codes
        :return: return nothing
        """
        if (self.char):
            return
        else:
            self.left.code = self.code + '0'
            self.right.code = self.code + '1'
            self.left.generate_codes()
            self.right.generate_codes()

# leafs = {}

# def collect_leafs(tree):
#     if (tree.is_leaf()):
#         leafs[tree.code] = char
#         return
#     with Pool() as pool:
#         pool.map(collect_leafs, [tree.left, tree.right])

# @calculate_time
# def collect_leafs_timer(tree):
#     collect_leafs(tree)
def chunks(lst, n):
    list =  []
    for i in range(0, len(lst), n):
        list.append(lst[i:i + n])
    return list

@calculate_time
def get_frequency(string):
    """
    calc_frequencies: calculates frequency of every character in given string in parallel
    Divides given text into CHUNK_NUMBER parts and calcs frequencies for each chunk in parallel
    Combining result is sequential

    :param string: input text  (string)
    :return: returns frequency of every char in string (dictionary)
    """
    size = len(string)
    n = size // cpu_count()
    if (n == 0 ):
        n = size
    string_parts = chunks(string, size)

    with Pool() as pool:
        counters = pool.map(count_frequency, string_parts)
    frequency = Counter({})
    for counter in counters:
        frequency += counter

    return frequency

def count_frequency(string_part):
    """
    calc_frequencies: calculates frequency of every character in given string part

    :param string: part of input text  (string)
    :return: returns frequency of every char in given string part (Counter)
    """
    frequency = Counter({})
    for c in string_part:
        if c in frequency.keys():
            frequency[c] += 1
        else:
            frequency[c] = 1

    return frequency

@calculate_time
def build_huffman_tree(string):
    """
    build_huffman_tree creates huffman tree for given string,
    uses heap implementation of priority queue

    :param string: input text for compression (string)
    :return: returns root of huffman tree (Node)
    """
    frequency = get_frequency(string)
    heap = []
    for c in frequency.keys():
        root = Node(None, None, c, frequency[c])
        heapq.heappush(heap, root)

    while len(heap) > 1:
        smallest = heapq.heappop(heap)
        second_smallest = heapq.heappop(heap)
        root = Node(smallest, second_smallest, None, smallest.frequency + second_smallest.frequency)
        heapq.heappush(heap, root)

    return heapq.heappop(heap)

def find_code(tree, c):
    if (tree.is_leaf()):
        if(tree.char == c):
            return tree.code
        else:
            return False
    left =  find_code(tree.left, c) 
    if (left):
        return left

    right = find_code(tree.right, c) 
    if(right):
        return right
    
def encode(string, tree):
    """
    encode : encode given string from codes dictionary

    :param string: input text for compression (string)
    :return: returns encoded string (string)
    """
    list = []
    for c in string:
        list.append(find_code(tree, c))
    return ''.join(list)

def decode_timer(tree, encoded, index=0, length=0):
    return decode(tree, encoded, index, length)

def decode(tree, encoded, index = 0, length = 0):
    """
    decode: finds sequence in encoded string that represents one character
    Finds path from root to leaf in tree

    :param tree: root of Huffman tree (Node)
    :param encoded: encoded representation of text (string)
    :param index: index of current character in text (int)
    :param length: length of char sequence that represents one Huffman code (int)
    :return: returns one character (char)
    """
    if len(encoded) == 0:
        return
    if tree.is_leaf():
        return tree.char, length
    elif encoded[index] == '0':
        return decode(tree.left, encoded, index + 1, length + 1)
    elif encoded[index] == '1':
        return decode(tree.right, encoded, index + 1, length + 1)

@calculate_time
def get_original(tree, encoded):
    """
    get_original: convert encoded document to original form

    :param tree: root of Huffman tree (Node)
    :param encoded: encoded representation of text (string)
    :return: returns original text (string)
    """
    decoded = []
    while(len(encoded) > 0):
        char, lenght = decode_timer(tree, encoded)
        encoded = encoded[lenght: ]
        decoded.append(char)

    return ''.join(decoded)

