from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Attributes(BaseModel):
    ip_address: Optional [str]

class Event(BaseModel):
    event_type:str
    event_id:int
    event_time:datetime
    ingest_time:datetime
    attributes: Optional [Attributes]

class Evidence(BaseModel):
    evidences:list [Event]

