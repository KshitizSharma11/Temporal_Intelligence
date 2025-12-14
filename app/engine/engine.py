from app.models.event import Event
from app.engine.rules.failed_login import FailedLoginRule
from app.engine.rules.correct_order_sequence import CorrectOrderSequenceRule
from app.engine.rules.absence_rules import AbsenceRules
from app.storage.persistance import signal_store
from datetime import datetime, timezone

class Engine:
    def __init__(self):
        # hardcode ONE rule for now
        self.failed_login_rule = FailedLoginRule()
        self.verify_sequence= CorrectOrderSequenceRule()
        self.absence_rules= AbsenceRules()
        self.signals= signal_store
    def process_event(self, event: Event):
        match event.event_type:
            case "LOGIN_FAILED":
                signal = self.failed_login_rule.evaluate(event)
            case "ORDER_UPDATE":
                signal = self.verify_sequence.evaluate(event)
            case "PROCESS_UPDATE":
                signal = self.absence_rules.evaluate(event)
            case _:
                signal = None

        if signal:
            self.signals.append(signal)
            print(signal)

        now = datetime.now(timezone.utc)
        timeout_signals = self.absence_rules.check_timeouts(now)

        for s in timeout_signals:
            self.signals.append(s)
            print(s)