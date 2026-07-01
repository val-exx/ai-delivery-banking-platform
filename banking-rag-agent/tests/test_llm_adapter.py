from __future__ import annotations

import unittest

from banking_rag_agent.llm_adapter import build_llm_answer


class LlmAdapterTest(unittest.TestCase):
    def test_returns_none_without_llm_function(self) -> None:
        answer = build_llm_answer(
            query="What is required for a personal loan?",
            retrieved_documents=[
                {
                    "doc_id": "DOC-003",
                    "title": "Personal Loan Requirements",
                    "text": "Personal loan applications require proof of income.",
                }
            ],
            llm_function=None,
        )

        self.assertIsNone(answer)

    def test_uses_llm_function_when_available(self) -> None:
        def fake_llm(query, documents):
            return f"Generated answer for: {query}"

        answer = build_llm_answer(
            query="What is required for a personal loan?",
            retrieved_documents=[
                {
                    "doc_id": "DOC-003",
                    "title": "Personal Loan Requirements",
                    "text": "Personal loan applications require proof of income.",
                }
            ],
            llm_function=fake_llm,
        )

        self.assertEqual(
            answer,
            "Generated answer for: What is required for a personal loan?",
        )