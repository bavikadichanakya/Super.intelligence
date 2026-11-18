# SUPER.INTELLIGENCEEE — Critical Risk Register & Forensic Audit

**Audit Date:** 2026-11-06  
**Auditor:** Principal AI Systems Architect & QA Lead  
**Scope:** Independent empirical verification of 14 previously identified architectural risks.

---

## 1. Risk Evaluation Summary

| # | Risk Description | Status Found | Severity | Action Required |
|---|---|---|---|---|
| **1** | Audio/video duration mismatch and truncation | **PARTIALLY_MITIGATED** | MEDIUM | Primary muxing uses exact `-t {audio_dur}`, but error fallback at line 123 in `video/ffmpeg_pipeline.py` still reverts to `-shortest`. Remove `-shortest` from fallback. |
| **2** | Direct publishing paths bypassing kill switch | **CONFIRMED DEFECT** | CRITICAL | Neither `publishing/instagram_integration.py` nor `publishing/youtube_integration.py` calls `kill_switch.assert_not_active()`. Add mandatory assertion at entry points. |
| **3** | Dashboard routes bypassing orchestration | **CONFIRMED DEFECT** | HIGH | `dashboard/routes.py` instantiates `SuperIntelligencePipeline` directly, skipping NEXUS stages (policy checks, opportunity scoring, task briefs). Route dashboard through orchestrator. |
| **4** | Duplicate publishing queue entries | **CONFIRMED DEFECT** | HIGH | `publishing/queue.py:enqueue_reel` performs blind `INSERT` without checking existing job ID in `publishing_queue`. Enforce idempotency and unique index. |
| **5** | Weak approval identity verification | **CONFIRMED DEFECT** | HIGH | `publishing/approval.py:approve_reel` defaults to `reviewer_name="Lead Editor"`, bypassing `owner_config.py` authorized reviewers. Enforce strict reviewer identity checks. |
| **6** | Static or unused analytics & intelligence agents | **CONFIRMED DEFECT** | MEDIUM | `AnalyticsAgent` is never dispatched in `NexusOrchestrator.execute_workflow()`. `PerformanceTracker` is only populated via manual dashboard form submission. |
| **7** | Fact-checking trusts database summaries | **CONFIRMED DEFECT** | CRITICAL | `FactChecker.audit_script_claims` compiles ground truth from `script_data.get("summary")` stored in SQLite, rather than fetching or verifying the primary source text. |
| **8** | Synthetic fallback topics producing unsupported claims | **CONFIRMED DEFECT** | HIGH | `FallbackTemplates.generate_script` injects pre-written boilerplate about "refined algorithmic optimizations" into any topic lacking deep text. Must fail or mark claims UNVERIFIED. |
| **9** | Fixed storyboard structures | **CONFIRMED DEFECT** | HIGH | `StoryboardGenerator.generate_storyboard` hardcodes exactly 7 scenes (`scene_001_hook` to `scene_007_takeaway`). Cannot accommodate dynamic narrative lengths. |
| **10** | Asset registration failures silently ignored | **CONFIRMED DEFECT** | MEDIUM | `visuals/visual_router.py:411` catches asset registration exceptions with `except Exception as e: logger.warning(...)`, allowing unverified assets into final compositions. |
| **11** | Competing rendering architectures simultaneously active | **CONFIRMED DEFECT** | MEDIUM | Legacy `rendering/video_renderer.py` and V2 `video/hyperframes_runner.py` both exist in codebase. Deprecate legacy renderer; route all rendering through unified V2 pipeline. |
| **12** | WhisperQA / quality checks not enforced | **CONFIRMED DEFECT** | HIGH | `core/pipeline.py:225` logs `audio_qa_report` with `logger.info`, but never checks `if not audio_qa_report.get('passed'): raise QualityError()`. It is a non-blocking soft log. |
| **13** | Unmanaged draft files consuming storage | **CONFIRMED DEFECT** | MEDIUM | Direct scan revealed **1.17 GB** across **4,810 unmanaged files** in `output/` and `.temp/`. No automated retention or cleanup policy exists. |
| **14** | External integrations marked operational without runtime evidence | **CONFIRMED DEFECT** | MEDIUM | Meta Instagram Graph API and YouTube Data API are labelled configured or operational in dashboard banners despite empty credentials (`META_APP_ID=""`). |

---

## 2. In-Depth Empirical Evidence & Code References

### Risk 1: Audio/Video Truncation Fallback
- **Location:** `video/ffmpeg_pipeline.py:116-126`
- **Evidence:** When the primary muxing command with `-t {audio_dur:.2f}` encounters a subtitle escaping error, the fallback command executes:
  ```python
  fallback_cmd = [
      self.ffmpeg_cmd, "-y",
      "-i", str(v_in), "-i", str(a_in),
      "-c:v", "libx264", "-pix_fmt", "yuv420p",
      "-c:a", "aac", "-b:a", "192k",
      "-shortest",  # <--- CRITICAL: Truncates audio if video duration is slightly shorter
      str(out_path),
  ]
  ```
- **Remediation:** Replace `-shortest` with `-t {audio_dur:.2f}` in the fallback path as well.

### Risk 2: Direct Publishing Paths Bypassing Kill Switch
- **Location:** `publishing/instagram_integration.py:502-530`, `publishing/youtube_integration.py:210-250`
- **Evidence:** A text search for `kill_switch` across the entire `publishing/` directory returned zero occurrences. If an operator triggers `POST /api/instagram/publish/{id}`, the request proceeds even if `.kill_switch` exists on disk or `KillSwitch.activate()` was called.
- **Remediation:** Inject `get_kill_switch().assert_not_active("Publishing:Instagram")` into `InstagramIntegration.publish_reel` and `YouTubeIntegration.publish_video`.

