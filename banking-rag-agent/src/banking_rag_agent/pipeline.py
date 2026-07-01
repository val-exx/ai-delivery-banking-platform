from __future__ import annotations

from pathlib import Path
from typing import Any

from banking_rag_agent.answering import build_answer
from banking_rag_agent.llm_adapter import LlmFunction
from banking_rag_agent.retrieval import load_documents, search_documents


def answer_question(
    *,
    query: str,
    documents_path: str | Path,
    top_k: int = 2,
    llm_function: LlmFunction | None = None,
) -> dict[str, Any]:
    """Answer a banking question using retrieved document context."""
    documents = load_documents(documents_path)
    retrieved_documents = search_documents(
        query=query,
        documents=documents,
        top_k=top_k,
    )

    return build_answer(
        query=query,
        retrieved_documents=retrieved_documents,
        llm_function=llm_function,
    )