def average_wait_time(df):
    return df["WaitTime"].mean()

def average_service_time(df):
    return df["ServiceTime"].mean()

def total_revenue(df):
    return df["Price"].sum()

def throughput(df, total_time):
    return len(df) / total_time  # customers per minute

# Added approximation of idle time
def barista_idle_time(df, num_baristas, day_length=480):
    total_service_time = df["ServiceTime"].sum()
    total_capacity_time = num_baristas * day_length
    idle_time = max(0, total_capacity_time - total_service_time)
    return idle_time

def total_dropped(df):
    if "Dropped" in df.columns:
        return df["Dropped"].sum()
    return 0