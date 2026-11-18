"""
SUPER.INTELLIGENCEEE — Phase 4.3.2B Multi-Engine Rendering Dispatcher
ThreeJsAdapter: Executes procedural 3D/2.5D hardware lattices, network topologies, and camera journeys
via Three.js r128 within HyperFrames headless Chrome ANGLE Direct3D11 WebGL.
Zero Blender dependency strictly enforced.
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

logger = logging.getLogger("super_intelligence.threejs_adapter")


class ThreeJsAdapter(BaseEngineAdapter):
    """
    Adapter for procedural Three.js (r128) rendering.
    Enables spatial 3D/2.5D scenes, hardware topologies, and dynamic camera travel
    using deterministic 'hf-seek' hooks without Blender.
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
        return RenderingEngine.THREEJS

    def is_available(self) -> bool:
        """Verifies that npx and HyperFrames are runnable to execute WebGL scenes."""
        if ThreeJsAdapter._class_cached_availability is not None:
            return ThreeJsAdapter._class_cached_availability

        has_npx = bool(shutil.which("npx") or shutil.which("npx.cmd"))
        ThreeJsAdapter._class_cached_availability = has_npx
        return ThreeJsAdapter._class_cached_availability

    def get_version(self) -> str:
        """Returns the version description."""
        if self._cached_version:
            return self._cached_version
        try:
            npx_bin = "npx.cmd" if os.name == "nt" else "npx"
            res = subprocess.run([npx_bin, "hyperframes", "--version"], capture_output=True, text=True, timeout=10)
            hf_ver = res.stdout.strip() if res.returncode == 0 else "unknown"
            self._cached_version = f"Three.js r128 (via HyperFrames {hf_ver} / Chrome ANGLE WebGL)"
            return self._cached_version
        except Exception:
            return "Three.js r128 (via HyperFrames / Chrome ANGLE WebGL)"

    def validate_scene(self, scene: UniversalSceneContract) -> bool:
        """Validates scene contract compatibility with Three.js rendering."""
        if not self.is_available():
            raise EngineUnavailableError("HyperFrames CLI / Chrome ANGLE WebGL is not available for Three.js rendering.")

        w, h = scene.output_resolution
        if w <= 0 or h <= 0:
            raise AdapterPreflightError(f"Invalid resolution for scene {scene.scene_id}: {scene.output_resolution}")

        duration = scene.actual_duration_seconds or scene.narration_duration_seconds or 0.0
        if duration <= 0.0:
            raise AdapterPreflightError(f"Invalid duration for scene {scene.scene_id}: {duration}s")

        return True

    def prepare(self, scene: UniversalSceneContract, context: ExecutionContext) -> Dict[str, Any]:
        """
        Generates a deterministic HTML composition containing Three.js r128 procedural rendering logic.
        """
        self.validate_scene(scene)

        w, h = scene.output_resolution
        fps = int(scene.frame_rate)
        duration = float(scene.actual_duration_seconds or scene.narration_duration_seconds or 5.0)

        comp_filename = f"gen_threejs_{scene.scene_id}_{context.timestamp}.html"
        comp_file = self.compositions_dir / comp_filename

        headline = (scene.narrative_purpose or scene.visual_concept or "NEURAL COMPUTE TOPOLOGY").upper()
        subhead = (scene.audience_takeaway or scene.mechanism_description or "Procedural 3D Accelerator Node Lattice")
        headline_clean = headline[:40].replace('"', '&quot;')
        subhead_clean = subhead[:60].replace('"', '&quot;')

        config_dict = scene.engine_specific_config or {}
        custom_js = config_dict.get("threejs_code") or ""

        # Procedural 3D scene template with deterministic hf-seek event protocol
        html_content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={w}, height={h}" />
    <title>Three.js Procedural Scene — {scene.scene_id}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: {w}px;
        height: {h}px;
        overflow: hidden;
        background: #07090e;
      }}
      #root {{
        width: {w}px;
        height: {h}px;
        position: relative;
        background: radial-gradient(circle at 50% 45%, #0f172a 0%, #07090e 100%);
      }}
      #three-canvas {{
        width: {w}px;
        height: {h}px;
        display: block;
      }}
      .hud-header {{
        position: absolute;
        top: 220px;
        left: 60px;
        right: 60px;
        text-align: center;
        pointer-events: none;
      }}
      .hud-title {{
        color: #00e5ff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 0 0 25px rgba(0, 229, 255, 0.4);
      }}
      .hud-sub {{
        color: #94a3b8;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 22px;
        font-weight: 500;
        margin-top: 10px;
      }}
      .hud-footer {{
        position: absolute;
        bottom: 240px;
        left: 60px;
        right: 60px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 14px;
        pointer-events: none;
      }}
      .hud-metric {{
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid #38bdf8;
        color: #38bdf8;
        padding: 12px 30px;
        border-radius: 24px;
        font-size: 24px;
        font-family: "Courier New", Courier, monospace;
        font-weight: 700;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
      }}
      .hud-provenance {{
        color: #64748b;
        font-size: 16px;
        font-family: monospace;
        letter-spacing: 1px;
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
      <canvas id="three-canvas" width="{w}" height="{h}"></canvas>
      <div class="hud-header">
        <div class="hud-title">{headline_clean}</div>
        <div class="hud-sub">{subhead_clean}</div>
      </div>
      <div class="hud-footer">
        <div class="hud-metric">LATENCY: 1.42 ms · THROUGHPUT: 18.4 TFLOPS</div>
        <div class="hud-provenance">ENGINE: THREE.JS (WEBGL) · ZERO BLENDER DEPENDENCY</div>
      </div>
    </div>

    <script>
      const canvas = document.getElementById("three-canvas");
      const renderer = new THREE.WebGLRenderer({{
        canvas,
        alpha: true,
        antialias: true,
        powerPreference: "high-performance"
      }});
      renderer.setSize({w}, {h});
      renderer.setPixelRatio(1);

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, {w} / {h}, 0.1, 100);

      // Lighting
      const ambientLight = new THREE.AmbientLight(0x0f172a, 1.5);
      scene.add(ambientLight);

      const keyLight = new THREE.PointLight(0x00e5ff, 3.5, 30);
      keyLight.position.set(5, 6, 8);
      scene.add(keyLight);

      const fillLight = new THREE.PointLight(0x8b5cf6, 3.0, 30);
      fillLight.position.set(-6, -4, 6);
      scene.add(fillLight);

      const rimLight = new THREE.DirectionalLight(0xf59e0b, 1.5);
      rimLight.position.set(0, -8, -5);
      scene.add(rimLight);

      // Central Computing Core (Icosahedron + Wireframe)
      const coreGroup = new THREE.Group();
      scene.add(coreGroup);

      const geoInner = new THREE.IcosahedronGeometry(1.6, 1);
      const matInner = new THREE.MeshPhongMaterial({{
        color: 0x1e1b4b,
        emissive: 0x0f172a,
        specular: 0x8b5cf6,
        shininess: 90,
        flatShading: true,
        transparent: true,
        opacity: 0.85
      }});
      const meshInner = new THREE.Mesh(geoInner, matInner);
      coreGroup.add(meshInner);

      const geoWire = new THREE.IcosahedronGeometry(1.65, 1);
      const matWire = new THREE.MeshBasicMaterial({{
        color: 0x00e5ff,
        wireframe: true,
        transparent: true,
        opacity: 0.6
      }});
      const meshWire = new THREE.Mesh(geoWire, matWire);
      coreGroup.add(meshWire);

      // Orbiting Hardware Token Nodes
      const orbitNodes = [];
      const nodeGeo = new THREE.BoxGeometry(0.28, 0.28, 0.28);
      const nodeMat = new THREE.MeshPhongMaterial({{
        color: 0x38bdf8,
        emissive: 0x0284c7,
        specular: 0xffffff,
        shininess: 100
      }});

      const NUM_NODES = 8;
      for (let i = 0; i < NUM_NODES; i++) {{
        const mesh = new THREE.Mesh(nodeGeo, nodeMat);
        const angleOffset = (i / NUM_NODES) * Math.PI * 2;
        const radius = 2.8 + 0.3 * Math.sin(i * 2);
        orbitNodes.push({{ mesh, angleOffset, radius, speed: 1.2 + (i % 3) * 0.4 }});
        scene.add(mesh);
      }}

      // Connecting Synaptic Lines
      const lineMat = new THREE.LineBasicMaterial({{ color: 0x6366f1, transparent: true, opacity: 0.4 }});
      const lineGeos = [];
      for (let i = 0; i < NUM_NODES; i++) {{
        const lineGeo = new THREE.BufferGeometry().setFromPoints([
          new THREE.Vector3(0, 0, 0),
          new THREE.Vector3(1, 1, 1)
        ]);
        const lineMesh = new THREE.Line(lineGeo, lineMat);
        lineGeos.push(lineGeo);
        scene.add(lineMesh);
      }}

      {custom_js}

      // Deterministic renderAt function (t in seconds, 0.0 to {duration:.2f})
      function renderAt(t) {{
        const progress = Math.min(Math.max(t / {duration:.2f}, 0), 1);
        const camZ = 7.5 - progress * 2.2;
        const camY = Math.sin(t * 0.7) * 0.8;
        const camX = Math.cos(t * 0.5) * 1.2;
        camera.position.set(camX, camY, camZ);
        camera.lookAt(0, 0, 0);

        coreGroup.rotation.y = t * 0.9;
        coreGroup.rotation.x = t * 0.45;
        coreGroup.rotation.z = Math.sin(t * 0.6) * 0.2;

        const pulse = 1.0 + Math.sin(t * 4.0) * 0.05;
        meshWire.scale.set(pulse, pulse, pulse);

        for (let i = 0; i < NUM_NODES; i++) {{
          const item = orbitNodes[i];
          const theta = item.angleOffset + t * item.speed;
          const nx = Math.cos(theta) * item.radius;
          const ny = Math.sin(theta * 0.8) * (item.radius * 0.45);
          const nz = Math.sin(theta) * item.radius;
          item.mesh.position.set(nx, ny, nz);
          item.mesh.rotation.x = t * 2;
          item.mesh.rotation.y = t * 3;

          const positions = lineGeos[i].attributes.position.array;
          positions[3] = nx;
          positions[4] = ny;
          positions[5] = nz;
          lineGeos[i].attributes.position.needsUpdate = true;
        }}

        renderer.render(scene, camera);
      }}

      // Deterministic time hooks for HyperFrames render loop
      window.addEventListener("hf-seek", function (e) {{
        if (e && e.detail && typeof e.detail.time === "number") {{
          renderAt(e.detail.time);
        }}
      }});

      document.addEventListener("seek", function (e) {{
        if (e && e.detail && typeof e.detail.time === "number") {{
          renderAt(e.detail.time);
        }}
      }});

      renderAt(0);

      // Fallback loop enabling HyperFrames virtual time detection
      let startTime = null;
      function loop(timestamp) {{
        if (!startTime) startTime = timestamp;
        const t = ((timestamp - startTime) / 1000) % Math.max(1, {duration:.2f});
        renderAt(t);
        requestAnimationFrame(loop);
      }}
      requestAnimationFrame(loop);
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
        Renders the Three.js scene via HyperFrames headless Chrome ANGLE Direct3D11.
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
        logger.info(f"Launching Three.js WebGL render for scene '{scene.scene_id}' via HyperFrames (timeout: {timeout:.1f}s)...")
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
            raise RenderExecutionError(f"Three.js render process failed: {e}", log_path=str(context.log_file))
        finally:
            # Clean up generated composition file to keep renderer/compositions tidy
            if comp_file.exists():
                try:
                    comp_file.unlink()
                except Exception:
                    pass

        if not result["success"]:
            raise RenderExecutionError(
                f"Three.js render exited with code {result['returncode']}",
                exit_code=result["returncode"],
                log_path=result.get("log_path", ""),
            )

        if not target_output.exists() or target_output.stat().st_size == 0:
            raise ArtifactValidationError(f"Three.js render completed but output missing or empty: {target_output}")

        render_time = time.time() - start_time
        logger.info(
            f"Three.js successfully rendered '{scene.scene_id}' to {target_output} "
            f"in {render_time:.2f}s (Peak RAM: {result.get('peak_ram_mb', 0.0)} MB)"
        )

        return self.verify_output(
            output_path=target_output,
            scene=scene,
            render_time_seconds=render_time,
            peak_ram_mb=result.get("peak_ram_mb", 0.0),
        )
