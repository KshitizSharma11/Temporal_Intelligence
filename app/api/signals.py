from app.models.signals import SignalResponse
from app.service.signals import SignalService
from fastapi import APIRouter
router = APIRouter(prefix="/signals")
signalService=SignalService()

@router.get("/",response_model=list[SignalResponse])
def get_all_signals():
   return signalService.getAll()

@router.get("/{id}",response_model=SignalResponse)
def get_signal(id:str):
   return signalService.getById(id)
    