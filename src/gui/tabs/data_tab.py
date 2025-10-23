import tkinter as tk
from tkinter import ttk

class build_data_tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Visualization goes here")
        self.label.pack(pady=10)

    def update_plot(self, message):
        """Public method to update something externally"""
        self.label.config(text=message)
