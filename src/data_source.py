import pandas as pd
import random
import os

def generate_data():
    random.seed(42)

    os.makedirs("data", exist_ok=True)

    services = ["Amazon EC2", "Amazon S3", "Amazon RDS", "Amazon DataZone", "Amazon EMR", "Amazon FSx"]
    dates = pd.date_range(start="2026-01-01", periods=90)

    base_costs = {
        "Amazon EC2": 120,
        "Amazon S3": 15,
        "Amazon RDS": 80,
        "Amazon DataZone": 5,
        "Amazon EMR": 100,
        "Amazon FSx": 50,
    }

    data = []

    for day in dates:
        for service in services:
            factor = random.uniform(0.8, 1.2)
            cost = base_costs[service] * factor
            data.append({"date": day.strftime("%Y-%m-%d"), "service": service, "cost": round(cost, 2)})

    df = pd.DataFrame(data)
    df.to_csv("data/cost_data.csv", index=False)

if __name__ == "__main__":
    generate_data()