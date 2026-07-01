"""Embedding vector value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmbeddingVector:
    """Dense vector representation of text."""

    values: tuple[float, ...]
