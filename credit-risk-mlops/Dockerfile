FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY credit-risk-mlops ./credit-risk-mlops
COPY agenticops_toolkit ./agenticops_toolkit

RUN python -m pip install --upgrade pip \
    && python -m pip install -e ".[dev]"

ENV PYTHONPATH=/app/credit-risk-mlops/src

EXPOSE 8000

CMD ["uvicorn", "credit_risk_mlops.api:app", "--host", "0.0.0.0", "--port", "8000"]