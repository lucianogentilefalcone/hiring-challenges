"""Pytest configuration with module-scoped DB fixtures."""

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app
from dependencies import (
    get_asset_service,
    get_signal_service,
    get_measurement_service,
    get_asset_repository,
    get_signal_repository,
    get_measurement_repository,
)
from repositories import (
    AssetRepository,
    SignalRepository,
    MeasurementRepository,
)
from services import (
    AssetService,
    SignalService,
    MeasurementService,
)
from models import Asset, Signal


TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


# Enable foreign key support for SQLite
@event.listens_for(test_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="module")
def db():
    """Create fresh in-memory DB per test module."""
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def session(db):
    """Create fresh session per test with rollback."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def override_get_db(session: Session):
    """Override get_db to use test database."""
    try:
        yield session
    finally:
        pass


@pytest.fixture
def client(db, session: Session):
    """FastAPI test client with overridden dependencies."""

    def get_db_override():
        return session

    app.dependency_overrides[get_db] = get_db_override

    app.dependency_overrides[get_asset_repository] = lambda: AssetRepository(session)
    app.dependency_overrides[get_signal_repository] = lambda: SignalRepository(session)
    app.dependency_overrides[get_measurement_repository] = (
        lambda: MeasurementRepository(session)
    )

    app.dependency_overrides[get_asset_service] = lambda: AssetService(
        AssetRepository(session)
    )
    app.dependency_overrides[get_signal_service] = lambda: SignalService(
        SignalRepository(session)
    )
    app.dependency_overrides[get_measurement_service] = lambda: MeasurementService(
        MeasurementRepository(session)
    )

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def base_asset(session: Session) -> Asset:
    """Create a base asset for signal/measurement tests."""
    asset = Asset(
        asset_id="BASE-ASSET-001",
        latitude=40.7128,
        longitude=-74.0060,
        description="Base test asset",
    )
    session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset


@pytest.fixture
def base_signal(session: Session, base_asset: Asset) -> Signal:
    """Create a base signal for measurement tests."""
    signal = Signal(
        signal_id="BASE-SIGNAL-001",
        signal_name="Base Test Signal",
        unit="kV",
        asset_id=base_asset.id,
    )
    session.add(signal)
    session.commit()
    session.refresh(signal)
    return signal
