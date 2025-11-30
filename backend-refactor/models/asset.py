from database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    asset_id = Column(String(255), unique=True, nullable=False, index=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    description = Column(String(500), nullable=True)

    signals = relationship(
        "Signal", back_populates="asset", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Asset(id={self.id}, asset_id={self.asset_id})>"
