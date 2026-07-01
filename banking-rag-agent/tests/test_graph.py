from __future__ import annotations

import unittest
from pathlib import Path

from banking_rag_agent.graph import run_rag_graph


DOCUMENTS_PATH = Path("banking-rag-agent/data/banking_documents.jsonl")


class GraphTest(unittest.TestCase):
    def test_runs_rag_graph_with_citations(self) -> None:
        response = run_rag_graph(
            query="What is required for a personal loan?",
            documents_path=DOCUMENTS_PATH,
            top_k=1,
        )

        self.assertIn("Personal Loan Requirements", response["answer"])
        self.assertEqual(response["citations"][0]["doc_id"], "DOC-003")

    def test_runs_rag_graph_with_optional_llm_function(self) -> None:
        def fake_llm(query, documents):
            return "Generated graph answer."

        response = run_rag_graph(
            query="What is required for a personal loan?",
            documents_path=DOCUMENTS_PATH,
            top_k=1,
            llm_function=fake_llm,
        )

        self.assertEqual(response["answer"], "Generated graph answer.")
        self.assertEqual(response["citations"][0]["doc_id"], "DOC-003")

    def test_returns_fallback_when_graph_has_no_source(self) -> None:
        response = run_rag_graph(
            query="How can I invest in cryptocurrency?",
            documents_path=DOCUMENTS_PATH,
            top_k=1,
        )

        self.assertIn("could not find relevant", response["answer"])
        self.assertEqual(response["citations"], [])