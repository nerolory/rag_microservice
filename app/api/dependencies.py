"""FastAPI dependency callables."""

from __future__ import annotations

from typing import Annotated, cast

from fastapi import Depends, Request

from app.services import AppContainer, DocumentService, QueryService


def get_container(request: Request) -> AppContainer:
    """Return the application container stored on FastAPI app state."""
    return cast(AppContainer, request.app.state.container)


def get_document_service(
    container: Annotated[AppContainer, Depends(get_container)],
) -> DocumentService:
    """Provide the document ingestion service."""
    return container.document_service


def get_query_service(
    container: Annotated[AppContainer, Depends(get_container)],
) -> QueryService:
    """Provide the question answering service."""
    return container.query_service
