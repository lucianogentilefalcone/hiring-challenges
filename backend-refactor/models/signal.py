from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Signal(Base):
    __tablename__ = "signals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    signal_gid = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    signal_id = Column(String(50), unique=True, nullable=False, index=True)
    signal_name = Column(String(255), nullable=False)
    unit = Column(String(20), nullable=False)

    asset_id = Column(
        UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True
    )
    asset = relationship("Asset", back_populates="signals")

    measurements = relationship(
        "Measurement", back_populates="signal", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Signal(id={self.id}, signal_id={self.signal_id}, signal_name={self.signal_name})>"
