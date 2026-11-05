class MotionGraphics:
    """Constructs dynamic visual overlays (animated progress bar, branded accents) for FFmpeg."""

    @staticmethod
    def get_progress_bar_filter(total_duration: float, height: int = 10, color: str = "0x06B6D4@1.0") -> str:
        """
        Creates an animated top progress bar that smoothly grows from 0 to 1080px across the Reel duration.
        """
        dur = max(1.0, float(total_duration))
        return f"drawbox=x=0:y=0:w='min(1080,(t/{dur:.2f})*1080)':h={height}:color={color}:t=fill"

    @staticmethod
    def get_subtle_vignette() -> str:
        """Subtle vignette for cinematic depth."""
        return "vignette=PI/7"
