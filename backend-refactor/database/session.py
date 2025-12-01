"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import get_settings

settings = get_settings()

Base = declarative_base()

engine = create_engine(
    settings.database_url,
    echo=settings.debug_mode,
    pool_pre_ping=True,
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency to get database session."""
    db = session()
    try:
        yield db
    finally:
        db.close()
