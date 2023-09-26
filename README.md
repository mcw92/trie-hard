# `triehard`: Multi-core prefix matching in Python 
![Logo](./logo.jpeg)
### What `triehard` can do for you: Match fast or die *trie*-ing

The `triehard` package provides a very basic proof-of-concept implementation of thread-parallel tries.
A global trie can be built in a thread-parallel manner by merging local tries created on data chunks of the input word 
list on all available CPU cores.

Note that this is not really optimized yet in terms of runtime performance.