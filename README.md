# SUPER.INTELLIGENCEEE — Autonomous 3D Educational Entertainment & Technology Documentary Engine

> **Understand What's Coming.**
> An industrial-grade, local-first, character-led autonomous media engine producing broadcast-quality 1080×1920 (9:16) educational entertainment and technology documentary videos.

---

## 1. Executive Overview & Creative Reset

**SUPER.INTELLIGENCEEE** combines character-led 3D storytelling, physical demonstrations, and rigorous technical explainers. Rather than generic slides or static talking heads, SUPER.INTELLIGENCEEE is driven by an original, recurring 3D animated host who actively demonstrates concepts, compares objects, reacts to technical breakthroughs, and simplifies complex artificial intelligence and frontier technology topics.

```
       ┌────────────────────────────────────────────────────────┐
       │             SUPER.INTELLIGENCEEE PIPELINE             │
       └────────────────────────────────────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Topic Research   │    │ Fact-Checking &  │    │ 3D Character     │
│ & Intake         │───►│ Editorial Script │───►│ Kinematics       │
│ (RSS / Web / ArXiv)    │ (7-Scene Arc)    │    │ (Remotion / R3F) │
└──────────────────┘    └──────────────────┘    └──────────────────┘
                                                           │
         ┌─────────────────────────────────────────────────┘
         ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Hybrid Rendering │    │ Kokoro-82M Audio │    │ Human-in-Loop    │
│ (Remotion+ThreeJS│───►│ & -16 LUFS Mixer │───►│ Review & Secure  │
│  + Manim Engine) │    │ (am_liam Voice)  │    │ Queue / Publish  │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## 2. Canonical 3D Host: Kavi

The face of SUPER.INTELLIGENCEEE is **Kavi**, an intelligent, curious, and witty technology presenter. Reconstructed from the canonical design authorities (`Character 3D.mp4` primary visual authority, `character.me.png` identity reference):

- **3D Asset Footprint:** Lightweight 1.30 MB GLTF 2.0 asset (`output/experiment_a3/character.glb`, `public/models/super_character/character.glb`).
- **Pixar Anatomical Proportions:** Scaled Disney/Pixar head volume with recessed eye sockets, zygomatic cheek curvature, and open forehead.
- **Hair Architecture:** 54 individual 3D helical curl locks with randomized orientation forming realistic wavy bangs, lush crown, and tapered sideburns.
- **Iconic Spectacles:** Extruded rounded-rectangle dark acetate frames with a keyhole bridge and temple arms.
- **Facial Rigging & Morph Targets:** 10 ARKit-compatible smooth Gaussian morph targets (`mouthSmile`, `mouthOpen`, `mouthPucker`, `mouthFrown`, `jawDropWide`, `browLeftUp`, `browRightUp`, `browFurrow`, `blinkLeft`, `blinkRight`).
- **Skeletal Armature:** Complete hierarchical skeleton (`Root -> Hips -> Spine -> Chest -> Neck -> Head`, dual Clavicle/Arm chains, and Prop Sockets).
- **Presenter Props:** 64-page spiral technical reporter notebook held facing the viewer, and yellow drafting pencil held ready to write and point.
- **Wardrobe:** Charcoal technical jacket with standing funnel collar, orange accent trim, orange zipper piping, and raglan shoulder caps.

### 10-Step Deterministic Kinematic Progression
The 540-frame (18.0s @ 30 FPS) Remotion validation sequence (`character_3d_validation.mp4`) verifies:
1. **Neutral Standing Pose** — Sinusoidal breathing, calm resting warmth.
2. **Head Rotation** — $\pm 22^\circ$ yaw sweep and pitch, establishing cranium volume and parallax.
3. **Eye Tracking Gaze** — Independent orbital tracking inspecting off-axis technical objects.
4. **Natural Blink Cycle** — 150 ms cosine upper eyelid rotational descent with zero normal inversion.
5. **Curious Expression** — Inquiring lateral head roll ($0.12$ rad), asymmetric brow raise ($0.85$).
6. **Surprised Expression** — Dynamic recoil attack, wide jaw drop, high arched brows.
7. **Explaining Gesture** — Rhythmic speech visemes and forward pencil pointing.
8. **Both-Arm Movement** — Notebook presentation gesture and conversational waving.
9. **Notebook Writing** — Pitch tilt down with drafting pencil micro-oscillations over notebook pages.
10. **Hero Resolution** — Smooth glide back to neutral camera distance and confident presenter stance.

---

## 3. Hybrid Rendering Architecture

SUPER.INTELLIGENCEEE utilizes a multi-engine rendering dispatcher selecting the optimal engine for each scene:

| Engine | Role | Technology Stack |
| :--- | :--- | :--- |
| **Remotion + Three.js** | 3D character animation, kinematics, camera framing, lighting | React 19, Remotion 4, Three.js 0.180, WebGL |
| **HyperFrames Engine** | Motion graphics, UI layouts, kinetic typography, overlays | HTML5, CSS3, GSAP, HyperFrames CLI |
| **Manim Community** | Precise mathematical visualisations, algorithmic proofs | Python 3.11, Manim Community 0.19, Cairo |
| **FFmpeg Pipeline** | Post-processing, stream muxing, subtitle burning, H.264/AAC | FFmpeg 9.0.1 (`libx264` / `aac` / `libass`) |

---

## 4. Audio & Narration Architecture

- **Primary Neural Voice:** Kokoro-82M high-fidelity neural voice model using `am_liam` (calm, authoritative, British/American hybrid documentary cadence).
- **Offline Secondary TTS:** Piper TTS (`en_US-lessac-medium.onnx`) for instant low-latency local rendering.
- **Operating System Fallback:** Windows SAPI (`pyttsx3`) zero-fail fallback.
- **Audio Engineering:** EBU R128 loudness normalization strictly normalized to **-16.0 LUFS** with -1.0 dBFS true-peak ceiling.
- **Multi-Track Sound Design:** Background ambient score with automated ducking during speech visemes.

---

## 5. Directory Structure

```
A:\SUPER.INTELLIGENCEEE\
├── app.py                      # Master FastAPI server & CLI dispatcher
├── config.yaml                 # Central pipeline configuration
├── requirements.txt            # Core Python dependencies
├── requirements-rendering.txt  # Rendering stack dependencies
├── START_SUPER_INTELLIGENCEEE.bat # Double-click Windows 11 launcher
├── character.me.png            # Canonical character identity reference
├── Character 3D.mp4            # Primary 3D host visual authority
│
├── core/                       # Governance, pipeline & orchestration
│   ├── orchestrator.py         # Multi-department autonomous coordinator
│   ├── unified_pipeline.py     # End-to-end documentary production line
│   ├── kill_switch.py          # Publishing kill switch & safety gates
│   ├── database.py             # SQLite WAL-mode schema & migration manager
│   ├── provenance.py           # Legal provenance & licensing classification
│   └── brand_os.py             # Brand creative guidelines and rule validator
│
├── rendering/                  # Multi-engine hybrid rendering subsystem
│   ├── engine_dispatcher.py    # Automatic scene-to-engine router
│   ├── smart_composition_engine.py # Hybrid composition assembler
│   ├── remotion/               # Remotion 3D project workspace
│   │   ├── src/
│   │   │   ├── components/Character3DScene.tsx # 3D Host Kinematics & WebGL scene
│   │   │   ├── compositions/Character3DValidationComposition.tsx # 540-frame sequence
│   │   │   └── assets/characterGlbBase64.ts   # Embedded GLB asset module
│   │   └── scripts/
│   │       ├── generate_super_character_v3.mjs # Procedural 3D GLB generator
│   │       └── generate_interactive_comparison_viewer.mjs
│   └── manim_engine/           # Mathematical & algorithmic scene generator
│
├── research/                   # Multi-source intelligence & intake
│   ├── multi_source_discovery.py # RSS, ArXiv, GitHub, Hacker News intake
│   ├── topic_scorer.py         # 5-factor scoring (relevance, freshness, depth)
│   └── fact_checking.py        # Independent claim auditor and source grounder
│
├── audio/                      # Speech synthesis & sound design
│   ├── narration/              # Kokoro-82M & Piper TTS providers
│   ├── audio_mixer.py          # FFmpeg mixer & -16.0 LUFS loudness normalizer
│   └── reference_sound_designer.py # Dynamic acoustic layer generator
│
├── dashboard/                  # Human-in-the-Loop review station
│   ├── routes.py               # FastAPI route controllers
│   └── templates/              # Production, scripts, review & queue interfaces
│
├── output/                     # Generated production outputs (git-ignored)
│   ├── experiment_a3/          # Experiment A.3 3D Character deliverables
│   ├── drafts/                 # Candidate videos awaiting human review
│   └── approved/               # Cleared videos ready for publishing
│
└── reports/                    # Engineering audit & QA documentation
    └── creative_reset/         # Experiment QA reports, specs & benchmark logs
