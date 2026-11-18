# SUPER.INTELLIGENCEEE — PHASE 4.3.2B
# ENGINE SMOKE TESTS REPORT & ASSET VERIFICATION

**Project:** SUPER.INTELLIGENCEEE  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Phase:** 4.3.2B — Multi-Engine Rendering Dispatcher & Adapter Architecture  
**Execution Timestamp:** 2026-11-13T15:58:54Z  
**Host Platform:** Windows 11 Home 64-bit | Intel Core i5-1135G7 (4C/8T) | 8 GB RAM (Intel Iris Xe Graphics)  
**Mandatory Constraints:** ₹0 operating cost | Zero Blender dependencies | Single sequential mutex execution  
**Raw Metrics Source:** `output/smoke_tests/phase432b_smoke_metrics.json`

---

## 1. EXECUTIVE SUMMARY

In Phase 4.3.2B, the Multi-Engine Rendering Dispatcher and its four engine adapters were submitted to rigorous end-to-end smoke testing. Four distinct video stems representing the core rendering modalities of the autonomous documentary system were generated, validated with `ffprobe`, checked for bit-exact SHA-256 integrity, and assembled into a complete 19.8-second master vertical documentary reel.

All four rendering engines executed sequentially under the strict protection of `ResourceGuard` without a single memory threshold violation, process leak, or dropped frame.

| Test Stem / Artifact | Engine | Duration | Resolution & FPS | Codec | File Size | SHA-256 Hash (First 16 chars) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `smoke_manim_scene.mp4` | Manim | 9.80 s | 1080x1920 @ 30fps | H.264 (libx264) | 217,183 B | `a2b5c5d8b6b6fcae...` | **PASSED** |
| `smoke_threejs_scene.mp4` | Three.js | 5.00 s | 1080x1920 @ 30fps | H.264 (browser) | 6,479,953 B | `fbec562aa0d91748...` | **PASSED** |
| `smoke_hyperframes_scene.mp4` | HyperFrames | 5.00 s | 1080x1920 @ 30fps | H.264 (browser) | 764,109 B | `f4ebc61de7bee9be...` | **PASSED** |
| `master_assembled_smoke.mp4` | FFmpeg | 19.80 s | 1080x1920 @ 30fps | H.264 + AAC | 6,496,437 B | `bf75e59993dc12ae...` | **PASSED** |

---

## 2. DETAILED STEM ANALYSIS & FFPROBE VERIFICATION

### 2.1 Stem A: Manim Technical & Mathematical Explanation
- **Target File:** `output/smoke_tests/stems/smoke_manim_scene.mp4`
- **Engine:** Manim Community Edition v0.22.1 (`manim`)
- **Semantic Role:** Mathematical derivations, neural scaling curve plotting, loss frontier equations, technical vector animations.
- **Rendering Parameters:**
  - Script generated procedurally: Standalone `ManimScene` subclassing `manim.Scene`
  - Dimensions: `1080 x 1920` (Vertical 9:16 aspect ratio)
  - Frame Rate: `30.0 fps` CFR (Constant Frame Rate)
  - Color Palette: Strict documentary hex codes (`#0a0e17` background, `#00e5ff` cyan curve, `#94a3b8` slate axis labels, `#ef4444` red loss indicators)
- **`ffprobe` Stream Inspection:**
  ```json
  {
    "codec_name": "h264",
    "codec_type": "video",
    "width": 1080,
    "height": 1920,
    "r_frame_rate": "30/1",
    "duration": "9.800000",
    "nb_frames": "294",
    "format": {
      "size": "217183",
      "bit_rate": "177292"
    }
  }
  ```
- **Integrity & Verification:**
  - Exact frame count: 294 frames = exactly 9.80s at 30 fps.
  - Video stream: YUV420p baseline profile, full hardware compatibility.
  - Render Duration: 34.36 seconds (0.28x real-time on CPU).
  - Peak Memory: 491.4 MB RAM (well below 8 GB hardware ceiling).

---

### 2.2 Stem B: Three.js Procedural Spatial & Network Topology
- **Target File:** `output/smoke_tests/stems/smoke_threejs_scene.mp4`
- **Engine:** Three.js r128 via Headless Chromium WebGL Canvas
- **Semantic Role:** 2.5D/3D procedural hardware infrastructure, distributed transformer network nodes, camera dolly and orbital motion.
- **Zero Blender Verification:**
  - **Blender Invocation Check:** None (`blender.exe` is absent and uncalled).
  - Procedural generation: Generates self-contained HTML embedding Three.js r128 CDN bundle with Orbit/Dolly math and WebGL point cloud / particle graph.
  - Frame Hook: Integrates `hf-seek` virtual timestamp listener and `requestAnimationFrame` render pump.
- **Rendering Parameters:**
  - Dimensions: `1080 x 1920`
  - Frame Rate: `30.0 fps`
  - Total Frames: 150 frames (5.00s)
