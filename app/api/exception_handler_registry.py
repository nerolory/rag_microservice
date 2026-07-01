"""Global API exception handler registry."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.schemas import ErrorDetail, ErrorResponse
from app.core import (
    DomainError,
    EmbeddingError,
    FileFormatError,
    LLMUnavailableError,
    SearchSystemUnavailableError,
    TraceContext,
    VectorDBError,
)


class ExceptionHandlerRegistry:
    """Register structured exception handlers on a FastAPI application."""

    def __init__(self, trace_context: TraceContext) -> None:
        self._trace_context = trace_context

    def register(self, app: FastAPI) -> None:
        """Attach exception handlers to the application."""

        @app.exception_handler(DomainError)
        async def domain_error_handler(
            request: Request,
            exc: DomainError,
        ) -> JSONResponse:
            status_code = self._status_code_for_domain_error(exc)
            return JSONResponse(
                status_code=status_code,
                content=self._error_payload(exc.code, exc.message).model_dump(
                    mode="json"
                ),
            )

        @app.exception_handler(RequestValidationError)
        async def validation_error_handler(
            request: Request,
            exc: RequestValidationError,
        ) -> JSONResponse:
            return JSONResponse(
                status_code=422,
                content=self._error_payload(
                    "VALIDATION_ERROR",
                    "Request validation failed",
                ).model_dump(mode="json"),
            )

        @app.exception_handler(Exception)
        async def unhandled_error_handler(
            request: Request,
            exc: Exception,
        ) -> JSONResponse:
            return JSONResponse(
                status_code=500,
                content=self._error_payload(
                    "INTERNAL_ERROR",
                    "An unexpected error occurred",
                ).model_dump(mode="json"),
            )

    def _status_code_for_domain_error(self, exc: DomainError) -> int:
        if isinstance(exc, FileFormatError):
            return 400
        if isinstance(
            exc,
            (
                SearchSystemUnavailableError,
                LLMUnavailableError,
                VectorDBError,
                EmbeddingError,
            ),
        ):
            return 503
        return 500

    def _error_payload(self, code: str, message: str) -> ErrorResponse:
        return ErrorResponse(
            error=ErrorDetail(
                code=code,
                message=message,
                trace_id=self._trace_context.get_trace_id(),
            )
        )
