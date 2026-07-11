import pandas as pd
import random
import os
import boto3

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
        date_str = day.strftime("%Y-%m-%d")
        for service in services:
            factor = random.uniform(0.8, 1.2)
            cost = base_costs[service] * factor

            # Planting the spike (for anomaly detection)
            if service == "Amazon EC2" and date_str == "2026-02-15":
                cost = cost * 6

            data.append({"date": date_str, "service": service, "cost": round(cost, 2)})

    df = pd.DataFrame(data)
    df.to_csv("data/cost_data.csv", index=False)
    return df

def parse_cost_response(response):
    """Turn a Cost Explorer response into a date/service/cost DataFrame. (free)"""
    rows = []
    for period in response["ResultsByTime"]:
        date = period["TimePeriod"]["Start"]
        for group in period["Groups"]:
            service = group["Keys"][0]
            cost = float(group["Metrics"]["UnblendedCost"]["Amount"])
            rows.append({"date": date, "service": service, "cost": round(cost, 2)})
    return pd.DataFrame(rows)

def get_aws_data(start, end):
    """Pull real cost data from AWS Cost Explorer. (Paid)"""
    client = boto3.client("ce")
    response = client.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )
    return parse_cost_response(response)

def get_cost_data():
    """Return a DataFrame from either fake data (free) or real AWS (paid)."""
    source = os.environ.get("DATA_SOURCE", "fake")
    if source == "aws":
        start = os.environ.get("AWS_START", "2026-01-01")
        end = os.environ.get("AWS_END", "2026-04-01")
        return get_aws_data(start, end)
    return generate_data()

if __name__ == "__main__":
    generate_data()