import os
from pathlib import Path

class Typography:
    """Manages typography formatting, font escaping, and safe drawing for FFmpeg overlays."""

    @staticmethod
    def get_system_font_path(bold: bool = True) -> str:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
        ]
        for c in candidates:
            if os.path.exists(c):
                # FFmpeg requires forward slashes and escaped colons
                return c.replace("\\", "/").replace(":", "\\:")
        return ""

    @classmethod
    def get_watermark_drawtext(cls, text: str = "SUPER.INTELLIGENCEEE", x: int = 80, y: int = 120, font_size: int = 26) -> str:
        font = cls.get_system_font_path(bold=True)
        font_opt = f"fontfile='{font}':" if font else ""
        return f"drawtext={font_opt}text='{text}':x={x}:y={y}:fontsize={font_size}:fontcolor=0x0284C7@1.0:box=1:boxcolor=0xF0F9FF@0.9:boxborderw=8"
