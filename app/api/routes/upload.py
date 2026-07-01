"""Document upload API route."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status

from app.api.dependencies import get_document_service
from app.api.schemas import UploadResponse
from app.core import FileFormatError
from app.services import DocumentService

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile,
    service: Annotated[DocumentService, Depends(get_document_service)],
) -> UploadResponse:
    """Accept a text document, chunk it, embed it, and store vectors."""
    raw = await file.read()

    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise FileFormatError("Document must be UTF-8 encoded text") from exc

    filename = file.filename or "unknown.txt"
    result = await service.ingest(filename=filename, content=content)

    return UploadResponse(
        document_id=result.document_id,
        filename=result.filename,
        indexed_chunks_count=result.chunks_stored,
    )
