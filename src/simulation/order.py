import numpy as np

# Dictionary of orders with deviation
ORDERS = {
    "coffee": {"price": 3.0, "mean_service": 2, "std_service": 0.5},
    "latte": {"price": 4.5, "mean_service": 4, "std_service": 1},
    "frappuccino": {"price": 6.0, "mean_service": 6, "std_service": 1.5},
}


def sample_order():
    # Randomly choose an order type with probability weights
    order_type = np.random.choice(
        list(ORDERS.keys()),
        p=[0.5, 0.3, 0.2]  # probabilities (50% coffee, 30% latte, 20% frap)
    )
    order = ORDERS[order_type]
    # Draw a service time from normal distribution, clipped at >0
    service_time = max(0.5, np.random.normal(order["mean_service"], order["std_service"]))
    return order_type, order["price"], service_time
 
