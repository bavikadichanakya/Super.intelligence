# SUPER.INTELLIGENCEEE — Phase 4.3 Risk Register
## Comprehensive Technical, Resource, Editorial & Governance Risk Matrix

**Document Version:** 1.0.0  
**Phase:** Phase 4.3 (Autonomous Video Production Architecture Transformation) — Phase 0 Gate  
**Date:** 2026-11-10T21:52:00+05:30  
**Author:** Lead Systems Risk & Production Assurance Director  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Execution Environment:** Windows 11, Python 3.11, Node.js v24.18.0, FFmpeg 9.0.1, 8 GB RAM, ₹0 Budget  

---

## 1. Risk Matrix Overview

This register documents all potential failure modes across the autonomous video production pipeline, assigning strict severity ratings, probability assessments, preventative controls, and automated recovery fallbacks.

| Risk ID | Category | Risk Description | Severity | Prob. | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | Resource | Host Out-Of-Memory (OOM) during Multi-Engine Rendering | **CRITICAL** | MED | Mitigated |
| **RSK-02** | Storage | Drive G: Temp Directory Exhaustion | **CRITICAL** | HIGH | Mitigated |
| **RSK-03** | Compliance | Prohibited Dependency Creep (Blender or Paid APIs) | **CRITICAL** | LOW | Prevented |
| **RSK-04** | Creative | Aesthetic Regression into Slide-Deck UI Presentation | **HIGH** | MED | Mitigated |
| **RSK-05** | Technical | Windows Subprocess Deadlock with Node/HyperFrames Pipes | **HIGH** | MED | Mitigated |
| **RSK-06** | Audio/Visual | Narration Audio Waveform and Visual Keyframe Desync | **HIGH** | MED | Mitigated |
| **RSK-07** | Editorial | Factual Hallucination or Ungrounded Quantitative Claims | **HIGH** | LOW | Prevented |
| **RSK-08** | Governance | Bypass of Human Publishing Approval or Kill Switch | **CRITICAL** | LOW | Prevented |
| **RSK-09** | Asset / Legal | Copyright Violation or Broken Media Download URLs | **MEDIUM** | MED | Mitigated |
| **RSK-10** | Audio Quality | Loudness Clipping or Narration Masking by Music/SFX | **MEDIUM** | LOW | Mitigated |

---

## 2. Detailed Risk Profiles & Controls

### RSK-01: Host Out-Of-Memory (OOM) During Multi-Engine Rendering
* **Severity:** **CRITICAL** | **Probability:** MEDIUM
* **Impact:** System freezing, process termination by Windows OS, incomplete corrupted video renders.
* **Root Cause:** Launching multiple heavy runtimes concurrently (e.g. Chrome Headless + Motion Canvas + Manim + Kokoro) on an 8 GB RAM workstation where available RAM is ~1.0 GB.
* **Preventative Controls:**
  1. Strict single-engine **sequential execution** enforced at the orchestrator level.
  2. Passing `NODE_OPTIONS="--max-old-space-size=2048"` and `--low-memory-mode` to HyperFrames.
  3. Strict prohibition of large NumPy array in-memory frame storage; streaming via FFmpeg pipes only.
  4. Explicit Python `gc.collect()` and OS process teardown between scene renders.
* **Automated Fallback:** If an engine fails with an exit code indicative of memory exhaustion, the orchestrator immediately invokes the lightweight FFmpeg Ken Burns fallback renderer.

---

### RSK-02: Drive G: Temp Directory Exhaustion
* **Severity:** **CRITICAL** | **Probability:** HIGH
* **Impact:** Windows temp disk exhaustion (Drive G: only has 1.57 GB free), immediate failure of Chrome headless shell extraction or FFmpeg temp muxing.
* **Root Cause:** Default Windows environment variables (`%TEMP%`, `%TMP%`) point to user profile on `G:`.
* **Preventative Controls:**
  1. Mandatory redirection of `TEMP`, `TMP`, and `HYPERFRAMES_EXTRACT_CACHE_DIR` to `A:\SUPER.INTELLIGENCEEE\.temp` (7.25 GB free headroom) in every script and subprocess invocation.
  2. Post-render cleanup hook purging intermediate `.png` extract caches immediately after final `.mp4` compilation.
* **Monitoring Metric:** Automated disk check asserting $>2.0\text{ GB}$ free space before initiating any render pass.

---

### RSK-03: Prohibited Dependency Creep (Blender or Paid APIs)
* **Severity:** **CRITICAL** | **Probability:** LOW
* **Impact:** Violation of non-negotiable project constraints; pipeline breakage on non-GPU environments; unexpected operating costs.
* **Root Cause:** Attempting to render 3D scenes using Blender, or attempting to fetch visual assets / voiceover using commercial paid APIs (Runway, ElevenLabs, Midjourney).
* **Preventative Controls:**
  1. **Absolute Blender Ban:** Automated lint/test rule failing any commit or script referencing `bpy`, `blender`, or `.blend` files.
  2. All 3D rendering delegated to **Three.js** in headless Chrome with software WebGL.
  3. Narration locked to local Voicebox Kokoro / Piper TTS.
  4. Media acquisition locked to Wikimedia Commons, NASA, and free-tier CC0 feeds.

