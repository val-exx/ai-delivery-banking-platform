from __future__ import annotations

import os
import unittest
from unittest.mock import patch

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