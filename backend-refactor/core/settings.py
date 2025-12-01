"""Application settings and environment variables."""

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings loaded from environment."""

    app_name: str = "SignalsBackend"
    api_version: str = "v1"
    debug_mode: bool = False
    database_url: str = "sqlite:///./signals.db"
    data_path: str = "data/signal.json"
    measurements_path: str = "data/measurements.csv"

    class Config:
        env_file = ".env"
        extra = "ignore"
