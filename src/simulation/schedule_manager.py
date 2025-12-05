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
        print(f"Maximum allowed drops for tomorrow: {self.max_allowed_drops}")
        print("Re-evaluating barista staffing for tomorrow...\n")

        # Determine tomorrow's staffing based on today's performance
        current_staff = self.current_baristas
        next_staff = current_staff

        if today_drops > self.max_allowed_drops:
            # Need to increase staffing
            next_staff = min(current_staff + 1, self.max_baristas)
            print(f"Increasing baristas from {current_staff} to {next_staff} due to high drops.\n")

        elif today_drops < 0.5 * self.max_allowed_drops and current_staff > self.base_baristas:
            # Goal met, try reducing staff
            next_staff = max(current_staff - 1, self.base_baristas)
            print(f"Decreasing baristas from {current_staff} to {next_staff} due to low drops.\n")
        
        else:
            print(f"Maintaining baristas at {current_staff}.\n")
        
        # update current baristas
        self.current_baristas = next_staff

        # record staffing that will be used tomorrow
        if day_number is not None:
            self.history.append((day_number, next_staff))

        return next_staff
