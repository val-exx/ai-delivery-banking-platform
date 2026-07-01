from __future__ import annotations

import unittest
from pathlib import Path

from banking_rag_agent.retrieval import load_documents, search_documents


DOCUMENTS_PATH = Path("banking-rag-agent/data/banking_documents.jsonl")


class RetrievalTest(unittest.TestCase):
    def test_loads_documents(self) -> None:
        documents = load_documents(DOCUMENTS_PATH)

        self.assertEqual(len(documents), 4)
        self.assertEqual(documents[0]["doc_id"], "DOC-001")

    def test_finds_relevant_loan_document(self) -> None:
        documents = load_documents(DOCUMENTS_PATH)

        results = search_documents(
            query="What documents are required for a personal loan?",
            documents=documents,
            top_k=1,
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["doc_id"], "DOC-003")
        self.assertGreater(results[0]["score"], 0)