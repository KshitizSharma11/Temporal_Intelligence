from app.models.event import Event
from app.engine.rules.failed_login import FailedLoginRule
from app.engine.rules.correct_order_sequence import CorrectOrderSequenceRule
from app.engine.rules.absence_rules import AbsenceRules


class Evaluator:
    """Generic FSM executor for evaluating rules against events"""
    
    def __init__(self, registry):
        self.registry = registry
        self.rules = {}
        self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialize all rule instances from registry configs"""
        for rule_name in self.registry.list_rules():
            config = self.registry.get_config(rule_name)
            
            if rule_name == 'login_failed':
                self.rules[rule_name] = FailedLoginRule(config)
            elif rule_name == 'order_sequence':
                self.rules[rule_name] = CorrectOrderSequenceRule(config)
            elif rule_name == 'process_absence':
                self.rules[rule_name] = AbsenceRules(config)
    
    def evaluate(self, event: Event) -> dict:
        """
        Evaluate an event against all applicable rules.
        Returns signal if one is generated, None otherwise.
        """
        signal = None
        
        match event.event_type:
            case "LOGIN_FAILED":
                signal = self.rules['login_failed'].evaluate(event)
            case "ORDER_UPDATE":
                signal = self.rules['order_sequence'].evaluate(event)
            case "PROCESS_UPDATE":
                signal = self.rules['process_absence'].evaluate(event)
        
        return signal
    
    def get_rule(self, rule_name: str):
        """Get a specific rule instance"""
        return self.rules.get(rule_name)
