# RAG Microservice

Production-oriented **Retrieval-Augmented Generation (RAG)** microservice on **FastAPI**: upload text documents, index them in ChromaDB, and ask questions using semantic search plus an LLM.

**Russian documentation:** [docs/README.ru.md](docs/README.ru.md)  
**Architecture:** [docs/architecture.md](docs/architecture.md)  
**Specification:** [docs/SPECIFICATION.md](docs/SPECIFICATION.md)

---

## Author & Licensing

**Copyright (c) 2026 Alexander Borisov.**

You may use, modify, and integrate this code with **attribution to the author**. You may **not sell** the source code as a standalone product or reusable library. **Paid integration** is available from the author.

**Contact:** [a.borisov@qsoft.ru](mailto:a.borisov@qsoft.ru) · See [LICENSE](LICENSE)

---

## API (per specification)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/documents/upload` | Upload `.txt` / `.md` (UTF-8), index chunks |
| `POST` | `/api/v1/documents/ask` | Ask a question against indexed content |
| `GET` | `/health` | Liveness and embedding warmup status |

OpenAPI: http://localhost:8000/docs

### Upload

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.txt"
```

Response `201 Created`:

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "document.txt",
  "indexed_chunks_count": 5
}
```

### Ask

```bash
curl -X POST http://localhost:8000/api/v1/documents/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

Response `200 OK`:

```json
{
  "answer": "...",
  "source_chunks_count": 3
}
```

---

## Quick Start

```bash
cp .env.example .env
# Edit API keys and provider settings
```

**Docker:**

```bash
docker compose up -d app
# Windows: .\scripts\run_docker.ps1
```

**Local (Python 3.11+):**

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -e ".[local]"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Configuration

| Variable | Description |
|----------|-------------|
| `EMBEDDING_PROVIDER` | `openai` or `local` |
| `LLM_PROVIDER` | `openrouter` or `openai` |
| `OPENAI_API_KEY` | OpenAI-compatible API key |
| `OPENROUTER_API_KEY` | OpenRouter key |
| `LOCAL_EMBEDDING_MODEL` | Hugging Face model for local embeddings |
| `CHROMA_PERSIST_DIR` | Chroma persistence path |
| `TOP_K` | Retrieved chunks per question |

The service starts without API keys; upload and ask return **503** until providers are configured.

---

## Testing & CI

**Light CI (Docker, no PyTorch):**

```bash
docker compose run --rm --build test
# or: make docker-test
```

Runs `ruff`, `mypy`, and `pytest`.

**E2E (local embeddings, requires `.env` keys):**

```bash
docker compose --profile e2e run --rm -e RUN_E2E_TESTS=1 test-e2e
```

**GitHub Actions:** `.github/workflows/ci.yml` runs the `test` target on push and pull requests.

---

## Project Structure

```
app/
  api/              # Routes, Pydantic schemas, dependencies
  services/         # DocumentService, QueryService
  domain/           # TextSplitter, PromptBuilder, value objects
  infrastructure/   # ChromaDB, embedding/LLM providers
  core/             # Settings, logging, exceptions
  bootstrap/        # Application factory
tests/
docs/
  SPECIFICATION.md
  architecture.md
  README.ru.md
```

---

## Integration Services

Paid deployment, customization, and support: [a.borisov@qsoft.ru](mailto:a.borisov@qsoft.ru)
