"""Question answering orchestration."""

from __future__ import annotations

from app.core import OperationTracer
from app.domain import PromptBuilder, RetrievedContext
from app.infrastructure import (
    EmbeddingInputKind,
    EmbeddingProvider,
    LLMProvider,
    VectorStore,
)
from app.services.query_result import QueryResult
from app.services.search_system_guard import SearchSystemGuard


class QueryService:
    """Coordinate retrieval-augmented generation across indexed documents."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        llm_provider: LLMProvider,
        prompt_builder: PromptBuilder,
        top_k: int,
        search_system_guard: SearchSystemGuard,
        operation_tracer: OperationTracer,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store
        self._llm_provider = llm_provider
        self._prompt_builder = prompt_builder
        self._top_k = top_k
        self._search_system_guard = search_system_guard
        self._operation_tracer = operation_tracer

    async def ask(self, question: str) -> QueryResult:
        """Answer a question using the most relevant chunks in the vector store."""
        with self._operation_tracer.trace("query"):
            self._search_system_guard.ensure_available()

            with self._operation_tracer.trace("query_embedding"):
                query_vector = await self._embedding_provider.embed(
                    question,
                    kind=EmbeddingInputKind.QUERY,
                )

            with self._operation_tracer.trace("retrieval"):
                search_results = await self._vector_store.search(
                    query_vector,
                    self._top_k,
                )

            context = RetrievedContext.from_search_results(search_results)
            prompt = self._prompt_builder.build(question, context)

            with self._operation_tracer.trace("llm"):
                answer = await self._llm_provider.generate(prompt)

            return QueryResult(answer=answer, sources=search_results.items)
