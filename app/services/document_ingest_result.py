"""Result of a successful document ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DocumentIngestResult:
    """Identifiers and counts produced after indexing a document."""

    document_id: UUID
    filename: str
    chunks_stored: int
