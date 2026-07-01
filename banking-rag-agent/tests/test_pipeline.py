from __future__ import annotations

import unittest
from pathlib import Path

from banking_rag_agent.pipeline import answer_question


DOCUMENTS_PATH = Path("banking-rag-agent/data/banking_documents.jsonl")


class PipelineTest(unittest.TestCase):
    def test_answers_question_with_citation(self) -> None:
        response = answer_question(
            query="What is required for a personal loan?",
            documents_path=DOCUMENTS_PATH,
            top_k=1,
        )

        self.assertIn("Personal Loan Requirements", response["answer"])
        self.assertEqual(response["citations"][0]["doc_id"], "DOC-003")

    def test_returns_fallback_when_question_has_no_source(self) -> None:
        response = answer_question(
            query="How can I invest in cryptocurrency?",
            documents_path=DOCUMENTS_PATH,
            top_k=1,
        )

        self.assertIn("could not find relevant", response["answer"])
        self.assertEqual(response["citations"], [])

    def test_answers_question_with_optional_llm_function(self) -> None:
        def fake_llm(query, documents):
            return "Generated answer from optional LLM."

        response = answer_question(
            query="What is required for a personal loan?",
            documents_path=DOCUMENTS_PATH,
            top_k=1,
            llm_function=fake_llm,
        )

        self.assertEqual(response["answer"], "Generated answer from optional LLM.")
        self.assertEqual(response["citations"][0]["doc_id"], "DOC-003")