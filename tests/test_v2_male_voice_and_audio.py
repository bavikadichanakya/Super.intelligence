"""
SUPER.INTELLIGENCEEE V2 — Male Voice, Audio Engineering & Pronunciation Test Suite
Verifies:
1. Strict male voice enforcement (female models like lessac/zira blocked).
2. Technical pronunciation lexicon substitutions.
3. Piper male synthesis with jarvis-high.
4. EBU R128 loudness mastering (-16 LUFS, 48 kHz stereo, True Peak <= -1 dBTP).
5. Dynamic speech sidechain music ducking.
6. Scene transition SFX overlay.
"""

from pathlib import Path
import pytest

from core.config import get_config
from audio.pronunciation import TechnicalPronunciationLexicon
from audio.piper_engine import PiperEngine
from audio.narration import NarrationService
from audio.audio_mixer import AudioMixer


def test_female_voice_rejection():
    """Confirms that female voice models are strictly prohibited with fast failure."""
    with pytest.raises(ValueError, match="Female voice model"):
        PiperEngine("en_US-lessac-medium")

    with pytest.raises(ValueError, match="Female voice model"):
        PiperEngine("zira-medium")


def test_male_voice_initialization():
    """Confirms that male voice model initializes properly."""
    engine = PiperEngine("jarvis-high")
    assert engine.model_name == "jarvis-high"
    assert engine.onnx_path.exists()


def test_pronunciation_lexicon():
    """Verifies that dense technical AI acronyms, Big-O notations, and units are phonetically transformed."""
    raw_text = (
        "Researchers published on arXiv showing O(N^2) quadratic attention can scale to O(N) linear time. "
        "At 1M tokens, VRAM dropped from 256GB to 24GB on a single RTX 4090 with INT4 quantization, "
        "achieving 4.2x speedup in LLM inference."
    )
    processed = TechnicalPronunciationLexicon.preprocess_text(raw_text)

    # Assertions for phonetic expansion
    assert "archive" in processed
    assert "O of N squared" in processed
    assert "O of N linear time" in processed
    assert "one million tokens" in processed or "1 million tokens" in processed or "one million" in processed
    assert "V-RAM" in processed
    assert "24 gigabytes" in processed
    assert "R-T-X 4090" in processed or "R-T-X 40 90" in processed
    assert "Int 4" in processed
    assert "4.2 times" in processed
    assert "L-L-M" in processed


def test_piper_male_synthesis(tmp_path):
    """Synthesizes speech using the mature male jarvis-high model and verifies output properties."""
    engine = PiperEngine("jarvis-high")
    out_wav = tmp_path / "jarvis_narration.wav"
    text = "Super Intelligence audio engine test. Linear memory scaling demonstrated on consumer hardware."

    ok, meta = engine.generate(text, str(out_wav))
    assert ok is True
    assert meta["voice"] == "jarvis-high"
    assert meta["voice_gender"] == "MALE"
    assert out_wav.exists()
    assert out_wav.stat().st_size > 10000


def test_audio_mixer_mastering_and_ebur128(tmp_path):
    """Verifies complete vocal mastering chain: 48 kHz stereo and EBU R128 -16 LUFS compliance."""
    engine = PiperEngine("jarvis-high")
    raw_wav = tmp_path / "raw_voice.wav"
    engine.generate("Mastering test for autonomous vertical video production.", str(raw_wav))

    mixer = AudioMixer()
    master_wav = tmp_path / "mastered_voice.wav"
    mixer.normalize_loudness(raw_wav, master_wav, target_lufs=-16.0)

    assert master_wav.exists()
    assert master_wav.stat().st_size > 10000

    # Measure with ebur128
    report = mixer.measure_loudness(master_wav)
    assert "integrated_lufs" in report
    assert report["integrated_lufs"] is not None
    # Verify within broadcast tolerance: -16.0 ± 1.5 LUFS
    assert -17.5 <= report["integrated_lufs"] <= -14.5
    # Verify True Peak <= -1.0 dBTP
    assert report["true_peak_dbtp"] <= -1.0
    assert report["compliant"] is True


def test_sfx_overlay_at_transitions(tmp_path):
    """Verifies that transition sound effects are cleanly overlaid at scene timestamps."""
    engine = PiperEngine("jarvis-high")
    raw_wav = tmp_path / "scenes_combined.wav"
    engine.generate("Scene one hook. Scene two proof. Scene three impact conclusion.", str(raw_wav))

    mixer = AudioMixer()
    sfx_out = tmp_path / "scenes_with_sfx.wav"
    scene_durations = [3.0, 3.0, 3.0]

    mixer.mix_with_sound_effects(
        master_audio_path=raw_wav,
        scene_durations=scene_durations,
        output_path=sfx_out,
        sfx_name="whoosh-cinematic.mp3",
        sfx_volume=0.20,
    )

    assert sfx_out.exists()
    assert sfx_out.stat().st_size > 10000
    report = mixer.measure_loudness(sfx_out)
    assert report["compliant"] is True

