"""
Integration tests for ResourceGuard hardware protection, environment redirection, and process isolation.
"""

import os
from pathlib import Path
from unittest.mock import patch
import pytest

from rendering.resource_guard import (
    RenderProcessTimeoutError,
    ResourceGuard,
    ResourceThresholdError,
)


class TestResourceGuardIntegration:
    def test_environment_configuration(self, tmp_path):
        guard = ResourceGuard(workspace_root=tmp_path)
        env = guard.configure_environment()

        temp_resolved = str(guard.temp_dir.resolve())
        assert env["TEMP"] == temp_resolved
        assert env["TMP"] == temp_resolved
        assert env["HYPERFRAMES_EXTRACT_CACHE_DIR"] == temp_resolved
        assert env["NODE_OPTIONS"] == "--max-old-space-size=2048"
        assert env["PRODUCER_LOW_MEMORY_MODE"] == "false"

    def test_preflight_safety_passes_on_healthy_system(self):
        guard = ResourceGuard()
        safety = guard.check_preflight_safety()
        assert safety["status"] == "SAFE_TO_RENDER"
        assert safety["free_disk_gb"] >= guard.MIN_FREE_DISK_GB
        assert safety["available_ram_mb"] >= guard.MIN_FREE_RAM_MB

    def test_preflight_safety_fails_on_disk_starvation(self, tmp_path):
        guard = ResourceGuard(workspace_root=tmp_path)
        with patch("psutil.disk_usage") as mock_disk:
            # Mock 0.5 GB free disk (< 2.0 GB min)
            mock_disk.return_value.free = int(0.5 * (1024**3))
            with pytest.raises(ResourceThresholdError) as exc_info:
                guard.check_preflight_safety()
            assert "Insufficient disk space" in str(exc_info.value)

    def test_preflight_safety_fails_on_memory_starvation(self, tmp_path):
        guard = ResourceGuard(workspace_root=tmp_path)
        with patch("psutil.disk_usage") as mock_disk, patch("psutil.virtual_memory") as mock_mem:
            # Mock healthy disk space (10 GB free)
            mock_disk.return_value.free = int(10.0 * (1024**3))
            # Mock 100 MB available RAM (< 200 MB min)
            mock_mem.return_value.available = int(100 * (1024**2))
            mock_mem.return_value.total = int(8 * (1024**3))
            mock_mem.return_value.percent = 98.0
            with pytest.raises(ResourceThresholdError) as exc_info:
                guard.check_preflight_safety()
            assert "Memory starvation" in str(exc_info.value)

    def test_isolated_render_timeout_termination(self):
        guard = ResourceGuard()  # Uses workspace_root on Drive A: (healthy disk space)
        # Execute a command that sleeps longer than timeout (e.g. 1.0s timeout)
        venv_py = "A:/SUPER.INTELLIGENCEEE/.venv/Scripts/python.exe"
        py_cmd = [venv_py, "-c", "import time; time.sleep(5)"]
        with pytest.raises(RenderProcessTimeoutError):
            guard.execute_isolated_render(py_cmd, timeout_seconds=1.0)
