from __future__ import annotations

from pathlib import Path

import mlflow

from credit_risk_mlops.modeling import TrainingResult


def configure_mlflow(tracking_dir: str | Path, experiment_name: str) -> None:
    tracking_path = Path(tracking_dir)
    tracking_path.mkdir(parents=True, exist_ok=True)

    db_path = (tracking_path / "mlflow.db").resolve()
    mlflow.set_tracking_uri(f"sqlite:///{db_path.as_posix()}")
    mlflow.set_experiment(experiment_name)


def log_training_run(
    result: TrainingResult,
    params: dict[str, float | int | str],
    run_name: str,
) -> str:
    with mlflow.start_run(run_name=run_name) as run:
        mlflow.log_params(params)
        mlflow.log_metrics(result.metrics)

        return run.info.run_id