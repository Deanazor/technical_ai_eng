from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    agent_model_name: str = "ollama/gemma3:12b"
    agent_base_url: str | None = None
    agent_api_key: str | None = None

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings():
    settings = Settings()
    if not settings.agent_base_url and settings.agent_model_name.startswith("ollama/"):
        settings.agent_base_url = "http://localhost:11434"
    return settings
