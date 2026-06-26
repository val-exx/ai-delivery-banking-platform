# Credit Risk MLOps

This module implements the first stages of an end-to-end credit risk machine learning workflow for a synthetic banking dataset.

## Current Scope

The current version covers synthetic data generation, EDA, baseline model training, experiment tracking, model persistence, inference, a FastAPI prediction service, PostgreSQL-backed prediction auditing, and Docker Compose orchestration.

Implemented features:

- reproducible synthetic credit application dataset;
- realistic financial constraints for income, loan amount, and existing debt;
- derived `debt_to_income` feature;
- probabilistic binary `default` target;
- CSV export for downstream ML pipelines;
- unit tests for schema, ranges, reproducibility, and file output;
- EDA utilities for dataset validation;
- baseline Logistic Regression model;
- configurable decision threshold;
- MLflow experiment tracking;
- persisted scikit-learn pipeline with joblib;
- FastAPI prediction service;
- automated API tests;
- PostgreSQL-backed prediction audit trail;
- Docker Compose orchestration for the API and database;
- database health checks to coordinate service startup.

## Dataset Schema

| Column | Description |
| --- | --- |
| `customer_id` | Unique customer identifier |
| `age` | Customer age, between 18 and 75 |
| `annual_income` | Annual income, clipped to a realistic minimum |
| `employment_years` | Number of years employed |
| `loan_amount` | Requested loan amount |
| `loan_term_months` | Loan duration in months |
| `credit_score` | Synthetic credit score between 300 and 850 |
| `existing_debt` | Existing customer debt |
| `debt_to_income` | Ratio between existing debt and annual income |
| `default` | Binary target: 1 means default, 0 means no default |

## Design Assumptions

The default probability is based on three risk drivers:

- higher debt-to-income ratio increases risk;
- lower credit score increases risk;
- higher requested loan amount relative to income increases risk.

The data is synthetic and is intended for portfolio and engineering demonstration purposes, not for real credit decisions.

## Local Usage

From the repository root:

```powershell
$env:PYTHONPATH="credit-risk-mlops/src"
python -c "from credit_risk_mlops.data_generation import save_credit_applications_csv; save_credit_applications_csv('credit-risk-mlops/data/raw/credit_applications.csv', 1000)"
```

## Baseline Model Results

A baseline Logistic Regression model was trained with a configurable decision threshold and tracked with MLflow.

| Threshold | Accuracy | Precision | Recall | False Negatives | False Positives |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.5 | 0.651 | 0.524 | 0.241 | 271 | 78 |
| 0.3 | 0.582 | 0.448 | 0.734 | 95 | 323 |

Lowering the threshold from 0.5 to 0.3 increases recall and reduces false negatives, but it also increases false positives. In a credit risk context, this threshold should be selected based on the business cost of missed defaults versus unnecessary risk flags.

## Experiment Tracking

Experiments are tracked with MLflow using a local SQLite backend.

```powershell
mlflow ui --backend-store-uri sqlite:///credit-risk-mlops/mlruns/mlflow.db
```

The `credit-risk-baseline` experiment compares Logistic Regression runs with different decision thresholds.

## Prediction API

The trained model is exposed through a FastAPI service.

Run the API from the repository root:

```powershell
$env:PYTHONPATH="credit-risk-mlops/src"
uvicorn credit_risk_mlops.api:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | Service healthcheck |
| `/predict` | POST | Predict default probability and label for a credit application |

Example request:

```json
{
  "age": 42,
  "annual_income": 38000,
  "employment_years": 6,
  "loan_amount": 22000,
  "loan_term_months": 60,
  "credit_score": 540,
  "existing_debt": 11000
}
```

Example response:

```json
{
  "default_probability": 0.42,
  "default_label": 1,
  "threshold": 0.3
}
```

## Docker

The FastAPI prediction service can be packaged and run with Docker.

Build the image from the repository root:

```powershell
docker build -f credit-risk-mlops/Dockerfile -t credit-risk-mlops-api .
```

Run the container:

```powershell
docker run --rm -p 8001:8000 credit-risk-mlops-api
```

Healthcheck:

```text
http://127.0.0.1:8001/health
```

Interactive API docs:

```text
http://127.0.0.1:8001/docs
```

The container includes the trained `baseline_logistic_regression.joblib` model artifact and serves predictions through the `/predict` endpoint.

## Docker Compose and Prediction Auditing

The API and PostgreSQL database can be run together with Docker Compose:

```powershell
docker compose up --build
```

The API is available at:
```
http://127.0.0.1:8001/docs
```
The API container receives the database connection string through the `DATABASE_URL` environment variable. Inside the Docker Compose network, the API connects to PostgreSQL using the service name `db`.

Each successful `/predict` request is stored in the `prediction_audit` table. The audit record includes the input features, predicted default probability, predicted label, decision threshold, and creation timestamp.

PostgreSQL exposes a health check based on `pg_isready`. Docker Compose starts the API only after the database service becomes healthy.

## Run Tests

```powershell
$env:PYTHONPATH="credit-risk-mlops/src"
python -m unittest discover -s credit-risk-mlops/tests
```

## Skills Demonstrated

- Python
- pandas
- scikit-learn
- MLflow
- synthetic data generation
- exploratory data analysis
- feature engineering
- model evaluation
- threshold tuning
- MLOps experiment tracking
- FastAPI
- Pydantic
- model serving
- API testing
- Docker
- containerized model serving 
- PostgreSQL
- SQLAlchemy
- psycopg
- Docker Compose
- service health checks
- prediction audit logging
