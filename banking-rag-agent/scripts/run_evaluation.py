from __future__ import annotations

import argparse
from pathlib import Path

from banking_rag_agent.evaluation import evaluate_retrieval


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate retrieval quality on banking RAG questions."
    )
    parser.add_argument(
        "--documents",
        default="banking-rag-agent/data/banking_documents.jsonl",
        help="Path to banking documents JSONL.",
    )
    parser.add_argument(
        "--evaluation",
        default="banking-rag-agent/data/evaluation_questions.jsonl",
        help="Path to evaluation questions JSONL.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    result = evaluate_retrieval(
        documents_path=Path(args.documents),
        evaluation_path=Path(args.evaluation),
    )

    print(f"total: {result['total']}")
    print(f"correct: {result['correct']}")
    print(f"accuracy: {result['accuracy']:.3f}")


if __name__ == "__main__":
    main()