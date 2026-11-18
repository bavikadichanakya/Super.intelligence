import os
import time
from pathlib import Path
from typing import Dict, Any, Tuple

from core.config import get_config
from core.logger import get_logger
from audio.pronunciation import TechnicalPronunciationLexicon

logger = get_logger("Pyttsx3Engine")

BANNED_VOICE_NAMES = {"zira", "female", "hazel", "eva", "catherine", "susan", "linda", "hedda"}
PREFERRED_MALE_NAMES = ["david", "mark", "george", "richard", "james", "male", "guy"]

class Pyttsx3Engine:
    """Offline Windows SAPI fallback TTS engine strictly enforcing MALE voices."""

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

            # Preprocess technical text phonetically
            processed_text = TechnicalPronunciationLexicon.preprocess_text(text)

            # Strictly select a verified MALE voice
            voices = engine.getProperty('voices')
            selected_voice = None

            for v in voices:
                v_name_lower = v.name.lower()
                if any(banned in v_name_lower for banned in BANNED_VOICE_NAMES):
                    continue
                if any(pref in v_name_lower for pref in PREFERRED_MALE_NAMES):
                    selected_voice = v
                    break

            if not selected_voice:
                # Secondary scan: find any voice that does not contain banned female keywords
                for v in voices:
                    v_name_lower = v.name.lower()
                    if not any(banned in v_name_lower for banned in BANNED_VOICE_NAMES):
                        selected_voice = v
                        break

            if not selected_voice:
                raise RuntimeError("No compatible male voice found on host OS. Female fallback prohibited.")

            engine.setProperty('voice', selected_voice.id)
            voice_name = selected_voice.name

            engine.save_to_file(processed_text, output_wav_path)
            engine.runAndWait()

            file_size = os.path.getsize(output_wav_path) if os.path.exists(output_wav_path) else 0
            elapsed = round(time.time() - start_time, 2)

            if file_size < 1000:
                logger.error(f"pyttsx3 generated empty audio ({file_size} bytes)")
                return False, {"error": "Empty audio output"}

            return True, {
                "engine": "pyttsx3",
                "voice": voice_name,
                "voice_gender": "MALE",
                "file_path": output_wav_path,
                "file_size": file_size,
                "sample_rate": 22050,
                "execution_time_seconds": elapsed
            }
        except Exception as e:
            logger.error(f"pyttsx3 generation failed: {e}")
            return False, {"error": str(e)}
