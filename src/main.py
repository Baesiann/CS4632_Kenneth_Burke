# Driver program

import simpy
import pandas as pd
from customer import customer
from barista import setup_baristas
from customer import simulate_cox_process

def run_simulation():
    env = simpy.Environment()
    baristas = setup_baristas(env, num_baristas=2)

    arrivals, times, baseline, stochastic_intensity = simulate_cox_process()

    records = []
    for cid, at in enumerate(arrivals, start=1):
        env.process(customer(env, cid, at, baristas, records))

    env.run(until=max(arrivals))
    return pd.DataFrame(records), times, baseline, stochastic_intensity

if __name__ == "__main__":
    df, times, baseline, stochastic_intensity = run_simulation()
    print(df.head())
    print(f"Total revenue: ${df['Price'].sum():.2f}")
    print(f"Average wait time: {df['WaitTime'].mean():.2f} minutes")
