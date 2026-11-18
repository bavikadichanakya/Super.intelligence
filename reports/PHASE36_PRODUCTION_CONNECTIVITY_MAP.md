# SUPER.INTELLIGENCEEE — PHASE 3.6
# PRODUCTION CONNECTIVITY MAP & ARCHITECTURAL TRACE

**Author:** Senior Video-Production Systems Architect & Software Auditor  
**Date:** 2026-11-07  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Purpose:** Disentangle implemented modules from production-connected modules; map actual runtime execution paths against the intended system architecture.

---

## 1. Architectural Reality: Intended vs Actual Execution Path

A core directive of Phase 3.6 is: **Do not confuse implemented modules with production-connected modules.**

The forensic investigation reveals a significant structural bifurcation between the planned modular architecture and the actual benchmark production script.

### Intended Architecture vs Actual Benchmark Script Path

```mermaid
flowchart TD
    subgraph INTENDED_MODULAR_PIPELINE["Intended Modular Architecture (Designed in Phase 1-2)"]
        A1["RSSCollector / AgentReach"] --> A2["ResearchAnalyst (Dossier)"]
        A2 --> A3["TopicScorer (100-pt)"]
        A3 --> A4["StoryArchitectureEngine"]
        A4 --> A5["CreativeDirector"]
        A5 --> A6["DynamicScenePlanner (Variable Scenes)"]
        A6 --> A7["DocumentaryCompositor"]
    end

    subgraph ACTUAL_PRODUCTION_PATH["Actual Benchmark Script Path (produce_phase3_5_tech_doc.py)"]
        B1["Hardcoded 6-Scene Dict Array in Script"] -->|Bypasses A1-A6| B2["Voicebox TTS (am_liam)"]
        B2 --> B3["TechDocProducer.produce_documentary()"]
        B3 --> B4["DocumentaryCompositor"]
        B4 --> B5["Individual PIL Scene Engines"]
        B5 --> B6["AudioMixer & FFmpeg Mux"]
        B6 --> B7["Stream Verification & Visual QA"]
    end
```

---

## 2. Detailed Production Connectivity Trace

### 2.1 The Production Entry Point (`scripts/produce_phase3_5_tech_doc.py`)
- **Lines 47–132:** Defines `scenes_data = [...]` as a static Python list containing 6 predefined scene dictionaries (Opening $\rightarrow$ Silicon Die $\rightarrow$ Verification Tree $\rightarrow$ Terminal Demo $\rightarrow$ Benchmarks $\rightarrow$ Verdict).
- **Architectural Disconnect:** `StoryArchitectureEngine.plan_architecture()` and `DynamicScenePlanner.plan_scenes()` are completely bypassed. The system did not dynamically evaluate topic complexity or synthesize beats; the human engineer hardcoded the scene count, narration text, and telemetry strings directly into the script.

### 2.2 Voice Synthesis Step (`scripts/produce_phase3_5_tech_doc.py:134-162`)
- **Connected Modules:** `audio/providers/voicebox_provider.py` (`VoiceboxProvider`).
- **Connection Status:** `LIVE_IN_PRODUCTION`.
- **Execution:** Connects to `http://127.0.0.1:17493`, synthesizes American Male narration stems (`am_liam`) via Kokoro-82M, validates 24 kHz WAV format, and asserts total duration between 55.0s and 75.0s.

### 2.3 Master Production Coordinator (`creative/tech_documentary/documentary_renderer/tech_doc_producer.py`)
- **Connection Status:** `LIVE_IN_PRODUCTION`.
- **Trace:**
  - `produce_documentary()` (Line 200) receives `scene_plan`, `topic`, `scene_audio_files`.
  - Lines 230–245: Computes cumulative duration with 0.25s transition padding per scene.
  - Lines 255–270: Iterates through each scene and calls `self.compositor.render_scene()`.
  - Lines 275–310: Calls `self.sound_designer.assemble_soundscape()`:
    - Generates 6-act continuous adaptive electronic soundtrack (`AdaptiveSoundtrack`).
    - Synthesizes 10 discrete UI/motion sound cues (`SoundCueTimeline`).
    - Mixes speech + score + foley with sidechain ducking (Threshold 0.08, Ratio 6.0:1) and normalizes to -14.0 LUFS.
  - Lines 312–330: Calls `self.caption_gen.generate_captions()` (outputs SRT, VTT, and ASS files).
  - Lines 332–340: Calls `self.ffmpeg_pipeline.concat_clips()` to generate `intermediate_video.mp4`.
  - Lines 342–355: Calls `self.ffmpeg_pipeline.compose_final_reel()` twice:
    - First for clean archival master: `raw_documentary.mp4` (video + audio, no captions).
    - Second for release master: `tech_doc_final.mp4` (video + audio + burned ASS subtitles).
  - Lines 357–365: Calls `self.verify_exported_video_stream()` on both MP4 files.
  - Lines 366–380: Calls `self.visual_qa.run_full_visual_audit()` and `MotionAuditor.audit_video()`.

