from tests.conftest import ASK_URL


def test_ask_empty_question_returns_422(client) -> None:
    response = client.post(ASK_URL, json={"question": ""})

    assert response.status_code == 422


def test_ask_missing_question_returns_422(client) -> None:
    response = client.post(ASK_URL, json={})

    assert response.status_code == 422
