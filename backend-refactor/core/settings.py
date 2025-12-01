"""Application settings and environment variables."""

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings loaded from environment."""

    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int = 5432
    app_name: str = "SignalsBackend"
    api_version: str = "v1"
    debug_mode: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def database_url(self) -> str:
        """Construct the database URL from settings."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )
