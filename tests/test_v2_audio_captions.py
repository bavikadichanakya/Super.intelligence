"""
Tests for Audio and Caption subsystems: Piper TTS, Audio Mixer (-16 LUFS), Captions (SRT/VTT/ASS), Whisper QA.
"""

import pytest
import wave
from pathlib import Path
from audio.narration import NarrationService
from audio.audio_mixer import AudioMixer
from captions.caption_generator import CaptionGenerator
from captions.whisper_qa import WhisperQA

def test_narration_synthesis(tmp_path):
    svc = NarrationService()
    test_out = tmp_path / "test_synth.wav"
    res = svc.synthesize_speech(
        text="Welcome to Super Intelligence. Autonomous offline media production.",
        output_filename=str(test_out)
    )
    assert res["success"] is True
    assert Path(res["path"]).exists()
    assert Path(res["path"]).stat().st_size > 1000
    assert res["duration_seconds"] > 1.0

def test_audio_mixer_loudnorm(tmp_path):
    svc = NarrationService()
    mixer = AudioMixer()
    
    # Synthesize two short clips
    f1 = svc.synthesize_speech("First technology update.", str(tmp_path / "clip1.wav"))
    f2 = svc.synthesize_speech("Second technology breakthrough.", str(tmp_path / "clip2.wav"))
    
    # Concat
    concat_out = tmp_path / "concat.wav"
    mixer.concatenate_scenes([f1["path"], f2["path"]], concat_out)
    assert concat_out.exists()
    assert concat_out.stat().st_size > 5000
    
    # Normalize to -16 LUFS
    norm_out = tmp_path / "normalized.wav"
    mixer.normalize_loudness(concat_out, norm_out, target_lufs=-16.0)
    assert norm_out.exists()
    assert norm_out.stat().st_size > 5000

def test_caption_generator(tmp_path):
    gen = CaptionGenerator()
    dummy_storyboard = {
        "scenes": [
            {"scene_index": 1, "duration": 4.0, "narration_text": "Did you see what just happened in AI?"},
            {"scene_index": 2, "duration": 5.0, "narration_text": "Researchers just unlocked sub quadratic attention scaling."}
        ]
    }
    caps = gen.generate_captions_from_storyboard(dummy_storyboard, tmp_path, base_name="test_caps")
    assert caps["srt"].exists()
    assert caps["vtt"].exists()
    assert caps["ass"].exists()
    assert caps["json"].exists()
    
    srt_content = caps["srt"].read_text(encoding="utf-8")
    assert "-->" in srt_content
    assert "DID YOU SEE WHAT" in srt_content

def test_whisper_qa(tmp_path):
    svc = NarrationService()
    qa = WhisperQA()
    text = "Artificial intelligence is evolving at lightning speed."
    res = svc.synthesize_speech(text, str(tmp_path / "qa_test.wav"))
    qa_report = qa.verify_audio(res["path"], text)
    assert qa_report["passed"] is True
    assert qa_report["score"] > 0.5

