"""Measurement repository for CRUD operations."""

from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from datetime import datetime
from models import Measurement


class MeasurementRepository:
    """Repository for Measurement CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, measurement: Measurement) -> Measurement:
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)
        return measurement

    def get_by_id(self, measurement_id: UUID) -> Optional[Measurement]:
        return (
            self.db.query(Measurement).filter(Measurement.id == measurement_id).first()
        )

    def list_paginated(self, skip: int, limit: int):
        query = self.db.query(Measurement)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def list_by_signal_id(self, signal_id: UUID) -> List[Measurement]:
        return (
            self.db.query(Measurement).filter(Measurement.signal_id == signal_id).all()
        )

    def list_by_signal_id_and_date_range(
        self, signal_id: UUID, from_date: datetime, to_date: datetime
    ) -> List[Measurement]:
        return (
            self.db.query(Measurement)
            .filter(Measurement.signal_id == signal_id)
            .filter(Measurement.timestamp >= from_date)
            .filter(Measurement.timestamp <= to_date)
            .order_by(Measurement.timestamp.desc())
            .all()
        )

    def update(self, measurement: Measurement) -> Measurement:
        self.db.merge(measurement)
        self.db.commit()
        self.db.refresh(measurement)
        return measurement

    def delete(self, measurement_id: UUID) -> bool:
        measurement = self.get_by_id(measurement_id)
        if not measurement:
            return False
        self.db.delete(measurement)
        self.db.commit()
        return True
