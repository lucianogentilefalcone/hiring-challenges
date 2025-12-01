"""Application factory and configuration."""

from fastapi import FastAPI
from core.config import get_settings
from api.routes import assets_router, signals_router, measurements_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.api_version)

    # Register routers
    app.include_router(assets_router, prefix="/api")
    app.include_router(signals_router, prefix="/api")
    app.include_router(measurements_router, prefix="/api")

    return app
