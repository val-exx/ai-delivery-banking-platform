from __future__ import annotations

from pathlib import Path

import pandas as pd

from credit_risk_mlops.model_persistence import load_model
from credit_risk_mlops.modeling import FEATURE_COLUMNS


def predict_default_probability(
    model_path: str | Path,
    application: dict[str, float | int],
) -> float:
    model = load_model(model_path)
    input_df = pd.DataFrame([application])

    probability = model.predict_proba(input_df[FEATURE_COLUMNS])[:, 1][0]

    return float(probability)


def predict_default_label(
    model_path: str | Path,
    application: dict[str, float | int],
    threshold: float = 0.3,
) -> int:
    probability = predict_default_probability(model_path, application)

    return int(probability >= threshold)