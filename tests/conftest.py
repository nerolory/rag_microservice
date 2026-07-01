from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.bootstrap import ApplicationFactory
from app.core import Settings

UPLOAD_URL = "/api/v1/documents/upload"
ASK_URL = "/api/v1/documents/ask"


@pytest.fixture
def client_without_credentials() -> Iterator[TestClient]:
    settings = Settings(
        openai_api_key="",
        openrouter_api_key="",
    )
    app = ApplicationFactory(settings=settings).create_app()

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def client() -> Iterator[TestClient]:
    if os.getenv("RUN_E2E_TESTS") == "1":
        settings = Settings()
    else:
        settings = Settings(
            openai_api_key="",
            openrouter_api_key="",
        )

    app = ApplicationFactory(settings=settings).create_app()

    with TestClient(app) as test_client:
        yield test_client
