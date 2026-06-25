from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from credit_risk_mlops.data_generation import generate_credit_applications
from credit_risk_mlops.inference import predict_default_label, predict_default_probability
from credit_risk_mlops.model_persistence import save_model
from credit_risk_mlops.modeling import FEATURE_COLUMNS, train_baseline_model


class InferenceTest(unittest.TestCase):
    def test_predict_default_probability_returns_float_between_zero_and_one(self) -> None:
        df = generate_credit_applications(1000)
        result = train_baseline_model(df)

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = save_model(result.model, Path(tmpdir) / "model.joblib")
            application = df[FEATURE_COLUMNS].iloc[0].to_dict()

            probability = predict_default_probability(model_path, application)

            self.assertIsInstance(probability, float)
            self.assertGreaterEqual(probability, 0.0)
            self.assertLessEqual(probability, 1.0)

    def test_predict_default_label_returns_binary_value(self) -> None:
        df = generate_credit_applications(1000)
        result = train_baseline_model(df)

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = save_model(result.model, Path(tmpdir) / "model.joblib")
            application = df[FEATURE_COLUMNS].iloc[0].to_dict()

            label = predict_default_label(model_path, application, threshold=0.3)

            self.assertIn(label, {0, 1})

if __name__ == "__main__":
    unittest.main()