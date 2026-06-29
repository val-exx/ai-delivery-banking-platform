from __future__ import annotations

import json
import os
from typing import Any

from kafka import KafkaProducer


DEFAULT_PREDICTION_TOPIC = "prediction-events"


def publish_prediction_event(
    *,
    event: dict[str, Any],
    bootstrap_servers: str | None = None,
    topic: str = DEFAULT_PREDICTION_TOPIC,
) -> bool:
    """Publish a prediction event to Kafka when Kafka is configured."""
    kafka_bootstrap_servers = bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS")

    if not kafka_bootstrap_servers:
        return False

    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        key_serializer=lambda value: value.encode("utf-8"),
    )

    producer.send(
        topic,
        key=str(event.get("event_id", "prediction-created")),
        value=event,
    )
    producer.flush()
    producer.close()

    return True