from __future__ import annotations

from credit_risk_mlops.data_generation import generate_credit_applications
from credit_risk_mlops.experiment_tracking import configure_mlflow, log_training_run
from credit_risk_mlops.modeling import train_baseline_model
from credit_risk_mlops.model_persistence import save_model

def main() -> None:
    n_rows = 5000
    df = generate_credit_applications(n_rows=n_rows, seed=42)

    configure_mlflow(
        tracking_dir="credit-risk-mlops/mlruns",
        experiment_name="credit-risk-baseline",
    )

    for threshold in [0.5, 0.3]:
        result = train_baseline_model(df, threshold=threshold)

        run_id = log_training_run(
            result=result,
            params={
                "n_rows": n_rows,
                "threshold": threshold,
                "model_type": "logistic_regression",
            },
            run_name=f"logistic-regression-threshold-{threshold}",
        )

        if threshold == 0.3:
            save_model(
                result.model,
                "credit-risk-mlops/models/baseline_logistic_regression.joblib",
            )

        print(f"\n=== Baseline Logistic Regression Metrics threshold={threshold} ===")
        print(f"mlflow_run_id: {run_id}")
        for metric_name, metric_value in result.metrics.items():
            print(f"{metric_name}: {metric_value:.3f}")

if __name__ == "__main__":
    main()