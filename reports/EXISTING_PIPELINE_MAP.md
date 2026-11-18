# SUPER.INTELLIGENCEEE — Existing Pipeline Topological Map

**Audit Date:** 2026-11-06  
**Scope:** Complete architectural mapping of data flow, execution chains, database tables, and competing subsystems.

---

## 1. End-to-End Pipeline Data Flow

The codebase contains two parallel execution entry points that share submodules but operate under different governance models:
1. **NEXUS Governed Orchestrator (`core/orchestrator.py`):** 9-stage multi-agent state machine enforcing owner configuration, task briefs, and department boundaries.
2. **Direct Production Pipeline (`core/pipeline.py`):** Direct sequential pipeline that coordinates TTS, HyperFrames, and FFmpeg directly without task briefs.

```mermaid
flowchart TD
    subgraph SignalAndDiscovery ["1. Discovery & Research"]
        RSS[RSSCollector] --> DB_Topics[(SQLite: topics)]
        AgentReach[AgentReachConnector] --> DB_Topics
        DB_Topics --> Scorer[TopicScorer / OpportunityScorer]
    end

    subgraph ContentGeneration ["2. Content & Fact Checking"]
        Scorer --> Writer[ScriptWriter / FallbackTemplates]
        Writer --> DB_Scripts[(SQLite: scripts)]
        DB_Scripts --> Checker[FactChecker]
    end

    subgraph StoryboardPlanning ["3. Storyboard & Creative Planning"]
        Checker --> Storyboard[StoryboardGenerator (Rigid 7 Scenes)]
        Storyboard --> Intel[VisualIntelligenceEngine]
        Intel --> CreativePlan[CreativePlan JSON]
    end

    subgraph AudioEngine ["4. Speech & Audio Engineering"]
        Storyboard --> PiperTTS[PiperEngine (Jarvis Male ONNX)]
        PiperTTS --> AudioMixer[AudioMixer (Concatenation + EBU R128 + SFX)]
        AudioMixer --> WhisperQA[WhisperQA (Soft Non-blocking QA)]
    end

    subgraph VisualEngine ["5. Visual Composition & Rendering"]
        CreativePlan --> StockProvider[StockProvider / VisualRouter]
        StockProvider --> Assets[(SQLite: assets)]
        StockProvider --> HyperFrames[HyperFramesRunner / Zoompan]
        HyperFrames --> RawMP4[raw_visuals.mp4]
    end

    subgraph PostProduction ["6. Assembly & Muxing"]
        RawMP4 --> FFmpeg[FFmpegVideoPipeline]
        AudioMixer --> FFmpeg
        Storyboard --> Captions[CaptionGenerator (ASS/SRT)]
        Captions --> FFmpeg
        FFmpeg --> FinalReel[final.mp4]
    end

    subgraph GovernanceAndPublishing ["7. QA & Distribution Gate"]
        FinalReel --> VideoValidator[VideoValidator (FFprobe)]
        FinalReel --> VisualQA[VisualQASubsystem]
        VideoValidator --> DB_Jobs[(SQLite: production_jobs)]
        DB_Jobs --> ApprovalMgr[ApprovalManager / ApprovalQueue]
        ApprovalMgr --> Queue[(SQLite: publishing_queue)]
        Queue --> Instagram[InstagramIntegration]
        Queue --> YouTube[YouTubeIntegration]
    end
```

---

## 2. Stage-by-Stage Module Inventory

