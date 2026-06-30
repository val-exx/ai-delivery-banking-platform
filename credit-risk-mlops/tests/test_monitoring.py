from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from credit_risk_mlops.monitoring import (
    compute_prediction_metrics,
    create_spark_session,
    write_metrics,
)


class PredictionMonitoringTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spark = create_spark_session("PredictionMonitoringTest")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.spark.stop()

    def test_computes_prediction_metrics(self) -> None:
        events_df = self.spark.createDataFrame(
            [
                {
                    "event_id": "prediction-1",
                    "event_type": "prediction_created",
                    "default_probability": 0.8,
                    "default_label": 1,
                    "threshold": 0.3,
                },
                {
                    "event_id": "prediction-2",
                    "event_type": "prediction_created",
                    "default_probability": 0.2,
                    "default_label": 0,
                    "threshold": 0.3,
                },
            ]
        )

        metrics = compute_prediction_metrics(events_df).collect()[0].asDict()

        self.assertEqual(metrics["prediction_count"], 2)
        self.assertAlmostEqual(metrics["average_default_probability"], 0.5)
        self.assertAlmostEqual(metrics["default_rate"], 0.5)
        self.assertAlmostEqual(metrics["average_threshold"], 0.3)

    def test_writes_metrics_to_json_file(self) -> None:
        events_df = self.spark.createDataFrame(
            [
                {
                    "event_id": "prediction-1",
                    "event_type": "prediction_created",
                    "default_probability": 0.8,
                    "default_label": 1,
                    "threshold": 0.3,
                }
            ]
        )
        metrics_df = compute_prediction_metrics(events_df)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "metrics"
            write_metrics(metrics_df, output_path)

            metrics = json.loads((output_path / "metrics.json").read_text())

        self.assertEqual(metrics["prediction_count"], 1)
        self.assertAlmostEqual(metrics["average_default_probability"], 0.8)
        self.assertAlmostEqual(metrics["default_rate"], 1.0)
        self.assertAlmostEqual(metrics["average_threshold"], 0.3)

    def test_ignores_non_prediction_events_when_computing_metrics(self) -> None:
        events_df = self.spark.createDataFrame(
            [
                {
                    "event_id": "prediction-1",
                    "event_type": "prediction_created",
                    "default_probability": 0.8,
                    "default_label": 1,
                    "threshold": 0.3,
                    "message": None,
                },
                {
                    "event_id": "manual-test",
                    "event_type": "manual_python_test",
                    "default_probability": None,
                    "default_label": None,
                    "threshold": None,
                    "message": "Kafka producer works from Python",
                },
            ]
        )

        metrics = compute_prediction_metrics(events_df).collect()[0].asDict()

        self.assertEqual(metrics["prediction_count"], 1)
        self.assertAlmostEqual(metrics["average_default_probability"], 0.8)
        self.assertAlmostEqual(metrics["default_rate"], 1.0)
        self.assertAlmostEqual(metrics["average_threshold"], 0.3)