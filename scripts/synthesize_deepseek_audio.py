"""
SUPER.INTELLIGENCEEE — Audio Synthesis for DeepSeek-R1 Spotlight
Voice: Kokoro-82M am_liam (General American English, male, documentary cadence).
Produces scene audio WAV files and master-mixed audio with ambient sound design.
"""

import os
import sys
import wave
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from audio.providers.kokoro_direct import KokoroDirectRunner

PROD_DIR = WORKSPACE_ROOT / "output" / "drafts" / "deepseek_r1_documentary"
AUDIO_DIR = PROD_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

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
    print("SYNTHESIZING DEEPSEEK-R1 DOCUMENTARY AUDIO (Kokoro-82M am_liam)")
    print("=" * 80)

    runner = KokoroDirectRunner()
    if not runner.is_available():
        print("ERROR: KokoroDirectRunner not available!")
        sys.exit(1)

    scene_durations = {}

    for sid, text in SCENES:
        raw_wav = AUDIO_DIR / f"{sid}_voice_raw.wav"
        norm_wav = AUDIO_DIR / f"{sid}_voice.wav"
        master_wav = AUDIO_DIR / f"{sid}_master.wav"

        print(f"\n[VOICE] Synthesizing {sid}...")
        runner.generate(text=text, output_wav_path=raw_wav, voice_id="am_liam", speed=1.0)

        # 1. Normalize voice to EBU R128 (-16 LUFS)
        cmd_norm = [
            "ffmpeg", "-y", "-i", str(raw_wav),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar", "44100", "-ac", "2",
            str(norm_wav)
        ]
        subprocess.run(cmd_norm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # 2. Get exact duration
        with wave.open(str(norm_wav), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            dur = frames / float(rate)
        
        # Add 0.6s trailing visual breathing room
        scene_dur = round(dur + 0.60, 2)
        scene_durations[sid] = scene_dur

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
        print(f"  -> Generated {master_wav.name}: Voice {dur:.2f}s | Scene Duration: {scene_dur:.2f}s")

    total_dur = sum(scene_durations.values())
    print("\n" + "=" * 80)
    print(f"TOTAL DOCUMENTARY DURATION: {total_dur:.2f} seconds (> 60s)")
    print("=" * 80)

    # Save manifest
    manifest_path = AUDIO_DIR / "durations.json"
    import json
    with open(manifest_path, "w") as f:
        json.dump(scene_durations, f, indent=2)
    print(f"Saved manifest to {manifest_path}")

if __name__ == "__main__":
    main()
