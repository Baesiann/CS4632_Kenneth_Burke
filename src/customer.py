import simpy
import pandas as pd
import numpy as np

# --- Arrival Cox Process ---
def simulate_cox_process(T=480, dt=1):
    times = np.arange(0, T, dt)

    # Morning + lunch peaks (baseline intensity)
    baseline = 5 + 10*np.exp(-((times-120)**2)/(2*60**2))  
    baseline += 8*np.exp(-((times-300)**2)/(2*90**2))

    # Add randomness (Gamma distributed intensity)
    stochastic_intensity = np.random.gamma(shape=2, scale=baseline/2)

    # Generate arrivals
    arrivals = []
    for t, lam in zip(times, stochastic_intensity):
        n = np.random.poisson(lam * dt / 60)  # arrivals per step
        arrivals.extend([t] * n)

    return arrivals, times, baseline, stochastic_intensity


# --- Customer process ---
def customer(env, customer_id, arrival_time, records):
    yield env.timeout(arrival_time - env.now)  # wait until arrival time
    records.append({"CustomerID": customer_id, "ArrivalTime": env.now})


# --- Simulation ---
def run_simulation():
    env = simpy.Environment()
    arrivals, times, baseline, stochastic_intensity = simulate_cox_process()

    records = []
    for cid, at in enumerate(arrivals, start=1):
        env.process(customer(env, cid, at, records))

    env.run(until=max(arrivals))  # run until last arrival
    return pd.DataFrame(records), times, baseline, stochastic_intensity


# --- Run ---
df, times, baseline, stochastic_intensity = run_simulation()
print(df.head())
print(f"Total customers: {len(df)}")
