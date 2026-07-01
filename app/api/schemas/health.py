"""API schemas for health checks."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health probe response."""

    status: str
    embeddings_ready: bool = True
