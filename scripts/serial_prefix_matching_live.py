import tkinter as tk
from tkinter import filedialog, StringVar
from trie import Trie
import numpy as np

def browse_file():
    path = filedialog.askopenfilename()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)

def perform_prefix_match(trie, prefix_var):
    if trie is None:
        result_label.config(text="Trie not loaded.")
        return

    prefix = prefix_var.get()
    if prefix:
        matches = trie.prefix_match(prefix)
        matches_str = "\n".join(matches)
        result_label.config(text=f"The following {len(matches)} words match the prefix '{prefix}': \n{matches_str}")
    else:
        result_label.config(text="No prefix entered.")


def load_words():
    path = path_entry.get()
    if not path:
        result_label.config(text="Please select a file.")
        return

    try:
        with open(path, "r") as f:
            words = f.read() .split("\n")
    except FileNotFoundError as e:
        result_label.config(text=f"FileNotFoundError: The file {path} you specified could not be found.")
        return

    global trie
    trie = Trie()
    for word in words:
        trie.insert(word)

    result_label.config(text="Trie loaded successfully.")


def on_prefix_entry_change(event):
    perform_prefix_match(trie, prefix_var)


if __name__ == "__main__":
    # Create a GUI window
    root = tk.Tk()
    root.title("Trie-Based Prefix Matching")

    # Create widgets
    path_label = tk.Label(root, text="Enter the path to your list of words:")
    path_entry = tk.Entry(root)
    browse_button = tk.Button(root, text="Browse", command=browse_file)
    load_button = tk.Button(root, text="Load Words", command=load_words)
    prefix_label = tk.Label(root, text="Enter prefix to search for:")
    prefix_var = StringVar()
    prefix_entry = tk.Entry(root, textvariable=prefix_var)
    search_button = tk.Button(root, text="Search")
    result_label = tk.Label(root, text="")

    # Arrange widgets top-down in the window.
    path_label.pack()
    path_entry.pack()
    browse_button.pack()
    load_button.pack()
    prefix_label.pack()
    prefix_entry.pack()
    search_button.pack()
    result_label.pack()

    # Initialize the trie.
    trie = None

    # Event handlers
    load_button.config(command=lambda: load_words())
    search_button.config(command=lambda: perform_prefix_match(trie, prefix_var))

    # Bind the KeyRelease event to prefix_entry
    prefix_entry.bind("<KeyRelease>", on_prefix_entry_change)

    # Start the main event loop of the GUI application.
    # It listens for user interactions and responds to events such as button clicks and text input.
    root.mainloop()
