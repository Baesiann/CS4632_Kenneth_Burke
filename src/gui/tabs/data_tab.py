import tkinter as tk
from tkinter import ttk, StringVar
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class build_data_tab(ttk.Frame):
    DAY_LENGTH = 480

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Directory with data files
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "data"))
        self.selected_file = StringVar()
        self.df = None

        # Dropdown and buttons
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(top_frame, text="Select Simulation File:").pack(side="left", padx=(0, 10))
        self.file_dropdown = ttk.Combobox(top_frame, textvariable=self.selected_file, width=40, state="readonly")
        self.file_dropdown.pack(side="left")
        ttk.Button(top_frame, text="Load", command=self.load_selected_file).pack(side="left", padx=10)
        ttk.Button(top_frame, text="Refresh", command=self.refresh_file_list).pack(side="left")

        self.refresh_file_list()

        # Matplotlib Figure
        self.figure = plt.Figure(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_file_list(self):
        files = [f for f in os.listdir(self.data_dir) if f.endswith((".csv", ".json"))]
        self.file_dropdown["values"] = files
        if files and not self.selected_file.get():
            self.selected_file.set(files[0])

    def load_selected_file(self):
        """Load CSV/JSON into DataFrame, preprocess, and update dashboard."""
        filename = self.selected_file.get()
        if not filename:
            return

        filepath = os.path.join(self.data_dir, filename)
        try:
            if filename.endswith(".csv"):
                self.df = pd.read_csv(filepath)
            else:
                self.df = pd.read_json(filepath)

            # --- Data Preprocessing ---
            # Type conversion and cleanup
            self.df["Dropped"] = self.df["Dropped"].astype(bool)
            self.df["Price"] = self.df["Price"].astype(float)
            self.df["ArrivalTime"] = self.df["ArrivalTime"].astype(float)
            self.df["WaitTime"] = self.df["WaitTime"].astype(float)
            self.df.dropna(subset=["ArrivalTime", "WaitTime"], inplace=True)
            
            # === FINAL CORRECT DAY LOGIC: Only count a new day when CustomerID is 1 ===
            self.df["Day"] = (self.df["CustomerID"] == 1).cumsum()
            
            # --- CRITICAL FIX: LIMIT ANALYSIS TO THE FIRST 5 DAYS ---
            self.df = self.df[self.df["Day"] <= 5].copy()
            
            # QueueExitTime calculation
            self.df["QueueExitTime"] = np.where(
                self.df["Dropped"] == False, 
                self.df["StartService"].fillna(self.DAY_LENGTH),
                self.df["ArrivalTime"] + self.df["WaitTime"]
            )
            
            # Create Total Minute columns
            self.df["TotalMinute"] = (self.df["Day"] - 1) * self.DAY_LENGTH + self.df["ArrivalTime"]
            self.df["QueueExitTotalMinute"] = (self.df["Day"] - 1) * self.DAY_LENGTH + self.df["QueueExitTime"]
            
            self.update_dashboard()
        except Exception as e:
            print(f"Error loading file: {e}")

    def update_dashboard(self):
        if self.df is None or self.df.empty:
            return

        self.figure.clear()
        axes = self.figure.subplots(2, 3, sharex=True)
        axes = axes.flatten()

        n_days = self.df["Day"].max()
        
        # --- 1. Daily Aggregation ---
        daily_metrics = self.df.groupby("Day").agg(
            AvgWaitTime=("WaitTime", "mean"),
            DroppedCustomers=("Dropped", "sum"),
            CustomerArrivals=("CustomerID", "count"),
        )
        
        # Revenue Calculation (Serviced Customers only)
        serviced_df = self.df[self.df["Dropped"] == False].copy()
        revenue = serviced_df.groupby("Day")["Price"].sum().rename("Revenue")
        daily_metrics = daily_metrics.merge(revenue, left_index=True, right_index=True, how='left').fillna({'Revenue': 0})
        
        # Throughput Calculation
        if not serviced_df.empty and 'EndService' in serviced_df.columns:
            serviced_df.loc[:, 'EndDay'] = ((serviced_df["Day"] - 1) * self.DAY_LENGTH + serviced_df["EndService"]) // self.DAY_LENGTH + 1
            throughput = serviced_df.groupby('EndDay')['CustomerID'].count().rename("Throughput")
            daily_metrics = daily_metrics.merge(throughput, left_index=True, right_index=True, how='left')
        
        daily_metrics.fillna(0, inplace=True)
        daily_metrics = daily_metrics.reindex(range(1, int(n_days) + 1), fill_value=0)
        daily_metrics.index.name = 'Day'
        daily_metrics = daily_metrics.reset_index()

        # --- 2. Average Customers in Queue per Day ---
        total_length = int(n_days * self.DAY_LENGTH)
        queue_per_min = np.zeros(total_length)
        
        for _, row in self.df.iterrows():
            start = int(row["TotalMinute"]) 
            end = int(np.ceil(row["QueueExitTotalMinute"]))
            end = min(end, total_length)
            
            if end > start:
                queue_per_min[start:end] += 1
        
        avg_queue_size = []
        for day in range(1, int(n_days) + 1):
            start_idx = (day - 1) * self.DAY_LENGTH
            end_idx = day * self.DAY_LENGTH
            daily_mean = queue_per_min[start_idx:end_idx].mean()
            avg_queue_size.append(daily_mean)
        
        daily_metrics["AvgQueueSize"] = avg_queue_size


        # --- 3. Plotting ---
        metrics_to_plot = {
            'AvgWaitTime': 'Average Wait Time (min) per Day',
            'Revenue': 'Total Revenue ($) per Day',
            'Throughput': 'Throughput (Customers/Day)',
            'DroppedCustomers': 'Dropped Customers per Day',
            'AvgQueueSize': 'Average Customers in Queue per Day',
            'CustomerArrivals': 'Customer Arrivals per Day'
        }

        x_days = daily_metrics['Day']
        total_days = len(x_days)
        
        xticks = x_days 

        for i, (metric_col, title) in enumerate(metrics_to_plot.items()):
            ax = axes[i]
            values = daily_metrics[metric_col]

            # Use bar plot
            ax.bar(x_days, values, color=plt.cm.Paired(i / len(metrics_to_plot)), width=0.8)

            # Set the title and labels
            ax.set_title(title, fontsize=10)
            ax.set_ylabel("Value", fontsize=9)
            ax.grid(axis='y', linestyle="--", alpha=0.5)

            # Set y-axis limit
            max_val = values.replace([np.inf, -np.inf], np.nan).max()
            if pd.isna(max_val) or max_val <= 0:
                ax.set_ylim(0, 1)
            else:
                ax.set_ylim(0, max_val * 1.1)

            # Apply clean X-axis settings
            ax.set_xticks(xticks)
            ax.set_xlim(0.5, total_days + 0.5)
            
            # Remove x-tick labels from the top row
            if i < 3:
                ax.tick_params(labelbottom=False)

        # Final X-axis labeling for the bottom row
        for ax in axes[3:]:
            ax.set_xlabel("Day Index", fontsize=10)
            ax.set_xticklabels([f'Day {int(d)}' for d in xticks], fontsize=8) 
            
        self.figure.tight_layout()
        self.canvas.draw()