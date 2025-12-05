# Migrate driver logic from main.py

# imports copied from main.py
import simpy
import pandas as pd
from simulation import schedule_manager
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
    schedule_manager = ScheduleManager(simulate_func=run_simulation_day, base_baristas=base_baristas)
    all_days_data = []

    schedule_manager.history.append((1, schedule_manager.current_baristas))

    for day in range(1, num_days + 1):
        staffing_today = schedule_manager.current_baristas
        print(f"Simulating Day {day} with {staffing_today} baristas")

        env = simpy.Environment()
        collector = DataCollector()

        df, times = run_simulation_day(env, staffing_today, collector, **params)

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

        # Store day and barista count in history
        # schedule_manager.history.append((day, staffing_today))
        if day < num_days:
            next_day_baristas = schedule_manager.optimize_schedule(df, day_number=day + 1)

        all_days_data.append(df)

    print("\n==============================")
    print("   SCHEDULE SUMMARY (FINAL)")
    print("==============================")
    for day, baristas in schedule_manager.history:
        print(f"Day {day}: {baristas} baristas scheduled")

    # Combine all days
    final_df = pd.concat(all_days_data, keys=[f"Day {i}" for i in range(1, num_days + 1)])
    return final_df