#!/Users/marieweiel/Projects/vector/vector-venv/bin/python

import tkinter as tk  # Standard library for creating graphical user interfaces in Python
import multiprocessing

from triehard import TrieLive


if __name__ == "__main__":
    multiprocessing.freeze_support()
    parallel = True
    root = tk.Tk()  # Create a GUI window.
    app = TrieLive(root, parallel)
    root.mainloop()  # Start the GUI event loop.
