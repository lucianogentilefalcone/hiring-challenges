"""Signal Pydantic schemas for API validation."""

from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, Field


class SignalBase(BaseModel):
    signal_gid: UUID = Field(..., description="Global signal identifier")
    signal_id: str = Field(..., description="Unique signal identifier")
    signal_name: str = Field(..., description="Signal name")
    unit: str = Field(..., description="Measurement unit (e.g., kV, kW)")


class SignalCreate(SignalBase):
    asset_id: UUID = Field(..., description="Asset UUID foreign key")


class SignalUpdate(BaseModel):
    signal_name: Optional[str] = None
    unit: Optional[str] = None


class SignalResponse(SignalBase):
    id: UUID = Field(..., description="Signal UUID primary key")
    asset_id: UUID = Field(..., description="Asset UUID foreign key")

    class Config:
        from_attributes = True


class SignalListResponse(BaseModel):
    items: List[SignalResponse] = Field(..., description="List of signals")
    total: int = Field(..., description="Total number of signals")

    class Config:
        from_attributes = True
