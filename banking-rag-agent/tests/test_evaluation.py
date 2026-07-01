from __future__ import annotations

import unittest
from pathlib import Path

from banking_rag_agent.evaluation import (
    evaluate_retrieval,
    load_evaluation_questions,
)


DOCUMENTS_PATH = Path("banking-rag-agent/data/banking_documents.jsonl")
EVALUATION_PATH = Path("banking-rag-agent/data/evaluation_questions.jsonl")


class EvaluationTest(unittest.TestCase):
    def test_loads_evaluation_questions(self) -> None:
        questions = load_evaluation_questions(EVALUATION_PATH)

        self.assertEqual(len(questions), 4)
        self.assertEqual(questions[0]["expected_doc_id"], "DOC-003")

    def test_evaluates_retrieval_accuracy(self) -> None:
        result = evaluate_retrieval(
            evaluation_path=EVALUATION_PATH,
            documents_path=DOCUMENTS_PATH,
        )

        self.assertEqual(result["total"], 4)
        self.assertEqual(result["correct"], 4)
        self.assertEqual(result["accuracy"], 1.0)