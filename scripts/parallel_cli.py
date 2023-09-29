from triehard import (
    Trie,
    load_data,
    build_global_trie,
    search_prefix,
    chunk_word_list,
    search_prefix_parallel,
)


if __name__ == "__main__":
    print("***************************************")
    print("* Threaded Trie-Based Prefix Matching *")
    print("***************************************")

    # Build global trie in parallel from chunked list of words loaded from user-specified path.
    trie = Trie.build_trie_parallel(chunk_word_list(load_data()))
    search_prefix(trie)  # Repeatedly search for user-defined prefix.
