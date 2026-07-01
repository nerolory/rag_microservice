"""Application service exports."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.app_container import AppContainer
    from app.services.app_container_factory import AppContainerFactory
    from app.services.document_ingest_result import DocumentIngestResult
    from app.services.document_service import DocumentService
    from app.services.query_result import QueryResult
    from app.services.query_service import QueryService
    from app.services.search_system_guard import SearchSystemGuard

__all__ = (
    "AppContainer",
    "AppContainerFactory",
    "DocumentIngestResult",
    "DocumentService",
    "QueryResult",
    "QueryService",
    "SearchSystemGuard",
)

_EXPORTS: dict[str, tuple[str, str]] = {
    "AppContainer": ("app.services.app_container", "AppContainer"),
    "AppContainerFactory": (
        "app.services.app_container_factory",
        "AppContainerFactory",
    ),
    "DocumentIngestResult": (
        "app.services.document_ingest_result",
        "DocumentIngestResult",
    ),
    "DocumentService": ("app.services.document_service", "DocumentService"),
    "QueryResult": ("app.services.query_result", "QueryResult"),
    "QueryService": ("app.services.query_service", "QueryService"),
    "SearchSystemGuard": ("app.services.search_system_guard", "SearchSystemGuard"),
}


def __getattr__(name: str) -> object:
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_path, attribute = _EXPORTS[name]
    module = __import__(module_path, fromlist=[attribute])

    return getattr(module, attribute)
