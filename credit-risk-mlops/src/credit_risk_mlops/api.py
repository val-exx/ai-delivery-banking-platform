from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from credit_risk_mlops.inference import predict_default_label, predict_default_probability


MODEL_PATH = Path("credit-risk-mlops/models/baseline_logistic_regression.joblib")
THRESHOLD = 0.3

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
    application_data["debt_to_income"] = (
        application.existing_debt / application.annual_income
    )

    probability = predict_default_probability(MODEL_PATH, application_data)
    label = predict_default_label(MODEL_PATH, application_data, threshold=THRESHOLD)

    return PredictionResponse(
        default_probability=probability,
        default_label=label,
        threshold=THRESHOLD,
    )