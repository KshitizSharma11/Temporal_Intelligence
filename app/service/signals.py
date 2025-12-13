from app.models.signals import SignalResponse
from app.storage.persistance import signal_store
class SignalService():
    def __init__(self):
        self.signals=signal_store
    
    def getAll(self):
     return self.signals.getAll()
    
    def getById(self,id:str):
       return self.signals.getById(id)