"""Protocol for local text encoding models."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol


class TextEncoderProtocol(Protocol):
    """Minimal interface required from a local embedding model."""

    def encode(
        self,
        sentences: list[str],
        *,
        convert_to_numpy: bool,
        show_progress_bar: bool,
    ) -> Sequence[Sequence[float]]:
        """Encode input texts into vector representations."""
        ...
