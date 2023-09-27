from typing import List, Dict


class TrieNode:
    """
    A node in the trie structure representing a single character.

    Attributes
    ----------
    value : str
        The node's values, i.e., the character represented by this node
    children : dict[str, TrieNode]
        Dictionary of a node's child nodes where keys are characters and values are respective child nodes
    is_end : bool
        Whether the node can be the end of a word
    """
    def __init__(self, char: str) -> None:
        self.value: str = char  # Character stored in this node.
        self.children: Dict[str, TrieNode] = {}  # Dict of child nodes where keys are characters and values are nodes.
        self.is_end: bool = False  # Whether this can be the end of a word.


class Trie:
    """
    The trie data structure for storing characters of words hierarchically.

    A trie is a tree-like data structure used for efficiently storing and retrieving a dynamic set of strings or keys.
    It is particularly useful for tasks involving searching, auto-completion, and dictionary-like functionality.

    Nodes in a trie represent single characters. As you traverse from the root to a leaf node along a specific path,
    you concatenate the characters along that path to form a string. Each path from the root to a leaf represents a
    unique string or key in the set.

    Attributes
    ----------
    root : TrieNode
        The trie's empty root node

    Methods
    -------
    insert(word)
        Insert a given word into the trie.
    _dfs(node, prefix, matches)
        Depth-first traversal (DFS) to explore the nodes of the trie recursively.
    prefix_match(prefix)
        Search trie for all words starting with given prefix.
    _dfs_merge(current_self, current_other)
        Recursively merge two nodes of different structure and depth.
    merge_with(other)
        Recursively merge a trie with another trie.
    get_all_keys()
        Get all keys, i.e., words stored, in the trie.
    """
    def __init__(self):
        """
        Initialize a trie structure.

        The trie has at least an empty root node which does not store any character.
        """
        self.root = TrieNode("")  # Insert empty root node.

    def insert(self, word: str) -> None:
        """
        Iteratively insert a word into the trie.

        Parameters
        ----------
        word : str
            Word to be inserted into the trie.
        """
        node = self.root  # Always start from (empty) root node.
        for char in word:  # Loop through word's characters and check if corresponding child node already exists.
            if char not in node.children:  # Child node containing character does not yet exist.
                node.children[char] = TrieNode(char)  # Add new node with that character to current node's children.
                # `node.children` is a dict where keys are characters and values are trie nodes.
            node = node.children[char]  # Update currently considered node accordingly.
        node.is_end = True  # Mark end of word for last node.

    def _dfs(self, node: TrieNode, prefix: str, matches: List[str]) -> List[str]:
        """
        Depth-first traversal (DFS) function that explores the nodes of the trie recursively, starting from a given
        node. Used in prefix matching, where you want to find all words in the trie that have a certain prefix.

        Parameters
        ----------
        node : TrieNode
            Current node in the trie that the function is exploring. It's initially called with the root node of the
            trie and then recursively called on child nodes.
        prefix : str
            Current prefix being formed while traversing the trie. Starts as an empty string and is built character by
            character as the function traverses the trie.

        matches : list[str]
            List for storing words matching the given prefix. Encountering a node marked as the end of a word during
            traversal means that the current prefix forms a valid word which is appended to the matches list.

        Returns
        -------
        list[str]
            Words matching the given prefix.
        """
        # Add word, i.e., current prefix, to matches if considered node can be the end of a word by checking its
        # `is_end` attribute. If True, the current prefix forms a valid word to be appended to the matches list.
        if node.is_end:
            matches.append(prefix)

        # Iterate over current node's child nodes. The children attribute of a node is a dict where keys
        # are characters and values are the child nodes themselves.
        for char, child in node.children.items():
            # Recursively call `_dfs` with the child node as the new node. The prefix is extended by the character
            # represented by this node, i.e., `prefix + char`, allowing to recursively explore the trie while building
            # the word represented by the prefix.
            self._dfs(child, prefix + char, matches)

        return matches  # Return words matching given prefix.

    def prefix_match(self, prefix: str) -> List[str]:
        """
        Search trie for all words starting with given prefix.

        Parameters
        ----------
        prefix : str
            Prefix

        Returns
        -------
        list[str]
            List of words matching given prefix.
        """
        node = self.root  # Start from root node.

        # Traverse the trie to the last node of the prefix
        for char in prefix:  # Loop through characters in prefix.
            if char not in node.children:  # Current char not a valid child of current node.
                return []  # No words with the given prefix found. Return empty list.
            node = node.children[char]  # Update node.

        results = []  # Initialize results lists.
        # Perform prefix matching starting from the last node of the prefix and return matches.
        return self._dfs(node, prefix, results)

    def _dfs_merge(self, current_self: TrieNode, current_other: TrieNode) -> None:
        """
        Recursively merge nodes of two tries of different structure and depth. When merging nodes, check if a character
        from the other trie exists in the self trie. If yes, recursively merge the children of those nodes.

        Parameters
        ----------
        current_self : TrieNode
            Node in first trie (self trie)
        current_other: TrieNode
            Node in second trie (other trie)
        """
        # Loop over child nodes in other trie (usually starting from root node).
        for char, other_child in current_other.children.items():
            if char in current_self.children:
                # If the character exists in 'self', recursively merge the children.
                self._dfs_merge(current_self.children[char], other_child)
            else:
                # If the character does not exist in 'self', add the 'other' node to 'self'.
                current_self.children[char] = other_child

            if other_child.is_end:
                # Update the 'self' node to mark the end of a word as well.
                current_self.children[char].is_end = True

    def merge_with(self, other: Trie) -> None:
        """
        Recursively merge with another trie of different structure and depth starting from their root nodes. Checks if a
        character from the other trie exists in the considered trie. If yes, their children are recursively merged.

        Parameters
        ----------
        other : Trie
            Other trie to merge with
        """
        if not isinstance(other, Trie):
            raise ValueError("The 'other' parameter must be an instance of Trie.")

        self._dfs_merge(self.root, other.root)

    def get_all_keys(self) -> List[str]:
        """
        Get all keys in the trie.

        Returns
        -------
        list
            A list of all keys stored in the Trie.
        """
        matches = []
        return self._dfs(self.root, "", matches)
