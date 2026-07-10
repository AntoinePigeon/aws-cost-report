from analysis import load_data, total_spend, cost_concentration, monthly_growth, find_anomalies
import pandas as pd
import os

def build_report(dataframe):
    total = total_spend(dataframe)
    concentration = cost_concentration(dataframe)
    growth = monthly_growth(dataframe)
    anomalies = find_anomalies(dataframe)[["date", "service", "cost"]].copy()
    anomalies["date"] = anomalies["date"].dt.strftime("%Y-%m-%d")

    report = f"""
# AWS Cost Report

## Summary
**Total spend:** ${total:,.2f}

## Cost Concentration (%)
{concentration.to_markdown()}

## Growth per Month
{growth.fillna("-").to_markdown()}

## Anomalies detection
{anomalies.to_markdown(index=False)}

"""
    return report

def save_report(dataframe, path="output/report.md"):
    os.makedirs("output", exist_ok=True)
    report = build_report(dataframe)
    with open("output/report.md", "w") as f:
        f.write(report)
    print(f"Report saved to {path}")

if __name__ == "__main__":
    df = load_data("data/cost_data.csv")
    save_report(df)