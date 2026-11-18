# PHASE 4.3.2C.1 — MULTI-ENGINE EXECUTION & DEGRADATION AUDIT

**Project:** SUPER.INTELLIGENCEEE  
**Audit Target:** Autonomous Multi-Engine Dispatcher & Adapter Execution  
**Topic:** Metal Sandbox: Isolated Execution and Command Scheduling for GPU Coding Agents on Apple Silicon  
**Date:** 2026-11-14  
**Auditor:** Autonomous Video Production Acceptance Auditor  

---

## 1. EXECUTIVE SUMMARY

The primary architectural promise of Phase 4.3.2B and 4.3.2C was an intelligent multi-engine rendering dispatcher capable of routing scenes dynamically to Manim, Three.js, HyperFrames, and FFmpeg based on scene intent.

This forensic audit inspected the underlying execution logs (`logs/phase432c_pipeline_run.log`, dispatcher traces, and stem visual outputs) to verify whether each engine actually produced its intended creative content, or whether the system silently relied on emergency fallback mechanisms to present a superficial illusion of pipeline success.

### Crucial Audit Finding:
- **Requested Multi-Engine Pipeline:** Three.js (Scene 1) + Manim (Scene 2) + HyperFrames (Scene 3).
- **Actual Rendered Pipeline:** **FFmpeg Testsrc (Scene 1) + Manim Cairo (Scene 2) + FFmpeg Testsrc (Scene 3)**.
- **Visual Degradation Rate:** **66.7% of documentary scenes suffered catastrophic fallback to procedural FFmpeg test cards**, losing all narrative diagrams, 3D topologies, and kinetic typography.

---

## 2. SCENE-BY-SCENE ENGINE EXECUTION BREAKDOWN

```
+-------------------------------------------------------------------------------------------------------+
| Scene | Target Beat             | Requested Engine | Fallback Engine | Rendered Output | Status       |
+-------------------------------------------------------------------------------------------------------+
| 01    | Hook & Topology         | Three.js (3D)    | HyperFrames->FF | FFmpeg testsrc  | DEGRADED (P1)|
| 02    | Efficiency Curves       | Manim (Vector)   | None (Direct)   | Manim Cairo MP4 | SUCCESS (P0) |
| 03    | Sandbox Verdict & HUD   | HyperFrames (Kin)| FFmpeg Proced.  | FFmpeg testsrc  | DEGRADED (P1)|
+-------------------------------------------------------------------------------------------------------+
```

---

## 3. ROOT CAUSE FORENSICS BY SCENE

### 3.1 Scene 01: Three.js Timeout & Cascading Fallback Collapse
- **Creative Intent:** A procedural 3D cluster topology displaying idle compute nodes alternating with agent command dispatch.
- **Target Engine:** `ThreeJsAdapter` (`core/rendering/adapters/threejs_adapter.py`).
- **Execution Event Log:**
  1. `ThreeJsAdapter` generated an HTML5 WebGL template with OrbitControls and procedural cube meshes.
  2. Adapter invoked headless Chromium (`chrome.exe --headless --disable-gpu`) via CDP to capture 323 frames (10.77s @ 30 fps) at 1080x1920.
  3. **The Bottleneck:** On this host (Intel Core i5-1135G7, 8 GB RAM, no dedicated GPU), headless Chrome rasterizes WebGL using the software ANGLE SwiftShader pipeline. Frame throughput was measured at **~1.15 seconds per frame**.
  4. Rendering 323 frames required **371+ seconds**.
  5. At **t=376.6s**, the adapter exceeded its safety timeout and terminated the Chromium worker.
  6. **Cascade:** The dispatcher attempted a secondary fallback to `HyperFramesAdapter`.
  7. HyperFrames also launched Chromium for frame capture, hit a duplicate stall, and subsequently threw a timeout exception.
  8. **Tertiary Degradation:** The dispatcher engaged the emergency safety net: `FFmpegAdapter.generate_procedural_background()` using `testsrc=size=1080x1920:rate=30`.
