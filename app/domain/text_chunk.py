"""Text chunk value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.domain import ChunkMetadata


@dataclass(frozen=True, slots=True)
class TextChunk:
    """A single text fragment extracted from a source document."""

    chunk_id: UUID
    content: str
    source_filename: str
    index: int

    def to_metadata(self) -> ChunkMetadata:
        """Convert the chunk into vector-store metadata."""
        from app.domain import ChunkMetadata

        return ChunkMetadata(
            chunk_id=self.chunk_id,
            content=self.content,
            source_filename=self.source_filename,
            index=self.index,
        )
