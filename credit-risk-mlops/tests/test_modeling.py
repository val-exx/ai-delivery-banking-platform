from __future__ import annotations

import unittest

from sklearn.pipeline import Pipeline

from credit_risk_mlops.data_generation import generate_credit_applications
from credit_risk_mlops.modeling import FEATURE_COLUMNS, train_baseline_model


class ModelingTest(unittest.TestCase):
    def test_train_baseline_model_returns_pipeline_and_metrics(self) -> None:
        df = generate_credit_applications(1000)

        result = train_baseline_model(df)

        self.assertIsInstance(result.model, Pipeline)
        self.assertIn("accuracy", result.metrics)
        self.assertIn("precision", result.metrics)
        self.assertIn("recall", result.metrics)
        self.assertIn("roc_auc", result.metrics)
        self.assertIn("true_negatives", result.metrics)
        self.assertIn("false_positives", result.metrics)
        self.assertIn("false_negatives", result.metrics)
        self.assertIn("true_positives", result.metrics)
        self.assertIn("threshold", result.metrics)

    def test_metrics_are_probabilities(self) -> None:
        df = generate_credit_applications(1000)

        result = train_baseline_model(df)

        probability_metrics = ["accuracy", "precision", "recall", "roc_auc", "threshold"]

        for metric_name in probability_metrics:
            self.assertGreaterEqual(result.metrics[metric_name], 0.0)
            self.assertLessEqual(result.metrics[metric_name], 1.0)

    def test_feature_columns_are_present_in_dataset(self) -> None:
        df = generate_credit_applications(100)

        for column in FEATURE_COLUMNS:
            self.assertIn(column, df.columns)

    def test_rejects_invalid_threshold(self) -> None:
        df = generate_credit_applications(1000)

        with self.assertRaises(ValueError):
            train_baseline_model(df, threshold=1.5)

    def test_lower_threshold_increases_or_preserves_recall(self) -> None:
        df = generate_credit_applications(5000)

        default_threshold = train_baseline_model(df, threshold=0.5)
        lower_threshold = train_baseline_model(df, threshold=0.3)

        self.assertGreaterEqual(
            lower_threshold.metrics["recall"],
            default_threshold.metrics["recall"],
        )


if __name__ == "__main__":
    unittest.main()