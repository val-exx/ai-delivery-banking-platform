from __future__ import annotations

import unittest

from credit_risk_mlops.data_generation import generate_credit_applications
from credit_risk_mlops.eda import (
    dataset_overview,
    default_group_summary,
    numeric_feature_summary,
)


class EdaTest(unittest.TestCase):
    def test_dataset_overview_returns_basic_metrics(self) -> None:
        df = generate_credit_applications(100)

        overview = dataset_overview(df)

        self.assertEqual(overview["rows"], 100)
        self.assertEqual(overview["columns"], 10)
        self.assertIn("default_rate", overview)
        self.assertIn("missing_values", overview)

    def test_numeric_feature_summary_contains_expected_features(self) -> None:
        df = generate_credit_applications(100)

        summary = numeric_feature_summary(df)

        self.assertIn("annual_income", summary.index)
        self.assertIn("credit_score", summary.index)
        self.assertIn("mean", summary.columns)

    def test_default_group_summary_groups_by_target(self) -> None:
        df = generate_credit_applications(1000)

        summary = default_group_summary(df)

        self.assertIn(0, summary.index)
        self.assertIn(1, summary.index)
        self.assertIn("debt_to_income", summary.columns)


if __name__ == "__main__":
    unittest.main()