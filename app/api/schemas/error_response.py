"""Top-level error response envelope."""

from pydantic import BaseModel

from app.api.schemas.error_detail import ErrorDetail


class ErrorResponse(BaseModel):
    """Top-level error response envelope."""

    error: ErrorDetail
