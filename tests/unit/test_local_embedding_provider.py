"""Tests for local embedding prefixes."""

from app.infrastructure.embeddings.embedding_input_kind import EmbeddingInputKind
from app.infrastructure.embeddings.local_embedding_provider import (
    LocalEmbeddingProvider,
)


def test_nomic_document_prefix() -> None:
    provider = LocalEmbeddingProvider(
        model_name="nomic-ai/nomic-embed-text-v1.5",
        device="cpu",
    )
    result = provider._prefix_texts(("chunk text",), kind=EmbeddingInputKind.DOCUMENT)
    assert result == ["search_document: chunk text"]


def test_nomic_query_prefix() -> None:
    provider = LocalEmbeddingProvider(
        model_name="nomic-ai/nomic-embed-text-v1.5",
        device="cpu",
    )
    result = provider._prefix_texts(
        ("What is the primary goal of this project?",),
        kind=EmbeddingInputKind.QUERY,
    )
    assert result == ["search_query: What is the primary goal of this project?"]


def test_non_nomic_model_has_no_prefix() -> None:
    provider = LocalEmbeddingProvider(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        device="cpu",
    )
    result = provider._prefix_texts(("plain",), kind=EmbeddingInputKind.QUERY)
    assert result == ["plain"]
