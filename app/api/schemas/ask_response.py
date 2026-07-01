"""Ask endpoint response schema."""

from pydantic import BaseModel, Field


class AskResponse(BaseModel):
    """LLM answer with the number of supporting context chunks."""

    answer: str
    source_chunks_count: int = Field(ge=0)
