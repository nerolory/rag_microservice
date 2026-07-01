"""Structured error payload schema."""

from uuid import UUID

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Structured error payload."""

    code: str
    message: str
    trace_id: UUID
