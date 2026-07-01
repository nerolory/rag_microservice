"""API package exports."""

from app.api.ask_response_mapper import AskResponseMapper
from app.api.dependencies import get_container, get_document_service, get_query_service
from app.api.exception_handler_registry import ExceptionHandlerRegistry

__all__ = (
    "ApiRouterFactory",
    "AskResponseMapper",
    "ExceptionHandlerRegistry",
    "get_container",
    "get_document_service",
    "get_query_service",
)


def __getattr__(name: str) -> object:
    if name == "ApiRouterFactory":
        from app.api.api_router_factory import ApiRouterFactory

        return ApiRouterFactory

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
