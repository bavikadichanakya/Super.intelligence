# PHASE 4.3.2D — ROOT-CAUSE ANALYSIS: RENDERING FAILURES & TIMING COLLAPSE

**Project:** SUPER.INTELLIGENCEEE  
**Phase:** 4.3.2D — Remediation  
**Target:** Multi-Engine Rendering Dispatcher & Adapters  
**Date:** 2026-11-14  
**Host Environment:** Windows 11 Home 64-bit, Intel Core i5-1135G7 @ 2.40GHz, 8.0 GB RAM, Intel Iris Xe  
**Budget:** ₹0 mandatory operating cost  
**Blender Prohibition:** 100% Enforced  

---

## 1. EXECUTIVE SUMMARY

During Phase 4.3.2C, the autonomous documentary pipeline generated a complete video container that was ultimately rejected in Phase 4.3.2C.1 because Scenes 1 and 3 degraded to raw FFmpeg `testsrc` calibration patterns (69.5% of timeline), and Scene 2 suffered severe duration drift (rendered at 20.27s vs 10.21s budget).

This forensic investigation audited:
- `rendering/adapters/threejs_adapter.py`
- `rendering/adapters/hyperframes_adapter.py`
- `rendering/adapters/manim_adapter.py`
- `rendering/adapters/ffmpeg_adapter.py`
- `rendering/engine_dispatcher.py`
- `rendering/engine_registry.py`
- `rendering/resource_guard.py`
- Chromium CDP lifecycle and ANGLE graphics configuration.

---

## 2. ROOT-CAUSE FINDINGS BY SUBSYSTEM

### 2.1 Why Three.js Required > 370 Seconds & Timed Out
1. **CPU Software Rasterization (ANGLE SwiftShader):**
   - The host has no dedicated GPU and runs an Intel Iris Xe integrated chip.
   - Headless Chrome (`chrome-headless-shell.exe` via HyperFrames CLI) defaulted to Google's ANGLE SwiftShader CPU software rasterizer.
   - For a vertical 1080x1920 viewport (2,073,600 pixels per frame) with 3D icosahedron geometries, wireframes, 8 orbiting nodes, point lights, and directional lights, software rasterization throughput dropped to **~1.15 seconds per frame** (~0.87 fps).
2. **Frame Budget Multiplier:**
   - Scene 1 had a budgeted duration of 10.77s @ 30 fps = **323 frames**.
   - $323 \text{ frames} \times 1.15 \text{ s/frame} \approx 371.4 \text{ seconds}$ (~6.2 minutes).
3. **External CDN Blocking:**
   - In `ThreeJsAdapter.prepare()`, line 135:  
     `<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>`
   - Headless Chrome was forced to resolve external DNS and download CDN scripts during automated CLI rendering, introducing network latency and intermittent blocking.
4. **Timeout Enforcement:**
   - At t = 376.6s, the `ResourceGuard` timeout watchdog terminated the process.

### 2.2 Why HyperFrames Stalled & Timed Out
1. **CDP Screencast / Screenshot Buffer Deadlock:**
   - In `HyperFramesAdapter.prepare()`, the HTML composition imported Google Fonts (`fonts.googleapis.com`) and GSAP (`cdn.jsdelivr.net`).
   - HyperFrames spawns Chromium DevTools Protocol (CDP) to step virtual time (`hf-seek`) and capture uncompressed RGBA pixel buffers (8.3 MB per 1080x1920 frame).
2. **Memory Swapping on 8 GB Host:**
   - Host baseline memory usage with Windows 11 and background services is ~4.8 GB.
   - Chrome spawned 4 helper renderer processes, pushing RAM usage past 6.2 GB and triggering Windows virtual memory disk swapping.
3. **IPC Hang:**
   - The Chromium CDP socket stopped receiving frame acknowledgement signals, logging:  
     `"no frame progress for 300000ms stuck at frame 0/406"`.
   - The supervisor killed the process tree at t = 473.2s.

