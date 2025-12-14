from datetime import timedelta, datetime
from app.models.event import Event
from collections import deque

class FailedLoginRule:
    def __init__(self, config: dict):
        self.ipstore: dict[str, deque] = {}
        self.threshold = config['threshold']
        self.window = timedelta(seconds=config['window_seconds'])
        self.severity = config['severity']
        self.signal_type = config['signal_type']
        self.rule_name = config['rule_name']
        self.cooldown = timedelta(seconds=config.get('cooldown_seconds', 300))
        self.last_signal_time: dict[str, datetime] = {}

    def evaluate(self, event: Event):
        if event.event_type != "LOGIN_FAILED":
            return None
        id = event.attributes.user_id
        if id not in self.ipstore:
            self.ipstore[id] = deque()
        window = self.ipstore[id]
        now = event.ingest_time
        window.append(now)
        while window and window[0] < now - self.window:
            window.popleft()

        if len(window) >= self.threshold:
            cur_time = datetime.now()
            last_signal = self.last_signal_time.get(id)

            # Check if we're in cooldown period - skip signal if we are
            if last_signal and cur_time - last_signal < self.cooldown:
                return None

            # Record this signal and send it
            self.last_signal_time[id] = cur_time
            return {"entity_id": id,
                    "signal_type": self.signal_type,
                    "rule_name": self.rule_name,
                    "severity": self.severity,
                    "createdAt": cur_time,
                    "evidence": list(window)}
        return None
    


        


