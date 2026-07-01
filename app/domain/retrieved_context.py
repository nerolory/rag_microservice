"""Retrieved context value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain import SearchResults, TextChunk


@dataclass(frozen=True, slots=True)
class RetrievedContext:
    """Context assembled for prompt construction."""

    chunks: tuple[TextChunk, ...]

    @classmethod
    def from_search_results(cls, results: SearchResults) -> RetrievedContext:
        """Build a retrieved context from ranked search hits."""
        return cls(
            chunks=tuple(
                result.to_text_chunk(index)
                for index, result in enumerate(results.items)
            )
        )
