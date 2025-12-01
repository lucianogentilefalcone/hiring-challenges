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


class MeasurementStatsResponse(BaseModel):
    """Statistics for measurements in a date range."""

    signal_id: str = Field(..., description="Signal UUID")
    from_date: datetime = Field(..., description="Start date (ISO format)")
    to_date: datetime = Field(..., description="End date (ISO format)")
    count: int = Field(..., description="Number of measurements")
    mean: Optional[float] = Field(None, description="Average value")
    min: Optional[float] = Field(None, description="Minimum value")
    max: Optional[float] = Field(None, description="Maximum value")
    median: Optional[float] = Field(None, description="Median value")
    std_dev: Optional[float] = Field(None, description="Standard deviation")
