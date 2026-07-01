from __future__ import annotations

from typing import Any

from banking_rag_agent.llm_adapter import LlmFunction, build_llm_answer


def build_answer(
    query: str,
    retrieved_documents: list[dict[str, Any]],
    llm_function: LlmFunction | None = None,
) -> dict[str, Any]:
    """Build a grounded answer from retrieved documents."""
    if not retrieved_documents:
        return {
            "answer": "I could not find relevant banking documents for this question.",
            "citations": [],
        }

    llm_answer = build_llm_answer(
        query=query,
        retrieved_documents=retrieved_documents,
        llm_function=llm_function,
    )

    main_document = retrieved_documents[0]
    answer = llm_answer or (
        f"Based on {main_document['title']}, "
        f"{main_document['text']}"
    )

    return {
        "answer": answer,
        "citations": [
            {
                "doc_id": document["doc_id"],
                "title": document["title"],
            }
            for document in retrieved_documents
        ],
    }