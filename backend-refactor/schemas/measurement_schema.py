"""Measurement Pydantic schemas for API validation."""

from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MeasurementBase(BaseModel):
    value: float = Field(..., description="Measurement value")
    timestamp: datetime = Field(..., description="Measurement timestamp")


class MeasurementCreate(MeasurementBase):
    signal_id: UUID = Field(..., description="Signal UUID foreign key")


class MeasurementUpdate(BaseModel):
    value: Optional[float] = None
    timestamp: Optional[datetime] = None


class MeasurementResponse(MeasurementBase):
    id: UUID = Field(..., description="Measurement UUID primary key")
    signal_id: UUID = Field(..., description="Signal UUID foreign key")

    class Config:
        from_attributes = True


class MeasurementListResponse(BaseModel):
    items: List[MeasurementResponse] = Field(..., description="List of measurements")
    total: int = Field(..., description="Total number of measurements")

    class Config:
        from_attributes = True
