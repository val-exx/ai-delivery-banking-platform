# AI Delivery Banking Platform

Portfolio project for a Junior Machine Learning Engineer role focused on ML, Generative AI, Agentic AI, AI-assisted coding, data platforms, and MLOps.

The platform is organized as a monorepo with four modules:

| Module | Purpose | Main skills |
| --- | --- | --- |
| `agenticops-toolkit` | Standards, prompts, templates, and CI practices for AI-assisted development | AI-assisted coding, DevOps, MLOps, CI/CD |
| `credit-risk-mlops` | End-to-end credit risk and fraud ML platform | Python, pandas, Spark, scikit-learn, MLflow, PostgreSQL |
| `banking-rag-agent` | Banking assistant based on RAG and agentic workflows | GenAI, LangGraph, PostgreSQL, MongoDB, evaluations |
| `customer-intelligence-streaming` | Real-time customer intelligence pipeline | Kafka, Spark Structured Streaming, real-time scoring |

## Target Role Mapping

This portfolio is designed to demonstrate:

- development of AI, ML, GenAI, and Agentic AI solutions;
- use of AI-assisted coding practices in the software delivery process;
- data and AI platform adoption, including Databricks-style workflows;
- design of reusable AI services for multiple vertical projects;
- participation in the full lifecycle: architecture, prototyping, data pipelines, production deployment, optimization, and maintenance;
- DevOps and MLOps fundamentals with Docker, CI/CD, Kubernetes, and release checklists.

## Current Status

| Module | Status |
| --- | --- |
| `agenticops-toolkit` | In progress |
| `credit-risk-mlops` | Planned |
| `banking-rag-agent` | Planned |
| `customer-intelligence-streaming` | Planned |

## Suggested Local Workflow

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
python -m unittest discover -s tests
ruff check .
```

## Portfolio Timeline

The recommended timeline is 8 weeks, with week 9 as buffer for polish, deployment, and interview preparation. See [docs/roadmap.md](docs/roadmap.md).
