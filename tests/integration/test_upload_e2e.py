import os

import pytest

from tests.conftest import UPLOAD_URL

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_E2E_TESTS") != "1",
    reason="Requires real API keys. Set RUN_E2E_TESTS=1 and provide .env credentials.",
)


def test_upload_txt_returns_document_id(client) -> None:
    content = b"Python is a programming language.\nFastAPI is a web framework."
    response = client.post(
        UPLOAD_URL,
        files={"file": ("notes.txt", content, "text/plain")},
    )

    assert response.status_code == 201
    payload = response.json()
    assert "document_id" in payload
    assert payload["filename"] == "notes.txt"
    assert payload["indexed_chunks_count"] > 0
