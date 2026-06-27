import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    llm_model: str = "google/gemini-2.5-flash"
    qdrant_path: str = "./qdrant_data"
    supabase_url: str = ""
    supabase_key: str = ""
    cors_origins: str = "http://localhost:5173"
    max_tokens: int = 300

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
