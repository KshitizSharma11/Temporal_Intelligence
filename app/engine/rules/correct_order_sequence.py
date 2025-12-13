from collections import deque
from app.models.event import Event
from datetime import datetime
class CorrectOrderSequenceRule:
    def __init__(self):
        # order_id -> deque of statuses
        self.order_seq: dict[str, deque] = {}

        self.VALID_FLOW = [
            "Payment_Success",
            "Order_Created",
            "Order_Shipped"
        ]

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
        if not seq and status != "Payment_Success":
            return  {"entity_id":order_id,
                    "signal_type":"warning",
                    "rule_name":"OrderSequence",
                    "createdAt":cur_time,
                    "evidence":["No prior payment"]}

        # Check ordering
        if seq:
            if len(seq) > 2:
                return {
                    "entity_id":order_id,
                    "signal_type":"warning",
                    "rule_name":"OrderSequence",
                    "createdAt":cur_time,
                    "evidence":f"status exceeds duplicate or invalid notification for status: {status}"
                }
            expected_next = self.VALID_FLOW[len(seq)]
            if status != expected_next:
                return {
                    "entity_id":order_id,
                    "signal_type":"warning",
                    "rule_name":"OrderSequence",
                    "createdAt":cur_time,
                    "evidence":list(seq)
                }

        seq.append({"status":status,
                    "timestamp":event.ingest_time})

        return None
