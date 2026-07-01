"""Vector store protocol."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from app.domain import ChunkMetadata, EmbeddingVector, SearchResults


class VectorStore(Protocol):
    """Contract for vector persistence and similarity search."""

    async def add(
        self,
        document_id: UUID,
        vectors: tuple[EmbeddingVector, ...],
        metadatas: tuple[ChunkMetadata, ...],
    ) -> None:
        """Persist embeddings for a document."""
        ...

    async def search(
        self,
        vector: EmbeddingVector,
        top_k: int,
    ) -> SearchResults:
        """Return the most relevant chunks across all indexed documents."""
        ...

    async def close(self) -> None:
        """Release external resources."""
        ...
