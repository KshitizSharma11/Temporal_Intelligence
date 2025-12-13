from pydantic import BaseModel
from datetime import datetime
from typing import Any
class SignalResponse(BaseModel):
    signal_type:str
    rule_name:str
    entity_id:str
    createdAt:datetime
    evidence:Any

