"""Core configuration module."""

from functools import lru_cache
from core.settings import AppSettings


@lru_cache()
def get_settings() -> AppSettings:
    """Get cached application settings."""
    return AppSettings()
