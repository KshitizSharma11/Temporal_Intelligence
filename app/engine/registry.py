import yaml
from pathlib import Path


class Registry:
    """Centralized configuration registry for all rules"""
    
    def __init__(self, rules_dir: str = 'app/engine/rules'):
        self.rules_dir = Path(rules_dir)
        self.configs = {}
        self._load_all_configs()
    
    def _load_all_configs(self):
        """Load all YAML config files from rules directory"""
        yaml_files = self.rules_dir.glob('*.yaml')
        for yaml_file in yaml_files:
            rule_name = yaml_file.stem  # filename without .yaml
            with open(yaml_file, 'r') as f:
                self.configs[rule_name] = yaml.safe_load(f)
    
    def get_config(self, rule_name: str) -> dict:
        """Retrieve configuration for a specific rule"""
        if rule_name not in self.configs:
            raise ValueError(f"Configuration not found for rule: {rule_name}")
        return self.configs[rule_name]
    
    def list_rules(self) -> list[str]:
        """List all available rules"""
        return list(self.configs.keys())
    
    def reload_configs(self):
        """Reload all configurations from disk"""
        self.configs.clear()
        self._load_all_configs()
