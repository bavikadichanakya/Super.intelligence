from pathlib import Path
from typing import List

class Transitions:
    """Manages scene concatenations and transitions for vertical video rendering."""

    @staticmethod
    def create_concat_file(clip_paths: List[str], concat_file_path: str) -> str:
        """Create a standard FFmpeg concat demuxer text file."""
        Path(concat_file_path).parent.mkdir(parents=True, exist_ok=True)
        lines = []
        for p in clip_paths:
            # Use forward slashes for cross-platform FFmpeg paths
            clean_path = str(Path(p).resolve()).replace("\\", "/")
            lines.append(f"file '{clean_path}'")
        
        with open(concat_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
            
        return concat_file_path
