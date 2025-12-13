from app.models.event import Event
from app.engine.rules.failed_login import FailedLoginRule
from app.engine.rules.correct_order_sequence import CorrectOrderSequenceRule


class Engine:
    def __init__(self):
        # hardcode ONE rule for now
        self.failed_login_rule = FailedLoginRule()
        self.verify_sequence= CorrectOrderSequenceRule()
    def process_event(self, event: Event):
        match event.event_type:
            case "LOGIN_FAILED":
                signal = self.failed_login_rule.evaluate(event)
            case "ORDER_UPDATE":
                signal = self.verify_sequence.evaluate(event)

        if signal:
            print(signal)
