"""Character-based text splitting for document ingestion."""

from __future__ import annotations

from uuid import UUID, uuid5

from app.domain.text_chunk import TextChunk
from app.domain.text_chunks import TextChunks


class TextSplitter:
    """Split documents into overlapping chunks of fixed size."""

    def __init__(self, chunk_size: int = 800, overlap_ratio: float = 0.15) -> None:
        if chunk_size < 1:
            raise ValueError("chunk_size must be positive")
        if not 0.0 <= overlap_ratio < 1.0:
            raise ValueError("overlap_ratio must be in [0.0, 1.0)")
        self._chunk_size = chunk_size
        self._overlap_ratio = overlap_ratio

    @property
    def chunk_size(self) -> int:
        """Return the configured maximum chunk size in characters."""
        return self._chunk_size

    def split(
        self,
        text: str,
        source_filename: str,
        document_id: UUID,
    ) -> TextChunks:
        """Split text into deterministic chunks scoped to a document."""
        if not text:
            return TextChunks(items=())

        step = max(1, int(self._chunk_size * (1.0 - self._overlap_ratio)))
        chunks: list[TextChunk] = []
        start = 0
        index = 0

        while start < len(text):
            end = min(start + self._chunk_size, len(text))
            chunks.append(
                TextChunk(
                    chunk_id=uuid5(document_id, str(index)),
                    content=text[start:end],
                    source_filename=source_filename,
                    index=index,
                )
            )
            if end >= len(text):
                break
            start += step
            index += 1

        return TextChunks(items=tuple(chunks))
