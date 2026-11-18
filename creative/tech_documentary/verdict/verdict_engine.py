"""
SUPER.INTELLIGENCEEE — Phase 3.5 Executive Verdict & Synthesis Engine
Renders a broadcast-grade full-screen architectural conclusion and synthesis plate:
- Staggered section reveals distributed across 0% to 90% of scene duration
- Active sweeping verification beam across hairline dividers
- Pulsing verification stamp box and traveling status packet
Guarantees continuous visual change and zero static holds (< 0.5s).
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
    harmonic_spring,
    smooth_step,
    cubic_ease_out,
)

logger = logging.getLogger("super_intelligence.verdict_engine")


class VerdictEngine:
    """Renders full-screen executive verdict, takeaways, and deployment decision plates."""

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
            self.font_title = ImageFont.truetype(str(arialbd_path), 60) if arialbd_path.exists() else ImageFont.load_default()
            self.font_sub = ImageFont.truetype(str(arial_path), 34) if arial_path.exists() else ImageFont.load_default()
            self.font_card_title = ImageFont.truetype(str(arialbd_path), 38) if arialbd_path.exists() else ImageFont.load_default()
            self.font_body = ImageFont.truetype(str(arial_path), 32) if arial_path.exists() else ImageFont.load_default()
            self.font_badge = ImageFont.truetype(str(consolab_path), 28) if consolab_path.exists() else ImageFont.load_default()
            self.font_telemetry = ImageFont.truetype(str(consola_path), 24) if consola_path.exists() else ImageFont.load_default()
        except Exception:
            self.font_title = ImageFont.load_default()
            self.font_sub = self.font_title
            self.font_card_title = self.font_title
            self.font_body = self.font_title
            self.font_badge = self.font_title
            self.font_telemetry = self.font_title

    def render_frame(
        self,
        frame_idx: int,
        total_frames: int,
        topic_header: str = "THE SPECULATIVE INFERENCE VERDICT",
        sub_header: str = "Architectural Synthesis on Draft-Verifier Decoding",
        telemetry: str = "SYSTEMS SUMMARY: EXACT TARGET DISTRIBUTION // 3.2X SPEEDUP",
    ) -> Image.Image:
        """Renders an edge-to-edge executive verdict frame with continuous kinetic progression."""
        img = Image.new("RGB", (self.width, self.height), (247, 247, 242))
        draw = ImageDraw.Draw(img)

        # 1. Subtle vertical grid lines
        for gx in range(80, self.width, 180):
            draw.line([(gx, 140), (gx, self.height - 240)], fill=(235, 235, 228), width=1)

        # 2. Editorial Top Header
        top_y = 150
        draw.line([(80, top_y), (self.width - 80, top_y)], fill=(49, 92, 255), width=2)
        draw.text((80, top_y + 16), "// SUPER.INTELLIGENCEEE  |  ARCHITECTURAL VERDICT", font=self.font_badge, fill=(49, 92, 255))
        draw.text((self.width - 320, top_y + 16), "PRODUCTION MANDATE", font=self.font_badge, fill=(120, 120, 120))

        draw.text((80, top_y + 56), topic_header[:36].upper(), font=self.font_title, fill=(21, 21, 21))
        draw.text((80, top_y + 120), sub_header[:60], font=self.font_sub, fill=(85, 85, 85))

        # Staggered Timeline Progression across entire duration (eliminates late-scene static freeze)
        prog_sec1 = min(1.0, frame_idx / max(1, total_frames * 0.28))
        prog_sec2 = min(1.0, max(0.0, (frame_idx - total_frames * 0.22) / max(1, total_frames * 0.30)))
        prog_sec3 = min(1.0, max(0.0, (frame_idx - total_frames * 0.48) / max(1, total_frames * 0.30)))
        prog_stamp = min(1.0, max(0.0, (frame_idx - total_frames * 0.72) / max(1, total_frames * 0.22)))

        # Continuous moving verification beam along divider hairlines
        beam_x = 80 + int((frame_idx * 15) % (self.width - 160))

        # 3. SECTION 1: THE CORE FINDING (Enters 0% - 28%)
        if prog_sec1 > 0.05:
            sec1_y = 320
            draw_open_hairline(draw, sec1_y, 80, self.width - 80, color=(5, 150, 105), width=2, label="01 / EMPIRICAL CORE FINDING")
            draw.line([(beam_x, sec1_y), (min(self.width - 80, beam_x + 40), sec1_y)], fill=(90, 230, 160), width=3)

            draw.text((80, sec1_y + 26), "SERIAL AUTOREGRESSIVE DECODING IS OBSOLETE", font=self.font_card_title, fill=(5, 150, 105))
            draw.text((80, sec1_y + 76), "Draft-verifier speculative decoding delivers 3.2x throughput acceleration", font=self.font_body, fill=(25, 25, 25))
            draw.text((80, sec1_y + 118), "by shifting inference from memory-bandwidth bound to parallel GEMM compute.", font=self.font_body, fill=(25, 25, 25))

            ind_y = sec1_y + 172
            draw.text((80, ind_y), "• THROUGHPUT: 98.4 tok/s (+321.6% acceleration)", font=self.font_badge, fill=(5, 150, 105))
            draw.text((80, ind_y + 44), "• LATENCY DROP: 10.2 ms vs 32.7 ms per token (-68.8%)", font=self.font_badge, fill=(49, 92, 255))
            draw.text((80, ind_y + 88), "• MATHEMATICAL PARITY: 0.000 PERPLEXITY DELTA (p=1.000)", font=self.font_badge, fill=(121, 86, 232))

        # 4. SECTION 2: EXPLICIT LIMITATION & HYBRID TRADE-OFF (Enters 22% - 52%)
        if prog_sec2 > 0.05:
            sec2_y = 690
            draw_open_hairline(draw, sec2_y, 80, self.width - 80, color=(235, 120, 20), width=2, label="02 / ENGINEERING TRADE-OFF & BOUNDARIES")
            draw.line([(beam_x, sec2_y), (min(self.width - 80, beam_x + 40), sec2_y)], fill=(255, 180, 80), width=3)

            draw.text((80, sec2_y + 26), "DRAFT MODEL CONVERGENCE & MEMORY OVERHEAD", font=self.font_card_title, fill=(235, 120, 20))
            draw.text((80, sec2_y + 76), "1. Acceptance Degradation: On high sampling temp (> 1.2), draft acc drops to 54%.", font=self.font_body, fill=(25, 25, 25))
            draw.text((80, sec2_y + 118), "2. VRAM Allocation: Keeping draft model pinned consumes ~15 GB VRAM in memory.", font=self.font_body, fill=(25, 25, 25))
            draw.text((80, sec2_y + 160), "3. Optimal Workloads: Dominates in code generation, mathematics, and structured JSON.", font=self.font_body, fill=(25, 25, 25))

        # 5. SECTION 3: DEFINITIVE DEPLOYMENT DECISION (Enters 48% - 78%)
        if prog_sec3 > 0.05:
            sec3_y = 1010
            draw_open_hairline(draw, sec3_y, 80, self.width - 80, color=(49, 92, 255), width=2, label="03 / PRODUCTION DEPLOYMENT MANDATE")
            draw.line([(beam_x, sec3_y), (min(self.width - 80, beam_x + 40), sec3_y)], fill=(120, 180, 255), width=3)

            draw.text((80, sec3_y + 26), "MANDATE SPECULATIVE ENGINES IN ALL PRODUCTION LLM SERVING", font=self.font_card_title, fill=(49, 92, 255))

            rec_y = sec3_y + 78
            draw.text((80, rec_y), "✔ Standard Batch-1 Serving:", font=self.font_badge, fill=(5, 150, 105))
            draw.text((490, rec_y), "MANDATORY (vLLM / TensorRT-LLM / SGLang)", font=self.font_badge, fill=(21, 21, 21))

            rec_y += 48
            draw.text((80, rec_y), "✔ Draft Architecture:", font=self.font_badge, fill=(49, 92, 255))
            draw.text((490, rec_y), "Pair 70B with 8B draft or Medusa multi-heads", font=self.font_badge, fill=(21, 21, 21))

            rec_y += 48
            draw.text((80, rec_y), "✔ Target Silicon:", font=self.font_badge, fill=(121, 86, 232))
            draw.text((490, rec_y), "NVIDIA A100 / H100 SXM5 / B200 Systems", font=self.font_badge, fill=(21, 21, 21))

        # 6. Continuous Pulsing Verification Stamp Box (Enters 72% - 100%, Spans Y = 1320 to 1620)
        stamp_y = 1320
        draw.line([(80, stamp_y), (self.width - 80, stamp_y)], fill=(225, 225, 218), width=1)

        stamp_box = (80, stamp_y + 25, self.width - 80, stamp_y + 155)
        pulse_val = int(235 + 12 * math.sin(frame_idx * 0.35))
        draw.rectangle(stamp_box, fill=(pulse_val, 248, 242), outline=(5, 150, 105), width=3)

        # Traveling verification beam inside stamp box
        dot_x = 90 + int((frame_idx * 24) % (self.width - 200))
        draw.rectangle([(dot_x, stamp_y + 28), (dot_x + 45, stamp_y + 152)], fill=(210, 245, 225))
        draw.ellipse([(dot_x + 12, stamp_y + 90 - 12), (dot_x + 32, stamp_y + 90 + 12)], fill=(5, 150, 105))

        draw.text((105, stamp_y + 44), "VERIFIED MANDATE: SPECULATIVE DECODING DELIVERS 3.2X SPEEDUP", font=self.font_card_title, fill=(5, 150, 105))
        draw.text((105, stamp_y + 96), "PROVABLY IDENTICAL TOKEN DISTRIBUTION // ZERO COMPUTE SACRIFICE // EXACT p=1.000", font=self.font_badge, fill=(40, 120, 80))

        # Bottom Academic Citation with moving status packet
        bottom_y = self.height - 240
        draw.line([(80, bottom_y), (self.width - 80, bottom_y)], fill=(225, 225, 218), width=1)
        draw.line([(beam_x, bottom_y), (min(self.width - 80, beam_x + 30), bottom_y)], fill=(5, 150, 105), width=2)
        draw.text((80, bottom_y + 20), "OFFLINE RESEARCH DOSSIER // SUPER.INTELLIGENCEEE // 2026", font=self.font_telemetry, fill=(110, 110, 110))
        draw.text((self.width - 280, bottom_y + 20), "OFFLINE VERIFIED", font=self.font_telemetry, fill=(5, 150, 105))

        return img

    def render_verdict_clip(
        self,
        output_path: Path | str,
        duration_seconds: float = 6.0,
        topic_header: str = "THE SPECULATIVE INFERENCE VERDICT",
        sub_header: str = "Architectural Synthesis on Draft-Verifier Decoding",
        telemetry: str = "SYSTEMS SUMMARY: EXACT TARGET DISTRIBUTION // 3.2X SPEEDUP",
        fps: int = 30,
    ) -> Path:
        """Renders the full-screen executive verdict plate to vertical MP4."""
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

        logger.info(f"Rendering full-screen executive verdict plate ({total_frames} frames, {duration_seconds:.2f}s) -> {out_p.name}")
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
                raise RuntimeError(f"Verdict plate render failed: {stderr[:300]}")

            logger.info(f"Executive verdict plate clip generated: {out_p.name} ({out_p.stat().st_size} bytes)")
            return out_p
        except Exception as e:
            if proc.poll() is None:
                proc.kill()
            raise RuntimeError(f"Verdict plate render error: {e}") from e
