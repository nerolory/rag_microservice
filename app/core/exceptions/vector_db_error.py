"""Vector database unavailable exception."""

from __future__ import annotations

from app.core.exceptions.domain_error import DomainError


class VectorDBError(DomainError):
    """Raised when the vector database cannot be reached."""

    def __init__(
        self,
        message: str = "Vector database is currently unavailable",
    ) -> None:
        super().__init__(message=message, code="VECTOR_DB_UNAVAILABLE")
