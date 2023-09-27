# -*- coding: utf-8 -*-
# The __init__.py file is used to mark a directory as a Python package.
# It is used to initialize the package when it is imported.
# It can contain code that will be executed when the package is imported,
# as well as function definitions and variable assignments.
from pkg_resources import DistributionNotFound, get_distribution

try:
    # Change if project is renamed and name does not equal the package name.
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

from .trie import Trie
from .utils import load_data, chunk_word_list, build_global_trie

__all__ = [
    "Trie",
    "load_data",
    "chunk_word_list",
    "build_global_trie"
]
