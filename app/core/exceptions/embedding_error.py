"""Embedding provider unavailable exception."""

from __future__ import annotations

from app.core.exceptions.domain_error import DomainError


class EmbeddingError(DomainError):
    """Raised when the embedding provider cannot be reached."""

    def __init__(
        self,
        message: str = "Embedding service is currently unavailable",
    ) -> None:
        super().__init__(message=message, code="EMBEDDING_UNAVAILABLE")
