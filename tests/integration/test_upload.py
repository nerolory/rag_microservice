from tests.conftest import UPLOAD_URL


def test_upload_non_utf8_returns_400(client) -> None:
    response = client.post(
        UPLOAD_URL,
        files={"file": ("broken.txt", b"\xff\xfe", "text/plain")},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"]["code"] == "FILE_FORMAT_INVALID"