```

---

## 6. Quick Start & Execution

### Option A: Launch Interactive 3D Character Viewer
Open `output/experiment_a3/character_viewer.html` directly in any modern browser for 360° orbit inspection, camera presets, and real-time morph target controls.

### Option B: Launch Web Dashboard
Double-click `START_SUPER_INTELLIGENCEEE.bat` or run:
```powershell
cd /d A:\SUPER.INTELLIGENCEEE
.\.venv\Scripts\activate
python app.py serve --host 127.0.0.1 --port 5000
```
Open your browser to: **`http://127.0.0.1:5000`**

### Option C: Run 3D Character Regeneration & Validation Render
```powershell
cd A:\SUPER.INTELLIGENCEEE\rendering\remotion

# 1. Regenerate procedural 3D GLB asset
node scripts/generate_super_character_v3.mjs

# 2. Render 10-step validation MP4 (540 frames @ 30 FPS)
npx remotion render Character3DValidation ..\..\output\experiment_a3\character_3d_validation.mp4
```

### Option D: Run Full Automated Test Suite
```powershell
cd /d A:\SUPER.INTELLIGENCEEE
.\.venv\Scripts\pytest.exe -v
```

---

## 7. Hardware & Performance Compliance

Engineered to operate on standard mobile workstations without cloud infrastructure:
- **Baseline Hardware:** Intel Core i5-1135G7 (4 cores / 8 threads), 8 GB RAM, Intel Iris Xe graphics, Windows 11.
- **Peak Memory Usage:** < 1.4 GB during full 1080×1920 3D WebGL render.
- **Rendering Throughput:** ~1.5s per frame with 4x concurrency in Remotion.
- **Zero Paid Subscriptions:** Zero external API fees for 3D modeling, speech generation, or video rendering.
- **Zero Blender Dependency:** 100% procedural Three.js geometry, materials, and GLTFExporter pipeline.
- **Publishing Governance:** Hard kill switch permanently armed; all external publishing requires human operator authorization.

---

## 8. License & Provenance

All procedural rigging code, character geometry generation, rendering dispatchers, and audio pipelines are proprietary to **SUPER.INTELLIGENCEEE**. Assets utilized are classified under strict legal provenance: CC0, MIT, or verified editorial fair-use documentation.
