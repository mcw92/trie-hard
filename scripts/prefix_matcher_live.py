import tkinter as tk # Standard library for creating graphical user interfaces in Python
from tkinter import filedialog, StringVar
from triehard import build_global_trie, Trie


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


def perform_prefix_match(trie: Trie, prefix_var: StringVar) -> None:
    """
    Perform live prefix matching on the loaded trie using the entered prefix (when user clicks "Search" button in GUI).

    Parameters
    ----------
    trie : Trie
        Trie data structure to search
    prefix_var : StringVar
        current prefix string entered by user
    """
    if trie is None:  # Trie not loaded.
        result_text.config(state=tk.NORMAL)  # Enable text widget for editing.
        result_text.delete(1.0, tk.END)  # Clear previous content.
        result_text.insert(tk.END, "Trie not loaded.")  # Insert text.
        result_text.config(state=tk.DISABLED)  # Disable text widget for editing.
        return

    prefix = prefix_var.get()  # Get current prefix string entered by the user.
    if prefix:  # Prefix not empty.
        matches = trie.prefix_match(prefix)  # Get matches in trie.
        result_text.config(state=tk.NORMAL)  # Enable text widget for editing.
        result_text.delete(1.0, tk.END)  # Clear previous content.
        result_text.insert(tk.END, f"{len(matches)} words match the prefix '{prefix}': \n{matches}")  # Insert.
        result_text.config(state=tk.DISABLED)  # Disable text widget for editing.
    else:
        result_text.config(state=tk.NORMAL)  # Enable text widget for editing
        result_text.delete(1.0, tk.END)  # Clear previous content
        result_text.insert(tk.END, "No prefix entered.")  # Insert.
        result_text.config(state=tk.DISABLED)  # Disable text widget for editing


def load_words() -> None:
    """
    Load words from a file into the trie global variable, allowing you to use the same loaded trie for multiple prefix
    searches.
    """
    path = path_entry.get()  # Read path entered in `path_entry` widget.
    if not path:  # No path provided.
        result_text.config(state=tk.NORMAL)  # Enable text widget for editing.
        result_text.delete(1.0, tk.END)  # Clear previous content.
        result_text.insert(tk.END, "Please select a file.")  # Insert new text into widget.
        result_text.config(state=tk.DISABLED)  # Disable text widget for editing.
        return

    try:  # Try to open file and load words.
        with open(path, "r") as f:
            words = f.read().split("\n")

    except FileNotFoundError as e:  # File not found.
        result_text.config(state=tk.NORMAL)  # Enable text widget for editing.
        result_text.delete(1.0, tk.END)  # Clear previous content.
        result_text.insert(tk.END, f"FileNotFoundError: The file {path} you specified could not be found.")
        result_text.config(state=tk.DISABLED)  # Disable text widget for editing.
        return

    global trie
    trie, parallel = build_global_trie(words)
    if parallel:
        res_str = f"Successfully built global trie by merging local tries from available cores."
    else:
        res_str = f"Successfully built global trie."
    # Display success message in  `result_text` widget after loading and building the trie.
    result_text.config(state=tk.NORMAL)  # Enable text widget for editing
    result_text.delete(1.0, tk.END)  # Clear previous content
    result_text.insert(tk.END, res_str)
    result_text.config(state=tk.DISABLED)  # Disable text widget for editing


def on_prefix_entry_change(event) -> None:
    """
    Upon specified event, call `perform_prefix_match` to perform the search based on the current content of the prefix entry field.

    Called whenever a key is released in the prefix_entry field.
    Use bind method to bind the <KeyRelease> event to the prefix_entry field, ensuring that on_prefix_entry_change
    is called whenever the user types or modifies the prefix.

    Parameters
    ----------
    event
        Event triggering the function
    """
    perform_prefix_match(trie, prefix_var)


if __name__ == "__main__":
    # Create a GUI window
    root = tk.Tk()
    root.title("Trie-Based Prefix Matching")

    # Create a frame to hold widgets.
    # Allows us to place widgets in a specific layout and add a scrollbar to the `result_text` widget.
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Create widgets.
    # Labels are used for displaying text.
    # Entry fields allow users to input text.
    # Buttons provide interactive elements.
    path_label = tk.Label(frame, text="Enter the path to your list of words:")
    path_entry = tk.Entry(frame)
    browse_button = tk.Button(frame, text="Browse", command=browse_file)
    load_button = tk.Button(frame, text="Load Words", command=load_words)
    prefix_label = tk.Label(frame, text="Enter prefix to search for:")
    prefix_var = StringVar()  # StringVar is a variable class for managing text variables in Tkinter.

    prefix_entry = tk.Entry(frame, textvariable=prefix_var)
    result_text = tk.Text(frame, height=10, width=40, wrap=tk.WORD)
    scrollbar = tk.Scrollbar(frame, command=result_text.yview)

    # Arrange widgets in the frame.
    path_label.grid(row=0, column=0, sticky="w")
    path_entry.grid(row=0, column=1)
    browse_button.grid(row=0, column=2)
    load_button.grid(row=0, column=3)
    prefix_label.grid(row=1, column=0, sticky="w")
    prefix_entry.grid(row=1, column=1)
    result_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
    scrollbar.grid(row=2, column=4, sticky="ns")

    # Initialize the trie.
    trie = None

    # Configure event handlers.
    load_button.config(command=lambda: load_words())
    # At <KeyRelease> event, bind call of `on_prefix_entry_change` to `prefix entry` widget to trigger search whenever
    # a key is released, i.e., whenever the user types or modifies the prefix, in the entry field.
    # Thus, the search is automatically performed as the user types or modifies the prefix in the `prefix_entry` field,
    # and the matching results are updated in real-time.
    prefix_entry.bind("<KeyRelease>", on_prefix_entry_change)

    # Start the GUI event loop
    root.mainloop()
