# SUPER.INTELLIGENCEEE — Voicebox Clone & Setup Report

**Document Version:** 1.0.0  
**Date:** 2026-11-07T12:53:00+05:30  
**Repository:** `https://github.com/jamiepine/voicebox.git`  
**Local Destination:** `A:\SUPER.INTELLIGENCEEE\external\voicebox`  
**Status:** **SUCCESSFULLY INSTALLED, CONFIGURED & VERIFIED**  

---

## 1. Git Repository & Clone Audit

| Parameter | Observed Status |
| :--- | :--- |
| **Clone Directory** | `A:\SUPER.INTELLIGENCEEE\external\voicebox` |
| **Remote Origin** | `https://github.com/jamiepine/voicebox.git` |
| **Branch** | `main` (tracked to `origin/main`) |
| **Commit SHA** | `8af7efe` (Merge pull request #1168 from jamiepine/prep/pr-1062) |
| **Working Tree** | Clean; isolated in `external/voicebox` |
| **Project Boundary** | Zero intrusion into root project files; isolated provider interface |

---

## 2. Environment & Dependency Isolation

To protect the host project from dependency conflicts, Voicebox was configured in its dedicated, pinned virtual environment:

- **OS Environment:** Windows 11 64-bit
- **Host GPU:** Intel(R) Iris(R) Xe Graphics (Integrated 1 GB VRAM, CPU execution primary)
- **Host RAM Budget:** 8,019,564 KB (~7.65 GB total / 8 GB RAM cap)
- **Python Version:** Python 3.12.13 (via `C:\Users\bavik\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe`)
- **Virtual Environment:** `A:\SUPER.INTELLIGENCEEE\external\voicebox\backend\venv`
- **PyTorch Installation:** CPU-only wheel (`torch==2.15.0+cpu`, `torchaudio==2.11.1+cpu`) to avoid downloading massive 2.5GB CUDA wheels on non-NVIDIA hardware.
- **Installed Packages:** 159 packages installed cleanly (including `fastapi==0.162.0`, `uvicorn==0.54.0`, `kokoro==0.9.4`, `misaki==0.9.4`, `pedalboard==0.9.26`, `soundfile==0.14.0`, `fastmcp==4.1.6`).

---

## 3. Server Architecture & Local Runtime Status

Voicebox runs as an independent local FastAPI REST API server:

- **Local Address:** `http://127.0.0.1:17493`
- **API Documentation (Swagger UI):** `http://127.0.0.1:17493/docs`
- **OpenAPI Schema:** `http://127.0.0.1:17493/openapi.json`
- **Health Check Endpoint:** `http://127.0.0.1:17493/health`
- **Model Status Endpoint:** `http://127.0.0.1:17493/models/status`
- **Voice Profile Endpoint:** `http://127.0.0.1:17493/profiles`
- **Preset Catalog Endpoint:** `http://127.0.0.1:17493/profiles/presets/{engine}`
- **Speech Generation Endpoints:**
  - `POST /generate/stream` (Synchronous direct WAV streaming)
  - `POST /generate` (Asynchronous queue-based job generation)
  - `GET /audio/{generation_id}` (Audio download endpoint)
  - `POST /speak` (Agent speech wrapper)
  - `/mcp` (Mounted FastMCP endpoint)

### Health Check Verification Response:
```json
{
  "status": "healthy",
  "model_loaded": false,
  "model_downloaded": null,
  "model_size": null,
  "gpu_available": false,
  "gpu_type": null,
  "vram_used_mb": null,
  "backend_type": "pytorch",
  "backend_variant": "cpu",
  "supports_rocm": false,
  "gpu_compatibility_warning": null,
  "cloud_enabled": false
}
```

---

## 4. Model Verification & Audio Generation Proof

In strict accordance with the 8 GB RAM constraint, the lightweight **Kokoro-82M** engine was initialized:

- **Model ID:** `hexgrad/Kokoro-82M` (82M parameters, 313 MB on disk)
- **Engine Capabilities:** 54 preset voices, CPU real-time inference, 24,000 Hz broadcast-ready audio.
- **Registered Male Profiles:**
  - `George British RP` (`bm_george`, Profile ID: `9e53847d-c226-4a70-b30c-7466579b7375`)
  - `Adam American Male` (`am_adam`, Profile ID: `143017a8-8e7a-4f05-9564-f68e5e650403`)
- **Speech Generation Verification:**
  - Streaming Test: `output/voice_samples/test_voicebox_stream.wav` (287,084 bytes, 5.98s, 24 kHz mono)
  - Async Queue Test: `output/voice_samples/test_voicebox_async.wav` (191,084 bytes, 3.98s, 24 kHz mono)
  - Direct Directed Render: `output/voice_samples/test_directed_narration.wav` (23.64s, 24 kHz mono, 5 segments)

---

## 5. Reliability & Restartability

The Voicebox backend was tested for shutdown and restart reliability:
- Can be terminated via process cancellation (`SIGTERM` / task kill).
- Can be launched via `cd external/voicebox; .\backend\venv\Scripts\python.exe -m backend.main --port 17493 --host 127.0.0.1`.
- The database (`data/voicebox.db`) maintains persistence across restarts.
- Unload mechanisms free memory on shutdown.

---

## 6. Known Limitations on Host Hardware

1. **No Hardware CUDA Acceleration:** Host GPU is an integrated Intel Iris Xe (1 GB VRAM). All neural inference runs via CPU multithreading.
2. **Heavy Model Precaution:** 1.7B parameter models (e.g. Qwen3-TTS 1.7B, TADA 3B) require ~4–6 GB RAM and should not be loaded on this 8 GB machine to prevent swapping. Kokoro-82M remains the optimal engine with an RSS footprint under 1 GB.

