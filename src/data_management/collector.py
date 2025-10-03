# Helper class for records dict

import pandas as pd

class DataCollector:
    def __init__(self):
        self.records = []

    def log(self, record: dict):
        # Append a single customer record
        self.records.append(record)

    def to_dataframe(self):
        # Convert to pandas DataFrame
        return pd.DataFrame(self.records)

    def reset(self):
        # Clear all stored records
        self.records = []
