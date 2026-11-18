# SUPER.INTELLIGENCEEE — PHASE 3.6
# FORENSIC FAILURE & DEFECT REGISTER

**Author:** Senior Quality Assurance Lead & Systems Auditor  
**Date:** 2026-11-07  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`

---

## 1. Summary of Identified Defects

The forensic audit of Phase 3.6 identified **12 distinct failures and architectural defects** across visual production, editorial intelligence, and system connectivity.

| Defect ID | Component | Severity | Category | Status |
| :--- | :--- | :--- | :--- | :--- |
| **FAIL-01** | `DocumentaryCompositor` / Rendering Engines | **HIGH** | Visual & Motion | Confirmed in Phase 3.5.1 Video |
| **FAIL-02** | `DynamicScenePlanner` $\rightarrow$ PIL Engines | **HIGH** | Architectural Disconnect | Verified in Code |
| **FAIL-03** | `CreativeDirector` (`creative_director.py:55`) | **HIGH** | Stale / Incompatible Theme | Verified in Code |
| **FAIL-04** | `TechDocProducer` (`produce_phase3_5_tech_doc.py`) | **HIGH** | Architectural Bypass | Verified in Code |
| **FAIL-05** | `PublicWebCollector` (`public_web_collector.py`) | **HIGH** | Network / WAF Block | Reproducible (HTTP 405 / 429) |
| **FAIL-06** | `AgentReachConnector` (`agent_reach_connector.py:178`) | **MEDIUM** | Code Defect (`TypeError`) | Reproducible on Null Raw Data |
| **FAIL-07** | `ResearchAnalyst` (`research_analyst.py:40`) | **MEDIUM** | Fragile Claim Extraction | Verified on Conceptual Articles |
| **FAIL-08** | `ResearchAnalyst` $\rightarrow$ `AgentReachConnector` | **MEDIUM** | Disconnected Fallback | Verified in Code |
| **FAIL-09** | `TechDocProducer` (`tech_doc_producer.py`) | **MEDIUM** | Intra-Scene A/V Desync | Verified in Benchmark Video |
| **FAIL-10** | `TransitionRouter` (`video/ffmpeg_pipeline.py`) | **MEDIUM** | Repetitive Mechanical Cuts | Verified in Benchmark Video |
| **FAIL-11** | `Database` (`data/super_intelligence.db`) | **LOW** | Synthetic Entity Pollution | 2 Synthetic Topics Detected |
| **FAIL-12** | `ArXivCollector` (`config.yaml`) | **LOW** | Weekend Empty Feed Blackout | Verified in Raw ArXiv XML |

---

## 2. Detailed Forensic Failure Profiles

### FAIL-01: Flat 2D Raster Rendering ("Slideshow Syndrome")
- **File & Function:** `creative/tech_documentary/kinetic_typography/kinetic_engine.py`, `vector_diagram_engine.py`, `hud_telemetry.py`, `verdict_engine.py`.
- **Severity:** `HIGH`
- **Category:** Visual & Motion Design
- **Description:** Scenes are drawn onto flat 1080x1920 2D bitmaps using Pillow `ImageDraw`. All UI cards, background grids, diagrams, and text exist on a single z-plane.
- **Root Cause:** Absence of a virtual 3D camera layer. Without perspective transforms, focal length, depth of field, or parallax offsets between background and foreground, moving elements appear as animated stickers sliding across a flat poster.
- **Remediation:** Introduce affine/perspective transform layer (e.g. via `scipy.ndimage` or OpenCV / PyCairo) with virtual camera coordinate mapping (`camera_x`, `camera_y`, `camera_zoom`, `camera_roll`).

---

### FAIL-02: Camera Motion Directives Dropped at Compositor Boundary
- **File & Function:** `creative/scene_planner/dynamic_scene_planner.py:68-80` vs `creative/tech_documentary/scene_composition/documentary_compositor.py:80-152`.
- **Severity:** `HIGH`
- **Category:** Architectural Disconnect
- **Description:** `DynamicScenePlanner` computes camera motions (`push_in_slow`, `snap_zoom`, `drift_subtle`), but `DocumentaryCompositor.render_scene()` and the underlying scene engines take no camera motion arguments.
- **Reproduction Evidence:** Inspected `DocumentaryCompositor.render_scene()` lines 90–152. Calls to `terminal_animator`, `diagram_engine`, `hud_engine`, and `kinetic_engine` completely omit the `camera_direction` property.
- **Remediation:** Update `render_scene()` and each engine's `render_clip()` signature to accept `camera_motion: str` and apply corresponding scale/pan keyframe curves across frame rendering.

---

### FAIL-03: CreativeDirector Stale Dark-Theme Hardcoding
- **File & Function:** `creative/director/creative_director.py:55, 63-72`.
- **Severity:** `HIGH`
- **Category:** Architectural Staleness
- **Description:** While Phase 3.2+ established a mandatory Light-First visual identity (`#F8FAFC` to `#FFFFFF`), `CreativeDirector` still emits:
  ```python
  visual_theme = "High-Fidelity Engineering Documentary: Dark Obsidian, Neon Telemetry, Diagrammatic Depth"
  color_palette = { "background_primary": "#080b11", "panel_surface": "#111722", ... }
  ```
