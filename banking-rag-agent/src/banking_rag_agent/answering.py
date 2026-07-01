from __future__ import annotations

from typing import Any


def build_answer(query: str, retrieved_documents: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a simple grounded answer from retrieved documents."""
    if not retrieved_documents:
        return {
            "answer": "I could not find relevant banking documents for this question.",
            "citations": [],
        }

    main_document = retrieved_documents[0]

    return {
        "answer": (
            f"Based on {main_document['title']}, "
            f"{main_document['text']}"
        ),
        "citations": [
            {
                "doc_id": document["doc_id"],
                "title": document["title"],
            }
            for document in retrieved_documents
        ],
    }