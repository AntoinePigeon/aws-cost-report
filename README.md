# AWS Cost Report Tool

A Python tool that pulls AWS billing data, analyzes it, and generates an automated cost report. Built as a FinOps automation project: it detects spend anomalies, surfaces cost-optimization opportunities, and produces a clean report on every push through a CI/CD pipeline.

![CI](https://github.com/AntoinePigeon/aws-cost-report/actions/workflows/ci.yml/badge.svg)

## What it does

- **Pulls cost data** from AWS Cost Explorer via `boto3`, broken down by day and by service.
- **Analyzes spend** with pandas: totals, per-service breakdown, daily and monthly trends.
- **Detects anomalies** automatically, flagging any service whose daily cost spikes far above its normal range (3-sigma per service).
- **Surfaces optimization signals**: cost concentration (which services dominate the bill) and month-over-month growth.
- **Generates a Markdown report** ready to read, share, or publish.
- **Runs itself**: a GitHub Actions pipeline runs the test suite and produces a fresh report on every push.

## Why it exists

This project demonstrates end-to-end FinOps automation: Python scripting, AWS SDK integration, data analysis with pandas, automated testing, and a working CI/CD pipeline, all in one piece. It maps directly to the day-to-day work of a cloud cost / infrastructure automation role.

## Tech stack

- **Python 3.12**
- **boto3** for AWS Cost Explorer integration
- **pandas** for data processing and analysis
- **pytest** for testing (including mocked AWS calls)
- **GitHub Actions** for CI/CD
- **tabulate** for Markdown table rendering

## Architecture

The core design decision is a clean separation between **where the data comes from** and **what the analysis does**. The analysis code receives data in a fixed `date / service / cost` shape and does not care whether it came from generated test data or from live AWS. This makes the tool testable, cost-aware, and easy to extend.

```
data source  ->  analysis  ->  report
 (fake or AWS)    (pandas)      (Markdown)
```

- `data_source.py` provides both a **generated data** path (free, for tests, demos, and CI) and a **real AWS** path (`boto3` Cost Explorer). A single switch selects between them.
- `analysis.py` computes every metric and returns clean data structures, never printing.
- `report.py` handles presentation only, turning the analysis results into a Markdown report.

## Project structure

```
aws-cost-report/
├── .github/
│   └── workflows/
│       └── ci.yml            # CI/CD pipeline
├── src/
│   ├── data_source.py        # fake data + real AWS (boto3) + source switch
│   ├── analysis.py           # all pandas analysis functions
│   └── report.py             # builds and saves the Markdown report
├── tests/
│   ├── test_analysis.py      # unit tests for the analysis logic
│   └── test_aws.py           # AWS integration tests (mocked, no real calls)
├── data/                     # generated cost data (fake data)
├── output/                   # generated report (gitignored)
├── pytest.ini                # test configuration
├── requirements.txt          # dependencies
└── README.md
```

## Getting started

**1. Clone and enter the project**

```bash
git clone https://github.com/AntoinePigeon/aws-cost-report.git
cd aws-cost-report
```

**2. Create a virtual environment and install dependencies**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

**Run on generated data (default, free, no AWS needed)**

```bash
python src/data_source.py    # generates data/cost_data.csv
python src/report.py         # writes output/report.md
```

**Run against real AWS Cost Explorer**

Requires AWS credentials configured in `~/.aws/` (via `aws configure` or an IAM user with Cost Explorer read access). Note that each Cost Explorer API call incurs a small charge (about $0.01 per request).

```bash
DATA_SOURCE=aws python src/data_source.py
```

The data source is controlled by the `DATA_SOURCE` environment variable. It defaults to generated data, so real AWS is only ever queried when you explicitly ask for it.

## Testing

```bash
pytest -v
```

The suite covers the analysis logic (totals, per-service spend, concentration, anomaly detection) and the AWS integration. The AWS tests use **mocking** to verify the `boto3` code parses Cost Explorer responses correctly **without making any real, paid API calls**.

## CI/CD pipeline

On every push and pull request to `main`, GitHub Actions:

1. Checks out the code on a fresh Ubuntu runner.
2. Installs dependencies from `requirements.txt`.
3. Runs the full pytest suite.
4. Generates the cost report and uploads it as a downloadable artifact.

The report is produced only after the tests pass, so a broken build never generates output.

## Design decisions

- **Security**: AWS credentials live in `~/.aws/` and are never committed. The code contains no keys.
- **Cost awareness**: generated data is the default, so development, testing, and CI cost nothing. Live AWS is opt-in.
- **Testability**: the network call is isolated from the parsing logic, and the parsing is tested against sample responses, so the paid AWS path is fully verified for free.
- **Modern pandas**: uses current idioms (`groupby`, `resample`, method chaining) with explicit rounding for clean, report-ready numbers.

## Possible extensions

- Add a genuine upward cost trend to the generated data to demo runaway-cost detection.
- Support additional cloud providers (GCP, Azure) behind the same data-source interface.
- Add cost-allocation analysis by tag.
- Schedule the pipeline to run daily and post the report to Slack or email.

## Author

Built by Antoine Pigeon as a FinOps automation portfolio project.
