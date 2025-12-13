from collections import deque
from app.models.event import Event

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

        # First event must be Payment_Success
        if not seq and status != "Payment_Success":
            return {"warning": f"{status} without prior payment", "order_id": order_id}

        # Check ordering
        if seq:
            expected_next = self.VALID_FLOW[len(seq)]
            if status != expected_next:
                return {
                    "warning": f"Invalid order transition",
                    "order_id": order_id,
                    "expected": expected_next,
                    "received": status
                }

        seq.append(status)

        return None
