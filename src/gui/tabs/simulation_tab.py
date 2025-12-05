import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

from gui.components.treev import EditableTreeview
from data_management.export import save_to_csv, save_to_json
from simulation.simulation_runner import run_full_simulation

# importing ORDERS
import sys, os
sys.path.append("..")
from simulation.order import ORDERS

class build_sim_tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.pack(fill="both", expand=True, padx=15, pady=20)
        
        """ SETUP FRAME """
        setup_frame = ttk.LabelFrame(parent, text="Setup", padding=10)
        setup_frame.grid(row=0, column=0, sticky="ew", pady=(30, 0), padx=20)
        setup_frame.columnconfigure((0, 1, 2, 3), weight=1)

        ttk.Label(setup_frame, text="Simulation Days:").grid(row=0, column=0, sticky="w")
        self.days_var = tk.IntVar(value=5)
        ttk.Entry(setup_frame, textvariable=self.days_var, width=8).grid(row=0, column=1)

        ttk.Label(setup_frame, text="Starting Baristas:").grid(row=1, column=0, sticky="w")
        self.baristas_var = tk.IntVar(value=2)
        ttk.Entry(setup_frame, textvariable=self.baristas_var, width=8).grid(row=1, column=1)

        ttk.Label(setup_frame, text="Random Seed:").grid(row=2, column=0, sticky="w")
        self.seed_var = tk.IntVar(value=random.randint(1000000, 9999999))
        ttk.Entry(setup_frame, textvariable=self.seed_var, width=8).grid(row=2, column=1)

        """ CUSTOMER ARRIVAL FRAME """
        arrival_frame = ttk.LabelFrame(parent, text="Customer Arrival", padding=10)
        arrival_frame.grid(row=0, column=1, sticky="ew", pady=(30, 0), padx=20)
        arrival_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # First Column
        ttk.Label(arrival_frame, text="Baseline Arrival Rate:").grid(row=0, column=0, sticky="w")
        self.baseline_rate_var = tk.DoubleVar(value=5.0)
        ttk.Entry(arrival_frame, textvariable=self.baseline_rate_var, width=8).grid(row=0, column=1)

        ttk.Label(arrival_frame, text="Morning Rush Intensity:").grid(row=1, column=0, sticky="w")
        self.morning_intensity_var = tk.DoubleVar(value=10.0)
        ttk.Entry(arrival_frame, textvariable=self.morning_intensity_var, width=8).grid(row=1, column=1)

        ttk.Label(arrival_frame, text="Lunch Rush Intensity:").grid(row=2, column=0, sticky="w")
        self.lunch_intensity_var = tk.DoubleVar(value=8.0)
        ttk.Entry(arrival_frame, textvariable=self.lunch_intensity_var, width=8).grid(row=2, column=1)

        ttk.Separator(arrival_frame, orient="vertical").grid(row=0, column=2, rowspan=3, sticky="ns", padx=10)

        # Second Column
        ttk.Label(arrival_frame, text="Randomness Intensity:").grid(row=0, column=3, sticky="w")
        self.rand_intensity_var = tk.DoubleVar(value=2.0)
        ttk.Entry(arrival_frame, textvariable=self.rand_intensity_var, width=8).grid(row=0, column=4)

        ttk.Label(arrival_frame, text="Morning Rush Duration (min):").grid(row=1, column=3, sticky="w")
        self.morning_dur_var = tk.IntVar(value=60)
        ttk.Entry(arrival_frame, textvariable=self.morning_dur_var, width=8).grid(row=1, column=4)

        ttk.Label(arrival_frame, text="Lunch Rush Duration (min):").grid(row=2, column=3, sticky="w")
        self.lunch_dur_var = tk.IntVar(value=90)
        ttk.Entry(arrival_frame, textvariable=self.lunch_dur_var, width=8).grid(row=2, column=4)

        # """ COST WEIGHT SETUP FRAME """
        # cost_frame = ttk.LabelFrame(parent, text="Cost Weight Setup", padding=10)
        # cost_frame.grid(row=1, column=0, sticky="ew", pady=20, padx=20)
        # cost_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # # First Column: Penalties
        # ttk.Label(cost_frame, text="Wait Time Penalty Weight:").grid(row=0, column=0, sticky="w")
        # self.wait_weight_var = tk.DoubleVar(value=1.0)
        # ttk.Entry(cost_frame, textvariable=self.wait_weight_var, width=8).grid(row=0, column=1)

        # ttk.Label(cost_frame, text="Idle Time Penalty Weight:").grid(row=1, column=0, sticky="w")
        # self.idle_weight_var = tk.DoubleVar(value=0.5)
        # ttk.Entry(cost_frame, textvariable=self.idle_weight_var, width=8).grid(row=1, column=1)

        # ttk.Label(cost_frame, text="Barista Count Penalty Weight:").grid(row=2, column=0, sticky="w")
        # self.barista_weight_var = tk.DoubleVar(value=1.0)
        # ttk.Entry(cost_frame, textvariable=self.barista_weight_var, width=8).grid(row=2, column=1)

        # ttk.Label(cost_frame, text="Dropped Customer Penalty Weight:").grid(row=3, column=0, sticky="w")
        # self.dropped_weight_var = tk.DoubleVar(value=3.0)
        # ttk.Entry(cost_frame, textvariable=self.dropped_weight_var, width=8).grid(row=3, column=1)

        # ttk.Separator(cost_frame, orient="vertical").grid(row=0, column=2, rowspan=4, sticky="ns", padx=10)

        # # Second Column: Rewards
        # ttk.Label(cost_frame, text="Throughput Reward Weight:").grid(row=0, column=3, sticky="w")
        # self.thpt_weight_var = tk.DoubleVar(value=2.0)
        # ttk.Entry(cost_frame, textvariable=self.thpt_weight_var, width=8).grid(row=0, column=4)

        """ ORDER SETUP FRAME """
        order_frame = ttk.LabelFrame(parent, text="Order Setup", padding=10)
        order_frame.grid(row=1, column=1, sticky="ew", pady=20, padx=20)
        order_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # Define columns
        columns = ("Drink", "Price", "Mean Service Time", "Standard Deviation of Service Time", "Drink Probability")
        order_tree = EditableTreeview(order_frame, ORDERS, columns=columns, show="headings", height=8)

        # Formulate columns
        for col in columns:
            order_tree.heading(col, text=col)
            order_tree.column(col, anchor="center", width=120)
        # Add to screen
        order_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate Tree from ORDERS
        for cid, data in ORDERS.items():
            order_tree.insert("", "end", values=(
                cid,
                data["price"],
                data["mean_service"],
                data["std_service"],
                data["likeliness"]
                )
            )

        """ SAVE / CONTROL AREA """
        save_frame = ttk.Frame(parent, padding=10)
        save_frame.grid(row=1, column=0, sticky="nsew", pady=(50, 5), padx=30)
        save_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Label(save_frame, text="Save Run As:").grid(row=0, column=0, sticky="e")
        self.save_name_var = tk.StringVar(value="simulation_run")
        ttk.Entry(save_frame, textvariable=self.save_name_var, width=25).grid(row=0, column=1, padx=10, sticky="w")
        self.save_as = tk.StringVar()
        ttk.Radiobutton(save_frame, text=".csv", variable=self.save_as, value="csv").grid(row=0, column=2, sticky="ew")
        ttk.Radiobutton(save_frame, text=".json", variable=self.save_as, value="json").grid(row=0, column=3, sticky="ew")

        """ BUTTONS """
        button_frame = ttk.Frame(parent, padding=10)
        button_frame.grid(row=1, column=0, pady=(10, 0))

        ttk.Button(button_frame, text="Start Simulation", command=self.start_simulation).grid(row=1, column=0, padx=10, sticky="n")
        ttk.Button(button_frame, text="Reset Parameters", command=self.reset_parameters).grid(row=1, column=1, padx=10, sticky="n")
        

    def start_simulation(self):
        """Gather all user input and run the simulation."""
        try:
            start = time.time()
            params = self.collect_parameters()

            print("Running simulation with parameters:", params)

            # Run sim with collected parameters
            results_df = run_full_simulation(**params)

            # Build filename from entry box
            filename = self.save_name_var.get().strip()
            if not filename:
                messagebox.showerror("Error", "Please enter a filename.")
                return
            
            save_format = self.save_as.get()
            if save_format == "csv":
                save_to_csv(results_df, filename + ".csv")
            elif save_format == "json":
                save_to_json(results_df, filename + ".json")
            else:
                messagebox.showerror("Error", "Please select a file format.")
                return
            # End time
            end = time.time()
            print(f"Runtime: {end - start:.4f} seconds")
            messagebox.showinfo("Success", f"Simulation completed and saved as {filename}.{save_format}")

        except Exception as e:
            messagebox.showerror("Simulation Error", f"An error occurred:\n{e}")
            

    def reset_parameters(self):
        """Reset all parameters to default values."""
        self.days_var.set(5)
        self.baristas_var.set(2)
        self.seed_var.set(random.randint(1000000, 9999999))

        self.baseline_rate_var.set(5.0)
        self.morning_intensity_var.set(10.0)
        self.lunch_intensity_var.set(8.0)
        self.rand_intensity_var.set(2.0)
        self.morning_dur_var.set(60)
        self.lunch_dur_var.set(90)

        # self.wait_weight_var.set(1.0)
        # self.idle_weight_var.set(0.5)
        # self.barista_weight_var.set(1.0)
        # self.dropped_weight_var.set(3.0)
        # self.thpt_weight_var.set(2.0)
        
        self.save_name_var.set("simulation_run")

    def collect_parameters(self):
        return {
            "num_days": self.days_var.get(),
            # "base_baristas": self.baristas_var.get(),
            "seed": self.seed_var.get(),

            "baseline_rate": self.baseline_rate_var.get(),
            "morning_intensity": self.morning_intensity_var.get(),
            "lunch_intensity": self.lunch_intensity_var.get(),
            "rand_intensity": self.rand_intensity_var.get(),
            "morning_dur": self.morning_dur_var.get(),
            "lunch_dur": self.lunch_dur_var.get()

            # "w_wait": self.wait_weight_var.get(),
            # "w_idle": self.idle_weight_var.get(),
            # "w_labor": self.barista_weight_var.get(),
            # "w_dropped": self.dropped_weight_var.get(),
            # "w_throughput": self.thpt_weight_var.get()
        }