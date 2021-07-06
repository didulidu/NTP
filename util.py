import os
import io
import time

"""
Functions for writing and reading from binary files as well as from txt files.
Functions for converting string to byte array as well as for encoding huffman tree to byte array
"""

def convert_to_bytes(string):
    """
    convert_to_bytes: converts string to byte array

    :param string: string to be converted (string)
    :return: return byte array representation of given string
    """
    b = bytearray()
    for i in range(0, len(string), 8):
        b.append(int(string[i:i+8], 2))
    return bytes(b)

def write_binary(file_name, mode, string):
    """
    write_binary: opens binary file and write string as byte array to it

    :param file_name: name of binary file, must have .bin extension (string)
    :param mode: mode for opening file accepted values are wb or ab
    :param string: string that will be written to file (string)
    :return: return nothing
    """
    filename, file_extension = os.path.splitext(file_name)
    if (file_extension != ".bin"):
        raise IOError("File must be binary!")
    if (mode not in ["ab", "wb"]):
        raise ValueError("Mode is not correct!")
    with open(file_name, mode) as writer:
        writer.write(convert_to_bytes(string))

def write_txt(file_name, string):
    """
    write_txt: opens txt file and write string

    :param file_name: name of txt file, must have .txt extension (string)
    :param string: string that will be written to file (string)
    :return: return nothing
    """
    filename, file_extension = os.path.splitext(file_name)
    if (file_extension != ".txt"):
        raise IOError("File must be txt!")
    with io.open(file_name, "w", encoding="utf-8") as writer:
        writer.write(string)

def convert_tree_to_bytes(tree):
    """
    convert_tree_to_bytes: converts Huffman tree to it's byte representation
    Each leaf is coded with 1 and all other nodes are coded with 0
    For each leaf bit 1 is followed by ASCII representation of character stored in that leaf

    :param tree: root node of Huffman tree (Node)
    :return: return byte array representation of Huffman tree
    """
    if (tree.is_leaf()):
        return '1' + bin(ord(tree.char))[2:]
    else:
        return '0' + convert_tree_to_bytes(tree.left) + convert_tree_to_bytes(tree.right)

def print_tree(node, level=0):
    """
    print_tree: prints Huffman tree with levels
    :param node: root node of Huffman tree (Node)
    :param level: level of node (root is 0 level and so on) (int)
    :return: return nothing
    """
    if node != None:
        if (node.char):
            print(' ' * 4 * level + '->', node.char, " kod: ", node.code)
        else:
            print(' ' * 4 * level + '->', node.frequency)
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)

def load_tree_from_file(file_name, r):
    """
    load_tree_from_file: loads bytes representation of Huffman tree from binary file
    :param file_name: name of binary file containing tree (string)
    :param r: rest from dividing length of tree (bit number) with 8 (one byte is 8 bits)
    represents length of last byte
    :return: return string representation of tree (string)
    """
    filename, file_extension = os.path.splitext(file_name)
    if (file_extension != ".bin"):
        raise IOError("File must be binary!")
    with open(file_name, "rb") as reader:
        encoded_tree = []
        while True:
            byte_s = reader.read(1)
            if not byte_s:
                break
            byte = byte_s[0]
            bits = bin(byte)[2:]
            if (bits == '0'):
                break
            while (len(bits) < 8):
                bits = '0' + bits
            encoded_tree.append(bits)
            last_bits = bits

    #remove zeros from last byte if it's length was less than 8
    if (r < 8):
        while (len(last_bits) != r):
            last_bits = last_bits[1:]
        encoded_tree[len(encoded_tree) - 1] = last_bits

    return ''.join(encoded_tree)


def save(output_file_name, r, encoded_tree, encoded):
    """
    save: save to file encoded tree with encoded data
    Changes name of file, name must contain number of bits in last written byte
    :param output_file_name: prefix of output file name, contains name of original file followed by _compressed_ (string)
    :param r: number of bits in last written byte (int)
    :param encoded_tree: Huffman's tree encoded to 1 and 0 (string)
    :param encoded: encoded input text (string)
    :return: return nothing
    """
    output_file_name += str(r) + ".bin"
    write_binary(output_file_name, "wb", encoded_tree)
    #extra 0 is for spacing tree from data
    write_binary(output_file_name, "ab", '0')
    write_binary(output_file_name, "ab", encoded)


def calculate_time(func):
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):
        # storing time before function execution
        begin = time.time()

        result = func(*args, **kwargs)

        # storing time after function execution
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)

        return result

    return inner1
