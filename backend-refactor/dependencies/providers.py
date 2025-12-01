"""Dependency injection providers."""

from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

from repositories import AssetRepository
from repositories import SignalRepository
from repositories import MeasurementRepository

from services import AssetService
from services import SignalService
from services import MeasurementService


def get_asset_repository(db: Session = Depends(get_db)) -> AssetRepository:
    return AssetRepository(db)


def get_asset_service(
    repository: AssetRepository = Depends(get_asset_repository),
) -> AssetService:
    return AssetService(repository)


def get_signal_repository(db: Session = Depends(get_db)) -> SignalRepository:
    return SignalRepository(db)


def get_signal_service(
    repository: SignalRepository = Depends(get_signal_repository),
) -> SignalService:
    return SignalService(repository)


def get_measurement_repository(db: Session = Depends(get_db)) -> MeasurementRepository:
    return MeasurementRepository(db)


def get_measurement_service(
    repository: MeasurementRepository = Depends(get_measurement_repository),
) -> MeasurementService:
    return MeasurementService(repository)
