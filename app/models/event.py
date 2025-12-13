from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime, timezone

class Attributes(BaseModel):
    user_id: Optional[str] = None
    order_id: Optional[str]= None
    order_status: Optional[str]=None

class Event(BaseModel):
    event_type: str
    event_time: datetime
    ingest_time: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    attributes: Attributes = Field(default_factory=Attributes)

class Evidence(BaseModel):
    events: list[Event]
