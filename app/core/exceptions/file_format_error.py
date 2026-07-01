"""Invalid file format exception."""

from __future__ import annotations

from app.core.exceptions.domain_error import DomainError


class FileFormatError(DomainError):
    """Raised when an uploaded document is invalid."""

    def __init__(self, message: str = "Unsupported file format") -> None:
        super().__init__(message=message, code="FILE_FORMAT_INVALID")
