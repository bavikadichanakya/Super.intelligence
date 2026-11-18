"""
SUPER.INTELLIGENCEEE — Phase 15 Prototype Audio Batch Synthesizer (Optimized 30-45s)
"""

import os
import sys
import time
from pathlib import Path
import numpy as np
import soundfile as sf

os.environ['HF_HUB_OFFLINE'] = '1'

from kokoro import KPipeline

OUT_DIR = Path(r"A:\SUPER.INTELLIGENCEEE\output\phase15_prototype\audio")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    (
        "scene1_overload",
        "To render just one frame in 4K, your computer must calculate eight million color values. Sixty times every single second."
    ),
    (
        "scene2_comparison",
        "A CPU is like an Olympic math genius solving one hard problem at a time. Great for chess, pure torture for graphics. A GPU is an army of thousands of workers painting every pixel simultaneously."
    ),
    (
        "scene3_silicon",
        "Inside the silicon die, complex control logic is stripped away. Instead, thousands of raw Arithmetic Logic Units are packed into Streaming Multiprocessors."
    ),
    (
        "scene4_simt",
        "This is SIMT: Single Instruction, Multiple Threads. One command executes across an entire warp of cores in lockstep, crunching matrices instantly."
    ),
    (
        "scene5_conclusion",
        "Let your CPU plan the strategy, and let the GPU do the heavy lifting. Super Intelligence. Understand what's next."
    ),
]

print("Initializing KPipeline (am_liam)...", flush=True)
pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')

total_dur = 0.0
for scene_id, text in SCENES:
    out_path = OUT_DIR / f"{scene_id}_speech.wav"
    generator = pipeline(text, voice="am_liam", speed=1.05)
    all_chunks = []
    for res in generator:
        if hasattr(res, 'audio') and res.audio is not None:
            chunk = res.audio
            if hasattr(chunk, 'detach'):
                chunk = chunk.detach().cpu().numpy()
            all_chunks.append(chunk.squeeze())
        elif isinstance(res, (tuple, list)) and len(res) >= 3 and res[2] is not None:
            chunk = res[2]
            if hasattr(chunk, 'detach'):
                chunk = chunk.detach().cpu().numpy()
            all_chunks.append(chunk.squeeze())

    audio = np.concatenate(all_chunks)
    sf.write(str(out_path), audio, 24000)
    dur = len(audio) / 24000.0
    total_dur += dur
    print(f"Saved: {out_path.name} | Duration: {dur:.2f}s", flush=True)

print(f"ALL SCENES READY! TOTAL PROTOTYPE DURATION: {total_dur:.2f}s (Target: 30-45s)", flush=True)
