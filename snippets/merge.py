from trie import Trie

# Usage example:
trie1 = Trie()
trie1.insert("apple")
trie1.insert("banana")

trie2 = Trie()
trie2.insert("apple")
trie2.insert("cherry")

print(trie1.get_all_keys())
print(trie2.get_all_keys())
# Merge trie2 into trie1 with a specific merge strategy
trie1.merge_with(trie2)
# Get all keys in the merged Trie
print(trie1.get_all_keys())
