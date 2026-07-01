"""Embedding input kinds for models that use task-specific prefixes."""

from enum import StrEnum


class EmbeddingInputKind(StrEnum):
    """Whether text is indexed as a document chunk or used as a search query."""

    DOCUMENT = "document"
    QUERY = "query"
