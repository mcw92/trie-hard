import tkinter as tk  # Standard library for creating graphical user interfaces in Python
from tkinter import filedialog, StringVar
from .trie import Trie
from .utils import build_global_trie


class TrieGui:
    """
    Class providing a basic GUI for trie-based prefix matching.

    Attributes
    ----------
    root
        Main window
    frame
        Frame holding widgets
    path_label
        Label of path entry field
    browse_button
        Clickable button to browse file dialog
    load_button
        Clickable button to load file
    prefix_label
        Label of prefix entry field
    prefix_entry
        Entry field for user input of prefix
    result_text
        Text field to display messages and results
    scrollbar
        Scrolling bar
    trie
        Trie object
    parallel
        Whether trie is to build serially or in a thread parallel manner

    Methods
    -------
    initialize_widgets()
        Initialize and configure widgets and event handlers.
    browse_file()
        Browse file dialog.
    perform_prefix_match()
        Perform prefix match.
    load_words()
        Load words from file into trie.
    on_prefix_entry_change()
        Event handler for live search.
    display_result()
        Display results in text widget.
    """

    def __init__(self, root, parallel) -> None:
        """
        Initialize GUI for trie-based prefix matcher.
        Parameters
        ----------
        root
            Main window
        parallel
            Whether trie is to build serially or in a thread parallel manner
        """
        self.root = root
        self.root.title("Trie-Based Prefix Matching")  # Set title.

        # Create a frame to hold widgets.
        # Allows us to place widgets in a specific layout and add a scrollbar to the `result_text` widget.
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Create widgets.
        # Labels are used for displaying text.
        # Entry fields allow users to input text.
        # Buttons provide interactive elements.
        self.path_label = tk.Label(
            self.frame, text="Enter the path to your list of words:"
        )
        self.path_entry = tk.Entry(self.frame)
        self.browse_button = tk.Button(
            self.frame, text="Browse", command=self.browse_file
        )
        self.load_button = tk.Button(
            self.frame, text="Load Words", command=self.load_words
        )
        self.prefix_label = tk.Label(self.frame, text="Enter prefix to search for:")
        self.prefix_entry = None
        self.result_text = tk.Text(self.frame, height=10, width=40, wrap=tk.WORD)
        self.scrollbar = tk.Scrollbar(self.frame, command=self.result_text.yview)
        self.trie = None
        self.parallel = parallel

    def initialize_widgets(self) -> None:
        """
        Initialize and configure widgets and event handlers.
        """
        self.path_label.grid(row=0, column=0, sticky="w")
        self.path_entry.grid(row=0, column=1)
        self.browse_button.grid(row=0, column=2)
        self.load_button.grid(row=0, column=3)
        self.prefix_label.grid(row=1, column=0, sticky="w")
        self.result_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
        self.scrollbar.grid(row=2, column=4, sticky="ns")
        # Configure event handlers.
        self.load_button.config(command=self.load_words)

    def browse_file(self) -> None:
        """
        Open a file dialog that allows the user to select a file using a graphical user interface (GUI).

        Clicking the "Browse" button in the GUI triggers the `browse_file` function.
        """
        # Open file dialog for selecting a file to open and return selected file's path as a string.
        path = filedialog.askopenfilename()
        # Clear current contents of `path_entry` widget (a text entry field) and insert selected file's path.
        self.path_entry.delete(0, tk.END)  # Clear current text in `path_entry` widget.
        self.path_entry.insert(
            0, path
        )  # Insert selected file's path into `path_entry` widget to make it visible.

    def load_words(self) -> None:
        """
        Load words from file into the trie attribute, allowing you to use the same loaded trie for multiple prefix
        searches.

        Raises
        ------
        FileNotFoundError
            When user-provided path is invalid.
        """
        path = self.path_entry.get()  # Read path entered in `path_entry` widget.
        if not path:  # No path provided.
            self.display_result(
                "Please select a file."
            )  # Display corresponding message in text widget.
            return

        try:  # Try to open file and load words.
            with open(path, "r") as f:
                words = f.read().split("\n")
        except FileNotFoundError:  # File not found.
            self.display_result(
                f"FileNotFoundError: The file {path} you specified could not be found."
            )
            return

        self.trie, parallel = build_global_trie(
            words, self.parallel
        )  # Build trie from loaded list of words.
        if parallel:
            res_str = "Successfully built global trie by merging local tries from available cores."
        else:
            res_str = "Successfully built global trie on a single CPU core."
        self.display_result(
            res_str
        )  # Display corresponding success message in text widget.

    def display_result(self, text: str) -> None:
        """
        Simplify the display of message in the result_text widget.

        Parameters
        ----------
        text : str
            Text to display
        """
        self.result_text.config(state=tk.NORMAL)  # Enable text widget for editing.
        self.result_text.delete(1.0, tk.END)  # Clear previous content.
        self.result_text.insert(tk.END, text)  # Insert text.
        self.result_text.config(state=tk.DISABLED)  # Disable text widget for editing

    def perform_prefix_match(self):
        raise NotImplementedError

    def _perform_prefix_match(self, prefix: str):
        """
        Perform live prefix matching on loaded trie using entered prefix.

        Parameters
        ----------
        prefix : str
            Prefix to search
        """
        if self.trie is None:  # Trie not loaded.
            self.display_result(
                "Trie not loaded."
            )  # Display corresponding message in text widget.
            return

        if prefix:  # Prefix not empty.
            matches = self.trie.prefix_match(prefix)  # Get matches in trie.
            result_str = (
                f"{len(matches)} words match the prefix '{prefix}': \n{matches}"
            )
            self.display_result(result_str)  # Display matches in text widget.
        else:  # No prefix given.
            self.display_result(
                "No prefix entered."
            )  # Display corresponding message in text widget.


