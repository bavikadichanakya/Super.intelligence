# PHASE 6 — STAGE 4: ARCHITECTURE TRANSFORMATION & ENGINE SPECIFICATION
**Project:** SUPER.INTELLIGENCEEE  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Execution Context:** Phase 6 Autonomous Visual Learning & Video Production Transformation  
**Production Job:** Job #67 — `phase6_bitnet_1bit_llm` (BitNet b1.58 1-Bit LLM Architecture)  
**Standard:** 1080 × 1920 @ 30.0 fps Progressive, H.264 High Profile, EBU R128 Audio, Zero Card Containers, Platform Safe Margins (Bottom 360 px)  

---

## 1. VISUAL STORYTELLING TRANSFORMATION (BREAKING THE TEMPLATE LOOP)

In legacy phases (Phases 4.3 – 5.1), the system suffered from a recurring template failure mode:
- Standardized slide cards and bordered panels centered on screen.
- Small diagrams occupying less than 35% of canvas area.
- Lack of kinetic movement during conceptual explanations.
- Disconnected mouse cursor animations on mock UI.

In Phase 6, the architecture enforces **explanation-first visual storytelling**:
1. **Full-Bleed Visual Dominance:** The explanatory canvas occupies 100% of the 1080×1920 portrait space. Visual subjects float in an infinite depth-projected environment. Zero cards, zero slide containers, zero dashboard borders.
2. **Subject-Driven Mechanistic Metaphors:** Every visual component is mathematically or physically grounded in the breakthrough itself:
   - Floating 16-bit MAC equations sliced by laser strikes into glowing particles.
   - 2.5D memory wall data jams and wattage heatmaps.
   - Dynamic 10×10 tensor matrices flipping into discrete ternary pills $\{-1, 0, +1\}$.
   - Silicon logic multiplexers routing integer activations into adder trees.
   - 3D comparative benchmark columns illustrating a 71.4× energy cliff.
   - Real acquired terminal recordings of `bitnet.cpp` streaming tokens at 29+ tok/sec on CPU.
3. **Dual-Font Typography Hierarchy & Dynamic Reticles:**
   - Primary headlines: Arial Bold (52–60 pt) in pure white (`#FFFFFF`) with drop shadows.
   - Editorial keywords: Georgia Italic (34–38 pt) in electric cyan (`#00E5FF`) and amber (`#FFD43B`).
   - Dynamic UI Selection Reticles: Animated vector brackets snapping to units and metrics in exact cadence with spoken words.

---

## 2. SEVEN-SCENE MECHANISTIC BREAKDOWN (JOB #67)

| Scene | Identifier | Headline | Visual Mechanism | Camera & Motion Choreography | Safe Zone Conformance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scene 1** | `bitnet_hook` | MULTIPLY IS DEAD. | Floating FP16 MAC equation ($y_i = \sum W \times x$); laser beam slices $\times$ operator at $t=1.8\text{s}$, exploding into cyan particle sparks. | Slow push-in ($1.0\times \to 1.15\times$), radial shockwave expansion. | Subtitle $y \ge 1560$, clear of central equation at $y=900$. |
| **Scene 2** | `bitnet_memory` | THE MEMORY WALL | 2.5D HBM3 memory stack with amber packet congestion jammed in transit bus; 450W thermal wattage bar. | Lateral tracking pan along memory bus; pulsing warning glow. | Subtitle $y \ge 1560$, clear of central bus chasm. |
| **Scene 3** | `bitnet_ternary` | ALL WEIGHTS IN 1.58 BITS | 36-cell tensor matrix stagger-flipping from decimal floats into discrete pills: $+1$ (Cyan), $0$ (Slate), $-1$ (Violet). | Slow push-in; HUD reticle framing $\log_2(3) = 1.58\text{ bits}$ stat. | Subtitle $y \ge 1560$, clear of matrix at $y \in [680, 1130]$. |
| **Scene 4** | `bitnet_logic` | ZERO MULTIPLICATIONS | Silicon 3-way MUX routing input activation: $+1 \to \text{ADD}$, $-1 \to \text{SUB}$, $0 \to \text{SKIP}$. Pulse flows along branches. | Lateral pan following activation packets through adder tree. | Subtitle $y \ge 1560$, clear of logic tree at $y=960$. |
| **Scene 5** | `bitnet_benchmark` | 71.4X LESS ENERGY | 2.5D perspective bar chart: FP16 MAC (3.7 pJ, tall red) vs BitNet Add (0.1 pJ, cyan); counter counts to 71.4×. | 2.5D low-angle crane elevation rising with bar growth. | Subtitle $y \ge 1560$, clear of comparative bars. |
| **Scene 6** | `bitnet_terminal` | 100B MODELS ON CONSUMER CPU | Authentic terminal demo asset (`bitnet_terminal_execution_demo.png`) showing AVX-512 CLI running 70B model at 29.35 tok/sec. | Subtle continuous zoom; active green cursor blink and HUD border. | Subtitle $y \ge 1560$, terminal positioned at $y=880$. |
| **Scene 7** | `bitnet_outro` | THE DAWN OF 1-BIT COMPUTING | Pulsing concentric discrete logic rings; branding lockup (`SUPER.INTELLIGENCEEE`) and looping horizon rays. | Slow zoom-out revealing full circular core lockup. | Subtitle $y \ge 1560$, core centered at $y=960$. |

---

## 3. AUDIO & SPEECH ARCHITECTURE

- **Vocal Persona:** Kokoro-82M `am_liam` General American English locked.
- **Batch Processing:** Uses `KokoroDirectRunner.generate_batch()` to process all 7 scene scripts through memory in an isolated subprocess, preventing multiple 40-second ONNX reload delays.
- **Mastering Chain:** `pyloudnorm` dual-pass integrated loudness normalization to **-16.0 LUFS** (±0.5 LUFS) with a True Peak ceiling of **-1.0 dBTP**.
- **Audio Bed:** Procedural lo-fi electronic bed with subtle ducking under narration (-18 dB attenuation during vocal transients).

---

## 4. PLATFORM INTEGRITY & SAFE MARGINS

- **Output Dimensions:** Native 1080 × 1920 px (9:16 vertical video).
- **Temporal Rate:** 30.0 fps constant progressive.
- **Top Safe Region:** $y \in [120, 340]\text{ px}$ (Headlines & Subheaders).
- **Central Graphic Region:** $y \in [350, 1520]\text{ px}$ (Explanatory Visuals).
- **Bottom Safe Region:** $y \in [1560, 1920]\text{ px}$ (Kinetic Subtitles with 360 px bottom clearance).
