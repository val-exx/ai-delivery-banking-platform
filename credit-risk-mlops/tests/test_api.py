from __future__ import annotations

import importlib
import os
import tempfile
from pathlib import Path

import unittest

from fastapi.testclient import TestClient

from credit_risk_mlops.api import app


class ApiTest(unittest.TestCase):
    def test_health_returns_ok(self) -> None:
        client = TestClient(app)

        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_predict_returns_prediction(self) -> None:
        client = TestClient(app)

        payload = {
            "age": 42,
            "annual_income": 38_000,
            "employment_years": 6,
            "loan_amount": 22_000,
            "loan_term_months": 60,
            "credit_score": 540,
            "existing_debt": 11_000,
        }

        response = client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertIn("default_probability", body)
        self.assertIn("default_label", body)
        self.assertEqual(body["threshold"], 0.3)
        self.assertIn(body["default_label"], {0, 1})

    def test_predict_saves_audit_when_database_url_is_configured(self) -> None:
       with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            db_path = Path(tmpdir) / "audit.db"
            os.environ["DATABASE_URL"] = f"sqlite:///{db_path.as_posix()}"

            import credit_risk_mlops.api as api_module

            importlib.reload(api_module)
            client = TestClient(api_module.app)

            payload = {
                "age": 42,
                "annual_income": 38_000,
                "employment_years": 6,
                "loan_amount": 22_000,
                "loan_term_months": 60,
                "credit_score": 540,
                "existing_debt": 11_000,
            }

            response = client.post("/predict", json=payload)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(db_path.exists())

            os.environ.pop("DATABASE_URL", None)
            importlib.reload(api_module)

if __name__ == "__main__":
    unittest.main()