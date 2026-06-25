from __future__ import annotations

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

from credit_risk_mlops.data_generation import generate_credit_applications
from credit_risk_mlops.eda import (
    dataset_overview,
    default_group_summary,
    numeric_feature_summary,
)


def main() -> None:
    df = generate_credit_applications(n_rows=1000, seed=42)

    print("\n=== Dataset Overview ===")
    print(dataset_overview(df))

    print("\n=== Numeric Feature Summary ===")
    print(numeric_feature_summary(df))

    print("\n=== Default Group Summary ===")
    print(default_group_summary(df))


if __name__ == "__main__":
    main()