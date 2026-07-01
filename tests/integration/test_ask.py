import os

import pytest

from tests.conftest import ASK_URL, UPLOAD_URL


@pytest.mark.skipif(
    os.getenv("RUN_E2E_TESTS") != "1",
    reason="Requires real API keys. Set RUN_E2E_TESTS=1 and provide .env credentials.",
)
def test_ask_after_upload_returns_non_empty_answer(client) -> None:
    content = (
        b"Python is a high-level programming language. "
        b"It is widely used for web development and data science."
    )
    upload_response = client.post(
        UPLOAD_URL,
        files={"file": ("python.txt", content, "text/plain")},
    )

    assert upload_response.status_code == 201

    ask_response = client.post(
        ASK_URL,
        json={"question": "What is Python used for?"},
    )

    assert ask_response.status_code == 200
    payload = ask_response.json()
    assert isinstance(payload["answer"], str)
    assert len(payload["answer"]) > 0
    assert payload["source_chunks_count"] > 0
