from trie import Trie
import numpy as np

if __name__ == "__main__":

    print("******************************")
    print("* Trie-Based Prefix Matching *")
    print("******************************")

    path = input("Enter the path to your list of words (press ENTER to exit): ")
    if path == "":
        exit()
    try:
        with open(path, "r") as f:
            words = f.read() .split("\n")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: The file {path} you specified could not be found. Exiting.")
        exit()

    trie = Trie()  # Instantiate trie.

    for word in words:  # Loop through list of words to insert words into trie.
        trie.insert(word)

    while True:  # Repeatedly prompt user for prefix to search for.
        prefix = input("Enter prefix to search for (press ENTER to exit search): ")
        if prefix == "":
            break
        matches = trie.prefix_match(prefix)
        print(f"The following {len(matches)} words match the prefix '{prefix}': {matches}")
