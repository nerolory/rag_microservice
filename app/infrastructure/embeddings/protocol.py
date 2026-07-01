"""Embedding provider protocol."""

from __future__ import annotations

from typing import Protocol

from app.domain import EmbeddingVector
from app.infrastructure.embeddings.embedding_input_kind import EmbeddingInputKind


class EmbeddingProvider(Protocol):
    """Contract for text embedding providers."""

    async def embed(
        self,
        text: str,
        *,
        kind: EmbeddingInputKind = EmbeddingInputKind.DOCUMENT,
    ) -> EmbeddingVector:
        """Embed a single text value."""
        ...

    async def embed_batch(
        self,
        texts: tuple[str, ...],
        *,
        kind: EmbeddingInputKind = EmbeddingInputKind.DOCUMENT,
    ) -> tuple[EmbeddingVector, ...]:
        """Embed multiple text values."""
        ...

    async def warmup(self) -> None:
        """Prepare the provider before handling traffic."""
        ...

    async def close(self) -> None:
        """Release external resources."""
        ...
