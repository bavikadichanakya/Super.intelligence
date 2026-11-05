"""
SUPER.INTELLIGENCEEE — Audio & Caption Quality Assurance Module
Optional Whisper QA verification when installed, with lightweight heuristic fallback.
Strictly non-blocking, zero crash risk on 8 GB RAM machines.
"""

from __future__ import annotations

import difflib
import logging
import subprocess
import wave
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("super_intelligence.whisper_qa")


class WhisperQA:
    """Performs speech-to-text QA and acoustic verification on synthesized narration."""

    def __init__(self):
        self._whisper_model = None
        self._attempted_load = False

    def _get_whisper_engine(self):
        """Attempts to load faster_whisper or whisper tiny model if available."""
        if self._attempted_load:
            return self._whisper_model

        self._attempted_load = True
        try:
            from faster_whisper import WhisperModel
            logger.info("Loading faster-whisper tiny CPU model for QA...")
            self._whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
        except ImportError:
            try:
                import whisper
                logger.info("Loading standard whisper tiny model for QA...")
                self._whisper_model = whisper.load_model("tiny")
            except ImportError:
                logger.info("Whisper not installed in environment; will use heuristic acoustic QA.")
                self._whisper_model = None
        except Exception as e:
            logger.warning(f"Could not initialize Whisper QA model: {e}")
            self._whisper_model = None

        return self._whisper_model

    def verify_audio(
        self,
        audio_path: Path | str,
        expected_text: str,
        expected_duration: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Validates synthesized audio against expected script text.
        Returns a structured QA report.
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            return {
                "passed": False,
                "score": 0.0,
                "qa_method": "file_check",
                "details": f"Audio file does not exist: {audio_path}",
            }

        # Check wave file properties
        try:
            with wave.open(str(audio_path), "rb") as wf:
                channels = wf.getnchannels()
                sample_rate = wf.getframerate()
                n_frames = wf.getnframes()
                duration = n_frames / float(sample_rate) if sample_rate > 0 else 0.0
                file_size = audio_path.stat().st_size
        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "qa_method": "wav_header_check",
                "details": f"Corrupt or non-WAV audio: {e}",
            }

        if file_size < 1000 or duration < 1.0:
            return {
                "passed": False,
                "score": 0.0,
                "qa_method": "duration_check",
                "details": f"Audio is too short or empty ({duration:.2f}s, {file_size} bytes)",
            }

        # Attempt Whisper model check if loaded
        engine = self._get_whisper_engine()
        if engine:
            try:
                # Transcribe with faster-whisper or whisper
                if hasattr(engine, "transcribe"):
                    segments, info = engine.transcribe(str(audio_path), beam_size=1)
                    transcribed_text = " ".join([s.text for s in segments]).strip().lower()
                else:
                    res = engine.transcribe(str(audio_path))
                    transcribed_text = res.get("text", "").strip().lower()

                # Calculate text similarity
                clean_expected = expected_text.strip().lower()
                matcher = difflib.SequenceMatcher(None, clean_expected, transcribed_text)
                sim_ratio = matcher.ratio()

                passed = sim_ratio >= 0.65
                return {
                    "passed": passed,
                    "score": round(sim_ratio, 3),
                    "qa_method": "whisper_stt",
                    "transcribed": transcribed_text,
                    "expected": clean_expected,
                    "duration": round(duration, 2),
                    "details": f"Speech similarity: {sim_ratio * 100:.1f}%",
                }
            except Exception as e:
                logger.warning(f"Whisper inference failed ({e}), falling back to acoustic checks.")

        # Heuristic acoustic verification
        # 1. Check expected word count vs duration (normal speech is 2.0 - 3.2 words per second)
        word_count = len(expected_text.split())
        words_per_sec = word_count / duration if duration > 0 else 0

        # Pacing sanity check
        pacing_ok = 1.0 <= words_per_sec <= 4.5
        score = 0.90 if pacing_ok else 0.60

        return {
            "passed": pacing_ok,
            "score": score,
            "qa_method": "acoustic_heuristics",
            "duration": round(duration, 2),
            "word_count": word_count,
            "words_per_sec": round(words_per_sec, 2),
            "sample_rate": sample_rate,
            "channels": channels,
            "details": f"Acoustic check: {duration:.2f}s for {word_count} words ({words_per_sec:.2f} wps).",
        }

