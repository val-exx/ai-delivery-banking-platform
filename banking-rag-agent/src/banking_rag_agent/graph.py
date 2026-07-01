from __future__ import annotations

from pathlib import Path
from typing import Any

from banking_rag_agent.answering import build_answer
from banking_rag_agent.llm_adapter import LlmFunction
from banking_rag_agent.retrieval import load_documents, search_documents


def retrieve_node(state: dict[str, Any]) -> dict[str, Any]:
    """Retrieve documents for the question."""
    documents = load_documents(state["documents_path"])
    retrieved_documents = search_documents(
        query=state["query"],
        documents=documents,
        top_k=state.get("top_k", 2),
    )

    return {
        **state,
        "retrieved_documents": retrieved_documents,
    }


def answer_node(state: dict[str, Any]) -> dict[str, Any]:
    """Build an answer from retrieved documents."""
    response = build_answer(
        query=state["query"],
        retrieved_documents=state["retrieved_documents"],
        llm_function=state.get("llm_function"),
    )

    return {
        **state,
        "response": response,
    }


def validate_node(state: dict[str, Any]) -> dict[str, Any]:
    """Validate whether the answer is grounded in citations."""
    response = state["response"]

    return {
        **state,
        "is_grounded": bool(response["citations"]),
    }


def run_rag_graph(
    *,
    query: str,
    documents_path: str | Path,
    top_k: int = 2,
    llm_function: LlmFunction | None = None,
) -> dict[str, Any]:
    """Run a small LangGraph-style RAG workflow."""
    state = {
        "query": query,
        "documents_path": documents_path,
        "top_k": top_k,
        "llm_function": llm_function,
    }

    state = retrieve_node(state)
    state = answer_node(state)
    state = validate_node(state)

    return state["response"]