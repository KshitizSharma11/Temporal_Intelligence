# app/engine/rules/absence_rules.py
from app.models.event import Event
from datetime import timedelta, datetime
from app.models.event import Event
from app.service import event

class AbsenceRules:
    def __init__(self):
        # process_id -> deadline_time
        self.deadlines: dict[str, datetime] = {}
        
    def evaluate(self, event: Event):
        pid = event.attributes.process_id
        status = event.attributes.process_status
        now = event.ingest_time
        self.TIMEOUT= timedelta(seconds=event.attributes.process_timeout or 60)
        if status == "START":
            # register deadline
            self.deadlines[pid] = now + self.TIMEOUT
            return None

        if status == "END":
            # process ended in time → cancel deadline
            if pid in self.deadlines:
                del self.deadlines[pid]
            return None

        return None
    def check_timeouts(self, now: datetime):
        signals = []

        expired = [
            pid for pid, deadline in self.deadlines.items()
            if now >= deadline
        ]

        for pid in expired:
            signals.append({
                "entity_id": pid,
                "signal_type": "warning",
                "rule_name": "AbsenceRule",
                "createdAt": now,
                "evidence": f"Process {pid} did not END within timeout {self.TIMEOUT}"
            })
            del self.deadlines[pid]  # prevent repeated alerts

        return signals
