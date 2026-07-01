"""OpenAI embedding provider."""

from __future__ import annotations

import httpx

from app.core import EmbeddingError
from app.domain import EmbeddingVector
from app.infrastructure.embeddings.embedding_input_kind import EmbeddingInputKind


class OpenAIEmbeddingProvider:
    """Generate embeddings through the OpenAI-compatible API."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._model = model
        self._client = client or httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0,
        )
        self._owns_client = client is None

    async def embed(
        self,
        text: str,
        *,
        kind: EmbeddingInputKind = EmbeddingInputKind.DOCUMENT,
    ) -> EmbeddingVector:
        """Embed a single text value."""
        _ = kind
        batch = await self.embed_batch((text,))
        return batch[0]

    async def embed_batch(
        self,
        texts: tuple[str, ...],
        *,
        kind: EmbeddingInputKind = EmbeddingInputKind.DOCUMENT,
    ) -> tuple[EmbeddingVector, ...]:
        """Embed multiple text values in one request."""
        _ = kind
        if not texts:
            return ()
        try:
            response = await self._client.post(
                "/embeddings",
                json={"model": self._model, "input": list(texts)},
            )
            response.raise_for_status()
            payload = response.json()
            data = sorted(payload["data"], key=lambda item: item["index"])
            return tuple(
                EmbeddingVector(values=tuple(item["embedding"])) for item in data
            )
        except (httpx.HTTPError, KeyError, TypeError) as exc:
            raise EmbeddingError(str(exc)) from exc

    async def warmup(self) -> None:
        """Cloud embeddings need no local preload."""
        return None

    async def close(self) -> None:
        """Close the underlying HTTP client when owned by this provider."""
        if self._owns_client:
            await self._client.aclose()
