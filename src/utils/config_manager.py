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
        },
        "prices": {
            "hay": 100,
            "silage": 150,
            "straw": 50,
            "mineral": 800,
            "tmr": 0 # Estimated cost placeholder
        }
    }
    
    def __init__(self, config_path: str = "config.json") -> None:
        self._config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        if os.path.exists(self._config_path):
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    self._config = self._merge_with_defaults(loaded_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                self._config = self.DEFAULT_CONFIG.copy()
                self._save_config()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
            self._save_config()
    
    def _merge_with_defaults(self, loaded: Dict[str, Any]) -> Dict[str, Any]:
        result = self.DEFAULT_CONFIG.copy()
        for key, default_value in self.DEFAULT_CONFIG.items():
            if key in loaded:
                if isinstance(default_value, dict) and isinstance(loaded[key], dict):
                    merged_nested = default_value.copy()
                    merged_nested.update(loaded[key])
                    result[key] = merged_nested
                else:
                    result[key] = loaded[key]
        return result
    
    def _save_config(self) -> None:
        try:
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error: Could not save config file: {e}")
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
        self._save_config()
    
    def get_ratio(self, ratio_key: str) -> int:
        ratios = self._config.get("ratios", {})
        return ratios.get(ratio_key, 0)
    
    def set_all_ratios(self, ratios: Dict[str, int]) -> None:
        self._config["ratios"] = ratios
        self._save_config()

    def get_price(self, key: str) -> float:
        prices = self._config.get("prices", {})
        return prices.get(key, 0.0)

    def set_price(self, key: str, value: float) -> None:
        if "prices" not in self._config:
            self._config["prices"] = {}
        self._config["prices"][key] = value
        self._save_config()
    
    def reset_to_defaults(self) -> None:
        self._config = self.DEFAULT_CONFIG.copy()
        self._save_config()