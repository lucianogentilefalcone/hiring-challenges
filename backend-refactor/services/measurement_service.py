"""Measurement service layer with business logic."""

from typing import List, Tuple
from uuid import UUID
from datetime import datetime

from models import Measurement
from schemas import MeasurementCreate, MeasurementUpdate
from repositories import MeasurementRepository
from api.exceptions import MeasurementNotFoundException


# TODO: Agregar todas las funciones que habia antes


class MeasurementService:
    """Service for managing measurements."""

    def __init__(self, repository: MeasurementRepository):
        self.repo = repository

    def get_all_measurements(
        self, skip: int = 0, limit: int = 100
    ) -> Tuple[List[Measurement], int]:
        return self.repo.list_paginated(skip, limit)

    def get_measurement_by_id(self, measurement_id: UUID) -> Measurement:
        measurement = self.repo.get_by_id(measurement_id)
        if not measurement:
            raise MeasurementNotFoundException(measurement_id)
        return measurement

    def get_measurements_by_signal(
        self, signal_id: UUID, skip: int = 0, limit: int = 100
    ) -> Tuple[List[Measurement], int]:
        measurements = self.repo.list_by_signal_id(signal_id)
        total = len(measurements)
        paginated = measurements[skip : skip + limit]
        return paginated, total

    def get_measurements_by_date_range(
        self,
        signal_id: UUID,
        from_date: datetime,
        to_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Measurement], int]:
        measurements = self.repo.list_by_signal_id_and_date_range(
            signal_id, from_date, to_date
        )
        total = len(measurements)
        paginated = measurements[skip : skip + limit]
        return paginated, total

    def create_measurement(self, measurement_in: MeasurementCreate) -> Measurement:
        measurement = Measurement(**measurement_in.model_dump())
        return self.repo.create(measurement)

    def update_measurement(
        self, measurement_id: UUID, measurement_in: MeasurementUpdate
    ) -> Measurement:
        measurement = self.repo.get_by_id(measurement_id)
        if not measurement:
            raise MeasurementNotFoundException(measurement_id)

        update_data = measurement_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(measurement, key, value)

        return self.repo.update(measurement)

    def delete_measurement(self, measurement_id: UUID) -> None:
        measurement = self.repo.get_by_id(measurement_id)
        if not measurement:
            raise MeasurementNotFoundException(measurement_id)
        self.repo.delete(measurement_id)
