# This just defines the resource 

import simpy

def setup_baristas(env, num_baristas=2):
    # Create a barista resource with capacity = num_baristas
    return simpy.Resource(env, capacity=num_baristas)
