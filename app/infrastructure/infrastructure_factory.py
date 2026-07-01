"""Infrastructure provider factory."""

from __future__ import annotations

from app.core import Settings
from app.infrastructure.embeddings import EmbeddingProvider, OpenAIEmbeddingProvider
from app.infrastructure.embeddings.local_embedding_provider import (
    LocalEmbeddingProvider,
)
from app.infrastructure.llm import LLMProvider, OpenAILLMProvider, OpenRouterLLMProvider
from app.infrastructure.vectorstore import ChromaVectorStore, VectorStore


class InfrastructureFactory:
    """Create configured infrastructure providers."""

    def build_embedding_provider(self, settings: Settings) -> EmbeddingProvider:
        """Create the configured embedding provider."""
        if settings.embedding_provider == "local":
            return LocalEmbeddingProvider(
                model_name=settings.local_embedding_model,
                device=settings.local_embedding_device,
                operation_timeout_seconds=settings.embedding_operation_timeout_seconds,
            )
        return OpenAIEmbeddingProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_embedding_model,
            base_url=settings.openai_base_url,
        )

    def build_llm_provider(self, settings: Settings) -> LLMProvider:
        """Create the configured LLM provider."""
        if settings.llm_provider == "openai":
            return OpenAILLMProvider(
                api_key=settings.openai_api_key,
                model=settings.openai_llm_model,
                base_url=settings.openai_base_url,
            )
        return OpenRouterLLMProvider(
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            base_url=settings.openrouter_base_url,
        )

    def build_vector_store(self, settings: Settings) -> VectorStore:
        """Create the configured vector store."""
        return ChromaVectorStore(
            persist_dir=settings.chroma_persist_dir,
            collection_name=settings.chroma_collection,
        )
