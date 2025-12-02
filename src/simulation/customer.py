import simpy
import pandas as pd
import numpy as np
from simulation.order import sample_order, ORDERS


def calc_patience():
    """
    Calculate customer patience based on order statistics.
    Here we use a normal distribution centered around
    2.5 times the average mean service time, with std dev
    as 0.5 times the average mean service time.
    """

    mean_service_times = [v["mean_service"] for v in ORDERS.values()]
    likeliness_weights = [v["likeliness"] for v in ORDERS.values()]
    AVG_MEAN_SERVICE = np.average(mean_service_times, weights=likeliness_weights)

    return AVG_MEAN_SERVICE

# --- Arrival Cox Process ---
def simulate_cox_process(T=480, dt=1, b_rate=5, m_int=10.0, l_int=8.0, rand_int=2.0, m_dur=60, l_dur=90):
    times = np.arange(0, T, dt)

    # Morning + lunch peaks (baseline intensity)
    baseline = b_rate + m_int*np.exp(-((times-120)**2)/(2*m_dur**2))  
    baseline += l_int*np.exp(-((times-300)**2)/(2*l_dur**2))

    # Add randomness (Gamma distributed intensity)
    stochastic_intensity = np.random.gamma(shape=rand_int, scale=baseline/2)

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

    # Customer patience based on drink service stats
    patience = np.random.normal(
        loc=calc_patience() * 2.5,
        scale=calc_patience() * 0.5
    )

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
