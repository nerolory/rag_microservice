"""Core exception exports."""

from app.core.exceptions.domain_error import DomainError
from app.core.exceptions.embedding_error import EmbeddingError
from app.core.exceptions.file_format_error import FileFormatError
from app.core.exceptions.llm_unavailable_error import LLMUnavailableError
from app.core.exceptions.search_system_unavailable_error import (
    SEARCH_SYSTEM_UNAVAILABLE_MESSAGE,
    SearchSystemUnavailableError,
)
from app.core.exceptions.vector_db_error import VectorDBError

__all__ = (
    "DomainError",
    "EmbeddingError",
    "FileFormatError",
    "LLMUnavailableError",
    "SEARCH_SYSTEM_UNAVAILABLE_MESSAGE",
    "SearchSystemUnavailableError",
    "VectorDBError",
)
