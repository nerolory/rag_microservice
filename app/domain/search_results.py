"""Search results collection value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain import SearchResult


@dataclass(frozen=True, slots=True)
class SearchResults:
    """Ranked search hits ordered by relevance."""

    items: tuple[SearchResult, ...]
