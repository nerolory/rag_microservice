"""File-backed prompt template storage."""

from __future__ import annotations

from pathlib import Path


class FilePromptTemplateStore:
    """Load the default prompt template from the filesystem."""

    def __init__(self, template_path: Path) -> None:
        self._template_path = template_path

    def get_template(self) -> str:
        """Return the prompt template stored on disk."""
        return self._template_path.read_text(encoding="utf-8")
