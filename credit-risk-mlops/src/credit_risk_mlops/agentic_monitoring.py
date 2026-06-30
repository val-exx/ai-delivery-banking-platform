from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_metrics(path: str | Path) -> dict[str, Any]:
    """Load monitoring metrics from a JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def assess_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    """Assess monitoring metrics with simple deterministic rules."""
    default_rate = float(metrics["default_rate"])

    if default_rate >= 0.7:
        risk_level = "critical"
        actions = [
            "review recent prediction events",
            "check whether the model threshold is too low",
        ]
    elif default_rate >= 0.5:
        risk_level = "warning"
        actions = [
            "monitor the next batch of predictions",
            "compare default rate with previous runs",
        ]
    else:
        risk_level = "ok"
        actions = [
            "continue regular monitoring",
        ]

    return {
        "risk_level": risk_level,
        "default_rate": default_rate,
        "prediction_count": int(metrics["prediction_count"]),
        "recommended_actions": actions,
    }


def format_report(assessment: dict[str, Any]) -> str:
    """Format the assessment as a short human-readable report."""
    actions = "\n".join(
        f"- {action}" for action in assessment["recommended_actions"]
    )

    return (
        f"Risk level: {assessment['risk_level']}\n"
        f"Prediction count: {assessment['prediction_count']}\n"
        f"Default rate: {assessment['default_rate']:.3f}\n"
        f"Recommended actions:\n{actions}"
    )