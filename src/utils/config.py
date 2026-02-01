"""
Application configuration management.
Handles settings persistence and theme configuration.
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Application configuration container."""
    
    theme: str = 'dark'
    confirm_critical_actions: bool = True
    log_level: str = 'INFO'
    window_width: int = 1000
    window_height: int = 700
    
    _config_path: Optional[Path] = None
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> 'Config':
        """Load configuration from file or create default."""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / 'config.json'
        
        config = cls()
        config._config_path = config_path
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(config, key) and not key.startswith('_'):
                            setattr(config, key, value)
            except (json.JSONDecodeError, IOError):
                pass
        
        return config
    
    def save(self) -> bool:
        """Persist configuration to file."""
        if self._config_path is None:
            return False
        
        try:
            data = {k: v for k, v in asdict(self).items() if not k.startswith('_')}
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except IOError:
            return False
