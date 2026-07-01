# Banking RAG Agent

This module implements a small, testable Retrieval-Augmented Generation workflow for synthetic banking documents.

The current version is intentionally deterministic: it does not call an LLM yet. The goal is to make retrieval, grounding, citations, guardrails, and evaluation clear before adding LangGraph or model calls.

## Current Scope

Implemented features:

- synthetic banking document collection;
- keyword-based retrieval with stopword filtering;
- grounded answer builder with citations;
- fallback response when no relevant source is found;
- retrieval evaluation set;
- automated tests for retrieval, answering, pipeline behavior, guardrails, and evaluation.

## Architecture

```text
user question
  -> load banking documents
  -> retrieve relevant documents
  -> build grounded answer
  -> return answer + citations
```

Evaluation flow:

```text
evaluation_questions.jsonl
  -> answer_question
  -> compare top citation with expected_doc_id
  -> retrieval accuracy
```

## Run Tests

```powershell
$env:PYTHONPATH="banking-rag-agent/src"
python -m unittest discover -s banking-rag-agent/tests
```

## Run Evaluation

```powershell
$env:PYTHONPATH="banking-rag-agent/src"
python banking-rag-agent/scripts/run_evaluation.py
```

Expected output:

```text
total: 4
correct: 4
accuracy: 1.000
```

## Design Notes

The retrieval implementation is simple on purpose. It tokenizes text, removes common stopwords, and scores documents by useful word overlap.

This is not semantic search yet. A later version can replace keyword retrieval with embeddings and a vector store while keeping the same pipeline shape.

## Next Steps

- add an optional LLM answer generator;
- introduce a small LangGraph workflow;
- add stronger guardrails;
- add PostgreSQL or MongoDB-backed tools;
- expand the evaluation set.

## Skills Demonstrated

- RAG fundamentals
- retrieval pipeline
- citations
- grounding
- guardrails
- automated RAG evaluation
- testable GenAI service design
