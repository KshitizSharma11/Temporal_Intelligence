from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class Attributes(BaseModel):
    ip_address: Optional[str] = None

class Event(BaseModel):
    event_type: str
    event_time: datetime
    ingest_time: datetime = datetime.now(timezone.utc)
    attributes: Attributes = Attributes()

class Evidence(BaseModel):
    events: list[Event]
