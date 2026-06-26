from __future__ import annotations

import unittest

from credit_risk_mlops.database import create_session_factory, save_prediction_audit


class DatabaseTest(unittest.TestCase):
    def test_save_prediction_audit_persists_record(self) -> None:
        session_factory = create_session_factory("sqlite:///:memory:")

        application_data = {
            "age": 42,
            "annual_income": 38_000,
            "employment_years": 6,
            "loan_amount": 22_000,
            "loan_term_months": 60,
            "credit_score": 540,
            "existing_debt": 11_000,
            "debt_to_income": 11_000 / 38_000,
        }

        with session_factory() as session:
            audit = save_prediction_audit(
                session=session,
                application_data=application_data,
                default_probability=0.43,
                default_label=1,
                threshold=0.3,
            )

            self.assertIsNotNone(audit.id)
            self.assertEqual(audit.default_label, 1)
            self.assertAlmostEqual(audit.default_probability, 0.43)