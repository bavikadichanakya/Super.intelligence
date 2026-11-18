"""
SUPER.INTELLIGENCEEE — Fast Batch Audio Synthesis for DeepSeek-R1 Spotlight
Direct Kokoro-82M (am_liam) batch synthesizer. Loads model once in-memory.
Produces:
- output/drafts/deepseek_r1_documentary/audio/scene*_voice_raw.wav
- output/drafts/deepseek_r1_documentary/audio/scene*_voice.wav (EBU R128 -16 LUFS)
- output/drafts/deepseek_r1_documentary/audio/scene*_master.wav (Subtle laboratory drone)
- output/drafts/deepseek_r1_documentary/audio/durations.json
"""

import os
import sys
import json
import wave
import time
import subprocess
from pathlib import Path

# Force offline HuggingFace Hub to eliminate any remote network hang
os.environ["HF_HUB_OFFLINE"] = "1"

import numpy as np
import soundfile as sf
import torch
from kokoro import KPipeline

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
OUTPUT_DIR = WORKSPACE_ROOT / "output" / "drafts" / "deepseek_r1_documentary" / "audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    (
        "scene1_hook_shockwave",
        "Ever wondered how a single open-source GitHub repository shook Silicon Valley and challenged trillion-dollar AI monopolies overnight?"
    ),
    (
        "scene2_reasoning_grpo",
        "Frontier reasoning models were assumed to require millions in human-labeled data, until DeepSeek proved pure reinforcement learning induces self-reflection from scratch."
    ),
    (
        "scene3_aha_moment",
        "Without any human guidance, the model spontaneously learned to pause, rethink, and verify its own deductions inside explicit thinking tokens before answering."
    ),
    (
        "scene4_mla_architecture",
        "To solve the catastrophic GPU memory crisis of traditional transformers, DeepSeek engineered Multi-Head Latent Attention, compressing the KV cache by ninety-three percent."
    ),
    (
        "scene5_moe_routing",
        "Scaling to six hundred seventy-one billion total parameters, its Mixture-of-Experts engine routes each token to just thirty-seven billion active parameters across two hundred fifty-six specialists."
    ),
    (
        "scene6_benchmark_showdown",
        "In standardized mathematical and coding benchmarks, this open-source architecture matches closed frontier models at a fraction of the cost."
    ),
    (
        "scene7_open_revolution",
        "By open-sourcing complete model weights and technical architecture under MIT license, DeepSeek proved that frontier intelligence belongs to the open developer ecosystem."
    ),
]

def main():
    print("=" * 80)
    print("INITIALIZING KOKORO-82M IN-MEMORY BATCH SYNTHESIZER (am_liam)")
    print("=" * 80)
    
    t0 = time.time()
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    print(f"Kokoro-82M pipeline loaded in {time.time() - t0:.2f}s")
    
    scene_durations = {}

    for idx, (sid, text) in enumerate(SCENES, 1):
        print(f"\n[{idx}/7] Synthesizing {sid}...")
        raw_wav = OUTPUT_DIR / f"{sid}_voice_raw.wav"
        norm_wav = OUTPUT_DIR / f"{sid}_voice.wav"
        master_wav = OUTPUT_DIR / f"{sid}_master.wav"

        # Generate audio
        t_gen = time.time()
        generator = pipeline(text, voice="am_liam", speed=1.0)
        chunks = []
        for res in generator:
            if hasattr(res, "audio") and res.audio is not None:
                chunk = res.audio
                if isinstance(chunk, torch.Tensor):
                    chunk = chunk.detach().cpu().numpy()
                chunks.append(chunk.squeeze())
        
        if not chunks:
            raise RuntimeError(f"Failed to generate audio for {sid}")
        
        full_audio = np.concatenate(chunks).astype(np.float32)
        sf.write(str(raw_wav), full_audio, 24000)
        dur_raw = len(full_audio) / 24000.0
        print(f"  Generated raw speech: {dur_raw:.2f}s in {time.time() - t_gen:.2f}s -> {raw_wav.name}")

        # 1. Normalize voice to EBU R128 (-16 LUFS)
        cmd_norm = [
            "ffmpeg", "-y", "-i", str(raw_wav),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar", "44100", "-ac", "2",
            str(norm_wav)
        ]
        subprocess.run(cmd_norm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # 2. Get exact normalized duration
        with wave.open(str(norm_wav), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            dur = frames / float(rate)
        
        # Add 0.60s trailing visual breathing room
        scene_dur = round(dur + 0.60, 2)
        scene_durations[sid] = {
            "voice_duration": round(dur, 2),
            "scene_duration": scene_dur,
            "text": text
        }

        # 3. Master mix with subtle laboratory ambient drone
        cmd_mix = [
            "ffmpeg", "-y",
            "-i", str(norm_wav),
            "-f", "lavfi", "-i", f"sine=frequency=55:duration={scene_dur}",
            "-filter_complex",
            f"[0:a]volume=1.0[voice];"
            f"[1:a]volume=0.03,afade=t=in:ss=0:d=1.5,afade=t=out:st={scene_dur-1.5}:d=1.5[amb];"
            f"[voice]apad=pad_dur=0.6[voice_pad];"
            f"[voice_pad][amb]amix=inputs=2:duration=first:dropout_transition=2[out]",
            "-map", "[out]",
            "-ar", "44100", "-ac", "2",
            str(master_wav)
        ]
        subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"  Master mixed -> {master_wav.name} (Duration: {scene_dur:.2f}s)")

    total_dur = sum(d["scene_duration"] for d in scene_durations.values())
    print("\n" + "=" * 80)
    print(f"BATCH SYNTHESIS COMPLETE: {len(SCENES)} scenes | Total Duration: {total_dur:.2f}s (> 60s)")
    print("=" * 80)

    manifest_path = OUTPUT_DIR / "durations.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(scene_durations, f, indent=2)
    print(f"Saved manifest: {manifest_path}")

if __name__ == "__main__":
    main()
