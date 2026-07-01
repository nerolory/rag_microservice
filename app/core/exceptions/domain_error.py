"""Base domain exception."""

from __future__ import annotations


class DomainError(Exception):
    """Base class for business and infrastructure errors."""

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
