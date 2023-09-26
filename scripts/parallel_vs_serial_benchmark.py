import time
import multiprocessing
from typing import List

from triehard.utils import load_data, chunk_word_list, build_trie
from triehard.trie import Trie


def build_serial_trie(words: List[str]) -> Trie:
    """
    Build global trie serially using a single CPU core.

    Parameters
    ----------
    words : list[str]
        List of words to build the trie from

    Returns
    -------
    Trie
        Global trie for that list of words
    """
    global_trie = Trie()
    for word in words:  # Loop through list of words to insert words into trie.
        global_trie.insert(word)
    return global_trie


def build_threaded_trie(words: List[str]) -> Trie:
    """
    Build global trie by merging local tries built in a thread-parallel manner using all available CPU cores.

    Parameters
    ----------
    words : list[str]
        List of words to build the trie from

    Returns
    -------
    Trie
        Global trie for that list of words
    """
    global_trie = Trie()
    chunks = chunk_word_list(words)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    local_tries = pool.map(build_trie, chunks)
    for local_trie in local_tries:
        global_trie.merge_with(local_trie)
    return global_trie


if __name__ == "__main__":

    print("******************************")
    print("* Trie-Based Prefix Matching *")
    print("******************************")

    words = load_data()

    start = time.perf_counter()
    build_serial_trie(words)
    elapsed_serial = time.perf_counter() - start
    print(f"Serial case using one CPU core took {elapsed_serial} s.")

    start = time.perf_counter()
    build_threaded_trie(words)
    elapsed_parallel = time.perf_counter() - start
    print(f"Parallel case using all available CPU cores took {elapsed_parallel} s.")
