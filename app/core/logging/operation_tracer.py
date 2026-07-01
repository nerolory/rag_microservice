"""Structured operation tracing."""

from __future__ import annotations

import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager
from uuid import UUID

from app.core.trace import TraceContext


class OperationTracer:
    """Trace service operations with structured logs."""

    def __init__(self, logger: logging.Logger, trace_context: TraceContext) -> None:
        self._logger = logger
        self._trace_context = trace_context

    @contextmanager
    def trace(self, event: str) -> Iterator[None]:
        """Log the start and completion of an operation with elapsed time."""
        trace_id = self._trace_context.get_trace_id()
        started = time.perf_counter()
        self._log(logging.INFO, f"{event} started", trace_id, f"{event}_start")
        try:
            yield
        finally:
            self._log(
                logging.INFO,
                f"{event} completed",
                trace_id,
                f"{event}_complete",
                duration_ms=(time.perf_counter() - started) * 1000,
            )

    def _log(
        self,
        level: int,
        message: str,
        trace_id: UUID,
        event: str,
        duration_ms: float | None = None,
    ) -> None:
        extra: dict[str, object] = {"event": event, "trace_id": str(trace_id)}
        if duration_ms is not None:
            extra["duration_ms"] = round(duration_ms, 2)
        self._logger.log(level, message, extra=extra)
