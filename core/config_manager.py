import os
import json
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent.parent

class ConfigManager:
    """Manages application configuration loaded from config.json and environment."""
    
    _instance = None
    
    def __new__(cls, config_path: str = None):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._init_config(config_path)
        return cls._instance

    def _init_config(self, config_path: str = None):
        self.base_dir = BASE_DIR
        self.config_path = Path(config_path) if config_path else self.base_dir / "config.json"
        
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.data: Dict[str, Any] = json.load(f)
        else:
            self.data = {}
            
        self._apply_env_overrides()

    def _apply_env_overrides(self):
        """Allow environment variables to override key settings safely."""
        if os.getenv("SUPER_HOST"):
            self.data.setdefault("server", {})["host"] = os.getenv("SUPER_HOST")
        if os.getenv("SUPER_PORT"):
            self.data.setdefault("server", {})["port"] = int(os.getenv("SUPER_PORT"))
        if os.getenv("MAX_CONCURRENT_RENDERS"):
            self.data.setdefault("rendering", {})["max_concurrent_renders"] = int(os.getenv("MAX_CONCURRENT_RENDERS"))
        if os.getenv("CLEANUP_TEMP_FILES"):
            self.data.setdefault("rendering", {})["cleanup_temp_files"] = os.getenv("CLEANUP_TEMP_FILES").lower() == "true"

    def get(self, key_path: str, default: Any = None) -> Any:
        """Retrieve nested configuration using dot notation, e.g. 'brand.name'."""
        keys = key_path.split(".")
        val = self.data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

    def resolve_path(self, relative_path: str) -> Path:
        """Resolve a path relative to the project base directory."""
        p = Path(relative_path)
        if p.is_absolute():
            return p
        return (self.base_dir / p).resolve()

    def reload(self):
        """Reload configuration from disk."""
        self._init_config(str(self.config_path))

# Global convenience accessor
def get_config() -> ConfigManager:
    return ConfigManager()