- **Consequence:** The dynamic planning pipeline could not be used without overriding or rewriting its theme output, forcing engineers to bypass `CreativeDirector` during production.
- **Remediation:** Update `CreativeDirector` to emit the approved Phase 3.5.1 Light-First editorial design system (`#F8FAFC` background, obsidian typography `#0F172A`, warm ivory surfaces, emerald `#059669` and electric blue `#315CFF` accents).

---

### FAIL-04: Benchmark Production Script Bypasses Dynamic Planning
- **File & Function:** `scripts/produce_phase3_5_tech_doc.py:47-132`.
- **Severity:** `HIGH`
- **Category:** Pipeline Architecture Bypass
- **Description:** `produce_phase3_5_tech_doc.py` defines a hardcoded 6-scene list of raw dictionaries instead of invoking `StoryArchitectureEngine.plan_architecture()` and `DynamicScenePlanner.plan_scenes()`.
- **Root Cause:** A contract mismatch existed between `DynamicScene` dataclasses and the dictionary schema expected by `TechDocProducer`.
- **Remediation:** Implement a clean adapter in `TechDocProducer` that natively consumes `DynamicScenePlan` and translates dataclass attributes (`sequence`, `scene_objective`, `visual_concept`) to render parameters.

---

### FAIL-05: PublicWebCollector Blocked by Standard WAFs
- **File & Function:** `research/public_web_collector.py:18-24`.
- **Severity:** `HIGH`
- **Category:** Network Scraping Fragility
- **Description:** Testing live URL extraction on Ars Technica resulted in HTTP 405 (Method Not Allowed), and VentureBeat returned HTTP 429 (Too Many Requests).
- **Root Cause:** `PublicWebCollector` sends `requests.get` with an amateur scraper user-agent (`SUPER.INTELLIGENCEEE-Researcher/2.0 ...`) without browser headers, cookie handling, or retry backoff.
- **Remediation:** Modernize request headers with standard browser headers, and implement an automatic fallback to `AgentReachConnector.read_web_page()` when status is not 200.

---

### FAIL-06: AgentReachConnector Crashes on Null "raw" Metadata
- **File & Function:** `research/agent_reach_connector.py:178, 183`.
- **Severity:** `MEDIUM`
- **Category:** Code Defect / Exception Handling
- **Description:** When running `search_github("security")`, the method crashed with:
  `TypeError: 'NoneType' object is not subscriptable`
- **Root Cause:** Line 178: `raw = item.get("raw", {})`. If the JSON output explicitly contains `"raw": null`, `.get("raw", {})` returns `None` (default is only used if key is missing). Line 183 then calls `raw.get(...)` on `None`.
- **Remediation:** Change line 178 to `raw = item.get("raw") or {}`.

---

