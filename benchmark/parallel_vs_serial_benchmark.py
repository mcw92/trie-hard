import time
import multiprocessing
from typing import List

from triehard import load_data, chunk_word_list, Trie


if __name__ == "__main__":

    print("**************************************************************")
    print("* Trie-Based Prefix Matching Benchmark : Serial vs. Threaded *")
    print("**************************************************************")

    words = load_data()

    start = time.perf_counter()
    serial_trie = Trie.build_trie(words)
    elapsed_serial = time.perf_counter() - start
    print(f"Serial case using one CPU core to build trie took {elapsed_serial} s.")

    start = time.perf_counter()
    threaded_trie = Trie.build_threaded_trie(chunk_word_list(words))
    elapsed_parallel = time.perf_counter() - start
    print(f"Parallel case using all available CPU cores to build trie took {elapsed_parallel} s.")

    # print(f"Words in serial trie: {serial_trie.get_all_keys()}")
    # print(f"Words in threaded trie: {threaded_trie.get_all_keys()}")
