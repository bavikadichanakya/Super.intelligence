"""
SUPER.INTELLIGENCEEE — Direct Kokoro-82M Benchmark Script
Tests Kokoro-82M model loading, RAM footprint, inference speed, and audio generation.
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# Add external/voicebox to sys.path
sys.path.insert(0, str(Path("external/voicebox").resolve()))

import numpy as np
import soundfile as sf
import psutil

from backend.backends.kokoro_backend import KokoroTTSBackend, KOKORO_SAMPLE_RATE

TEST_TEXT = (
    "Attention scaling has officially shattered the quadratic memory wall — "
    "fused state-space kernels achieve one million tokens of context with sub-quadratic complexity."
)

OUTPUT_DIR = Path("output/voice_samples")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


async def benchmark_kokoro():
    process = psutil.Process(os.getpid())
    ram_before = process.memory_info().rss / 1024 / 1024
    print(f"[Kokoro Benchmark] Initial RAM: {ram_before:.2f} MB")

    backend = KokoroTTSBackend()
    t0 = time.time()
    await backend.load_model()
    load_time = time.time() - t0
    ram_after_load = process.memory_info().rss / 1024 / 1024
    print(f"[Kokoro Benchmark] Model Loaded in {load_time:.2f}s | RAM: {ram_after_load:.2f} MB (+{ram_after_load - ram_before:.2f} MB)")

    # Test Voices: British Male (bm_george), American Male (am_adam)
    voices_to_test = [
        ("bm_george", "British RP Male (George)"),
        ("am_adam", "American Male (Adam)"),
    ]

    for voice_id, voice_desc in voices_to_test:
        print(f"\n--- Testing Kokoro Voice: {voice_id} ({voice_desc}) ---")
        prompt = {"preset_voice_id": voice_id}
        
        t_start = time.time()
        audio, sr = await backend.generate(
            text=TEST_TEXT,
            voice_prompt=prompt,
            language="en",
            seed=42,
        )
        gen_time = time.time() - t_start
        audio_dur = len(audio) / sr
        rtf = gen_time / audio_dur if audio_dur > 0 else 0
        ram_now = process.memory_info().rss / 1024 / 1024

        out_path = OUTPUT_DIR / f"kokoro_{voice_id}_benchmark.wav"
        sf.write(str(out_path), audio, sr)

        print(f"  Audio File: {out_path} ({out_path.stat().st_size} bytes)")
        print(f"  Duration: {audio_dur:.2f}s | Generation Time: {gen_time:.2f}s")
        print(f"  Real-Time Factor (RTF): {rtf:.3f}x (Lower is faster)")
        print(f"  Peak RAM: {ram_now:.2f} MB")

    backend.unload_model()
    print("\n[Kokoro Benchmark] Completed successfully!")


if __name__ == "__main__":
    asyncio.run(benchmark_kokoro())

