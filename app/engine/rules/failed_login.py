from datetime import timedelta, datetime
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
        id=event.attributes.user_id
        if id not in self.ipstore:
            self.ipstore[id]=deque()
        window=self.ipstore[id]
        now=event.ingest_time
        window.append(now)
        while window and window[0]<now-self.window:
            window.popleft()

        if len(window)>=self.threshold:
            cur_time= datetime.now()
            return {"entity_id":id,
                    "signal_type":"warning",
                    "rule_name":"FailedLoginBruteForceFlag",
                    "createdAt":cur_time,
                    "evidence":list(window)}
        return None
    


        