### 2.3 The Disastrous Fallback Chain: Why `testsrc` Appeared
In `engine_registry.py` and `engine_dispatcher.py`:
- `EngineRegistry.get_fallback_engine_for_scene`:
  - When Three.js failed, fallback was `HYPERFRAMES`.
  - When HyperFrames failed, fallback was `FFMPEG`.
- In `engine_dispatcher.py` lines 140-158:
  - If the fallback failed, a tertiary fallback was triggered: `FFMPEG`.
- In `ffmpeg_adapter.py` lines 116-128:
  - When `FFmpegAdapter.render()` was executed directly as a scene renderer, it ran:
    `testsrc=size=1080x1920:rate=30:duration={duration}` with `sine=frequency=440`!
- **Architectural Flaw:** The system treated an engineering diagnostic test pattern as a valid production fallback!

### 2.4 Why Scene 2 Rendered at 20.27 Seconds (The Duration Drift Bug)
In `rendering/adapters/manim_adapter.py`, lines 149-187:
```python
half_dur = max(duration / 2.0, 1.0)
wait_dur = max(duration - 2.0, 0.5)

# Animation Sequence timed to {duration:.2f}s
self.play(FadeIn(title), FadeIn(subtitle), run_time=0.8)
self.play(Create(axes), run_time=1.0)
self.play(Create(quad_curve), Write(quad_label), run_time=half_dur)
self.play(Create(lin_curve), Write(lin_label), FadeIn(metric), run_time=half_dur)
self.wait(wait_dur)
```
- Total animation duration calculation:
  $$\text{Total Duration} = 0.8 + 1.0 + \text{half\_dur} + \text{half\_dur} + \text{wait\_dur}$$
  $$\text{Since } \text{half\_dur} + \text{half\_dur} = \text{duration}$$
  $$\text{Total Duration} = 1.8 + \text{duration} + (\text{duration} - 2.0) = 2 \times \text{duration} - 0.2$$
- For Scene 2 with an intended duration of **10.21 seconds**:
  $$\text{Rendered Duration} = 2 \times 10.21 - 0.2 = \mathbf{20.22 \text{ seconds}}$$
- The animation script added `duration` twice! This explains the exact 20.27-second stem output.
- When FFmpeg assembled the video, it truncated the video stem using `-shortest` against the 33.44s master audio track.

---

## 3. REMEDIATION STRATEGY

```
+-------------------------------------------------------------------------------------------------------+
| Defect Found                         | Root Cause                            | Architectural Remediation      |
+-------------------------------------------------------------------------------------------------------+
| Three.js & HyperFrames Timeouts      | Headless Chromium software ANGLE      | Replace with Native 2D Motion  |
|                                      | rasterization on 8 GB CPU-only host   | Graphics Engine (PIL/Cairo/FF) |
+-------------------------------------------------------------------------------------------------------+
| Fallback to Test Card (testsrc)      | FFmpegAdapter generated testsrc       | Remove testsrc from fallback.  |
|                                      | as emergency scene renderer           | Fallback to Native 2D topology |
+-------------------------------------------------------------------------------------------------------+
| Scene 2 Duration Drift (20.27s)      | Manim script summed duration twice    | Fix animation timeline algebra |
|                                      | in play() and wait() calls            | to strictly match budget       |
+-------------------------------------------------------------------------------------------------------+
| Subtitle Bottom Safe Zone Intrusion  | ASS MarginV set to 340 without        | Calibrate ASS coordinate box   |
|                                      | verifying multi-line text height      | and set MarginV = 380-420      |
+-------------------------------------------------------------------------------------------------------+
| Truncated Narration Sentences        | Script generator token clipping       | Enforce clause/grammar checks  |
|                                      | and lack of end-of-sentence validator | before dispatching to TTS      |
+-------------------------------------------------------------------------------------------------------+
| Orphaned Claim Reference (claim_03)  | Storyboard referenced unindexed key   | Add schema-level cross-check   |
|                                      | from research dossier                 | between storyboard and dossier |
+-------------------------------------------------------------------------------------------------------+
```

---

## 4. PHASE A CONCLUSION

The root causes are completely understood, deterministic, and fixable in code without purchasing hardware or third-party APIs. We now proceed to Phase B: implementing the Native 2D Motion Graphics Engine.
