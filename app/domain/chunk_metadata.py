"""Chunk metadata value object."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ChunkMetadata:
    """Metadata stored alongside a vector embedding."""

    chunk_id: UUID
    content: str
    source_filename: str
    index: int
