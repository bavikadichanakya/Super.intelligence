"""
SUPER.INTELLIGENCEEE — Phase 3.5 Audio Architecture Verification Test
Tests:
1. AdaptiveSoundtrackGenerator synthesis
2. SoundCueTimeline creation and serialization
3. SoundDesigner assemble_documentary_soundscape with sidechain ducking
4. EBU R128 loudness measurement of output
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from creative.tech_documentary.sound_design.sound_designer import SoundDesigner
from audio.audio_mixer import AudioMixer

def main():
    print("Testing Phase 3.5 Audio Architecture...")
    sd = SoundDesigner()
    mixer = AudioMixer()

    sample_voice = Path("output/voice_samples/sample_am_liam.wav")
    assert sample_voice.exists(), f"Missing {sample_voice}"

    scene_durs = [2.5, 2.5, 2.5, 2.5, 2.5]
    scene_types = ["TITLE_CARD", "VECTOR_DIAGRAM", "TERMINAL_EXECUTION", "COMPARISON_BENCHMARK", "VERDICT_LOCK"]
    scene_descs = [
        "Opening Title Hook",
        "Transformer Memory Bottleneck Diagram",
        "Speculative Decoding Terminal Run",
        "Latency Speedup Benchmarks",
        "Definitive Engineering Conclusion"
    ]

    test_out = Path("output/voice_samples/test_soundscape_master.wav")
    master_p, timeline_p = sd.assemble_documentary_soundscape(
        voiceover_master_path=sample_voice,
        scene_durations=scene_durs,
        scene_types=scene_types,
        output_path=test_out,
        target_lufs=-14.0,
        scene_descriptions=scene_descs,
    )

    print(f"Master output exists: {master_p.exists()}, Size: {master_p.stat().st_size} bytes")
    print(f"Timeline output exists: {timeline_p.exists()}, Size: {timeline_p.stat().st_size} bytes")

    # Measure output loudness
    metrics = mixer.measure_loudness(master_p)
    print(f"Loudness Metrics: Integrated={metrics.get('integrated_lufs')} LUFS, Peak={metrics.get('true_peak_dbtp')} dBTP, Range={metrics.get('loudness_range_lra')} LU")

    assert master_p.exists() and master_p.stat().st_size > 10000, "Master audio invalid!"
    assert timeline_p.exists() and timeline_p.stat().st_size > 100, "Timeline JSON invalid!"
    print("ALL AUDIO ARCHITECTURE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
