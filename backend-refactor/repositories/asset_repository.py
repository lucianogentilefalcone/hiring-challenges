from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from models import Asset


class AssetRepository:
    """Repository for Asset CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, asset: Asset) -> Asset:
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def get_by_id(self, asset_id: UUID) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def get_by_asset_id(self, asset_id: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.asset_id == asset_id).first()

    def list_paginated(self, skip: int, limit: int):
        query = self.db.query(Asset)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def update(self, asset: Asset) -> Asset:
        asset = self.db.merge(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete(self, asset_id: UUID) -> bool:
        asset = self.get_by_id(asset_id)
        if not asset:
            return False
        self.db.delete(asset)
        self.db.commit()
        return True
