from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

from credit_risk_mlops.database import create_session_factory, save_prediction_audit
from credit_risk_mlops.events import publish_prediction_event
from credit_risk_mlops.inference import predict_default_label, predict_default_probability

MODEL_PATH = Path("credit-risk-mlops/models/baseline_logistic_regression.joblib")
THRESHOLD = 0.3

DATABASE_URL = os.getenv("DATABASE_URL")
SessionFactory = create_session_factory(DATABASE_URL) if DATABASE_URL else None

app = FastAPI(title="Credit Risk MLOps API")


class CreditApplication(BaseModel):
    age: int = Field(ge=18, le=75)
    annual_income: float = Field(gt=0)
    employment_years: int = Field(ge=0)
    loan_amount: float = Field(gt=0)
    loan_term_months: int = Field(gt=0)
    credit_score: int = Field(ge=300, le=850)
    existing_debt: float = Field(ge=0)


class PredictionResponse(BaseModel):
    default_probability: float
    default_label: int
    threshold: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(application: CreditApplication) -> PredictionResponse:
    application_data = application.model_dump()
    application_data["debt_to_income"] = application.existing_debt / application.annual_income

    probability = predict_default_probability(MODEL_PATH, application_data)
    label = predict_default_label(MODEL_PATH, application_data, threshold=THRESHOLD)

    if SessionFactory is not None:
        with SessionFactory() as session:
            save_prediction_audit(
                session=session,
                application_data=application_data,
                default_probability=probability,
                default_label=label,
                threshold=THRESHOLD,
            )

    publish_prediction_event(
        event={
            "event_id": f"prediction-{uuid4()}",
            "event_type": "prediction_created",
            "application": application_data,
            "default_probability": probability,
            "default_label": label,
            "threshold": THRESHOLD,
        }
    )

    return PredictionResponse(
        default_probability=probability,
        default_label=label,
        threshold=THRESHOLD,
    )