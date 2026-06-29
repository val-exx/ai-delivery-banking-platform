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

## How did I use Kafka?

I added Kafka to publish prediction events after the API serves a `/predict` request. The API still returns the prediction synchronously to the caller, but it also emits an asynchronous event to the `prediction-events` Kafka topic.

The flow is:

```text
POST /predict
  -> FastAPI validates the request
  -> the scikit-learn model returns a probability and label
  -> PostgreSQL stores an audit record
  -> Kafka receives a prediction_created event
```

This introduces an event-driven pattern. Other systems could later consume the Kafka topic for monitoring, dashboards, model drift analysis, alerting, or data lake ingestion without calling the API directly.

## What Kafka concepts did I learn?

I learned the basic Kafka roles:

- a broker is the Kafka server that stores and serves messages;
- a topic is a named stream of events, such as `prediction-events`;
- a producer writes messages to a topic;
- a consumer reads messages from a topic.

In this project, FastAPI is the producer. Kafka UI acted as a simple local consumer and inspection tool.

## Why did Kafka need different internal and external listeners?

When I first tested the Python producer from PowerShell, the producer timed out while fetching Kafka metadata. The issue was that Kafka was advertising the internal Docker address `kafka:9092`, which works for containers but not for programs running directly on the host machine.

I fixed this by configuring two listeners:

```text
INTERNAL: kafka:9092
EXTERNAL: localhost:29092
```

The API container uses `kafka:9092`, while local Python scripts use `localhost:29092`.

This taught me that service addresses depend on where the client is running. `localhost` from my laptop and `localhost` from inside a container are not the same thing.

## How did I make the Kafka integration optional?

The Kafka producer reads the broker address from the `KAFKA_BOOTSTRAP_SERVERS` environment variable. If the variable is missing, the function returns `False` and does not publish anything.

This is intentional because the prediction API should still work when Kafka is not configured, especially during local tests or partial deployments.

I added a unit test to verify this behavior.

## How did I verify Kafka end to end?

I first created the `prediction-events` topic in Kafka UI and produced a manual test message. Then I tested the Python producer directly from PowerShell. Finally, I connected FastAPI to Kafka through Docker Compose by setting:

```text
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

After calling `/predict` through Swagger, Kafka UI showed a new `prediction_created` event in the `prediction-events` topic. This confirmed that the API, Kafka producer, broker, topic, and UI were connected correctly.

## How did I use Spark?

I added a PySpark batch monitoring job for prediction events. The job reads prediction events from a JSON Lines file, loads them into a Spark DataFrame, computes aggregate monitoring metrics, and writes a small JSON report.

The metrics include:

- number of predictions;
- average default probability;
- default rate;
- average decision threshold.

This simulates a Databricks-style monitoring workflow where production prediction logs could be processed on a schedule.

## Why did Spark require Java?

PySpark is the Python API for Spark, but the Spark engine runs on the JVM. When I first ran the monitoring test, Spark failed because Java was missing. Then it failed with Java 8 because the installed Spark version required Java 17.

I installed and configured Temurin JDK 17 and set `JAVA_HOME` so PySpark could start the Java gateway.

This taught me that Spark local development requires both Python and a compatible Java runtime, while managed platforms like Databricks usually provide this runtime environment.

## Why did I configure the PySpark Python executable?

After Java was fixed, Spark still failed because the Python worker could not start. Spark workers were trying to call a generic `python` command instead of the Python interpreter from my virtual environment.

I fixed this by setting `PYSPARK_DRIVER_PYTHON` and `PYSPARK_PYTHON` from `sys.executable` in the Spark session setup. This makes Spark use the same Python interpreter as the active virtual environment.

## How did I handle Spark writing on Windows?

Spark successfully computed the monitoring metrics, but local Spark JSON writing failed on Windows with a Hadoop `NativeIO$Windows.access0` error.

To keep the local job reliable, I kept Spark responsible for the aggregation and used standard Python `json.dump` to write the final small `metrics.json` report.

This is a pragmatic local-development choice. In Databricks or a Linux-based Spark environment, Spark writers would normally be used directly for distributed output.

## How did I start using Kubernetes?

I added a minimal Kubernetes configuration for the FastAPI inference service. The goal was not to train the model on Kubernetes, but to describe how the already containerized API could be deployed and exposed in a cluster.

I created two manifests:

- `api-deployment.yaml`, which tells Kubernetes to run one replica of the API container and keep it alive;
- `api-service.yaml`, which exposes the API through a stable Service and forwards traffic to the FastAPI container port.

The important concept I learned is that a Kubernetes `Deployment` manages application replicas, while a Kubernetes `Service` provides stable network access to the Pods created by that Deployment.

## What Kubernetes issue did I debug locally?

When I first applied the Deployment on Docker Desktop Kubernetes, the Pod did not become ready. By using `kubectl get pods` and `kubectl describe pod`, I found the error:

```text
Container image "credit-risk-mlops-api:latest" is not present with pull policy of Never
```

This means the Kubernetes node could not see the locally built Docker image. The YAML configuration was structurally correct, but the cluster did not have access to the image.

This taught me that Kubernetes does not run source code directly. It runs container images, and the cluster must be able to pull or access the exact image referenced in the Deployment.

## How did I solve image availability for Kubernetes?

I solved the image availability problem by publishing the Docker image to GitHub Container Registry.

I tagged the local image with a registry name:

```text
ghcr.io/val-exx/credit-risk-mlops-api:latest
```

Then I authenticated Docker to GHCR and pushed the image. This changed the deployment flow from relying on a local Docker image to using a registry-based image that Kubernetes could pull.

The deployment flow became:

```text
Dockerfile
  -> Docker image
  -> GitHub Container Registry
  -> Kubernetes Deployment
  -> Running Pod
