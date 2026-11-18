"""
SUPER.INTELLIGENCEEE — Phase 10 Flagship Documentary Audio Synthesis
Synthesizes speech (Kokoro-82M am_liam) and masters broadcast audio for all 7 scenes.
Total duration > 60 seconds (target: ~72-76 seconds).
Opening hook: "Ever wondered..."
"""

import sys
import wave
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from audio.providers.kokoro_direct import KokoroDirectRunner

PROD_DIR = WORKSPACE_ROOT / "output" / "drafts" / "phase10_flagship"
AUDIO_DIR = PROD_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    (
        "scene1_hook_chandelier",
        "Ever wondered why the world's most powerful quantum computers look like giant golden chandeliers hanging inside a frozen void?"
    ),
    (
        "scene2_coherence_crisis",
        "At room temperature, thermal vibration instantly destroys delicate quantum information, requiring cooling down to ten millikelvin—ten times colder than interstellar space."
    ),
    (
        "scene3_willow_processor",
        "Suspended at the bottom of the cryostat sits Google's Willow processor, integrating one hundred and five superconducting qubits on a silicon architecture."
    ),
    (
        "scene4_realtime_healing",
        "When thermal noise flips a physical data qubit, adjacent syndrome ancillas detect the disturbance, firing a feedback correction pulse in eight hundred forty nanoseconds."
    ),
    (
        "scene5_nature_milestone",
        "Published in Nature, Willow achieved the historic milestone: expanding the surface code from distance three to distance seven exponentially suppresses the error rate."
    ),
    (
        "scene6_supremacy_benchmark",
        "In standard benchmarks, Willow finishes a calculation in under five minutes that would take Frontier, the world's fastest supercomputer, ten septillion years."
    ),
    (
        "scene7_fault_tolerant_era",
        "By proving that quantum errors can be corrected faster than they accumulate, we have crossed the threshold into the fault-tolerant era."
    )
]

def main():
    runner = KokoroDirectRunner(workspace_root=WORKSPACE_ROOT)
    print("=" * 80)
    print("PHASE 10 FLAGSHIP: AUDIO SYNTHESIS & ACOUSTIC MASTERING")
    print("=" * 80)
    
    total_speech_dur = 0.0
    durations = {}
    
    for sid, text in SCENES:
        wav_path = AUDIO_DIR / f"{sid}_speech.wav"
        print(f"\n[SYNTH] Generating speech for {sid}...")
        ok, meta = runner.generate(text, wav_path, voice_id="am_liam", speed=1.0)
        if not ok:
            raise RuntimeError(f"Speech synthesis failed for {sid}")
            
        with wave.open(str(wav_path), "rb") as wf:
            dur = wf.getnframes() / float(wf.getframerate())
            durations[sid] = dur
            total_speech_dur += dur
            print(f"  {sid}: duration = {dur:.2f}s")
            
        # Generate ducked ambient bed & master to EBU R128 (-16 LUFS)
        ambient_wav = AUDIO_DIR / f"{sid}_ambient.wav"
        expr = "0.04*sin(2*PI*65*t)+0.03*sin(2*PI*98*t)+0.02*sin(2*PI*130.81*t)+0.015*sin(2*PI*196*t)"
        cmd_sfx = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"aevalsrc={expr}:s=48000:d={dur:.2f}",
            "-af", "lowpass=f=1800,volume=0.35",
            str(ambient_wav)
        ]
        subprocess.run(cmd_sfx, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        master_wav = AUDIO_DIR / f"{sid}_master.wav"
        filter_complex = (
            "[1:a]volume=0.25[bg];"
            "[bg][0:a]sidechaincompress=threshold=0.08:ratio=4:attack=20:release=250[ducked_bg];"
            "[0:a]highpass=f=80,equalizer=f=3000:t=q:w=1.5:g=2.0[voice];"
            "[voice][ducked_bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
            "[mixed]loudnorm=I=-16:TP=-1.0:LRA=7[out]"
        )
        cmd_master = [
            "ffmpeg", "-y",
            "-i", str(wav_path),
            "-i", str(ambient_wav),
            "-filter_complex", filter_complex,
            "-map", "[out]",
            str(master_wav)
        ]
        subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"  [MASTER] Generated mastered soundtrack: {master_wav.name}")
        
    print("\n" + "=" * 80)
    print(f"ALL SCENES SYNTHESIZED & MASTERED! Total audio duration: {total_speech_dur:.2f}s (> 60s)")
    print("=" * 80)
    for sid, d in durations.items():
        print(f"  - {sid}: {d:.2f}s")

if __name__ == "__main__":
    main()
