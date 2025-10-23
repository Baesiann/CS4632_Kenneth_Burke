# Allows for saving simulation runs to a csv for further analysis

import os
import json

def save_to_csv(df, filename):
    # ensure we save inside cafe-simulation/data/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    collection_dir = os.path.join(base_dir, "data")
    os.makedirs(collection_dir, exist_ok=True)   # make folder if missing

    filepath = os.path.join(collection_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"[+] Data saved to {filepath}")

def save_to_json(df, filename):
    # ensure we save inside cafe-simulation/data/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    collection_dir = os.path.join(base_dir, "data")
    os.makedirs(collection_dir, exist_ok=True)  # make folder if missing

    filepath = os.path.join(collection_dir, filename)
    df.to_json(filepath, orient="records", indent=4)
    print(f"[+] Data saved to {filepath}")