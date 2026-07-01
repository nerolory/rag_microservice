"""FastAPI application factory."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.api.api_router_factory import ApiRouterFactory
from app.api.exception_handler_registry import ExceptionHandlerRegistry
from app.api.schemas import HealthResponse
from app.core import (
    JsonLogFormatter,
    LoggerProvider,
    LoggingConfigurator,
    Settings,
    TraceContext,
    TraceIdMiddleware,
)
from app.infrastructure import InfrastructureFactory
from app.services import AppContainerFactory


class ApplicationFactory:
    """Create and configure the FastAPI application."""

    def __init__(
        self,
        settings: Settings | None = None,
        trace_context: TraceContext | None = None,
        logger_provider: LoggerProvider | None = None,
    ) -> None:
        self._settings = settings or Settings()
        self._trace_context = trace_context or TraceContext()
        self._logger_provider = logger_provider or LoggerProvider()

    def create_app(self) -> FastAPI:
        """Build the configured FastAPI application and wire its dependencies."""
        LoggingConfigurator(JsonLogFormatter()).configure(self._settings.log_level)
        container_factory = AppContainerFactory(
            infrastructure_factory=InfrastructureFactory(),
            logger_provider=self._logger_provider,
            trace_context=self._trace_context,
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncIterator[None]:
            container = container_factory.build(self._settings)
            app.state.container = container
            startup_logger = self._logger_provider.get_logger("startup")

            if (
                self._settings.embedding_provider == "local"
                and self._settings.warmup_local_embeddings
                and self._settings.is_search_system_configured()
            ):
                startup_logger.info("Warming up local embedding model...")
                await container.warmup()
                startup_logger.info("Local embedding model is ready")

            yield

            await container.close()

        app = FastAPI(title="RAG Service", lifespan=lifespan)
        app.add_middleware(
            TraceIdMiddleware,
            trace_context=self._trace_context,
        )
        app.include_router(ApiRouterFactory().build())
        ExceptionHandlerRegistry(self._trace_context).register(app)

        @app.get("/health", response_model=HealthResponse)
        async def health(request: Request) -> HealthResponse:
            """Report service readiness and embedding warmup status."""
            container = request.app.state.container
            embeddings_ready = container.is_embeddings_ready()

            return HealthResponse(
                status="ok" if embeddings_ready else "starting",
                embeddings_ready=embeddings_ready,
            )

        return app