---

### RSK-04: Aesthetic Regression into Slide-Deck UI Presentation
* **Severity:** **HIGH** | **Probability:** MEDIUM
* **Impact:** Video rejected by creative review for resembling a PowerPoint presentation or dashboard UI.
* **Root Cause:** Over-reliance on static rectangular card blitting (`PIL.ImageDraw.rounded_rectangle`), progressive text reveals, and synthetic box diagrams.
* **Preventative Controls:**
  1. Formal deprecation of Pillow rectangular card drawing.
  2. Universal Scene Contract enforcing documentary visual archetypes (Cinematic Cold Open, Context, Problem, Mechanism, Proof, Benchmark, Implication).
  3. Minimum 60% real-world documentary footage or fluid vector motion per video.
  4. Continuous camera movement (Ken Burns push-in, 3D orbit) across all scenes.

---

### RSK-05: Windows Subprocess Deadlock with Node/HyperFrames Pipes
* **Severity:** **HIGH** | **Probability:** MEDIUM
* **Impact:** Rendering process hangs indefinitely during `subprocess.run` on Windows.
* **Root Cause:** In Python on Windows, using `shell=True` with `capture_output=True` where child processes inherit stdout/stderr pipes prevents EOF signaling.
* **Preventative Controls:**
  1. Direct binary invocation (`["npx.cmd", "hyperframes", ...]`) without `shell=True`.
  2. Redirecting stdout/stderr to disk-backed log files (`render.log`) rather than in-memory pipes.
  3. Setting strict non-blocking timeouts with process tree termination (`taskkill /F /T /PID`).

---

### RSK-06: Narration Audio Waveform and Visual Keyframe Desynchronization
* **Severity:** **HIGH** | **Probability:** MEDIUM
* **Impact:** Explainer graphics appearing before or seconds after the narrator explains the concept; jarring viewer experience.
* **Root Cause:** Hardcoding arbitrary scene durations (e.g. 5.0s) rather than measuring actual synthesized WAV audio duration.
* **Preventative Controls:**
  1. Two-stage timing lock: Audio is synthesized first; exact WAV duration is measured via `wave.open()`; scene duration in storyboard is dynamically updated to match audio duration ($\Delta t \le 0.01\text{s}$).
  2. Word-level alignment manifest generated by Voicebox / Whisper to anchor visual animation trigger frames.

---

### RSK-07: Factual Hallucination or Ungrounded Quantitative Claims
* **Severity:** **HIGH** | **Probability:** LOW
* **Impact:** Loss of viewer credibility; scientific inaccuracies in public technology explainers.
* **Root Cause:** Script generator inventing synthetic benchmark numbers (e.g. ">90% tokens discarded") not grounded in the source research paper.
* **Preventative Controls:**
  1. Mandatory claim-to-passage verification in `content/fact_checker.py`.
  2. Generation of a formal `source_ledger.json` documenting exact paper citations, section numbers, and formal equations (e.g. $O(G \cdot L)$ from arXiv:2611.08453).
  3. Unverified scripts trigger an automated hard build failure (`NEEDS_FACT_CHECK_REVISION`).

---

### RSK-08: Bypass of Human Publishing Approval or Kill Switch
* **Severity:** **CRITICAL** | **Probability:** LOW
* **Impact:** Accidental or unauthorized public upload to YouTube or Instagram without editorial review.
* **Root Cause:** Automated pipeline attempting to publish directly upon render completion.
* **Preventative Controls:**
  1. Architectural isolation: The publishing publisher module is physically decoupled from the rendering pipeline.
  2. All finished renders are deposited exclusively into `output/approval_queue/` with state `NEEDS_REVIEW`.
  3. `core/kill_switch.py` performs atomic checks before any network upload; if kill switch is active, all publishing actions immediately abort.

---

### RSK-09: Copyright Infringement or Broken Asset URLs
* **Severity:** **MEDIUM** | **Probability:** MEDIUM
* **Impact:** Content takedown, broken video renders, licensing liability.
* **Root Cause:** Fetching copyrighted stock media without licensing verification, or network timeouts on external image CDNs.
* **Preventative Controls:**
  1. Automated license filtering: Only fetch media tagged Public Domain (CC0, NASA Public Domain) or Creative Commons Attribution (CC-BY).
  2. Local cryptographic caching: All downloaded assets are hashed (SHA256) and cached locally under `assets/media_cache/`.
  3. Automated fallback: If an external asset download fails, the system automatically substitutes a verified local procedural background.

---

### RSK-10: Loudness Non-Compliance & Narration Masking
* **Severity:** **MEDIUM** | **Probability:** LOW
* **Impact:** Audio too quiet or distorted on mobile devices; background music drowning out the narrator.
* **Root Cause:** Static mixing volumes without dynamic ducking or loudness normalization.
* **Preventative Controls:**
  1. Automated two-pass EBU R128 loudness normalization (`-16.0 LUFS ±0.5 LUFS`, true peak `-1.0 dBFS`).
  2. Dynamic sidechain ducking attenuating background audio by **-16 dB** whenever speech is detected.
  3. Automated FFprobe EBU R128 compliance inspection in the QA test gate.

