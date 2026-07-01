"""Prompt template source protocol."""

from __future__ import annotations

from typing import Protocol


class PromptTemplateSource(Protocol):
    """Read the active LLM prompt template."""

    def get_template(self) -> str:
        """Return the active prompt template text."""
        ...
