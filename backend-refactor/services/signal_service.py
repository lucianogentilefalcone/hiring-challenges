"""Signal service layer with business logic."""

from typing import List, Tuple
from uuid import UUID

from models import Signal
from schemas import SignalCreate, SignalUpdate
from repositories import SignalRepository
from api.exceptions import SignalNotFoundException, SignalAlreadyExistsException


class SignalService:
    """Service for managing signals."""

    def __init__(self, repository: SignalRepository):
        self.repo = repository

    def get_all_signals(
        self, skip: int = 0, limit: int = 100
    ) -> Tuple[List[Signal], int]:
        return self.repo.list_paginated(skip, limit)

    def get_signal_by_id(self, signal_id: UUID) -> Signal:
        signal = self.repo.get_by_id(signal_id)
        if not signal:
            raise SignalNotFoundException(signal_id)
        return signal

    def get_signals_by_asset(
        self, asset_id: UUID, skip: int = 0, limit: int = 100
    ) -> Tuple[List[Signal], int]:
        signals = self.repo.list_by_asset_id(asset_id)
        total = len(signals)
        paginated = signals[skip : skip + limit]
        return paginated, total

    def create_signal(self, signal_in: SignalCreate) -> Signal:
        existing = self.repo.get_by_signal_id(signal_in.signal_id)
        if existing:
            raise SignalAlreadyExistsException(signal_in.signal_id)

        signal = Signal(**signal_in.model_dump())
        return self.repo.create(signal)

    def update_signal(self, signal_id: UUID, signal_in: SignalUpdate) -> Signal:
        signal = self.repo.get_by_id(signal_id)
        if not signal:
            raise SignalNotFoundException(signal_id)

        if signal_in.signal_id and signal_in.signal_id != signal.signal_id:
            existing = self.repo.get_by_signal_id(signal_in.signal_id)
            if existing:
                raise SignalAlreadyExistsException(signal_in.signal_id)

        update_data = signal_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(signal, key, value)

        return self.repo.update(signal)

    def delete_signal(self, signal_id: UUID) -> None:
        signal = self.repo.get_by_id(signal_id)
        if not signal:
            raise SignalNotFoundException(signal_id)
        self.repo.delete(signal_id)
