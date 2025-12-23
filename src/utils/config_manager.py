"""
Configuration Manager Module
============================
Handles loading, saving, and managing application settings via JSON.
"""

import json
import os
from typing import Any, Dict, Optional


class ConfigManager:
    """
    Manages application configuration stored in a JSON file.
    
    Handles default values, loading existing configurations,
    and immediate persistence on changes.
    """
    
    # Default configuration values
    DEFAULT_CONFIG: Dict[str, Any] = {
        "save_game_path": "",
        "wagon_capacity": 24000,
        "bale_hay": 5500,
        "bale_straw": 7500,
        "bale_silage": 5000,
        "ratios": {
            "hay": 38,
            "silage": 30,
            "straw": 30,
            "mineral": 2
        }
    }
    
    def __init__(self, config_path: str = "config.json") -> None:
        """
        Initialize the ConfigManager.
        
        Args:
            config_path: Path to the JSON configuration file.
        """
        self._config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """
        Load configuration from file or create default if not exists.
        """
        if os.path.exists(self._config_path):
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self._config = self._merge_with_defaults(loaded_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                self._config = self.DEFAULT_CONFIG.copy()
                self._save_config()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
            self._save_config()
    
    def _merge_with_defaults(self, loaded: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge loaded configuration with defaults to ensure all keys exist.
        
        Args:
            loaded: The loaded configuration dictionary.
            
        Returns:
            Merged configuration with all default keys.
        """
        result = self.DEFAULT_CONFIG.copy()
        
        for key, default_value in self.DEFAULT_CONFIG.items():
            if key in loaded:
                if isinstance(default_value, dict) and isinstance(loaded[key], dict):
                    # Deep merge for nested dictionaries
                    merged_nested = default_value.copy()
                    merged_nested.update(loaded[key])
                    result[key] = merged_nested
                else:
                    result[key] = loaded[key]
        
        return result
    
    def _save_config(self) -> None:
        """
        Save current configuration to the JSON file.
        """
        try:
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error: Could not save config file: {e}")
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: The configuration key to retrieve.
            default: Default value if key doesn't exist.
            
        Returns:
            The configuration value or default.
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value and save immediately.
        
        Args:
            key: The configuration key to set.
            value: The value to store.
        """
        self._config[key] = value
        self._save_config()
    
    def get_ratio(self, ratio_key: str) -> int:
        """
        Get a specific ratio value.
        
        Args:
            ratio_key: The ratio key (hay, silage, straw, mineral).
            
        Returns:
            The ratio value as integer.
        """
        ratios = self._config.get("ratios", {})
        return ratios.get(ratio_key, 0)
    
    def set_ratio(self, ratio_key: str, value: int) -> None:
        """
        Set a specific ratio value and save.
        
        Args:
            ratio_key: The ratio key (hay, silage, straw, mineral).
            value: The ratio value to set.
        """
        if "ratios" not in self._config:
            self._config["ratios"] = {}
        self._config["ratios"][ratio_key] = value
        self._save_config()
    
    def get_all_ratios(self) -> Dict[str, int]:
        """
        Get all ratio values.
        
        Returns:
            Dictionary of all ratios.
        """
        return self._config.get("ratios", self.DEFAULT_CONFIG["ratios"]).copy()
    
    def set_all_ratios(self, ratios: Dict[str, int]) -> None:
        """
        Set all ratio values at once.
        
        Args:
            ratios: Dictionary of ratio values.
        """
        self._config["ratios"] = ratios
        self._save_config()
    
    def reset_to_defaults(self) -> None:
        """
        Reset all configuration to default values.
        """
        self._config = self.DEFAULT_CONFIG.copy()
        self._save_config()
    
    @property
    def config_path(self) -> str:
        """Get the configuration file path."""
        return self._config_path
