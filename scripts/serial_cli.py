from triehard import Trie, load_data, search_prefix
import numpy as np


if __name__ == "__main__":

    print("*************************************")
    print("* Serial Trie-Based Prefix Matching *")
    print("*************************************")

    words = load_data()  # Load list of words from user-specified path.
    trie = Trie.build_trie(words)  # Instantiate trie.
    search_prefix(trie)  # Repeatedly search for user-defined prefix.
