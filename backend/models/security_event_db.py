from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class SecurityEventDB(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, autoincrement=True)

    timestamp = Column(DateTime, nullable=False)
    source_ip = Column(String(45), nullable=False)
    destination_ip = Column(String(45))
    event_type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    username = Column(String(100))
    message = Column(Text)

    risk_score = Column(Integer, default=0)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )