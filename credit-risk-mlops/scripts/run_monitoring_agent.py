from __future__ import annotations

import argparse
from pathlib import Path

from credit_risk_mlops.agentic_monitoring import (
    assess_metrics,
    format_report,
    load_metrics,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assess monitoring metrics and print recommended actions."
    )
    parser.add_argument(
        "--metrics",
        default="credit-risk-mlops/tmp/monitoring_metrics/metrics.json",
        help="Path to the monitoring metrics JSON file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    metrics = load_metrics(Path(args.metrics))
    assessment = assess_metrics(metrics)
    report = format_report(assessment)

    print(report)


if __name__ == "__main__":
    main()