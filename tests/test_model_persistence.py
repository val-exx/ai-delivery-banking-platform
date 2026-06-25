from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sklearn.pipeline import Pipeline

from credit_risk_mlops.data_generation import generate_credit_applications
from credit_risk_mlops.model_persistence import load_model, save_model
from credit_risk_mlops.modeling import FEATURE_COLUMNS, train_baseline_model


class ModelPersistenceTest(unittest.TestCase):
    def test_saves_and_loads_model(self) -> None:
        df = generate_credit_applications(1000)
        result = train_baseline_model(df)

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = Path(tmpdir) / "model.joblib"

            saved_path = save_model(result.model, model_path)
            loaded_model = load_model(saved_path)

            self.assertTrue(saved_path.exists())
            self.assertIsInstance(loaded_model, Pipeline)

    def test_loaded_model_can_predict_probabilities(self) -> None:
        df = generate_credit_applications(1000)
        result = train_baseline_model(df)

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = Path(tmpdir) / "model.joblib"
            saved_path = save_model(result.model, model_path)
            loaded_model = load_model(saved_path)

            probabilities = loaded_model.predict_proba(df[FEATURE_COLUMNS].head(5))[:, 1]

            self.assertEqual(len(probabilities), 5)