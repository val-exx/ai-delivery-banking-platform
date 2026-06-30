from __future__ import annotations

import argparse
from pathlib import Path

from credit_risk_mlops.event_consumer import consume_prediction_events_to_jsonl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Consume Kafka prediction events and append them to a JSONL file."
    )
    parser.add_argument(
        "--bootstrap-servers",
        default="localhost:29092",
        help="Kafka bootstrap server reachable from the host machine.",
    )
    parser.add_argument(
        "--output",
        default="credit-risk-mlops/data/events/prediction_events.jsonl",
        help="Output JSON Lines file for consumed prediction events.",
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=10,
        help="Maximum number of Kafka messages to consume before exiting.",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=10000,
        help="Stop waiting after this many milliseconds without new messages.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    consumed_count = consume_prediction_events_to_jsonl(
        output_path=Path(args.output),
        bootstrap_servers=args.bootstrap_servers,
        max_messages=args.max_messages,
        timeout_ms=args.timeout_ms,
    )

    print(f"Consumed {consumed_count} prediction event(s)")
    print(f"Events appended to: {args.output}")


if __name__ == "__main__":
    main()