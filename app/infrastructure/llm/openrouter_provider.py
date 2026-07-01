"""OpenRouter LLM provider."""

from __future__ import annotations

import httpx

from app.core import LLMUnavailableError
from app.domain import Prompt


class OpenRouterLLMProvider:
    """Generate answers through the OpenRouter chat completions API."""

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
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/rag-service",
            },
            timeout=120.0,
        )
        self._owns_client = client is None

    async def generate(self, prompt: Prompt) -> str:
        """Generate a completion for the supplied prompt."""
        try:
            response = await self._client.post(
                "/chat/completions",
                json={
                    "model": self._model,
                    "messages": [{"role": "user", "content": prompt.text}],
                },
            )
            response.raise_for_status()
            payload = response.json()
            return str(payload["choices"][0]["message"]["content"])
        except (httpx.HTTPError, KeyError, TypeError, IndexError) as exc:
            raise LLMUnavailableError(str(exc)) from exc

    async def close(self) -> None:
        """Close the underlying HTTP client when owned by this provider."""
        if self._owns_client:
            await self._client.aclose()
