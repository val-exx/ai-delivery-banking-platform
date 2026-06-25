from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "age",
    "annual_income",
    "employment_years",
    "loan_amount",
    "loan_term_months",
    "credit_score",
    "existing_debt",
    "debt_to_income",
]

TARGET_COLUMN = "default"


@dataclass(frozen=True)
class TrainingResult:
    model: Pipeline
    metrics: dict[str, float]


def train_baseline_model(df: pd.DataFrame, random_state: int = 42, threshold: float = 0.5) -> TrainingResult:
    if not 0 < threshold < 1:
        raise ValueError("threshold must be between 0 and 1")
    
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=random_state,
        stratify=y,
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "true_negatives": float(tn),
        "false_positives": float(fp),
        "false_negatives": float(fn),
        "true_positives": float(tp),
        "threshold": threshold,
    }

    return TrainingResult(model=model, metrics=metrics)