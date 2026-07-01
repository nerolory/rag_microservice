"""ChromaDB-backed vector store implementation."""

from __future__ import annotations

import asyncio
from typing import Any, cast
from uuid import UUID

import chromadb
from chromadb.api.models.Collection import Collection

from app.core import VectorDBError
from app.domain import ChunkMetadata, EmbeddingVector, SearchResult, SearchResults


class ChromaVectorStore:
    """Persist and query embeddings through ChromaDB."""

    def __init__(self, persist_dir: str, collection_name: str) -> None:
        self._persist_dir = persist_dir
        self._collection_name = collection_name
        self._client: object | None = None
        self._collection: Collection | None = None

    def _ensure_collection(self) -> Collection:
        """Return the persistent Chroma collection, creating it when needed."""
        if self._collection is not None:
            return self._collection

        try:
            self._client = chromadb.PersistentClient(path=self._persist_dir)
            self._collection = self._client.get_or_create_collection(
                name=self._collection_name,
                metadata={"hnsw:space": "cosine"},
            )

            return self._collection
        except Exception as exc:
            raise VectorDBError(str(exc)) from exc

    async def add(
        self,
        document_id: UUID,
        vectors: tuple[EmbeddingVector, ...],
        metadatas: tuple[ChunkMetadata, ...],
    ) -> None:
        """Store chunk embeddings and metadata for a document."""
        if not vectors:
            return

        if len(vectors) != len(metadatas):
            raise VectorDBError("Vectors and metadata count mismatch")

        def _add() -> None:
            collection = self._ensure_collection()
            collection.add(
                ids=[str(metadata.chunk_id) for metadata in metadatas],
                embeddings=cast(
                    Any,
                    [list(vector.values) for vector in vectors],
                ),
                metadatas=[
                    {
                        "document_id": str(document_id),
                        "chunk_id": str(metadata.chunk_id),
                        "content": metadata.content,
                        "source_filename": metadata.source_filename,
                        "index": metadata.index,
                    }
                    for metadata in metadatas
                ],
            )

        try:
            await asyncio.to_thread(_add)
        except VectorDBError:
            raise
        except Exception as exc:
            raise VectorDBError(str(exc)) from exc

    async def search(
        self,
        vector: EmbeddingVector,
        top_k: int,
    ) -> SearchResults:
        """Return the most relevant chunks across the indexed collection."""

        def _search() -> SearchResults:
            collection = self._ensure_collection()
            chroma_response = collection.query(
                query_embeddings=cast(Any, [list(vector.values)]),
                n_results=top_k,
            )
            chunk_ids = chroma_response.get("ids")
            distances = chroma_response.get("distances")
            metadatas = chroma_response.get("metadatas")

            if not chunk_ids or not chunk_ids[0]:
                return SearchResults(items=())

            ranked_results: list[SearchResult] = []

            for _chunk_id, distance, metadata in zip(
                chunk_ids[0],
                distances[0] if distances else [],
                metadatas[0] if metadatas else [],
                strict=True,
            ):
                relevance = 1.0 - float(distance)
                ranked_results.append(
                    SearchResult(
                        chunk_id=UUID(str(metadata["chunk_id"])),
                        content=str(metadata["content"]),
                        score=relevance,
                        source_filename=str(metadata["source_filename"]),
                    )
                )

            ranked_results.sort(key=lambda item: item.score, reverse=True)

            return SearchResults(items=tuple(ranked_results))

        try:
            return await asyncio.to_thread(_search)
        except VectorDBError:
            raise
        except Exception as exc:
            raise VectorDBError(str(exc)) from exc

    async def close(self) -> None:
        """Release the underlying Chroma client."""
        self._client = None
        self._collection = None
