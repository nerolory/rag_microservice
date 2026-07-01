"""Core package exports."""

from app.core.config import Settings
from app.core.exceptions import (
    SEARCH_SYSTEM_UNAVAILABLE_MESSAGE,
    DomainError,
    EmbeddingError,
    FileFormatError,
    LLMUnavailableError,
    SearchSystemUnavailableError,
    VectorDBError,
)
from app.core.logging import (
    JsonLogFormatter,
    LoggerProvider,
    LoggingConfigurator,
    OperationTracer,
)
from app.core.middleware import TraceIdMiddleware
from app.core.trace import TraceContext

__all__ = (
    "DomainError",
    "EmbeddingError",
    "FileFormatError",
    "JsonLogFormatter",
    "LLMUnavailableError",
    "LoggerProvider",
    "LoggingConfigurator",
    "OperationTracer",
    "SEARCH_SYSTEM_UNAVAILABLE_MESSAGE",
    "SearchSystemUnavailableError",
    "Settings",
    "TraceContext",
    "TraceIdMiddleware",
    "VectorDBError",
)
