import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List

from core.config import get_config
from core.logger import get_logger
from audio.piper_engine import PiperEngine
from audio.pyttsx3_engine import Pyttsx3Engine
from audio.audio_processor import AudioProcessor

logger = get_logger("Narration")

class NarrationService:
    """
    Unified offline narration interface.
    Primary Engine: Piper TTS (en_US-lessac-medium)
    Fallback Engine: pyttsx3
    """

    def __init__(self, db=None, config=None):
        self.config = config or get_config()
        self.db = db
        self.piper = PiperEngine()
        self.pyttsx3 = Pyttsx3Engine()

    def synthesize_speech(self, text: str, output_filename: Optional[str] = None) -> Dict[str, Any]:
        """Convenience method returning structured dictionary with file Path and duration."""
        if not output_filename:
            voices_dir = self.config.resolve_path(self.config.get("paths.voices_dir", "assets/voices"))
            voices_dir.mkdir(parents=True, exist_ok=True)
            output_path = voices_dir / f"speech_{int(time.time() * 1000)}.wav"
        else:
            output_path = Path(output_filename)
            if not output_path.is_absolute() and not output_path.parent.name:
                voices_dir = self.config.resolve_path(self.config.get("paths.voices_dir", "assets/voices"))
                output_path = voices_dir / output_filename
            output_path.parent.mkdir(parents=True, exist_ok=True)

        ok, meta = self.generate_narration(text, str(output_path))
        return {
            "success": ok,
            "path": output_path,
            "duration_seconds": meta.get("duration", 0.0),
            "engine": meta.get("engine", "unknown"),
            "voice": meta.get("voice", "unknown"),
        }

    def generate_narration(self, text: str, output_wav_path: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Generate narration audio with automatic fallback.
        Validates WAV file and logs performance metrics.
        """
        start = time.time()
        logger.info(f"Synthesizing voiceover ({len(text.split())} words)...")

        # 1. Try Primary Engine (Piper)
        ok_piper, meta_piper = self.piper.generate(text, output_wav_path)
        if ok_piper:
            info = AudioProcessor.get_audio_info(output_wav_path)
            meta_piper["duration"] = info.get("duration", 0.0)
            logger.info(f"Narration generated via Piper ({meta_piper['voice']}): {meta_piper['duration']:.2f}s in {meta_piper['execution_time_seconds']}s")
            return True, meta_piper

        # 2. Try Fallback Engine (pyttsx3)
        logger.warning(f"Piper engine unavailable ({meta_piper.get('error')}), switching to pyttsx3 fallback...")
        ok_pyttsx, meta_pyttsx = self.pyttsx3.generate(text, output_wav_path)
        if ok_pyttsx:
            info = AudioProcessor.get_audio_info(output_wav_path)
            meta_pyttsx["duration"] = info.get("duration", 0.0)
            logger.info(f"Narration generated via pyttsx3 ({meta_pyttsx['voice']}): {meta_pyttsx['duration']:.2f}s")
            return True, meta_pyttsx

        logger.error("All narration engines failed to generate audio.")
        return False, {"error": "All TTS engines failed", "execution_time_seconds": round(time.time() - start, 2)}
