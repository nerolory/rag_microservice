"""Application settings."""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

EmbeddingProviderName = Literal["openai", "local"]
LLMProviderName = Literal["openrouter", "openai"]


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    embedding_provider: EmbeddingProviderName = "openai"
    llm_provider: LLMProviderName = "openrouter"

    openrouter_api_key: str = ""
    openrouter_model: str = "mistralai/mistral-7b-instruct"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_llm_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    local_embedding_model: str = "nomic-ai/nomic-embed-text-v1.5"
    local_embedding_device: str = "cpu"
    embedding_operation_timeout_seconds: float = 300.0
    warmup_local_embeddings: bool = True

    chroma_persist_dir: str = "./data/chroma"
    chroma_collection: str = "documents"

    chunk_size: int = 800
    chunk_overlap: float = 0.15
    top_k: int = 5
    log_level: str = "INFO"

    prompt_template_path: str = "app/domain/prompts/default.txt"
    allowed_extensions: tuple[str, ...] = (".txt", ".md")

    def is_embedding_configured(self) -> bool:
        """Return whether the embedding backend is ready to use."""
        if self.embedding_provider == "local":
            return True

        return bool(self.openai_api_key.strip())

    def is_llm_configured(self) -> bool:
        """Return whether the LLM backend is ready to use."""
        if self.llm_provider == "openrouter":
            return bool(self.openrouter_api_key.strip())

        return bool(self.openai_api_key.strip())

    def is_search_system_configured(self) -> bool:
        """Return whether the full search stack is configured."""
        return self.is_embedding_configured() and self.is_llm_configured()

    def resolve_prompt_path(self) -> Path:
        """Resolve the prompt template path on disk."""
        return Path(self.prompt_template_path)
