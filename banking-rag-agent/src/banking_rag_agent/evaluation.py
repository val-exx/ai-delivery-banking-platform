from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from banking_rag_agent.pipeline import answer_question


def load_evaluation_questions(path: str | Path) -> list[dict[str, Any]]:
    """Load evaluation questions from a JSON Lines file."""
    questions = []

    for line in Path(path).read_text(encoding="utf-8").splitlines():
        questions.append(json.loads(line))

    return questions


def evaluate_retrieval(
    *,
    evaluation_path: str | Path,
    documents_path: str | Path,
) -> dict[str, Any]:
    """Evaluate whether the top citation matches the expected document."""
    questions = load_evaluation_questions(evaluation_path)
    correct = 0

    for item in questions:
        response = answer_question(
            query=item["question"],
            documents_path=documents_path,
            top_k=1,
        )

        top_doc_id = None
        if response["citations"]:
            top_doc_id = response["citations"][0]["doc_id"]

        if top_doc_id == item["expected_doc_id"]:
            correct += 1

    return {
        "total": len(questions),
        "correct": correct,
        "accuracy": correct / len(questions),
    }