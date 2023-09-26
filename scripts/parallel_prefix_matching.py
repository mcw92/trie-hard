from utils import load_data, build_global_trie


if __name__ == "__main__":

    print("******************************")
    print("* Trie-Based Prefix Matching *")
    print("******************************")

    words = load_data()
    global_trie = build_global_trie(words)

    # Perform prefix matching on the global trie.
    while True:  # Repeatedly prompt user for prefix to search for.
        prefix = input("Enter prefix to search for (press ENTER to exit search): ")
        if prefix == "":
            break
        matches = global_trie.prefix_match(prefix)
        print(f"The following {len(matches)} words match the prefix '{prefix}': {matches}")