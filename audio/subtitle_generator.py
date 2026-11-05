import re
from typing import List, Dict, Any
from pathlib import Path

class SubtitleGenerator:
    """Generates mobile-optimized, timed SRT subtitle files for 9:16 vertical video."""

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Format floating seconds into standard SRT timestamp HH:MM:SS,mmm."""
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int(round((seconds - int(seconds)) * 1000))
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def wrap_text_for_mobile(text: str, max_chars_per_line: int = 32) -> str:
        """Wrap text into 1 or 2 lines optimal for mobile vertical screens."""
        words = text.strip().split()
        lines = []
        current_line = []
        current_len = 0

        for w in words:
            if current_len + len(w) + (1 if current_line else 0) <= max_chars_per_line:
                current_line.append(w)
                current_len += len(w) + (1 if current_line else 0)
            else:
                lines.append(" ".join(current_line))
                current_line = [w]
                current_len = len(w)

        if current_line:
            lines.append(" ".join(current_line))

        # Join at most 2 lines per caption cue
        return "\n".join(lines[:2])

    @classmethod
    def generate_srt_from_scenes(cls, scenes: List[Dict[str, Any]], output_srt_path: str) -> str:
        """
        Generate timed SRT subtitles based on actual scene timings.
        Splits each scene narration into natural sentence/clause chunks.
        """
        Path(output_srt_path).parent.mkdir(parents=True, exist_ok=True)
        srt_entries = []
        current_time = 0.0
        counter = 1

        for scene in scenes:
            scene_duration = float(scene.get("duration", scene.get("duration_est", 4.0)))
            narration = scene.get("narration", "").strip()
            if not narration:
                current_time += scene_duration
                continue

            # Split narration into natural phrases by punctuation
            clauses = [c.strip() for c in re.split(r'[,;:.!?]+', narration) if len(c.strip()) > 3]
            if not clauses:
                clauses = [narration]

            # Allocate duration proportionally by word count
            clause_word_counts = [len(c.split()) for c in clauses]
            total_words = sum(clause_word_counts) if sum(clause_word_counts) > 0 else 1

            clause_time = current_time
            for i, clause in enumerate(clauses):
                share = clause_word_counts[i] / total_words
                cue_duration = max(1.2, scene_duration * share)
                start_ts = cls.format_timestamp(clause_time)
                end_ts = cls.format_timestamp(clause_time + cue_duration)
                
                wrapped_text = cls.wrap_text_for_mobile(clause.upper())

                srt_entries.append(f"{counter}\n{start_ts} --> {end_ts}\n{wrapped_text}\n")
                counter += 1
                clause_time += cue_duration

            current_time += scene_duration

        srt_content = "\n".join(srt_entries)
        with open(output_srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)

        return output_srt_path

    @staticmethod
    def get_ffmpeg_subtitle_filter(srt_path: str) -> str:
        """
        Produce a bulletproof FFmpeg subtitles filter string with high-contrast mobile typography.
        Uses safe escaping for Windows backslashes and colons.
        """
        # Escape path for FFmpeg filter syntax
        clean_path = str(Path(srt_path).resolve()).replace("\\", "/").replace(":", "\\:")
        # Styling: Sans font, yellow/white text, black outline, subtle semi-transparent box
        style = (
            "FontSize=14,"
            "PrimaryColour=&H00FFFFFF,"   # White
            "OutlineColour=&H00000000,"   # Black outline
            "BackColour=&H60000000,"      # Semi-transparent dark background box
            "BorderStyle=3,"              # Opaque box
            "Outline=1,"
            "Shadow=0,"
            "Alignment=2,"                # Centered bottom
            "MarginV=175"                 # Safe zone above Instagram bottom overlay
        )
        return f"subtitles='{clean_path}':force_style='{style}'"
