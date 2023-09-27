from triehard import Trie, load_data, search_prefix
import numpy as np


if __name__ == "__main__":

    print("*************************************")
    print("* Serial Trie-Based Prefix Matching *")
    print("*************************************")

    trie = Trie.build_trie(load_data())  # Build trie from list of words loaded from user-specified path.
    search_prefix(trie)  # Repeatedly search for user-defined prefix.
