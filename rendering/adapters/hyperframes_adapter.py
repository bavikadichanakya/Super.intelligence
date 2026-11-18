"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
HyperFramesAdapter: Executes timeline composition, editorial HUDs, kinetic typography, and multi-scene layouts.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional

from core.universal_scene_contract import RenderingEngine, UniversalSceneContract
from rendering.adapters.base_adapter import BaseEngineAdapter
from rendering.engine_errors import (
    AdapterPreflightError,
    ArtifactValidationError,
    EngineUnavailableError,
    RenderExecutionError,
    RenderTimeoutError,
)
from rendering.execution_context import ExecutionContext
from rendering.render_artifact import RenderArtifact
from rendering.resource_guard import RenderProcessTimeoutError, ResourceGuard

logger = logging.getLogger("super_intelligence.hyperframes_adapter")


class HyperFramesAdapter(BaseEngineAdapter):
    """
    Adapter for HyperFrames (HTML/CSS/GSAP) timeline rendering.
    Handles editorial HUDs, kinetic typography, graphic layouts, and multi-track compositions.
    """

    _class_cached_availability: Optional[bool] = None

    def __init__(
        self,
        renderer_dir: Optional[Path | str] = None,
        resource_guard: Optional[ResourceGuard] = None,
    ):
        super().__init__(resource_guard=resource_guard)
        self.workspace_root = Path("A:/SUPER.INTELLIGENCEEE").resolve()
        self.renderer_dir = Path(renderer_dir or (self.workspace_root / "renderer")).resolve()
        self.compositions_dir = self.renderer_dir / "compositions"
        self.compositions_dir.mkdir(parents=True, exist_ok=True)
        self._cached_version: Optional[str] = None

    @property
    def engine_name(self) -> RenderingEngine:
        return RenderingEngine.HYPERFRAMES

    def is_available(self) -> bool:
        """Verifies that npx and HyperFrames are runnable on the host."""
        if HyperFramesAdapter._class_cached_availability is not None:
            return HyperFramesAdapter._class_cached_availability

        has_npx = bool(shutil.which("npx") or shutil.which("npx.cmd"))
        HyperFramesAdapter._class_cached_availability = has_npx
        return HyperFramesAdapter._class_cached_availability

    def get_version(self) -> str:
        """Returns the HyperFrames CLI version string."""
        if self._cached_version:
            return self._cached_version
        try:
            npx_bin = "npx.cmd" if os.name == "nt" else "npx"
            res = subprocess.run([npx_bin, "hyperframes", "--version"], capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                self._cached_version = f"HyperFrames v{res.stdout.strip()}"
                return self._cached_version
        except Exception as e:
            logger.warning(f"Failed to query HyperFrames version: {e}")
        return "HyperFrames (version unknown)"

    def validate_scene(self, scene: UniversalSceneContract) -> bool:
        """Validates scene contract compatibility with HyperFrames."""
        if not self.is_available():
            raise EngineUnavailableError("HyperFrames CLI is not available in Node.js environment.")

        w, h = scene.output_resolution
        if w <= 0 or h <= 0:
            raise AdapterPreflightError(f"Invalid resolution for scene {scene.scene_id}: {scene.output_resolution}")

        duration = scene.actual_duration_seconds or scene.narration_duration_seconds or 0.0
        if duration <= 0.0:
            raise AdapterPreflightError(f"Invalid duration for scene {scene.scene_id}: {duration}s")

        return True

    def prepare(self, scene: UniversalSceneContract, context: ExecutionContext) -> Dict[str, Any]:
        """
        Generates an HTML composition adhering to the HyperFrames paused timeline contract.
        """
        self.validate_scene(scene)

        w, h = scene.output_resolution
        fps = int(scene.frame_rate)
        duration = float(scene.actual_duration_seconds or scene.narration_duration_seconds or 5.0)

        comp_filename = f"gen_hf_{scene.scene_id}_{context.timestamp}.html"
        comp_file = self.compositions_dir / comp_filename

        headline = (scene.narrative_purpose or scene.visual_concept or "TECHNICAL DOCUMENTARY").upper()
        subhead = (scene.audience_takeaway or scene.mechanism_description or "Autonomous Pipeline Analysis")
        headline_clean = headline[:45].replace('"', '&quot;')
        subhead_clean = subhead[:70].replace('"', '&quot;')

        stage_str = f"PULSE {scene.sequence_number:02d} / {scene.narrative_stage.upper()}"

        html_content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={w}, height={h}" />
    <title>HyperFrames Scene — {scene.scene_id}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --ground: #07090e;
        --ink: #f8fafc;
        --cyan: #00e5ff;
        --purple: #8b5cf6;
        --font-main: "Inter", -apple-system, sans-serif;
        --font-mono: "JetBrains Mono", monospace;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: {w}px;
        height: {h}px;
        overflow: hidden;
        background: var(--ground);
        font-family: var(--font-main);
      }}
      #root {{
        width: {w}px;
        height: {h}px;
        position: relative;
        background: radial-gradient(circle at 50% 30%, #151a2e 0%, #07090e 100%);
        overflow: hidden;
      }}
      .scene-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: {w}px;
        height: {h}px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 240px 80px 340px 80px;
        pointer-events: none;
      }}
      .tech-hud {{
        display: flex;
        justify-content: center;
      }}
      .hud-pill {{
        background: rgba(14, 20, 36, 0.9);
        color: var(--cyan);
        border: 2px solid var(--cyan);
        padding: 12px 32px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 24px;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.25);
        font-family: var(--font-mono);
      }}
      .headline-wrapper {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
      }}
      .scene-headline {{
        color: var(--ink);
        font-size: 52px;
        font-weight: 900;
        text-align: center;
        line-height: 1.25;
        letter-spacing: -0.5px;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.9);
      }}
      .scene-subhead {{
        color: #94a3b8;
        font-size: 28px;
        font-weight: 500;
        text-align: center;
        max-width: 800px;
        line-height: 1.4;
      }}
      .graphic-center {{
        width: 320px;
        height: 320px;
        border-radius: 50%;
        border: 3px dashed var(--cyan);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 35px rgba(0, 229, 255, 0.2);
      }}
      .graphic-inner {{
        width: 240px;
        height: 240px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, rgba(14, 20, 36, 0.8) 100%);
        border: 2px solid var(--purple);
      }}
      .scanlines {{
        position: absolute;
        top: 0;
        left: 0;
        width: {w}px;
        height: {h}px;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
        background-size: 100% 4px;
        pointer-events: none;
        z-index: 10;
        opacity: 0.35;
      }}
    </style>
  </head>
  <body>
    <div id="root"
         data-composition-id="{scene.scene_id}"
         data-start="0"
         data-duration="{duration:.2f}"
         data-width="{w}"
         data-height="{h}"
         data-fps="{fps}">
      <div class="scene-overlay">
        <div class="tech-hud">
          <span class="hud-pill">{stage_str}</span>
        </div>
        <div style="display: flex; justify-content: center;">
          <div class="graphic-center">
            <div class="graphic-inner"></div>
          </div>
        </div>
        <div class="headline-wrapper">
          <h2 class="scene-headline">{headline_clean}</h2>
          <p class="scene-subhead">{subhead_clean}</p>
        </div>
      </div>
      <div class="scanlines"></div>
    </div>

    <script>
      // HyperFrames Paused Timeline Contract
      const tl = gsap.timeline({{ paused: true }});
      
      const hudPill = document.querySelector(".hud-pill");
      const headline = document.querySelector(".scene-headline");
      const subhead = document.querySelector(".scene-subhead");
      const graphic = document.querySelector(".graphic-center");
      const inner = document.querySelector(".graphic-inner");

      // HUD entrance
      tl.fromTo(hudPill,
        {{ opacity: 0, scale: 0.85, y: -20 }},
        {{ opacity: 1, scale: 1.0, y: 0, duration: 0.5, ease: "back.out(1.5)" }},
        0.1
      );

      // Central graphic rotation & pulse
      tl.fromTo(graphic,
        {{ opacity: 0, scale: 0.7, rotation: -45 }},
        {{ opacity: 1, scale: 1.0, rotation: 0, duration: 0.8, ease: "power2.out" }},
        0.2
      );
      tl.to(graphic,
        {{ rotation: 180, duration: {duration:.2f} - 0.2, ease: "none" }},
        0.2
      );
      tl.fromTo(inner,
        {{ scale: 0.9 }},
        {{ scale: 1.1, duration: 1.5, repeat: -1, yoyo: true, ease: "sine.inOut" }},
        0.2
      );

      // Typography entrance
      tl.fromTo(headline,
        {{ opacity: 0, y: 30 }},
        {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }},
        0.4
      );
      tl.fromTo(subhead,
        {{ opacity: 0, y: 20 }},
        {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }},
        0.6
      );

      window.__timelines = window.__timelines || {{}};
      window.__timelines["{scene.scene_id}"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

        with open(comp_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return {
            "composition_file": comp_file,
            "relative_composition": f"compositions/{comp_filename}",
        }

    def render(self, scene: UniversalSceneContract, context: ExecutionContext) -> RenderArtifact:
        """
        Renders the HyperFrames composition.
        """
        prep = self.prepare(scene, context)
        comp_file = prep["composition_file"]
        rel_comp = prep["relative_composition"]
        target_output = context.get_output_stem_path(".mp4")

        npx_bin = "npx.cmd" if os.name == "nt" else "npx"
        cmd = [
            npx_bin, "hyperframes", "render",
            "renderer",
            "-c", rel_comp,
            "-o", str(target_output),
        ]

        timeout = max(float(scene.timeout_seconds or 360.0), float(scene.actual_duration_seconds or 10.0) * 35.0)
        logger.info(f"Launching HyperFrames render for scene '{scene.scene_id}' (timeout: {timeout:.1f}s)...")
        start_time = time.time()

        try:
            result = self.guard.execute_isolated_render(
                command=cmd,
                cwd=context.workspace_root,
                timeout_seconds=timeout,
                log_file=context.log_file,
            )
        except RenderProcessTimeoutError as e:
            raise RenderTimeoutError(str(e), timeout_seconds=timeout)
        except Exception as e:
            raise RenderExecutionError(f"HyperFrames render process failed: {e}", log_path=str(context.log_file))
        finally:
            if comp_file.exists():
                try:
                    comp_file.unlink()
                except Exception:
                    pass

        if not result["success"]:
            raise RenderExecutionError(
                f"HyperFrames render exited with code {result['returncode']}",
                exit_code=result["returncode"],
                log_path=result.get("log_path", ""),
            )

        if not target_output.exists() or target_output.stat().st_size == 0:
            raise ArtifactValidationError(f"HyperFrames completed but output missing or empty: {target_output}")

        render_time = time.time() - start_time
        logger.info(
            f"HyperFrames successfully rendered '{scene.scene_id}' to {target_output} "
            f"in {render_time:.2f}s (Peak RAM: {result.get('peak_ram_mb', 0.0)} MB)"
        )

        return self.verify_output(
            output_path=target_output,
            scene=scene,
            render_time_seconds=render_time,
            peak_ram_mb=result.get("peak_ram_mb", 0.0),
        )
