from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from credit_risk_mlops.data_generation import generate_credit_applications
from credit_risk_mlops.experiment_tracking import configure_mlflow, log_training_run
from credit_risk_mlops.modeling import train_baseline_model


class ExperimentTrackingTest(unittest.TestCase):
    def test_logs_training_run_to_local_mlflow_store(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            tracking_dir = Path(tmpdir) / "mlruns"

            configure_mlflow(
                tracking_dir=tracking_dir,
                experiment_name="test-credit-risk",
            )

            df = generate_credit_applications(1000)
            result = train_baseline_model(df, threshold=0.3)

            run_id = log_training_run(
                result=result,
                params={
                    "n_rows": 1000,
                    "threshold": 0.3,
                    "model_type": "logistic_regression",
                },
                run_name="test-run",
            )

            self.assertIsInstance(run_id, str)
            self.assertTrue((tracking_dir).exists())