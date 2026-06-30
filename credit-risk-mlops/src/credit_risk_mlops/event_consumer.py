from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kafka import KafkaConsumer

from credit_risk_mlops.events import DEFAULT_PREDICTION_TOPIC


def append_event_to_jsonl(event: dict[str, Any], output_path: str | Path) -> None:
    """Append one prediction event as a JSON Lines record."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    needs_leading_newline = False
    if path.exists() and path.stat().st_size > 0:
        with path.open("rb") as file:
            file.seek(-1, 2)
            needs_leading_newline = file.read(1) != b"\n"

    with path.open("a", encoding="utf-8") as file:
        if needs_leading_newline:
            file.write("\n")

        file.write(json.dumps(event))
        file.write("\n")


def consume_prediction_events_to_jsonl(
    *,
    output_path: str | Path,
    bootstrap_servers: str = "localhost:29092",
    topic: str = DEFAULT_PREDICTION_TOPIC,
    group_id: str = "credit-risk-monitoring",
    max_messages: int = 10,
    timeout_ms: int = 10000,
) -> int:
    """Consume prediction events from Kafka and append them to a JSONL file."""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=timeout_ms,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    consumed_count = 0

    try:
        for message in consumer:
            append_event_to_jsonl(message.value, output_path)
            consumed_count += 1

            if consumed_count >= max_messages:
                break
    finally:
        consumer.close()

    return consumed_count