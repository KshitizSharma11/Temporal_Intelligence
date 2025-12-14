# app/engine/rules/absence_rules.py
from app.models.event import Event
from datetime import timedelta, datetime
from app.models.event import Event


class AbsenceRules:
    def __init__(self, config: dict):
        # process_id -> deadline_time
        self.deadlines: dict[str, datetime] = {}
        self.timeout = timedelta(seconds=config['timeout_seconds'])
        self.severity = config['severity']
        self.signal_type = config['signal_type']
        self.rule_name = config['rule_name']
        
    def evaluate(self, event: Event):
        pid = event.attributes.process_id
        status = event.attributes.process_status
        now = event.ingest_time
        timeout = timedelta(seconds=event.attributes.process_timeout or self.timeout.total_seconds())
        if status == "START":
            # register deadline
            self.deadlines[pid] = now + timeout
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
                "signal_type": self.signal_type,
                "rule_name": self.rule_name,
                "severity": self.severity,
                "createdAt": now,
                "evidence": f"Process {pid} did not END within timeout {self.timeout}"
            })
            del self.deadlines[pid]  # prevent repeated alerts

        return signals
