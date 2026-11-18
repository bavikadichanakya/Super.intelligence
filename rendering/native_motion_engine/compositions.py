"""
SUPER.INTELLIGENCEEE — Phase 4.3.3.2 Cinematic Explainer Visual Storytelling Engine
Authoritative Composition Families for High-Fidelity Technical Explainer Documentaries.
Provides:
1. FullScreenArchitectureComposition (Family 1: Full-Screen Architectural Visualization)
2. CloseUpMechanismComposition (Family 2: Close-Up Technical Mechanism / Idle Accelerator Hook)
3. ProcessEntityTrackingComposition (Family 3: Process Visualization with Moving Command Entity)
4. ExplodedHardwareStackComposition (Family 4: Exploded-View System Architecture Stack)
5. CinematicEvidenceVerdictComposition (Family 5: Hero Speedup 1.68x-2.05x, Race Bars, Synthesis)
6. GenericMotionComposition (Light-first kinetic fallback for generalized tech topics)
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw

from core.universal_scene_contract import UniversalSceneContract
from rendering.native_motion_engine.camera import CinematicCamera
from rendering.native_motion_engine.cinematic_components import (
    AppleSiliconHardwareHero,
    CinematicBenchmarkRace,
    CodingAgentRolloutVisual,
    HeroEditorialHeader,
    ProcessConfinementLaserBoundary,
)
from rendering.native_motion_engine.components import (
    LightEditorialBackground,
    get_scene_protected_regions,
)
from rendering.native_motion_engine.palette import (
    ACCENT_AMBER,
    ACCENT_EMERALD,
    ACCENT_INDIGO_SILICON,
    ACCENT_TECH_BLUE,
    BG_SURFACE_CARD,
    BG_SURFACE_SUBTLE,
    BORDER_LIGHT,
    BORDER_STRONG,
    TEXT_INVERSE_WHITE,
    TEXT_MUTED,
    TEXT_OBSIDIAN,
    TEXT_SLATE,
)
from rendering.native_motion_engine.primitives import (
    fade_in,
    fade_out,
    get_progress,
    scale_in,
)
from rendering.native_motion_engine.typography import (
    SafeZone,
    TextAlignment,
    TypographyEngine,
)
from rendering.subtitle_layout import BoundingBox


# =============================================================================
# BASE CINEMATIC COMPOSITION
# =============================================================================
class BaseMotionComposition:
    """Base class for all procedural cinematic motion compositions with virtual camera support."""

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        self.scene = scene
        self.width = width
        self.height = height
        self.safe_zone = SafeZone(top=180, bottom=260, left=60, right=60, canvas_width=width, canvas_height=height)
        self.typo = TypographyEngine(safe_zone=self.safe_zone)
        self.bg = LightEditorialBackground(width=width, height=height)
        self.camera = CinematicCamera(viewport_width=width, viewport_height=height)

    def _draw_gradient_background(self, img: Image.Image, t: float = 0.0):
        """Draws the warm ivory to soft white editorial background with subtle micro-grid."""
        self.bg.render(img, t)

    @property
    def protected_regions(self) -> List[BoundingBox]:
        """Returns the list of bounding boxes reserved for visual elements."""
        return []

    def render_frame(self, t: float) -> Image.Image:
        """Renders and returns a single frame at timestamp t."""
        raise NotImplementedError


# =============================================================================
# FAMILY 1: FULL-SCREEN ARCHITECTURAL VISUALIZATION
# =============================================================================
class FullScreenArchitectureComposition(BaseMotionComposition):
    """
    Family 1: Full-Screen Architectural Visualization.
    Spans the entire vertical canvas showing interconnected hardware cluster nodes,
    conduits, and distributed scheduling pipelines.
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.header = HeroEditorialHeader(typo=self.typo)
        self.rollout = CodingAgentRolloutVisual(typo=self.typo)

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=110, x1=1020, y1=240, label="hero_header"),
            BoundingBox(x0=60, y0=270, x1=1020, y1=580, label="agent_session_rollout"),
            BoundingBox(x0=60, y0=680, x1=1020, y1=1380, label="apple_m4_hardware_hero"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        # 1. Warm ivory background
        self._draw_gradient_background(img, t)

        # 2. Camera: Subtle push-in on agent, then pull-out to reveal hardware bottleneck
        if t < 3.0:
            self.camera.push_in_transition(t, 0.0, 3.0, from_zoom=1.0, to_zoom=1.06, target=(540, 420))
        else:
            self.camera.pull_out_transition(t, 3.0, 5.0, from_zoom=1.06, to_zoom=1.0, target=(540, 1000))

        # 3. Compact Hero Editorial Header
        self.header.render(
            draw=draw,
            t=t,
            category="HARDWARE ACCELERATOR BOTTLENECK",
            title="THE ROLLOUT UTILIZATION PROBLEM",
            subhead="Autonomous AI Coding Agents · Apple Silicon M4 Testbed · arXiv:2611.17294v1",
            top_y=110,
        )

        # 4. Agent Rollout Visual & Apple Silicon M4 Hero
        self.rollout.render(draw, t, camera=self.camera)

        return img


# =============================================================================
# FAMILY 2: CLOSE-UP TECHNICAL MECHANISM
# =============================================================================
class CloseUpMechanismComposition(BaseMotionComposition):
    """
    Family 2: Close-Up Technical Mechanism.
    Camera pushes tightly into the Apple M4 Silicon die and execution slots,
    revealing the single-tenant serial bottleneck.
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.header = HeroEditorialHeader(typo=self.typo)
        self.rollout = CodingAgentRolloutVisual(typo=self.typo)

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=110, x1=1020, y1=240, label="hero_header"),
            BoundingBox(x0=60, y0=270, x1=1020, y1=580, label="agent_session_rollout"),
            BoundingBox(x0=60, y0=680, x1=1020, y1=1380, label="apple_m4_hardware_hero"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(img, t)

        # Camera dynamic zoom
        self.camera.push_in_transition(t, 0.0, 4.0, from_zoom=1.0, to_zoom=1.08, target=(540, 950))

        self.header.render(
            draw=draw,
            t=t,
            category="COMPUTE ARCHITECTURE",
            title="ON-DEVICE ACCELERATOR BOTTLENECK",
            subhead="Single-Tenant Serial Pauses Leave GPU Cores Idle · arXiv:2611.17294v1",
            top_y=110,
        )

        self.rollout.render(draw, t, camera=self.camera)

        return img


# =============================================================================
# FAMILY 3: PROCESS VISUALIZATION WITH MOVING ENTITY
# =============================================================================
class ProcessEntityTrackingComposition(BaseMotionComposition):
    """
    Family 3: Process Visualization with Moving Entities.
    Follows a recognizable Command Entity through:
    1. Agent Session Ingress
    2. Filesystem & Process Confinement Boundary
    3. Central Hardware Queue Scheduling & Harbor Task Migration
    4. Execution Return
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.header = HeroEditorialHeader(typo=self.typo)
        self.mechanism = ProcessConfinementLaserBoundary(typo=self.typo)

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=110, x1=1020, y1=240, label="hero_header"),
            BoundingBox(x0=60, y0=260, x1=1020, y1=420, label="agent_session_ingress"),
            BoundingBox(x0=60, y0=445, x1=1020, y1=810, label="confinement_boundary"),
            BoundingBox(x0=60, y0=835, x1=1020, y1=1180, label="hardware_queue_scheduling"),
            BoundingBox(x0=60, y0=1205, x1=1020, y1=1380, label="architectural_property"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(img, t)

        self.header.render(
            draw=draw,
            t=t,
            category="EXECUTION SECURITY & SCHEDULING",
            title="COMMAND ISOLATION & QUEUE ARBITRATION",
            subhead="Restricted Filesystem Confinement · Harbor Task Migration · arXiv:2611.17294v1",
            top_y=110,
        )

        self.mechanism.render(draw, t, camera=self.camera)

        return img


# =============================================================================
# FAMILY 4: EXPLODED-VIEW HARDWARE / SYSTEM DIAGRAM
# =============================================================================
class ExplodedHardwareStackComposition(BaseMotionComposition):
    """
    Family 4: Exploded-View System Architecture Stack.
    Separates the execution layers into elevated tiers:
    Tier 1 (Top): Concurrent Agent Sessions
    Tier 2 (Mid): Per-Instance Filesystem Sandboxes
    Tier 3 (Bridge): Queue Scheduler & Harbor Migration
    Tier 4 (Bottom): Shared Apple Silicon Metal Hardware
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.header = HeroEditorialHeader(typo=self.typo)

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=110, x1=1020, y1=240, label="hero_header"),
            BoundingBox(x0=60, y0=270, x1=1020, y1=1380, label="exploded_stack"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(img, t)

        self.header.render(
            draw=draw,
            t=t,
            category="SYSTEM ARCHITECTURE",
            title="EXPLODED EXECUTION STACK",
            subhead="Hierarchical Separation of Workspace Confinement and Hardware Acceleration",
            top_y=110,
        )

        # 4 Elevated Tiers spanning y = 280 to 1380
        tiers = [
            ("TIER 1: CONCURRENT AGENT SESSIONS", "Multi-tenant coding agents in exploratory rollout loops", ACCENT_TECH_BLUE, 280, 500),
            ("TIER 2: PER-INSTANCE FILESYSTEM SANDBOX", "Restricted workspace chroot · blocked host /System access", ACCENT_EMERALD, 530, 750),
            ("TIER 3: CENTRAL COMMAND QUEUE SCHEDULER", "Hardware queue arbitration & Harbor cross-node migration", ACCENT_INDIGO_SILICON, 780, 1000),
            ("TIER 4: APPLE SILICON METAL ACCELERATOR", "4× Mac mini M4 nodes · 10-core GPU · 16GB Unified Memory", ACCENT_OBSIDIAN if hasattr(self, 'ACCENT_OBSIDIAN') else TEXT_OBSIDIAN, 1030, 1340),
        ]

        for idx, (t_title, t_desc, t_col, y0, y1) in enumerate(tiers):
            t_scale = scale_in(t, 0.2 + idx * 0.35, 0.45)
            if t_scale > 0.01:
                draw.rounded_rectangle([66, y0 + 6, 1026, y1 + 6], radius=16, fill=(210, 218, 230, 110))
                draw.rounded_rectangle([60, y0, 1020, y1], radius=16, fill=BG_SURFACE_CARD, outline=t_col, width=3)
                draw.text((84, y0 + 20), t_title, font=self.typo.get_font(size=18, bold=True, mono=True), fill=TEXT_OBSIDIAN)
                draw.text((84, y0 + 52), t_desc, font=self.typo.get_font(size=15), fill=TEXT_SLATE)

        return img


# =============================================================================
# FAMILY 5: CINEMATIC EVIDENCE VERDICT & BENCHMARK RACE
# =============================================================================
class CinematicEvidenceVerdictComposition(BaseMotionComposition):
    """
    Family 5: Minimal Editorial Conclusion with Strong Typography & Dynamic Infographics.
    Features:
    - Giant Hero Typography (1.68x - 2.05x Command Throughput Gain)
    - Full-Width Dual Timeline Race Visualizer (-22.3% Elapsed Time, -18.8% Latency)
    - Distinct Empirical Measured vs Model Estimated badges
    - Minimal Editorial Synthesis Verdict
    """

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.header = HeroEditorialHeader(typo=self.typo)
        self.race = CinematicBenchmarkRace(typo=self.typo)

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=110, x1=1020, y1=240, label="hero_header"),
            BoundingBox(x0=60, y0=260, x1=1020, y1=520, label="hero_speedup_gauge"),
            BoundingBox(x0=60, y0=545, x1=1020, y1=900, label="dual_timeline_race"),
            BoundingBox(x0=60, y0=925, x1=1020, y1=1180, label="methodological_classification"),
            BoundingBox(x0=60, y0=1205, x1=1020, y1=1380, label="architectural_synthesis"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(img, t)

        self.header.render(
            draw=draw,
            t=t,
            category="EMPIRICAL BENCHMARK",
            title="VERIFIED PERFORMANCE & HARDWARE AUDIT",
            subhead="Controlled Experiments on 4× Apple Mac mini M4 · arXiv:2611.17294v1",
            top_y=110,
        )

        self.race.render(draw, t, camera=self.camera)

        return img


# =============================================================================
# BACKWARD-COMPATIBILITY ALIASES & GENERIC MOTION
# =============================================================================
# Alias existing composition names so renderer and legacy tests resolve smoothly
SystemTopologyComposition = FullScreenArchitectureComposition
SandboxIsolationComposition = ProcessEntityTrackingComposition
EditorialVerdictComposition = CinematicEvidenceVerdictComposition


class GenericMotionComposition(BaseMotionComposition):
    """General fallback composition for generic documentary topics."""

    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.header = HeroEditorialHeader(typo=self.typo)

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=110, x1=1020, y1=240, label="hero_header"),
            BoundingBox(x0=60, y0=280, x1=1020, y1=1380, label="generic_content_body"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        self._draw_gradient_background(img, t)

        self.header.render(
            draw=draw,
            t=t,
            category="TECHNICAL EXPLAINER",
            title=self.scene.narrative_purpose or "TECHNICAL ANALYSIS",
            subhead="SUPER.INTELLIGENCEEE Autonomous Documentary Production",
            top_y=110,
        )

        draw.rounded_rectangle([66, 286, 1026, 1386], radius=20, fill=(210, 218, 230, 110))
        draw.rounded_rectangle([60, 280, 1020, 1380], radius=20, fill=BG_SURFACE_CARD, outline=BORDER_STRONG, width=2)

        self.typo.draw_text_block(
            draw=draw,
            text=self.scene.visual_concept or self.scene.mechanism_description or "Visual explanation",
            box=(100, 340, 880, 400),
            fill=TEXT_OBSIDIAN,
            preferred_size=32,
            min_size=20,
            bold=True,
        )

        return img
