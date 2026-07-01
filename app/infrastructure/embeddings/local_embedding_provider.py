"""Local embedding provider backed by sentence-transformers."""

from __future__ import annotations

import asyncio
import logging
import threading
from collections.abc import Callable
from typing import TypeVar

from app.core import EmbeddingError
from app.domain import EmbeddingVector
from app.infrastructure.embeddings.embedding_input_kind import EmbeddingInputKind
from app.infrastructure.embeddings.text_encoder_protocol import TextEncoderProtocol

logger = logging.getLogger(__name__)

T = TypeVar("T")

_NOMIC_DOCUMENT_PREFIX = "search_document: "
_NOMIC_QUERY_PREFIX = "search_query: "


class LocalEmbeddingProvider:
    """Generate embeddings with a locally loaded Hugging Face model."""

    def __init__(
        self,
        model_name: str,
        device: str,
        operation_timeout_seconds: float = 300.0,
    ) -> None:
        self._model_name = model_name
        self._device = device
        self._operation_timeout_seconds = operation_timeout_seconds
        self._model: TextEncoderProtocol | None = None
        self._load_lock = threading.Lock()
        self._ready = False

    @property
    def is_ready(self) -> bool:
        """Return whether the model is loaded and ready to encode."""
        return self._ready

    async def warmup(self) -> None:
        """Load the model before the first API request."""
        await self._run_in_thread(self._load_model, "model_warmup")

    async def embed(
        self,
        text: str,
        *,
        kind: EmbeddingInputKind = EmbeddingInputKind.DOCUMENT,
    ) -> EmbeddingVector:
        """Embed a single text value."""
        batch = await self.embed_batch((text,), kind=kind)
        return batch[0]

    async def embed_batch(
        self,
        texts: tuple[str, ...],
        *,
        kind: EmbeddingInputKind = EmbeddingInputKind.DOCUMENT,
    ) -> tuple[EmbeddingVector, ...]:
        """Embed multiple text values with a local model."""
        if not texts:
            return ()
        return await self._run_in_thread(
            lambda: self._encode_texts(texts, kind=kind),
            "embedding",
        )

    async def close(self) -> None:
        """Release the loaded model from memory."""
        with self._load_lock:
            self._model = None
            self._ready = False

    async def _run_in_thread(self, fn: Callable[[], T], operation: str) -> T:
        try:
            return await asyncio.wait_for(
                asyncio.to_thread(fn),
                timeout=self._operation_timeout_seconds,
            )
        except TimeoutError as exc:
            raise EmbeddingError(
                f"{operation} timed out after {self._operation_timeout_seconds}s"
            ) from exc
        except EmbeddingError:
            raise
        except Exception as exc:
            raise EmbeddingError(str(exc)) from exc

    def _encode_texts(
        self,
        texts: tuple[str, ...],
        *,
        kind: EmbeddingInputKind,
    ) -> tuple[EmbeddingVector, ...]:
        model = self._load_model()
        prefixed = self._prefix_texts(texts, kind=kind)
        raw_vectors = model.encode(
            prefixed,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return tuple(
            EmbeddingVector(values=tuple(float(value) for value in vector))
            for vector in raw_vectors
        )

    def _prefix_texts(
        self,
        texts: tuple[str, ...],
        *,
        kind: EmbeddingInputKind,
    ) -> list[str]:
        if "nomic" not in self._model_name.lower():
            return list(texts)
        prefix = (
            _NOMIC_QUERY_PREFIX
            if kind is EmbeddingInputKind.QUERY
            else _NOMIC_DOCUMENT_PREFIX
        )
        return [f"{prefix}{text}" for text in texts]

    def _load_model(self) -> TextEncoderProtocol:
        with self._load_lock:
            if self._model is not None:
                return self._model
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise EmbeddingError(
                    "Local embeddings require the optional dependency: "
                    "pip install '.[local]'"
                ) from exc
            logger.info(
                "Loading local embedding model %s (first run may download weights)",
                self._model_name,
            )
            self._model = SentenceTransformer(
                self._model_name,
                device=self._device,
                trust_remote_code=True,
            )
            self._ready = True
            logger.info("Local embedding model %s is ready", self._model_name)
            return self._model
