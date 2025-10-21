import simpy
import pandas as pd
import numpy as np
from simulation.order import sample_order

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

    # Addition of customer patience: normal distribution of 9 minutes
    patience = np.random.normal(loc=9, scale=2)

    # Request a barista / timeout if patience out
    with baristas.request() as req:
        results = yield req | env.timeout(patience)  # wait until a barista is available
        
        if req in results:  # Customer got a barista
            start_service = env.now
            yield env.timeout(service_time)
            end_service = env.now
            dropped = False
        else:   # Customer left
            start_service = None
            end_service = None
            dropped = True

        records.append({
            "CustomerID": customer_id,
            "OrderType": order_type,
            "Price" : price,
            "ArrivalTime": arrival,
            "StartService": start_service,
            "EndService": end_service,
            "WaitTime": (start_service - arrival) if start_service is not None else patience,
            "ServiceTime": service_time if start_service is not None else 0,
            "TotalTime": (end_service - arrival) if end_service is not None else patience,
            "Dropped": dropped
        })
