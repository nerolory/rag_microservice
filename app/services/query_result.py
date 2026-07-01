"""Result of a successful question answering flow."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain import SearchResult


@dataclass(frozen=True, slots=True)
class QueryResult:
    """Result of a successful question answering flow."""

    answer: str
    sources: tuple[SearchResult, ...]
