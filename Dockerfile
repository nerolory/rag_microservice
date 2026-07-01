FROM python:3.11-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml .
RUN pip install --no-cache-dir .

FROM base AS test

RUN pip install --no-cache-dir ".[dev]"

COPY app/ app/
COPY tests/ tests/

CMD ["sh", "-c", "ruff check app tests && ruff format --check app tests && mypy app && pytest tests -v"]

FROM base AS test-e2e

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir ".[local,dev]"

COPY app/ app/
COPY tests/ tests/

CMD ["sh", "-c", "ruff check app tests && ruff format --check app tests && mypy app && pytest tests -v"]

FROM base AS production

RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir ".[local]"

COPY app/ app/

EXPOSE 8000

HEALTHCHECK --interval=60s --timeout=5s --start-period=360s --retries=5 \
    CMD curl -fsS http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
