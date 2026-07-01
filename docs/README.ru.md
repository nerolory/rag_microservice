# RAG Microservice (RU)

Микросервис **Retrieval-Augmented Generation (RAG)** на **FastAPI**: загрузка документов, индексация в ChromaDB и ответы через семантический поиск и LLM.

**English documentation:** [../README.md](../README.md)  
**Архитектура:** [architecture.md](architecture.md)  
**ТЗ:** [SPECIFICATION.md](SPECIFICATION.md)

---

## Автор и лицензия

**Copyright (c) 2026 Alexander Borisov.**

Код можно использовать и интегрировать **с указанием автора**. **Продавать код нельзя.** Доступна **платная интеграция**.

**Контакт:** [a.borisov@qsoft.ru](mailto:a.borisov@qsoft.ru) · [LICENSE](../LICENSE)

---

## API (по ТЗ)

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/api/v1/documents/upload` | Загрузка `.txt` / `.md` (UTF-8) |
| `POST` | `/api/v1/documents/ask` | Вопрос по проиндексированным документам |
| `GET` | `/health` | Статус сервиса |

OpenAPI: http://localhost:8000/docs

### Загрузка

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.txt"
```

Ответ `201 Created`:

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "document.txt",
  "indexed_chunks_count": 5
}
```

### Вопрос

```bash
curl -X POST http://localhost:8000/api/v1/documents/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "О чём этот документ?"}'
```

Ответ `200 OK`:

```json
{
  "answer": "...",
  "source_chunks_count": 3
}
```

---

## Быстрый старт

```bash
cp .env.example .env
```

**Docker:**

```bash
docker compose up -d app
# Windows: .\scripts\run_docker.ps1
```

**Локально (Python 3.11+):**

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -e ".[local]"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Конфигурация

| Переменная | Описание |
|------------|----------|
| `EMBEDDING_PROVIDER` | `openai` или `local` |
| `LLM_PROVIDER` | `openrouter` или `openai` |
| `OPENAI_API_KEY` | Ключ OpenAI-compatible API |
| `OPENROUTER_API_KEY` | Ключ OpenRouter |
| `LOCAL_EMBEDDING_MODEL` | Модель Hugging Face |
| `CHROMA_PERSIST_DIR` | Путь к данным Chroma |
| `TOP_K` | Число чанков на вопрос |

Без API-ключей сервис стартует; upload и ask вернут **503**.

---

## Тестирование и CI

```bash
docker compose run --rm --build test
```

GitHub Actions: `.github/workflows/ci.yml`

E2E с локальными эмбеддингами:

```bash
docker compose --profile e2e run --rm -e RUN_E2E_TESTS=1 test-e2e
```

---

## Структура

```
app/
  api/              # Маршруты, схемы, dependencies
  services/         # DocumentService, QueryService
  domain/           # Бизнес-логика
  infrastructure/   # ChromaDB, провайдеры
  core/             # Настройки, логи, исключения
  bootstrap/        # Фабрика приложения
tests/
docs/
```

---

## Интеграция

Платное развёртывание и доработки: [a.borisov@qsoft.ru](mailto:a.borisov@qsoft.ru)
