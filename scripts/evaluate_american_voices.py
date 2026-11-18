"""
SUPER.INTELLIGENCEEE — Phase 3.5 American Voice Evaluation Runner
Generates and acoustic-analyzes standardized tech documentary narration samples
across available Voicebox Kokoro General American English male voices.
"""

import json
import logging
import math
import os
import sys
import time
import wave
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from audio.narration.narration_service import NarrationService
from audio.providers.voicebox_provider import VoiceboxProvider

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("evaluate_american_voices")

TEST_SCRIPT = (
    "Frontier AI models are abandoning traditional brute-force scaling. "
    "By optimizing test-time compute through speculative verification, "
    "autonomous systems achieve a three-hundred percent acceleration without degrading precision."
)

CANDIDATES = [
    {
        "id": "am_adam",
        "name": "Adam",
        "archetype": "Authoritative & Deep Academic",
        "expected_accent": "General American (GA)",
    },
    {
        "id": "am_michael",
        "name": "Michael",
        "archetype": "Engaging & Conversational Tech Presenter",
        "expected_accent": "General American (GA)",
    },
    {
        "id": "am_eric",
        "name": "Eric",
        "archetype": "Precise & Energetic Systems Specialist",
        "expected_accent": "General American (GA)",
    },
    {
        "id": "am_liam",
        "name": "Liam",
        "archetype": "Modern & Dynamic Engineering Lead",
        "expected_accent": "General American (GA)",
    },
]


def analyze_wav(wav_path: Path) -> dict:
    with wave.open(str(wav_path), "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)

    duration = n_frames / float(framerate)
    
    # Calculate peak amplitude and RMS
    import struct
    fmt = f"<{n_frames * n_channels}h"
    samples = struct.unpack(fmt, raw_bytes)
    
    peak = max(abs(s) for s in samples) if samples else 0
    peak_db = 20 * math.log10(peak / 32768.0) if peak > 0 else -99.0
    
    rms = math.sqrt(sum(s * s for s in samples) / len(samples)) if samples else 0
    rms_db = 20 * math.log10(rms / 32768.0) if rms > 0 else -99.0

    return {
        "duration_seconds": round(duration, 3),
        "sample_rate": framerate,
        "channels": n_channels,
        "sample_width_bytes": sampwidth,
        "peak_db": round(peak_db, 2),
        "rms_db": round(rms_db, 2),
        "file_size_bytes": wav_path.stat().st_size,
    }


def main():
    logger.info("=== Phase 3.5 General American Voice Evaluation Runner ===")
    out_dir = Path("output/voice_samples")
    out_dir.mkdir(parents=True, exist_ok=True)

    narration_service = NarrationService(use_voicebox=True)
    health = narration_service.check_providers_health()
    logger.info(f"Voicebox Provider Status: {health.get('primary_voicebox', {}).get('available')}")

    if not health.get("primary_voicebox", {}).get("available"):
        raise RuntimeError("Voicebox server is not available at http://127.0.0.1:17493")

    results = []

    for c in CANDIDATES:
        voice_id = c["id"]
        voice_name = c["name"]
        out_file = f"sample_{voice_id}.wav"
        target_path = out_dir / out_file

        logger.info(f"Synthesizing test sample for {voice_name} ({voice_id})...")
        t0 = time.time()
        res = narration_service.synthesize_speech(
            text=TEST_SCRIPT,
            output_filename=f"../output/voice_samples/{out_file}",
            voice_id=voice_id,
            engine="kokoro",
        )
        elapsed = time.time() - t0

        if not res.get("success"):
            logger.error(f"Failed to generate {voice_id}: {res}")
            continue

        actual_path = Path(res["path"])
        metrics = analyze_wav(actual_path)
        metrics["voice_id"] = voice_id
        metrics["name"] = voice_name
        metrics["archetype"] = c["archetype"]
        metrics["generation_time_seconds"] = round(elapsed, 2)
        metrics["file_path"] = str(actual_path)
        metrics["engine"] = res.get("engine")
        metrics["fallback_used"] = res.get("fallback_used", False)
        
        results.append(metrics)
        logger.info(
            f"Successfully generated {voice_id} in {elapsed:.2f}s | "
            f"Dur: {metrics['duration_seconds']}s | Peak: {metrics['peak_db']} dB | RMS: {metrics['rms_db']} dB"
        )

    # Save evaluation results JSON
    summary_path = out_dir / "american_voice_evaluation_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Evaluation summary saved to {summary_path}")

    print("\n=== VOICE CANDIDATE ACOUSTIC COMPARISON ===")
    print(f"{'Voice ID':12} | {'Name':8} | {'Duration':8} | {'Peak dB':8} | {'RMS dB':8} | {'Gen Time':8}")
    print("-" * 65)
    for r in results:
        print(f"{r['voice_id']:12} | {r['name']:8} | {r['duration_seconds']}s    | {r['peak_db']} dB | {r['rms_db']} dB | {r['generation_time_seconds']}s")

    return results


if __name__ == "__main__":
    main()

