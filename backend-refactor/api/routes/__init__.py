"""Routers package."""

from api.routes.assets import router as assets_router
from api.routes.signals import router as signals_router
from api.routes.measurements import router as measurements_router

__all__ = [
    "assets_router",
    "signals_router",
    "measurements_router",
]
