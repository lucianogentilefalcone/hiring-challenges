"""Signal repository for CRUD operations."""

from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from models import Signal


class SignalRepository:
    """Repository for Signal CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, signal: Signal) -> Signal:
        self.db.add(signal)
        self.db.commit()
        self.db.refresh(signal)
        return signal

    def get_by_id(self, signal_id: UUID) -> Optional[Signal]:
        return self.db.query(Signal).filter(Signal.id == signal_id).first()

    def get_by_signal_id(self, signal_id: str) -> Optional[Signal]:
        return self.db.query(Signal).filter(Signal.signal_id == signal_id).first()

    def get_by_signal_gid(self, signal_gid: UUID) -> Optional[Signal]:
        return self.db.query(Signal).filter(Signal.signal_gid == signal_gid).first()

    def list_all(self) -> List[Signal]:
        return self.db.query(Signal).all()

    def list_by_asset_id(self, asset_id: UUID) -> List[Signal]:
        return self.db.query(Signal).filter(Signal.asset_id == asset_id).all()

    def update(self, signal: Signal) -> Signal:
        self.db.merge(signal)
        self.db.commit()
        self.db.refresh(signal)
        return signal

    def delete(self, signal_id: UUID) -> bool:
        signal = self.get_by_id(signal_id)
        if not signal:
            return False
        self.db.delete(signal)
        self.db.commit()
        return True
