"""Root API router factory."""

from fastapi import APIRouter

from app.api.routes import ask, upload

API_V1_DOCUMENTS_PREFIX = "/api/v1/documents"


class ApiRouterFactory:
    """Build the versioned API router with application routes."""

    def build(self) -> APIRouter:
        """Create and wire the public API router under /api/v1/documents."""
        router = APIRouter(prefix=API_V1_DOCUMENTS_PREFIX)
        router.include_router(upload.router, tags=["documents"])
        router.include_router(ask.router, tags=["documents"])

        return router
