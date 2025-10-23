# Migrate driver logic from main.py

# imports copied from main.py
import simpy
import pandas as pd
from simulation.customer import customer
from simulation.barista import setup_baristas
from simulation.customer import simulate_cox_process
from data_management.collector import DataCollector
from data_management.metrics import average_wait_time, total_revenue, throughput, total_dropped
from data_management.export import save_to_csv
from simulation.schedule_manager import ScheduleManager

# single day run copied from main.py
def run_simulation_day(env, num_baristas, collector, **params):
    baristas = setup_baristas(env, num_baristas)
    
    # Pass arrival params to simulate_cox_process
    arrivals, times, *_ = simulate_cox_process(
        b_rate=params.get("baseline_rate", 5.0),
        m_int=params.get("morning_intensity", 10.0),
        l_int=params.get("lunch_intensity", 8.0),
        rand_int=params.get("rand_intensity", 2.0),
        m_dur=params.get("morning_dur", 60),
        l_dur=params.get("lunch_dur", 90)
    )

    # Spawn customers
    for cid, at in enumerate(arrivals, start=1):
        env.process(customer(env, cid, at, baristas, collector.records))

    env.run(until=max(arrivals))

    # Convert to dataframe
    return collector.to_dataframe(), times

# full simulation run mostly copied from main
# added functionality for seed, as well as parameters
def run_full_simulation(
        num_days=7,
        base_baristas=2,
        seed=None,
        **params
):
    if seed:
        import numpy as np
        np.random.seed(seed)
        import random
        random.seed(seed)

    # pass in params weights
    schedule_manager = ScheduleManager(
        base_baristas=base_baristas,
        max_baristas=10,
        w_wait=params.get("w_wait", 1.0),
        w_idle=params.get("w_idle", 1.0),
        w_labor=params.get("w_labor", 1.0),
        w_dropped=params.get("w_dropped", 1.0),
        w_throughput=params.get("w_throughput", 1.0)
    )
    all_days_data = []

    for day in range(1, num_days + 1):
        print(f"Simulating Day {day} with {schedule_manager.current_baristas} baristas")

        env = simpy.Environment()
        collector = DataCollector()

        df, times = run_simulation_day(env, schedule_manager.current_baristas, collector, **params)

        # Compute & print daily metrics
        avg_wait = average_wait_time(df)
        rev = total_revenue(df)
        thpt = throughput(df, total_time=480)
        drop_count = total_dropped(df)

        print(f"Day {day} Summary:")
        print(f" - Average Wait Time: {avg_wait:.2f} min")
        print(f" - Total Revenue: ${rev:.2f}")
        print(f" - Throughput: {thpt:.2f} customers/min")
        print(f" - Dropped: {drop_count} Customers")

        all_days_data.append(df)

        # Call the optimizer for next day
        schedule_manager.optimize_schedule(df)

    # Combine all days
    final_df = pd.concat(all_days_data, keys=[f"Day {i}" for i in range(1, num_days + 1)])
    return final_df