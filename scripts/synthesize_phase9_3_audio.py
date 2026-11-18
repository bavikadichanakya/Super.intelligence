"""
Synthesizes speech and masters audio for Phase 9.3 Prototypes (Kokoro-82M am_liam).
"""
import sys
import wave
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from audio.providers.kokoro_direct import KokoroDirectRunner

AUDIO_DIR = WORKSPACE_ROOT / "output" / "drafts" / "phase9_3" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

PROTOTYPES = [
    ("proto_a_hardware", "To preserve delicate quantum coherence, superconducting transmons are housed inside a multi-stage dilution refrigerator, cooling gold-plated copper stages down to ten millikelvin."),
    ("proto_b_mechanism", "When thermal noise flips a physical data qubit, adjacent syndrome ancillas detect the parity disturbance, firing a feedback correction pulse in eight hundred and forty nanoseconds."),
    ("proto_c_evidence", "Published in Nature, Willow achieved the historic milestone: expanding the surface code from distance three to distance seven exponentially suppresses the logical error rate.")
]

def main():
    runner = KokoroDirectRunner(workspace_root=WORKSPACE_ROOT)
    print("=" * 80)
    print("PHASE 9.3: PROTOTYPE AUDIO SYNTHESIS & ACOUSTIC TIMING")
    print("=" * 80)
    
    for pid, text in PROTOTYPES:
        wav_path = AUDIO_DIR / f"{pid}_speech.wav"
        print(f"\n[SYNTH] Generating speech for {pid}...")
        ok, meta = runner.generate(text, wav_path, voice_id="am_liam", speed=1.0)
        if not ok:
            raise RuntimeError(f"Speech synthesis failed for {pid}")
            
        with wave.open(str(wav_path), "rb") as wf:
            dur = wf.getnframes() / float(wf.getframerate())
            print(f"  {pid}: duration = {dur:.2f}s")
            
        # Generate ducked ambient bed & master to EBU R128 (-16 LUFS)
        ambient_wav = AUDIO_DIR / f"{pid}_ambient.wav"
        expr = "0.04*sin(2*PI*65*t)+0.03*sin(2*PI*98*t)+0.02*sin(2*PI*130.81*t)+0.015*sin(2*PI*196*t)"
        cmd_sfx = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"aevalsrc={expr}:s=48000:d={dur:.2f}",
            "-af", "lowpass=f=1800,volume=0.35",
            str(ambient_wav)
        ]
        subprocess.run(cmd_sfx, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        master_wav = AUDIO_DIR / f"{pid}_master.wav"
        filter_complex = (
            "[1:a]volume=0.25[bg];"
            "[bg][0:a]sidechaincompress=threshold=0.08:ratio=4:attack=20:release=250[ducked_bg];"
            "[0:a]highpass=f=80,equalizer=f=3000:t=q:w=1.5:g=2.0[voice];"
            "[voice][ducked_bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
            "[mixed]loudnorm=I=-16:TP=-1.0:LRA=6[out]"
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

if __name__ == "__main__":
    main()
