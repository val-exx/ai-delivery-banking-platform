from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.pipeline import Pipeline


def save_model(model: Pipeline, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, path)

    return path


def load_model(model_path: str | Path) -> Pipeline:
    return joblib.load(model_path)