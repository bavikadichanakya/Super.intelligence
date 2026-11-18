# PHASE 4.3.2D — ENGINE ROUTING AND FALLBACK INTELLIGENCE

**Project:** SUPER.INTELLIGENCEEE  
**Phase:** 4.3.2D — Remediation  
**Module:** `rendering/engine_registry.py` & `rendering/engine_dispatcher.py`  
**Date:** 2026-11-14  

---

## 1. EXECUTIVE SUMMARY

In Phase 4.3.2C, engine routing suffered from a catastrophic fallback failure: when Three.js and HyperFrames timed out, the dispatcher degraded to FFmpeg `testsrc` calibration patterns, rendering 69.5% of the documentary unwatchable.

Phase 4.3.2D completely restructures engine selection, prioritizes native Python/Pillow/FFmpeg vector and raster rendering, and permanently bans `testsrc` from all production fallback paths.

---

## 2. RECONFIGURED ENGINE ROUTING MATRIX

```
+-------------------------------------------------------------------------------------------------------+
| Scene Archetype / Intent       | Primary Engine       | Fallback Engine      | Fallback Guarantee     |
+-------------------------------------------------------------------------------------------------------+
| Mathematical Graphs & Curves   | Manim Community      | Native Motion Engine | 2D Vector Chart        |
| Equation Animations & Scaling  | Manim Community      | Native Motion Engine | 2D Vector Equations    |
| Hardware & Cluster Topologies  | Native Motion Engine | Manim Community      | 2D Animated Nodes      |
| Architecture & Dataflow Paths  | Native Motion Engine | Manim Community      | 2D Conduit Graphics    |
| Editorial Verdict & HUD Badges | Native Motion Engine | Manim Community      | 2D Card Composition    |
| Kinetic Typography & Callouts  | Native Motion Engine | Manim Community      | 2D Scaled Typography   |
| Procedural 3D (Experimental)   | Three.js (Optional)  | Native Motion Engine | 2D Topology (Zero Test)|
| Timeline Assembly & Mastering  | FFmpeg Adapter       | None (Critical)      | Final MP4 & Audio      |
+-------------------------------------------------------------------------------------------------------+
```

---

## 3. STRICT FALLBACK & SAFETY ENFORCEMENTS

1. **Explanatory Purpose Preservation:**
   - If a scene requests a 3D system topology (Three.js) and fails, the fallback routes immediately to `NativeMotionEngine` to generate an equivalent animated 2D cluster topology with nodes and data flow pulses.
   - It will **never** generate a test pattern.
2. **Permanent Banning of `testsrc`:**
   - The tertiary fallback in `EngineDispatcher` to `FFMPEG` has been removed.
   - In `FFmpegAdapter.render()`, an explicit guard raises `RenderExecutionError` if called in a production context without `ALLOW_FFMPEG_TESTSRC=true`.
3. **Clean Failure Reporting (`RENDER_FAILED`):**
   - If both the primary and fallback engines fail, `FallbackExhaustedError` is raised immediately. The scene is marked as `FAILED`, halting video assembly and preventing damaged assets from reaching the approval queue.

