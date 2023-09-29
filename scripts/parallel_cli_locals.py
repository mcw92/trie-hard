#!/Users/marieweiel/Projects/vector/vector-venv/bin/python
from triehard import Trie, load_data, build_global_trie, chunk_word_list, search_prefix_parallel


if __name__ == "__main__":

    print("***************************************")
    print("* Threaded Trie-Based Prefix Matching *")
    print("***************************************")

    # Build local tries in parallel from chunked list of words loaded from user-specified path.
    tries = Trie.build_local_tries(chunk_word_list(load_data()))
    search_prefix_parallel(tries)  # Repeatedly search for user-defined prefix.