- **Delivered Output:** A synthetic color grid with moving noise squares.
- **Impact:** Complete loss of the conceptual 3D cluster topology and visual explanation of idle GPU nodes.

### 3.2 Scene 02: Manim Mathematical Vector Success
- **Creative Intent:** Dynamic vector coordinate graph plotting duty cycle efficiency curves against baseline agent execution.
- **Target Engine:** `ManimAdapter` (`core/rendering/adapters/manim_adapter.py`).
- **Execution Event Log:**
  1. `ManimAdapter` authored a standalone Python scene script utilizing Manim Community v0.19.0.
  2. Script defined `Axes`, labeled coordinates, plotted parametric efficiency curves ($1.68\times$--$2.05\times$ throughput gain), and rendered text labels.
  3. Cairo software rasterization executed purely in-process via C libraries without Chromium overhead.
  4. **Execution Time:** **8.84 seconds total** for 608 frames.
- **Delivered Output:** A crisp, high-contrast, perfectly rendered vector animation showing coordinate axes and dynamic curve plots.
- **Impact:** Complete success. Demonstrates that Manim is highly optimized, stable, and production-ready on this CPU-bound host.

### 3.3 Scene 03: HyperFrames CDP Stall & Timeout Collapse
- **Creative Intent:** Editorial HUD badge displaying isolation parameters, security boundary status, and architectural synthesis.
- **Target Engine:** `HyperFramesAdapter` (`core/rendering/adapters/hyperframes_adapter.py`).
- **Execution Event Log:**
  1. `HyperFramesAdapter` authored a CSS/HTML kinetic typography layout with card borders and status badges.
  2. Adapter spawned a headless Chrome CDP session to capture 406 frames (13.53s @ 30 fps).
  3. Chrome CDP worker encountered an IPC thread deadlock: `no frame progress for 300000ms stuck at frame 0/406`.
  4. At **t=473.2s**, the worker timed out and was killed by the process supervisor.
  5. The dispatcher caught the timeout and engaged the emergency fallback: `FFmpegAdapter.generate_procedural_background()`.
- **Delivered Output:** An identical synthetic color grid with moving noise squares.
- **Impact:** Complete loss of kinetic typography, HUD metrics, and final architectural verdict.

---

## 4. ARCHITECTURAL EVALUATION OF THE DISPATCHER

### Strengths:
1. **Fault Isolation:** The pipeline did not crash or abort mid-run. The multi-tiered fallback architecture successfully prevented catastrophic uncaught exceptions and ensured that a playable container was delivered to the approval queue.
2. **Graceful Degradation:** When an engine hung, the dispatcher enforced hard timeouts, killed rogue Chrome processes, and substituted procedural video rather than hanging indefinitely.

### Critical Vulnerabilities:
1. **False Equivalence of Success:** The dispatcher reported status `SUCCESS` because a valid `.mp4` file was emitted. In reality, substituting a raw test pattern for a planned architectural diagram is a **functional editorial failure**.
2. **Chromium Concurrency on 8 GB RAM:** Running headless Chrome CDP frame capture at 1080x1920 on an 8 GB RAM system without GPU acceleration is fundamentally unviable for real-time or high-throughput production (taking ~1.1s per frame).
3. **Absence of Lightweight 2D Fallback:** When Three.js or HyperFrames fails, the fallback should not be a raw test card; it must be a lightweight, deterministic PIL/Cairo/FFmpeg motion graphic template with real text and iconography.

---

## 5. PHASE B AUDIT CONCLUSION

The multi-engine dispatcher demonstrated structural stability, but the underlying rendering engines exhibited severe platform incompatibility:
- **Manim:** **100% Production Ready** (fast, stable, beautiful vector rendering).
- **Three.js (Chromium WebGL):** **Unviable on Current Host** (>350s render times, triggers timeouts).
- **HyperFrames (Chromium CDP):** **Unstable on Current Host** (frequent IPC deadlocks on high-res portrait frames).

Remediation requires shifting non-mathematical scenes to lightweight direct-rasterization engines (PIL/Cairo/FFmpeg drawtext) to eliminate Chromium CDP bottlenecks.

