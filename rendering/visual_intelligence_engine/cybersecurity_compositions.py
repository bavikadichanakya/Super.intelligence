"""
SUPER.INTELLIGENCEEE — Cybersecurity & Systems Compositions
Implements full-bleed 1080x1920 explanatory visualizations for eBPF kernel security,
verifier static analysis, register truncation exploits, and arbitrary memory read/write.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw

from core.universal_scene_contract import UniversalSceneContract
from creative.visual_intelligence.motion_director import MotionDirector
from rendering.visual_intelligence_engine.composition_base import BaseVisualIntelligenceComposition


class KernelRingBoundaryComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes the hierarchical CPU protection rings (Ring 3 User Space to Ring 0 Kernel Space).
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Concentric Protection Rings
        rings = [
            (460 * scale, "RING 3: USER APPLICATION SPACE", (71, 85, 105), 1),
            (340 * scale, "RING 2: SYSTEM DEVICE DRIVERS", (100, 116, 139), 1),
            (230 * scale, "RING 1: HYPERVISOR VIRTUALIZATION", (148, 163, 184), 1),
            (130 * scale, "RING 0: LINUX KERNEL CORE", (244, 63, 94), 3),
        ]

        for radius, label, color, width in rings:
            bbox = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
            draw.ellipse(bbox, outline=color, width=width)
            # Label
            draw.text((center_x - radius + 20, center_y - 12), label, fill=color, font=self.font_mono)

        # Pulsing Kernel Core at center
        pulse = MotionDirector.pulse_sin(t, freq=2.0, min_val=50, max_val=75)
        draw.ellipse([center_x - pulse, center_y - pulse, center_x + pulse, center_y + pulse], fill=(244, 63, 94, 70), outline=(244, 63, 94), width=2)
        draw.text((center_x - 45, center_y - 10), "RING 0", fill=(255, 255, 255), font=self.font_sans_head)

        # Telemetry badge: Kernel Execution Privilege
        draw.rounded_rectangle([center_x - 220, center_y + 490, center_x + 220, center_y + 560], radius=12, fill=(15, 23, 42, 240), outline=(244, 63, 94), width=2)
        draw.text((center_x - 190, center_y + 508), "ROOT PRIVILEGE ZONE: UNRESTRICTED", fill=(244, 63, 94), font=self.font_mono_bold)


class BytecodeVerifierGraphComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes eBPF Static Verifier:
    Traversing execution branches to guarantee memory safety before kernel execution.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Verifier Execution Flow Chart
        steps = [
            ("INSTRUCTION FEED", -380, "bpf_prog_load()", (2, 132, 199)),
            ("CONTROL FLOW GRAPH", -200, "DAG Cycle & Loop Check", (2, 132, 199)),
            ("REGISTER BOUNDS CHECK", -20, "ALU Min/Max State Tracking", (5, 150, 105)),
            ("MEMORY ACCESS VALIDATION", 160, "Check Stack & Map Boundaries", (5, 150, 105)),
            ("JIT MACHINE CODE EMIT", 340, "Native x86_64 Instructions", (15, 23, 42)),
        ]

        card_w, card_h = 360, 48
        for name, oy, sub, col in steps:
            by = center_y + oy
            draw.rounded_rectangle([center_x - card_w, by - card_h, center_x + card_w, by + card_h], radius=10, fill=(255, 255, 255), outline=col, width=2)
            draw.text((center_x - card_w + 24, by - 26), name, fill=col, font=self.font_mono_bold)
            draw.text((center_x - card_w + 24, by + 4), sub, fill=(71, 85, 105), font=self.font_mono)

            # Connector arrows
            if oy < 340:
                draw.line([(center_x, by + card_h), (center_x, by + card_h + 30)], fill=(2, 132, 199), width=2)

        # Scanning laser line across verifier
        laser_progress = (t * 0.4) % 1.0
        laser_y = (center_y - 420) + laser_progress * 800
        draw.line([(center_x - 420, laser_y), (center_x + 420, laser_y)], fill=(5, 150, 105), width=2)
        draw.text((center_x + 220, laser_y - 20), "[VERIFYING SAFE]", fill=(5, 150, 105), font=self.font_mono)


class MemoryCorruptionMapComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes CVE-2023-2163:
    32-bit register truncation creating a mismatch between verifier assumption and runtime state.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Dual Register Display: Verifier State vs Actual Hardware State
        box_w, box_h = 380, 220

        # Left: Verifier Believed State
        lx = center_x - 200
        draw.rounded_rectangle([lx - box_w/2, center_y - box_h/2 - 120, lx + box_w/2, center_y + box_h/2 - 120], radius=12, fill=(240, 253, 244), outline=(5, 150, 105), width=2)
        draw.text((lx - 160, center_y - 200), "VERIFIER BELIEVED STATE", fill=(5, 150, 105), font=self.font_mono_bold)
        draw.text((lx - 160, center_y - 150), "Register R1: [0, 0]", fill=(15, 23, 42), font=self.font_mono)
        draw.text((lx - 160, center_y - 110), "Truncated: 0x00000000", fill=(71, 85, 105), font=self.font_mono)
        draw.text((lx - 160, center_y - 70), "Safety Verdict: APPROVED", fill=(5, 150, 105), font=self.font_sans_head)

        # Right: Actual Hardware State (Divergence!)
        rx = center_x + 200
        draw.rounded_rectangle([rx - box_w/2, center_y - box_h/2 - 120, rx + box_w/2, center_y + box_h/2 - 120], radius=12, fill=(254, 242, 242), outline=(220, 38, 38), width=2)
        draw.text((rx - 160, center_y - 200), "ACTUAL RUNTIME STATE", fill=(220, 38, 38), font=self.font_mono_bold)
        draw.text((rx - 160, center_y - 150), "Register R1: [0x100000000]", fill=(15, 23, 42), font=self.font_mono)
        draw.text((rx - 160, center_y - 110), "64-bit Overflow Bit Intact", fill=(71, 85, 105), font=self.font_mono)
        draw.text((rx - 160, center_y - 70), "Result: OUT-OF-BOUNDS", fill=(220, 38, 38), font=self.font_sans_head)

        # Big Animated Exploit Pointer Jump
        p_exploit = min(1.0, max(0.0, (t - 1.5) / 1.0))
        p_arrow = MotionDirector.ease_out_back(p_exploit)
        draw.line([(center_x, center_y + 40), (center_x, center_y + 40 + 260 * p_arrow)], fill=(220, 38, 38), width=4)
        draw.polygon([
            (center_x, center_y + 40 + 260 * p_arrow),
            (center_x - 14, center_y + 40 + 260 * p_arrow - 20),
            (center_x + 14, center_y + 40 + 260 * p_arrow - 20),
        ], fill=(220, 38, 38))

        # Target Overwrite: Kernel Credential Block
        draw.rounded_rectangle([center_x - 280, center_y + 340, center_x + 280, center_y + 440], radius=12, fill=(15, 23, 42), outline=(220, 38, 38), width=2)
        draw.text((center_x - 240, center_y + 360), "OUT-OF-BOUNDS ARBITRARY WRITE TARGET", fill=(248, 113, 113), font=self.font_mono)
        draw.text((center_x - 240, center_y + 395), "Overwriting struct cred -> uid=0, gid=0", fill=(255, 255, 255), font=self.font_sans_head)


class TracepointInterceptionComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes kernel hook overwrite and root privilege elevation.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Credential elevation indicator
        elevated = t >= 2.0
        badge_color = (220, 38, 38) if not elevated else (5, 150, 105)
        badge_text = "UID: 1000 (UNPRIVILEGED USER)" if not elevated else "UID: 0 [ROOT AUTHORITY ACQUIRED]"

        draw.rounded_rectangle([center_x - 320, center_y - 200, center_x + 320, center_y - 80], radius=14, fill=(15, 23, 42), outline=badge_color, width=3)
        draw.text((center_x - 270, center_y - 150), badge_text, fill=badge_color, font=self.font_sans_head)

        # Linux syscall interception table
        syscalls = [
            ("sys_read()", "Normal Execution", (71, 85, 105)),
            ("sys_write()", "Normal Execution", (71, 85, 105)),
            ("sys_execve()", "INTERCEPTED BY BPF ROOTKIT", (220, 38, 38)),
            ("sys_setuid()", "OVERRIDDEN -> ALWAYS RETURN 0", (220, 38, 38)),
        ]

        sy_base = center_y + 40
        for name, status, col in syscalls:
            draw.rectangle([center_x - 300, sy_base - 25, center_x + 300, sy_base + 25], fill=(255, 255, 255), outline=col, width=1)
            draw.text((center_x - 280, sy_base - 10), name, fill=(15, 23, 42), font=self.font_mono_bold)
            draw.text((center_x - 40, sy_base - 10), status, fill=col, font=self.font_mono)
            sy_base += 70
