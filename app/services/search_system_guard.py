"""Guard that verifies search infrastructure availability."""

from app.core import SearchSystemUnavailableError, Settings


class SearchSystemGuard:
    """Ensure the external search stack is configured before use."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def ensure_available(self) -> None:
        """Raise when the search system is not configured."""
        if not self._settings.is_search_system_configured():
            raise SearchSystemUnavailableError()
