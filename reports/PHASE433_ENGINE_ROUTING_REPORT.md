# SUPER.INTELLIGENCEEE — Phase 4.3.3 Engine Routing Report
## Multi-Engine Rendering Dispatcher & Adaptive Scene Routing

**Project:** SUPER.INTELLIGENCEEE  
**Phase:** 4.3.3 — Visual Transformation & Voice Restoration  
**Date:** November 15, 2026  
**Status:** VALIDATED  

---

### 1. Dispatcher Architecture & Engine Capabilities

The multi-engine architecture connects five distinct engines coordinated by `rendering/engine_dispatcher.py` and `rendering/engine_registry.py`:

```
                                +-----------------------------+
                                |  UniversalSceneContract     |
                                +-----------------------------+
                                              |
                                              v
                                +-----------------------------+
                                |  EngineDispatcher           |
                                |  - Sequential Lock          |
                                |  - ResourceGuard Preflight  |
                                +-----------------------------+
                                              |
                     +------------------------+------------------------+
                     |                        |                        |
                     v                        v                        v
            +-----------------+      +-----------------+      +-----------------+
            |  NATIVE_MOTION  |      |      MANIM      |      |     FFMPEG      |
            |  Light-First    |      |  Light-First    |      |  Master Concat, |
            |  Cluster / Die  |      |  Curves / Plots |      |  Loudnorm -16,  |
            |  Sandbox UI     |      |  Equations      |      |  ASS Subtitles  |
            +-----------------+      +-----------------+      +-----------------+
```

---

### 2. Scene Archetype Classification & Engine Routing Rules

The `EngineRegistry.infer_engine_for_scene()` method maps scene metadata to the optimal rendering engine:

| Scene Type / Archetype | Preferred Engine | Engine Selected | Composition / Template |
| :--- | :--- | :--- | :--- |
| `ANIMATED_PROCESS` (Cluster/Topology) | `NATIVE_MOTION` | `NativeMotionAdapter` | `SystemTopologyComposition` |
| `TECHNICAL_DIAGRAM` (Sandbox/Security)| `NATIVE_MOTION` | `NativeMotionAdapter` | `SandboxIsolationComposition` |
| `KINETIC_TYPOGRAPHY` (Verdict/Verdict)| `NATIVE_MOTION` | `NativeMotionAdapter` | `EditorialVerdictComposition` |
| `DATA_VISUALIZATION` (Curves/Axes)   | `MANIM`         | `ManimAdapter`        | `ManimScene` (Light-First theme) |
| `FINAL_ASSEMBLY` (Mastering)         | `FFMPEG`        | `FFmpegAdapter`       | Concat + Audio Loudnorm + ASS |

---

### 3. Light-First Coherence Across Engines

In Phase 4.3.3, all active engines share an identical light-first color contract:
1. **Native Motion Engine:**
   - Background: `#FAF7F2` (Warm Ivory) to `#FFFFFF` (Soft White) gradient.
   - Micro-grid: `#E2E8F0` (Light Slate).
   - Typography: `#0F172A` (Obsidian Bold) and `#475569` (Secondary Slate).
   - Accents: `#0284C7` (Technical Blue), `#059669` (Emerald), `#D97706` (Amber).
2. **Manim Adapter (`rendering/adapters/manim_adapter.py`):**
   - Config: `config.background_color = "#FAF7F2"`.
   - Title/Text: `#0F172A` (Obsidian) and `#475569` (Slate).
   - Axes: `#94A3B8` (Light Slate).
   - Function Plots: `#D97706` (Baseline Amber) and `#0284C7` (Interleaved Blue).
   - Metrics: `#059669` (Emerald).
3. **FFmpeg Adapter (`rendering/adapters/ffmpeg_adapter.py`):**
   - Subtitles: Clean white text with 3px solid black outline (`BorderStyle=1, Outline=3`), positioned at `MarginV = 380px` to guarantee 100% legibility on light ivory backgrounds while remaining clear of platform UI elements.

---

### 4. Robust Sequential Execution & Fallback Policy

1. **Sequential Lock (`threading.Lock()`):**
   - No two rendering processes ever execute concurrently. Peak memory is preserved at all times for the active engine.
2. **Preflight Resource Verification (`ResourceGuard`):**
   - Checks available RAM (> 500 MB) and free disk (> 2 GB) before launching any sub-process.
3. **Graceful Fallback:**
   - If a preferred engine encounters a runtime timeout or exception, the dispatcher cleanly terminates the process, clears scratch artifacts, and falls back to `NATIVE_MOTION` or `FFMPEG`.
   - Silent substitution to test patterns (`testsrc`) is strictly blocked in production pipelines.
