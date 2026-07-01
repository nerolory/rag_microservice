"""Application dependency graph construction."""

from __future__ import annotations

from app.core import (
    LoggerProvider,
    OperationTracer,
    Settings,
    TraceContext,
)
from app.domain import PromptBuilder, TextSplitter
from app.infrastructure import FilePromptTemplateStore, InfrastructureFactory
from app.services.app_container import AppContainer
from app.services.document_service import DocumentService
from app.services.query_service import QueryService
from app.services.search_system_guard import SearchSystemGuard


class AppContainerFactory:
    """Construct the application dependency graph from runtime settings."""

    def __init__(
        self,
        infrastructure_factory: InfrastructureFactory,
        logger_provider: LoggerProvider,
        trace_context: TraceContext,
    ) -> None:
        self._infrastructure_factory = infrastructure_factory
        self._logger_provider = logger_provider
        self._trace_context = trace_context

    def build(self, settings: Settings) -> AppContainer:
        """Wire and return the application container."""
        search_system_guard = SearchSystemGuard(settings)
        embedding_provider = self._infrastructure_factory.build_embedding_provider(
            settings
        )
        llm_provider = self._infrastructure_factory.build_llm_provider(settings)
        vector_store = self._infrastructure_factory.build_vector_store(settings)
        prompt_template_store = FilePromptTemplateStore(
            template_path=settings.resolve_prompt_path(),
        )
        text_splitter = TextSplitter(
            chunk_size=settings.chunk_size,
            overlap_ratio=settings.chunk_overlap,
        )
        prompt_builder = PromptBuilder(template_source=prompt_template_store)
        document_tracer = OperationTracer(
            self._logger_provider.get_logger("document_service"),
            self._trace_context,
        )
        query_tracer = OperationTracer(
            self._logger_provider.get_logger("query_service"),
            self._trace_context,
        )
        document_service = DocumentService(
            text_splitter=text_splitter,
            embedding_provider=embedding_provider,
            vector_store=vector_store,
            allowed_extensions=settings.allowed_extensions,
            search_system_guard=search_system_guard,
            operation_tracer=document_tracer,
        )
        query_service = QueryService(
            embedding_provider=embedding_provider,
            vector_store=vector_store,
            llm_provider=llm_provider,
            prompt_builder=prompt_builder,
            top_k=settings.top_k,
            search_system_guard=search_system_guard,
            operation_tracer=query_tracer,
        )

        return AppContainer(
            settings=settings,
            document_service=document_service,
            query_service=query_service,
            embedding_provider=embedding_provider,
            llm_provider=llm_provider,
            vector_store=vector_store,
        )
