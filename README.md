# `triehard`: Multi-core prefix matching in Python 
![Logo](./logo.jpeg)
*Created with [ideogram.ai](https://ideogram.ai/).*
## What `triehard` can do for you: Match fast or die *trie*-ing

The `triehard` package provides a very basic proof-of-concept implementation of thread-parallel tries.
A global trie can be built in a thread-parallel manner by merging local tries created on data chunks of the input word 
list on all available CPU cores.
Furthermore, it offers a GUI-based live search for prefix matching on said tries.

Note that this is not really optimized yet in terms of runtime performance.

## What you find here

- `data/`: Exemplary lists of new-line separated words as text files.
  - `words_10.txt`: Small list of 10 words that I like for debugging
  - `words_1k.txt`: Lexicographically sorted list of 1000 most frequent English words, taken from [ef.com/wwen/english-resources/english-vocabulary/top-1000-words/](https://www.ef.com/wwen/english-resources/english-vocabulary/top-1000-words/) on 2023-09-23 at 18:25.
  - `words_1k_shuffled.txt`: The same as above but in random order.
  - `words_400k.txt`: Lexicographically sorted list of 370,105 English words taken from [github.com/dwyl/english-words/blob/master/words_alpha.txt](https://github.com/dwyl/english-words/blob/master/words_alpha.txt) on 2023-09-26 at 09:15.
  - `words_400k_shuffled.txt`: The same as above but in random order.


- `triehard/`: The package containing the actual implementations
  - `trie.py`: The trie data structure
  - `utils.py`: Utility functions
  - `gui.py`: A basic graphical user interface


- `scripts/`: Exemplary usage scripts
  - `serial_cli.py`: Serial trie-based prefix matching with command-line interface
  - `parallel_cli.py`: Thread-parallel trie-based prefix matching with CLI
  - `parallel_gui.py`: Thread-parallel trie-based prefix matching with graphical user interface
  - `parallel_live.py`: Thread-parallel trie-based prefix matching with live search and GUI
 
- `benchmark/`: Scripts to benchmark the implementations

- `snippets/`: Potentially useful code snippets (not relevant for users).
- `tests/`: This folder will maybe contain unit and integration test in the future.

## Installation
To install the `triehard` package, clone this repo and run `pip install -e .` or `python setup.py install`.