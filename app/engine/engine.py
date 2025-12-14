import asyncio
from app.models.event import Event
from app.engine.registry import Registry
from app.engine.evaluator import Evaluator
from app.engine.scheduler import Scheduler
from app.storage.persistance import signal_store


class Engine:
    def __init__(self):
        # Initialize registry to load all configs
        self.registry = Registry()
        
        # Initialize evaluator with all rules
        self.evaluator = Evaluator(self.registry)
        
        # Initialize scheduler for timers and periodic checks
        self.scheduler = Scheduler(self.evaluator)
        
        # Keep reference to signal store for backward compatibility
        self.signals = signal_store
        self.timer = self.scheduler.get_absence_timer()

    async def start_timer(self):
        """Start the async scheduler"""
        await self.scheduler.start()

    def process_event(self, event: Event):
        """Process an event through the evaluator"""
        signal = self.evaluator.evaluate(event)

        if signal:
            self.signals.append(signal)
            print(signal)
        
        return signal
