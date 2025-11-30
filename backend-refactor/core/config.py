"""Core configuration module."""

from functools import lru_cache
from core import AppSettings


@lru_cache()
def get_settings() -> AppSettings:
    """Get cached application settings."""
    return AppSettings()
