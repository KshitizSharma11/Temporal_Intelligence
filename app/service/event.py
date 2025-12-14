import asyncio
from app.models.event import Event, Evidence
from app.engine.engine import Engine
from app.storage.memory import InMemoryEventStore

class EventService:
    def __init__(self, store: InMemoryEventStore):
        self.store = store
        self.engine = Engine()
        # Start the absence timer asynchronously
        asyncio.create_task(self.engine.start_timer())

    def pushEvent(self, event: Event):
        self.store.append(event)
        self.engine.process_event(event)
        return {"status": "submitted"}
        


