"""Map application query results to API responses."""

from __future__ import annotations

from app.api.schemas import AskResponse
from app.services.query_result import QueryResult


class AskResponseMapper:
    """Convert application query results into API response schemas."""

    def to_ask_response(self, result: QueryResult) -> AskResponse:
        """Build the public ask response from a completed query result."""
        return AskResponse(
            answer=result.answer,
            source_chunks_count=len(result.sources),
        )
