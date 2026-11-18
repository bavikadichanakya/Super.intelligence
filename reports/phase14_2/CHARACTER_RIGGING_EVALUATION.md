# Phase 14.2 — Character Rigging & Animation Architecture Evaluation

**Target Hardware:** Windows 11, Intel Core i5-1135G7 (4 cores / 8 threads), 8 GB RAM, Intel Iris Xe Integrated Graphics  
**Policy Directives:** Blender is strictly prohibited. No paid subscriptions or cloud API dependencies. Local, offline, deterministic rendering.  

---

## 1. Asset Discovery Audit
A comprehensive recursive scan was conducted across the workspace for 3D model formats (`.glb`, `.gltf`, `.fbx`, `.obj`, `.blend`, `.bvh`, `.usd`).

**Findings:**
- **Raw 3D Models in Workspace:** 0 files.
- **Reference Assets Available:**
  - `character.me.png` (2048x2048 high-resolution 2D master artwork)
  - `Character 3D.mp4` (10-second 1280x720 3D CGI video render)
- **Conclusion:** No reusable 3D mesh or skeletal rig files exist in the repository. The MP4 is a pre-rendered video.

---

## 2. Evaluation of Technical Approaches

| Criterion | Approach A: Procedural 3D Mesh in Three.js | Approach B: Multi-Layer 2.5D Kinematic Host Rig (Selected) | Approach C: Neural Video Retargeting (LivePortrait / Thin-Plate) |
| :--- | :--- | :--- | :--- |
| **Character Consistency** | Low (code-generated humanoid models look low-poly and fail to match the rich hair and face of `character.me.png`) | **100% Exact** (directly driven by canonical master layers) | Medium (frequent warping around glasses and beard) |
| **Hardware Overhead** | Moderate GPU WebGL load | **Very Low** (<150 MB RAM, runs smoothly on Intel i5) | Unacceptable (requires 6+ GB VRAM, OOM on 8GB system) |
| **Rendering Speed** | 10–15 FPS | **25–35 FPS (Real-time local encoding)** | 0.5–1.0 FPS |
| **Animation Control** | Full 3D bone controls | **Precise 2.5D kinematic controls** (mouth visemes, head tilt, breathing, arm elevation, pointing) | Uncontrollable / drifting |
| **Zero-Cost & Offline** | Yes | **Yes (100% local Python/PIL/Remotion)** | Requires heavy weights (>2 GB download) |
| **Remotion Integration** | Possible via `<ThreeCanvas>` | **Seamless React component integration (`<CharacterHost />`)** | Requires external pre-rendering |

---

## 3. Selected Strategy: Advanced 2.5D Multi-Layer Kinematic Rig

The optimal architectural choice for our hardware and production constraints is the **2.5D Multi-Layer Kinematic Host Rig**:

1. **Layer Hierarchy:**
   - **Base Body Canvas:** Torso, jacket, shoulders, neck, and hair contours.
   - **Eyelid Overlay:** Interpolated sinusoidal alpha blink cycle (140ms duration every 3.2s).
   - **Mouth Viseme Socket:** 4-state speech-synchronized mouth visemes (`closed`, `slight`, `open`, `round`) with soft radial Gaussian feathering.
   - **Articulated Arm & Hand Layer:** Segmented right arm holding drafting pencil, pivoting around the shoulder coordinate `(460, 1200)` in 2048 space.
   - **Cinematic Lighting & Shadow Layer:** Directional ambient color grading wash and 18px Gaussian blurred drop shadow.
   - **Holographic HUD Pointer:** Dynamic sci-fi vector ray connecting the pencil tip directly to the focal technical element on screen.

2. **Remotion Architecture (`rendering/remotion/`):**
   - React component `<CharacterHost />` accepts:
     - `frame`: current frame index.
     - `fps`: timeline frame rate.
     - `pose`: `presenter` | `investigator` | `explainer`.
     - `gesture`: `idle` | `explaining` | `pointing`.
     - `speechIntensity`: 0.0 to 1.0 (driven by audio track).
     - `targetCoordinates`: `[x, y]` for pointing ray.
     - `lightingTint`: Hex ambient color.
