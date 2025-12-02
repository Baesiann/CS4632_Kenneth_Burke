import tkinter as tk
from tkinter import ttk, messagebox
import sys, os, json
#Import base ORDERS as a default
sys.path.append("..")
from simulation.order import ORDERS as DEFAULT_ORDERS
from simulation.customer import calc_patience

# Load orders from JSON (persistent)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "../../data_management/orders.json")
DATA_FILE = os.path.normpath(DATA_FILE)
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        ORDERS = json.load(file)
else:
    ORDERS = DEFAULT_ORDERS.copy()

class EditableTreeview(ttk.Treeview):
    def __init__(self, parent, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data = data    # ref to ORDERS
        self.bind("<Double-1>", self._on_double_click)  # Edit cell on double click

        # Entry Section
        self.form_frame = ttk.Frame(parent)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Drink:").grid(row=0, column=0, padx=5)
        ttk.Label(self.form_frame, text="Price:").grid(row=0, column=1, padx=5)
        ttk.Label(self.form_frame, text="Avg. Service Time:").grid(row=0, column=2, padx=5)
        ttk.Label(self.form_frame, text="Std. Service Time:").grid(row=0, column=3, padx=5)
        ttk.Label(self.form_frame, text="Order Likeliness:").grid(row=0, column=4, padx=5)

        self.drink_var = tk.StringVar()
        self.price_var = tk.DoubleVar()
        self.avg_var = tk.DoubleVar()
        self.std_var = tk.DoubleVar()
        self.like_var = tk.DoubleVar()

        ttk.Entry(self.form_frame, textvariable=self.drink_var, width=12).grid(row=1, column=0, padx=5)
        ttk.Entry(self.form_frame, textvariable=self.price_var, width=8).grid(row=1, column=1, padx=5)
        ttk.Entry(self.form_frame, textvariable=self.avg_var, width=12).grid(row=1, column=2, padx=5)
        ttk.Entry(self.form_frame, textvariable=self.std_var, width=12).grid(row=1, column=3, padx=5)
        ttk.Entry(self.form_frame, textvariable=self.like_var, width=12).grid(row=1, column=4, padx=5)

        self.drink_var.set("")
        self.price_var.set(3.0)
        self.avg_var.set(3.0)
        self.std_var.set(2.0)
        self.like_var.set(2)

        ttk.Button(self.form_frame, text="Add Drink", command=self._add_item).grid(row=1, column=6, padx=10)

        # Removal
        rem_frame = ttk.Frame(parent)
        rem_frame.pack(pady=10)
        ttk.Button(rem_frame, text="Delete Selected", command=self._delete_selected).pack()

    # Edit an existing row
    def _on_double_click(self, event):
        # ID row/column
        region = self.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.identify_row(event.y)
        col_id = self.identify_column(event.x)
        col_index = int(col_id[1:]) - 1     # '#1' -> 0, '#2' -> 1

        # Get current value and cell
        item = self.item(row_id)
        values = list(item["values"])
        old_value = values[col_index]
        x, y, width, height = self.bbox(row_id, col_id)

        # Create Entry Box
        entry = ttk.Entry(self)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, old_value)
        entry.focus()

        def save_edit(event):
            new_val = entry.get()
            entry.destroy()

            # Try to convert numbers to float
            try:
                new_val = float(new_val)
            except ValueError:
                pass

            values[col_index] = new_val
            self.item(row_id, values=values)

            # Sync change to self.data
            item_name = values[0]
            key_map = ["price", "mean service, std_service", "likeliness"]
            if item_name in self.data and 0 < col_index < len(key_map) + 1:
                self.data[item_name][key_map[col_index - 1]] = new_val
                self._save_to_file()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    # Adding new item to treeview and ORDERS
    def _add_item(self):
        drink = self.drink_var.get().strip().lower()
        price = self.price_var.get()
        avg = self.avg_var.get()
        std = self.std_var.get()
        like = self.like_var.get()

        if not drink:
            print("Drink Name Required")
            return
        
        if drink in self.data:
            messagebox.showerror("Error", f"'{drink}' already exists.")
            return
        
        # Update ORDERS
        self.data[drink] = {"price": price, "mean_service": avg, "std_service": std, "likeliness": like}

        # Recalculate customer patience stats
        print(f"Average mean service time across orders: {calc_patience():.2f} minutes")
        print(f"Average patience time modeled as ~ N({calc_patience() * 2.5:.2f}, {calc_patience() * 0.5:.2f}) minutes")

        # Add to treeview
        self.insert("", "end", values=(drink, price, avg, std, like))

        # Clear inputs
        self.drink_var.set("")
        self.price_var.set(3.0)
        self.avg_var.set(3.0)
        self.std_var.set(2.0)
        self.like_var.set(2)

        self._save_to_file()

        print("Added new drink:", drink)
        print("Updated ORDERS:", self.data)

    # Delete selected drinks
    def _delete_selected(self):
        selected_items = self.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Select one or more items to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Delete {len(selected_items)} item(s)?")
        if not confirm:
            return

        for item_id in selected_items:
            values = self.item(item_id, "values")
            drink_name = values[0]
            if drink_name in self.data:
                del self.data[drink_name]
            self.delete(item_id)

        self._save_to_file()
        print("Deleted items, updated ORDERS:", self.data)
        # Recalculate customer patience stats
        print(f"Average mean service time across orders: {calc_patience():.2f} minutes")
        print(f"Average patience time modeled as ~ N({calc_patience() * 2.5:.2f}, {calc_patience() * 0.5:.2f}) minutes")

    def _save_to_file(self):
        # Write current dict back into orders.json
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4)
            print("Saved changes to orders.json")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data: {e}")