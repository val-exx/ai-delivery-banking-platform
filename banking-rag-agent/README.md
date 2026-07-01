# Banking RAG Agent

This module implements a small, testable Retrieval-Augmented Generation workflow for synthetic banking documents.

The current version is intentionally deterministic: it does not call a real LLM provider yet. The goal is to make retrieval, grounding, citations, guardrails, evaluation, and graph orchestration clear before adding external model calls.

## Current Scope

Implemented features:

- synthetic banking document collection;
- keyword-based retrieval with stopword filtering;
- grounded answer builder with citations;
- optional LLM adapter with deterministic fallback;
- LangGraph-style workflow with explicit retrieve, answer, and validate nodes;
- real LangGraph workflow using the same node logic;
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

LangGraph-style workflow:

```text
state
  -> retrieve_node
  -> answer_node
  -> validate_node
  -> response
```

Real LangGraph workflow:

```text
START
  -> retrieve
  -> answer
  -> validate
  -> END
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

## Run Graph Workflow

```powershell
$env:PYTHONPATH="banking-rag-agent/src"
python banking-rag-agent/scripts/run_graph.py "What is required for a personal loan?"
```

Example output:

```text
Based on Personal Loan Requirements, Personal loan applications require proof of income, identity verification, and an affordability assessment based on existing debt and income.

Citations:
- DOC-003: Personal Loan Requirements
```

## Run LangGraph Workflow

```powershell
$env:PYTHONPATH="banking-rag-agent/src"
python banking-rag-agent/scripts/run_langgraph.py "What is required for a personal loan?"
```

This runs the same RAG nodes through a compiled LangGraph `StateGraph`.

## Design Notes

The retrieval implementation is simple on purpose. It tokenizes text, removes common stopwords, and scores documents by useful word overlap.

This is not semantic search yet. A later version can replace keyword retrieval with embeddings and a vector store while keeping the same pipeline shape.

The LLM integration is also intentionally provider-agnostic. The pipeline accepts an optional `llm_function`, which can generate the answer from the query and retrieved documents. If no function is provided, the system uses the deterministic answer builder.

This keeps the RAG pipeline testable without API keys or network calls, while leaving a clear integration point for a real LLM provider later.

The graph workflow was first implemented manually to make the node/state pattern clear. The real LangGraph workflow reuses the same node logic and moves orchestration to a compiled `StateGraph`.

## Next Steps

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
- LangGraph-style orchestration
- LangGraph StateGraph workflow
- automated RAG evaluation
- testable GenAI service design
