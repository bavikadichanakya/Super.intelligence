import os
import wave
import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

from core.config import get_config
from core.logger import get_logger

logger = get_logger("PiperEngine")

class PiperEngine:
    """Primary offline TTS narration engine using Piper."""

    def __init__(self, voice_model: Optional[str] = None):
        self.config = get_config()
        self.model_name = voice_model or self.config.get("narration.piper_voice", "en_US-lessac-medium")
        voice_dir = self.config.resolve_path(self.config.get("narration.piper_voice_dir", "assets/voices"))
        self.onnx_path = voice_dir / f"{self.model_name}.onnx"
        self._voice = None

    def _get_voice(self):
        if self._voice is None:
            if not self.onnx_path.exists():
                raise FileNotFoundError(f"Piper ONNX model not found: {self.onnx_path}")
            import piper
            self._voice = piper.PiperVoice.load(str(self.onnx_path))
        return self._voice

    def generate(self, text: str, output_wav_path: str) -> Tuple[bool, Dict[str, Any]]:
        Path(output_wav_path).parent.mkdir(parents=True, exist_ok=True)
        start_time = time.time()
        try:
            voice = self._get_voice()
            sample_rate = voice.config.sample_rate

            with wave.open(output_wav_path, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                for chunk in voice.synthesize(text):
                    wav_file.writeframes(chunk.audio_int16_bytes)

            file_size = os.path.getsize(output_wav_path) if os.path.exists(output_wav_path) else 0
            elapsed = round(time.time() - start_time, 2)

            if file_size < 1000:
                logger.error(f"Piper generated empty or corrupted audio ({file_size} bytes)")
                return False, {"error": "Empty audio output"}

            return True, {
                "engine": "piper",
                "voice": self.model_name,
                "file_path": output_wav_path,
                "file_size": file_size,
                "sample_rate": sample_rate,
                "execution_time_seconds": elapsed
            }
        except Exception as e:
            logger.error(f"Piper generation failed: {e}")
            return False, {"error": str(e)}

