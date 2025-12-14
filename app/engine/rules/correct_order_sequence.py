from collections import deque
from app.models.event import Event
from datetime import datetime
class CorrectOrderSequenceRule:
    def __init__(self, config: dict):
        # order_id -> deque of statuses
        self.order_seq: dict[str, deque] = {}

        self.valid_flow = config['valid_flow']
        self.severity = config['severity']
        self.signal_type = config['signal_type']
        self.rule_name = config['rule_name']

    def evaluate(self, event: Event):
        order_id = event.attributes.order_id
        status = event.attributes.order_status

        if not order_id or not status:
            return None

        if order_id not in self.order_seq:
            self.order_seq[order_id] = deque()

        seq = self.order_seq[order_id]
        cur_time=datetime.now()
        # First event must be Payment_Success
        if not seq and status != self.valid_flow[0]:
            return  {"entity_id":order_id,
                    "signal_type":self.signal_type,
                    "rule_name":self.rule_name,
                    "severity":self.severity,
                    "createdAt":cur_time,
                    "evidence":["No prior payment"]}

        # Check ordering
        if seq:
            if len(seq) > len(self.valid_flow) - 1:
                return {
                    "entity_id":order_id,
                    "signal_type":self.signal_type,
                    "rule_name":self.rule_name,
                    "severity":self.severity,
                    "createdAt":cur_time,
                    "evidence":f"status exceeds duplicate or invalid notification for status: {status}"
                }
            expected_next = self.valid_flow[len(seq)]
            if status != expected_next:
                return {
                    "entity_id":order_id,
                    "signal_type":self.signal_type,
                    "rule_name":self.rule_name,
                    "severity":self.severity,
                    "createdAt":cur_time,
                    "evidence":list(seq)
                }

        seq.append({"status":status,
                    "timestamp":event.ingest_time})

        return None
