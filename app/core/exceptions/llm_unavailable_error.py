"""LLM unavailable exception."""

from __future__ import annotations

from app.core.exceptions.domain_error import DomainError


class LLMUnavailableError(DomainError):
    """Raised when the LLM provider cannot be reached."""

    def __init__(
        self,
        message: str = "LLM service is currently unavailable",
    ) -> None:
        super().__init__(message=message, code="LLM_UNAVAILABLE")
