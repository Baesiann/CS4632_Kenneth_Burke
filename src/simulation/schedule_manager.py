# Oversee multi-day simulation planning. Determines # of baristas and hours
# Adapts based on metrics

import simpy
import numpy as np
from data_management.metrics import average_wait_time, throughput, barista_idle_time
from data_management.collector import DataCollector

class ScheduleManager:
    """
    Schedule manager that uses drop-only optimization.
    It searches for the minimum number of baristas that produce
    drop_count <= max_allowed_drops by running new simulations.
    """

    def __init__(
        self,
        simulate_func,
        day_length=480,
        base_baristas=2,
        max_baristas=10,
    ):
        # store simulator to use inside optimize_schedule
        self.simulate_func = simulate_func

        self.day_length = day_length
        self.base_baristas = base_baristas
        self.max_baristas = max_baristas
        self.max_allowed_drops = None

        # what driver uses as "current baristas"
        self.current_baristas = base_baristas

        # Keep a history of barista counts
        self.history = []


    def optimize_schedule(self, df_today, day_number=None):
        """
        Called by driver after today's df is generated.
        We ignore today's df except for printing drops,
        because optimal staffing is determined by running
        multiple simulated scenarios internally.
        """

        total_arrivals = len(df_today)
        self.max_allowed_drops = int(0.01 * total_arrivals)
        # today's drop count (for logging only)
        today_drops = df_today["Dropped"].sum()
        print(f"\nToday's dropped customers: {today_drops}")
        print("Re-evaluating barista staffing for tomorrow...\n")

        # Try 1..max_baristas
        for num in range(1, self.max_baristas + 1):
            print(f"Testing {num} barista(s)...")

            # We run a fresh single-day simulation internally
            env = simpy.Environment()
            collector = DataCollector()
            df, _ = self.simulate_func(env, num, collector)

            drop_count = df["Dropped"].sum()
            print(f" -> Drops: {drop_count}")

            if drop_count <= self.max_allowed_drops:
                print(f" => Optimal staffing for tomorrow: {num} baristas\n")
                self.current_baristas = num
                if day_number is not None:
                    self.history.append((day_number, num))
                return num

        # If even max baristas was not enough
        print(
            f"WARNING: Even {self.max_baristas} baristas exceed drop limit "
            f"({self.max_allowed_drops}). Using max.\n"
        )
        self.current_baristas = self.max_baristas
        return self.max_baristas
