from util import *
from huffman import build_huffman_tree, encode, decode, reconstruct_tree

def encode_huffman(string):
    tree = build_huffman_tree(string)
    tree.generate_codes()
    encoded_tree =convert_tree_to_bytes(tree)
    print("ENCODED TREE: ", encoded_tree)

    r = len(encoded_tree) % 8
    file_name = "compressed_" + str(r) + ".bin"
    write_binary(file_name, "wb", encoded_tree)
    encoded = encode(string)
    #extra 0 is for spacing tree from data
    write_binary(file_name, "ab", '0')
    write_binary(file_name, "ab", encoded)
    write_txt("not_compressed.txt", string)

    return encoded, tree, r

def get_original(tree, encoded):
    decoded = []
    while(len(encoded) > 0):
        char, lenght = decode(tree, encoded)
        encoded = encoded[lenght: ]
        decoded.append(char)

    return ''.join(decoded)


def start():
    string = "abracadabra"
    encoded, tree,  r = encode_huffman(string)
    print("ENCODED STRING : ", encoded)

    # original = get_original(tree, encoded)
    # print("DECODED STRING : ", original)
    encoded_tree = load_tree_from_file("compressed_" + str(r) + ".bin", r)
    print("ENCODED TREE FROM FILE : ", encoded_tree)
    reconstructed_tree = reconstruct_tree(encoded_tree)
    print_tree(tree)
    print()
    # print_tree(reconstructed_tree)

if __name__ == '__main__':
    start()