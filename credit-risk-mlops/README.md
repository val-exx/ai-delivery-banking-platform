# Credit Risk MLOps

This module implements the first stages of an end-to-end credit risk machine learning workflow for a synthetic banking dataset.

## Current Scope

The current version covers synthetic data generation, EDA, baseline model training, experiment tracking, model persistence, inference, a FastAPI prediction service, PostgreSQL-backed prediction auditing, Kafka prediction events, Docker Compose orchestration, and basic Kubernetes deployment manifests.

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
- Kafka prediction event publishing;
- Kafka UI for local topic and message inspection;
- Docker Compose orchestration for the API and database;
- database health checks to coordinate service startup;
- Kubernetes `Deployment` and `Service` manifests for the API;
- GitHub Container Registry image publishing;
- Kubernetes private registry authentication with `imagePullSecrets`;
- local Kubernetes inference testing through `kubectl port-forward`.

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

## Docker Compose, Prediction Auditing, and Kafka Events

The API, PostgreSQL database, Kafka broker, and Kafka UI can be run together with Docker Compose:

```powershell
docker compose up --build
```

The API is available at:
```
http://127.0.0.1:8001/docs
```
The API container receives the database connection string through the `DATABASE_URL` environment variable. Inside the Docker Compose network, the API connects to PostgreSQL using the service name `db`.

The API container also receives Kafka configuration through:

```yaml
KAFKA_BOOTSTRAP_SERVERS: kafka:9092
```

Inside Docker Compose, the API connects to Kafka using the service name `kafka`.

Each successful `/predict` request is stored in the `prediction_audit` table. The audit record includes the input features, predicted default probability, predicted label, decision threshold, and creation timestamp.

Each successful `/predict` request also publishes a Kafka event to the `prediction-events` topic when Kafka is configured. This makes the prediction available to downstream systems without tightly coupling those systems to the API.

PostgreSQL exposes a health check based on `pg_isready`. Docker Compose starts the API only after the database service becomes healthy.

### Kafka Setup

Kafka is used as an event broker. In this project, the FastAPI service acts as a Kafka producer:

```text
POST /predict
  -> FastAPI computes prediction
  -> PostgreSQL stores audit record
  -> Kafka receives prediction_created event
  -> downstream consumers can read the event
```

The local topic is:

```text
prediction-events
```

Kafka UI is available at:

```text
http://127.0.0.1:8082
```

Kafka uses two listeners in Docker Compose:

| Listener | Address | Used by |
| --- | --- | --- |
| `INTERNAL` | `kafka:9092` | Containers inside Docker Compose |
| `EXTERNAL` | `localhost:29092` | Python scripts or tools running from the host machine |

This distinction matters because `localhost` means different things depending on where the code runs. From the API container, `localhost` would mean the API container itself, not Kafka. Therefore, the API uses `kafka:9092`.

### Kafka Event Schema

The API publishes events similar to:

```json
{
  "event_id": "prediction-<uuid>",
  "event_type": "prediction_created",
  "application": {
    "age": 42,
    "annual_income": 38000,
    "employment_years": 6,
    "loan_amount": 22000,
    "loan_term_months": 60,
    "credit_score": 540,
    "existing_debt": 11000,
    "debt_to_income": 0.2894736842105263
  },
  "default_probability": 0.4299264096226507,
  "default_label": 1,
  "threshold": 0.3
}
```

The Kafka integration is optional. If `KAFKA_BOOTSTRAP_SERVERS` is not configured, `publish_prediction_event` returns `False` and the API can still serve predictions.

### Manual Kafka Producer Test

From the host machine, Kafka can be tested with:

```powershell
$env:PYTHONPATH="credit-risk-mlops/src"
python -c "from credit_risk_mlops.events import publish_prediction_event; print(publish_prediction_event(event={'event_id':'manual-python-test-1','event_type':'manual_python_test','message':'Kafka producer works from Python'}, bootstrap_servers='localhost:29092'))"
```

Expected result:

```text
True
```

The message can then be inspected in Kafka UI under:

```text
local -> Topics -> prediction-events -> Messages
```

## Kubernetes Manifests

This module includes a minimal Kubernetes configuration for the FastAPI inference service:

