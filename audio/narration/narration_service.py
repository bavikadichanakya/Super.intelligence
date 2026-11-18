"""
SUPER.INTELLIGENCEEE — Unified Narration Service
Primary Engine: Voicebox AI Voice Studio (Kokoro-82M British RP/American Male)
Fallback Engine 1: Piper Neural TTS (jarvis-high, mature British RP male)
Fallback Engine 2: pyttsx3 (strictly male Windows SAPI)
Strictly guarantees MALE voice output with no silent fallback.
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from core.config import get_config
from core.logger import get_logger
from audio.providers.voicebox_provider import VoiceboxProvider
from audio.piper_engine import PiperEngine
from audio.pyttsx3_engine import Pyttsx3Engine
from audio.audio_processor import AudioProcessor

logger = get_logger("NarrationService")


# Authoritative Production Voice Lock Constants
VOICE_PROVIDER = "voicebox"
TTS_ENGINE = "kokoro"
VOICE_ID = "am_liam"
VOICE_LOCALE = "en-US"
VOICE_ACCENT = "general_american"


class NarrationVoiceLockError(Exception):
    """Raised when the locked General American narration voice cannot be synthesized."""
    pass


class NarrationService:
    """
    Unified narration interface orchestrating Voicebox / Kokoro as primary locked provider.
    Strictly guarantees General American male voice (am_liam) with zero silent substitution.
    """

    def __init__(self, db=None, config=None, use_voicebox: bool = True):
        self.config = config or get_config()
        self.db = db
        self.use_voicebox = use_voicebox
        self.voicebox = VoiceboxProvider(config=self.config)
        self.piper = PiperEngine()
        self.pyttsx3 = Pyttsx3Engine()

    def check_providers_health(self) -> Dict[str, Any]:
        """Inspects status of all available TTS providers."""
        vb_health = self.voicebox.check_health()
        return {
            "primary_voicebox": {
                "available": self.voicebox.is_available(),
                "endpoint": self.voicebox.api_url,
                "engine": TTS_ENGINE,
                "voice": VOICE_ID,
                "locale": VOICE_LOCALE,
                "accent": VOICE_ACCENT,
                "details": vb_health,
            },
            "fallback_piper": {
                "available": Path("assets/voices/jarvis-high.onnx").exists(),
                "model": "jarvis-high.onnx",
                "voice": "Jarvis British RP Male (DISABLED IN PRODUCTION)",
            },
            "fallback_sapi": {
                "available": True,
                "engine": "pyttsx3",
                "voice": "Microsoft David (DISABLED IN PRODUCTION)",
            },
        }

    def synthesize_speech(
        self,
        text: str,
        output_filename: Optional[str] = None,
        voice_id: Optional[str] = None,
        engine: Optional[str] = None,
        tone: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convenience method returning structured dictionary with file Path and duration."""
        voices_dir = self.config.resolve_path(self.config.get("paths.voices_dir", "assets/voices"))
        voices_dir.mkdir(parents=True, exist_ok=True)

        if not output_filename:
            output_path = voices_dir / f"speech_{int(time.time() * 1000)}.wav"
        else:
            output_path = Path(output_filename)
            if not output_path.is_absolute() and not output_path.parent.name:
                output_path = voices_dir / output_filename
            output_path.parent.mkdir(parents=True, exist_ok=True)

        ok, meta = self.generate_narration(
            text=text,
            output_wav_path=str(output_path),
            voice_id=voice_id or VOICE_ID,
            engine=engine or TTS_ENGINE,
        )
        return {
            "success": ok,
            "path": output_path,
            "duration_seconds": meta.get("duration", 0.0),
            "engine": meta.get("engine", TTS_ENGINE),
            "voice": meta.get("voice", VOICE_ID),
            "voice_gender": "MALE",
            "locale": meta.get("locale", VOICE_LOCALE),
            "accent": meta.get("accent", VOICE_ACCENT),
            "fallback_used": meta.get("fallback_used", False),
            "meta": meta,
        }

    def generate_narration(
        self,
        text: str,
        output_wav_path: str,
        voice_id: Optional[str] = None,
        engine: Optional[str] = None,
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Generate narration audio with locked General American voice (am_liam).
        Silent fallback to other voices is strictly rejected.
        """
        start = time.time()
        words = len(text.split())
        target_voice = voice_id or VOICE_ID
        target_engine = engine or TTS_ENGINE

        logger.info(f"Synthesizing voiceover ({words} words) via locked voice '{target_voice}'...")

        if target_voice != VOICE_ID and not os.environ.get("ALLOW_VOICE_OVERRIDE"):
            raise NarrationVoiceLockError(
                f"Production voice lock violation: '{target_voice}' requested, but '{VOICE_ID}' is strictly required."
            )

        # 1. Primary Engine: Voicebox / Kokoro with locked voice am_liam
        if self.use_voicebox and self.voicebox.is_available():
            try:
                ok_vb, meta_vb = self.voicebox.generate_speech(
                    text=text,
                    output_wav_path=output_wav_path,
                    voice_id=target_voice,
                    engine=target_engine,
                )
                if ok_vb:
                    meta_vb["voice_gender"] = "MALE"
                    meta_vb["fallback_used"] = False
                    meta_vb["voice_locked"] = True
                    meta_vb["locale"] = VOICE_LOCALE
                    meta_vb["accent"] = VOICE_ACCENT
                    logger.info(
                        f"Narration generated via Voicebox/Kokoro ({meta_vb.get('voice')} [MALE]): "
                        f"{meta_vb.get('duration', 0):.2f}s in {meta_vb.get('execution_time_seconds', 0)}s"
                    )
                    return True, meta_vb
                else:
                    logger.warning(f"Voicebox/Kokoro returned failure: {meta_vb.get('error')}")
            except Exception as e:
                logger.error(f"Voicebox/Kokoro provider error ({e})")

        # 2. Strict Fallback Policy: Reject silent fallback to Piper / SAPI
        if not os.environ.get("ALLOW_VOICE_FALLBACK"):
            raise NarrationVoiceLockError(
                f"Production Voice Lock Violated: Required voice '{VOICE_ID}' ({TTS_ENGINE}) "
                "could not be generated. Silent fallback to Piper or other voices is strictly prohibited."
            )

        # 3. Controlled Fallback (Only reachable if ALLOW_VOICE_FALLBACK is explicitly enabled)
        logger.warning("ALLOW_VOICE_FALLBACK is set; attempting fallback to Piper...")
        ok_piper, meta_piper = self.piper.generate(text, output_wav_path)
        if ok_piper:
            info = AudioProcessor.get_audio_info(output_wav_path)
            meta_piper["duration"] = info.get("duration", 0.0)
            meta_piper["voice_gender"] = "MALE"
            meta_piper["fallback_used"] = True
            meta_piper["fallback_reason"] = "Voicebox offline and fallback explicitly authorized"
            return True, meta_piper

        logger.error("All narration options failed.")
        return False, {
            "error": "Kokoro narration generation failed and fallback is prohibited.",
            "execution_time_seconds": round(time.time() - start, 2),
            "fallback_used": False,
        }

