"""Search result value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.domain import TextChunk


@dataclass(frozen=True, slots=True)
class SearchResult:
    """A chunk returned by vector similarity search."""

    chunk_id: UUID
    content: str
    score: float
    source_filename: str

    def to_text_chunk(self, index: int) -> TextChunk:
        """Convert a search hit back into a domain text chunk."""
        from app.domain import TextChunk

        return TextChunk(
            chunk_id=self.chunk_id,
            content=self.content,
            source_filename=self.source_filename,
            index=index,
        )
