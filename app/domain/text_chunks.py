"""Text chunks collection value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain import TextChunk


@dataclass(frozen=True, slots=True)
class TextChunks:
    """Collection of text chunks produced by splitting."""

    items: tuple[TextChunk, ...]