### Risk 3: Dashboard Routes Bypassing Orchestration
- **Location:** `dashboard/routes.py:46-49`
- **Evidence:**
  ```python
  pipeline = SuperIntelligencePipeline(db=db, config=config)
  approval_mgr = ApprovalManager(db=db, config=config)
  ```
  The dashboard never imports or calls `NexusOrchestrator` (`core/orchestrator.py`). All UI-initiated jobs bypass Stage 2 (Policy Validation), Stage 3 (Opportunity Scoring), and Stage 4/5 (TaskBriefStore lifecycle tracking).
- **Remediation:** Refactor dashboard execution triggers to dispatch through `NexusOrchestrator.execute_workflow()`.

### Risk 4: Duplicate Publishing Queue Entries
- **Location:** `publishing/queue.py:75-96`
- **Evidence:**
  ```python
  cursor.execute(
      """
      INSERT INTO publishing_queue (
          production_job_id, job_id, title, caption, caption_text,
          scheduled_time, scheduled_for, status, video_path,
          hashtags, retry_count
      ) VALUES (?, ?, ?, ?, ?, ?, ?, 'SCHEDULED', ?, ?, 0)
      """,
      ...
  )
  ```
  No check exists for whether `production_job_id` is already queued. Calling approval or enqueue twice creates multiple duplicate posts scheduled for different weekdays.
- **Remediation:** Query `SELECT id FROM publishing_queue WHERE production_job_id = ? AND status IN ('SCHEDULED', 'QUEUED')` before inserting, or add a UNIQUE constraint.

### Risk 5: Weak Approval Identity Verification
- **Location:** `publishing/approval.py:47-52`, `dashboard/routes.py:218-222`
- **Evidence:** `approval_mgr.approve_reel` defaults `reviewer_name="Lead Editor"` and performs no authentication check against `owner_config.py:authorized_reviewers`. Furthermore, `dashboard/routes.py` invokes `approval_mgr.approve_reel` directly, bypassing the anti-self-approval checks in `publishing/approval_queue.py`.
- **Remediation:** Unify approval logic into `ApprovalQueue`, require explicit reviewer identity, validate against `owner_config`, and enforce self-approval blocks across both web and CLI interfaces.

### Risk 7: Fact-Checking Trusts Database Summaries
- **Location:** `content/fact_checker.py:109-124`
- **Evidence:**
  ```python
  ref_corpus_parts = [
      script_data.get("title", ""),
      script_data.get("summary", ""),
      script_data.get("context", ""),
      script_data.get("content_objective", ""),
  ]
  ```
  The fact-checker treats the RSS feed's 2-sentence summary as ground truth. If the script writer elaborates or invents plausible technical claims, the fact checker scores them as `VERIFIED` as long as common keywords match the summary.
- **Remediation:** In Phase 1 (Editorial Intelligence), build a structured Research Dossier that fetches and validates against primary source documents.

### Risk 8: Synthetic Fallback Generating Unsupported Claims
- **Location:** `intelligence/fallback_templates.py:25-28`
- **Evidence:**
  ```python
  explanation = "Architecturally, this advance leverages refined algorithmic optimizations and focused data pipelines rather than just raw brute-force compute."
  implications = "For engineers and builders, this unlocks more efficient inference, reduced operational latency, and smarter autonomous workflows."
  limitations = "However, researchers note that edge-case validation and broader stress testing in complex production environments are still underway."
  ```
  These pre-scripted phrases are inserted whenever an article has insufficient detail, fabricating an authoritative tone without evidence.
- **Remediation:** Prohibit generic synthetic boilerplate. If primary research is insufficient, mark the topic as `RESEARCH_BLOCKED`.

### Risk 9: Fixed 7-Scene Storyboard Lock
- **Location:** `content/storyboard.py:131-290`
- **Evidence:**
  `generate_storyboard` explicitly defines scenes 1 through 7 with hardcoded roles (`HOOK`, `CONTEXT`, `DEVELOPMENT`, `EXPLANATION`, `IMPLICATIONS`, `LIMITATIONS`, `TAKEAWAY`).
- **Remediation:** In Phase 2, transition to dynamic scene planning where scene count ($N \in [3, 12]$) and individual scene durations are driven by story structure.

### Risk 12: Soft Non-Enforced Quality Checks
- **Location:** `core/pipeline.py:223-227`, `core/pipeline.py:293-298`
- **Evidence:**
  ```python
  audio_qa_report = self.whisper_qa.verify_audio(...)
  logger.info(f"Narration QA: passed={audio_qa_report.get('passed')}")
  # Does not halt or raise error on failure!
  ```
  The pipeline logs `passed=False` and continues rendering. Only `VideoValidator` raises an exception.
- **Remediation:** Enforce hard gating on critical QA failures (e.g. intelligibility score $< 0.65$ or severe digital clipping).

### Risk 13: Unmanaged Draft Accumulation
- **Location:** Direct filesystem audit of `A:\SUPER.INTELLIGENCEEE\output\` and `A:\SUPER.INTELLIGENCEEE\.temp\`
- **Evidence:** **1,106,500,203 bytes** (1.106 GB) across 453 files in `output/` and **66,437,708 bytes** (66.4 MB) across 4,357 files in `.temp/`. Total: **1.17 GB**.
- **Remediation:** Implement an automatic draft cleanup policy in Phase 4 that rotates unapproved intermediate WAV/PNG/MP4 buffers while preserving final approved reels.

