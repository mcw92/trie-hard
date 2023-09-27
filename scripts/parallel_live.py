import tkinter as tk  # Standard library for creating graphical user interfaces in Python
from triehard import TrieLive


if __name__ == "__main__":
    parallel = True
    root = tk.Tk()  # Create a GUI window.
    app = TrieLive(root, parallel)
    root.mainloop()  # Start the GUI event loop.
