from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
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

    def list_all(self) -> List[Asset]:
        return self.db.query(Asset).all()

    def update(self, asset: Asset) -> Asset:
        self.db.merge(asset)
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
