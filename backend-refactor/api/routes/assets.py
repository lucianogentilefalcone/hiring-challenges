"""Assets router."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query

from models import Asset
from schemas import (
    AssetCreate,
    AssetUpdate,
    AssetResponse,
    AssetListResponse,
)
from services import AssetService
from dependencies import get_asset_service


router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("", response_model=AssetListResponse)
def list_assets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: AssetService = Depends(get_asset_service),
):
    items, total = service.get_all_assets(skip=skip, limit=limit)
    return AssetListResponse(items=items, total=total)


@router.post("", response_model=AssetResponse, status_code=201)
def create_asset(
    asset_in: AssetCreate,
    service: AssetService = Depends(get_asset_service),
) -> Asset:
    return service.create_asset(asset_in)


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: UUID,
    service: AssetService = Depends(get_asset_service),
) -> Asset:
    return service.get_asset_by_id(asset_id)


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: UUID,
    asset_in: AssetUpdate,
    service: AssetService = Depends(get_asset_service),
) -> Asset:
    return service.update_asset(asset_id, asset_in)


@router.delete("/{asset_id}", status_code=204)
def delete_asset(
    asset_id: UUID,
    service: AssetService = Depends(get_asset_service),
):
    service.delete_asset(asset_id)
