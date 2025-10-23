import tkinter as tk
from tkinter import ttk
import random

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

        """ COST WEIGHT SETUP FRAME """
        cost_frame = ttk.LabelFrame(parent, text="Cost Weight Setup", padding=10)
        cost_frame.grid(row=1, column=0, sticky="ew", pady=20, padx=20)
        cost_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # First Column: Penalties
        ttk.Label(cost_frame, text="Wait Time Penalty Weight:").grid(row=0, column=0, sticky="w")
        self.wait_weight_var = tk.DoubleVar(value=1.0)
        ttk.Entry(cost_frame, textvariable=self.wait_weight_var, width=8).grid(row=0, column=1)

        ttk.Label(cost_frame, text="Idle Time Penalty Weight:").grid(row=1, column=0, sticky="w")
        self.idle_weight_var = tk.DoubleVar(value=0.5)
        ttk.Entry(cost_frame, textvariable=self.idle_weight_var, width=8).grid(row=1, column=1)

        ttk.Label(cost_frame, text="Barista Count Penalty Weight:").grid(row=2, column=0, sticky="w")
        self.barista_weight_var = tk.DoubleVar(value=1.0)
        ttk.Entry(cost_frame, textvariable=self.barista_weight_var, width=8).grid(row=2, column=1)

        ttk.Label(cost_frame, text="Dropped Customer Penalty Weight:").grid(row=3, column=0, sticky="w")
        self.dropped_weight_var = tk.DoubleVar(value=3.0)
        ttk.Entry(cost_frame, textvariable=self.dropped_weight_var, width=8).grid(row=3, column=1)

        ttk.Separator(cost_frame, orient="vertical").grid(row=0, column=2, rowspan=4, sticky="ns", padx=10)

        # Second Column: Rewards
        ttk.Label(cost_frame, text="Throughput Reward Weight:").grid(row=0, column=3, sticky="w")
        self.thpt_weight_var = tk.DoubleVar(value=2.0)
        ttk.Entry(cost_frame, textvariable=self.thpt_weight_var, width=8).grid(row=0, column=4)

        """ ORDER SETUP FRAME """
        order_frame = ttk.LabelFrame(parent, text="Order Setup", padding=10)
        order_frame.grid(row=1, column=1, sticky="ew", pady=20, padx=20)
        order_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # Define columns
        order_tree = ttk.Treeview(order_frame)
        order_tree['columns'] = ("Drink", "Price", "Mean Service Time", "Standard Deviation of Service Time", "Drink Probability")

        # Formulate columns
        order_tree.column("#0", width=0, minwidth=25)   # I still don't know what this line does
        order_tree.column("Drink", anchor="center", width=120)
        order_tree.column("Price", anchor="center", width=120)
        order_tree.column("Mean Service Time", anchor="center", width=120)
        order_tree.column("Standard Deviation of Service Time", anchor="center", width=120)
        order_tree.column("Drink Probability", anchor="center", width=120)

        # Create Headings
        order_tree.heading('#0', text="Label", anchor="w")
        order_tree.heading("Drink", text="Drink", anchor="center")
        order_tree.heading("Price", text="Price", anchor="center")
        order_tree.heading("Mean Service Time", text="Avg. Service Time", anchor="center")
        order_tree.heading("Standard Deviation of Service Time", text="Std. Service Time", anchor="center")
        order_tree.heading("Drink Probability", text="Order Likeliness", anchor="center")

        # Populate Tree from ORDERS
        for cid, data in ORDERS.items():
            order_tree.insert("", "end", values=(
                cid,
                data["price"],
                data["mean_service"],
                data["std_service"],
                2
                )
            )

        # Add to screen
        order_tree.pack(pady=20)

        """ SAVE / CONTROL AREA """
        save_frame = ttk.Frame(parent, padding=10)
        save_frame.grid(row=2, column=0, sticky="nsew", pady=(15, 5), padx=30)
        save_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Label(save_frame, text="Save Run As:").grid(row=0, column=0, sticky="e")
        self.save_name_var = tk.StringVar(value="simulation_run")
        ttk.Entry(save_frame, textvariable=self.save_name_var, width=25).grid(row=0, column=1, padx=10, sticky="w")
        self.save_as = tk.StringVar()
        ttk.Radiobutton(save_frame, text=".csv", variable=self.save_as, value="csv").grid(row=0, column=2, sticky="ew")
        ttk.Radiobutton(save_frame, text=".json", variable=self.save_as, value="json").grid(row=0, column=3, sticky="ew")

        """ BUTTONS """
        button_frame = ttk.Frame(parent, padding=10)
        button_frame.grid(row=5, column=0, pady=(10, 0))

        ttk.Button(button_frame, text="Start Simulation", command=self.start_simulation).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Reset Parameters", command=self.reset_parameters).grid(row=0, column=1, padx=10)
        

    def start_simulation(self):
        """Gather all user input and run the simulation."""
        # TODO: connect to run_simulation_day() logic
        print("Starting simulation with parameters:")
        print({
            "days": self.days_var.get(),
            "baristas": self.baristas_var.get(),
            "arrival_rate": self.arrival_rate_var.get(),
            "cost_weights": (self.wait_weight_var.get(), self.idle_weight_var.get(), self.revenue_weight_var.get())
        })

    def reset_parameters(self):
        """Reset all parameters to default values."""
        self.days_var.set(5)
        self.baristas_var.set(2)
        self.seed_var.set(random.randint(1000000, 9999999))
        self.arrival_rate_var.set(10.0)
        self.arrival_var.set(2.0)
        self.peak_hours_var.set("120, 300")
        self.wait_weight_var.set(0.4)
        self.idle_weight_var.set(0.3)
        self.revenue_weight_var.set(0.3)
        self.order_types_var.set("coffee,latte,espresso")
        self.price_avg_var.set(4.5)
        self.price_var_var.set(1.0)
        self.save_name_var.set("simulation_run")

