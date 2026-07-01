"""Application logger provider."""

from __future__ import annotations

import logging


class LoggerProvider:
    """Provide named loggers for application components."""

    def get_logger(self, name: str) -> logging.Logger:
        """Return a logger for the given component name."""
        return logging.getLogger(name)
