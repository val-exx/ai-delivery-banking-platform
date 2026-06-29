from __future__ import annotations

import argparse
from pathlib import Path

from credit_risk_mlops.monitoring import (
    compute_prediction_metrics,
    create_spark_session,
    load_prediction_events,
    write_metrics,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute Spark monitoring metrics from prediction events."
    )
    parser.add_argument(
        "--input",
        default="credit-risk-mlops/data/events/prediction_events.jsonl",
        help="Path to a JSON Lines file containing prediction events.",
    )
    parser.add_argument(
        "--output",
        default="credit-risk-mlops/tmp/monitoring_metrics",
        help="Output folder for the Spark JSON metrics report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    spark = create_spark_session()
    try:
        events_df = load_prediction_events(spark, input_path)
        metrics_df = compute_prediction_metrics(events_df)

        metrics_df.show(truncate=False)
        write_metrics(metrics_df, output_path)
    finally:
        spark.stop()

    print(f"Monitoring metrics written to: {output_path}")


if __name__ == "__main__":
    main()
