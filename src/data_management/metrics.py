def average_wait_time(df):
    return df["WaitTime"].mean()

def average_service_time(df):
    return df["ServiceTime"].mean()

def total_revenue(df):
    return df["Price"].sum()

def throughput(df, total_time):
    return len(df) / total_time  # customers per minute
