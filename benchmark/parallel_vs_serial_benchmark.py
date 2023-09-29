import time
import multiprocessing
from typing import List

from triehard import load_data, chunk_word_list, Trie, _search_prefix_parallel

# TODO: Write context manager for measuring execution times.

if __name__ == "__main__":
    print("**************************************************************")
    print("* Trie-Based Prefix Matching Benchmark : Serial vs. Threaded *")
    print("**************************************************************")

    words = load_data()
    prefix = input("Enter prefix to search for (press ENTER to exit search): ")

    start = time.perf_counter()
    serial_trie = Trie.build_trie(words)
    elapsed_build_serial = time.perf_counter() - start
    start = time.perf_counter()
    serial_trie.prefix_match(prefix)
    elapsed_match_serial = time.perf_counter() - start
    print(f"Serial case using one CPU core: Building trie took {elapsed_build_serial} s, "
          f"prefix matching took {elapsed_match_serial} s.")

    start = time.perf_counter()
    parallel_trie = Trie.build_trie_parallel(chunk_word_list(words))
    elapsed_build_merged = time.perf_counter() - start
    start = time.perf_counter()
    parallel_trie.prefix_match(prefix)
    elapsed_match_merged = time.perf_counter() - start
    print(f"Parallel case using all available CPU cores: Building and merging trie took {elapsed_build_merged} s, "
          f"prefix matching took {elapsed_match_merged} s.")

    start = time.perf_counter()
    tries = Trie.build_local_tries(chunk_word_list(words))
    elapsed_build_parallel = time.perf_counter() - start
    start = time.perf_counter()
    _search_prefix_parallel(tries, prefix)  # Repeatedly search for user-defined prefix.
    elapsed_match_parallel = time.perf_counter() - start
    print(f"Parallel case using all available CPU cores: Building local tries took {elapsed_build_parallel} s, "
          f"prefix matching using local tries in parallel and merging matches took {elapsed_match_parallel} s.")
