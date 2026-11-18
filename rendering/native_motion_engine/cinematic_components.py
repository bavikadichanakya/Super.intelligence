"""
SUPER.INTELLIGENCEEE — Phase 4.3.3.2 Cinematic Explainer Visual Components
Provides high-impact, full-screen technical illustration components:
1. HeroEditorialHeader (Cinematic, compact header with large typography)
2. CodingAgentRolloutVisual (Autonomous agent session, rollout loop, idle accelerator reveal)
3. AppleSiliconHardwareHero (Full-scale Apple M4 unibody & silicon die, idle capacity warning)
4. ProcessConfinementLaserBoundary (Spatial filesystem & process confinement wall, not a card)
5. CommandQueuePipeline & TravelingCommandEntity (Animated moving command traveling through system)
6. CinematicBenchmarkRace (Full-width dual timeline race, 1.68x-2.05x hero typography, -22.3% & -18.8% deltas)
7. CinematicEditorialTakeaway (Minimalist publication-grade conclusion with high-contrast typography)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from rendering.native_motion_engine.camera import CinematicCamera
from rendering.native_motion_engine.palette import (
    ACCENT_AMBER,
    ACCENT_AMBER_LIGHT,
    ACCENT_EMERALD,
    ACCENT_EMERALD_LIGHT,
    ACCENT_INDIGO_SILICON,
    ACCENT_MUTED_RED,
    ACCENT_MUTED_RED_LIGHT,
    ACCENT_TECH_BLUE,
    ACCENT_TECH_BLUE_LIGHT,
    BG_LIGHT_NEUTRAL,
    BG_SOFT_WHITE,
    BG_SURFACE_CARD,
    BG_SURFACE_SUBTLE,
    BG_WARM_IVORY,
    BORDER_LIGHT,
    BORDER_STRONG,
    GRID_LINE,
    TEXT_INVERSE_WHITE,
    TEXT_MUTED,
    TEXT_OBSIDIAN,
    TEXT_SLATE,
)
from rendering.native_motion_engine.primitives import (
    counter_animation,
    ease_in_out_cubic,
    ease_out_back,
    ease_out_cubic,
    fade_in,
    fade_out,
    get_progress,
    scale_in,
    slide_in,
)
from rendering.native_motion_engine.typography import (
    SafeZone,
    TextAlignment,
    TypographyEngine,
)
from rendering.subtitle_layout import BoundingBox


# =============================================================================
# 1. HERO EDITORIAL HEADER (Compact, Cinematic, High-Contrast)
# =============================================================================
class HeroEditorialHeader:
    """Compact cinematic header occupying only y = 100 to 240, freeing vertical canvas for visuals."""

    def __init__(self, typo: TypographyEngine):
        self.typo = typo

    def render(
        self,
        draw: ImageDraw.ImageDraw,
        t: float,
        category: str,
        title: str,
        subhead: str,
        top_y: int = 110,
    ):
        opacity = fade_in(t, 0.05, 0.35)
        if opacity <= 0.01:
            return

        alpha_int = int(255 * opacity)

        # Category pill badge (Clean technical blue pill)
        pill_font = self.typo.get_font(size=18, bold=True, mono=True)
        pill_text = category.upper()
        pill_bbox = draw.textbbox((0, 0), pill_text, font=pill_font)
        pw = pill_bbox[2] - pill_bbox[0] + 24
        ph = 32
        px = 60
        py = top_y

        draw.rounded_rectangle(
            [px, py, px + pw, py + ph],
            radius=6,
            fill=(ACCENT_TECH_BLUE[0], ACCENT_TECH_BLUE[1], ACCENT_TECH_BLUE[2], alpha_int),
        )
        draw.text(
            (px + 12, py + 7),
            pill_text,
            font=pill_font,
            fill=(TEXT_INVERSE_WHITE[0], TEXT_INVERSE_WHITE[1], TEXT_INVERSE_WHITE[2], alpha_int),
        )

        # Primary Title (Large, bold obsidian typography)
        title_y = py + ph + 10
        title_font = self.typo.get_font(size=36, bold=True)
        draw.text(
            (px, title_y),
            title,
            font=title_font,
            fill=(TEXT_OBSIDIAN[0], TEXT_OBSIDIAN[1], TEXT_OBSIDIAN[2], alpha_int),
        )

        # Secondary subhead breadcrumb
        sub_y = title_y + 46
        sub_font = self.typo.get_font(size=19, mono=False)
        draw.text(
            (px, sub_y),
            subhead,
            font=sub_font,
            fill=(TEXT_SLATE[0], TEXT_SLATE[1], TEXT_SLATE[2], alpha_int),
        )

        # Subtle separating baseline rule
        rule_y = sub_y + 32
        draw.line(
            [(px, rule_y), (px + 960, rule_y)],
            fill=(BORDER_LIGHT[0], BORDER_LIGHT[1], BORDER_LIGHT[2], alpha_int),
            width=2,
        )


# =============================================================================
# 2. CODING AGENT ROLLOUT VISUAL & APPLE SILICON HARDWARE HERO
# =============================================================================
class AppleSiliconHardwareHero:
    """Full-scale Apple M4 unibody & silicon die representation with idle capacity visualizer."""

    def __init__(self, typo: TypographyEngine):
        self.typo = typo
        self._rollout = CodingAgentRolloutVisual(typo)

    def render(self, draw: ImageDraw.ImageDraw, t: float, camera: Optional[CinematicCamera] = None):
        self._rollout.render(draw, t, camera=camera)


class CodingAgentRolloutVisual:
    """
    Visualizes an autonomous coding agent operating in an exploratory rollout loop.
    Reveals the hardware problem: agent reasoning pauses leave GPU accelerators idle.
    """

    def __init__(self, typo: TypographyEngine):
        self.typo = typo

    def render(self, draw: ImageDraw.ImageDraw, t: float, camera: Optional[CinematicCamera] = None):
        # 1. Autonomous Agent Session Node (Top focal element: y = 280 to 580)
        agent_scale = scale_in(t, 0.1, 0.45)
        if agent_scale > 0.01:
            ax0, ay0 = 60, 270
            ax1, ay1 = 1020, 580

            # Subtle drop shadow
            draw.rounded_rectangle([ax0 + 6, ay0 + 8, ax1 + 6, ay1 + 8], radius=20, fill=(210, 218, 230, 110))
            draw.rounded_rectangle([ax0, ay0, ax1, ay1], radius=20, fill=BG_SURFACE_CARD, outline=BORDER_STRONG, width=2)

            # Agent Header Bar
            draw.rounded_rectangle([ax0, ay0, ax1, ay0 + 60], radius=18, fill=TEXT_OBSIDIAN)
            draw.rectangle([ax0, ay0 + 30, ax1, ay0 + 60], fill=TEXT_OBSIDIAN)

            # Agent Session Pulse Indicator
            pulse = 0.5 + 0.5 * math.sin(t * 4.0)
            led_radius = int(6 + 2 * pulse)
            draw.circle((ax0 + 36, ay0 + 30), radius=led_radius + 3, fill=(2, 132, 199, 120))
            draw.circle((ax0 + 36, ay0 + 30), radius=6, fill=ACCENT_TECH_BLUE)

            draw.text((ax0 + 58, ay0 + 18), "AGENT_SESSION // M4_CODING_ROLLOUT", font=self.typo.get_font(size=18, bold=True, mono=True), fill=TEXT_INVERSE_WHITE)

            # State badge
            is_waiting = t > 3.0
            st_text = "STATE: IDLE WAITING (TOOL RETURN)" if is_waiting else "STATE: GENERATING ROLLOUT CODE"
            st_bg = ACCENT_AMBER_LIGHT if is_waiting else ACCENT_EMERALD_LIGHT
            st_col = ACCENT_AMBER if is_waiting else ACCENT_EMERALD
            draw.rounded_rectangle([ax1 - 340, ay0 + 14, ax1 - 24, ay0 + 46], radius=6, fill=st_bg, outline=st_col, width=1)
            draw.text((ax1 - 325, ay0 + 22), st_text, font=self.typo.get_font(size=12, bold=True, mono=True), fill=st_col)

            # Simulated Terminal / Code generation stream
            tx0 = ax0 + 24
            ty0 = ay0 + 80
            draw.rounded_rectangle([tx0, ty0, ax1 - 24, ay1 - 24], radius=12, fill=BG_SURFACE_SUBTLE, outline=BORDER_LIGHT, width=1)

            # Terminal code text
            code_font = self.typo.get_font(size=16, mono=True)
            lines = [
                ("01", "def rollout_step(state, model):", TEXT_SLATE),
                ("02", "    # Agent generates candidate Metal kernel", TEXT_MUTED),
                ("03", "    kernel_code = model.generate(prompt=state.context)", TEXT_OBSIDIAN),
                ("04", "    result = hardware.dispatch(kernel_code)  # <--- DISPATCH CALL", ACCENT_TECH_BLUE),
                ("05", "    return evaluate_metrics(result)", TEXT_SLATE),
            ]
            for i, (ln, l_text, col) in enumerate(lines):
                ly = ty0 + 16 + i * 36
                draw.text((tx0 + 16, ly), ln, font=code_font, fill=TEXT_MUTED)
                draw.text((tx0 + 56, ly), l_text, font=code_font, fill=col)

            # Moving code cursor
            cur_p = get_progress(t, 0.4, 2.5, "linear")
            cur_x = tx0 + 56 + int(cur_p * 500) % 520
            cur_y = ty0 + 16 + (3 * 36)
            draw.rectangle([cur_x, cur_y, cur_x + 9, cur_y + 20], fill=ACCENT_TECH_BLUE)

        # 2. Downward Conduit with Traveling Command Pulse (y = 580 to 680)
        conduit_t = fade_in(t, 1.2, 0.4)
        if conduit_t > 0:
            c_alpha = int(255 * conduit_t)
            draw.line([(540, 580), (540, 680)], fill=(BORDER_STRONG[0], BORDER_STRONG[1], BORDER_STRONG[2], c_alpha), width=4)

            # Traveling command packet
            pkt_p = (t * 1.5) % 1.0
            pkt_y = 580 + int(pkt_p * 100)
            draw.circle((540, pkt_y), radius=10, fill=ACCENT_TECH_BLUE)
            draw.circle((540, pkt_y), radius=5, fill=TEXT_INVERSE_WHITE)

        # 3. Large Physical Apple Silicon M4 Hardware Representation (y = 680 to 1380)
        hw_scale = scale_in(t, 0.6, 0.5)
        if hw_scale > 0.01:
            hx0, hy0 = 60, 680
            hx1, hy1 = 1020, 1380

            draw.rounded_rectangle([hx0 + 6, hy0 + 8, hx1 + 6, hy1 + 8], radius=24, fill=(210, 218, 230, 110))
            draw.rounded_rectangle([hx0, hy0, hx1, hy1], radius=24, fill=BG_SURFACE_CARD, outline=BORDER_STRONG, width=3)

            # Hardware Header: Apple Silicon Testbed Node
            draw.text((hx0 + 30, hy0 + 24), "APPLE MAC MINI (M4, 2024) // DEDICATED HOST NODE", font=self.typo.get_font(size=22, bold=True, mono=True), fill=TEXT_OBSIDIAN)
            draw.text((hx0 + 30, hy0 + 54), "10-Core CPU (4P+6E) · 10-Core GPU · 16GB Unified Memory · 120 GB/s", font=self.typo.get_font(size=16, mono=True), fill=ACCENT_TECH_BLUE)

            # Large Apple M4 Silicon Die (y = 780 to 1040)
            die_x0 = hx0 + 30
            die_y0 = hy0 + 95
            die_w = 900
            die_h = 240
            draw.rounded_rectangle([die_x0, die_y0, die_x0 + die_w, die_y0 + die_h], radius=16, fill=BG_SURFACE_SUBTLE, outline=ACCENT_INDIGO_SILICON, width=3)

            # Die Label
            draw.text((die_x0 + 24, die_y0 + 16), "APPLE M4 UNIFIED SILICON DIE", font=self.typo.get_font(size=18, bold=True, mono=True), fill=ACCENT_INDIGO_SILICON)

            # Core partitions
            # 10-Core CPU cluster
            cpu_box = [die_x0 + 24, die_y0 + 50, die_x0 + 280, die_y0 + 215]
            draw.rounded_rectangle(cpu_box, radius=8, fill=BG_SURFACE_CARD, outline=BORDER_STRONG, width=1)
            draw.text((cpu_box[0] + 16, cpu_box[1] + 14), "10-CORE CPU CLUSTER", font=self.typo.get_font(size=14, bold=True, mono=True), fill=TEXT_OBSIDIAN)
            draw.text((cpu_box[0] + 16, cpu_box[1] + 40), "4 Performance Cores\n6 Efficiency Cores\nHost Agent Runtime", font=self.typo.get_font(size=13), fill=TEXT_SLATE)

            # 10-Core GPU cluster (Metal execution engine)
            gpu_box = [die_x0 + 305, die_y0 + 50, die_x0 + 610, die_y0 + 215]
            draw.rounded_rectangle(gpu_box, radius=8, fill=BG_SURFACE_CARD, outline=ACCENT_TECH_BLUE, width=2)
            draw.text((gpu_box[0] + 16, gpu_box[1] + 14), "10-CORE METAL GPU", font=self.typo.get_font(size=14, bold=True, mono=True), fill=ACCENT_TECH_BLUE)
            draw.text((gpu_box[0] + 16, gpu_box[1] + 40), "Hardware Raytracing\nParallel Compute Slots\nMetal Shading Engine", font=self.typo.get_font(size=13), fill=TEXT_SLATE)

            # 16GB Unified Memory Bus
            mem_box = [die_x0 + 635, die_y0 + 50, die_x0 + 876, die_y0 + 215]
            draw.rounded_rectangle(mem_box, radius=8, fill=BG_SURFACE_CARD, outline=BORDER_STRONG, width=1)
            draw.text((mem_box[0] + 16, mem_box[1] + 14), "UNIFIED MEMORY", font=self.typo.get_font(size=14, bold=True, mono=True), fill=TEXT_OBSIDIAN)
            draw.text((mem_box[0] + 16, mem_box[1] + 40), "16 GB Shared Pool\n120 GB/s Bandwidth\nZero-Copy Pipeline", font=self.typo.get_font(size=13), fill=TEXT_SLATE)

            # 4. The Utilization Bottleneck Visualizer (y = 1060 to 1340)
            bot_y = hy0 + 360
            draw.text((hx0 + 30, bot_y), "HARDWARE ACCELERATOR UTILIZATION BREAKDOWN (Single-Tenant Baseline):", font=self.typo.get_font(size=17, bold=True), fill=TEXT_OBSIDIAN)

            # Large Utilization Bar (Full Width 900px)
            bar_w = 900
            bar_h = 56
            bar_x0 = hx0 + 30
            bar_y0 = bot_y + 32
            draw.rounded_rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h], radius=10, fill=BG_SURFACE_SUBTLE, outline=BORDER_STRONG, width=2)

            # Active Slot (18% duty)
            active_w = int(bar_w * 0.18)
            draw.rounded_rectangle([bar_x0, bar_y0, bar_x0 + active_w, bar_y0 + bar_h], radius=10, fill=ACCENT_TECH_BLUE)
            draw.text((bar_x0 + 16, bar_y0 + 18), "ACTIVE EXEC", font=self.typo.get_font(size=14, bold=True, mono=True), fill=TEXT_INVERSE_WHITE)

            # Idle Slot (82% idle capacity warning pattern)
            idle_x0 = bar_x0 + active_w + 6
            idle_w = bar_w - active_w - 6
            draw.rounded_rectangle([idle_x0, bar_y0, idle_x0 + idle_w, bar_y0 + bar_h], radius=10, fill=ACCENT_AMBER_LIGHT, outline=ACCENT_AMBER, width=2)

            # Warning stripes inside idle bar
            stripe_step = 28
            for sx in range(idle_x0 + 10, idle_x0 + idle_w - 10, stripe_step):
                draw.line([(sx, bar_y0 + 6), (sx + 14, bar_y0 + bar_h - 6)], fill=ACCENT_AMBER, width=2)

            draw.text((idle_x0 + 40, bar_y0 + 18), "UNUTILIZED ACCELERATOR CAPACITY DURING AGENT ROLLOUT PAUSES", font=self.typo.get_font(size=14, bold=True, mono=True), fill=ACCENT_AMBER)

            # Explanatory takeaway callout
            draw.text(
                (hx0 + 30, bar_y0 + 72),
                "Single-tenant execution ties the physical accelerator to one agent's decision loop, leaving GPU cores idle.",
                font=self.typo.get_font(size=15),
                fill=TEXT_SLATE,
            )


# =============================================================================
# 3. PROCESS CONFINEMENT & COMMAND ENTITY (The Mechanism)
# =============================================================================
class ProcessConfinementLaserBoundary:
    """
    Full-screen spatial visualization of the Metal Sandbox mechanism.
    Features:
    - Spatial dividing barrier separating Host System from Isolated Workspace
    - Follows an animated Command Entity traveling from session to queue to hardware
    - 4-stage execution sequence with clear cause and effect
    """

    def __init__(self, typo: TypographyEngine):
        self.typo = typo

    def render(self, draw: ImageDraw.ImageDraw, t: float, camera: Optional[CinematicCamera] = None):
        # 1. Host Agent Workspace Emitting Command (y = 260 to 420)
        top_scale = scale_in(t, 0.1, 0.4)
        if top_scale > 0.01:
            ax0, ay0 = 60, 260
            ax1, ay1 = 1020, 420
            draw.rounded_rectangle([ax0 + 6, ay0 + 8, ax1 + 6, ay1 + 8], radius=16, fill=(210, 218, 230, 110))
            draw.rounded_rectangle([ax0, ay0, ax1, ay1], radius=16, fill=BG_SURFACE_CARD, outline=BORDER_STRONG, width=2)

            draw.text((ax0 + 24, ay0 + 18), "STEP 1: HOST AGENT WORKSPACE (Session Ingress)", font=self.typo.get_font(size=20, bold=True, mono=True), fill=TEXT_OBSIDIAN)
            draw.text((ax0 + 24, ay0 + 50), "Agent generates native development command (Metal kernel build / validation test)", font=self.typo.get_font(size=16), fill=TEXT_SLATE)

            # Command creation badge
            draw.rounded_rectangle([ax0 + 24, ay0 + 85, ax0 + 340, ay0 + 130], radius=8, fill=ACCENT_TECH_BLUE_LIGHT, outline=ACCENT_TECH_BLUE, width=2)
            draw.text((ax0 + 40, ay0 + 98), "EMIT: build_kernel_m4.cmd", font=self.typo.get_font(size=14, bold=True, mono=True), fill=ACCENT_TECH_BLUE)

        # 2. Filesystem & Process Confinement Boundary (y = 445 to 810)
        # Prominent spatial split: Left = Restricted Host, Right = Permitted Instance
        bound_scale = scale_in(t, 0.8, 0.5)
        if bound_scale > 0.01:
            bx0, by0 = 60, 445
            bx1, by1 = 1020, 810

            draw.rounded_rectangle([bx0 + 6, by0 + 8, bx1 + 6, by1 + 8], radius=18, fill=(210, 218, 230, 110))
            draw.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=BG_SURFACE_CARD, outline=ACCENT_EMERALD, width=3)

            # Security Banner Header
            draw.rounded_rectangle([bx0, by0, bx1, by0 + 48], radius=16, fill=ACCENT_EMERALD_LIGHT)
            draw.rectangle([bx0, by0 + 24, bx1, by0 + 48], fill=ACCENT_EMERALD_LIGHT)
            draw.text((bx0 + 24, by0 + 14), "STEP 2: PER-INSTANCE FILESYSTEM & PROCESS CONFINEMENT", font=self.typo.get_font(size=18, bold=True, mono=True), fill=ACCENT_EMERALD)

            col_w = 430
            col_h = 230

            # Left Column: Permitted Instance Workspace
            c1_x0 = bx0 + 24
            c1_y0 = by0 + 64
            draw.rounded_rectangle([c1_x0, c1_y0, c1_x0 + col_w, c1_y0 + col_h], radius=10, fill=BG_SURFACE_SUBTLE, outline=ACCENT_EMERALD, width=2)
            draw.text((c1_x0 + 18, c1_y0 + 16), "PERMITTED INSTANCE PATHS", font=self.typo.get_font(size=15, bold=True, mono=True), fill=ACCENT_EMERALD)
            paths = [
                "./workspace/* (Isolated Git Repo)",
                "./build/kernel.metal (Compiled Output)",
                "/tmp/instance_session_499/* (Scratch)",
            ]
            for i, p in enumerate(paths):
                draw.text((c1_x0 + 18, c1_y0 + 52 + i * 36), f"✓  {p}", font=self.typo.get_font(size=13, mono=True), fill=TEXT_OBSIDIAN)

            # Right Column: Restricted Host Paths
            c2_x0 = bx1 - 24 - col_w
            c2_y0 = c1_y0
            draw.rounded_rectangle([c2_x0, c2_y0, c2_x0 + col_w, c2_y0 + col_h], radius=10, fill=BG_SURFACE_SUBTLE, outline=ACCENT_MUTED_RED, width=2)
            draw.text((c2_x0 + 18, c2_y0 + 16), "RESTRICTED HOST PATHS", font=self.typo.get_font(size=15, bold=True, mono=True), fill=ACCENT_MUTED_RED)
            blocked = [
                "/System/* (macOS Core Daemons)",
                "/Users/Shared/credentials (Keys)",
                "Cross-session workspace trees",
            ]
            for i, b in enumerate(blocked):
                draw.text((c2_x0 + 18, c2_y0 + 52 + i * 36), f"✕  {b}", font=self.typo.get_font(size=13, mono=True), fill=TEXT_SLATE)

            # Central Confinement Guarantee Callout
            draw.text(
                (bx0 + 24, by0 + 312),
                "Process confinement isolates files and credentials, while commands route to shared GPU queues.",
                font=self.typo.get_font(size=15, bold=True),
                fill=TEXT_OBSIDIAN,
            )

        # 3. Hardware Queue Scheduling & Harbor Cross-Node Migration (y = 835 to 1180)
        q_scale = scale_in(t, 2.0, 0.45)
        if q_scale > 0.01:
            qx0, qy0 = 60, 835
            qx1, qy1 = 1020, 1180

            draw.rounded_rectangle([qx0 + 6, qy0 + 8, qx1 + 6, qy1 + 8], radius=18, fill=(210, 218, 230, 110))
            draw.rounded_rectangle([qx0, qy0, qx1, qy1], radius=18, fill=BG_SURFACE_CARD, outline=ACCENT_TECH_BLUE, width=3)

            draw.text((qx0 + 24, qy0 + 18), "STEP 3: HARDWARE QUEUE ARBITRATION & HARBOR MIGRATION", font=self.typo.get_font(size=18, bold=True, mono=True), fill=TEXT_OBSIDIAN)
            draw.text((qx0 + 24, qy0 + 50), "Interleaves commands from concurrent agent sessions onto shared Mac mini M4 nodes", font=self.typo.get_font(size=15), fill=TEXT_SLATE)

            # 4 Sequential Queue Pipeline Slots
            slots = [
                ("1. SERIAL SLOT", "1 task / node", ACCENT_TECH_BLUE),
                ("2. METAL PIPELINE", "Direct GPU dispatch", ACCENT_INDIGO_SILICON),
                ("3. SYNC BARRIER", "Kernel completion", ACCENT_EMERALD),
                ("4. HARBOR RETURN", "Result back to agent", ACCENT_TECH_BLUE),
            ]
            slot_w = 215
            active_slot_idx = int(t * 1.6) % 4 if t >= 2.5 else -1

            for i, (s_name, s_desc, s_col) in enumerate(slots):
                sx = qx0 + 24 + i * (slot_w + 18)
                sy = qy0 + 95
                is_active = (i == active_slot_idx)
                s_bg = ACCENT_TECH_BLUE_LIGHT if is_active else BG_SURFACE_SUBTLE
                draw.rounded_rectangle([sx, sy, sx + slot_w, sy + 85], radius=10, fill=s_bg, outline=s_col, width=3 if is_active else 2)
                draw.text((sx + 14, sy + 16), s_name, font=self.typo.get_font(size=13, bold=True, mono=True), fill=s_col)
                draw.text((sx + 14, sy + 44), s_desc, font=self.typo.get_font(size=12), fill=TEXT_SLATE)

            # Continuous animated command pulse moving through stages
            if t >= 2.5:
                phase = (t * 1.6) % 4.0
                curr_st = int(phase)
                frac = phase - curr_st
                curr_x = qx0 + 24 + curr_st * (slot_w + 18) + int(frac * slot_w)
                curr_y = qy0 + 137
                draw.circle((curr_x, curr_y), radius=8, fill=ACCENT_INDIGO_SILICON)
                draw.circle((curr_x, curr_y), radius=4, fill=TEXT_INVERSE_WHITE)

            draw.text(
                (qx0 + 24, qy0 + 205),
                "Hardware queue scheduling interleaves execution without modifying the underlying agent rollout logic.",
                font=self.typo.get_font(size=14, mono=True),
                fill=TEXT_MUTED,
            )

        # 4. Evaluated Architectural Property Callout (y = 1205 to 1380)
        callout_t = fade_in(t, 3.5, 0.5)
        if callout_t > 0.01:
            cx0, cy0 = 60, 1205
            cx1, cy1 = 1020, 1380

            draw.rounded_rectangle([cx0 + 6, cy0 + 8, cx1 + 6, cy1 + 8], radius=16, fill=(210, 218, 230, int(110 * callout_t)))
            draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=16, fill=BG_SURFACE_CARD, outline=ACCENT_EMERALD, width=2)

            draw.text((cx0 + 24, cy0 + 18), "EVALUATED ARCHITECTURAL PROPERTY // arXiv:2611.17294v1", font=self.typo.get_font(size=16, bold=True, mono=True), fill=ACCENT_EMERALD)
            c_text = (
                "Decouples filesystem confinement from accelerator scheduling. "
                "Agent sessions remain restricted to private workspaces, while command-level queues maximize Apple Silicon GPU utilization."
            )
            self.typo.draw_text_block(
                draw=draw,
                text=c_text,
                box=(cx0 + 24, cy0 + 50, 912, 110),
                fill=TEXT_OBSIDIAN,
                preferred_size=18,
                min_size=14,
                bold=False,
            )


# =============================================================================
# 4. CINEMATIC BENCHMARK RACE (Evidence & Measured Results)
# =============================================================================
class CinematicBenchmarkRace:
    """
    Full-width visual comparison presenting verified empirical figures from arXiv:2611.17294v1.
    Replaces static metric cards with an animated race visualizer:
    - 1.68x - 2.05x Command Throughput Gain (Hero Speedup Indicator)
    - -22.3% Batch Elapsed Time Reduction (Visual Race Bar)
    - -18.8% Tool Waiting Latency Reduction (Latency Drop Meter)
    - Distinct Measured Hardware vs Estimated Model badges
    """

    def __init__(self, typo: TypographyEngine):
        self.typo = typo

    def render(self, draw: ImageDraw.ImageDraw, t: float, camera: Optional[CinematicCamera] = None):
        # 1. Hero Throughput Speedup Display (y = 260 to 520)
        hero_scale = scale_in(t, 0.1, 0.45)
        if hero_scale > 0.01:
            hx0, hy0 = 60, 260
            hx1, hy1 = 1020, 520

            draw.rounded_rectangle([hx0 + 6, hy0 + 8, hx1 + 6, hy1 + 8], radius=20, fill=(210, 218, 230, 110))
            draw.rounded_rectangle([hx0, hy0, hx1, hy1], radius=20, fill=BG_SURFACE_CARD, outline=ACCENT_EMERALD, width=3)

            # Header pill
            draw.rounded_rectangle([hx0 + 24, hy0 + 18, hx0 + 360, hy0 + 52], radius=6, fill=ACCENT_EMERALD_LIGHT, outline=ACCENT_EMERALD, width=1)
            draw.text((hx0 + 36, hy0 + 26), "PRIMARY MEASURED HARDWARE METRIC", font=self.typo.get_font(size=13, bold=True, mono=True), fill=ACCENT_EMERALD)

            # Giant Hero Typography: 1.68x – 2.05x
            gain_prog = get_progress(t, 0.4, 1.4, "ease_out_cubic")
            cur_gain = 1.68 + (2.05 - 1.68) * gain_prog
            hero_text = f"1.68× — {cur_gain:.2f}×"
            hero_font = self.typo.get_font(size=64, bold=True)
            draw.text((hx0 + 24, hy0 + 68), hero_text, font=hero_font, fill=TEXT_OBSIDIAN)

            draw.text((hx0 + 24, hy0 + 155), "COMMAND THROUGHPUT GAIN UNDER CONCENTRATED DEMAND", font=self.typo.get_font(size=18, bold=True), fill=ACCENT_TECH_BLUE)
            draw.text((hx0 + 24, hy0 + 188), "Measured on 4× Apple Mac mini M4 nodes vs unmanaged single-tenant execution (arXiv:2611.17294v1 Section 4)", font=self.typo.get_font(size=14, mono=True), fill=TEXT_MUTED)

            # Live Verification Badge
            pulse = 0.5 + 0.5 * math.sin(t * 3.0)
            p_rad = int(5 + 2 * pulse)
            draw.circle((hx1 - 40, hy0 + 36), radius=p_rad + 2, fill=(5, 150, 105, 120))
            draw.circle((hx1 - 40, hy0 + 36), radius=5, fill=ACCENT_EMERALD)
            draw.text((hx1 - 180, hy0 + 28), "VERIFIED EMPIRICAL", font=self.typo.get_font(size=12, bold=True, mono=True), fill=ACCENT_EMERALD)

        # 2. Dual Timeline Race Comparison (y = 545 to 900)
        race_scale = scale_in(t, 0.8, 0.5)
        if race_scale > 0.01:
            rx0, ry0 = 60, 545
            rx1, ry1 = 1020, 900

            draw.rounded_rectangle([rx0 + 6, ry0 + 8, rx1 + 6, ry1 + 8], radius=20, fill=(210, 218, 230, 110))
            draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=20, fill=BG_SURFACE_CARD, outline=BORDER_STRONG, width=2)

            draw.text((rx0 + 24, ry0 + 18), "BATCH ELAPSED TIME COMPARISON // 16 STATIC AGENT TRACES", font=self.typo.get_font(size=18, bold=True, mono=True), fill=TEXT_OBSIDIAN)

            bar_w = 912

            # Track 1: Baseline Single-Tenant (100% time)
            t1_y = ry0 + 60
            draw.text((rx0 + 24, t1_y), "1. BASELINE SINGLE-TENANT SCHEDULING (100% ELAPSED TIME):", font=self.typo.get_font(size=14, bold=True), fill=TEXT_SLATE)
            draw.rounded_rectangle([rx0 + 24, t1_y + 24, rx0 + 24 + bar_w, t1_y + 68], radius=8, fill=BG_SURFACE_SUBTLE, outline=BORDER_LIGHT, width=1)
            draw.rounded_rectangle([rx0 + 24, t1_y + 24, rx0 + 24 + bar_w, t1_y + 68], radius=8, fill=BORDER_STRONG)
            draw.text((rx0 + 40, t1_y + 36), "BASELINE REPLAY: 100.0% ELAPSED DURATION", font=self.typo.get_font(size=14, bold=True, mono=True), fill=TEXT_OBSIDIAN)

            # Track 2: Metal Sandbox Dynamic Scheduling (-22.3% time reduction)
            t2_y = t1_y + 85
            draw.text((rx0 + 24, t2_y), "2. METAL SANDBOX INTERLEAVED SCHEDULING:", font=self.typo.get_font(size=14, bold=True), fill=ACCENT_TECH_BLUE)
            draw.rounded_rectangle([rx0 + 24, t2_y + 24, rx0 + 24 + bar_w, t2_y + 68], radius=8, fill=BG_SURFACE_SUBTLE, outline=BORDER_LIGHT, width=1)

            prog2 = get_progress(t, 1.2, 1.2, "ease_out_cubic")
            target_fill = int(bar_w * 0.777)  # 100% - 22.3% = 77.7%
            cur_fill = int(bar_w * (1.0 - (0.223 * prog2)))
            draw.rounded_rectangle([rx0 + 24, t2_y + 24, rx0 + 24 + cur_fill, t2_y + 68], radius=8, fill=ACCENT_TECH_BLUE)

            # Reduction callout badge
            draw.text((rx0 + 40, t2_y + 36), f"-{22.3 * prog2:.1f}% BATCH ELAPSED TIME [MEASURED TRACE REPLAY]", font=self.typo.get_font(size=14, bold=True, mono=True), fill=TEXT_INVERSE_WHITE)

            # Track 3: Tool Waiting Latency Reduction (-18.8%)
            t3_y = t2_y + 85
            draw.text((rx0 + 24, t3_y), "3. MEAN TOOL WAITING LATENCY REDUCTION:", font=self.typo.get_font(size=14, bold=True), fill=TEXT_SLATE)
            draw.rounded_rectangle([rx0 + 24, t3_y + 24, rx0 + 24 + bar_w, t3_y + 68], radius=8, fill=BG_SURFACE_SUBTLE, outline=BORDER_LIGHT, width=1)
            prog3 = get_progress(t, 1.8, 1.2, "ease_out_cubic")
            cur_lat = int(bar_w * (1.0 - (0.188 * prog3)))
            draw.rounded_rectangle([rx0 + 24, t3_y + 24, rx0 + 24 + cur_lat, t3_y + 68], radius=8, fill=ACCENT_EMERALD)
            draw.text((rx0 + 40, t3_y + 36), f"-{18.8 * prog3:.1f}% TOOL WAITING LATENCY [MEASURED TRACE REPLAY]", font=self.typo.get_font(size=14, bold=True, mono=True), fill=TEXT_INVERSE_WHITE)

        # 3. Model Estimate vs Empirical Distinction Card (y = 925 to 1180)
        est_scale = scale_in(t, 2.2, 0.45)
        if est_scale > 0.01:
            ex0, ey0 = 60, 925
            ex1, ey1 = 1020, 1180

            draw.rounded_rectangle([ex0 + 6, ey0 + 8, ex1 + 6, ey1 + 8], radius=18, fill=(210, 218, 230, 110))
            draw.rounded_rectangle([ex0, ey0, ex1, ey1], radius=18, fill=BG_SURFACE_CARD, outline=BORDER_STRONG, width=2)

            draw.text((ex0 + 24, ey0 + 18), "METHODOLOGICAL EVIDENCE CLASSIFICATION", font=self.typo.get_font(size=18, bold=True, mono=True), fill=TEXT_OBSIDIAN)

            # Two distinct badges: Measured Hardware vs Estimated Trace Model
            b1_w = 440
            draw.rounded_rectangle([ex0 + 24, ey0 + 54, ex0 + 24 + b1_w, ey0 + 195], radius=10, fill=ACCENT_EMERALD_LIGHT, outline=ACCENT_EMERALD, width=2)
            draw.text((ex0 + 40, ey0 + 70), "● MEASURED ON HARDWARE", font=self.typo.get_font(size=15, bold=True, mono=True), fill=ACCENT_EMERALD)
            draw.text((ex0 + 40, ey0 + 100), "• 1.68× – 2.05× Command Throughput\n• -22.3% Batch Elapsed Duration\n• -18.8% Tool Waiting Latency\n(Tested on 4× Mac mini M4 Nodes)", font=self.typo.get_font(size=13), fill=TEXT_OBSIDIAN)

            b2_x0 = ex1 - 24 - b1_w
            draw.rounded_rectangle([b2_x0, ey0 + 54, b2_x0 + b1_w, ey0 + 195], radius=10, fill=ACCENT_TECH_BLUE_LIGHT, outline=ACCENT_TECH_BLUE, width=2)
            draw.text((b2_x0 + 16, ey0 + 70), "○ ESTIMATED TRACE MODEL", font=self.typo.get_font(size=15, bold=True, mono=True), fill=ACCENT_TECH_BLUE)
            draw.text((b2_x0 + 16, ey0 + 100), "• 2.14× Sustained Replay Gain\n(Estimated for 4 sessions/node vs 1\nunder 16 static trace assumptions)", font=self.typo.get_font(size=13), fill=TEXT_OBSIDIAN)

        # 4. Architectural Synthesis Verdict (y = 1205 to 1380)
        verdict_t = fade_in(t, 3.2, 0.5)
        if verdict_t > 0.01:
            vx0, vy0 = 60, 1205
            vx1, vy1 = 1020, 1380

            draw.rounded_rectangle([vx0 + 6, vy0 + 8, vx1 + 6, vy1 + 8], radius=16, fill=(210, 218, 230, int(110 * verdict_t)))
            draw.rounded_rectangle([vx0, vy0, vx1, vy1], radius=16, fill=TEXT_OBSIDIAN)

            draw.text((vx0 + 24, vy0 + 18), "ARCHITECTURAL SYNTHESIS // SUPER.INTELLIGENCEEE", font=self.typo.get_font(size=16, bold=True, mono=True), fill=ACCENT_TECH_BLUE_LIGHT)
            v_text = (
                "Decoupling per-instance filesystem sandboxing from command-level GPU queues unlocks up to 2.05x throughput gains "
                "across Apple Silicon clusters without sacrificing host integrity."
            )
            self.typo.draw_text_block(
                draw=draw,
                text=v_text,
                box=(vx0 + 24, vy0 + 50, 912, 110),
                fill=TEXT_INVERSE_WHITE,
                preferred_size=19,
                min_size=15,
                bold=True,
            )
