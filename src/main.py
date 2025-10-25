from tkinter import *
from tkinter import ttk
from gui.tabs.simulation_tab import build_sim_tab
from gui.tabs.data_tab import build_data_tab
import os

class CafeSimGUI(Tk):
    def __init__(self):
        super().__init__()  # Initializes Tk
        # Initialize the Window
        self.title("Cafe Simulation")
        self.geometry("1600x900")

        # Notebook setup
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, pady=15)

        # Tabs, instantiated as objects, references kept
        self.tab_sim = build_sim_tab(self.notebook)
        self.tab_data = build_data_tab(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.tab_sim, text="Simulation Manager")
        self.notebook.add(self.tab_data, text="Data Visualization")

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    os.makedirs(DATA_DIR, exist_ok=True)

    app = CafeSimGUI()
    app.mainloop()
