"""
TASK 4 — NARRATION FAILURE TEST
Standalone verification script for Piper TTS and pyttsx3 fallback.
"""

import os
import json
import wave
import subprocess
from pathlib import Path

from core.config import get_config
from audio.piper_engine import PiperEngine
from audio.pyttsx3_engine import Pyttsx3Engine
from audio.narration import NarrationService


def get_audio_stream_info(wav_path: str):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_name,channels,sample_rate,duration",
        "-show_entries", "format=size,duration",
        "-of", "json", wav_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def test_narration_subsystem():
    config = get_config()
    test_out_dir = config.resolve_path("output/test_narration")
    test_out_dir.mkdir(parents=True, exist_ok=True)

    text = "Superintelligence is accelerating breakthrough research in multimodal neural architectures."

    # 1. Independent Piper TTS Test
    piper_out = test_out_dir / "test_piper_direct.wav"
    if piper_out.exists():
        piper_out.unlink()

    piper = PiperEngine()
    ok_piper, meta_piper = piper.generate(text, str(piper_out))
    
    assert ok_piper is True, f"Piper direct generation failed: {meta_piper}"
    assert piper_out.exists(), "Piper WAV does not exist"
    assert piper_out.stat().st_size > 1000, f"Piper WAV is too small ({piper_out.stat().st_size} bytes)"

    with wave.open(str(piper_out), "rb") as wf:
        piper_channels = wf.getnchannels()
        piper_framerate = wf.getframerate()
        piper_nframes = wf.getnframes()
        piper_duration_wave = round(piper_nframes / float(piper_framerate), 3)

    piper_ffprobe = get_audio_stream_info(str(piper_out))

    piper_report = {
        "engine": "piper",
        "voice": meta_piper.get("voice"),
        "file_path": str(piper_out),
        "file_size_bytes": piper_out.stat().st_size,
        "sample_rate_hz": piper_framerate,
        "channels": piper_channels,
        "duration_seconds": piper_duration_wave,
        "ffprobe_codec": piper_ffprobe["streams"][0]["codec_name"],
        "ffprobe_valid": len(piper_ffprobe.get("streams", [])) > 0
    }

    # 2. Simulated Piper Failure & pyttsx3 Fallback Test
    fallback_out = test_out_dir / "test_pyttsx3_fallback.wav"
    if fallback_out.exists():
        fallback_out.unlink()

    service = NarrationService()
    # Simulate Piper failure by setting invalid model path
    service.piper.onnx_path = Path("A:/SUPER.INTELLIGENCEEE/assets/voices/non_existent_voice.onnx")
    service.piper._voice = None

    ok_service, meta_service = service.generate_narration(text, str(fallback_out))

    assert ok_service is True, f"Fallback narration failed: {meta_service}"
    assert meta_service.get("engine") == "pyttsx3", f"Engine was not pyttsx3: {meta_service.get('engine')}"
    assert fallback_out.exists(), "Fallback WAV does not exist"
    assert fallback_out.stat().st_size > 1000, f"Fallback WAV too small ({fallback_out.stat().st_size} bytes)"

    with wave.open(str(fallback_out), "rb") as wf:
        fb_channels = wf.getnchannels()
        fb_framerate = wf.getframerate()
        fb_nframes = wf.getnframes()
        fb_duration_wave = round(fb_nframes / float(fb_framerate), 3)

    fb_ffprobe = get_audio_stream_info(str(fallback_out))

    fallback_report = {
        "engine": meta_service.get("engine"),
        "voice": meta_service.get("voice"),
        "file_path": str(fallback_out),
        "file_size_bytes": fallback_out.stat().st_size,
        "sample_rate_hz": fb_framerate,
        "channels": fb_channels,
        "duration_seconds": fb_duration_wave,
        "ffprobe_codec": fb_ffprobe["streams"][0]["codec_name"],
        "ffprobe_valid": len(fb_ffprobe.get("streams", [])) > 0
    }

    final_results = {
        "task": "TASK 4 — NARRATION FAILURE TEST",
        "piper_primary": piper_report,
        "pyttsx3_fallback": fallback_report,
        "status": "PASS"
    }

    print(json.dumps(final_results, indent=2))
    return final_results


if __name__ == "__main__":
    test_narration_subsystem()

