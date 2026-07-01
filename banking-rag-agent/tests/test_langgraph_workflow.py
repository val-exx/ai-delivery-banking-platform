from __future__ import annotations

import unittest
from pathlib import Path

from banking_rag_agent.langgraph_workflow import run_langgraph_rag


DOCUMENTS_PATH = Path("banking-rag-agent/data/banking_documents.jsonl")


class LangGraphWorkflowTest(unittest.TestCase):
    def test_runs_langgraph_rag_with_citations(self) -> None:
        response = run_langgraph_rag(
            query="What is required for a personal loan?",
            documents_path=DOCUMENTS_PATH,
            top_k=1,
        )

        self.assertIn("Personal Loan Requirements", response["answer"])
        self.assertEqual(response["citations"][0]["doc_id"], "DOC-003")

    def test_runs_langgraph_rag_with_optional_llm_function(self) -> None:
        def fake_llm(query, documents):
            return "Generated LangGraph answer."

        response = run_langgraph_rag(
            query="What is required for a personal loan?",
            documents_path=DOCUMENTS_PATH,
            top_k=1,
            llm_function=fake_llm,
        )

        self.assertEqual(response["answer"], "Generated LangGraph answer.")
        self.assertEqual(response["citations"][0]["doc_id"], "DOC-003")