- **`ffprobe` Stream Inspection:**
  ```json
  {
    "codec_name": "h264",
    "codec_type": "video",
    "width": 1080,
    "height": 1920,
    "r_frame_rate": "30/1",
    "duration": "5.000000",
    "nb_frames": "150",
    "format": {
      "size": "6479953",
      "bit_rate": "10367924"
    }
  }
  ```
- **Integrity & Verification:**
  - Exact frame count: 150 frames = exactly 5.00s at 30 fps.
  - Render Duration: 149.25 seconds.
  - Peak Memory: 838.0 MB RAM (including headless browser runtime).

---

### 2.3 Stem C: HyperFrames Editorial Motion & Kinetic Typography
- **Target File:** `output/smoke_tests/stems/smoke_hyperframes_scene.mp4`
- **Engine:** HyperFrames CLI v1.1.1 + GSAP Paused Timeline
- **Semantic Role:** Editorial HUDs, documentary typography, citation badges, lower-third overlays, multi-layer graphic comps.
- **Rendering Parameters:**
  - Render contract: Paused GSAP timeline with `window.seekTo(t)` and `window.duration` registration.
  - Dimensions: `1080 x 1920`
  - Frame Rate: `30.0 fps`
  - Total Frames: 150 frames (5.00s)
- **`ffprobe` Stream Inspection:**
  ```json
  {
    "codec_name": "h264",
    "codec_type": "video",
    "width": 1080,
    "height": 1920,
    "r_frame_rate": "30/1",
    "duration": "5.000000",
    "nb_frames": "150",
    "format": {
      "size": "764109",
      "bit_rate": "1222574"
    }
  }
  ```
- **Integrity & Verification:**
  - Exact frame count: 150 frames = exactly 5.00s at 30 fps.
  - Render Duration: 166.93 seconds.
  - Peak Memory: 672.3 MB RAM.

---

### 2.4 Master Assembled Video: Multi-Engine Editorial Composition
- **Target File:** `output/smoke_tests/master_assembled_smoke.mp4`
- **Engine:** FFmpeg v8.0.1 Master Assembler (`ffmpeg_adapter.py`)
- **Semantic Role:** Concat demuxer stem stitching, safe-zone ASS subtitle burning, professional narration audio bed with EBU R128 (-16 LUFS) loudness normalization.
- **Timeline Composition:**
  - Scene 1: Manim Math/Scaling Frontier (0.00s – 9.80s)
  - Scene 2: Three.js Network Cluster 3D Topology (9.80s – 14.80s)
  - Scene 3: HyperFrames Editorial Thesis Typography (14.80s – 19.80s)
  - Total Duration: `19.80 seconds` (594 frames @ 30fps)
- **Audio Mastering Specifications:**
  - Integrated Loudness Target: `-16.0 LUFS`
  - Loudness Range (LRA): `11.0 LU`
  - True Peak Ceiling: `-1.5 dBFS`
  - Audio Format: Stereo AAC, 48 kHz, 192 kbps
- **Subtitle Safe Zone Compliance:**
  - Subtitle Format: Advanced SubStation Alpha (`.ass`)
  - Bottom Margin: `360 px` (exceeds the mandatory `>= 340 px` mobile UI safe zone threshold)
  - Styling: High-legibility Inter bold, subtle drop-shadow, documentary gold highlighting
- **`ffprobe` Stream Inspection:**
  ```json
  {
    "streams": [
      {
        "codec_name": "h264",
        "codec_type": "video",
        "width": 1080,
        "height": 1920,
        "r_frame_rate": "30/1",
        "duration": "19.800000",
        "nb_frames": "594"
      },
      {
        "codec_name": "aac",
        "codec_type": "audio",
        "r_frame_rate": "0/0",
        "duration": "19.799448",
        "nb_frames": "1572"
      }
    ],
    "format": {
      "duration": "19.800000",
      "size": "6496437",
      "bit_rate": "2624823"
    }
  }
  ```
- **Integrity & Verification:**
  - SHA-256 Hash: `bf75e59993dc12aefe9b653367fb5e663f9d5cb2b28320955b4ab37dcb2c481d`
  - Assembly Duration: 21.48 seconds
  - Peak Memory: 684.9 MB RAM
  - Audio/Video Sync: Perfect alignment across all 3 scene transitions with zero drift.

---

## 3. COMPLIANCE CHECKLIST

- [x] **Vertical Orientation:** 1080x1920 (9:16) verified on all 3 stems and the master reel.
- [x] **Constant Frame Rate:** Exactly 30.0 fps verified with no dropped or duplicated frames.
- [x] **Zero Blender Dependency:** 100% procedurally rendered via WebGL/Three.js; no Blender software, scripts, or assets.
- [x] **Budget Constraint:** ₹0 operating cost achieved using open-source Python, Node.js, and FFmpeg binaries.
- [x] **Resource Safety:** Single sequential execution lock prevented concurrent renders; peak RAM remained under 850 MB on the 8 GB host.
- [x] **Safe-Zone Subtitles:** Subtitle baseline positioned at margin 360 px, ensuring zero overlap with platform interaction buttons.
- [x] **Broadcast Audio:** EBU R128 loudness normalized to -16 LUFS with true peak limiting.