### FAIL-07: Overly Restrictive Quantitative Metric Regex in Claim Extraction
- **File & Function:** `research/research_analyst.py:40-54`.
- **Severity:** `MEDIUM`
- **Category:** Research Intelligence Quality
- **Description:** In the 10-topic live discovery test, 4 out of 10 genuine topics extracted 0 claims (e.g. Meta Spaces, Artex hacking tools, FloMo world models) despite containing substantive technical documentation.
- **Root Cause:** `metric_re` requires explicit numeric strings (`%`, `x`, `$`, `tokens`, `GB`, `ms`). Conceptual architectural assertions, security vulnerability disclosures, and algorithmic breakthroughs without immediate numbers in the first 15 sentences are discarded.
- **Remediation:** Broaden `extract_claims_from_text()` with semantic sentence extraction (NLP subject-predicate-object assertion scoring) to capture conceptual and qualitative claims.

---

### FAIL-08: ResearchAnalyst Decoupled from Agent Reach Fallback
- **File & Function:** `research/research_analyst.py:91-100`.
- **Severity:** `MEDIUM`
- **Category:** Architecture Integration
- **Description:** When `self.web_collector.extract_page(url)` fails, `ResearchAnalyst` immediately marks the dossier as `RESEARCH_BLOCKED` rather than attempting retrieval through `AgentReachConnector`.
- **Consequence:** Fails to retrieve pages that `agent-reach` can easily extract (such as Ars Technica).
- **Remediation:** Wire `AgentReachConnector` into `ResearchAnalyst` as a tier-2 retrieval provider before declaring a topic blocked.

---

### FAIL-09: Macroscopic-Only Audio/Visual Synchronization
- **File & Function:** `creative/tech_documentary/documentary_renderer/tech_doc_producer.py:230-245`.
- **Severity:** `MEDIUM`
- **Category:** Pacing & Synchronization
- **Description:** Visual events within scenes are triggered by static frame fractions (e.g. `frame_idx > 0.45 * total_frames`) rather than the exact timestamp when the narrator pronounces the corresponding term.
- **Result:** Visual elements (such as tree nodes or benchmark bars) appear several seconds before or after the narrator mentions them.
- **Remediation:** Ingest the word-level timestamps generated by `CaptionGenerator` / Kokoro TTS into `DocumentaryCompositor` to trigger key visual reveals on exact speech cue timestamps.

---

### FAIL-10: Uniform Repetitive Transition Syndrome
- **File & Function:** `video/ffmpeg_pipeline.py:180-220`.
- **Severity:** `MEDIUM`
- **Category:** Motion & Editing
- **Description:** Every scene boundary in the documentary uses an identical 0.3-second `wipeleft` cut.
- **Result:** The video feels like a mechanical PowerPoint presentation rather than a professionally edited film.
- **Remediation:** Dynamically assign transition types based on narrative beats (e.g. `fadeblack` between Act 1 and Act 2, directional wipe for before/after comparison, seamless match cut or zoom-through between hardware and diagram).

---

### FAIL-11: Synthetic Entity Pollution in Database
- **File & Function:** `data/super_intelligence.db` (`topics` table).
- **Severity:** `LOW`
- **Category:** Data Cleanliness
- **Description:** Rows 487 and 493 contain synthetic topics with fictitious `.local` domains (`https://super.intelligenceee.local/...`) scoring 95.0–99.0 points.
- **Risk:** Automated topic selection queries without environment filters could select mock data over real news.
- **Remediation:** Add an `is_synthetic` boolean flag to the database schema and filter out non-production fixtures during live editorial selection.

---

### FAIL-12: ArXiv Weekend RSS Blackout
- **File & Function:** `config.yaml:48-52`.
- **Severity:** `LOW`
- **Category:** Ingestion Monitoring
- **Description:** On Saturdays and Sundays, `export.arxiv.org/rss/cs.AI` returns 0 entries because arXiv does not publish preprints on weekends (`<skipDays>`).
- **Consequence:** Scrapers that treat 0 entries as a network failure flag false alarms.
- **Remediation:** Update `RSSCollector` to inspect the `<skipDays>` XML tag and query arXiv's Search API (`export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate`) as a weekend fallback.

