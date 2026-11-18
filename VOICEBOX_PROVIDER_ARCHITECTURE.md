# SUPER.INTELLIGENCEEE — Voicebox Provider Architecture

**Document Version:** 1.0.0  
**Date:** 2026-11-07T12:55:00+05:30  
**Architect:** Principal Software Systems Architect  
**Implementation:** `audio/providers/voicebox_provider.py`  

---

## 1. Architectural Overview & Component Diagram

The `VoiceboxProvider` serves as the modular adapter bridging SUPER.INTELLIGENCEEE's production pipeline with the local Voicebox REST API server.

```
+───────────────────────────────────────────────────────────────────────────────────+
|                           SUPER.INTELLIGENCEEE PIPELINE                           |
+───────────────────────────────────────────────────────────────────────────────────+
                                       │
                                       ▼
                     [ NarrationService / TechDocProducer ]
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
            [ VoiceboxProvider (Primary) ]    [ PiperEngine (Fallback) ]
                         │                           │
          ┌──────────────┴──────────────┐            ▼
          ▼                             ▼       assets/voices/
   POST /generate/stream         POST /generate  jarvis-high.onnx
          │                             │
          │                       GET /history/{id}
          │                             │
          │                       GET /audio/{id}
          └──────────────┬──────────────┘
                         ▼
        [ Local Voicebox REST API Server ] (http://127.0.0.1:17493)
                         │
                         ▼
             [ Kokoro-82M Neural Engine ] (24 kHz Mono Audio)
```

---

## 2. Interface Specification (`VoiceboxProvider`)

### 2.1 Configuration Parameters
The provider is initialized with configurable defaults overridable via environment variables or `config.yaml`:

```python
class VoiceboxProvider:
    DEFAULT_API_URL: str = "http://127.0.0.1:17493"
    DEFAULT_ENGINE: str = "kokoro"
    DEFAULT_MALE_VOICE: str = "bm_george"  # British RP Male
    DEFAULT_TIMEOUT_SEC: float = 45.0
```

- `VOICEBOX_API_URL`: Base URL for the running Voicebox server (default: `http://127.0.0.1:17493`).
- `VOICEBOX_ENGINE`: Active TTS engine (default: `kokoro`).
- `VOICEBOX_VOICE_ID`: Active preset voice ID (e.g. `bm_george`, `bm_daniel`, `am_adam`).
- `VOICEBOX_TIMEOUT_SEC`: HTTP socket timeout in seconds (default: `45.0`).

---

## 3. Core Method Contracts

### 3.1 Health & Availability
- **`check_health() -> Dict[str, Any]`**
  Executes a non-blocking `GET /health` call. Returns parsed status dictionary or error detail.
- **`is_available() -> bool`**
  Returns `True` only if `check_health()["healthy"] == True`. Guarantees fast failure detection before sending heavy speech generation requests.

### 3.2 Voice Profile & Preset Management
- **`list_profiles() -> List[Dict[str, Any]]`**
  Retrieves registered user profiles from `GET /profiles`.
- **`list_preset_voices(engine: str = "kokoro") -> List[Dict[str, Any]]`**
  Queries `GET /profiles/presets/{engine}` to discover engine voices dynamically.
- **`get_or_create_preset_profile(...) -> Dict[str, Any]`**
  Idempotently looks up an existing voice profile matching the specified engine and preset voice ID (e.g. `bm_george`). If absent, registers the profile via `POST /profiles`.

### 3.3 Speech Generation Execution Flow
`generate_speech(...)` implements a dual-path generation strategy:

```
[ generate_speech ]
        │
        ├─► Path 1: POST /generate/stream (Direct Streaming)
        │     │
        │     ├─► Success: Read raw WAV bytes directly -> validate audio file.
        │     └─► Failure / Timeout: Fall back to Path 2.
        │
        └─► Path 2: POST /generate (Background Job Queue)
              │
              ├─► Submit job -> receive job_id.
              ├─► Poll GET /history/{job_id} until status=="completed".
              ├─► GET /audio/{job_id} -> download WAV file.
              └─► On timeout: Trigger POST /generate/{job_id}/cancel.
```

---

## 4. Audio Output Validation

Every generated audio file must pass rigorous mathematical inspection in `validate_audio_file(file_path)` before being delivered to downstream compositors:

1. **Existence & Size:** File must exist and exceed 1,024 bytes.
2. **WAV Header Integrity:** Must open cleanly via Python's `wave` module.
3. **Channels & Rate:** Must report valid sample rates (24,000 Hz for Kokoro, 22,050 Hz for Piper).
4. **Minimum Duration:** Duration must exceed 0.20s (rejects truncated or empty clicks).
5. **Non-Zero Signal:** Audio must contain non-zero amplitude to reject silent frames.

---

## 5. Error Handling & Failover Guarantees

- **No Silent Failures:** Every fallback event logs an explicit warning detailing the exact root cause (e.g. `Voicebox connection timed out`).
- **No Uncontrolled Resource Consumption:** Generation jobs that exceed `timeout_seconds` issue an explicit cancellation request to free memory on the Voicebox worker queue.
- **Strict Male Voice Enforcement:** Fallbacks only route to verified male voices (`Piper jarvis-high` or `Windows SAPI David`).

