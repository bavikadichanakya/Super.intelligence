"""
Synthesizes speech and masters soundtrack for Phase 9.2 Complete Documentary.
"""
import sys
import wave
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from audio.providers.kokoro_direct import KokoroDirectRunner

AUDIO_DIR = WORKSPACE_ROOT / "output" / "productions" / "phase9_2_documentary" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    ("scene1_cryostat", "To protect fragile qubits from room-temperature noise, Willow is suspended inside a multi-stage dilution refrigerator, cooling superconducting circuits down to ten millikelvin."),
    ("scene2_architecture", "Beneath the gold thermal stages sits the processor: one hundred and five physical qubits arranged in an alternating checkerboard of data and syndrome ancillas."),
    ("scene3_error_healing", "When thermal decoherence flips a data qubit, adjacent syndrome detectors pinpoint the disturbance, firing a correction pulse in eight hundred and forty nanoseconds."),
    ("scene4_nature_scaling", "Published in Nature, Willow crossed the historic threshold: scaling physical qubits now exponentially suppresses error rates, proving the foundation of quantum memory."),
    ("scene5_supremacy_contrast", "In standard benchmarks, Willow completes in under five minutes a calculation that would take the fastest classical supercomputer ten septillion years."),
    ("scene6_conclusion_loop", "Practical quantum computing is no longer a distant theoretical dream: it is an operating machine, protected forever in the cold.")
]

def main():
    runner = KokoroDirectRunner(workspace_root=WORKSPACE_ROOT)
    print("=" * 80)
    print("PHASE 9.2: SPEECH SYNTHESIS & AUDIO MASTERING")
    print("=" * 80)
    
    scene_durations = []
    speech_files = []
    
    for sid, text in SCENES:
        speech_wav = AUDIO_DIR / f"{sid}_speech.wav"
        if speech_wav.exists() and speech_wav.stat().st_size > 10000:
            print(f"[REUSE] {sid}: existing {speech_wav.name}")
        else:
            print(f"[SYNTH] Generating speech for {sid}...")
            ok, meta = runner.generate(text, speech_wav, voice_id="am_liam", speed=1.0)
            if not ok:
                raise RuntimeError(f"Speech synthesis failed for {sid}")
                
        with wave.open(str(speech_wav), "rb") as wf:
            dur = wf.getnframes() / float(wf.getframerate())
            print(f"  {sid}: duration = {dur:.2f}s")
            scene_durations.append((sid, dur))
            speech_files.append(speech_wav)
            
    # Concatenate all speech tracks into one master speech file
    master_speech_wav = AUDIO_DIR / "master_documentary_speech.wav"
    concat_list = AUDIO_DIR / "speech_concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for sf in speech_files:
            f.write(f"file '{sf.resolve().as_posix()}'\n")
            
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(master_speech_wav)
    ]
    subprocess.run(cmd_cat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    with wave.open(str(master_speech_wav), "rb") as wf:
        total_speech_dur = wf.getnframes() / float(wf.getframerate())
    print(f"\n[MASTER SPEECH] Total concatenated duration = {total_speech_dur:.2f}s")
    
    # Generate continuous ambient harmonic pad bed matching total duration
    ambient_wav = AUDIO_DIR / "master_ambient_bed.wav"
    # Multi-harmonic drone with slow warm chord progression
    expr = (
        "0.05*sin(2*PI*65*t)+0.04*sin(2*PI*98*t)+0.03*sin(2*PI*130.81*t)+"
        "0.025*sin(2*PI*164.81*t)+0.02*sin(2*PI*196.00*t)+0.015*sin(2*PI*261.63*t)"
    )
    cmd_sfx = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"aevalsrc={expr}:s=48000:d={total_speech_dur:.2f}",
        "-af", "lowpass=f=2000,volume=0.5",
        str(ambient_wav)
    ]
    subprocess.run(cmd_sfx, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Master audio: voice + ducked ambient bed + EBU R128 (-16 LUFS)
    master_audio_wav = AUDIO_DIR / "master_documentary_soundtrack.wav"
    filter_complex = (
        "[1:a]volume=0.30[bg];"
        "[bg][0:a]sidechaincompress=threshold=0.08:ratio=4:attack=20:release=250[ducked_bg];"
        "[0:a]highpass=f=80,equalizer=f=3000:t=q:w=1.5:g=2.0[voice];"
        "[voice][ducked_bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        "[mixed]loudnorm=I=-16:TP=-1.0:LRA=6[out]"
    )
    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(master_speech_wav),
        "-i", str(ambient_wav),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", "48000",
        "-c:a", "pcm_s16le",
        str(master_audio_wav)
    ]
    subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[MASTER AUDIO] Finished mastered soundtrack: {master_audio_wav}")

if __name__ == "__main__":
    main()
