import tkinter as tk
from tkinter import filedialog
from trie import Trie
import numpy as np


def browse_file() -> None:
    """
    Open a file dialog that allows the user to select a file using a graphical user interface (GUI).

    Clicking the "Browse" button in the GUI triggers the `browse_file` function.
    """
    # Open file dialog for selecting a file to open and return selected file's path as a string.
    path = filedialog.askopenfilename()
    # Clear current contents of `path_entry` widget (a text entry field) and insert selected file's path.
    path_entry.delete(0, tk.END)  # Clear current text in `path_entry` widget.
    path_entry.insert(0, path)  # Insert selected file's path into `path_entry` widget to make it visible to user.


def perform_prefix_match() -> None:
    """
    Perform prefix matching on the loaded trie using the entered prefix (when user clicks the "Search" button in GUI).

    When the "Search" button in the GUI is clicked, it triggers the `perform_prefix_match` function.
    """
    prefix = prefix_entry.get()  # Retrieve text entered by user into `prefix_entry` widget.
    if prefix:
        matches = trie.prefix_match(prefix)
        # Display results to user by updating `result_label` widget, which is a label used to display text in the GUI.
        result_label.config(text=f"The following {len(matches)} words match the prefix '{prefix}':\n{matches}")
    else:
        result_label.config(text="No prefix entered.")


def load_words() -> None:
    """
    Load words from a file into the trie global variable, allowing you to use the same loaded trie for multiple prefix searches.
    """
    path = path_entry.get()
    if not path:
        result_label.config(text="Please select a file.")
        return

    try:
        with open(path, "r") as f:
            words = f.read().split("\n")
    except FileNotFoundError as e:
        result_label.config(text=f"FileNotFoundError: The file {path} you specified could not be found.")
        return

    global trie
    trie = Trie()
    for word in words:
        trie.insert(word)

    result_label.config(text="Trie loaded successfully.")

if __name__ == "__main__":
    # Create a GUI window.
    root = tk.Tk()  # Create Tkinter main application window.
    root.title("Trie-Based Prefix Matching")  # Set title of GUI window.

    # Create widgets.
    # Labels are used for displaying text.
    # Entry fields allow users to input text.
    # Buttons provide interactive elements.
    path_label = tk.Label(root, text="Enter the path to your list of words:")
    path_entry = tk.Entry(root)
    browse_button = tk.Button(root, text="Browse", command=browse_file)
    load_button = tk.Button(root, text="Load Words", command=load_words)  # Load words from specified file when clicked.
    prefix_label = tk.Label(root, text="Enter prefix to search for:")
    prefix_entry = tk.Entry(root)
    search_button = tk.Button(root, text="Search", command=perform_prefix_match)
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
    trie = None  # This variable will hold the trie data structure after loading words from a file.

    # Start the main event loop of the GUI application.
    # It listens for user interactions and responds to events such as button clicks and text input.
    root.mainloop()
