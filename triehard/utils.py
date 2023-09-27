import multiprocessing
import numpy as np
from typing import List, Tuple

from .trie import Trie


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


def chunk_word_list(words: List[str]):
    """
    Divide given word list into load balanced chunks according to number of available CPUs core.

    Parameters
    ----------
    words : list[str]
        list of words to chunk

    Returns
    -------
    list[list[str]]
        chunks of original word list
    """
    num_cores = multiprocessing.cpu_count()  # Determine number of available cores.
    num_words = len(words)  # Determine number of words in list.
    basis_chunk_count = num_words // num_cores  # Determine base chunk size for each process.
    remainder_chunk_count = num_words % num_cores  # Determine remainder.
    chunk_counts = basis_chunk_count * np.ones(num_cores, dtype=int)  # Construct array with each rank's chunk counts.

    if remainder_chunk_count:  # Equally distribute remainder over respective processes to balance load.
        chunk_counts[:remainder_chunk_count] += 1
    chunk_displs = np.concatenate(  # Determine displs via cumulative sum from counts.
        (np.zeros((1,), dtype=int), np.cumsum(chunk_counts, dtype=int)[:-1])
    )

    return [words[displ:displ + count] for count, displ in zip(chunk_counts, chunk_displs)]  # Return chunks.


def build_global_trie(words: List[str], threaded: bool = True) -> Tuple:
    """
    Build global trie for given list of words.

    If the number of cores exceeds the number of words in the list, the trie is built using a single core. Otherwise,
    the list is chunked across all available CPU cores. Local tries are built in parallel on each CPU core and finally
    merged into one global trie.

    Parameters
    ----------
    words : list[str]
        List of words to build trie from
    threaded : bool, optional
        Whether trie should be built using multiple threads (True) or not (False)

    Returns
    -------
    Trie
        Global trie
    bool
        Whether trie was built using multiple threads (True) or not (False)
    """
    num_cores = multiprocessing.cpu_count()  # Get number of available CPU cores.
    num_words = len(words)  # Get number of words in list.
    if num_words < num_cores:  # Only use multiple threads if number of words is larger than number of cores.
        threaded = False
        print("Build one global trie.")
        global_trie = Trie.build_trie(words)

    else:
        global_trie = Trie.build_threaded_trie(chunk_word_list(words))

    return global_trie, threaded


def search_prefix(trie: Trie) -> None:
    """
    Repeatedly search trie for words matching user-defined prefix.

    Parameters
    ----------
    trie : Trie
        Trie to search
    """
    while True:
        prefix = input("Enter prefix to search for (press ENTER to exit search): ")
        if prefix == "":
            break
        matches = trie.prefix_match(prefix)
        print(f"The following {len(matches)} words match the prefix '{prefix}': {matches}")
