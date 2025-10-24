# Oversee multi-day simulation planning. Determines # of baristas and hours
# Adapts based on metrics

import numpy as np
from data_management.metrics import average_wait_time, throughput, barista_idle_time

class ScheduleManager:
    def __init__(self, day_length=480,
                base_baristas=2,
                max_baristas=10,
                w_wait=1,
                w_idle=1,
                w_labor=1,
                w_dropped=1,
                w_throughput=1):
        self.base_baristas = base_baristas
        self.day_length = day_length
        self.current_baristas = base_baristas
        self.max_baristas = max_baristas

        # cost weights used for cost minimization optimization
        self.w_wait = w_wait   # Wait time penalty
        self.w_idle = w_idle   # Idle barista penalty
        self.w_throughput = w_throughput # Throughput reward
        self.w_labor = w_labor  # Per barista penalty
        self.w_dropped = w_dropped    # Drop penalty

        # Internal targets for normalization
        self.TARGET_AVG_WAIT = 5.0  # 5 min is target max penalty
        self.TARGET_THROUGHPUT = 100.0  # This many customers a day for max reward
        self.LABOR_BASE_COST = 5.0  # Base to labor cost meaningful (barista * 5)
        self.TARGET_MAX_DROPPED = 10.0  # 10 customers dropped is max penalty

    def evaluate_cost(self, df, num_baristas):
        # Compute cost function from simulation data
        avg_wait = average_wait_time(df)
        avg_throughput = throughput(df, self.day_length)
        idle_time = barista_idle_time(df, num_baristas, self.day_length)
        dropout_count = df["Dropped"].sum() if "Dropped" in df.columns else 0

        # Normalized metrics
        norm_weight = min(avg_wait, 10.0)
        norm_idle = idle_time / (self.day_length * num_baristas) * 10.0
        norm_throughput = (avg_throughput / self.TARGET_THROUGHPUT) * 10.0
        norm_dropped = (dropout_count / self.TARGET_MAX_DROPPED) * 10.0
        labor_pen = num_baristas * self.LABOR_BASE_COST

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