class TrieLive(TrieGui):
    """
    Class providing a basic GUI for trie-based prefix matching.

    Attributes
    ----------
    root
        Main window
    frame
        Frame holding widgets
    path_label
        Label of path entry field
    path_entry
        Entry field for user input of path
    browse_button
        Clickable button to browse file dialog
    load_button
        Clickable button to load file
    prefix_label
        Label of prefix entry field
    prefix_var = StringVar()
        StringVar object to managing prefix variables
    prefix_entry
        Entry field for user input of prefix
    result_text
        Text field to display messages and results
    scrollbar
        Scrolling bar
    trie
        Trie object
    parallel
        Whether trie is to build serially or in a thread parallel manner

    Methods
    -------
    initialize_widgets()
        Initialize and configure widgets and event handlers.
    browse_file()
        Browse file dialog.
    perform_prefix_match()
        Perform prefix match.
    load_words()
        Load words from file into trie.
    on_prefix_entry_change()
        Event handler for live search.
    display_result()
        Display results in text widget.
    """

    def __init__(self, root, parallel) -> None:
        """
        Initialize GUI for trie-based prefix matcher.
        Parameters
        ----------
        root
            Main window
        parallel
            Whether trie is to build serially or in a thread parallel manner
        """
        super().__init__(root, parallel)
        self.prefix_var = (
            StringVar()
        )  # StringVar is a variable class for managing text variables in Tkinter.
        self.prefix_entry = tk.Entry(self.frame, textvariable=self.prefix_var)
        self.initialize_widgets()

    def initialize_widgets(self) -> None:
        """
        Initialize and configure widgets and event handlers.
        """
        super().initialize_widgets()
        self.prefix_entry.grid(row=1, column=1)
        # At <KeyRelease> event, bind call of `on_prefix_entry_change` to `prefix entry` widget to trigger search
        # whenever a key is released, i.e., whenever the user types or modifies the prefix, in the entry field.
        # Thus, the search is automatically performed as the user types or modifies the prefix in the `prefix_entry`
        # field and the matching results are updated in real-time.
        self.prefix_entry.bind("<KeyRelease>", self.on_prefix_entry_change)

    def perform_prefix_match(self):
        """
        Perform live prefix matching on loaded trie using entered prefix.
        """
        self._perform_prefix_match(self.prefix_var.get())

    def on_prefix_entry_change(self, event):
        """
        Upon specified event, call `perform_prefix_match` to perform the search based on the current content of the
        prefix entry field.

        Called whenever a key is released in the prefix_entry field.
        Use bind method to bind the <KeyRelease> event to the prefix_entry field, ensuring that on_prefix_entry_change
        is called whenever the user types or modifies the prefix.

        Parameters
        ----------
        event
            Event triggering the function
        """

        self.perform_prefix_match()


class TrieStatic(TrieGui):
    """
    Class providing a basic GUI for trie-based prefix matching.

    Attributes
    ----------
    root
        Main window
    frame
        Frame holding widgets
    path_label
        Label of path entry field
    path_entry
        Entry field for user input of path
    browse_button
        Clickable button to browse file dialog
    load_button
        Clickable button to load file
    prefix_label
        Label of prefix entry field
    prefix_entry
        Entry field for user input of prefix
    search_button
        Clickable button to trigger search
    result_text
        Text field to display messages and results
    scrollbar
        Scrolling bar
    trie
        Trie object
    parallel
        Whether trie is to build serially or in a thread parallel manner

    Methods
    -------
    initialize_widgets()
        Initialize and configure widgets and event handlers.
    browse_file()
        Browse file dialog.
    perform_prefix_match()
        Perform prefix match.
    load_words()
        Load words from file into trie.
    display_result()
        Display results in text widget.
    """

    def __init__(self, root, parallel) -> None:
        """
        Initialize GUI for trie-based prefix matcher.
        Parameters
        ----------
        root
            Main window
        parallel
            Whether trie is to build serially or in a thread parallel manner
        """
        super().__init__(root, parallel)
        self.search_button = tk.Button(
            self.frame, text="Search", command=self.perform_prefix_match
        )
        self.prefix_entry = tk.Entry(self.frame)
        self.initialize_widgets()

    def initialize_widgets(self) -> None:
        """
        Initialize and configure widgets and event handlers.
        """
        super().initialize_widgets()
        self.prefix_entry.grid(row=1, column=1)
        self.search_button.grid(row=1, column=2)

    def perform_prefix_match(self):
        """
        Perform live prefix matching on loaded trie using entered prefix.
        """
        self._perform_prefix_match(
            self.prefix_entry.get()
        )  # Retrieve text entered by user into `prefix_entry` widget.
