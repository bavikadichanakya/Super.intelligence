# SUPER.INTELLIGENCEEE — Phase 4.3 Dependency Inventory
## Complete Tooling, Package, Codec & Runtime Ecosystem Audit

**Document Version:** 1.0.0  
**Phase:** Phase 4.3 (Autonomous Video Production Architecture Transformation) — Phase 0 Gate  
**Date:** 2026-11-10T21:49:00+05:30  
**Author:** Lead Infrastructure & Tooling Systems Architect  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Host Environment:** Windows 11 Home 64-bit, Intel Core i5-1135G7, 8 GB RAM, ₹0 Budget  

---

## 1. Executive Tooling Summary

The SUPER.INTELLIGENCEEE production pipeline operates strictly as a **local-first, zero-mandatory-cost, zero-GPU-dependency** system. This inventory documents every installed package, runtime binary, media codec, audio provider, and prohibited dependency.

---

## 2. Python 3.11 Main Runtime Environment (`.\.venv\`)

The primary application logic, topic research, claim verification, database persistence, and orchestration execute within an isolated Python 3.11.15 virtual environment.

### 2.1 Package Inventory

| Package | Version | License | Functional Role in Architecture |
| :--- | :--- | :--- | :--- |
| `annotated-doc` | 0.0.5 | MIT | Type annotation inspection |
| `annotated-types` | 0.8.0 | MIT | Pydantic constraint metadata |
| `anyio` | 4.16.0 | MIT | Asynchronous concurrency abstraction |
| `beautifulsoup4` | 4.15.0 | MIT | Web scraping & HTML parsing for research feeds |
| `blinker` | 1.9.0 | MIT | In-process pub/sub signaling |
| `certifi` | 2026.10.23 | MPL-2.0 | Root SSL certificates for secure HTTPS |
| `cffi` | 2.1.1 | MIT | C-Foreign Function Interface |
| `charset-normalizer` | 3.5.2 | MIT | Encoding detection for raw text and feeds |
| `click` | 8.5.0 | BSD-3-Clause | CLI command parsing |
| `colorama` | 0.4.6 | BSD-3-Clause | Terminal ANSI color formatting on Windows |
| `comtypes` | 1.4.17 | MIT | Windows COM interface for SAPI speech |
| `coverage` | 7.17.1 | Apache 2.0 | Unit test code coverage measurement |
| `cryptography` | 50.0.2 | Apache 2.0 / BSD | Cryptographic hashing & token encryption |
| `fastapi` | 0.162.0 | MIT | REST API framework for dashboards & daemons |
| `feedparser` | 6.0.14 | BSD-2-Clause | RSS/Atom feed collection (arXiv, Nature, etc.) |
| `feedparser-sgmllib`| 2.1.0 | Python-2.0 | SGML parser compatibility for legacy feeds |
| `Flask` | 3.1.3 | BSD-3-Clause | Lightweight dashboard web interface |
| `flatbuffers` | 25.12.19 | Apache 2.0 | Efficient serialization for ONNX runtime |
| `h11` | 0.16.0 | MIT | HTTP/1.1 protocol state machine |
| `httpcore` | 1.0.9 | BSD-3-Clause | Core HTTP transport |
| `httpx` | 0.28.1 | BSD-3-Clause | Asynchronous HTTP client for API connectors |
| `idna` | 3.20 | BSD-3-Clause | Internationalized Domain Names in Applications |
| `iniconfig` | 2.3.1 | MIT | INI configuration parser for pytest |
| `itsdangerous` | 2.2.0 | BSD-3-Clause | Cryptographic data signing for sessions |
| `Jinja2` | 3.1.6 | BSD-3-Clause | Template rendering for compositions & captions |
| `lxml` | 6.1.3 | BSD-3-Clause | High-performance XML/HTML processing |
| `markdown-it-py` | 4.2.0 | MIT | Markdown parser for reports and scripts |
| `MarkupSafe` | 3.0.4 | BSD-3-Clause | String escaping for HTML security |
| `mdurl` | 0.1.2 | MIT | URL utilities for markdown-it |
| `numpy` | 2.4.6 | BSD-3-Clause | Numerical arrays, waveform data, image buffers |
| `onnxruntime` | 1.31.1 | MIT | Local inference engine for Piper TTS voice |
| `opentelemetry-api` | 1.45.2 | Apache 2.0 | System telemetry & tracing |
| `packaging` | 26.3 | Apache 2.0 / BSD | Python package version parsing |
| `pathvalidate` | 3.3.1 | MIT | Filesystem path sanitization on Windows |
| `pillow` | 13.0.0 | HPND | Image manipulation, thumbnailing, inspection |
| `pip` | 26.3 | MIT | Package management |
| `piper-tts` | 1.8.0 | MIT | Offline neural TTS engine (Jarvis male voice) |
| `pluggy` | 1.7.0 | MIT | Plugin management for pytest |
| `protobuf` | 7.36.2 | BSD-3-Clause | Protocol buffers for ONNX |
| `psutil` | 7.2.2 | BSD-3-Clause | RAM, CPU, disk telemetry & process monitoring |
| `pycparser` | 3.12 | BSD-3-Clause | C parser in Python |
| `pydantic` | 2.14.2 | MIT | Strict data contracts & schema validation |
| `pydantic_core` | 2.50.2 | MIT | Rust backend for high-speed Pydantic validation |
| `Pygments` | 2.21.0 | BSD-2-Clause | Syntax highlighting for terminal demonstrations |
| `pypiwin32` | 223 | PSF | Windows API extensions |
| `pytest` | 9.2.0 | MIT | Automated test framework |
| `pytest-cov` | 7.1.0 | MIT | Pytest coverage reporting |
| `python-dotenv` | 1.2.4 | BSD-3-Clause | Environment variable management |
| `python-multipart` | 0.0.33 | Apache 2.0 | Multipart form-data parser |
| `pyttsx3` | 2.99 | MPL-2.0 | Offline SAPI5 TTS fallback engine |
| `pywin32` | 312 | PSF | Low-level Windows OS bindings |
| `PyYAML` | 6.0.3 | MIT | YAML configuration parsing |
| `requests` | 2.34.2 | Apache 2.0 | Synchronous HTTP client |
| `rich` | 15.0.0 | MIT | Rich terminal formatting and diagnostics |
| `setuptools` | 84.2.1 | MIT | Build and distribution utilities |
| `shellingham` | 1.5.4 | BSD-3-Clause | Shell detection for CLI scripts |
| `soupsieve` | 4.0 | MIT | CSS selector support for BeautifulSoup |
| `starlette` | 1.10.0 | BSD-3-Clause | ASGI framework foundation |
| `tqdm` | 4.70.1 | MIT / MPL-2.0 | Progress bar rendering |
| `typer` | 0.27.3 | MIT | Type-driven CLI framework |
| `typing_extensions`| 4.16.0 | PSF | Modern typing backports for Python 3.11 |
| `typing-inspection`| 0.4.5 | MIT | Runtime type introspection |
| `urllib3` | 2.8.0 | MIT | Resilient HTTP transport client |
| `uvicorn` | 0.54.0 | BSD-3-Clause | High-performance ASGI web server |
| `Werkzeug` | 3.1.9 | BSD-3-Clause | WSGI web application library |
| `wheel` | 0.48.0 | MIT | Built-package format support |

