"""
SUPER.INTELLIGENCEEE — Caption Generator Module
Generates SRT, VTT, ASS, and JSON captions formatted specifically for 1080x1920 vertical Reels.
Adheres to mobile safe areas (protects top 200px and bottom 250px).
"""

from __future__ import annotations

import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.config import get_config

logger = logging.getLogger("super_intelligence.captions")


class CaptionGenerator:
    """Generates subtitle tracks (SRT, VTT, ASS, JSON) synchronized to storyboard scenes."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.safe_margin_bottom = 280  # Pixels from bottom on 1920h canvas
        self.safe_margin_top = 220     # Pixels from top on 1920h canvas
        self.words_per_second = 2.5    # Average speaking rate

    def format_timestamp_srt(self, seconds: float) -> str:
        """Formats seconds into SRT format: 00:00:00,000"""
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milli = int(round((seconds - int(seconds)) * 1000))
        if milli >= 1000:
            secs += 1
            milli = 0
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{milli:03d}"

    def format_timestamp_vtt(self, seconds: float) -> str:
        """Formats seconds into VTT format: 00:00:00.000"""
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milli = int(round((seconds - int(seconds)) * 1000))
        if milli >= 1000:
            secs += 1
            milli = 0
        return f"{hrs:02d}:{mins:02d}:{secs:02d}.{milli:03d}"

    def format_timestamp_ass(self, seconds: float) -> str:
        """Formats seconds into ASS format: 0:00:00.00"""
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        cs = int(round((seconds - int(seconds)) * 100))
        if cs >= 100:
            secs += 1
            cs = 0
        return f"{hrs}:{mins:02d}:{secs:02d}.{cs:02d}"

    def chunk_narration_into_lines(self, text: str, max_words: int = 5) -> List[str]:
        """Splits scene text into punchy short lines suitable for vertical video screens."""
        words = text.strip().split()
        if not words:
            return []

        chunks = []
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i:i + max_words])
            chunks.append(chunk)
        return chunks

    def generate_captions_from_storyboard(
        self,
        storyboard: Dict[str, Any],
        output_dir: Path | str,
        base_name: str = "reel_captions",
    ) -> Dict[str, Path]:
        """
        Builds synchronized SRT, VTT, ASS, and JSON files from storyboard scene timings.
        """
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        scenes = storyboard.get("scenes", [])
        if not scenes:
            logger.warning("Storyboard has no scenes; creating empty subtitle set.")

        caption_items = []
        current_time = 0.0

        for sc in scenes:
            duration = float(sc.get("duration", 5.0))
            text = sc.get("narration_text", sc.get("voiceover", "")).strip()

            chunks = self.chunk_narration_into_lines(text, max_words=4)
            if not chunks:
                current_time += duration
                continue

            chunk_duration = duration / len(chunks)
            chunk_start = current_time

            for c in chunks:
                chunk_end = chunk_start + chunk_duration
                caption_items.append({
                    "start": round(chunk_start, 3),
                    "end": round(chunk_end, 3),
                    "text": c.upper(),  # High-energy bold caps for tech reels
                })
                chunk_start = chunk_end

            current_time += duration

        # 1. Generate SRT
        srt_path = out_dir / f"{base_name}.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            for idx, item in enumerate(caption_items, start=1):
                start_str = self.format_timestamp_srt(item["start"])
                end_str = self.format_timestamp_srt(item["end"])
                f.write(f"{idx}\n{start_str} --> {end_str}\n{item['text']}\n\n")

        # 2. Generate VTT
        vtt_path = out_dir / f"{base_name}.vtt"
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for idx, item in enumerate(caption_items, start=1):
                start_str = self.format_timestamp_vtt(item["start"])
                end_str = self.format_timestamp_vtt(item["end"])
                f.write(f"{idx}\n{start_str} --> {end_str}\n{item['text']}\n\n")

        # 3. Generate ASS (Advanced SubStation Alpha with yellow punch typography)
        # MarginV: 340 pushes text above the Instagram bottom tray
        ass_path = out_dir / f"{base_name}.ass"
        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(
                "[Script Info]\n"
                "Title: SUPER.INTELLIGENCEEE Reel Captions\n"
                "ScriptType: v4.00+\n"
                "PlayResX: 1080\n"
                "PlayResY: 1920\n\n"
                "[V4+ Styles]\n"
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                "Style: Default,Arial Black,58,&H0000E5FF,&H00000000,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,5,3,2,60,60,340,1\n\n"
                "[Events]\n"
                "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            )
            for item in caption_items:
                start_ass = self.format_timestamp_ass(item["start"])
                end_ass = self.format_timestamp_ass(item["end"])
                clean_text = item["text"].replace("\n", " ")
                f.write(f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{clean_text}\n")

        # 4. Generate JSON for DOM / HyperFrames overlay
        json_path = out_dir / f"{base_name}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "meta": {
                    "total_captions": len(caption_items),
                    "total_duration": round(current_time, 2),
                },
                "captions": caption_items
            }, f, indent=2)

        logger.info(f"Generated captions: SRT ({srt_path.name}), VTT ({vtt_path.name}), ASS ({ass_path.name})")

        return {
            "srt": srt_path,
            "vtt": vtt_path,
            "ass": ass_path,
            "json": json_path,
        }

