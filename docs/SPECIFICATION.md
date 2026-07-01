# Technical Assessment: Document RAG (Retrieval-Augmented Generation) Microservice

## Project Overview
The goal of this assessment is to design and implement a production-ready, highly structured RESTful API microservice using **FastAPI** that enables users to upload text documents, index them into a vector database, and perform semantic search and question-answering using a Large Language Model (LLM).

This project focuses on the core principles of **Retrieval-Augmented Generation (RAG)**, adhering strictly to **Western Style software engineering standards**: robust architecture, explicit typing, domain separation, rigorous error handling, and clean code culture.

---

## Technical Stack Requirements
- **Language:** Python 3.10+ (Strict Type Hinting required)
- **Framework:** FastAPI
- **Data Validation:** Pydantic v2
- **Vector Database:** Lightweight/In-Memory solution (e.g., ChromaDB, FAISS, or similar)
- **LLM Integration:** Any accessible inference engine (Local GGUF via `llama-cpp-python`, Hugging Face `sentence-transformers`, or external APIs via Groq / OpenRouter / OpenAI)

---

## Architecture & Design Patterns
The application must not be bundled into a single file. You are expected to demonstrate clean architectural separation using layers (e.g., Layered/Clean Architecture or Service-Repository patterns). 

Key design elements:
- **Thin API Layer:** Routers should handle HTTP concerns only (request routing, validation via Pydantic, and calling core services).
- **Service/Domain Layer:** Business logic (text splitting, prompt orchestration) must be encapsulated in pure OOP classes.
- **Infrastructure Layer:** Low-level integrations (LLM clients, vector storage read/write) must be decoupled from the core business logic.
- **Dependency Injection:** Utilize FastAPI's `Depends` for loose coupling and decoupled state management.
- **Lazy Loading:** Optimization patterns (such as lazy package exports in `__init__.py`) are highly encouraged.

---

## API Specifications & Endpoints

### 1. Document Upload & Indexing
- **Endpoint:** `POST /api/v1/documents/upload`
- **Content-Type:** `multipart/form-data`
- **Payload:** A file stream accepting `.txt` or `.md` files.
- **Behavior:** 
  1. Read the input document.
  2. Parse and split the text into meaningful paragraphs or chunks (e.g., handling specific token/character thresholds).
  3. Generate vector embeddings for each text chunk.
  4. Upsert/Save the text chunks along with their vector embeddings into the vector database.
- **Success Response:** `201 Created` with metadata (e.g., number of indexed chunks, file metadata).

### 2. Contextual Question Answering (RAG Query)
- **Endpoint:** `POST /api/v1/documents/ask`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "question": "What is the primary architectural goal of this project?"
  }
  ```
- **Behavior:**
  1. Validate the input query payload.
  2. Generate a vector embedding for the incoming question.
  3. Query the vector database using semantic similarity search to retrieve the most relevant text chunks (Context).
  4. Orchestrate an explicit prompt combining the retrieved Context and the original Question.
  5. Stream or return the generated response from the local or cloud-based LLM.
- **Success Response:** `200 OK`
  ```json
  {
    "answer": "The primary architectural goal is to implement production-ready separation of concerns...",
    "source_chunks_count": 3
  }
  ```

---

## Evaluation & Assessment Criteria (The "Western Way" Standards)

Your code will be evaluated based on industry-standard engineering practices rather than just "getting the application to run."

### 1. Explicit Typing & Validation
- Comprehensive **Type Hinting** across all modules, classes, and function signatures.
- Idiomatic use of Pydantic v2 models for enforcing strict boundaries on DTOs (Data Transfer Objects).

### 2. Production-Grade Error Handling
- **Zero Raw Exceptions:** Intercept infrastructure failures (e.g., Vector DB timeouts, LLM API rate limits, corrupted files) using clean exception handling registries.
- Custom middleware or global exception handlers to map domain-specific exceptions to correct, predictable HTTP responses (e.g., `422 Unprocessable Entity`, `503 Service Unavailable`), preventing `500 Internal Server Error` leakages.

### 3. Automated Testing Culture
- A dedicated `/tests` directory leveraging **PyTest**.
- Implement at least 2–3 meaningful automated tests:
  - Integration tests verifying payload validation edge-cases (e.g., submitting empty schemas, invalid file types).
  - Mocked or unit tests verifying business service logic isolation.

### 4. Code Formatting & Configuration
- Externalize all credentials, local model paths, and API keys into a unified configuration component reading exclusively from environment variables (leveraging a `.env` file or `pydantic-settings`).
- Adherence to standard Python naming conventions (`snake_case` for filenames and variables, `PascalCase` for classes).
- Clean, predictable import ordering (standard libs, third-party libraries, local codebase blocks).

---

## Deliverables
Provide a link to your public GitHub repository containing:
1. The structured codebase (`app/` module configuration).
2. Automated test suites (`tests/`).
3. A technical `README.md` in English detailing step-by-step instructions on setting up the local environment, installation dependencies, configuration setup, and sample `curl` requests.
