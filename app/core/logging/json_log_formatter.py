"""JSON log formatter."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime


class JsonLogFormatter(logging.Formatter):
    """Serialize log records as JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string."""
        payload = self._build_base_payload(record)
        self._append_trace_fields(record, payload)

        return json.dumps(payload, ensure_ascii=False)

    def _build_base_payload(self, record: logging.LogRecord) -> dict[str, object]:
        """Build the standard JSON fields for a log record."""
        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

    def _append_trace_fields(
        self,
        record: logging.LogRecord,
        payload: dict[str, object],
    ) -> None:
        """Attach optional tracing fields when they are present on the record."""
        if hasattr(record, "trace_id"):
            payload["trace_id"] = record.trace_id

        if hasattr(record, "duration_ms"):
            payload["duration_ms"] = record.duration_ms

        if hasattr(record, "event"):
            payload["event"] = record.event