| File | Purpose |
| --- | --- |
| `k8s/api-deployment.yaml` | Defines how Kubernetes should run and keep the API container alive |
| `k8s/api-service.yaml` | Exposes the API through a stable Kubernetes Service |

The Kubernetes `Deployment` describes the desired application state:

- run one replica of the credit risk API;
- pull the API image from GitHub Container Registry;
- use the `ghcr.io/val-exx/credit-risk-mlops-api:latest` Docker image;
- authenticate to the private registry with the `ghcr-login` image pull secret;
- expose container port `8000`, where Uvicorn serves FastAPI.

The Kubernetes `Service` exposes the API Pod through a stable network abstraction:

- `selector: app: credit-risk-api` connects the Service to the Pods created by the Deployment;
- `targetPort: 8000` forwards traffic to the FastAPI container;
- `nodePort: 30080` is intended for local cluster access through a NodePort.

### Publish the API Image

Kubernetes should pull the API image from a registry instead of relying on a local Docker image. The image was tagged and pushed to GitHub Container Registry:

```powershell
docker tag credit-risk-mlops-api:latest ghcr.io/val-exx/credit-risk-mlops-api:latest
docker login ghcr.io -u val-exx
docker push ghcr.io/val-exx/credit-risk-mlops-api:latest
```

The GitHub token used for `docker login` must not be committed to the repository.

### Configure Registry Authentication

If the GitHub Container Registry package is private, Kubernetes needs credentials to pull the image. A Docker registry secret can be created locally:

```powershell
kubectl create secret docker-registry ghcr-login `
  --docker-server=ghcr.io `
  --docker-username=val-exx `
  --docker-password=<github-token>
```

The Deployment references this secret through:

```yaml
imagePullSecrets:
  - name: ghcr-login
```

### Deploy to Local Kubernetes

Apply the manifests from the repository root:

```powershell
kubectl apply -f credit-risk-mlops/k8s/api-deployment.yaml
kubectl apply -f credit-risk-mlops/k8s/api-service.yaml
```

Useful inspection commands:

```powershell
kubectl get deployments
kubectl get pods
kubectl get services
kubectl describe pod <pod-name>
```

Expected result:

```text
credit-risk-api-...   1/1   Running
```

### Test Through Port Forwarding

In this Docker Desktop setup, the `NodePort` was created successfully but was not reachable directly through `127.0.0.1:30080`. For local testing, `kubectl port-forward` was used:

```powershell
kubectl port-forward service/credit-risk-api-service 8081:80
```

This creates a temporary tunnel:

```text
localhost:8081 -> Kubernetes Service port 80 -> FastAPI container port 8000
```

Healthcheck:

```text
http://127.0.0.1:8081/health
```

Prediction request:

```powershell
$body = @{
  age = 42
  annual_income = 38000
  employment_years = 6
  loan_amount = 22000
  loan_term_months = 60
  credit_score = 540
  existing_debt = 11000
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8081/predict" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

Example response:

```text
default_probability default_label threshold
------------------- ------------- ---------
0.4299264096226507              1       0.3
```

### Local Docker Desktop Debugging Notes

During local testing with Docker Desktop Kubernetes, the API Pod reached `ErrImageNeverPull` because the Kubernetes node did not see the locally built Docker image:

```text
Container image "credit-risk-mlops-api:latest" is not present with pull policy of Never
```

This is an image visibility issue between the local Docker image store and the Kubernetes cluster image store. It was solved by pushing the image to GitHub Container Registry and updating the Deployment to reference the registry image.

After switching to GHCR, the Pod reached `ImagePullBackOff` with `401 Unauthorized`. This meant Kubernetes could find the registry image, but it was trying to pull it anonymously. The issue was solved by creating a Kubernetes Docker registry secret and referencing it with `imagePullSecrets`.

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
- Kafka
- kafka-python
- Kafka UI
- event-driven architecture
- producer events
- Docker Compose
- service health checks
- prediction audit logging
- Kubernetes
- kubectl
- Deployment manifests
- Service manifests
- GitHub Container Registry
- Kubernetes Secrets
- imagePullSecrets
- port-forwarding
- local Kubernetes deployment debugging
