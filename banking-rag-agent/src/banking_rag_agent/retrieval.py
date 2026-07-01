from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "can",
    "do",
    "for",
    "how",
    "i",
    "in",
    "is",
    "of",
    "the",
    "to",
    "what",
}


def tokenize(text: str) -> set[str]:
    """Convert text into useful lowercase words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {word for word in words if word not in STOPWORDS}


def load_documents(path: str | Path) -> list[dict[str, Any]]:
    """Load banking documents from a JSON Lines file."""
    documents = []

    for line in Path(path).read_text(encoding="utf-8").splitlines():
        documents.append(json.loads(line))

    return documents


def score_document(query: str, document: dict[str, Any]) -> int:
    """Score a document by counting useful query words found in it."""
    query_words = tokenize(query)
    document_words = tokenize(f"{document['title']} {document['text']}")

    return len(query_words & document_words)


def search_documents(
    query: str,
    documents: list[dict[str, Any]],
    top_k: int = 2,
) -> list[dict[str, Any]]:
    """Return the most relevant documents for a query."""
    scored_documents = []

    for document in documents:
        score = score_document(query, document)

        if score > 0:
            scored_documents.append(
                {
                    "doc_id": document["doc_id"],
                    "title": document["title"],
                    "text": document["text"],
                    "score": score,
                }
            )

    return sorted(
        scored_documents,
        key=lambda document: document["score"],
        reverse=True,
    )[:top_k]