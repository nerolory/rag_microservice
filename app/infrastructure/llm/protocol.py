"""LLM provider protocol."""

from __future__ import annotations

from typing import Protocol

from app.domain import Prompt


class LLMProvider(Protocol):
    """Contract for large language model providers."""

    async def generate(self, prompt: Prompt) -> str:
        """Generate a completion for the supplied prompt."""
        ...

    async def close(self) -> None:
        """Release external resources."""
        ...
