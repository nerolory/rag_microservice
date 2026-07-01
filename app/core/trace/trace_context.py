"""Request trace context."""

from __future__ import annotations

import contextvars
from uuid import UUID, uuid4


class TraceContext:
    """Manage request-scoped trace identifiers."""

    def __init__(self) -> None:
        self._trace_id_var: contextvars.ContextVar[UUID | None] = (
            contextvars.ContextVar("trace_id", default=None)
        )

    def get_trace_id(self) -> UUID:
        """Return the current trace identifier, creating one when missing."""
        trace_id = self._trace_id_var.get()
        if trace_id is None:
            trace_id = uuid4()
            self._trace_id_var.set(trace_id)
        return trace_id

    def set_trace_id(self, trace_id: UUID) -> None:
        """Bind a trace identifier to the current execution context."""
        self._trace_id_var.set(trace_id)
