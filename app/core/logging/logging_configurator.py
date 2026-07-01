"""Logging system configurator."""

from __future__ import annotations

import logging
import sys

from app.core.logging.json_log_formatter import JsonLogFormatter


class LoggingConfigurator:
    """Configure structured application logging."""

    def __init__(self, formatter: JsonLogFormatter) -> None:
        self._formatter = formatter

    def configure(self, level: str) -> logging.Logger:
        """Apply structured logging to the root logger and return it."""
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self._formatter)
        root = logging.getLogger()
        root.handlers.clear()
        root.addHandler(handler)
        root.setLevel(level.upper())

        return root
