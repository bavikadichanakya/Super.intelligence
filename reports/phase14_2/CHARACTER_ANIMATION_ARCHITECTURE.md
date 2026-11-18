# Phase 14.2 — Character Animation Architecture Specification

**Component:** Host Animation & Kinematics Subsystem  
**Module:** `rendering/character/` & `rendering/animated_character_host.py`  
**Remotion Integration:** `<CharacterHost />` (`rendering/remotion/src/components/CharacterHost.tsx`)  

---

## 1. Kinematic Control Hierarchy

The character animation system decouples high-level narrative intent from low-level frame synthesis:

```
                  ┌────────────────────────────────────┐
                  │    Narrative / Scene Controller    │
                  │ (Pose, Gesture Mode, Screen Anchor)│
                  └─────────────────┬──────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌───────────────────────┐                        ┌───────────────────────┐
│  Acoustic Speech Sync │                        │  Kinematic Transforms │
│ (Kokoro-82M am_liam)  │                        │ (Breathing, Sway, HUD)│
└──────────┬────────────┘                        └──────────┬────────────┘
           │                                                │
           ▼                                                ▼
┌───────────────────────┐                        ┌───────────────────────┐
│ 4-State Mouth Visemes │                        │ Shoulder Pivot & Arm  │
│(closed,slight,open,rd)│                        │   Angle (-16° pointing│
└──────────┬────────────┘                        └──────────┬────────────┘
           │                                                │
           └────────────────────────┬───────────────────────┘
                                    ▼
                  ┌────────────────────────────────────┐
                  │     Multi-Layer 2.5D Compositor    │
                  │   (Drop Shadow, Ambient Wash, HUD) │
                  └─────────────────┬──────────────────┘
                                    ▼
                  ┌────────────────────────────────────┐
                  │    1080x1920 Cinematic Canvas      │
                  └────────────────────────────────────┘
```

---

## 2. Speech Viseme State Machine

Speech lip-sync is driven directly by audio timing and syllable cadence:

- **Cadence Frequency:** 4.8 Hz (average English speech phoneme transition rate).
- **Phonetic State Transition Table:**
  - `0.00 <= cycle < 0.15`: `mouth_slight` (onset of plosives / consonants / bilabials: M, B, P, T, S).
  - `0.15 <= cycle < 0.60`: `mouth_open` / `mouth_round` (peak vowel opening: A, E, I, O, U).
  - `0.60 <= cycle < 0.85`: `mouth_slight` (vowel offset and transition).
  - `0.85 <= cycle < 1.00`: `mouth_closed` (inter-syllable boundary).
- **Resting Gate:** When narration ends or pauses occur (>200ms inter-phrase gap), mouth smoothly clamps to `mouth_closed` (canonical smile).

---

## 3. Gestural Kinematics

1. **`presenter_direct` (Explaining Cadence):**
   - Natural sinusoidal elevation of right arm & drafting pencil:
     $$\Delta y = -14.0 \times (0.5 + 0.5 \sin(2\pi \cdot 0.9 \cdot t)) \text{ px}$$
     $$\theta_{\text{arm}} = -5.0 \times (0.5 + 0.5 \sin(2\pi \cdot 0.9 \cdot t))^{\circ}$$
   - Emphasizes spoken syllables without erratic twitching.

2. **`investigator_examining` / `pointing`:**
   - Shoulder pivot anchor at $(460, 1200)$ in 2048 space.
   - Smooth cubic ease-in to pointing attitude:
     $$\text{ease}(t) = 1.0 - (1.0 - \text{clamp}(t / 0.40, 0, 1))^3$$
     $$\theta_{\text{arm}} = -16.0^{\circ} \times \text{ease}(t) + 1.2^{\circ} \sin(2\pi \cdot 0.8 \cdot t)$$
     $$\Delta y_{\text{arm}} = -35.0 \times \text{ease}(t) \text{ px}$$
   - Holographic vector beam generated from pencil tip coordinates directly to the target UI/hardware coordinate $(t_x, t_y)$.

---

## 4. Subtitle Safe Area Collision Guarantees
- Subtitle Safe Zone: $y \in [1640, 1820]$, $x \in [90, 990]$.
- Standard host bottom anchor: $y_{\text{bottom}} = 1560\text{px}$ (at scale 0.70) or $1580\text{px}$ (at scale 0.58).
- Mathematical clearance: Minimum $60\text{px}$ to $80\text{px}$ buffer above subtitle safe zone. Zero occlusion guaranteed.
