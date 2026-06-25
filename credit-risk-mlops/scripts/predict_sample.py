from __future__ import annotations

from credit_risk_mlops.inference import predict_default_label, predict_default_probability


MODEL_PATH = "credit-risk-mlops/models/baseline_logistic_regression.joblib"

SAMPLE_APPLICATION = {
    "age": 42,
    "annual_income": 38_000,
    "employment_years": 6,
    "loan_amount": 22_000,
    "loan_term_months": 60,
    "credit_score": 540,
    "existing_debt": 11_000,
    "debt_to_income": 11_000 / 38_000,
}


def main() -> None:
    probability = predict_default_probability(MODEL_PATH, SAMPLE_APPLICATION)
    label = predict_default_label(MODEL_PATH, SAMPLE_APPLICATION, threshold=0.3)

    print("\n=== Sample Credit Application Prediction ===")
    print(f"default_probability: {probability:.3f}")
    print(f"default_label: {label}")


if __name__ == "__main__":
    main()