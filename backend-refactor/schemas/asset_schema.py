"""Asset Pydantic schemas for API validation."""

from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    asset_id: str = Field(..., description="Unique asset identifier")
    latitude: float = Field(..., description="Asset latitude")
    longitude: float = Field(..., description="Asset longitude")
    description: str = Field(..., description="Asset description")


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    asset_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None


class AssetResponse(AssetBase):
    id: UUID = Field(..., description="Asset UUID primary key")

    class Config:
        from_attributes = True


class AssetListResponse(BaseModel):
    items: List[AssetResponse] = Field(..., description="List of assets")
    total: int = Field(..., description="Total number of assets")

    class Config:
        from_attributes = True
