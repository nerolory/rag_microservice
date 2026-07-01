"""Question answering API route."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api import AskResponseMapper
from app.api.dependencies import get_query_service
from app.api.schemas import AskRequest, AskResponse
from app.services import QueryService

router = APIRouter()
ask_response_mapper = AskResponseMapper()


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    body: AskRequest,
    service: Annotated[QueryService, Depends(get_query_service)],
) -> AskResponse:
    """Answer a question using the most relevant indexed document chunks."""
    result = await service.ask(body.question)

    return ask_response_mapper.to_ask_response(result)
