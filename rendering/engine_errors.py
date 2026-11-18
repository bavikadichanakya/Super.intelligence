"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
Exception hierarchy for rendering engines, adapters, preflight checks, and artifacts.
"""

from __future__ import annotations


class EngineError(Exception):
    """Base exception for all engine dispatcher and adapter operations."""
    pass


class EngineUnavailableError(EngineError):
    """Raised when a requested engine binary or runtime is missing or not configured."""
    pass


class AdapterPreflightError(EngineError):
    """Raised when a scene contract fails preflight validation for a specific adapter."""
    pass


class RenderExecutionError(EngineError):
    """Raised when a render process exits with a non-zero exit code."""
    def __init__(self, message: str, exit_code: int = -1, log_path: str = ""):
        super().__init__(f"{message} (exit_code={exit_code}, log={log_path})")
        self.exit_code = exit_code
        self.log_path = log_path


class RenderTimeoutError(EngineError):
    """Raised when a rendering child process exceeds its maximum allocated timeout."""
    def __init__(self, message: str, timeout_seconds: float = 0.0):
        super().__init__(f"{message} (timeout={timeout_seconds}s)")
        self.timeout_seconds = timeout_seconds


class ArtifactValidationError(EngineError):
    """Raised when a rendered artifact fails verification (missing, empty, corrupt, invalid dimensions/fps)."""
    pass


class ResourceThresholdBreachedError(EngineError):
    """Raised when RAM or disk headroom is insufficient to safely launch an engine."""
    pass


class FallbackExhaustedError(EngineError):
    """Raised when both the preferred engine and fallback engine have failed to render a scene."""
    def __init__(self, scene_id: str, preferred_err: str, fallback_err: str = ""):
        msg = f"All rendering engines failed for scene '{scene_id}'. Preferred error: {preferred_err}"
        if fallback_err:
            msg += f" | Fallback error: {fallback_err}"
        super().__init__(msg)
        self.scene_id = scene_id
        self.preferred_err = preferred_err
        self.fallback_err = fallback_err
