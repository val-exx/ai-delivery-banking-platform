from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from credit_risk_mlops.event_consumer import append_event_to_jsonl
from credit_risk_mlops.events import publish_prediction_event


class PredictionEventsTest(unittest.TestCase):
    def test_returns_false_when_kafka_is_not_configured(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            published = publish_prediction_event(
                event={
                    "event_id": "test-event",
                    "event_type": "prediction_created",
                }
            )

        self.assertFalse(published)

    def test_appends_prediction_event_to_jsonl(self) -> None:
        event = {
            "event_id": "prediction-1",
            "event_type": "prediction_created",
            "default_probability": 0.8,
            "default_label": 1,
            "threshold": 0.3,
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "events" / "prediction_events.jsonl"

            append_event_to_jsonl(event, output_path)

            lines = output_path.read_text(encoding="utf-8").splitlines()

        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0]), event)

    def test_appends_event_on_new_line_when_file_has_no_trailing_newline(self) -> None:
        first_event = {
            "event_id": "prediction-1",
            "event_type": "prediction_created",
        }
        second_event = {
            "event_id": "prediction-2",
            "event_type": "prediction_created",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "events.jsonl"
            output_path.write_text(json.dumps(first_event), encoding="utf-8")

            append_event_to_jsonl(second_event, output_path)

            lines = output_path.read_text(encoding="utf-8").splitlines()

        self.assertEqual(len(lines), 2)
        self.assertEqual(json.loads(lines[0]), first_event)
        self.assertEqual(json.loads(lines[1]), second_event)