| Stage | Primary Module | Helper Modules | Database Tables | Output Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **1. Research** | `research/rss_collector.py` | `research/agent_reach_connector.py`, `research/deduplicator.py` | `topics` | Candidate topic rows |
| **2. Scoring** | `intelligence/opportunity_scorer.py` | `research/topic_scorer.py`, `research/topic_ranker.py` | `topics` | `OpportunityScore` object |
| **3. Scripting** | `content/script_writer.py` | `intelligence/fallback_templates.py`, `intelligence/hook_generator.py` | `scripts` | `script_data` dictionary |
| **4. Fact Checking** | `content/fact_checker.py` | `research/fact_checking.py`, `research/source_verifier.py` | `scripts` | `AuditResult` tuple |
| **5. Storyboard** | `content/storyboard.py` | `intelligence/scene_planner.py`, `visuals/visual_intelligence.py` | `storyboards` (file-based) | `storyboard.json`, `creative_plan.json` |
| **6. Narration** | `audio/narration.py` | `audio/piper_engine.py`, `audio/pronunciation.py`, `audio/pyttsx3_engine.py` | In-memory / filesystem | Per-scene `.wav` audio files |
| **7. Audio Master** | `audio/audio_mixer.py` | `captions/whisper_qa.py` | None | `audio_master.wav`, `audio_sfx.wav` |
| **8. Captions** | `captions/caption_generator.py` | `audio/subtitle_generator.py` | None | `.ass`, `.srt`, `.vtt`, `.json` |
| **9. Visual Synthesis** | `visuals/stock_provider.py` | `visuals/visual_router.py`, `video/template_builder.py`, `video/editorial_graphics.py` | `assets` | Scene PNGs, motion clips |
| **10. Video Render** | `video/hyperframes_runner.py` | `rendering/video_renderer.py` (legacy) | None | `raw_visuals.mp4` |
| **11. Final Mux** | `video/ffmpeg_pipeline.py` | `rendering/ffmpeg_manager.py` | None | `final.mp4` |
| **12. Technical QA**| `video/video_validator.py` | `rendering/visual_qa.py`, `rendering/quality_checker.py` | `production_jobs` | Validation report JSON |
| **13. Approval** | `publishing/approval.py` | `publishing/approval_queue.py` | `approvals`, `production_jobs` | `queue/needs-your-ok/job_*.json` |
| **14. Publishing** | `publishing/queue.py` | `publishing/instagram_integration.py`, `publishing/youtube_integration.py` | `publishing_queue` | Scheduled queue item |

---

## 3. Identification of Duplicate & Competing Subsystems

A forensic analysis of the workspace reveals several parallel, partially redundant implementations:

### 3.1 Orchestration Redundancy
- **Path A (`core/orchestrator.py` — `NexusOrchestrator`):** Implements 9 formal stages, task brief persistence (`task_briefs` table), activity logging, and policy boundaries.
- **Path B (`core/pipeline.py` — `SuperIntelligencePipeline`):** Direct script-to-render procedural orchestrator. Bypasses task briefs and policy validation.
- **Path C (`dashboard/routes.py`):** Instantiates `SuperIntelligencePipeline` directly, ignoring `NexusOrchestrator`.

### 3.2 Video Rendering Redundancy
- **Renderer A (`video/hyperframes_runner.py` + `video/template_builder.py`):** The V2 rendering engine. Generates HTML templates or uses FFmpeg zoompan clips (`clip_0.mp4`–`clip_6.mp4`), then stitches them into `raw_visuals.mp4`.
- **Renderer B (`rendering/video_renderer.py` + `rendering/ffmpeg_manager.py`):** The legacy V1 rendering engine. Creates static scene cards via `ImageManager`, runs individual Ken Burns FFmpeg filters, and muxes directly.
- *Status:* Renderer B is obsolete and creates confusion, but tests in `test_engine.py` still invoke it.

### 3.3 Publishing & Queue Redundancy
- **Queue Manager A (`publishing/queue.py`):** Inserts rows into the SQLite table `publishing_queue` for weekly weekday scheduling.
- **Queue Manager B (`publishing/content_queue.py`):** An older scheduling helper that handles basic schedule calculations.
- **Approval System A (`publishing/approval.py`):** Updates `production_jobs` and `approvals` tables.
- **Approval System B (`publishing/approval_queue.py`):** Mirrors approval state into filesystem JSON files (`queue/needs-your-ok/`) and adds anti-self-approval checks.
- *Status:* Both are partially coupled, with `ApprovalQueue` delegating to `ApprovalManager`, but `dashboard/routes.py` calling `ApprovalManager` directly, bypassing the filesystem mirror and self-check.

---

## 4. Database Schema Relationships

The SQLite database (`data/super_intelligence.db`) maintains the following core tables:
- `topics`: Discovered articles, RSS items, source URLs, scores, and status.
- `scripts`: Generated video narration, sections, word counts, and status.
- `storyboards`: Storyboard scenes and archetype assignments.
- `assets`: Registered media files, hashes, file paths, license types, and author metadata.
- `production_jobs`: Video rendering job lifecycle, status (`IN_PROGRESS`, `NEEDS_REVIEW`, `APPROVED`, `FAILED`), output paths.
- `approvals`: Human review audit logs, reviewer identities, decisions, and timestamps.
- `publishing_queue`: Scheduled publication items, platform channels, target times, and status.
- `task_briefs`: Governed task lifecycle state for department agents.
- `brand_signals`: Tracked market trends and competitor signals.
- `analytics`: Post-publication views, reach, engagement rates, and watch times.

