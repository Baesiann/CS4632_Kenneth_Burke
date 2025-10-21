# Driver program

import simpy
import pandas as pd
from simulation.customer import customer
from simulation.barista import setup_baristas
from simulation.customer import simulate_cox_process
from data_management.collector import DataCollector
from data_management.metrics import average_wait_time, total_revenue, throughput
from data_management.export import save_to_csv
from simulation.schedule_manager import ScheduleManager

# Number of simulation days (add to gui later)
NUM_DAYS = 7

def run_simulation_day(env, num_baristas, collector):
    baristas = setup_baristas(env, num_baristas)
    arrivals, times, baseline, stochastic_intensity = simulate_cox_process()

    # Spawn customers
    for cid, at in enumerate(arrivals, start=1):
        env.process(customer(env, cid, at, baristas, collector.records))

    env.run(until=max(arrivals))

    # Convert to dataframe
    return collector.to_dataframe(), times

if __name__ == "__main__":
    schedule_manager = ScheduleManager(base_baristas=2)
    all_days_data = []

    for day in range(1, NUM_DAYS + 1):
        print(f"Simulating Day {day} with {schedule_manager.current_baristas} baristas")

        env = simpy.Environment()
        collector = DataCollector()

        df, times = run_simulation_day(env, schedule_manager.current_baristas, collector)
        all_days_data.append(df)

        # Call the optimizer for next day
        schedule_manager.optimize_schedule(df)

    # Combine all days
    final_df = pd.concat(all_days_data, keys=[f"Day {i}" for i in range(1, NUM_DAYS + 1)])

    # Use external save to csv
    save_to_csv(final_df, "simulation_results.csv")
