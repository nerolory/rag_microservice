"""Prompt value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Prompt:
    """Final prompt sent to the LLM."""

    text: str
