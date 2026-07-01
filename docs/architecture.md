# Architecture

This document describes the current structure of the RAG microservice and how the main request flows are wired.

## Goals

The service implements a production-oriented **Retrieval-Augmented Generation (RAG)** pipeline:

1. Upload and index text documents.
2. Answer natural-language questions using the most relevant indexed chunks and an LLM.

The codebase follows **layered architecture** with explicit typing, Pydantic DTOs at the HTTP boundary, and infrastructure adapters kept separate from business logic.

## Layer Overview

```
HTTP Client
    |
    v
+-----------+
| api       |  Routes, Pydantic schemas, exception handlers, Depends()
+-----------+
    |
    v
+-----------+
| services  |  Use-case orchestration (upload, ask)
+-----------+
    |
    +------------------+
    v                  v
+-----------+   +------------------+
| domain    |   | infrastructure   |
| pure logic|   | Chroma, LLM, etc.|
+-----------+   +------------------+
    |
    v
+-----------+
| core      |  Settings, logging, tracing, domain exceptions
+-----------+
```

### `app/api`

Thin HTTP layer. Responsibilities:

- Route definitions under `/api/v1/documents`
- Request and response validation through Pydantic v2 models
- Dependency injection via FastAPI `Depends`
- Mapping between service results and API DTOs

Does **not** contain business rules or direct calls to ChromaDB / LLM SDKs.

### `app/services`

Application services coordinate use cases:

| Service | Responsibility |
|---------|----------------|
| `DocumentService` | Validate file, split text, embed chunks, persist vectors |
| `QueryService` | Embed question, retrieve top-K chunks, build prompt, call LLM |
| `SearchSystemGuard` | Block upload/ask when providers are not configured |

### `app/domain`

Framework-agnostic business logic and value objects:

- `TextSplitter` — character-based chunking with overlap
- `PromptBuilder` — render `{context}` and `{question}` from `default.txt`
- `TextChunk`, `SearchResults`, `EmbeddingVector`, and related models

No FastAPI, HTTP, or database imports.

### `app/infrastructure`

External system adapters:

| Component | Implementation |
|-----------|----------------|
| Vector store | `ChromaVectorStore` (persistent, cosine similarity) |
| Embeddings | `OpenAIEmbeddingProvider`, `LocalEmbeddingProvider` |
| LLM | `OpenAILLMProvider`, `OpenRouterLLMProvider` |
| Prompt file | `FilePromptTemplateStore` |

Protocols (`EmbeddingProvider`, `LLMProvider`, `VectorStore`) define adapter contracts.

### `app/core`

Cross-cutting concerns:

- `Settings` via `pydantic-settings`
- Structured JSON logging and `trace_id` middleware
- Domain exception hierarchy mapped to HTTP status codes

### `app/bootstrap`

Composition root:

- `ApplicationFactory` builds the FastAPI app
- `lifespan` creates `AppContainer`, runs embedding warmup, and closes resources

## Request Flows

### Upload (`POST /api/v1/documents/upload`)

```
Upload route
  -> DocumentService.ingest()
       -> validate extension and UTF-8
       -> TextSplitter.split()
       -> EmbeddingProvider.embed_batch()
       -> VectorStore.add()
  -> UploadResponse (201 Created)
```

### Ask (`POST /api/v1/documents/ask`)

```
Ask route
  -> QueryService.ask()
       -> SearchSystemGuard.ensure_available()
       -> EmbeddingProvider.embed(question, QUERY)
       -> VectorStore.search(top_k) across all indexed chunks
       -> PromptBuilder.build()
       -> LLMProvider.generate()
  -> AskResponse (answer + source_chunks_count)
```

## Dependency Injection

FastAPI dependencies live in `app/api/dependencies.py`:

- `get_container()` reads `AppContainer` from `app.state`
- `get_document_service()` and `get_query_service()` expose application services

`AppContainerFactory` wires the full graph at startup.

## Configuration

All runtime settings come from environment variables through `Settings`:

- Provider selection: `EMBEDDING_PROVIDER`, `LLM_PROVIDER`
- Chroma path and collection name
- Chunk size, overlap, and `TOP_K`
- API keys and model names

The service starts without credentials; `/upload` and `/ask` return **503** until providers are configured.

## Error Handling

`ExceptionHandlerRegistry` maps domain exceptions to predictable HTTP responses:

| Exception | HTTP |
|-----------|------|
| `FileFormatError` | 400 |
| `SearchSystemUnavailableError`, `EmbeddingError`, `LLMUnavailableError`, `VectorDBError` | 503 |
| Validation errors | 422 |
| Unexpected errors | 500 |

Responses use a structured envelope: `{ "error": { "code", "message", "trace_id" } }`.

## Local Embeddings Note

When `LOCAL_EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5`, the local provider applies Nomic task prefixes:

- `search_document:` for indexed chunks
- `search_query:` for questions

Re-index documents after changing the embedding model or prefix logic.

## Testing Layout

```
tests/
  unit/          TextSplitter, PromptBuilder, Settings, embedding prefixes
  integration/   HTTP endpoints, validation, provider availability
```

CI runs the `test` Docker target: `ruff`, `mypy`, and `pytest`.

Optional e2e profile (`test-e2e`) loads local embeddings and requires `RUN_E2E_TESTS=1` plus configured API keys.

## Project Layout

```
app/
  api/              HTTP routes, schemas, dependencies
  bootstrap/        Application factory
  core/             Settings, logging, exceptions
  domain/           Business logic and value objects
  infrastructure/   External adapters
  services/         Use-case orchestration
  main.py           Uvicorn entrypoint
tests/
docs/
  SPECIFICATION.md  Assignment requirements
  architecture.md   This file
  README.ru.md      Russian documentation
```
