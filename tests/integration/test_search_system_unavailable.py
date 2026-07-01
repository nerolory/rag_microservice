from app.core import SEARCH_SYSTEM_UNAVAILABLE_MESSAGE
from tests.conftest import ASK_URL, UPLOAD_URL


def test_upload_without_credentials_returns_search_system_unavailable(
    client_without_credentials,
) -> None:
    response = client_without_credentials.post(
        UPLOAD_URL,
        files={"file": ("notes.txt", b"Some document content.", "text/plain")},
    )

    assert response.status_code == 503
    payload = response.json()
    assert payload["error"]["code"] == "SEARCH_SYSTEM_UNAVAILABLE"
    assert payload["error"]["message"] == SEARCH_SYSTEM_UNAVAILABLE_MESSAGE


def test_ask_without_credentials_returns_search_system_unavailable(
    client_without_credentials,
) -> None:
    response = client_without_credentials.post(
        ASK_URL,
        json={"question": "What is this about?"},
    )

    assert response.status_code == 503
    payload = response.json()
    assert payload["error"]["code"] == "SEARCH_SYSTEM_UNAVAILABLE"
    assert payload["error"]["message"] == SEARCH_SYSTEM_UNAVAILABLE_MESSAGE


def test_health_works_without_credentials(client_without_credentials) -> None:
    response = client_without_credentials.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "embeddings_ready": True}
