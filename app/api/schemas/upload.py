"""Upload endpoint response schema."""

from uuid import UUID

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Document ingestion metadata returned after indexing."""

    document_id: UUID
    filename: str
    indexed_chunks_count: int = Field(ge=0)
