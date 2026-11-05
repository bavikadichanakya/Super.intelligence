import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any

try:
    import psutil
except ImportError:
    psutil = None

from core.config_manager import get_config

_logger = None

def get_system_resources() -> Dict[str, Any]:
    """Capture current process and system resource metrics (RAM, CPU)."""
    if not psutil:
        return {"ram_process_mb": 0.0, "ram_system_percent": 0.0, "ram_available_mb": 0.0, "cpu_percent": 0.0}
    
    try:
        proc = psutil.Process(os.getpid())
        ram_proc = proc.memory_info().rss / (1024 * 1024)
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=None)
        return {
            "ram_process_mb": round(ram_proc, 2),
            "ram_system_percent": round(mem.percent, 1),
            "ram_available_mb": round(mem.available / (1024 * 1024), 2),
            "ram_total_mb": round(mem.total / (1024 * 1024), 2),
            "cpu_percent": round(cpu, 1)
        }
    except Exception:
        return {"ram_process_mb": 0.0, "ram_system_percent": 0.0, "ram_available_mb": 0.0, "cpu_percent": 0.0}

class ResourceFormatter(logging.Formatter):
    """Custom formatter including process memory stats in logs."""
    def format(self, record):
        res = get_system_resources()
        record.ram = f"RAM:{res['ram_process_mb']}MB"
        return super().format(record)

def setup_logger(name: str = "SUPER.INTELLIGENCEEE") -> logging.Logger:
    global _logger
    if _logger is not None:
        return _logger

    config = get_config()
    logs_dir = config.resolve_path(config.get("paths.logs_dir", "logs"))
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "super_intelligence.log"

    logger = logging.getLogger(name)
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, log_level_name, logging.INFO)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        fmt = ResourceFormatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s] [%(ram)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        ch.setLevel(level)
        logger.addHandler(ch)

        # Rotating file handler (5 MB max per file, 3 backups)
        fh = RotatingFileHandler(
            str(log_file),
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        fh.setFormatter(fmt)
        fh.setLevel(level)
        logger.addHandler(fh)

    _logger = logger
    return _logger

def get_logger(name: str = "SUPER.INTELLIGENCEEE") -> logging.Logger:
    return setup_logger(name)
