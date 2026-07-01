from __future__ import annotations

import argparse
from pathlib import Path

from banking_rag_agent.graph import run_rag_graph


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the LangGraph-style banking RAG workflow."
    )
    parser.add_argument(
        "query",
        help="Banking question to answer.",
    )
    parser.add_argument(
        "--documents",
        default="banking-rag-agent/data/banking_documents.jsonl",
        help="Path to banking documents JSONL.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    response = run_rag_graph(
        query=args.query,
        documents_path=Path(args.documents),
        top_k=2,
    )

    print(response["answer"])
    print()
    print("Citations:")
    for citation in response["citations"]:
        print(f"- {citation['doc_id']}: {citation['title']}")


if __name__ == "__main__":
    main()