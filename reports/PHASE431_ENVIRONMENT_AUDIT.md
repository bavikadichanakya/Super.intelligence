# SUPER.INTELLIGENCEEE — Phase 4.3.1 Forensic Environment Audit
## Comprehensive System, Tooling, Hardware & Runtime Verification

**Document Version:** 1.0.0  
**Phase:** Phase 4.3.1 (Rendering Framework Feasibility, Dependency Verification & Hardware Benchmark)  
**Date:** 2026-11-10T22:13:00+05:30  
**Author:** Lead Video Systems Architect & Systems Reliability Engineer  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Execution Environment:** Windows 11 Home 64-bit, Intel Core i5-1135G7, 8 GB RAM, ₹0 Budget  

---

## 1. Executive Environment Summary

This forensic audit documents the physical and logical runtime environment of the workstation, recording exact executable paths, package counts, storage allocations, memory pressure, and codec support.

---

## 2. Python Runtime Audit

### 2.1 Main Production Environment
- **Python Version:** `3.11.15 (main, Jun 23 2026, 15:20:37) [MSC v.1944 64 bit (AMD64)]`
- **Virtualenv Executable:** `A:\SUPER.INTELLIGENCEEE\.venv\Scripts\python.exe`
- **Virtualenv Root (`sys.prefix`):** `A:\SUPER.INTELLIGENCEEE\.venv`
- **Base Interpreter (`sys.base_prefix`):** `G:\JarvisModels\uv-python\cpython-3.11.15-windows-x86_64-none`
- **Active Packages in Site-Packages:** 203 directories / packages (includes core orchestration, FastAPI, Pydantic 2.14.2, NumPy 2.4.6, Pillow 13.0.0, Piper-TTS 1.8.0, and Manim Community 0.22.1).

### 2.2 Isolated Voicebox Environment
- **Path:** `A:\SUPER.INTELLIGENCEEE\external\voicebox\backend\venv\Scripts\python.exe`
- **Status:** **HEALTHY & VERIFIED**
- **Python Version:** 3.12 (64-bit)
- **Key Modules:** PyTorch CPU-Only (2.6.0+cpu), Kokoro TTS (82M neural model), Uvicorn, FastAPI, Phonemizers.
- **Service Endpoint:** `http://127.0.0.1:17493` (local REST daemon).

---

## 3. Node.js & Tooling Environment

| Binary | Exact Path | Version | Verification Status |
| :--- | :--- | :--- | :--- |
| **Node.js** | `C:\Program Files\nodejs\node.EXE` | `v24.18.0` | Active (win32 x64) |
| **npm** | `C:\Program Files\nodejs\npm.CMD` | `11.16.0` | Active |
| **npx** | `C:\Program Files\nodejs\npx.CMD` | `11.16.0` | Active |
| **HyperFrames CLI** | Temporary NPX Cache / Local | `v0.9.30` | Verified with `check` and `render` passes |

---

## 4. Media Processing Suite (FFmpeg & Codecs)

### 4.1 Binaries
- **FFmpeg:** `C:\Users\bavik\AppData\Local\Microsoft\WinGet\Links\ffmpeg.EXE`
- **FFprobe:** `C:\Users\bavik\AppData\Local\Microsoft\WinGet\Links\ffprobe.EXE`
- **Build Version:** `9.0.1-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers` (built with `gcc 16.1.0`).

### 4.2 Verified Codecs & Filters
- **Video Encoders:** `libx264` (H.264 High/Main/Baseline), `h264_qsv` (Intel QuickSync), `ffv1` (lossless archive).
- **Audio Encoders:** `aac` (Advanced Audio Coding, native), `libmp3lame`, `flac`, `pcm_s16le`.
- **EBU R128 Mastering Filters:** `loudnorm` (two-pass integrated loudness), `ebur128` (real-time metering).
- **Video Motion & Composition Filters:** `scale` (bicubic/lanczos), `crop`, `overlay` (alpha blending), `zoompan` (Ken Burns push-in), `concat` (seamless stream splicing).
- **Subtitle Burner:** `ass` (libass native Advanced SubStation Alpha subtitle renderer).

---

## 5. Headless Chrome & GPU Environment

### 5.1 Headless Chrome Shell
- **Cache Location:** `C:\Users\bavik\.cache\hyperframes\chrome\`
- **Binary:** `C:\Users\bavik\.cache\hyperframes\chrome\chrome-headless-shell\win64-152.0.7977.30\chrome-headless-shell-win64\chrome-headless-shell.exe`
- **Execution Mode:** Headless Shell with hardware GPU acceleration via ANGLE Direct3D11.

### 5.2 GPU & Graphics Capabilities
- **Processor:** Intel Core i5-1135G7 @ 2.40 GHz (Family 6 Model 140 Stepping 1).
- **GPU:** Intel Iris Xe Integrated Graphics (`vendor="Google Inc. (Intel)" renderer="ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)"`).
- **Dedicated GPU:** **None (No NVIDIA discrete GPU, No CUDA).**
- **Software Fallback:** Chrome SwiftShader / ANGLE D3D11 WARP (verified functional when hardware acceleration is disabled).

---

## 6. Storage Allocation & Drive Headroom

| Partition | Total Space | Used Space | Free Space | Percent Used | Status / Architectural Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A:\\** | 150.39 GB | 143.51 GB | **6.88 GB** | 95.4% | Primary project workspace & designated `.temp` root |
| **C:\\** | 226.84 GB | 214.70 GB | **12.13 GB** | 94.7% | Operating system, Node runtime, Chrome cache |
| **G:\\** | 48.83 GB | 47.25 GB | **1.58 GB** | 96.8% | **CRITICAL LOW-SPACE ALERT: Excluded from temp caching** |

> [!CAUTION]
> **Drive G: Quarantine:** Drive G: possesses only 1.58 GB of free space. Standard Windows environment configurations pointing `%TEMP%` or `%TMP%` to user profiles on G: risk immediate OOM/disk crashes. All rendering scripts must explicitly force `TEMP`, `TMP`, and `HYPERFRAMES_EXTRACT_CACHE_DIR` to `A:\SUPER.INTELLIGENCEEE\.temp`.

---

## 7. Memory & CPU Profile

- **Physical RAM:** 7.65 GB Total.
- **Available RAM:** **0.66 GB – 1.20 GB** (Active memory pressure under host background load).
- **Pagefile / Swap:** 12.4 GB Total, 9.8 GB Free.
- **CPU Cores:** 4 Physical Cores / 8 Logical SMT Threads.
- **Architectural Directive:** Strict **sequential rendering execution**. Concurrency among heavy engines is strictly prohibited. Intermediate video stems must stream directly to disk or FFmpeg pipes without lingering in memory.

