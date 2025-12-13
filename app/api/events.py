from fastapi import APIRouter
from app.models.event import Event,Attributes
from app.service.event import EventService
from app.storage.memory import InMemoryEventStore
router=APIRouter(prefix="/event")
store=InMemoryEventStore()
eventService=EventService(store)
@router.post("/createEvent")
def sendEvent(event:Event):
    eventService.pushEvent(event=event)
    return {"status":"accepted"}
    