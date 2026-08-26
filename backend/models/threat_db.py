from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from backend.models.security_event_db import Base


class ThreatDB(Base):

    __tablename__ = "threats"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    event_id = Column(
        Integer,
        nullable=False
    )

    threat_type = Column(
        String(100),
        nullable=False
    )

    risk_score = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(30),
        default="OPEN"
    )

    detected_at = Column(
        DateTime,
        default=datetime.utcnow
    )