### 2.4 The Scene Compositor (`creative/tech_documentary/scene_composition/documentary_compositor.py`)
- **Connection Status:** `LIVE_IN_PRODUCTION`.
- **Dispatch Mapping:**
  - `SceneType.KINETIC_TYPOGRAPHY` $\rightarrow$ `self.kinetic_engine.render_kinetic_clip()`
  - `SceneType.CINEMATIC_BROLL` $\rightarrow$ `self.asset_resolver.resolve_broll_clip()`
  - `SceneType.TECHNICAL_DIAGRAM` $\rightarrow$ `self.diagram_engine.render_diagram_clip()`
  - `SceneType.SCREEN_DEMONSTRATION` $\rightarrow$ `self.terminal_animator.render_terminal_clip()`
  - `SceneType.DATA_VISUALIZATION` $\rightarrow$ `self.hud_engine.render_metric_hud_clip()`
  - `SceneType.NARRATIVE_SCENE` $\rightarrow$ `self.verdict_engine.render_verdict_clip()`

---

## 3. The Broken Link: Why Creative Director & Scene Planner Were Decoupled

When inspecting `creative/director/creative_director.py` and `creative/scene_planner/dynamic_scene_planner.py`:

```
┌────────────────────────────────────────┐
│ StoryArchitectureEngine                │ -> Outputs StoryArchitecturePlan
└────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ CreativeDirector                       │ -> Hardcodes Dark Theme (#080b11) & Neon Cyan!
└────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ DynamicScenePlanner                    │ -> Outputs DynamicScenePlan (with camera_direction)
└────────────────────────────────────────┘
                   │  MISSING ADAPTER:
                   ▼  (Compositor expects a raw Python Dict, not a DynamicScene dataclass!)
┌────────────────────────────────────────┐
│ TechDocProducer.produce_documentary()  │ -> Expects scene_plan: List[Dict[str, Any]]
└────────────────────────────────────────┘
```

1. **Theme Incompatibility:** `CreativeDirector` was still emitting `"theme": "Dark Obsidian & Neon Telemetry"`, `"background_primary": "#080b11"`. To comply with Phase 3.2+ Light-First visual directives, the production engineer bypassed `CreativeDirector` entirely and directly coded light-first scenes in the benchmark script.
2. **Dataclass vs Dict Contract Mismatch:** `DynamicScenePlanner` returns `DynamicScenePlan` with instances of `DynamicScene` dataclasses containing properties `sequence`, `scene_objective`, `camera_direction`. Meanwhile, `produce_documentary()` and `DocumentaryCompositor` expected dictionary keys `scene_index`, `narrative_role`, `stat_number`.
3. **Ignored Camera Directives:** `DynamicScene` provides `camera_direction = "push_in_slow"` and `motion_direction = "draw_reveal"`. However, `DocumentaryCompositor` and the underlying PIL engines have **zero parameter inputs** for camera movement! The fields are dropped on the floor.

---

## 4. Component Status Inventory

### Active In Production (`LIVE_IN_PRODUCTION`)
- `scripts/produce_phase3_5_tech_doc.py`
- `creative/tech_documentary/documentary_renderer/tech_doc_producer.py`
- `creative/tech_documentary/scene_composition/documentary_compositor.py`
- `creative/tech_documentary/kinetic_typography/kinetic_engine.py`
- `creative/tech_documentary/cinematic_assets/asset_resolver.py`
- `creative/tech_documentary/technical_diagrams/vector_diagram_engine.py`
- `creative/tech_documentary/screen_demonstration/terminal_animator.py`
- `creative/tech_documentary/motion_graphics/hud_telemetry.py`
- `creative/tech_documentary/verdict/verdict_engine.py`
- `audio/providers/voicebox_provider.py`
- `audio/audio_mixer.py`
- `audio/sound_design/adaptive_soundtrack.py`
- `captions/caption_generator.py`
- `video/ffmpeg_pipeline.py`
- `rendering/visual_qa.py`
- `rendering/motion_audit.py`

### Implemented But Not Connected (`IMPLEMENTED_NOT_CONNECTED`)
- `creative/story_architecture/story_architect.py` (Bypassed by hardcoded script)
- `creative/director/creative_director.py` (Bypassed due to dark-theme obsolescence)
- `creative/scene_planner/dynamic_scene_planner.py` (Bypassed due to contract mismatch)
- `creative/scene_planner/timing_coordinator.py` (Bypassed; timing handled inline in producer)
- `creative/scene_planner/visual_diversity_analyzer.py` (Bypassed; diversity checked post-hoc in QA)
- `video/hyperframes_runner.py` (Inactive in Phase 3.5.1)
- `video/template_builder.py` (Inactive in Phase 3.5.1)
- `visuals/graphics.py` (Legacy PIL chart generator)
- `visuals/visual_router.py` (Legacy router)
- `core/orchestrator.py` (NexusOrchestrator designed for 9-agent social loop, disconnected from TechDocProducer)

### Simulated or Mock Fallback (`MOCK_OR_SIMULATED`)
- `visuals/stock_provider.py` (Solid color generator fallback when Pexels API key missing)
- `creative/scene_planner/dynamic_scene_planner.py:68-80` (`camera_direction` is simulated metadata)

### Incomplete or Defective (`INCOMPLETE` / `FAILED`)
- `captions/whisper_qa.py` (Not executed in automated build loop)
- `research/agent_reach_connector.py:178` (Crashes with `TypeError` when `"raw"` is `None` in search results)
- `research/public_web_collector.py` (Fails with 405 on Ars Technica and 429 on VentureBeat)

