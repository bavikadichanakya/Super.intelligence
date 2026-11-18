"""
SUPER.INTELLIGENCEEE — Global Application Kill Switch & Emergency Stop
Application-layer enforcement: halts tasks, cancels queued work, blocks publishing,
and prevents external API side effects when owner/STOP is engaged.
"""

from __future__ import annotations

import datetime
import logging
import os
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from core.config import get_config

logger = logging.getLogger("super_intelligence.kill_switch")


class KillSwitchActiveError(RuntimeError):
    """Raised whenever an operation is attempted while the kill switch is active."""


class KillSwitch:
    """Centrally enforced emergency stop controller."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(KillSwitch, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, stop_file: Optional[Path | str] = None):
        if stop_file is not None:
            self.stop_file = Path(stop_file).resolve()
            self._initialized = True
            return
        if self._initialized:
            return
        self.stop_file = get_config().resolve_path("owner/STOP").resolve()
        self._initialized = True

    def is_active(self) -> bool:
        """Returns True if the kill switch file owner/STOP exists on disk."""
        return self.stop_file.exists()

    def activate(self, reason: str = "Emergency stop requested by owner") -> None:
        """Engages the kill switch by creating owner/STOP with audit metadata."""
        now = datetime.datetime.now().isoformat()
        content = f"# GLOBAL EMERGENCY STOP ENGAGED\nTimestamp: {now}\nReason: {reason}\n"
        self.stop_file.parent.mkdir(parents=True, exist_ok=True)
        self.stop_file.write_text(content, encoding="utf-8")
        logger.critical(f"GLOBAL KILL SWITCH ACTIVATED: {reason}")

    def deactivate(self, operator: str = "Owner") -> None:
        """Disengages the kill switch by safely removing owner/STOP."""
        if self.stop_file.exists():
            try:
                self.stop_file.unlink()
                logger.info(f"Global kill switch DEACTIVATED by {operator}.")
            except Exception as e:
                logger.error(f"Failed to remove kill switch file: {e}")

    def assert_not_active(self, operation: str = "operation") -> None:
        """
        Guards an execution point. Raises KillSwitchActiveError immediately if STOP file exists.
        Must be called:
        - Before task execution
        - Before agent dispatch
        - Before external API calls
        - Before publishing
        - Before sending messages
        - Before financial actions
        """
        if self.is_active():
            err_msg = f"Operation '{operation}' BLOCKED: Global Kill Switch is actively engaged ({self.stop_file})."
            logger.critical(err_msg)
            raise KillSwitchActiveError(err_msg)

    def guard(self, operation_name: str = "operation") -> Callable:
        """Decorator to guard any function with the kill switch."""
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                self.assert_not_active(operation_name)
                return func(*args, **kwargs)
            return wrapper
        return decorator


def get_kill_switch() -> KillSwitch:
    return KillSwitch()

