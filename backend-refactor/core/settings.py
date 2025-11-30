"""Application settings and environment variables."""

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings loaded from environment."""

    # App
    app_name: str = "SignalsBackend"
    api_version: str = "v1"
    debug_mode: bool = False

    # Database
    database_url: str = "sqlite:///./signals.db"

    class Config:
        env_file = ".env"
