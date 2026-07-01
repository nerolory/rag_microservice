"""Document ingestion orchestration."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from app.core import FileFormatError, OperationTracer
from app.domain import TextSplitter
from app.infrastructure import EmbeddingProvider, VectorStore
from app.services.document_ingest_result import DocumentIngestResult
from app.services.search_system_guard import SearchSystemGuard


class DocumentService:
    """Coordinate validation, chunking, embedding, and storage."""

    def __init__(
        self,
        text_splitter: TextSplitter,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        allowed_extensions: tuple[str, ...],
        search_system_guard: SearchSystemGuard,
        operation_tracer: OperationTracer,
    ) -> None:
        self._text_splitter = text_splitter
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store
        self._allowed_extensions = allowed_extensions
        self._search_system_guard = search_system_guard
        self._operation_tracer = operation_tracer

    async def ingest(self, filename: str, content: str) -> DocumentIngestResult:
        """Validate, chunk, embed, and store a document."""
        with self._operation_tracer.trace("upload"):
            self._validate_extension(filename)
            if not content.strip():
                raise FileFormatError("Document is empty")

            self._search_system_guard.ensure_available()

            document_id = uuid4()
            chunks = self._text_splitter.split(content, filename, document_id)

            texts = tuple(chunk.content for chunk in chunks.items)
            with self._operation_tracer.trace("embedding"):
                vectors = await self._embedding_provider.embed_batch(texts)

            metadatas = tuple(chunk.to_metadata() for chunk in chunks.items)
            await self._vector_store.add(document_id, vectors, metadatas)

            return DocumentIngestResult(
                document_id=document_id,
                filename=filename,
                chunks_stored=len(chunks.items),
            )

    def _validate_extension(self, filename: str) -> None:
        extension = Path(filename).suffix.lower()
        if extension not in self._allowed_extensions:
            allowed = ", ".join(self._allowed_extensions)
            raise FileFormatError(
                f"Unsupported file format '{extension}'. Allowed: {allowed}"
            )
