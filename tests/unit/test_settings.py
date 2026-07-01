from app.core import Settings


def test_local_embeddings_do_not_require_openai_key() -> None:
    settings = Settings(
        embedding_provider="local",
        openai_api_key="",
        llm_provider="openrouter",
        openrouter_api_key="test-key",
    )

    assert settings.is_embedding_configured() is True
    assert settings.is_llm_configured() is True
    assert settings.is_search_system_configured() is True


def test_openai_embeddings_require_api_key() -> None:
    settings = Settings(
        embedding_provider="openai",
        openai_api_key="",
        llm_provider="openrouter",
        openrouter_api_key="test-key",
    )

    assert settings.is_embedding_configured() is False
    assert settings.is_search_system_configured() is False
