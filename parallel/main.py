from multiprocessing import *
import time
import sys
sys.path.append('../../NTP')
from util import *
from huffman import *

@calculate_time
def generate_codes_timer(tree):
    tree.generate_codes()

@calculate_time
def convert_tree_to_bytes_timer(tree):
    return convert_tree_to_bytes(tree)

def chunks(lst, n, tree):
    list =  []
    for i in range(0, len(lst), n):
        list.append((lst[i:i + n], tree))
    return list

@calculate_time
def encode_huffman(string):
    tree = build_huffman_tree(string)
    generate_codes_timer(tree)
    encoded_tree = convert_tree_to_bytes_timer(tree)
    r = len(encoded_tree) % 8
    string_parts = chunks(string, len(string)//cpu_count(), tree)
 
    with Pool() as pool:
        results = pool.starmap(encode, string_parts)   
    
    return ''.join(results), tree, r, encoded_tree

def start():
    if len(sys.argv) == 1:
        print("[ERROR] Path to txt document is required.")
        sys.exit()
    else:
        file_name = sys.argv[1]

    print("Compressing file: ", file_name)
    output_file_name = file_name.replace(".txt", "") + "_compressed_"
    with open(file_name, "r") as reader:
        document = reader.read()

    start_time = time.time()
    encoded, tree,  r, encoded_tree = encode_huffman(document)
    save(output_file_name, r, encoded_tree, encoded)

    original = get_original(tree, encoded)

    if (original == document):
        print("MATCHES")
    else:
        print("ERROR")
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")

if __name__ == '__main__':
    start()