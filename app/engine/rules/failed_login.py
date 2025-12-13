from datetime import timedelta
from app.models.event import Event
from collections import deque
class FailedLoginRule:
    def __init__(self):
        self.ipstore:dict[str,deque]={}
        self.threshold=3
        self.window=timedelta(seconds=60)

    def evaluate(self,event:Event):
        if event.event_type != "LOGIN_FAILED":
            return None
        ip=event.attributes.ip_address
        if ip not in self.ipstore:
            self.ipstore[ip]=deque()
        window=self.ipstore[ip]
        now=event.event_time
        window.append(now)
        while window and window[0]<now-self.window:
            window.popleft()

        if len(window)>=self.threshold:
            print (f"limit exceeds for {ip}")
            return {"message":"exceeded"}
        return None
    


        


