from __future__ import annotations

import pandas as pd


def dataset_overview(df: pd.DataFrame) -> dict[str, object]:
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "default_rate": df["default"].mean(),
        "missing_values": df.isna().sum().to_dict(),
    }


def numeric_feature_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = [
        "age",
        "annual_income",
        "employment_years",
        "loan_amount",
        "loan_term_months",
        "credit_score",
        "existing_debt",
        "debt_to_income",
    ]

    return df[numeric_columns].describe().T


def default_group_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("default")[
        [
            "annual_income",
            "loan_amount",
            "credit_score",
            "existing_debt",
            "debt_to_income",
        ]
    ].mean()