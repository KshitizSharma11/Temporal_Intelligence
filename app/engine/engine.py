from app.models.event import Event
from app.engine.rules.failed_login import FailedLoginRule

class Engine:
    def __init__(self):
        # hardcode ONE rule for now
        self.failed_login_rule = FailedLoginRule()

    def process_event(self, event: Event):
        match event.event_type:
            case "LOGIN_FAILED":
                signal = self.failed_login_rule.evaluate(event)

        if signal:
            print("🚨 SIGNAL:", signal)