```

## How did I handle private registry authentication?

After switching the Deployment to use the GHCR image, Kubernetes returned a `401 Unauthorized` error while pulling the image. This happened because Docker was authenticated on my machine, but Kubernetes did not automatically inherit those credentials.

I created a Kubernetes Docker registry secret named `ghcr-login` and referenced it in the Deployment with `imagePullSecrets`.

This taught me that private container registries require explicit authentication inside Kubernetes.

## How did I expose and test the API in Kubernetes?

I created a Kubernetes `Service` of type `NodePort` to expose the FastAPI Pod. The Service maps traffic from Kubernetes to the container port where Uvicorn is running.

In my Docker Desktop setup, the NodePort was created but was not directly reachable from `127.0.0.1`. To test the service locally, I used:

```text
kubectl port-forward service/credit-risk-api-service 8081:80
```

This created a temporary tunnel from my local machine to the Kubernetes Service. I verified both:

- `/health`, to check that the API was alive;
- `/predict`, to check that the API could load the model and return an ML prediction.

The prediction request returned a default probability, a default label, and the model threshold, proving that the inference service was working through Kubernetes.

## What would I improve in a production-like Kubernetes setup?

In a real project, I would use immutable image tags instead of `latest`, configure readiness and liveness probes, externalize configuration through ConfigMaps and Secrets, deploy PostgreSQL as a managed database or with a dedicated Kubernetes setup, and use a proper ingress controller instead of local port-forwarding.

For example, I would reference an immutable image such as:

```text
ghcr.io/val-exx/credit-risk-mlops-api:2026-06-28
```

This would make deployments easier to reproduce and roll back.

## How would I explain the Kubernetes part in an interview?

I would say:

> I containerized a FastAPI machine learning inference service with Docker and deployed it on local Kubernetes. I pushed the image to GitHub Container Registry, configured a Kubernetes image pull secret for private registry authentication, used a Deployment to manage the API Pod, exposed it with a Service, and tested `/health` and `/predict` through `kubectl port-forward`. During the process, I debugged `ErrImageNeverPull`, `ImagePullBackOff`, and a `401 Unauthorized` pull error, which helped me understand how Kubernetes accesses container images and private registries.
