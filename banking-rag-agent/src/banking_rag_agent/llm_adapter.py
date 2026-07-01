from __future__ import annotations

from typing import Any, Callable


LlmFunction = Callable[[str, list[dict[str, Any]]], str]


def build_llm_answer(
    *,
    query: str,
    retrieved_documents: list[dict[str, Any]],
    llm_function: LlmFunction | None = None,
) -> str | None:
    """Generate an answer with an optional LLM function."""
    if llm_function is None or not retrieved_documents:
        return None

    return llm_function(query, retrieved_documents)