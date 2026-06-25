from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd



def generate_credit_applications(n_rows: int, seed: int = 42) -> pd.DataFrame:
    if n_rows <= 0:
        raise ValueError("n_rows must be positive")
    
    rng = np.random.default_rng(seed)

    data = {
        "customer_id": range(1, n_rows + 1),
        "age": rng.integers(18, 76, size=n_rows),
        "annual_income": rng.normal(45_000, 15_000, size=n_rows).round(2),
        "employment_years": rng.integers(0, 40, size=n_rows),
        "loan_amount": rng.normal(18_000, 8_000, size=n_rows).round(2),
        "loan_term_months": rng.choice([12, 24, 36, 48, 60, 72], size=n_rows),
        "credit_score": rng.integers(300, 851, size=n_rows),
        "existing_debt": rng.normal(8_000, 5_000, size=n_rows).round(2),
    }

    df = pd.DataFrame(data)

    df["annual_income"] = df["annual_income"].clip(lower=12_000)
    df["loan_amount"] = df["loan_amount"].clip(lower=1_000)
    df["existing_debt"] = df["existing_debt"].clip(lower=0)
    df["debt_to_income"] = df["existing_debt"] / df["annual_income"]

    risk_score = (
        0.45 * df["debt_to_income"]
        + 0.35 * (1 - (df["credit_score"] - 300) / 550)
        + 0.20 * (df["loan_amount"] / df["annual_income"])
)

    default_probability = risk_score.clip(0.02, 0.85)
    df["default"] = rng.binomial(1, default_probability)

    return df

#il rischio è più alto se:
# - il debito rispetto al reddito è alto
# - il credit score è basso
# - il prestito richiesto è alto rispetto al redditoù

def save_credit_applications_csv(
    output_path: str | Path,
    n_rows: int,
    seed: int = 42,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    df = generate_credit_applications(n_rows=n_rows, seed=seed)
    df.to_csv(output, index=False)

    return output