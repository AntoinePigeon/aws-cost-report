from unittest.mock import patch
from data_source import parse_cost_response, get_aws_data

SAMPLE = {
    "ResultsByTime": [
        {
            "TimePeriod": {"Start": "2026-01-01", "End": "2026-01-02"},
            "Groups": [
                {"Keys": ["Amazon EC2"], "Metrics": {"UnblendedCost": {"Amount": "123.4561", "Unit": "USD"}}},
                {"Keys": ["Amazon S3"],  "Metrics": {"UnblendedCost": {"Amount": "12.30", "Unit": "USD"}}},
            ],
        },
        {
            "TimePeriod": {"Start": "2026-01-02", "End": "2026-01-03"},
            "Groups": [
                {"Keys": ["Amazon EC2"], "Metrics": {"UnblendedCost": {"Amount": "130.10", "Unit": "USD"}}},
                {"Keys": ["Amazon S3"],  "Metrics": {"UnblendedCost": {"Amount": "11.50", "Unit": "USD"}}},
            ],
        },
    ]
}

def test_parse_cost_response():
    df = parse_cost_response(SAMPLE)
    assert len(df) == 4
    assert list(df.columns) == ["date", "service", "cost"]
    assert df.iloc[0]["cost"] == 123.46

def test_get_aws_data_uses_client_without_real_call():
    with patch("data_source.boto3.client") as mock_client:
        mock_client.return_value.get_cost_and_usage.return_value = SAMPLE
        df = get_aws_data("2026-01-01", "2026-01-03")
    assert len(df) == 4
    assert df.iloc[0]["service"] == "Amazon EC2"
    mock_client.assert_called_once_with("ce")