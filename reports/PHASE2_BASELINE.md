# SUPER.INTELLIGENCEEE — Phase 2 Architecture Baseline & Forensic Audit Report

**Date:** 2026-11-06  
**Auditor & Implementation Architect:** Principal Creative Systems Architect & Senior AI Video Production Engineer  
**Objective:** Establish the forensic baseline of the existing script-to-storyboard and rendering pipeline before implementing the Phase 2 Creative Intelligence and Dynamic Story Architecture Engine.

---

## 1. Forensic Pipeline Data-Flow Tracing

Data currently flows from discovery to final video through the following sequence:

```mermaid
flowchart LR
    Dossier[ResearchDossier] --> ScriptWriter[ScriptWriter / FallbackTemplates]
    ScriptWriter --> ScriptData[script_data (7 Sections)]
    ScriptData --> FactChecker[FactChecker]
    FactChecker --> StoryboardGen[StoryboardGenerator (Rigid 7 Scenes)]
    StoryboardGen --> Narration[NarrationService (Piper TTS)]
    Narration --> AudioMixer[AudioMixer (Concat + EBU R128 + SFX)]
    StoryboardGen --> VisualIntel[VisualIntelligenceEngine (Rigid 7 Indices)]
    VisualIntel --> StockProvider[StockProvider / VisualRouter]
    StockProvider --> HyperFrames[HyperFramesRunner (FFmpeg Zoompan)]
    HyperFrames --> FinalMux[FFmpegVideoPipeline]
    AudioMixer --> FinalMux
    FinalMux --> FinalVideo[final.mp4]
```

---

## 2. Forensic Findings & Architectural Deficiencies

### 2.1 Fixed 7-Scene Structural Lock
Every module in the creative chain contains an explicit assumption that all videos have exactly seven scenes:
1. `content/storyboard.py:131-290`: `generate_storyboard` explicitly defines scenes 1 through 7 with fixed roles (`HOOK`, `CONTEXT`, `DEVELOPMENT`, `EXPLANATION`, `IMPLICATIONS`, `LIMITATIONS`, `TAKEAWAY`).
2. `intelligence/scene_planner.py:24-100`: `plan_scenes` constructs a list of 7 hardcoded dictionaries.
3. `visuals/visual_intelligence.py:75-200`: `plan_reel_creative` uses `if idx == 1: ... elif idx == 2: ... elif idx == 7: ...`. Any scene index beyond 7 has no narrative or visual mapping.
4. `core/orchestrator.py:156,166`: Task briefs specifically dictate: *"Draft 7-section verified script"* and *"Construct 7-scene storyboard"*.
*Impact:* A fast 3-scene breaking alert or a comprehensive 10-scene technical documentary cannot be planned or rendered without schema breaking.

### 2.2 Schema Inconsistencies & Renamed Fields Across Modules
Data structures undergo multiple lossy field mappings across module boundaries:
- **Duration:** Represented as `duration_seconds` (float) in `UniversalScene` and `SceneCreativeBrief`, but expected as `duration` (float) in `HyperFramesTemplateBuilder`, and `duration_est` in `ScenePlanner`.
- **Visual Type:** Represented as `visual_archetype` (Enum) in `UniversalScene`, `visual_type` (str) in storyboard dicts, `scene_type` in `graphics.py`, and `production_mode` (Enum) in `SceneCreativeBrief`.
- **Narration Text:** Represented as `narration_text` in modern schemas, but expected as `narration` in legacy templates and audio services.
- **On-Screen Text:** Named `on_screen_text` in `UniversalScene` and `SceneCreativeBrief`, but named `headline` in `SceneProps` and `ImageManager`.
*Impact:* Modules rely on brittle runtime `.get("field_a", .get("field_b"))` chains. A unified creative contract with bi-directional adapters is mandatory.

### 2.3 Absence of Story Architecture & Narrative Pacing
Currently, the pipeline has no layer that evaluates the topic's nature to determine its narrative structure:
- Complex multi-benchmark research papers are forced into the same cadence as single-tool GitHub announcements.
- There is no mechanism to choose between:
  - *Problem → Mechanism → Solution → Limitations* (Engineering architecture)
  - *Demonstration → Technical Breakdown → Evaluation* (Developer tools & software)
  - *Comparison → Testing → Results → Verdict* (Model vs Model benchmarks)
  - *Historical Context → Breakthrough → Current State → Future Possibilities* (Deep tech explainers)

### 2.4 Lack of Genuine Creative Direction
`VisualIntelligenceEngine` generates visual briefs, but its choices are statically bound to the scene index:
- Scene 1 is always silicon wafer particles.
- Scene 2 is always an engineering bottleneck text.
- Scene 3 is always a glowing line graph.
- Scene 4 is always a blue cube network diagram.
- Scene 5 is always a server rack split-screen.
- Scene 6 is always an amber warning card.
- Scene 7 is always a closing logo.
*Impact:* Perceptual monotony. The visuals are not driven by the story or topic; they are driven by the scene number.

### 2.5 Narration and Visual Timing Disconnect
- `StoryboardGenerator` estimates durations using a fixed 2.5 words-per-second heuristic.
- `NarrationService` produces real WAV files with exact durations.
- While `core/pipeline.py` updates `duration_seconds` from actual WAV lengths, there is no timing planner that identifies pacing bottlenecks, visual hold times, or rapid-fire text prior to rendering.

---

## 3. Phase 2 Architectural Blueprint

To resolve these deficiencies, Phase 2 implements:

1. **Shared Creative Contracts (`core/creative_contracts.py`):**
   - Strictly typed Pydantic/Dataclass contracts: `StoryArchitecturePlan`, `CreativeDirectionPlan`, `DynamicScenePlan`, `DynamicScene`, `VisualInstruction`, `AssetRequirement`, `AudioCue`, `TimingMap`.
   - Bi-directional compatibility adapter to `UniversalScene` and existing renderers.
2. **Story Architecture Engine (`creative/story_architecture/`):**
   - Evaluates topic complexity, density, and evidence claims to select an optimal narrative structure.
   - Plans variable scene counts ($N \in [3, 12]$) driven by story needs.
3. **Creative Director (`creative/director/`):**
   - Decides visual purpose, visual metaphor, emphasis beats, B-roll placement, technical diagram needs, software demos, and ending resolutions.
4. **Dynamic Scene Planner (`creative/scene_planner/`):**
   - Generates fully populated, validated scene specifications with camera movements, motion presets, on-screen kinetic text, and evidence references.
5. **Creative Format Profiles (`creative/formats/`):**
   - `TechDocumentaryProfile` (Primary priority)
   - `TrendShortFormProfile`
   - `AnimatedStorytellingProfile`
6. **Visual Diversity & Timing Analyzer:**
   - Evaluates consecutive scene composition similarity, scene-type distribution, and audio-visual synchronization before rendering.

