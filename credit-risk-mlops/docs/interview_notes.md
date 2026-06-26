# Interview Notes

## What did I build?

I built the first part of a credit risk ML pipeline: a synthetic dataset generator for credit applications, with data validation and CSV export.

## Why did I use synthetic data?

I used synthetic data because the project is portfolio-oriented and avoids privacy issues related to real banking data. I still introduced realistic constraints and risk drivers to make the ML task meaningful.

## How is the default target generated?

The `default` target is generated probabilistically. The probability increases when debt-to-income is high, credit score is low, or the requested loan amount is high compared to annual income.

## What assumptions did I make?

I assumed that income, loan amount, and existing debt should have realistic lower bounds. I also assumed that credit risk can be approximated with a simple weighted formula for this first synthetic version.

## What did I test?

I tested the dataset shape, expected columns, unique customer IDs, valid ranges, binary target values, reproducibility with a fixed seed, and CSV export.

## What would I improve in a real banking project?

I would use real approved data sources, stronger data quality checks, bias and fairness analysis, feature versioning, model monitoring, and validation with domain experts.

## What did I learn from EDA?

The EDA showed that the synthetic dataset contains coherent credit risk signals. Customers with `default=1` have lower average credit scores, higher average debt-to-income ratios, lower annual income, and slightly higher loan amounts than customers with `default=0`.

This validates the dataset before model training because the target is not random noise.

## What did I learn from threshold tuning?

The default threshold of 0.5 produced low recall, meaning the model missed many real defaults. By lowering the threshold to 0.3, recall increased from 0.241 to 0.734 and false negatives dropped from 271 to 95.

This improved risk detection but increased false positives, so the threshold should be selected based on business cost trade-offs.

## How did I use MLflow?

I used MLflow with a local SQLite backend to track model experiments. Each run logs parameters such as the decision threshold and metrics such as precision, recall, ROC AUC, false negatives, and false positives.

This makes experiments reproducible and easier to compare.

## How did I expose the model?

I exposed the trained scikit-learn pipeline through a FastAPI service. The `/predict` endpoint validates the request with Pydantic, computes `debt_to_income`, loads the persisted model, and returns both the default probability and the threshold-based label.

This separates model training from inference and makes the model usable by other applications.

## How did I test the API?

I used FastAPI `TestClient` to test the API without manually starting the server. The tests verify that `/health` returns a valid service status and that `/predict` accepts a valid credit application payload and returns the expected prediction fields.

This helps catch regressions when the API or inference logic changes.

## How did I containerize the API?

I created a Dockerfile for the FastAPI prediction service using Python 3.10. The image installs the project dependencies, includes the trained model artifact, sets the correct `PYTHONPATH`, and starts Uvicorn on port 8000.

I tested the container by mapping host port 8001 to container port 8000 and calling `/health`, `/docs`, and `/predict`.

This makes the service more reproducible and prepares it for future deployment on Kubernetes or OpenShift.

## How did I persist prediction audits?

I added a PostgreSQL-backed audit trail for model predictions. After each successful `/predict` request, the API stores the input features, default probability, predicted label, decision threshold, and timestamp in the `prediction_audit` table.

I used SQLAlchemy as the ORM and psycopg as the PostgreSQL driver. Persisting predictions supports traceability, debugging, and future monitoring of model behavior.

## How did I orchestrate the API and database?

I used Docker Compose to run the FastAPI service and PostgreSQL database as separate containers. The API receives its database connection string through the `DATABASE_URL` environment variable and connects to the database through the internal Docker service name `db`.

This setup separates responsibilities: the API serves predictions, while PostgreSQL persists audit data.

## How did I make service startup more reliable?

I configured a PostgreSQL health check using `pg_isready` and made the API depend on the database becoming healthy.

This prevents the API from starting before PostgreSQL is ready to accept connections. It is a small but important reliability practice for containerized services.