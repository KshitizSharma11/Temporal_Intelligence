import asyncio
from datetime import datetime, timezone
from app.storage.persistance import signal_store


class Scheduler:
    """Manages timers and periodic checks for the engine"""
    
    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.absence_rule = None
        self.signals = signal_store
        self._setup_timers()
    
    def _setup_timers(self):
        """Initialize all timers"""
        self.absence_rule = self.evaluator.get_rule('process_absence')
    
    async def _run_absence_check(self):
        """Periodically check for process absence timeouts"""
        while True:
            if self.absence_rule:
                now = datetime.now(timezone.utc)
                timeout_signals = self.absence_rule.check_timeouts(now)
                for signal in timeout_signals:
                    self.signals.append(signal)
                    print(signal)
            await asyncio.sleep(10)  # Check every 10 seconds
    
    async def start(self):
        """Start all scheduled tasks"""
        if self.absence_rule:
            await asyncio.create_task(self._run_absence_check())
    
    async def stop(self):
        """Stop all scheduled tasks"""
        # Placeholder for cleanup logic
        pass
    
    def get_absence_timer(self):
        """Get the absence rule instance (for backward compatibility)"""
        return self.absence_rule
