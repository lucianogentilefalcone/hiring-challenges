from database import Base
from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)

    signal_id = Column(
        UUID(as_uuid=True), ForeignKey("signals.id"), nullable=False, index=True
    )
    signal = relationship("Signal", back_populates="measurements")

    def __repr__(self):
        return f"<Measurement(id={self.id}, value={self.value}, timestamp={self.timestamp})>"
