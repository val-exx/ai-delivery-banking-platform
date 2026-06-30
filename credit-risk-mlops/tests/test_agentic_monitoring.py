from __future__ import annotations

import unittest

from credit_risk_mlops.agentic_monitoring import assess_metrics, format_report


class AgenticMonitoringTest(unittest.TestCase):
    def test_assesses_critical_risk(self) -> None:
        metrics = {
            "prediction_count": 10,
            "default_rate": 0.8,
        }

        assessment = assess_metrics(metrics)

        self.assertEqual(assessment["risk_level"], "critical")
        self.assertEqual(assessment["prediction_count"], 10)

    def test_assesses_warning_risk(self) -> None:
        metrics = {
            "prediction_count": 10,
            "default_rate": 0.6,
        }

        assessment = assess_metrics(metrics)

        self.assertEqual(assessment["risk_level"], "warning")

    def test_formats_report(self) -> None:
        assessment = {
            "risk_level": "warning",
            "prediction_count": 10,
            "default_rate": 0.6,
            "recommended_actions": ["monitor the next batch of predictions"],
        }

        report = format_report(assessment)

        self.assertIn("Risk level: warning", report)
        self.assertIn("Prediction count: 10", report)
        self.assertIn("- monitor the next batch of predictions", report)