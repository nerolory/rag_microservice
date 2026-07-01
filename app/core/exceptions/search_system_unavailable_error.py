"""Search system unavailable exception."""

from __future__ import annotations

from app.core.exceptions.domain_error import DomainError


class SearchSystemUnavailableError(DomainError):
    """Raised when embedding or LLM providers are not configured."""

    MESSAGE = (
        "The search system is not configured. "
        "Try again later or contact the administrator."
    )

    def __init__(self) -> None:
        super().__init__(
            message=self.MESSAGE,
            code="SEARCH_SYSTEM_UNAVAILABLE",
        )


SEARCH_SYSTEM_UNAVAILABLE_MESSAGE = SearchSystemUnavailableError.MESSAGE
