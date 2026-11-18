# SUPER.INTELLIGENCEEE — Phase 3 Tech Documentary Engine Architecture

**Date:** 2026-11-06  
**Architect:** Principal Systems Architect & Senior AI Video Production Engineer  
**Status:** Approved for Implementation  
**Operating Constraint:** Windows 11, Python 3.11, 8 GB RAM, ₹0 Operating Budget  

---

## 1. System Vision & Objective

The **Tech Documentary Production Engine** transforms raw technical research dossiers into visually rich, broadcast-grade technology mini-documentaries. Unlike slideshow generators, this engine produces genuine continuous motion, interactive terminal code walkthroughs, progressive vector system diagrams, kinetic typography, and multi-layered sound design.

```mermaid
flowchart TD
    Dossier[Research Dossier / Content Brief] --> Architect[Dynamic Story Architect]
    Architect --> Director[Creative Director]
    Director --> Planner[Dynamic Scene Planner]
    Planner --> ScenePlan[DynamicScenePlan (Strict Contracts)]
    
    subgraph Production Engine [Tech Documentary Engine: creative/tech_documentary/]
        ScenePlan --> Dispatcher[TechDocProducer]
        Dispatcher --> TermAnim[Terminal Animator\n(Typing & Execution)]
        Dispatcher --> DiagEngine[Vector Diagram Engine\n(Progressive Dataflows)]
        Dispatcher --> KineticTypo[Kinetic Typography\n(Spring Easing & Stats)]
        Dispatcher --> AssetResolver[Cinematic Asset Resolver\n(Hardware B-Roll & Provenance)]
        Dispatcher --> HUDGen[HUD Telemetry Engine\n(Gauges & Diagnostics)]
        
        TermAnim --> Compositor[Documentary Compositor\n(1080x1920 Vertical Layouts)]
        DiagEngine --> Compositor
        KineticTypo --> Compositor
        AssetResolver --> Compositor
        HUDGen --> Compositor
        
        Compositor --> Transitions[Transition Router\n(Cinematic FFmpeg xfade)]
        Transitions --> RawVideo[Continuous Raw Video (30 fps)]
    end
    
    subgraph Audio Soundscape [sound_design/sound_designer.py]
        Narration[Jarvis Male TTS (-14 LUFS)] --> SoundDesigner[Multi-Layer Audio Mixer]
        SubDrone[Low-End Tech Drone (-28 dB)] --> SoundDesigner
        FoleySFX[Mechanical Typing & Clicks] --> SoundDesigner
        WhooshSFX[Ducked Transition Whooshes] --> SoundDesigner
        SoundDesigner --> MasterAudio[Master Soundscape WAV]
    end
    
    RawVideo --> FinalMux[FFmpeg Final Mux & Subtitles]
    MasterAudio --> FinalMux
    FinalMux --> FinalDoc[Broadcast Tech Documentary MP4]
    FinalDoc --> VisualQA[Visual QA Subsystem & Manifest]
```

---

## 2. Subsystem Architectural Specifications

### 2.1 Screen Demonstration Subsystem (`screen_demonstration/terminal_animator.py`)
- **Objective:** Render realistic dark-mode developer CLI walkthroughs.
- **Visual Spec:**
  - Modern terminal window with macOS/Linux traffic light buttons (close, minimize, expand).
  - Customizable prompt: `❯ super-cli run --quantize fp8`.
  - Realistic typing animation with variable keystroke delays and blinking block cursor.
  - Progressive streaming output (progress bars, throughput tables, benchmark tokens/sec).
  - Background styling: 1080x1920 vertical canvas with obsidian gradient `#050811`, subtle neon telemetry borders, and active line glow.

### 2.2 Technical Diagrams Subsystem (`technical_diagrams/vector_diagram_engine.py`)
- **Objective:** Render dynamic multi-stage systems architecture flows.
- **Visual Spec:**
  - Modular node graphs (e.g. Input Stage → Attention / Kernel Layer → State Matrix → Output Projection).
  - Progressive stage illumination: nodes light up in sequence as narration explains the mechanism.
  - Animated data packet flow: glowing particle pulses traveling along connecting vector lines.
  - Telemetry badges at each node displaying runtime latency, memory footprint, or tensor dimensions.

