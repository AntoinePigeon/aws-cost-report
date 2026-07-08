import pandas as pd

def load_data(data_path):
    df = pd.read_csv(data_path, parse_dates=["date"])
    return df

def total_spend(dataframe):
    total_cost = dataframe["cost"].sum()
    return round(total_cost, 2)

def spend_by_service(dataframe):
    return (
        dataframe.groupby("service")["cost"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )

def spend_by_day(dataframe):
    return (
        dataframe.groupby("date")["cost"]
        .sum()
        .round(2)
    )

def spend_by_month(dataframe):
    return (
        dataframe.set_index("date").resample("ME")["cost"].sum()
    )

def find_anomalies(dataframe, threshold=3):
    found = []
    for service in dataframe["service"].unique():
        service_rows = dataframe[dataframe["service"] == service]
        upper_limit = service_rows["cost"].mean() + (threshold * service_rows["cost"].std())
        spikes = service_rows[service_rows["cost"] > upper_limit]
        found.append(spikes)
    return pd.concat(found)

def cost_concentration(dataframe):
    totals = spend_by_service(dataframe)
    grand_total = totals.sum()
    return (totals / grand_total * 100).round(1)

def focus_areas(dataframe, min_percent=25):
    concentration = cost_concentration(dataframe)
    return concentration[concentration > min_percent]

def monthly_growth(dataframe):
    dataframe = dataframe.copy()
    dataframe["month"] = dataframe["date"].dt.strftime("%Y-%m")
    pivot = dataframe.pivot_table(
        index="service",
        columns="month",
        values="cost",
        aggfunc="sum",
    )
    return (pivot.pct_change(axis=1) * 100).round(1)

if __name__ == "__main__":
    df = load_data("data/cost_data.csv")
    print("Total:", total_spend(df))
    print("\nConcentration (%):\n", cost_concentration(df))
    print("\nMonthly growth (%):\n", monthly_growth(df))
    print("\nAnomalies:\n", find_anomalies(df))
