"""
SUPER.INTELLIGENCEEE — Hardware & GPU Compiler Compositions
Implements full-bleed 1080x1920 explanatory visualizations for GPU memory hierarchy,
asynchronous TMA streaming, WGMMA warp groups, and FlashAttention-3 Hopper speedups.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw

from core.universal_scene_contract import UniversalSceneContract
from creative.visual_intelligence.motion_director import MotionDirector
from rendering.visual_intelligence_engine.composition_base import BaseVisualIntelligenceComposition


class MemoryHierarchyPipelineComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes the GPU Memory Wall:
    Off-chip HBM3 high latency vs On-chip SRAM ultra-low latency.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Top: HBM3 Global Memory Stack
        hbm_y = center_y - 280
        draw.rounded_rectangle([center_x - 340, hbm_y - 80, center_x + 340, hbm_y + 80], radius=14, fill=(15, 23, 42), outline=(245, 158, 11), width=2)
        draw.text((center_x - 300, hbm_y - 45), "HBM3 GLOBAL MEMORY (OFF-CHIP)", fill=(245, 158, 11), font=self.font_sans_head)
        draw.text((center_x - 300, hbm_y + 10), "Bandwidth: 3.35 TB/s | Roundtrip Latency: 400 Cycles", fill=(203, 213, 225), font=self.font_mono)

        # Chasm / Latency Gap
        draw.line([(center_x - 160, hbm_y + 80), (center_x - 160, center_y + 160)], fill=(239, 68, 68), width=3)
        draw.line([(center_x + 160, hbm_y + 80), (center_x + 160, center_y + 160)], fill=(239, 68, 68), width=3)

        draw.rounded_rectangle([center_x - 140, center_y - 40, center_x + 140, center_y + 40], radius=10, fill=(69, 10, 10), outline=(239, 68, 68), width=2)
        draw.text((center_x - 110, center_y - 14), "THE MEMORY WALL", fill=(254, 202, 202), font=self.font_sans_head)

        # Bottom: On-Chip SRAM (Shared Memory)
        sram_y = center_y + 280
        draw.rounded_rectangle([center_x - 340, sram_y - 80, center_x + 340, sram_y + 80], radius=14, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
        draw.text((center_x - 300, sram_y - 45), "HOPPER SM SHARED MEMORY (ON-CHIP)", fill=(56, 189, 248), font=self.font_sans_head)
        draw.text((center_x - 300, sram_y + 10), "Bandwidth: 33 TB/s (10x Faster) | Latency: 20 Cycles", fill=(203, 213, 225), font=self.font_mono)


class CacheLineConcurrencyComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes traditional attention bottleneck:
    SM cores stalling while waiting for Softmax normalization before next GEMM.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Timeline visualization of synchronous execution
        phases = [
            ("STAGE 1: GEMM-1 (Q * K^T)", -280, (2, 132, 199)),
            ("STAGE 2: SOFTMAX WAIT STALL (IDLE SM)", -100, (239, 68, 68)),
            ("STAGE 3: GEMM-2 (P * V)", 80, (2, 132, 199)),
            ("STAGE 4: GLOBAL WRITEBACK STALL", 260, (239, 68, 68)),
        ]

        bar_w = 680
        for name, oy, col in phases:
            by = center_y + oy
            draw.rounded_rectangle([center_x - bar_w/2, by - 36, center_x + bar_w/2, by + 36], radius=10, fill=(255, 255, 255), outline=col, width=2)
            draw.text((center_x - bar_w/2 + 24, by - 14), name, fill=col, font=self.font_mono_bold)

        # Stamped stall telemetry
        draw.rounded_rectangle([center_x - 240, center_y + 380, center_x + 240, center_y + 460], radius=12, fill=(254, 226, 226), outline=(239, 68, 68), width=2)
        draw.text((center_x - 200, center_y + 404), "SM COMPUTE UTILIZATION: ONLY 38%", fill=(185, 28, 28), font=self.font_sans_head)


class AsynchronousTensorWarpComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes Hardware TMA (Tensor Memory Accelerator):
    Direct asynchronous hardware copy from HBM3 to SRAM bypassing SM registers.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Hardware TMA direct DMA conduit
        draw.rounded_rectangle([center_x - 360, center_y - 320, center_x + 360, center_y + 320], radius=16, fill=(255, 255, 255), outline=(5, 150, 105), width=2)
        draw.text((center_x - 320, center_y - 280), "HARDWARE TMA DIRECT ENGINE (HOPPER)", fill=(5, 150, 105), font=self.font_sans_head)

        # 3 Parallel Streaming Conduits
        conduits = ["Q Tile Stream", "K Tile Stream", "V Tile Stream"]
        for idx, cname in enumerate(conduits):
            cy = center_y - 120 + idx * 110
            draw.line([(center_x - 300, cy), (center_x + 300, cy)], fill=(203, 213, 225), width=8)

            # Animated packet moving along conduit
            flow_p = (t * 1.5 + idx * 0.33) % 1.0
            px = (center_x - 300) + flow_p * 600
            draw.rounded_rectangle([px - 40, cy - 24, px + 40, cy + 24], radius=6, fill=(5, 150, 105))
            draw.text((center_x - 290, cy - 35), cname, fill=(71, 85, 105), font=self.font_mono)

        # SM Register Load: ZERO
        draw.rounded_rectangle([center_x - 280, center_y + 220, center_x + 280, center_y + 290], radius=10, fill=(240, 253, 244), outline=(5, 150, 105), width=2)
        draw.text((center_x - 240, center_y + 242), "SM REGISTER LOAD: 0% (HARDWARE DMA)", fill=(5, 150, 105), font=self.font_mono_bold)


class HardwareRegisterMeshComposition(BaseVisualIntelligenceComposition):
    """
    Visualizes Ping-Pong Double Buffering:
    Overlapping WGMMA Tensor Core computation with Softmax and TMA memory copies.
    """

    def render_mechanism(self, draw: ImageDraw.Draw, canvas: Image.Image, t: float):
        scale, pan_x, pan_y, rot = self.camera.get_transform(t)
        center_x = self.width / 2.0 + pan_x
        center_y = 960.0 + pan_y

        # Ping-Pong Buffer Display
        bw, bh = 340, 260
        b1_x = center_x - 190
        b2_x = center_x + 190

        # Buffer 1
        active_b1 = (int(t * 2.0) % 2) == 0
        col1 = (2, 132, 199) if active_b1 else (148, 163, 184)
        status1 = "COMPUTING GEMM (TENSOR CORE)" if active_b1 else "TMA LOADING NEXT TILE"
        draw.rounded_rectangle([b1_x - bw/2, center_y - bh/2, b1_x + bw/2, center_y + bh/2], radius=12, fill=(255, 255, 255), outline=col1, width=2)
        draw.text((b1_x - 140, center_y - 90), "STAGE A BUFFER", fill=col1, font=self.font_sans_head)
        draw.text((b1_x - 140, center_y - 20), status1, fill=(15, 23, 42), font=self.font_mono)

        # Buffer 2
        active_b2 = not active_b1
        col2 = (2, 132, 199) if active_b2 else (148, 163, 184)
        status2 = "COMPUTING GEMM (TENSOR CORE)" if active_b2 else "TMA LOADING NEXT TILE"
        draw.rounded_rectangle([b2_x - bw/2, center_y - bh/2, b2_x + bw/2, center_y + bh/2], radius=12, fill=(255, 255, 255), outline=col2, width=2)
        draw.text((b2_x - 140, center_y - 90), "STAGE B BUFFER", fill=col2, font=self.font_sans_head)
        draw.text((b2_x - 140, center_y - 20), status2, fill=(15, 23, 42), font=self.font_mono)

        # Overlap Badge: 100% Compute Overlap
        draw.rounded_rectangle([center_x - 240, center_y + 200, center_x + 240, center_y + 280], radius=12, fill=(240, 253, 244), outline=(5, 150, 105), width=2)
        draw.text((center_x - 200, center_y + 225), "OVERLAP EFFICIENCY: 100% CONTINUOUS", fill=(5, 150, 105), font=self.font_sans_head)
