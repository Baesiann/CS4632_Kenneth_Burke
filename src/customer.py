import simpy
import pandas as pd
import numpy as np
from order import sample_order

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
def customer(env, customer_id, arrival_time, baristas, records):
    # Wait until arrival time
    yield env.timeout(arrival_time - env.now)

    arrival = env.now

    order_type, price, service_time = sample_order()

    # Request a barista
    with baristas.request() as req:
        yield req  # wait until a barista is available
        start_service = env.now

        yield env.timeout(service_time)
        end_service = env.now

        records.append({
            "CustomerID": customer_id,
            "OrderType": order_type,
            "Price" : price,
            "ArrivalTime": arrival,
            "StartService": start_service,
            "EndService": end_service,
            "WaitTime": start_service - arrival,
            "ServiceTime": service_time,
            "TotalTime": end_service - arrival
        })
