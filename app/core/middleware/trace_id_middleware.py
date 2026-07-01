"""HTTP trace middleware."""

from __future__ import annotations

from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.core.trace import TraceContext


class TraceIdMiddleware(BaseHTTPMiddleware):
    """Attach a unique trace identifier to every HTTP request."""

    def __init__(self, app: ASGIApp, trace_context: TraceContext) -> None:
        super().__init__(app)
        self._trace_context = trace_context

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Assign a trace identifier and forward the request."""
        trace_id = uuid4()
        self._trace_context.set_trace_id(trace_id)
        response = await call_next(request)
        response.headers["X-Trace-Id"] = str(trace_id)
        return response
