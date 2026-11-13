"""Application settings, read from environment variables and the repo-root .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/config.py -> repo root is two levels above the app package.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    app_env: str = "development"
    # SQLite fallback lets the app start without PostgreSQL during early development.
    database_url: str = "sqlite:///./adguard.db"
    frontend_origin: str = "http://localhost:5173"
    upload_dir: str = "./uploads"
    gemini_api_key: str = ""
    groq_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
