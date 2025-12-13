from app.models.event import Event, Evidence
from app.storage.memory import InMemoryEventStore

class EventService:
    def __init__(self,store:InMemoryEventStore):
        self.store=store
    def pushEvent(self,event:Event):
        self.store.append(event)
        


