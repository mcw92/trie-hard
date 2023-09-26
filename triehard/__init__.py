# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound, get_distribution

try:
    # Change here if project is renamed and does not equal the package name
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