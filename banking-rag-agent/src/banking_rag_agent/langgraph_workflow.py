from __future__ import annotations

from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from banking_rag_agent.graph import answer_node, retrieve_node, validate_node
from banking_rag_agent.llm_adapter import LlmFunction


class RagState(TypedDict, total=False):
    query: str
    documents_path: str | Path
    top_k: int
    llm_function: LlmFunction | None
    retrieved_documents: list[dict[str, Any]]
    response: dict[str, Any]
    is_grounded: bool


def build_rag_app():
    """Build the LangGraph RAG workflow."""
    graph = StateGraph(RagState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)
    graph.add_node("validate", validate_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", "validate")
    graph.add_edge("validate", END)

    return graph.compile()


def run_langgraph_rag(
    *,
    query: str,
    documents_path: str | Path,
    top_k: int = 2,
    llm_function: LlmFunction | None = None,
) -> dict[str, Any]:
    """Run the real LangGraph RAG workflow."""
    app = build_rag_app()

    final_state = app.invoke(
        {
            "query": query,
            "documents_path": documents_path,
            "top_k": top_k,
            "llm_function": llm_function,
        }
    )

    return final_state["response"]