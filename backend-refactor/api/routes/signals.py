"""Signals router."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query

from models import Signal
from schemas import (
    SignalCreate,
    SignalUpdate,
    SignalResponse,
    SignalListResponse,
)
from services import SignalService, AssetService
from dependencies import get_signal_service, get_asset_service


router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("", response_model=SignalListResponse)
def list_signals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: SignalService = Depends(get_signal_service),
):
    items, total = service.get_all_signals(skip=skip, limit=limit)
    return SignalListResponse(items=items, total=total)


@router.post("", response_model=SignalResponse, status_code=201)
def create_signal(
    signal_in: SignalCreate,
    service: SignalService = Depends(get_signal_service),
) -> Signal:
    return service.create_signal(signal_in)


@router.get("/{signal_id}", response_model=SignalResponse)
def get_signal(
    signal_id: UUID,
    service: SignalService = Depends(get_signal_service),
) -> Signal:
    return service.get_signal_by_id(signal_id)


@router.put("/{signal_id}", response_model=SignalResponse)
def update_signal(
    signal_id: UUID,
    signal_in: SignalUpdate,
    service: SignalService = Depends(get_signal_service),
) -> Signal:
    return service.update_signal(signal_id, signal_in)


@router.delete("/{signal_id}", status_code=204)
def delete_signal(
    signal_id: UUID,
    service: SignalService = Depends(get_signal_service),
):
    service.delete_signal(signal_id)


@router.get("/asset/{asset_id}", response_model=SignalListResponse)
def get_signals_by_asset(
    asset_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: SignalService = Depends(get_signal_service),
    asset_service: AssetService = Depends(get_asset_service),
):
    asset_service.get_asset_by_id(asset_id)  # Validate asset existence
    items, total = service.get_signals_by_asset(asset_id, skip=skip, limit=limit)
    return SignalListResponse(items=items, total=total)
