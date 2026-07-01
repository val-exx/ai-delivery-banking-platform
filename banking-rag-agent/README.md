# Banking RAG Agent

This module implements a small, testable Retrieval-Augmented Generation workflow for synthetic banking documents.

The current version is intentionally deterministic: it does not call an LLM yet. The goal is to make retrieval, grounding, citations, guardrails, and evaluation clear before adding LangGraph or model calls.

## Current Scope

Implemented features:

- synthetic banking document collection;
- keyword-based retrieval with stopword filtering;
- grounded answer builder with citations;
- optional LLM adapter with deterministic fallback;
- fallback response when no relevant source is found;
- retrieval evaluation set;
- automated tests for retrieval, answering, pipeline behavior, guardrails, and evaluation.

## Architecture

```text
user question
  -> load banking documents
  -> retrieve relevant documents
  -> optional LLM answer generation
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

The LLM integration is also intentionally provider-agnostic. The pipeline accepts an optional `llm_function`, which can generate the answer from the query and retrieved documents. If no function is provided, the system uses the deterministic answer builder.

This keeps the RAG pipeline testable without API keys or network calls, while leaving a clear integration point for a real LLM provider later.

## Next Steps

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
- optional LLM adapter
- automated RAG evaluation
- testable GenAI service design
