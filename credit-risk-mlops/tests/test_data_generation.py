from __future__ import annotations

import unittest

import pandas as pd
from pathlib import Path

from credit_risk_mlops.data_generation import (
    generate_credit_applications,
    save_credit_applications_csv,
)

class GenerateCreditApplicationsTest(unittest.TestCase):
    def test_generates_requested_number_of_rows(self) -> None:
        df = generate_credit_applications(10)

        self.assertEqual(len(df), 10)

    def test_contains_expected_columns(self) -> None:
        df = generate_credit_applications(10)

        expected_columns = {
            "customer_id",
            "age",
            "annual_income",
            "employment_years",
            "loan_amount",
            "loan_term_months",
            "credit_score",
            "existing_debt",
            "debt_to_income",
            "default",
        }

        self.assertEqual(set(df.columns), expected_columns)

    def test_customer_id_is_unique(self) -> None:
        df = generate_credit_applications(50)

        self.assertTrue(df["customer_id"].is_unique)

    def test_values_are_in_expected_ranges(self) -> None:
        df = generate_credit_applications(100)

        self.assertTrue(df["age"].between(18, 75).all())
        self.assertTrue(df["credit_score"].between(300, 850).all())
        self.assertTrue(df["annual_income"].ge(12_000).all())
        self.assertTrue(df["loan_amount"].ge(1_000).all())
        self.assertTrue(df["existing_debt"].ge(0).all())

    def test_default_is_binary(self) -> None:
        df = generate_credit_applications(100)

        self.assertTrue(set(df["default"]).issubset({0, 1}))

    def test_rejects_non_positive_row_count(self) -> None:
        with self.assertRaises(ValueError):
            generate_credit_applications(0)

    def test_same_seed_generates_same_dataset(self) -> None:
        first = generate_credit_applications(20, seed=123)
        second = generate_credit_applications(20, seed=123)

        self.assertTrue(first.equals(second))

    def test_saves_credit_applications_to_csv(self) -> None:
        output_path = Path("credit-risk-mlops/tmp/test_credit_applications.csv")

        saved_path = save_credit_applications_csv(output_path, n_rows=5)
        saved_df = pd.read_csv(saved_path)

        self.assertEqual(saved_path, output_path)
        self.assertTrue(saved_path.exists())
        self.assertEqual(len(saved_df), 5)


if __name__ == "__main__":
    unittest.main()