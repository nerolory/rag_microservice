from uuid import UUID, uuid4

import pytest

from app.domain import TextChunks, TextSplitter


@pytest.fixture
def document_id() -> UUID:
    return uuid4()


@pytest.fixture
def splitter() -> TextSplitter:
    return TextSplitter(chunk_size=100, overlap_ratio=0.2)


def test_empty_text_returns_empty_chunks(
    splitter: TextSplitter, document_id: UUID
) -> None:
    result = splitter.split("", "doc.txt", document_id)

    assert isinstance(result, TextChunks)
    assert result.items == ()


def test_short_text_produces_single_chunk(
    splitter: TextSplitter, document_id: UUID
) -> None:
    text = "Short document content."

    result = splitter.split(text, "doc.txt", document_id)

    assert len(result.items) == 1
    chunk = result.items[0]
    assert chunk.content == text
    assert chunk.source_filename == "doc.txt"
    assert chunk.index == 0


def test_long_text_produces_multiple_chunks(
    splitter: TextSplitter, document_id: UUID
) -> None:
    text = "a" * 250

    result = splitter.split(text, "long.txt", document_id)

    assert len(result.items) > 1
    assert all(chunk.source_filename == "long.txt" for chunk in result.items)
    assert tuple(chunk.index for chunk in result.items) == tuple(
        range(len(result.items))
    )


def test_chunk_size_respected(splitter: TextSplitter, document_id: UUID) -> None:
    text = "x" * 500

    result = splitter.split(text, "size.txt", document_id)

    for chunk in result.items:
        assert len(chunk.content) <= splitter.chunk_size


def test_consecutive_chunks_overlap(splitter: TextSplitter, document_id: UUID) -> None:
    text = "abcdefghijklmnopqrstuvwxyz" * 20

    result = splitter.split(text, "overlap.txt", document_id)

    assert len(result.items) >= 2
    first = result.items[0].content
    second = result.items[1].content
    overlap_region = first[-20:]
    assert overlap_region in second


def test_chunk_ids_are_deterministic_per_document(document_id: UUID) -> None:
    splitter = TextSplitter(chunk_size=50, overlap_ratio=0.1)
    text = "word " * 100

    first_run = splitter.split(text, "doc.txt", document_id)
    second_run = splitter.split(text, "doc.txt", document_id)

    first_ids = tuple(chunk.chunk_id for chunk in first_run.items)
    second_ids = tuple(chunk.chunk_id for chunk in second_run.items)
    assert first_ids == second_ids


def test_invalid_chunk_size_raises() -> None:
    with pytest.raises(ValueError, match="chunk_size"):
        TextSplitter(chunk_size=0)


def test_invalid_overlap_ratio_raises() -> None:
    with pytest.raises(ValueError, match="overlap_ratio"):
        TextSplitter(overlap_ratio=1.0)
