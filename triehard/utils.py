import multiprocessing
import numpy as np
from typing import List, Tuple

from .trie import Trie


def build_trie(words: List[str]) -> Trie:
    """
    Build trie data structure from given list of words.

    Parameters
    ----------
    words : list[str]
        List of words to build trie from

    Returns
    -------
    Trie
        The respective trie data structure
    """
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def load_data() -> List[str]:
    """
    Load data from user-prompted path.

    Returns
    -------
    list[str]
        List of words loaded from path
    """
    path = input("Enter the path to your list of words (press ENTER to exit): ")
    if path == "":
        exit()
    try:
        with open(path, "r") as f:
            words = f.read().split("\n")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: The file {path} you specified could not be found. Exiting.")
        exit()
    return words


def chunk_word_list(words):
    """
    Divide given word list into load balanced chunks according to number of available CPUs core.

    Parameters
    ----------
    num_cores :
    words : list[str]

    Returns
    -------
    list[list[str]]
        chunks of original word list
    """
    num_cores = multiprocessing.cpu_count()
    num_words = len(words)
    basis_chunk_count = num_words // num_cores  # Determine base chunk size for each process.
    remainder_chunk_count = num_words % num_cores  # Determine remainder
    chunk_counts = basis_chunk_count * np.ones(num_cores, dtype=int)  # Construct array with each rank's chunk counts.

    if remainder_chunk_count:  # Equally distribute remainder over respective processes to balance load.
        chunk_counts[:remainder_chunk_count] += 1
    chunk_displs = np.concatenate(  # Determine displs via cumulative sum from counts.
        (np.zeros((1,), dtype=int), np.cumsum(chunk_counts, dtype=int)[:-1])
    )

    return [words[displ:displ + count] for count, displ in zip(chunk_counts, chunk_displs)]


def build_global_trie(words: List[str]) -> Tuple[Trie, bool]:
    """
    Build global trie for given list of words.

    If the number of words in the list exceeds the number of CPU cores available, the list is chunked across all
    available CPU cores. Local tries are built in parallel on each CPU core and finally merged into
    one global trie.

    Parameters
    ----------
    words : list[str]
        List of words to build trie from

    Returns
    -------
    Trie
        Global trie
    """
    num_cores = multiprocessing.cpu_count()
    num_words = len(words)
    global_trie = Trie()
    if num_words < num_cores:
        parallel = False
        print("Build one global trie.")
        for word in words:  # Loop through list of words to insert words into trie.
            global_trie.insert(word)
    else:
        parallel = True
        chunks = chunk_word_list(words)
        pool = multiprocessing.Pool(processes=num_cores)
        local_tries = pool.map(build_trie, chunks)
        for local_trie in local_tries:
            global_trie.merge_with(local_trie)

    return global_trie, parallel