---

## 3. Isolated Voicebox Environment (`external/voicebox/backend/venv/`)

Voicebox operates as an independent, fully isolated local service with its own dedicated Python 3.12 runtime.

### Key Components:
- **Python Version:** 3.12.x (64-bit)
- **PyTorch (CPU-Only):** `torch 2.6.0+cpu`, `torchaudio 2.6.0+cpu`
- **Kokoro TTS Engine:** `kokoro >= 0.8.4` (82M parameter neural voice model)
- **Voice Assets:** `am_liam` (General American Male, default), `bm_george` (British RP Male)
- **Phonemizers:** `phonemize`, `spacy`, `fugashi`
- **FastAPI Daemon:** Serves REST API on `http://127.0.0.1:17493` with `/generate/stream`, `/health`, and `/profiles`
- **Memory Footprint:** 650 MB RAM active during speech generation, 0 MB when idle.

---

## 4. Node.js & JavaScript Tooling Environment

The visual rendering layer leverages modern Node.js tooling for headless web-based composition:

### 4.1 Runtimes & CLIs
- **Node.js:** `v24.18.0` (x64 Windows)
- **npm:** `11.16.0`
- **HyperFrames CLI:** `v0.9.30` (invoked via `npx hyperframes` or local binary)
- **Chrome Headless Shell:** `win64-152.0.7977.30` (cached under `$HOME\.cache\hyperframes\chrome\`)

### 4.2 Renderer Dependencies (`renderer/package.json`)
- `gsap@3.15.0`: Timeline motion engine, SVG tweens, smooth interpolation.
- Google Fonts: `Inter` (neutral grotesque typography), `JetBrains Mono` (technical telemetry), `Caveat` (annotations).

---

## 5. Media Processing: FFmpeg & Codec Audit

The final media muxing, loudness normalization, and subtitle burning rely on the system-installed FFmpeg suite.

### 5.1 Binary Specifications
- **FFmpeg Version:** `9.0.1-full_build-www.gyan.dev`
- **FFprobe Version:** `9.0.1-full_build-www.gyan.dev`
- **Compiler:** Built with `gcc 16.1.0 (Rev2, Built by MSYS2 project)`
- **Configuration:** Static full build with all free codecs, filters, and hardware acceleration libraries enabled.

### 5.2 Required Audio Filters
- `loudnorm=I=-16.0:TP=-1.0:LRA=11.0`: EBU R128 two-pass integrated loudness normalization.
- `ebur128`: Real-time loudness metering and compliance verification.
- `amix=inputs=2:duration=first:dropout_transition=2`: Voice and background soundscape mixing.
- `volume`: Precise dynamic ducking (-16 dB attenuation during voice narration).

### 5.3 Required Video Codecs & Filters
- `libx264`: High-profile 1080×1920 30fps H.264 video encoding (`-pix_fmt yuv420p`, `-preset medium`, `-crf 19`).
- `aac`: High-quality AAC audio encoding (`-b:a 192k`, `-ar 48000`).
- `ass`: Advanced SubStation Alpha subtitle burn-in with custom styles and safe-zone clipping guards.
- `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920`: Clean 9:16 aspect ratio enforcement.
- `zoompan`: Smooth cinematic camera push-in (Ken Burns effect) for static high-resolution assets.

---

## 6. Target Multi-Engine Stack for Phase 1–3

To achieve true documentary visual quality without relying on presentation slides, the following specialized rendering engines are scheduled for acquisition:

| Engine | Technology / Runtime | Specialized Role in Video Production |
| :--- | :--- | :--- |
| **HyperFrames** | Node.js / Headless Chrome | Primary compositor, master 9:16 canvas, scene sequencing, real footage overlays, global transitions. |
| **Motion Canvas** | TypeScript / Vite | Algorithmic, dataflow, and mechanistic explainer animations (programmatic vector scenes). |
| **Manim Community** | Python 3.11 / Cairo | Mathematical formulas, coordinate spaces, scaling laws, and analytical proofs. |
| **Three.js** | WebGL / JavaScript | Procedural 3D models (neural networks, compute clusters, silicon wafers) rendered in headless Chrome. |
| **GSAP** | JavaScript | High-precision micro-interactions and coordinated motion timelines inside HyperFrames. |
| **Voicebox Kokoro** | Python 3.12 / ONNX | Primary studio-grade American male narration (24 kHz). |
| **FFmpeg** | C / Assembly Native | Master media multiplexing, audio mastering (-16 LUFS), subtitle burn-in, final MP4 delivery. |

---

## 7. Explicit Prohibition Register

### 7.1 BLENDER IS EXPLICITLY PROHIBITED
- **Mandate:** Under no circumstances shall Blender, Blender CLI, `bpy` Python package, or Blender rendering workflows be installed or used.
- **Technical Rationale:** Blender requires multi-gigabyte installations, heavy GPU compute, introduces unpredictable head-less rendering quirks on Windows, and violates the 8 GB RAM constraint.
- **Sanctioned Alternative:** All 3D procedural visualizations (clusters, nodes, topological surfaces) are authored using **Three.js** running in headless Chrome or SVG vector projections in **Motion Canvas**, consuming under 300 MB RAM on CPU.

### 7.2 Commercial API Paywalls
- **Mandate:** Zero mandatory paid APIs.
- **Sanctioned Fallbacks:**
  - Narration: Voicebox Kokoro (free local) / Piper (free local).
  - Stock Visuals: Wikimedia Commons (free open API) / NASA Media Library (free public domain) / Internet Archive / Pexels (free tier with synthetic fallback).
  - LLM / Research: Public arXiv API, RSS feeds, local heuristics.

