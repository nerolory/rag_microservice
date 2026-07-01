"""Ask endpoint request schema."""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Question payload for retrieval-augmented generation."""

    question: str = Field(min_length=1)
