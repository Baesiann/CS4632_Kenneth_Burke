# Oversee multi-day simulation planning. Determines # of baristas and hours
# Adapts based on metrics

import numpy as np
from data_management.metrics import average_wait_time, throughput, barista_idle_time

class ScheduleManager:
    def __init__(self, base_baristas=2, max_baristas=5, day_length=480):
        self.base_baristas = base_baristas
        self.max_baristas = max_baristas
        self.day_length = day_length
        self.current_baristas = base_baristas

        # cost weights used for cost minimization optimization
        self.w_wait = 1.0   # Wait time penalty
        self.w_idle = 0.5   # Idle barista penalty
        self.w_throughput = 2.0 # Throughput reward
        self.w_labor = 1.0  # Per barista penalty
        self.w_dropped = 3.0    # Drop penalty

    def evaluate_cost(self, df, num_baristas):
        # Compute cost function from simulation data
        avg_wait = average_wait_time(df)
        avg_throughput = throughput(df, self.day_length)
        idle_time = barista_idle_time(df, num_baristas, self.day_length)
        dropout_count = df["Dropped"].sum() if "Dropped" in df.columns else 0

        # Normalized metrics
        norm_weight = avg_wait / 10.0
        norm_idle = idle_time / (self.day_length * num_baristas)
        norm_throughput = avg_throughput / 10.0
        norm_dropped = dropout_count / 10.0

        cost = (
            self.w_wait * norm_weight + 
            self.w_idle * norm_idle +
            self.w_labor * num_baristas - 
            self.w_throughput * norm_throughput +
            self.w_dropped * norm_dropped
        )
        return cost
    
    def optimize_schedule(self, df):
        # Try different barista counts to minimize total cost
        results = []
        for num in range(1, self.max_baristas + 1):
            cost = self.evaluate_cost(df, num)
            results.append((num, cost))

        optimal_baristas, min_cost = min(results, key=lambda x: x[1])
        self.current_baristas = optimal_baristas
        print(f"Optimized next day staffing: {optimal_baristas} baristas (cost = {min_cost:.3f})")
        return optimal_baristas
