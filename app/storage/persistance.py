from collections import deque
from app.models.signals import SignalResponse


class InMemorySignalStore():
    def __init__(self):
        self.signal_store=deque()

    def append(self, signal: SignalResponse):
        self.signal_store.append(signal)

    def getAll(self):
        return list(self.signal_store)
    
    def getById(self, entity_id: str):
        return [s for s in self.signal_store if s.entity_id==entity_id]


signal_store = InMemorySignalStore()
