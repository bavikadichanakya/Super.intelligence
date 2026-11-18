"""
SUPER.INTELLIGENCEEE — Phase 3.5 Vector Diagram & Systems Flow Engine
Visualizes parallel draft-verifier speculative decoding mechanics:
- Phase A (0% - 42%): Serial Autoregressive Bottleneck (HBM memory bus saturation waveform & token fetch stalls)
- Phase B (42% - 100%): Parallel Speculative Tree (Sweeping verification beam, parallel candidate evaluation, throughput acceleration)
Continuous wave packets, oscillating memory bus telemetry, and sweeping radar beams guarantee zero static holds.
"""

from __future__ import annotations

import logging
import math
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from creative.tech_documentary.motion_primitives import (
    draw_hud_brackets,
    draw_open_hairline,
    smooth_step,
    cubic_ease_out,
)

logger = logging.getLogger("super_intelligence.vector_diagram_engine")


class VectorDiagramEngine:
    """Renders full-screen mathematical and systems architecture animations to vertical 1080x1920 MP4."""

    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self._init_fonts()

    def _init_fonts(self) -> None:
        font_dir = Path("C:/Windows/Fonts")
        arial_path = font_dir / "arial.ttf"
        arialbd_path = font_dir / "arialbd.ttf"
        consola_path = font_dir / "consola.ttf"
        consolab_path = font_dir / "consolab.ttf"

        try:
            self.font_header = ImageFont.truetype(str(arialbd_path), 58) if arialbd_path.exists() else ImageFont.load_default()
            self.font_sub = ImageFont.truetype(str(arial_path), 34) if arial_path.exists() else ImageFont.load_default()
            self.font_math = ImageFont.truetype(str(consolab_path), 38) if consolab_path.exists() else ImageFont.load_default()
            self.font_label = ImageFont.truetype(str(arialbd_path), 34) if arialbd_path.exists() else ImageFont.load_default()
            self.font_badge = ImageFont.truetype(str(consolab_path), 26) if consolab_path.exists() else ImageFont.load_default()
            self.font_telemetry = ImageFont.truetype(str(consola_path), 24) if consola_path.exists() else ImageFont.load_default()
        except Exception:
            self.font_header = ImageFont.load_default()
            self.font_sub = self.font_header
            self.font_math = self.font_header
            self.font_label = self.font_header
            self.font_badge = self.font_header
            self.font_telemetry = self.font_header

    def render_frame(
        self,
        frame_idx: int,
        total_frames: int,
        topic_header: str = "SPECULATIVE VERIFICATION TREE",
        sub_header: str = "Draft Model Emits K=4 Tokens; Target Model Verifies in 1 Parallel Pass",
        telemetry: str = "REJECTION SAMPLING: min(1, p/q) // EXACT PROBABILITY MATCH // P=1.0",
    ) -> Image.Image:
        """
        Renders two-phase speculative systems architecture with active continuous motion:
        Phase A (0% - 42%): Autoregressive Sequential Stall (Memory bus ripple + traveling fetch packets)
        Phase B (42% - 100%): Speculative Verification Tree (Sweeping verification beam + parallel tree gates)
        """
        img = Image.new("RGB", (self.width, self.height), (247, 247, 242))
        draw = ImageDraw.Draw(img)

        # 1. Subtle vertical grid lines
        for gx in range(80, self.width, 180):
            draw.line([(gx, 140), (gx, self.height - 240)], fill=(235, 235, 228), width=1)

        frame_split = int(total_frames * 0.42)
        is_phase_a = frame_idx < frame_split

        # 2. Top Editorial Header
        top_y = 150
        header_color = (235, 80, 20) if is_phase_a else (49, 92, 255)
        draw.line([(80, top_y), (self.width - 80, top_y)], fill=header_color, width=2)
        draw.text((80, top_y + 16), "// SUPER.INTELLIGENCEEE  |  INFERENCE ARCHITECTURE", font=self.font_badge, fill=header_color)
        draw.text((self.width - 320, top_y + 16), "SYSTEMS PROOF", font=self.font_badge, fill=(120, 120, 120))

        if is_phase_a:
            # ─── PHASE A: SERIAL AUTOREGRESSIVE STALL (Evenly distributed Y = 150 to 1660) ───
            progress_a = frame_idx / max(1, frame_split)
            eased_a = smooth_step(progress_a)

            draw.text((80, top_y + 56), "SERIAL AUTOREGRESSIVE STALL", font=self.font_header, fill=(21, 21, 21))
            draw.text((80, top_y + 128), "1 Forward Pass = 1 Token = Full 140 GB Weight Memory Fetch from HBM", font=self.font_sub, fill=(75, 75, 75))

            # Visualizing Sequential Serial Memory Fetches with Continuous Pulse
            seq_y = 380
            tokens = ["x₁", "x₂", "x₃", "x₄", "x₅", "x₆"]
            num_tokens = len(tokens)
            spacing_x = (self.width - 240) // (num_tokens - 1)

            # Continuous traveling memory fetch packet along bus
            draw.line([(120, seq_y), (self.width - 120, seq_y)], fill=(225, 80, 40), width=4)
            for p_idx in range(3):
                pkt_x = 120 + int((frame_idx * 12 + p_idx * 260) % (self.width - 240))
                draw.rectangle([(pkt_x - 22, seq_y - 8), (pkt_x + 22, seq_y + 8)], fill=(255, 140, 60))

            active_token_idx = int(eased_a * (num_tokens - 0.1))

            for t_idx, t_name in enumerate(tokens):
                tx = 120 + (t_idx * spacing_x)
                is_active = (t_idx == active_token_idx)
                is_done = (t_idx < active_token_idx)

                # Continuous subtle radius breathing on active token
                r_base = 36
                if is_active:
                    r_base += int(4 * math.sin(frame_idx * 0.35))

                fill_col = (235, 80, 40) if is_active else (255, 255, 255) if is_done else (240, 240, 240)
                outline_col = (235, 80, 40) if is_active or is_done else (200, 205, 215)
                text_col = (255, 255, 255) if is_active else (21, 21, 21) if is_done else (140, 140, 140)

                draw.ellipse([(tx - r_base, seq_y - r_base), (tx + r_base, seq_y + r_base)], fill=fill_col, outline=outline_col, width=3)
                draw.text((tx - 16, seq_y - 18), t_name, font=self.font_label, fill=text_col)

            # Active Oscilloscope: Memory Bus Bandwidth Saturation Ripple
            wave_y = 540
            draw.text((120, wave_y - 28), "HBM3e MEMORY BUS SATURATION RIPPLE (2.0 TB/s BUS)", font=self.font_badge, fill=(235, 80, 40))
            draw.line([(120, wave_y + 50), (self.width - 120, wave_y + 50)], fill=(230, 230, 225), width=1)
            for wx in range(120, self.width - 120, 8):
                sin_val = math.sin((wx * 0.035) + (frame_idx * 0.22))
                bar_len = int(24 + 18 * sin_val)
                draw.line([(wx, wave_y + 50), (wx, wave_y + 50 - bar_len)], fill=(240, 95, 50), width=2)

            # Open Architectural Breakdown (Spaced across middle canvas Y = 740 to 1320)
            info_y = 740
            draw_open_hairline(draw, info_y, 80, self.width - 80, color=(235, 80, 40), width=2, label="01 / MEMORY ROOFLINE BOTTLENECK")
            draw.text((80, info_y + 30), "GPU ARITHMETIC INTENSITY < 1.0 FLOP / BYTE", font=self.font_label, fill=(235, 80, 40))
            draw.text((80, info_y + 90), "• Memory Access Time: 70.0 ms per generated token (140 GB / 2.0 TB/s)", font=self.font_math, fill=(21, 21, 21))
            draw.text((80, info_y + 150), "• Tensor Core Utilization: Only 11.2% active (88.8% idle wait states)", font=self.font_math, fill=(220, 40, 40))
            draw.text((80, info_y + 210), "• Batch-1 Generation Speed: 14.3 tok/s ceiling on NVIDIA A100-80GB", font=self.font_sub, fill=(70, 70, 70))

            # Hardware Allocation Penalty Callout
            pen_y = 1140
            draw_open_hairline(draw, pen_y, 80, self.width - 80, color=(120, 120, 120), width=1, label="02 / HARDWARE IDLE PENALTY")
            draw.text((80, pen_y + 26), "FULL 70B PARAMETER WEIGHT RE-FETCH ON EVERY STEP", font=self.font_badge, fill=(220, 40, 40))
            draw.text((80, pen_y + 68), "DRAM Transfer Stall: 98.4% of execution time spent waiting on HBM", font=self.font_sub, fill=(50, 50, 50))
            draw.text((80, pen_y + 115), "Compute roofline throttled by pin bandwidth rather than TFLOPS capacity", font=self.font_telemetry, fill=(90, 90, 90))

            # Continuous scanning radar hairline across breakdown card
            scan_hud_y = 1420
            draw.line([(80, scan_hud_y), (self.width - 80, scan_hud_y)], fill=(225, 225, 218), width=1)
            radar_pt = 80 + int((frame_idx * 14) % (self.width - 160))
            draw.line([(radar_pt, scan_hud_y - 4), (radar_pt + 30, scan_hud_y - 4)], fill=(235, 80, 40), width=3)
            draw.text((80, scan_hud_y + 20), "STATUS: MEMORY BANDWIDTH SATURATED // HIGH INFERENCE LATENCY", font=self.font_badge, fill=(220, 40, 40))

            bottom_y = self.height - 240
            draw.line([(80, bottom_y), (self.width - 80, bottom_y)], fill=(225, 225, 218), width=1)
            draw.text((80, bottom_y + 20), "COMPLEXITY: O(K · T_mem) [SERIAL MEMORY WALL]", font=self.font_telemetry, fill=(220, 40, 40))
            draw.text((self.width - 280, bottom_y + 20), "MEMORY BOTTLENECK", font=self.font_telemetry, fill=(220, 40, 40))

        else:
            # ─── PHASE B: PARALLEL SPECULATIVE VERIFICATION TREE (Evenly distributed Y = 150 to 1660) ───
            rel_idx = frame_idx - frame_split
            rem_frames = total_frames - frame_split
            progress_b = min(1.0, rel_idx / max(1, rem_frames * 0.45))
            eased_b = cubic_ease_out(progress_b)

            draw.text((80, top_y + 56), "SPECULATIVE VERIFICATION TREE", font=self.font_header, fill=(21, 21, 21))
            draw.text((80, top_y + 128), "Draft model emits K=4 candidates; Target verifies in 1 parallel pass", font=self.font_sub, fill=(75, 75, 75))

            # Mathematical Rejection Sampling Criterion
            math_y = 310
            draw_open_hairline(draw, math_y, 80, self.width - 80, color=(49, 92, 255), width=2, label="02 / MODIFIED REJECTION SAMPLING")
            draw.text((80, math_y + 28), "Acceptance Probability:  β_i = min(1, p(x_i) / q(x_i))", font=self.font_math, fill=(49, 92, 255))
            draw.text((80, math_y + 80), "THEOREM: Exact Target Distribution Preserved (p=1.000)", font=self.font_telemetry, fill=(5, 150, 105))

            # Enlarged Visual Speculative Tree Diagram (Spans Y = 460 to 760)
            tree_y = 530
            root_x = 130
            root_r = 44
            draw.ellipse([(root_x - root_r, tree_y - root_r), (root_x + root_r, tree_y + root_r)], fill=(49, 92, 255))
            draw.text((root_x - 18, tree_y - 18), "x₀", font=self.font_label, fill=(255, 255, 255))
            draw.text((root_x - 42, tree_y + 54), "Context", font=self.font_telemetry, fill=(60, 60, 60))

            draft_tokens = [
                ("x̃₁", True, "β=0.94"),
                ("x̃₂", True, "β=0.88"),
                ("x̃₃", True, "β=0.79"),
                ("x̃₄", False, "β=0.31"),
            ]
            num_drafts = len(draft_tokens)
            draft_step_x = (self.width - 340) // num_drafts

            # Sweeping parallel verification beam across tree
            beam_x = root_x + int((frame_idx * 16) % (self.width - 240))
            draw.rectangle([(beam_x - 20, tree_y - 65), (beam_x + 20, tree_y + 65)], fill=(220, 240, 255))

            node_r = 42
            for d_idx, (d_name, is_acc, beta_str) in enumerate(draft_tokens):
                dx = root_x + 130 + (d_idx * draft_step_x)
                prev_x = root_x if d_idx == 0 else (root_x + 130 + ((d_idx - 1) * draft_step_x))

                line_col = (5, 150, 105) if is_acc else (235, 80, 40)
                draw.line([(prev_x + root_r, tree_y), (dx - node_r, tree_y)], fill=line_col, width=4)

                node_fill = (5, 150, 105) if is_acc else (235, 80, 40)
                draw.ellipse([(dx - node_r, tree_y - node_r), (dx + node_r, tree_y + node_r)], fill=node_fill)
                draw.text((dx - 18, tree_y - 18), d_name, font=self.font_label, fill=(255, 255, 255))

                draw.text((dx - 34, tree_y + 54), beta_str, font=self.font_badge, fill=(30, 30, 30))
                tag_str = "ACCEPTED" if is_acc else "REJECTED"
                tag_col = (5, 150, 105) if is_acc else (220, 40, 40)
                draw.text((dx - 44, tree_y + 90), tag_str, font=self.font_telemetry, fill=tag_col)

            # Continuous traveling verification packet
            wave_x = root_x + int((frame_idx * 18) % (self.width - 240))
            draw.ellipse([(wave_x - 14, tree_y - 14), (wave_x + 14, tree_y + 14)], fill=(0, 220, 255))

            # Hardware Parallel Verification Box (Spans Y = 780 to 1240)
            stat_y = 780
            draw_open_hairline(draw, stat_y, 80, self.width - 80, color=(5, 150, 105), width=2, label="03 / PARALLEL TARGET VERIFICATION (1 FORWARD PASS)")
            draw.text((80, stat_y + 28), "1 PARALLEL FORWARD PASS VERIFIES ALL K=4 TOKENS", font=self.font_label, fill=(5, 150, 105))

            m_y1 = stat_y + 90
            draw.text((80, m_y1), "• Verification Time:", font=self.font_sub, fill=(50, 50, 50))
            draw.text((440, m_y1), "72.4 ms total", font=self.font_math, fill=(5, 150, 105))
            draw.text((680, m_y1), "(vs 280 ms sequential)", font=self.font_sub, fill=(90, 90, 90))

            m_y2 = m_y1 + 70
            draw.text((80, m_y2), "• Effective Throughput:", font=self.font_sub, fill=(50, 50, 50))
            draw.text((440, m_y2), "98.4 tok/s", font=self.font_math, fill=(5, 150, 105))
            draw.text((680, m_y2), "(+321% acceleration)", font=self.font_sub, fill=(90, 90, 90))

            m_y3 = m_y2 + 70
            draw.text((80, m_y3), "• Mathematical Parity:", font=self.font_sub, fill=(50, 50, 50))
            draw.text((440, m_y3), "Δ Perplexity = 0.00", font=self.font_math, fill=(49, 92, 255))
            draw.text((760, m_y3), "(p=1.000)", font=self.font_sub, fill=(90, 90, 90))

            # DRAM Bandwidth Amortization Block (Spans Y = 1140 to 1380)
            dram_y = 1140
            draw_open_hairline(draw, dram_y, 80, self.width - 80, color=(49, 92, 255), width=2, label="04 / MEMORY ACCESS REDUCTION")
            draw.text((80, dram_y + 26), "75% REDUCTION IN HBM PARAMETER TRANSFERS", font=self.font_badge, fill=(49, 92, 255))
            draw.text((80, dram_y + 68), "Weights loaded ONCE per 4 tokens // Arithmetic Intensity > 35 FLOP/byte", font=self.font_sub, fill=(40, 40, 40))
            draw.text((80, dram_y + 115), "Compute bound parallel GEMM replaces memory bound sequential waiting", font=self.font_telemetry, fill=(90, 90, 90))

            # Active live throughput waveform (Spans Y = 1420 to 1580)
            spark_y = 1440
            draw.line([(80, spark_y), (self.width - 80, spark_y)], fill=(220, 235, 225), width=1)
            for sx in range(80, self.width - 80, 8):
                sh = int(18 + 12 * math.sin((sx * 0.05) + (frame_idx * 0.25)))
                draw.line([(sx, spark_y), (sx, spark_y - sh)], fill=(5, 150, 105), width=2)

            draw.text((80, spark_y + 20), "DRAFT ACCEPTANCE RATE: 78.4% AVERAGE ACROSS CODE & REASONING", font=self.font_badge, fill=(49, 92, 255))
            draw.text((80, spark_y + 56), "STATUS: REPRODUCIBLE INFERENCE READY // vLLM NATIVE ENGINE", font=self.font_badge, fill=(5, 150, 105))

            bottom_y = self.height - 240
            draw.line([(80, bottom_y), (self.width - 80, bottom_y)], fill=(225, 225, 218), width=1)
            draw.text((80, bottom_y + 20), "COMPLEXITY: O(1 · T_mem) [PARALLEL GEMM VERIFICATION]", font=self.font_telemetry, fill=(110, 110, 110))
            draw.text((self.width - 280, bottom_y + 20), "OFFLINE VERIFIED", font=self.font_telemetry, fill=(5, 150, 105))

            bottom_y = self.height - 240
            draw.line([(80, bottom_y), (self.width - 80, bottom_y)], fill=(225, 225, 218), width=1)
            draw.text((80, bottom_y + 20), "COMPLEXITY: O(1 · T_mem) [PARALLEL GEMM VERIFICATION]", font=self.font_telemetry, fill=(110, 110, 110))
            draw.text((self.width - 280, bottom_y + 20), "OFFLINE VERIFIED", font=self.font_telemetry, fill=(5, 150, 105))

        return img

    def render_diagram_clip(
        self,
        output_path: Path | str,
        duration_seconds: float = 6.0,
        topic_header: str = "SPECULATIVE VERIFICATION TREE",
        sub_header: str = "Draft Model Emits K=4 Tokens; Target Model Verifies in 1 Parallel Pass",
        telemetry: str = "REJECTION SAMPLING: min(1, p/q) // EXACT PROBABILITY MATCH // P=1.0",
        fps: int = 30,
    ) -> Path:
        """Renders the full-screen technical speculative verification animation MP4 clip."""
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        total_frames = max(30, int(duration_seconds * fps))

        cmd = [
            "ffmpeg", "-y",
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "-s", f"{self.width}x{self.height}",
            "-r", str(fps),
            "-i", "-",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "19",
            "-pix_fmt", "yuv420p",
            "-t", f"{duration_seconds:.2f}",
            "-an",
            str(out_p),
        ]

        logger.info(f"Rendering technical speculative diagram flow ({total_frames} frames, {duration_seconds:.2f}s) -> {out_p.name}")
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        try:
            for f_idx in range(total_frames):
                frame_img = self.render_frame(
                    frame_idx=f_idx,
                    total_frames=total_frames,
                    topic_header=topic_header,
                    sub_header=sub_header,
                    telemetry=telemetry,
                )
                proc.stdin.write(frame_img.tobytes())

            proc.stdin.close()
            stderr = proc.stderr.read().decode("utf-8", errors="ignore")
            proc.wait()

            if proc.returncode != 0 or not out_p.exists() or out_p.stat().st_size < 1000:
                raise RuntimeError(f"Technical animation render failed: {stderr[:300]}")

            logger.info(f"Technical speculative diagram clip generated: {out_p.name} ({out_p.stat().st_size} bytes)")
            return out_p
        except Exception as e:
            if proc.poll() is None:
                proc.kill()
            raise RuntimeError(f"Technical animation error: {e}") from e
