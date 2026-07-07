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

if __name__ == "__main__":
    df = load_data("data/cost_data.csv")
    print("Total:", total_spend(df))
    print("\nBy service:\n", spend_by_service(df))
    print("\nBy month:\n", spend_by_month(df))
    print("\nFirst 5 days:\n", spend_by_day(df).head())