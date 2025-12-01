"""Asset service layer with business logic."""

from typing import List, Tuple
from uuid import UUID

from models import Asset
from schemas import AssetCreate, AssetUpdate
from repositories import AssetRepository
from api.exceptions import (
    AssetNotFoundException,
    AssetAlreadyExistsException,
)


class AssetService:
    """Service for managing assets."""

    def __init__(self, repository: AssetRepository):
        self.repo = repository

    def get_all_assets(
        self, skip: int = 0, limit: int = 100
    ) -> Tuple[List[Asset], int]:
        return self.repo.list_paginated(skip, limit)

    def get_asset_by_id(self, asset_id: UUID) -> Asset:
        asset = self.repo.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundException(asset_id)
        return asset

    def create_asset(self, asset_in: AssetCreate) -> Asset:
        existing = self.repo.get_by_asset_id(asset_in.asset_id)
        if existing:
            raise AssetAlreadyExistsException(asset_in.asset_id)

        asset = Asset(**asset_in.model_dump())
        return self.repo.create(asset)

    def update_asset(self, asset_id: UUID, asset_in: AssetUpdate) -> Asset:
        asset = self.repo.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundException(asset_id)

        if asset_in.asset_id and asset_in.asset_id != asset.asset_id:
            existing = self.repo.get_by_asset_id(asset_in.asset_id)
            if existing:
                raise AssetAlreadyExistsException(asset_in.asset_id)

        update_data = asset_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(asset, key, value)

        return self.repo.update(asset)

    def delete_asset(self, asset_id: UUID) -> None:
        asset = self.repo.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundException(asset_id)
        self.repo.delete(asset_id)
