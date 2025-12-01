"""Measurements router."""

from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, Query

from models import Measurement
from schemas import (
    MeasurementCreate,
    MeasurementUpdate,
    MeasurementResponse,
    MeasurementListResponse,
)
from services import MeasurementService
from dependencies import get_measurement_service


router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.get("", response_model=MeasurementListResponse)
def list_measurements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: MeasurementService = Depends(get_measurement_service),
):
    items, total = service.get_all_measurements(skip=skip, limit=limit)
    return MeasurementListResponse(items=items, total=total)


@router.post("", response_model=MeasurementResponse, status_code=201)
def create_measurement(
    measurement_in: MeasurementCreate,
    service: MeasurementService = Depends(get_measurement_service),
) -> Measurement:
    return service.create_measurement(measurement_in)


@router.get("/{measurement_id}", response_model=MeasurementResponse)
def get_measurement(
    measurement_id: UUID,
    service: MeasurementService = Depends(get_measurement_service),
) -> Measurement:
    return service.get_measurement_by_id(measurement_id)


@router.put("/{measurement_id}", response_model=MeasurementResponse)
def update_measurement(
    measurement_id: UUID,
    measurement_in: MeasurementUpdate,
    service: MeasurementService = Depends(get_measurement_service),
) -> Measurement:
    return service.update_measurement(measurement_id, measurement_in)


@router.delete("/{measurement_id}", status_code=204)
def delete_measurement(
    measurement_id: UUID,
    service: MeasurementService = Depends(get_measurement_service),
):
    service.delete_measurement(measurement_id)


@router.get("/signal/{signal_id}", response_model=MeasurementListResponse)
def get_measurements_by_signal(
    signal_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: MeasurementService = Depends(get_measurement_service),
):
    items, total = service.get_measurements_by_signal(signal_id, skip=skip, limit=limit)
    return MeasurementListResponse(items=items, total=total)


@router.get("/signal/{signal_id}/range", response_model=MeasurementListResponse)
def get_measurements_by_date_range(
    signal_id: UUID,
    from_date: datetime = Query(...),
    to_date: datetime = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: MeasurementService = Depends(get_measurement_service),
):
    items, total = service.get_measurements_by_date_range(
        signal_id, from_date, to_date, skip=skip, limit=limit
    )
    return MeasurementListResponse(items=items, total=total)