### 2.3 Motion Graphics & Telemetry (`motion_graphics/hud_telemetry.py`)
- **Objective:** Procedural diagnostic telemetry HUD overlays.
- **Visual Spec:**
  - Precision grid coordinates (`[SYS.TEL 47.109 // KERNEL_INIT]`).
  - Circular telemetry rings and animated progress gauges (`SPEEDUP: 3.4x`).
  - Status indicators with live timestamp and pulsing indicator beacons.
  - Subtle scanline overlay and corner reticles.

### 2.4 Cinematic Assets Subsystem (`cinematic_assets/asset_resolver.py`)
- **Objective:** Resolve high-quality B-roll, hardware macro photography, and paper schematics with cryptographic provenance.
- **Visual Spec:**
  - Curated high-tech hardware textures (silicon dies, GPU racks, neural network representations).
  - Aspect ratio adaptation (panoramic 16:9 to vertical 9:16 with Gaussian blurred background fill or split framing).
  - Cryptographic verification: SHA-256 integrity hash and attribution metadata saved to production manifest.

### 2.5 Kinetic Typography Subsystem (`kinetic_typography/kinetic_engine.py`)
- **Objective:** High-impact text motion graphics for hooks, key findings, and takeaways.
- **Visual Spec:**
  - Large punchy headline typography with spring scale easing ($0.95 \rightarrow 1.05 \rightarrow 1.0$).
  - Animated numerical counter animations ($0\% \rightarrow 340\%$).
  - Two-tone color emphasis (e.g. Neon Emerald `#00ff88` on Obsidian `#080b11`).
  - High-legibility vertical safe-zone compliance (avoiding TikTok/Reels UI overlay zones).

### 2.6 Scene Composition Subsystem (`scene_composition/documentary_compositor.py`)
- **Objective:** Assemble individual visual elements into balanced 1080x1920 frames and clips.
- **Supported Layout Archetypes:**
  1. `TERMINAL_WALKTHROUGH`: Centered terminal window with top context header and bottom live telemetry.
  2. `ARCHITECTURE_FLOW`: Multi-stage vector diagram centered with top topic header and bottom node details.
  3. `SPLIT_EVALUATION`: Dual vertical split (Top: Real Demo, Bottom: Performance Telemetry).
  4. `METRIC_CALLOUT`: Large kinetic typography stat counter with peripheral diagnostic meters.
  5. `CINEMATIC_OVERLAY`: Full-bleed hardware macro asset with gradient scrim and lower-third headline.

### 2.7 Transition Router (`transitions/transition_router.py`)
- **Objective:** Apply cinematic transitions between scene clips without performance overhead.
- **Supported Transitions:**
  - `crossfade`: Smooth blending between scene clips.
  - `wipeleft` / `wiperight`: Fast directional horizontal wipes.
  - `dissolve`: Organic dissolve transition.
  - `circleopen`: Iris transition for revealing hardware or architectural breakthroughs.
- **Implementation:** Leverages FFmpeg `xfade` filter with fallback to clean cuts if duration constraints require.

### 2.8 Sound Design Subsystem (`sound_design/sound_designer.py`)
- **Objective:** Produce an authentic multi-track soundscape.
- **Audio Layers:**
  1. `Voice Track`: Master narration (Jarvis RP male voice) normalized to -14.0 LUFS.
  2. `Bed Track`: Subtle continuous low-end atmospheric tech drone (-28.0 LUFS) with gentle ducking.
  3. `Diegetic Foley`: Tactile mechanical keyboard clicks during terminal typing scenes; subtle digital chime on diagram reveals.
  4. `Punctuation SFX`: Ducked whoosh transitions (-18.0 dB) at scene boundary markers.

### 2.9 Master Tech Documentary Producer (`documentary_renderer/tech_doc_producer.py`)
- **Objective:** Master coordinator uniting all subsystems.
- **Interface:** Takes `DynamicScenePlan`, topic metadata, and synthesized audio files; orchestrates clip rendering, composition, audio soundscape mastering, transition application, and final FFmpeg assembly.
- **Output:** Fully packaged 1080x1920 30fps technology documentary MP4 with complete provenance and automated visual QA validation.

---

## 3. Resource & Memory Footprint Budget

- **Max RAM during scene rendering:** $< 1.5$ GB (Pillow sequential frame processing with immediate garbage collection).
- **Max Disk Space during temp render:** $< 250$ MB per documentary (immediate cleanup of intermediate clip directories).
- **Render Time:** $< 35$ seconds total on Windows 11 CPU for a 60-second documentary.
- **Zero-Dollar Budget:** 100% offline procedural execution without external cloud dependencies.

