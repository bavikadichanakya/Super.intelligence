import os
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from core.config_manager import get_config
from core.logger import get_logger

logger = get_logger("TTSEngine")

class TTSEngine:
    """Zero-budget dual TTS engine providing high-quality neural voice with offline SAPI fallback."""

    def __init__(self):
        self.config = get_config()
        self.primary_engine = self.config.get("audio.primary_tts", "edge-tts")
        self.default_edge_voice = self.config.get("audio.edge_tts_voice", "en-US-ChristopherNeural")
        self.pyttsx3_rate = self.config.get("audio.pyttsx3_rate", 180)

    async def _render_edge_tts(self, text: str, output_path: str, voice: str) -> bool:
        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            return True
        except Exception as e:
            logger.warning(f"edge-tts rendering failed: {e}")
            return False

    def _render_pyttsx3(self, text: str, output_path: str) -> bool:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', self.pyttsx3_rate)
            # Find an English voice
            voices = engine.getProperty('voices')
            for v in voices:
                if "david" in v.name.lower() or "zira" in v.name.lower() or "english" in v.name.lower():
                    engine.setProperty('voice', v.id)
                    break
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            # Verify file exists and has size
            if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
                return True
        except Exception as e:
            logger.error(f"pyttsx3 rendering failed: {e}")
        return False

    def generate_speech(self, text: str, output_path: str, voice: Optional[str] = None) -> Tuple[bool, str]:
        """Generate voiceover audio with automatic fallback between edge-tts and pyttsx3."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        chosen_voice = voice or self.default_edge_voice

        # 1. Try edge-tts if preferred
        if self.primary_engine == "edge-tts":
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                success = loop.run_until_complete(self._render_edge_tts(text, output_path, chosen_voice))
                loop.close()
                if success and os.path.exists(output_path) and os.path.getsize(output_path) > 500:
                    logger.info(f"Generated neural audio via edge-tts ({chosen_voice}): {output_path}")
                    return True, "edge-tts"
            except Exception as e:
                logger.warning(f"edge-tts exception: {e}, falling back to pyttsx3")

        # 2. Offline Fallback: pyttsx3
        logger.info("Using offline Windows SAPI pyttsx3 voice engine")
        # pyttsx3 writes WAV files best on Windows
        wav_path = str(Path(output_path).with_suffix(".wav"))
        success = self._render_pyttsx3(text, wav_path)
        if success:
            # If caller wanted mp3, we can point to wav or convert later
            logger.info(f"Generated offline audio via pyttsx3: {wav_path}")
            return True, "pyttsx3"

        return False, "All TTS engines failed"
