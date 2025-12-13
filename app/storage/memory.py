from collections import deque
from app.models.event import Event
class InMemoryEventStore:
    def __init__ (self):
        self.memory=deque()

    def append(self,event:Event):
        self.memory.append(event)

    


 