"""
SUPER.INTELLIGENCEEE — Phase 3.5 Full-Bleed Software & Terminal Demonstrator
Renders edge-to-edge authentic developer CLI environments:
- Real command typing with blinking cursor
- Live engine initialization & CUDA graph compilation
- Animated streaming progress bar and live throughput counter distributed across 95% of frames
- Formatted ASCII benchmark table and continuous bottom stream telemetry
Guarantees continuous visual progression and zero static holds (< 0.5s).
"""

from __future__ import annotations

import logging
import math
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from creative.tech_documentary.motion_primitives import draw_open_hairline

logger = logging.getLogger("super_intelligence.terminal_animator")


class TerminalAnimator:
    """Renders authentic full-bleed developer CLI environments to vertical 1080x1920 MP4."""

    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self._init_fonts()

    def _init_fonts(self) -> None:
        font_dir = Path("C:/Windows/Fonts")
        consola_path = font_dir / "consola.ttf"
        consolab_path = font_dir / "consolab.ttf"
        arialbd_path = font_dir / "arialbd.ttf"

        try:
            self.font_code = ImageFont.truetype(str(consolab_path), 30) if consolab_path.exists() else ImageFont.load_default()
            self.font_code_bold = ImageFont.truetype(str(consolab_path), 32) if consolab_path.exists() else self.font_code
            self.font_header = ImageFont.truetype(str(arialbd_path), 54) if arialbd_path.exists() else ImageFont.load_default()
            self.font_badge = ImageFont.truetype(str(consolab_path), 26) if consolab_path.exists() else ImageFont.load_default()
            self.font_status = ImageFont.truetype(str(consola_path), 24) if consola_path.exists() else ImageFont.load_default()
        except Exception:
            self.font_code = ImageFont.load_default()
            self.font_code_bold = self.font_code
            self.font_header = self.font_code
            self.font_badge = self.font_code
            self.font_status = self.font_code

    def render_frame(
        self,
        frame_idx: int,
        total_frames: int,
        command: str = "vllm serve Llama-3-70b --speculative-model Llama-3-8b --spec-tokens 4",
        topic_header: str = "LIVE INFERENCE VERIFICATION",
        sub_header: str = "vLLM Speculative Engine on NVIDIA A100-SXM4-80GB",
        telemetry: str = "CUDA 12.4 | A100-80GB | ACCEPTANCE RATE 78.4% | FP16 PARITY",
    ) -> Image.Image:
        """Renders a single 1080x1920 developer CLI frame in light-first theme with elevated console."""
        img = Image.new("RGB", (self.width, self.height), (247, 247, 242))
        draw = ImageDraw.Draw(img)

        # Subtle vertical grid lines with scanning highlight
        scan_x = 80 + int((frame_idx * 5) % (self.width - 160))
        for gx in range(80, self.width, 180):
            line_col = (222, 226, 235) if abs(gx - scan_x) < 40 else (235, 235, 228)
            draw.line([(gx, 140), (gx, self.height - 240)], fill=line_col, width=1)

        # 2. Editorial Top Header
        top_y = 150
        draw.line([(80, top_y), (self.width - 80, top_y)], fill=(49, 92, 255), width=2)
        draw.text((80, top_y + 16), "// SUPER.INTELLIGENCEEE  |  SOFTWARE VERIFICATION", font=self.font_badge, fill=(49, 92, 255))
        draw.text((self.width - 340, top_y + 16), "LIVE REPRODUCIBLE CLI", font=self.font_badge, fill=(120, 120, 120))
        draw.text((80, top_y + 54), topic_header[:36].upper(), font=self.font_header, fill=(21, 21, 21))

        # 3. Appropriately Sized Developer Terminal Console (H=880px, Y=270 to 1150)
        term_x = 60
        term_y = 270
        term_w = self.width - 120
        term_h = 880
        corner_r = 8

        draw.rounded_rectangle(
            [(term_x, term_y), (term_x + term_w, term_y + term_h)],
            radius=corner_r,
            fill=(18, 21, 28),
            outline=(195, 200, 208),
            width=2,
        )

        titlebar_h = 52
        draw.rounded_rectangle(
            [(term_x, term_y), (term_x + term_w, term_y + titlebar_h)],
            radius=corner_r,
            fill=(235, 237, 240),
        )
        draw.rectangle([(term_x, term_y + titlebar_h - 10), (term_x + term_w, term_y + titlebar_h)], fill=(235, 237, 240))
        draw.line([(term_x, term_y + titlebar_h), (term_x + term_w, term_y + titlebar_h)], fill=(205, 208, 215), width=1)

        btn_y = term_y + 26
        draw.ellipse([(term_x + 22, btn_y - 8), (term_x + 38, btn_y + 8)], fill=(255, 95, 86))
        draw.ellipse([(term_x + 48, btn_y - 8), (term_x + 64, btn_y + 8)], fill=(255, 189, 46))
        draw.ellipse([(term_x + 74, btn_y - 8), (term_x + 90, btn_y + 8)], fill=(39, 201, 63))

        cpu_pct = int(48 + 12 * math.sin(frame_idx * 0.35))
        gpu_pct = int(88 + 4 * math.cos(frame_idx * 0.28))
        tab_title = f"zsh — a100-hbm-01 // vllm-speculative [CPU: {cpu_pct}% | GPU: {gpu_pct}%]"
        draw.text((term_x + 115, term_y + 16), tab_title, font=self.font_status, fill=(70, 75, 85))

        # 4. Two-Phase Execution Timing Inside Terminal
        content_x = term_x + 36
        content_y = term_y + titlebar_h + 30

        frame_split = int(total_frames * 0.38)
        is_phase_a = frame_idx < frame_split

        typing_frames = max(12, int(frame_split * 0.60))
        chars_to_show = min(len(command), int(len(command) * (frame_idx / typing_frames))) if typing_frames > 0 else len(command)
        current_typed = command[:chars_to_show]

        draw.text((content_x, content_y), "❯ ", font=self.font_code_bold, fill=(5, 150, 105))
        draw.text((content_x + 36, content_y), current_typed, font=self.font_code, fill=(240, 248, 255))

        # Blinking cursor on command prompt
        show_cursor = (frame_idx // 10) % 2 == 0
        cursor_x = content_x + 36 + (len(current_typed) * 17.5)
        if show_cursor and (chars_to_show < len(command) or is_phase_a):
            draw.rectangle([(cursor_x, content_y + 2), (cursor_x + 14, content_y + 32)], fill=(5, 150, 105))

        output_y = content_y + 60

        if is_phase_a:
            # ─── PHASE A: ENGINE INIT & CUDA GRAPH CAPTURE ───
            phase_a_prog = max(0.0, min(1.0, (frame_idx - typing_frames) / max(1, frame_split - typing_frames)))
            phase_a_lines = [
                "[1/3] Loading target model: Llama-3-70B (FP16)...",
                "[INFO] 70B weights pinned in VRAM (134.4 GB)",
                "[2/3] Loading draft model: Llama-3-8B (FP16)...",
                "[INFO] Draft pinned (15.2 GB) // K=4 speculative heads",
                "[3/3] Capturing CUDA graph for rejection sampling...",
                "[READY] vLLM Speculative Engine active. Generating...",
            ]
            vis_lines = min(len(phase_a_lines), int(len(phase_a_lines) * phase_a_prog) + 1)
            for i in range(vis_lines):
                l_str = phase_a_lines[i]
                ly = output_y + (i * 48)
                l_col = (0, 255, 140) if "[READY]" in l_str else (255, 195, 50) if "[1/3]" in l_str or "[2/3]" in l_str or "[3/3]" in l_str else (0, 210, 255)
                draw.text((content_x, ly), l_str, font=self.font_code, fill=l_col)

        else:
            # ─── PHASE B: LIVE SPECULATIVE BENCHMARK RUN (Progression through 95% of frames) ───
            rel_idx = frame_idx - frame_split
            rem_frames = total_frames - frame_split
            phase_b_prog = min(1.0, rel_idx / max(1, rem_frames * 0.95))

            tok_fluct = int(math.sin(frame_idx * 0.35) * 4)
            current_tok_speed = max(30, int(98.4 * phase_b_prog) + tok_fluct)

            full_lines = [
                "[INFO] Pinned 70B Target + 8B Draft in High-Bandwidth Memory",
                "[INFO] K=4 Speculative Branches Emitted per Forward Step",
                f"Speculative Stream: [{'█' * int(18 * phase_b_prog)}{'░' * (18 - int(18 * phase_b_prog))}] {int(100 * phase_b_prog)}%",
                f"Throughput: {current_tok_speed} tok/s  |  Draft Acceptance: 78.4%",
                "• Generation Speed:  30.6 tok/s ──► 98.4 tok/s (+321%) ✔",
                "• Per-Token Latency: 32.7 ms    ──► 10.2 ms    (-68.8%) ✔",
                "• Reasoning Parity:  100% Match (GSM8K: 92.4% / MMLU: 86.7%)",
                "✔ Provably exact output: Leviathan et al. Rejection Theorem",
            ]

            vis_count = min(len(full_lines), 4 + int((len(full_lines) - 4) * min(1.0, phase_b_prog * 1.3)))
            for i in range(vis_count):
                l_str = full_lines[i]
                ly = output_y + (i * 48)
                if "✔" in l_str:
                    l_col = (0, 255, 140)
                elif "Speculative Stream:" in l_str or "Throughput:" in l_str:
                    l_col = (0, 255, 140) if phase_b_prog >= 0.95 else (0, 210, 255)
                elif "[INFO]" in l_str:
                    l_col = (255, 195, 50)
                else:
                    l_col = (230, 235, 245)
                draw.text((content_x, ly), l_str, font=self.font_code, fill=l_col)

        # 5. Dedicated Hardware Telemetry Plate Below Terminal (Y = 1200 to 1660)
        telem_y = 1200
        draw_open_hairline(draw, telem_y, 80, self.width - 80, color=(5, 150, 105), width=2, label="02 / LIVE RUNTIME TELEMETRY")
        draw.text((80, telem_y + 26), "VLLM SPECULATIVE INFERENCE RUNTIME", font=self.font_header, fill=(21, 21, 21))

        # Two-Column Hardware Metrics
        col_y = telem_y + 86
        draw.line([(540, col_y), (540, col_y + 140)], fill=(225, 225, 218), width=1)

        draw.text((80, col_y), "GPU TENSOR CORE UTILIZATION", font=self.font_badge, fill=(5, 150, 105))
        draw.text((80, col_y + 36), "94.2% ACTIVE", font=self.font_header, fill=(5, 150, 105))
        draw.text((80, col_y + 100), "Arithmetic Intensity: > 35 FLOP/byte", font=self.font_status, fill=(70, 70, 70))

        draw.text((560, col_y), "EFFICIENCY ACCELERATION", font=self.font_badge, fill=(49, 92, 255))
        draw.text((560, col_y + 36), "3.2x SPEEDUP", font=self.font_header, fill=(49, 92, 255))
        draw.text((560, col_y + 100), "0.000 Perplexity Drift (p=1.000)", font=self.font_status, fill=(70, 70, 70))

        # Active Oscilloscope Sparkline at Y = 1480
        spark_y = 1500
        draw.line([(80, spark_y), (self.width - 80, spark_y)], fill=(220, 235, 225), width=1)
        for sx in range(80, self.width - 80, 8):
            sh = int(14 + 10 * math.sin((sx * 0.05) + (frame_idx * 0.28)))
            draw.line([(sx, spark_y), (sx, spark_y - sh)], fill=(5, 150, 105), width=2)

        draw.text((80, spark_y + 18), "K=4 SPECULATIVE HEADS // 78.4% MEAN ACCEPTANCE RATE", font=self.font_badge, fill=(49, 92, 255))
        draw.text((80, spark_y + 54), "REPRODUCIBLE PRODUCTION INFERENCE // NVIDIA A100-80GB", font=self.font_badge, fill=(5, 150, 105))

        # Bottom Academic Citation
        bottom_y = self.height - 240
        draw.line([(80, bottom_y), (self.width - 80, bottom_y)], fill=(225, 225, 218), width=1)
        draw.text((80, bottom_y + 20), "OFFLINE RESEARCH PROOF // SUPER.INTELLIGENCEEE // 2026", font=self.font_status, fill=(110, 110, 110))
        draw.text((self.width - 280, bottom_y + 20), "OFFLINE VERIFIED", font=self.font_status, fill=(5, 150, 105))

        return img

    def render_terminal_clip(
        self,
        output_path: Path | str,
        command: str = "vllm serve Llama-3-70b --speculative-model Llama-3-8b --spec-tokens 4",
        duration_seconds: float = 6.0,
        topic_header: str = "LIVE INFERENCE VERIFICATION",
        sub_header: str = "vLLM Speculative Engine on NVIDIA A100-SXM4-80GB",
        telemetry: str = "CUDA 12.4 | A100-80GB | ACCEPTANCE RATE 78.4% | FP16 PARITY",
        fps: int = 30,
    ) -> Path:
        """Renders the full-screen terminal CLI MP4 clip via FFmpeg rawvideo pipe."""
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

        logger.info(f"Rendering full-screen developer terminal ({total_frames} frames, {duration_seconds:.2f}s) -> {out_p.name}")
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        try:
            for f_idx in range(total_frames):
                frame_img = self.render_frame(
                    frame_idx=f_idx,
                    total_frames=total_frames,
                    command=command,
                    topic_header=topic_header,
                    sub_header=sub_header,
                    telemetry=telemetry,
                )
                proc.stdin.write(frame_img.tobytes())

            proc.stdin.close()
            stderr = proc.stderr.read().decode("utf-8", errors="ignore")
            proc.wait()

            if proc.returncode != 0 or not out_p.exists() or out_p.stat().st_size < 1000:
                raise RuntimeError(f"Terminal animation render failed: {stderr[:300]}")

            logger.info(f"Developer terminal clip generated: {out_p.name} ({out_p.stat().st_size} bytes)")
            return out_p
        except Exception as e:
            if proc.poll() is None:
                proc.kill()
            raise RuntimeError(f"Terminal animation error: {e}") from e
