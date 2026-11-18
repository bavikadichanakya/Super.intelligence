# SUPER.INTELLIGENCEEE — Voicebox Integration Audit

**Document Version:** 1.0.0  
**Date:** 2026-11-07T12:54:00+05:30  
**Auditor:** Principal AI Systems Architect & Audio Post-Production Lead  
**Scope:** Architecture inspection of existing audio subsystems and local Voicebox capabilities  

---

## 1. Existing Audio Pipeline Inspection

Prior to this integration, the audio generation pipeline in `A:\SUPER.INTELLIGENCEEE` was composed of:

1. **`audio/narration.py` (`NarrationService`):**
   - Dispatched speech synthesis to local `PiperEngine`.
   - Used Windows SAPI `pyttsx3` as a secondary fallback.
   - Enforced male voice generation via model naming checks (`jarvis-high`, `David`).
   - Lacked modular provider abstractions (tightly coupled to Piper and pyttsx3 classes).
2. **`audio/piper_engine.py` (`PiperEngine`):**
   - Executed ONNX Runtime inference using `assets/voices/jarvis-high.onnx`.
   - Sample rate: 22,050 Hz 16-bit mono PCM.
   - High intelligibility but limited emotional range and fixed British persona.
3. **`audio/pyttsx3_engine.py` (`Pyttsx3Engine`):**
   - Legacy Windows SAPI COM wrapper.
   - Fast (0.14x RTF) but robotic and flat (MOS 2.5/5.0).
4. **`audio/audio_mixer.py` & `creative/tech_documentary/sound_design/sound_designer.py`:**
   - Multi-layer audio mixing combining voice narration, 55 Hz ambient sub-bass drone, and diegetic sound effects.
   - FFmpeg `loudnorm` filter mastering final mix to **-14.0 LUFS** (EBU R128 standard).
   - Side-chain ducking (-16 dB) during active dialogue.

---

## 2. Voicebox Environment & Local API Discovery

Voicebox was cloned from the official repository (`https://github.com/jamiepine/voicebox.git`) into `external/voicebox` to preserve repository boundaries.

### Local API Discovery Findings:
- **Default Port:** `17493` (configured across `backend/main.py`, `app.py`, and `justfile`).
- **REST Endpoints Audited:**
  - `GET /health`: Returns runtime status, GPU detection, and loaded model metadata.
  - `GET /docs`: Interactive Swagger UI documentation.
  - `GET /models/status`: Complete status catalog of all 8 TTS engines, Whisper STT, and local LLM models.
  - `GET /profiles`: Returns registered voice profiles and their underlying presets or clones.
  - `GET /profiles/presets/{engine}`: Discovers built-in preset voices (e.g. all 54 voices for Kokoro).
  - `POST /generate/stream`: Real-time streaming WAV generation.
  - `POST /generate`: Asynchronous job submission to the background worker queue.
  - `GET /history/{id}`: Polls task status (`generating`, `completed`, `failed`).
  - `GET /audio/{id}`: Downloads the completed WAV file for completed jobs.
  - `POST /generate/{id}/cancel`: Gracefully cancels running/queued generation tasks.
  - `/mcp`: FastMCP endpoint exposing `voicebox_speak` and `voicebox_transcribe`.

---

## 3. Host System Resource Audit (8 GB RAM Constraint)

The host machine was profiled before model loading:
- **Total Physical RAM:** 8,019,564 KB (~7.65 GB visible).
- **Available Free RAM:** 862,172 KB (~842 MB free at idle).
- **Graphics Subsystem:** Intel(R) Iris(R) Xe Graphics (Integrated 1 GB shared VRAM).
- **Operating Constraint:** Because there is no discrete NVIDIA GPU with dedicated VRAM, all PyTorch models execute via CPU multithreading.
- **Model Load Capacity:**
  - Kokoro-82M (82M params, ~313 MB disk): **Compatible & Recommended.** Fits comfortably in memory (peak RAM ~999 MB).
  - Qwen CustomVoice 0.6B (0.6B params, ~1.2 GB disk): **Marginal.** Risk of memory swapping on 8 GB RAM when compositing video simultaneously.
  - 1.7B+ models (Qwen 1.7B, TADA 3B): **Incompatible.** Exceeds free physical RAM.

---

## 4. Integration Blueprint & Guardrails

1. **Isolation Guarantee:** Voicebox lives exclusively in `external/voicebox/` with its own Python 3.12 venv.
2. **Provider Pattern:** All communication occurs over local loopback HTTP via `audio/providers/voicebox_provider.py`.
3. **Cadence & Tag Guard:** `VoiceDirector` in `audio/narration/voice_director.py` strips unsupported paralinguistic tags before sending to engines like Kokoro that would otherwise speak tags literally.
4. **Segmented Rendering & Crossfading:** `NarrationRenderer` renders clause-by-clause, trims dead air, crossfades boundaries, and emits a timing manifest.
5. **No Silent Fallback:** If Voicebox is unavailable, `NarrationService` explicitly logs warnings and falls back to Piper `jarvis-high` while recording provenance metadata.

