"""
SUPER.INTELLIGENCEEE — Phase 3.5 Editorial Kinetic Typography Engine
Renders broadcast-grade, full-screen editorial kinetic motion design with:
- True staggered word-by-word typography reveals (word-level opacity fade + spring slide)
- Parameterized Phase A (Problem / Bottleneck) and Phase B (Breakthrough / Metric)
- Continuous active background tracking & grid pulse (zero static holds)
- Light-first Swiss editorial design standards
"""

from __future__ import annotations

import logging
import math
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger("super_intelligence.kinetic_engine")


class KineticTypographyEngine:
    """Full-screen editorial kinetic typography generator with staggered word reveals."""

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
            self.font_super = ImageFont.truetype(str(arialbd_path), 88) if arialbd_path.exists() else ImageFont.load_default()
            self.font_hero = ImageFont.truetype(str(arialbd_path), 72) if arialbd_path.exists() else ImageFont.load_default()
            self.font_stat_hero = ImageFont.truetype(str(consolab_path), 130) if consolab_path.exists() else ImageFont.load_default()
            self.font_sub = ImageFont.truetype(str(arial_path), 36) if arial_path.exists() else ImageFont.load_default()
            self.font_badge = ImageFont.truetype(str(consolab_path), 26) if consolab_path.exists() else ImageFont.load_default()
            self.font_citation = ImageFont.truetype(str(consola_path), 24) if consola_path.exists() else ImageFont.load_default()
        except Exception:
            self.font_super = ImageFont.load_default()
            self.font_hero = self.font_super
            self.font_stat_hero = self.font_super
            self.font_sub = self.font_super
            self.font_badge = self.font_super
            self.font_citation = self.font_super

    def _spring_scale(self, progress: float) -> float:
        """Damped harmonic oscillator spring easing."""
        if progress <= 0.0:
            return 0.0
        if progress >= 1.0:
            return 1.0
        return 1.0 - math.exp(-6.5 * progress) * math.cos(7.5 * progress)

    def _blend_color(self, fg: Tuple[int, int, int], bg: Tuple[int, int, int], alpha: float) -> Tuple[int, int, int]:
        """Blends foreground color with background canvas based on alpha factor (0.0 to 1.0)."""
        a = max(0.0, min(1.0, alpha))
        return (
            int(bg[0] * (1.0 - a) + fg[0] * a),
            int(bg[1] * (1.0 - a) + fg[1] * a),
            int(bg[2] * (1.0 - a) + fg[2] * a),
        )

    def render_staggered_text(
        self,
        draw: ImageDraw.Draw,
        text: str,
        start_x: int,
        start_y: int,
        progress: float,
        font: ImageFont.ImageFont,
        base_color: Tuple[int, int, int],
        bg_color: Tuple[int, int, int] = (247, 247, 242),
        highlight_word: str = "",
        highlight_color: Tuple[int, int, int] = (49, 92, 255),
        max_line_width: int = 920,
        line_height: int = 82,
        stagger_delay: float = 0.07,
    ) -> int:
        """
        Renders words with individual staggered spring entrances and alpha fades.
        Returns final y coordinate after all rendered lines.
        """
        raw_words = text.split()
        if not raw_words:
            return start_y

        # Word wrap into lines
        lines: List[List[str]] = []
        curr_line: List[str] = []
        curr_w = 0.0
        space_w = draw.textlength(" ", font=font)

        for w in raw_words:
            w_len = draw.textlength(w, font=font)
            if curr_w + w_len > max_line_width and curr_line:
                lines.append(curr_line)
                curr_line = [w]
                curr_w = w_len + space_w
            else:
                curr_line.append(w)
                curr_w += w_len + space_w
        if curr_line:
            lines.append(curr_line)

        # Flatten words to calculate sequential stagger indices
        global_word_idx = 0
        total_words = len(raw_words)
        y_pos = start_y

        for line in lines:
            x_pos = start_x
            for word in line:
                # Calculate word animation progression
                w_start = global_word_idx * stagger_delay
                w_dur = 0.35
                w_rel = max(0.0, min(1.0, (progress - w_start) / w_dur))
                w_ease = self._spring_scale(w_rel)

                if w_rel > 0.01:
                    # Staggered slide & alpha fade
                    y_offset = int((1.0 - w_ease) * 14.0)
                    x_offset = int((1.0 - w_ease) * 6.0)
                    alpha = min(1.0, w_rel * 1.5)

                    is_hl = highlight_word and (highlight_word.lower() in word.lower())
                    target_col = highlight_color if is_hl else base_color
                    draw_col = self._blend_color(target_col, bg_color, alpha)

                    draw.text((x_pos + x_offset, y_pos + y_offset), word, font=font, fill=draw_col)

                x_pos += draw.textlength(word + " ", font=font)
                global_word_idx += 1
            y_pos += line_height

        return y_pos

    def render_frame(
        self,
        frame_idx: int,
        total_frames: int,
        primary_text: str = "SPECULATIVE DECODING ACCELERATION",
        highlight_keyword: str = "SPECULATIVE",
        stat_number: Optional[str] = "3.2x",
        sub_text: str = "Draft verifier models break autoregressive memory latency without quality loss.",
        category: str = "SYSTEMS ARCHITECTURE",
        citation: str = "SOURCE: LEVIATHAN ET AL. // FAST INFERENCE VIA SPECULATIVE DECODING",
        problem_headline: str = "THE AUTOREGRESSIVE MEMORY WALL",
        problem_subtext: str = "Sequential token generation is memory-bandwidth bound at batch size 1.",
        stat_label: str = "VERIFIED SPEEDUP MULTIPLIER",
        spec_col1_title: str = "INFERENCE THROUGHPUT",
        spec_col1_val: str = "3.2x Speedup",
        spec_col1_sub: str = "98.4 tok/s vs 30.6 tok/s",
        spec_col2_title: str = "MATHEMATICAL INTEGRITY",
        spec_col2_val: str = "Exact Match (p=1.0)",
        spec_col2_sub: str = "Provably Identical Token Distribution",
    ) -> Image.Image:
        """
        Renders full-bleed editorial kinetic typography with staggered reveals.
        Phase A (0% - 40%): The Engineering Bottleneck / Memory Wall
        Phase B (40% - 100%): The Algorithmic Breakthrough & Metric Benchmark
        """
        # 1. Warm Ivory Canvas with active continuous micro-depth
        img = Image.new("RGB", (self.width, self.height), (247, 247, 242))
        draw = ImageDraw.Draw(img)

        # Continuous subtle ambient pulse so frame delta is NEVER zero
        ambient_lfo = math.sin(frame_idx * 0.08) * 2.0
        mid_y = self.height // 2
        for y in range(0, self.height, 4):
            factor = 1.0 - (abs(y - mid_y) / float(mid_y))
            r = int(245 + (4 * factor) + ambient_lfo)
            g = int(245 + (4 * factor) + ambient_lfo)
            b = int(240 + (5 * factor))
            draw.rectangle([(0, y), (self.width, y + 4)], fill=(r, g, b))

        # Architectural structural hairlines with continuous scanning accent
        scan_x = 80 + int((frame_idx * 5) % (self.width - 160))
        for gx in (80, 260, 440, 620, 800, 1000):
            line_col = (220, 225, 235) if abs(gx - scan_x) < 40 else (234, 234, 228)
            draw.line([(gx, 140), (gx, self.height - 220)], fill=line_col, width=1)

        # Phase split
        frame_split = int(total_frames * 0.40)
        is_phase_a = frame_idx < frame_split

        if is_phase_a:
            # ─── PHASE A: THE ENGINEERING BOTTLENECK ───
            phase_a_prog = frame_idx / max(1, frame_split)
            ease_a = self._spring_scale(min(1.0, phase_a_prog * 1.4))

            # Top Header (Crisis Coral)
            top_y = 150
            draw.line([(80, top_y), (self.width - 80, top_y)], fill=(235, 80, 40), width=2)
            draw.text((80, top_y + 16), "// SUPER.INTELLIGENCEEE  |  ENGINEERING BOTTLENECK", font=self.font_badge, fill=(235, 80, 40))
            draw.text((self.width - 340, top_y + 16), "CRITICAL LIMITATION", font=self.font_badge, fill=(120, 120, 120))

            content_y = 260
            draw.text((95, content_y), "⚠ MEMORY BANDWIDTH SATURATION", font=self.font_badge, fill=(235, 80, 40))
            draw.line([(80, content_y - 4), (90, content_y - 4)], fill=(235, 80, 40), width=2)
            draw.line([(80, content_y - 4), (80, content_y + 26)], fill=(235, 80, 40), width=2)

            # Staggered Word Reveal for Problem Headline
            content_y += 60
            next_y = self.render_staggered_text(
                draw=draw,
                text=problem_headline.upper(),
                start_x=80,
                start_y=content_y,
                progress=phase_a_prog * 1.5,
                font=self.font_hero,
                base_color=(21, 21, 21),
                highlight_word="WALL",
                highlight_color=(235, 80, 40),
                line_height=86,
            )

            # Sub-text with vertical rule
            content_y = next_y + 30
            draw.line([(80, content_y), (80, content_y + 84)], fill=(235, 80, 40), width=4)
            draw.text((100, content_y + 4), problem_subtext[:52], font=self.font_sub, fill=(60, 60, 60))
            if len(problem_subtext) > 52:
                draw.text((100, content_y + 46), problem_subtext[52:115], font=self.font_sub, fill=(90, 90, 90))

            # Dynamic Memory Bandwidth Saturation Meter (Expanded prominent readout)
            meter_y = content_y + 180
            draw.line([(80, meter_y), (self.width - 80, meter_y)], fill=(225, 225, 218), width=1)
            draw.text((80, meter_y + 20), "GPU MEMORY BANDWIDTH SATURATION (HBM3e)", font=self.font_badge, fill=(235, 80, 40))
            draw.text((self.width - 340, meter_y + 20), "ARITHMETIC INTENSITY < 1.0", font=self.font_badge, fill=(120, 120, 120))

            # Active Dynamic Track (Expanded H=54px)
            track_y = meter_y + 70
            track_w = self.width - 160
            vram_fill = int(track_w * 0.92 * min(1.0, ease_a))
            draw.rectangle([(80, track_y), (80 + track_w, track_y + 54)], fill=(240, 240, 238))
            draw.rectangle([(80, track_y), (80 + vram_fill, track_y + 54)], fill=(235, 80, 40))
            # Sweeping scan pulse across track
            pulse_a_x = 80 + int((frame_idx * 16) % max(1, vram_fill))
            draw.rectangle([(pulse_a_x, track_y), (min(80 + vram_fill, pulse_a_x + 36), track_y + 54)], fill=(255, 140, 90))
            draw.text((95, track_y + 14), "92.4% MEMORY BUS BOTTLENECK (IDLE TENSOR CORES)", font=self.font_badge, fill=(255, 255, 255))

            # Two-Column Baseline Readouts (Evenly spaced across lower third Y = 1180 to 1580)
            col_y = track_y + 180
            draw.line([(80, col_y), (self.width - 80, col_y)], fill=(225, 225, 218), width=1)
            draw.line([(540, col_y + 20), (540, col_y + 240)], fill=(225, 225, 218), width=1)

            draw.text((80, col_y + 30), "STANDARD AUTOREGRESSIVE LATENCY", font=self.font_badge, fill=(110, 110, 110))
            draw.text((80, col_y + 74), "30.6 tok/s", font=self.font_hero, fill=(21, 21, 21))
            draw.text((80, col_y + 165), "1 GPU Forward Pass Per Token", font=self.font_sub, fill=(90, 90, 90))
            draw.text((80, col_y + 208), "Zero speculation // Full DRAM fetch", font=self.font_citation, fill=(130, 130, 130))

            draw.text((560, col_y + 30), "GPU COMPUTE EFFICIENCY", font=self.font_badge, fill=(235, 80, 40))
            draw.text((560, col_y + 74), "11.2% UTIL", font=self.font_hero, fill=(220, 40, 30))
            draw.text((560, col_y + 165), "Severe Memory Latency Underutilization", font=self.font_sub, fill=(90, 90, 90))
            draw.text((560, col_y + 208), "Compute cores idle waiting on weights", font=self.font_citation, fill=(130, 130, 130))

        else:
            # ─── PHASE B: THE ALGORITHMIC BREAKTHROUGH ───
            rel_idx = frame_idx - frame_split
            rem_frames = total_frames - frame_split
            anim_progress = min(1.0, rel_idx / max(1, rem_frames * 0.40))
            scale_val = self._spring_scale(anim_progress)

            # Top Header (Breakthrough Electric Blue)
            top_y = 150
            draw.line([(80, top_y), (self.width - 80, top_y)], fill=(49, 92, 255), width=2)
            draw.text((80, top_y + 16), f"// SUPER.INTELLIGENCEEE  |  {category.upper()}", font=self.font_badge, fill=(49, 92, 255))
            draw.text((self.width - 340, top_y + 16), "BREAKTHROUGH REPORT", font=self.font_badge, fill=(120, 120, 120))

            content_start_y = 260

            # Massive Hero Number directly on canvas with zero box
            if stat_number:
                import re
                num_match = re.search(r"(\d+(\.\d+)?)", stat_number)
                if num_match:
                    target_val = float(num_match.group(1))
                    curr_val = round(target_val * min(1.0, anim_progress), 1)
                    prefix = stat_number[:num_match.start()]
                    suffix = stat_number[num_match.end():]
                    display_stat = f"{prefix}{curr_val}{suffix}"
                else:
                    display_stat = stat_number

                draw.text((80, content_start_y), display_stat, font=self.font_stat_hero, fill=(5, 150, 105))
                draw.line([(80, content_start_y + 155), (80 + 440, content_start_y + 155)], fill=(5, 150, 105), width=4)
                content_start_y += 185

            # Staggered Word Reveal for Primary Headline
            next_y = self.render_staggered_text(
                draw=draw,
                text=primary_text.upper(),
                start_x=80,
                start_y=content_start_y,
                progress=anim_progress * 1.5,
                font=self.font_hero,
                base_color=(21, 21, 21),
                highlight_word=highlight_keyword,
                highlight_color=(49, 92, 255),
                line_height=86,
            )

            # Sub-text with blue rule
            if sub_text:
                sub_y = next_y + 25
                draw.line([(80, sub_y), (80, sub_y + 78)], fill=(49, 92, 255), width=4)
                draw.text((100, sub_y + 4), sub_text[:50], font=self.font_sub, fill=(60, 60, 60))
                if len(sub_text) > 50:
                    draw.text((100, sub_y + 44), sub_text[50:110], font=self.font_sub, fill=(90, 90, 90))

            # Dynamic Acceleration Progress Track (Evenly spaced in middle canvas Y = 880 to 1120)
            horiz_y = max(880, next_y + 150)
            draw.line([(80, horiz_y), (self.width - 80, horiz_y)], fill=(225, 225, 218), width=1)
            draw.text((80, horiz_y + 20), stat_label.upper(), font=self.font_badge, fill=(49, 92, 255))
            draw.text((self.width - 340, horiz_y + 20), "PARALLEL VERIFICATION", font=self.font_badge, fill=(5, 150, 105))

            hbar_y = horiz_y + 65
            hbar_w = self.width - 160
            draw.rectangle([(80, hbar_y), (80 + int(hbar_w * 0.28), hbar_y + 42)], fill=(220, 224, 230))
            draw.text((95, hbar_y + 10), "BASELINE: 1x (30.6 tok/s)", font=self.font_badge, fill=(90, 100, 115))

            target_w = int(hbar_w * min(1.0, scale_val))
            draw.rectangle([(80, hbar_y + 54), (80 + target_w, hbar_y + 106)], fill=(49, 92, 255))
            # Moving pulse beam along progress bar
            pulse_x = 80 + int((frame_idx * 16) % max(1, target_w))
            draw.rectangle([(pulse_x, hbar_y + 54), (min(80 + target_w, pulse_x + 36), hbar_y + 106)], fill=(90, 210, 255))
            draw.text((100, hbar_y + 68), f"SPECULATIVE SPEC: {stat_number} THROUGHPUT ACCELERATION", font=self.font_badge, fill=(255, 255, 255))

            # Open Two-Column Specifications (Evenly spaced across lower third Y = 1180 to 1580)
            spec_y = hbar_y + 170
            draw.line([(80, spec_y), (self.width - 80, spec_y)], fill=(225, 225, 218), width=1)
            draw.line([(540, spec_y + 20), (540, spec_y + 240)], fill=(225, 225, 218), width=1)

            draw.text((80, spec_y + 25), spec_col1_title.upper(), font=self.font_badge, fill=(5, 150, 105))
            draw.text((80, spec_y + 68), spec_col1_val, font=self.font_hero, fill=(5, 150, 105))
            draw.text((80, spec_y + 158), spec_col1_sub, font=self.font_sub, fill=(40, 40, 40))
            draw.text((80, spec_y + 202), "Single Target GPU Execution", font=self.font_citation, fill=(110, 110, 110))

            draw.text((560, spec_y + 25), spec_col2_title.upper(), font=self.font_badge, fill=(49, 92, 255))
            draw.text((560, spec_y + 68), spec_col2_val, font=self.font_hero, fill=(49, 92, 255))
            draw.text((560, spec_y + 158), spec_col2_sub, font=self.font_sub, fill=(40, 40, 40))
            draw.text((560, spec_y + 202), "Zero Perplexity Degradation", font=self.font_citation, fill=(110, 110, 110))

        # Persistent Bottom Academic Citation
        bottom_rule_y = self.height - 220
        draw.line([(80, bottom_rule_y), (self.width - 80, bottom_rule_y)], fill=(220, 220, 214), width=1)
        draw.text((80, bottom_rule_y + 20), citation.upper(), font=self.font_citation, fill=(110, 110, 110))
        draw.text((self.width - 280, bottom_rule_y + 20), "OFFLINE VERIFIED", font=self.font_citation, fill=(5, 150, 105))

        return img

    def render_kinetic_clip(
        self,
        output_path: Path | str,
        primary_text: str = "SPECULATIVE DECODING ACCELERATION",
        highlight_keyword: str = "SPECULATIVE",
        stat_number: Optional[str] = "3.2x",
        sub_text: str = "Draft verifier models break autoregressive memory latency without quality loss.",
        category: str = "SYSTEMS ARCHITECTURE",
        citation: str = "SOURCE: LEVIATHAN ET AL. // FAST INFERENCE VIA SPECULATIVE DECODING",
        problem_headline: str = "THE AUTOREGRESSIVE MEMORY WALL",
        problem_subtext: str = "Sequential token generation is memory-bandwidth bound at batch size 1.",
        stat_label: str = "VERIFIED SPEEDUP MULTIPLIER",
        spec_col1_title: str = "INFERENCE THROUGHPUT",
        spec_col1_val: str = "3.2x Speedup",
        spec_col1_sub: str = "98.4 tok/s vs 30.6 tok/s",
        spec_col2_title: str = "MATHEMATICAL INTEGRITY",
        spec_col2_val: str = "Exact Match (p=1.0)",
        spec_col2_sub: str = "Provably Identical Token Distribution",
        duration_seconds: float = 5.0,
        fps: int = 30,
    ) -> Path:
        """Renders full-bleed editorial kinetic typography MP4 clip via FFmpeg rawvideo pipe."""
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

        logger.info(f"Rendering staggered kinetic typography ({total_frames} frames, {duration_seconds:.2f}s) -> {out_p.name}")
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        try:
            for f_idx in range(total_frames):
                frame_img = self.render_frame(
                    frame_idx=f_idx,
                    total_frames=total_frames,
                    primary_text=primary_text,
                    highlight_keyword=highlight_keyword,
                    stat_number=stat_number,
                    sub_text=sub_text,
                    category=category,
                    citation=citation,
                    problem_headline=problem_headline,
                    problem_subtext=problem_subtext,
                    stat_label=stat_label,
                    spec_col1_title=spec_col1_title,
                    spec_col1_val=spec_col1_val,
                    spec_col1_sub=spec_col1_sub,
                    spec_col2_title=spec_col2_title,
                    spec_col2_val=spec_col2_val,
                    spec_col2_sub=spec_col2_sub,
                )
                proc.stdin.write(frame_img.tobytes())

            proc.stdin.close()
            stderr = proc.stderr.read().decode("utf-8", errors="ignore")
            proc.wait()

            if proc.returncode != 0 or not out_p.exists() or out_p.stat().st_size < 1000:
                raise RuntimeError(f"Kinetic typography render failed (code {proc.returncode}): {stderr[:300]}")

            logger.info(f"Staggered kinetic typography clip complete: {out_p.name} ({out_p.stat().st_size} bytes)")
            return out_p
        except Exception as e:
            if proc.poll() is None:
                proc.kill()
            raise RuntimeError(f"Kinetic typography error: {e}") from e
