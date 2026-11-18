# SUPER.INTELLIGENCEEE — Phase 2 Architecture Specification
## Creative Intelligence, Dynamic Story Architecture & Scene Planning

**Date:** 2026-11-06  
**Architect:** Principal Creative Systems Architect & Senior AI Video Production Engineer  
**Objective:** Decouple SUPER.INTELLIGENCEEE from the rigid 7-scene slide format, establishing an intelligent, story-first creative direction system that supports variable scene counts ($N \in [3, 12]$) and dynamic narrative patterns.

---

## 1. System Architecture Overview

```mermaid
flowchart TD
    subgraph EditorialInputs ["1. Editorial Intelligence Inputs"]
        Dossier[ResearchDossier] --> Architect[StoryArchitectureEngine]
        Brief[ContentBrief] --> Architect
    end

    subgraph NarrativeArchitecture ["2. Story Architecture Engine"]
        Architect --> Complexity[Topic Complexity Analyzer]
        Complexity --> StructSelect[Narrative Structure Selector]
        StructSelect --> ArchPlan[StoryArchitecturePlan (3-12 Beats)]
    end

    subgraph CreativeDirection ["3. Creative Director"]
        ArchPlan --> Director[CreativeDirector]
        Dossier --> Director
        Director --> DirPlan[CreativeDirectionPlan (Palette, Demos, Diagrams, B-Roll, Sound)]
    end

    subgraph DynamicScenePlanning ["4. Dynamic Scene Planner"]
        DirPlan --> Planner[DynamicScenePlanner]
        ArchPlan --> Planner
        Planner --> ScenePlan[DynamicScenePlan (Typed DynamicScenes)]
    end

    subgraph QAAndSync ["5. Quality & Timing Governance"]
        ScenePlan --> Diversity[VisualDiversityAnalyzer (Anti-Slideshow / Density)]
        Diversity --> Timing[TimingCoordinator (Exact Audio Sync & Holds)]
        Timing --> Adapter[Bi-Directional UniversalScene Adapter]
    end

    subgraph ProductionOutput ["6. Production & Rendering"]
        Adapter --> UniversalScenes[UniversalScene List]
        Adapter --> LegacyDict[Legacy Storyboard Dict]
        UniversalScenes --> HyperFrames[HyperFrames / FFmpeg Pipeline]
    end
```

---

## 2. Core Subsystems & Responsibilities

### 2.1 Story Architecture Engine (`creative/story_architecture/story_architect.py`)
- **Responsibility:** Evaluates topic complexity, density, claim count, and developer utility to select or synthesize the optimal narrative structure.
- **Narrative Structures Supported:**
  1. `DISCOVERY_EXPLANATION_IMPLICATIONS` (3–4 scenes: Fast breaking milestones, timely releases).
  2. `PROBLEM_MECHANISM_SOLUTION_LIMITATIONS` (5–6 scenes: Deep architectural breakdowns, attention mechanisms, quantization).
  3. `QUESTION_INVESTIGATION_EVIDENCE_CONCLUSION` (4–6 scenes: Analytical deep dives, scientific claims).
  4. `DEMONSTRATION_BREAKDOWN_EVALUATION` (5–8 scenes: Developer tools, CLI frameworks, agent systems).
  5. `COMPARISON_TESTING_RESULTS_VERDICT` (5–8 scenes: Model vs. Model benchmarks, speed/accuracy head-to-heads).
  6. `HISTORICAL_BREAKTHROUGH_CURRENT_FUTURE` (6–10 scenes: Comprehensive historical & frontier technology explainers).
- **Scene Count:** Completely variable ($N \in [3, 12]$). No hardcoded 7-scene lock.

### 2.2 Creative Director (`creative/director/creative_director.py`)
- **Responsibility:** Converts abstract narrative beats into an intentional visual strategy before rendering.
- **Decisions Made:**
  - Identifies which claims deserve visual emphasis and highlighted metrics.
  - Allocates screen demonstrations for developer tooling and terminal interactions.
  - Allocates animated technical diagrams for internal model architectures.
  - Allocates cinematic B-roll for real-world context and hardware wafers.
  - Formulates sound design strategy (subtle drones, mechanical reveals, ducked whoosh transitions).
  - Specifies ending resolution and branding lockup.

### 2.3 Dynamic Scene Planner (`creative/scene_planner/dynamic_scene_planner.py`)
- **Responsibility:** Produces the executable `DynamicScenePlan`.
- **Scene Attributes:**
  - `scene_id`, `sequence`, `narration`, `scene_objective`, `scene_type`
  - `visual_concept`, `visual_description`
  - `asset_requirements` (typed `AssetRequirement` objects)
  - `camera_direction` (`push_in_slow`, `static_locked`, `drift_subtle`, `snap_zoom`)
  - `motion_direction` (`draw_reveal`, `slide_up`, `zoom_punch`, `ken_burns`)
  - `on_screen_text`, `transition_in`, `transition_out`
  - `estimated_duration`, `actual_duration`
  - `audio_cues` (typed `AudioCue` objects with timestamp offsets and gains)
  - `evidence_references`, `production_complexity`

### 2.4 Visual Diversity Analyzer (`creative/scene_planner/visual_diversity_analyzer.py`)
- **Responsibility:** Enforces semantic and compositional variety to eliminate slideshow appearances.
- **Checks Performed:**
  - Consecutive identical scene types (e.g. typography next to typography) -> flags and remediates.
  - Scene-type distribution (requires $\ge 3\text{--}4$ unique visual treatments).
  - Excessive on-screen text density ($> 12$ words / $> 75$ characters) -> condenses text to punchy headlines.
  - Motion preset variety across scenes.

### 2.5 Timing Coordinator (`creative/scene_planner/timing_coordinator.py`)
- **Responsibility:** Audio-visual synchronization and pacing governance.
- **Capabilities:**
  - Estimates narration durations based on spoken rate (~2.5 words per second).
  - Reads exact audio duration directly from synthesized WAV headers via `wave`.
  - Injects visual hold padding ($+0.25\text{s}$) to prevent abrupt scene cuts.
  - Audits for rushed scenes ($< 2.5\text{s}$) and static frame stagnation ($> 15.0\text{s}$).

---

## 3. Shared Creative Contracts & Bi-Directional Compatibility

The shared contracts in [`core/creative_contracts.py`](file:///A:/SUPER.INTELLIGENCEEE/core/creative_contracts.py) provide complete interoperability:
- **`DynamicScene.to_universal_scene()`:** Transforms any dynamic scene into a `UniversalScene` object understood by the modern visual engine.
- **`DynamicScene.to_dict()`:** Exports a backward-compatible dictionary with both modern and legacy field aliases (`scene_number`, `duration`, `visual_type`, `headline`), allowing existing renderers (`video/template_builder.py`, `video/hyperframes_runner.py`) to execute without modifications.
- **`StoryboardGenerator.generate_storyboard()`:** Updated to automatically recognize and pass through variable scene counts from `DynamicScenePlan`.

---

## 4. Creative Format Profiles

Three independent format profiles are established under `creative/formats/`:
1. **Tech Documentary (`TechDocumentaryProfile`):** Primary production priority. Combines screen demos, animated diagrams, B-roll, kinetic typography, and synchronized sound design (45–90s target duration).
2. **Trend-Driven Short-Form (`TrendShortFormProfile`):** High-tempo breaking news and discoveries (25–45s target duration, 3–5 scenes).
3. **Animated Storytelling (`AnimatedStorytellingProfile`):** Planning contracts for character identity, environment consistency, and camera direction (50–90s target duration).

