"""Application dependency graph holder."""

from __future__ import annotations

from app.core import Settings
from app.infrastructure import EmbeddingProvider, LLMProvider, VectorStore
from app.services.document_service import DocumentService
from app.services.query_service import QueryService


class AppContainer:
    """Hold the wired application graph for request handling and lifecycle."""

    def __init__(
        self,
        settings: Settings,
        document_service: DocumentService,
        query_service: QueryService,
        embedding_provider: EmbeddingProvider,
        llm_provider: LLMProvider,
        vector_store: VectorStore,
    ) -> None:
        self.settings = settings
        self.document_service = document_service
        self.query_service = query_service
        self._embedding_provider = embedding_provider
        self._llm_provider = llm_provider
        self._vector_store = vector_store

    async def warmup(self) -> None:
        """Pre-load slow resources before serving traffic."""
        if not self.settings.is_search_system_configured():
            return

        if (
            self.settings.embedding_provider == "local"
            and self.settings.warmup_local_embeddings
        ):
            await self._embedding_provider.warmup()

    def is_embeddings_ready(self) -> bool:
        """Return whether embeddings can be served without blocking setup."""
        if self.settings.embedding_provider != "local":
            return True

        if not self.settings.is_search_system_configured():
            return True

        provider = self._embedding_provider

        if hasattr(provider, "is_ready"):
            return bool(provider.is_ready)

        return True

    async def close(self) -> None:
        """Release external resources held by infrastructure providers."""
        await self._embedding_provider.close()
        await self._llm_provider.close()
        await self._vector_store.close()
