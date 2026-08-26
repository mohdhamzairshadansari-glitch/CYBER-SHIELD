from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SecurityEvent(BaseModel):
    timestamp: datetime
    source_ip: str
    destination_ip: Optional[str] = None
    event_type: str
    severity: str
    username: Optional[str] = None
    message: str