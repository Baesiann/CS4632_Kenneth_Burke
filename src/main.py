# Driver program

import simpy
import pandas as pd
from simulation.customer import customer
from simulation.barista import setup_baristas
from simulation.customer import simulate_cox_process
from data_management.collector import DataCollector
from data_management.metrics import average_wait_time, total_revenue, throughput
from data_management.export import save_to_csv

def run_simulation():
    env = simpy.Environment()
    baristas = setup_baristas(env, num_baristas=2)

    # Generation of arrivals
    arrivals, times, baseline, stochastic_intensity = simulate_cox_process()

    # Use DataCollector in place of records[]
    collector = DataCollector()

    for cid, at in enumerate(arrivals, start=1):
        env.process(customer(env, cid, at, baristas, collector.records))

    env.run(until=max(arrivals))

    # Convert to dataframe
    df = collector.to_dataframe()

    return df, times, baseline, stochastic_intensity

if __name__ == "__main__":
    df, times, baseline, stochastic_intensity = run_simulation()

    print(df.head())
    print(f"Total revenue: ${df['Price'].sum():.2f}")
    print(f"Average wait time: {df['WaitTime'].mean():.2f} minutes")
    print(f"Throughput: {throughput(df, max(times)):.2f} customers/min")

    # Use external save to csv
    save_to_csv(df, "simulation_results.csv")
