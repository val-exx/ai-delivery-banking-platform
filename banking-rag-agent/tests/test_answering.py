from __future__ import annotations

import unittest

from banking_rag_agent.answering import build_answer


class AnsweringTest(unittest.TestCase):
    def test_builds_answer_with_citations(self) -> None:
        documents = [
            {
                "doc_id": "DOC-003",
                "title": "Personal Loan Requirements",
                "text": "Personal loan applications require proof of income.",
                "score": 3,
            }
        ]

        response = build_answer(
            query="What is required for a personal loan?",
            retrieved_documents=documents,
        )

        self.assertIn("Personal Loan Requirements", response["answer"])
        self.assertEqual(response["citations"][0]["doc_id"], "DOC-003")

    def test_returns_fallback_when_no_documents_are_found(self) -> None:
        response = build_answer(
            query="How do I open a business account?",
            retrieved_documents=[],
        )

        self.assertIn("could not find relevant", response["answer"])
        self.assertEqual(response["citations"], [])