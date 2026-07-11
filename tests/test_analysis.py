import pandas as pd
import pytest
from analysis import total_spend, spend_by_service, cost_concentration, find_anomalies

def test_total_spend():
    df = pd.DataFrame({
        "date": ["2026-01-01", "2026-01-01"],
        "service": ["EC2", "S3"],
        "cost": [100.0, 50.0],
    })
    result = total_spend(df)
    assert result == 150.0

def test_spend_by_service():
    df = pd.DataFrame({
        "date": ["2026-01-01", "2026-01-02", "2026-01-01"],
        "service": ["EC2", "EC2", "S3"],
        "cost": [100.0, 50.0, 30.0]
    })
    result = spend_by_service(df)
    assert result["EC2"] == 150.0
    assert result["S3"] == 30.0

def test_cost_concentration():
    df = pd.DataFrame({
        "date": ["2026-01-01", "2026-01-01"],
        "service": ["EC2", "S3"],
        "cost": [70.0, 30.0]
    })
    result = cost_concentration(df)
    assert result["EC2"] == pytest.approx(70.0)
    assert result["S3"] == pytest.approx(30.0)

def test_find_anomalies_catches_spike():
    df = pd.DataFrame({
        "date":    ["2026-01-01"] * 16,
        "service": ["EC2"] * 16,
        "cost":    [100.0] * 15 + [1000.0],
    })
    result = find_anomalies(df)
    assert len(result) == 1
    assert result.iloc[0]["cost"] == 1000.0 

def test_find_anomalies_ignores_normal_data():
    df = pd.DataFrame({
        "date":    ["2026-01-01"] * 5,
        "service": ["EC2"] * 5,
        "cost":    [100.0, 102.0, 98.0, 101.0, 99.0],
    })
    result = find_anomalies(df)
    assert len(result) == 0