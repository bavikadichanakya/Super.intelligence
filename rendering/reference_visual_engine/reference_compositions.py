"""
SUPER.INTELLIGENCEEE — Phase 5 Reference Composition Templates
Authoritative, reference-style composition families extracted from 'This is what i want.mp4':
1. ReferenceIsometricHookComposition (Dark Theme, 3D Voxel Cube, RAM DIMM, Kinetic Typography)
2. ReferenceBarChartComparisonComposition (Light Theme, 3D Column Chart, Highlighted Pillar)
3. ReferenceRepoEvidenceComposition (Light Theme, GitHub Repo Card, Lollipop Chart with Focus Box)
4. ReferenceMoEMechanismComposition (Light Theme, 896-Expert Grid, 16 Active Red Nodes, M.2 SSD)
5. ReferenceLayerStreamingComposition (Light Theme, 93-Layer Slab Stack, Flatline RAM Telemetry)
6. ReferenceDeterminismComparisonComposition (Light Theme, Side-by-Side Laptop vs Workstation Cards)
7. ReferenceLatencyTimerComposition (Light Theme, Giant Digital Timer, Prompt Card, Progress Steps)
8. ReferenceLoopConclusionComposition (Dark Theme, 3D Cube over Laptop, Seamless Loop Transition)
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from core.universal_scene_contract import UniversalSceneContract
from rendering.native_motion_engine.camera import CinematicCamera
from rendering.native_motion_engine.compositions import BaseMotionComposition
from rendering.reference_visual_engine.charts_and_telemetry import (
    DigitalStopwatchTimer,
    FlatlineTelemetryCard,
    LollipopChart,
    MoEExpertGrid,
)
from rendering.reference_visual_engine.evidence_cards import (
    DocumentationFigureViewer,
    GitHubRepoCard,
    SideBySideComparisonCard,
)
from rendering.reference_visual_engine.isometric_3d import (
    IsometricBarChart,
    IsometricHardwareModels,
    IsometricLayerStack,
    IsometricVoxelCube,
)
from rendering.reference_visual_engine.kinetic_typography import (
    KineticWord,
    ReferenceKineticTypography,
)
from rendering.subtitle_layout import BoundingBox


# =============================================================================
# 1. REFERENCE ISOMETRIC HOOK (Dark Theme, 3D Cube, RAM DIMM)
# =============================================================================
class ReferenceIsometricHookComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.cube = IsometricVoxelCube()
        self.hardware = IsometricHardwareModels()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=80, x1=1020, y1=320, label="kinetic_headline"),
            BoundingBox(x0=120, y0=380, x1=960, y1=880, label="isometric_3d_cube"),
            BoundingBox(x0=60, y0=940, x1=1020, y1=1380, label="ram_stick_hardware"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (10, 13, 20, 255))
        draw = ImageDraw.Draw(img)

        # 1. Subtle dark grid background
        grid_step = 40
        for gx in range(0, self.width, grid_step):
            draw.line([(gx, 0), (gx, self.height)], fill=(20, 30, 45, 120), width=1)
        for gy in range(0, self.height, grid_step):
            draw.line([(0, gy), (self.width, gy)], fill=(20, 30, 45, 120), width=1)

        # 2. Central blue radial glow
        draw.ellipse([240, 400, 840, 1000], fill=(2, 132, 199, 35))

        # 3. Kinetic Headline: "Now you can run a 2.78T parameters on just [8 gigs]"
        words = [
            KineticWord("Now you can", is_bold=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=540, top_y=95, t=t, is_dark_theme=True)
        self.kinetics.render_hero_stat(draw, "2.78", "T", "parameters", center_x=540, center_y=160, t=t, is_dark_theme=True)

        if t > 2.0:
            words2 = [
                KineticWord("on just", is_bold=True),
                KineticWord("8 gigs", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words2, center_x=540, top_y=280, t=t - 2.0, is_dark_theme=True)

        # 4. Floating 3D Isometric Voxel Cube
        self.cube.render(draw, t=t, center=(540, 680), size=190.0, is_dark_theme=True)

        # 5. RAM DIMM hardware stick
        if t > 2.5:
            self.hardware.render_ram_stick(draw, center=(540, 1140), label="8 GB RAM")

        return img


# =============================================================================
# 2. REFERENCE BAR CHART COMPARISON (Light Theme, 3D Columns)
# =============================================================================
class ReferenceBarChartComparisonComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.barchart = IsometricBarChart()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=80, x1=1020, y1=240, label="kinetic_headline"),
            BoundingBox(x0=60, y0=280, x1=1020, y1=1380, label="isometric_bar_chart"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        # Warm light background: #E5E5E0
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # Kinetic Headline: "one of the biggest open models out there,"
        words = [
            KineticWord("one of the", is_bold=True),
            KineticWord("biggest", is_serif_italic=True),
            KineticWord("open", is_bold=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=540, top_y=100, t=t, is_dark_theme=False)

        words2 = [
            KineticWord("models out there,", is_bold=True),
        ]
        self.kinetics.render_headline(draw, words2, center_x=540, top_y=160, t=t, is_dark_theme=False)

        # 3D Isometric Comparative Bar Chart
        self.barchart.render(draw, t=t, center=(540, 780))

        return img


# =============================================================================
# 3. REFERENCE REPO EVIDENCE (Light Theme, GitHub Card & Lollipop Chart)
# =============================================================================
class ReferenceRepoEvidenceComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.repo_card = GitHubRepoCard()
        self.chart = LollipopChart()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=80, x1=1020, y1=240, label="kinetic_headline"),
            BoundingBox(x0=60, y0=260, x1=1020, y1=1380, label="repo_evidence_visual"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        if t < 4.5:
            # First sub-beat: Authentic GitHub Repo Card
            words = [
                KineticWord("But this", is_bold=True),
                KineticWord("repo", is_serif_italic=True),
                KineticWord("runs it", is_bold=True),
            ]
            self.kinetics.render_headline(draw, words, center_x=540, top_y=110, t=t, is_dark_theme=False)
            self.repo_card.render(draw, top_y=320, t=t)
        else:
            # Second sub-beat: Lollipop comparison chart
            words = [
                KineticWord("and the whole engine is", is_bold=True),
                KineticWord("176 KB", is_bold=True, is_highlight_box=True),
            ]
            self.kinetics.render_headline(draw, words, center_x=540, top_y=110, t=t - 4.5, is_dark_theme=False)
            self.chart.render(draw, t=t - 4.5, center_y=780)

        return img


# =============================================================================
# 4. REFERENCE MOE MECHANISM (Light Theme, 896 Grid, 16 Awake, M.2 SSD)
# =============================================================================
class ReferenceMoEMechanismComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.grid = MoEExpertGrid()
        self.hardware = IsometricHardwareModels()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=80, x1=1020, y1=240, label="kinetic_headline"),
            BoundingBox(x0=60, y0=260, x1=1020, y1=1380, label="moe_expert_mechanism"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # Kinetic Headline: "only 16 wake up off your drive"
        if t < 3.5:
            words = [
                KineticWord("that Kimi's", is_bold=True),
                KineticWord("split", is_bold=True),
                KineticWord("into 896", is_bold=True),
            ]
            self.kinetics.render_headline(draw, words, center_x=540, top_y=100, t=t, is_dark_theme=False)
        else:
            words = [
                KineticWord("only", is_bold=True),
                KineticWord("16", is_bold=True, is_highlight_box=True),
                KineticWord("wake up off your", is_bold=True),
                KineticWord("drive", is_serif_italic=True),
            ]
            self.kinetics.render_headline(draw, words, center_x=540, top_y=100, t=t - 3.5, is_dark_theme=False)

        # 896-Expert dense grid
        self.grid.render(draw, t=t, center_y=680)

        # Isometric M.2 NVMe SSD at bottom
        self.hardware.render_m2_ssd(draw, center=(540, 1180), t=t)

        return img


# =============================================================================
# 5. REFERENCE LAYER STREAMING (Light Theme, 93 Layers, Flatline RAM)
# =============================================================================
class ReferenceLayerStreamingComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.stack = IsometricLayerStack()
        self.telemetry = FlatlineTelemetryCard()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=80, x1=1020, y1=240, label="kinetic_headline"),
            BoundingBox(x0=60, y0=260, x1=1020, y1=1380, label="layer_streaming_visual"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        # Kinetic Headline: "streams in layer by layer around [8 gigs]"
        words = [
            KineticWord("streams in", is_bold=True),
            KineticWord("layer by layer,", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=540, top_y=90, t=t, is_dark_theme=False)

        words2 = [
            KineticWord("so your RAM stays around", is_bold=True),
            KineticWord("8 gigs", is_bold=True, is_highlight_box=True),
        ]
        self.kinetics.render_headline(draw, words2, center_x=540, top_y=150, t=t, is_dark_theme=False)

        # 93-Layer Isometric Stack
        self.stack.render(draw, t=t, center=(320, 680))

        # Single Active Resident Layer Card (Right)
        rc_x0, rc_y0 = 600, 480
        draw.rounded_rectangle([rc_x0, rc_y0, rc_x0 + 360, rc_y0 + 260], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((rc_x0 + 24, rc_y0 + 20), "🗲 RAM (Resident Buffer)", font=ImageFont.truetype("arialbd.ttf", 18), fill=(15, 23, 42))
        draw.text((rc_x0 + 24, rc_y0 + 54), "1 Layer active in memory at a time", font=ImageFont.truetype("consola.ttf", 13), fill=(100, 116, 139))
        draw.text((rc_x0 + 24, rc_y0 + 210), "layer 83 / 93", font=ImageFont.truetype("consola.ttf", 14), fill=(185, 28, 28))

        # Bottom: Flatline RAM Telemetry Card
        self.telemetry.render(draw, t=t, center_y=1180)

        return img


# =============================================================================
# 6. REFERENCE DETERMINISM (Light Theme, Side-by-Side Cards)
# =============================================================================
class ReferenceDeterminismComparisonComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.comparison = SideBySideComparisonCard()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=80, x1=1020, y1=240, label="kinetic_headline"),
            BoundingBox(x0=60, y0=260, x1=1020, y1=1380, label="side_by_side_comparison"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        words = [
            KineticWord("on", is_bold=True),
            KineticWord("8 gigs", is_bold=True, is_highlight_box=True),
            KineticWord("or", is_bold=True),
            KineticWord("128,", is_bold=True, is_highlight_box=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=540, top_y=110, t=t, is_dark_theme=False)

        # Side-by-side laptop vs workstation cards
        self.comparison.render(draw, t=t, center_y=720)

        return img


# =============================================================================
# 7. REFERENCE LATENCY TIMER (Light Theme, Stopwatch, Progress Blocks)
# =============================================================================
class ReferenceLatencyTimerComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.timer = DigitalStopwatchTimer()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=80, x1=1020, y1=240, label="kinetic_headline"),
            BoundingBox(x0=60, y0=260, x1=1020, y1=1380, label="latency_stopwatch_timer"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (229, 229, 224, 255))
        draw = ImageDraw.Draw(img)

        words = [
            KineticWord("took over", is_bold=True),
            KineticWord("four", is_bold=True, is_highlight_box=True),
            KineticWord("minutes,", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=540, top_y=110, t=t, is_dark_theme=False)

        # Compute dynamic timer string based on t
        sec = int(t * 12)
        mins = sec // 60
        secs = sec % 60
        disp = f"{mins}:{secs:02d}"

        self.timer.render(
            draw,
            t=t,
            center_y=720,
            prompt_text="The capital of France is",
            time_display=disp,
        )

        return img


# =============================================================================
# 8. REFERENCE LOOP CONCLUSION (Dark Theme, Cube over Laptop, Seamless Loop)
# =============================================================================
class ReferenceLoopConclusionComposition(BaseMotionComposition):
    def __init__(self, scene: UniversalSceneContract, width: int = 1080, height: int = 1920):
        super().__init__(scene, width, height)
        self.kinetics = ReferenceKineticTypography(width, height)
        self.cube = IsometricVoxelCube()

    @property
    def protected_regions(self) -> List[BoundingBox]:
        return [
            BoundingBox(x0=60, y0=80, x1=1020, y1=240, label="kinetic_headline"),
            BoundingBox(x0=60, y0=260, x1=1020, y1=1380, label="loop_conclusion_visual"),
        ]

    def render_frame(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (10, 13, 20, 255))
        draw = ImageDraw.Draw(img)

        # Dark grid background
        grid_step = 40
        for gx in range(0, self.width, grid_step):
            draw.line([(gx, 0), (gx, self.height)], fill=(20, 30, 45, 120), width=1)
        for gy in range(0, self.height, grid_step):
            draw.line([(0, gy), (self.width, gy)], fill=(20, 30, 45, 120), width=1)

        # Kinetic Headline: "won't stop a model running on your machine"
        words = [
            KineticWord("won't", is_bold=True),
            KineticWord("stop", is_serif_italic=True),
        ]
        self.kinetics.render_headline(draw, words, center_x=540, top_y=95, t=t, is_dark_theme=True)

        words2 = [
            KineticWord("on", is_bold=True),
            KineticWord("your machine.", is_bold=True, is_highlight_box=True),
        ]
        self.kinetics.render_headline(draw, words2, center_x=540, top_y=155, t=t, is_dark_theme=True)

        # Floating 3D Voxel Cube hovering over laptop
        self.cube.render(draw, t=t, center=(540, 580), size=160.0, is_dark_theme=True)

        # Laptop outline illustration underneath
        lx0 = 220
        lx1 = 860
        ly0 = 780
        ly1 = 1200
        # Laptop screen
        draw.rounded_rectangle([lx0, ly0, lx1, ly1], radius=16, outline=(71, 85, 105), width=3)
        draw.rounded_rectangle([lx0 + 12, ly0 + 12, lx1 - 12, ly1 - 12], radius=8, fill=(15, 23, 42))
        # Laptop base
        draw.polygon([(lx0 - 40, ly1 + 30), (lx1 + 40, ly1 + 30), (lx1, ly1), (lx0, ly1)], fill=(30, 41, 59), outline=(71, 85, 105))

        return img
