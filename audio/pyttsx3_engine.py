import os
import time
from pathlib import Path
from typing import Dict, Any, Tuple

from core.config import get_config
from core.logger import get_logger

logger = get_logger("Pyttsx3Engine")

class Pyttsx3Engine:
    """Offline Windows SAPI fallback TTS engine."""

    def __init__(self):
        self.config = get_config()
        self.rate = self.config.get("narration.pyttsx3_rate", 180)
        self.volume = self.config.get("narration.pyttsx3_volume", 1.0)

    def generate(self, text: str, output_wav_path: str) -> Tuple[bool, Dict[str, Any]]:
        Path(output_wav_path).parent.mkdir(parents=True, exist_ok=True)
        start_time = time.time()
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)

            # Select an English voice if available
            voices = engine.getProperty('voices')
            voice_name = "default"
            for v in voices:
                if any(k in v.name.lower() for k in ("david", "zira", "english", "mark")):
                    engine.setProperty('voice', v.id)
                    voice_name = v.name
                    break

            engine.save_to_file(text, output_wav_path)
            engine.runAndWait()

            file_size = os.path.getsize(output_wav_path) if os.path.exists(output_wav_path) else 0
            elapsed = round(time.time() - start_time, 2)

            if file_size < 1000:
                logger.error(f"pyttsx3 generated empty audio ({file_size} bytes)")
                return False, {"error": "Empty audio output"}

            return True, {
                "engine": "pyttsx3",
                "voice": voice_name,
                "file_path": output_wav_path,
                "file_size": file_size,
                "sample_rate": 22050,
                "execution_time_seconds": elapsed
            }
        except Exception as e:
            logger.error(f"pyttsx3 generation failed: {e}")
            return False, {"error": str(e)}

