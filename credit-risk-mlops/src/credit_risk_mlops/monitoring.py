from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def create_spark_session(app_name: str = "CreditRiskMonitoring") -> SparkSession:
    """Create a local Spark session for prediction monitoring jobs."""
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)

    return (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )


def load_prediction_events(spark: SparkSession, input_path: str | Path) -> DataFrame:
    """Load prediction events from a JSON Lines file."""
    return spark.read.json(str(input_path))


def compute_prediction_metrics(events_df: DataFrame) -> DataFrame:
    """Compute aggregate monitoring metrics from prediction events."""
    return events_df.agg(
        F.count("*").alias("prediction_count"),
        F.avg("default_probability").alias("average_default_probability"),
        F.avg("default_label").alias("default_rate"),
        F.avg("threshold").alias("average_threshold"),
    )


def write_metrics(metrics_df: DataFrame, output_path: str | Path) -> None:
    """Write monitoring metrics as a JSON file.

    Spark computes the metrics, then Python writes the final small report. This
    avoids local Windows Hadoop writer issues while keeping the monitoring
    aggregation itself in Spark.
    """
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics = metrics_df.collect()[0].asDict()
    with (output_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)
        file.write("\n")
