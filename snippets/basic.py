import time

import numpy as np
from typing import Union, List
import multiprocessing as mp
from mpi4py import MPI


class PrefixMatcher:
    def __init__(
        self, list_of_words: Union[List[str], np.ndarray[str]], prefix: str
    ) -> None:
        self.list_of_words = list_of_words
        self.prefix = prefix

    @staticmethod
    def find_matches_numpy_core(
        list_of_words: np.ndarray[str], prefix: str
    ) -> np.ndarray[str]:
        """
        Get words matching given prefix using NumPy's `np.core.defchararray.startswith` method.

        When working with a large dataset of strings, you can use NumPy to perform element-wise string operations.
        NumPy's `np.core.defchararray.startswith` allows you to check if a NumPy array of strings starts with
        a specified string efficiently. The result will be a Boolean NumPy array indicating whether each string in
        strings_array starts with the specified_string. This can be more efficient than using lists when
        working with large arrays of strings.

        Returns
        -------
        numpy.ndarray
            numpy array of prefix matches
        """
        return list_of_words[np.core.defchararray.startswith(list_of_words, prefix)]

    # @staticmethod


def find_matches_list_comprehension(
    prefix: str,
    list_of_words: np.ndarray[str],
) -> np.ndarray[str]:
    """
    Get words matching given prefix using list comprehension.

    Returns
    -------
    numpy.ndarray
        numpy array of prefix matches
    """
    return list_of_words[[s.startswith(prefix) for s in list(list_of_words)]]


if __name__ == "__main__":
    path = "./words.txt"
    prefix = "th"
    rng = np.random.default_rng(seed=0)

    list_of_words = np.loadtxt(
        path, dtype=str, comments="#"
    )  # Load list of words from txt file.
    rng.shuffle(list_of_words)  # Shuffle list.

    cpu_count = mp.cpu_count()  # Get number of CPUs available.
    pool = mp.Pool(
        processes=cpu_count
    )  # Create a process pool with the number of CPU cores available.

    # Split the string_list into chunks for parallel processing
    chunk_size = len(list_of_words) // cpu_count
    chunks = [
        list_of_words[i : i + chunk_size]
        for i in range(0, list_of_words.shape[0], chunk_size)
    ]

    # Use the pool.map() function to apply the function to each chunk in parallel.
    results = pool.starmap(
        find_matches_list_comprehension, [(prefix, chunk) for chunk in chunks]
    )
    print(results)
    # Flatten the results list
    # flattened_results = [item for sublist in results for item in sublist]

    pool.close()
    pool.join()

    # matcher = PrefixMatcher(list_of_words=list_of_words, prefix=prefix)
    # start_time = time.perf_counter()
    # matches = matcher.find_matches_numpy_core()
    # elapsed = time.perf_counter() - start_time
    # print(matches, elapsed)
    # start_time = time.perf_counter()
    # matches = matcher.find_matches_list_comprehension()
    # elapsed = time.perf_counter() - start_time
    # print(matches, elapsed)
