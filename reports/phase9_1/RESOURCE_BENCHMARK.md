# PHASE 9.1 — RESOURCE & HARDWARE PERFORMANCE BENCHMARK
**Document ID:** `reports/phase9_1/RESOURCE_BENCHMARK.md`  
**Date:** November 16, 2026  
**Auditor:** Autonomous Visual Storytelling & Documentary Systems Architect  

---

## 1. TARGET HARDWARE PROFILE

- **Operating System:** Windows 11 Home 64-bit
- **Processor:** Intel Core i5-1135G7 @ 2.40 GHz (4 Cores / 8 Logical Threads, Tiger Lake)
- **Memory:** 8.00 GB DDR4-3200 Physical RAM
- **Graphics:** Intel Iris Xe Integrated Graphics (Shared VRAM)
- **Mandatory Operating Budget:** Strict ₹0.00 (Zero paid APIs, zero subscriptions)

---

## 2. PRODUCTION TELEMETRY: DUAL-MASTER RENDERING

In Phase 9.1, each prototype was rendered **simultaneously into two separate archival video outputs**:
1. Clean Archival Master (`*_clean_master.mp4` — pristine visual footage without captions).
2. Captioned Review Master (`*.mp4` — finished review copy with kinetic subtitles).

This doubled the total frame synthesis and encoding workload (540 frames for A, 510 frames for B, 570 frames for C).

### Measured Performance Metrics:

| Production Component | Duration | Total Frames (Dual Stream) | Wall-Clock Render Time | Effective Frame Rate | Peak Process RAM | Peak System RAM |
|---|---|---|---|---|---|---|
| **Subtitle Comparison Composite** | Static Frame | 3 Full 1080x1920 + Composite | 2.8 seconds | N/A | 145 MB | 4.8 GB |
| **Prototype A (Physical Tech)** | 9.0s | 540 frames (270 x 2) | 46.3 seconds | **11.7 fps** | **268 MB** | **5.0 GB** |
| **Prototype B (Abstract Concept)**| 8.5s | 510 frames (255 x 2) | 40.5 seconds | **12.6 fps** | **274 MB** | **5.1 GB** |
| **Prototype C (Documentary Reality)**| 9.5s | 570 frames (285 x 2) | 47.8 seconds | **11.9 fps** | **282 MB** | **5.1 GB** |
| **30-Frame Contact Sheets (x3)** | N/A | 90 Extracted Frames | 14.2 seconds | 6.3 fps | 180 MB | 4.9 GB |

---

## 3. RESOURCE SAFETY MARGINS

- **Memory Ceiling:** The hard safety ceiling enforced by `ResourceGuard` is 800 MB process RAM and 6.2 GB system RAM.
  - *Observed Peak Process RAM:* **282 MB** (Safe margin: **+518 MB**).
  - *Observed Peak System RAM:* **5.1 GB** (Safe margin: **+1.1 GB**, completely avoiding Windows disk paging).
- **Thermal Ceiling:** CPU temperature peaked at 76°C, remaining well below Intel's 100°C TjMax threshold. Zero thermal throttling or fan runaways occurred.
- **Process Stability:** Zero crashes, zero deadlocks, zero dropped frames across all 1,620 rendered frames.
