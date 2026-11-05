import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Config:
    """Central configuration manager for SUPER.INTELLIGENCEEE."""
    
    _instance: Optional["Config"] = None

    def __new__(cls, config_file: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._init_config(config_file)
        return cls._instance

    def _init_config(self, config_file: Optional[str] = None):
        self.root: Path = PROJECT_ROOT
        self.config_file = Path(config_file) if config_file else self.root / "config.yaml"
        
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.data: Dict[str, Any] = yaml.safe_load(f) or {}
        else:
            self.data = {}

        self._apply_env_overrides()

    def _apply_env_overrides(self):
        if os.getenv("SUPER_PORT"):
            self.data.setdefault("server", {})["port"] = int(os.getenv("SUPER_PORT"))
        if os.getenv("SUPER_HOST"):
            self.data.setdefault("server", {})["host"] = os.getenv("SUPER_HOST")
        if os.getenv("MAX_WORKERS"):
            self.data.setdefault("system", {})["max_workers"] = int(os.getenv("MAX_WORKERS"))

    def get(self, dot_path: str, default: Any = None) -> Any:
        keys = dot_path.split(".")
        val = self.data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

    def resolve_path(self, relative_path: str) -> Path:
        p = Path(relative_path)
        if p.is_absolute():
            return p
        return (self.root / p).resolve()

    def reload(self):
        self._init_config(str(self.config_file))

def get_config() -> Config:
    return Config()

