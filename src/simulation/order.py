import numpy as np
import json

# Dictionary of orders with deviation
ORDERS = {
    "coffee": {"price": 3.0, "mean_service": 2, "std_service": 0.5, "likeliness":5},
    "latte": {"price": 4.5, "mean_service": 4, "std_service": 1, "likeliness": 3},
    "frappuccino": {"price": 6.0, "mean_service": 6, "std_service": 1.5, "likeliness": 2},
}

with open("../data_management/orders.json") as f:
    ORDERS = json.load(f)

def sample_order():
    # Randomly choose an order type with probability weights
    # Revamp for calculation of likeliness without hardcoding
    if not ORDERS:
        raise ValueError("ORDERS dictionary is empty.")
    
    # Keys and weights
    items = list(ORDERS.keys())
    weights = np.array([ORDERS[item].get("likeliness", 1) for item in items], dtype=float)

    # Normalize
    total = weights.sum()
    if total == 0:
        raise ValueError("All 'likeliness' values are zero, cannot sample.")
    prob = weights / total

    order_type = np.random.choice(
        items,
        p = prob  # modified for gui expansion
    )
    order = ORDERS[order_type]
    # Draw a service time from normal distribution, clipped at >0
    service_time = max(0.5, np.random.normal(order["mean_service"], order["std_service"]))
    return order_type, order["price"], service_time
 
