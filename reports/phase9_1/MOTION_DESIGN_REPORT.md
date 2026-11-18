# PHASE 9.1 — MOTION DESIGN & CAMERA CHOREOGRAPHY REPORT
**Document ID:** `reports/phase9_1/MOTION_DESIGN_REPORT.md`  
**Date:** November 16, 2026  
**Auditor:** Autonomous Visual Storytelling & Documentary Systems Architect  

---

## 1. MOTION DESIGN OBJECTIVE & PHILOSOPHY

The visual failure of Phase 9 was static presentation: objects were drawn nicely, but the camera remained effectively stationary, treating each scene like an animated PowerPoint slide.

In Phase 9.1, motion is not decorative; **motion is the primary explanatory tool**.
Every camera dive, pan, scale transition, and visual emphasis exists solely to direct cognitive attention to the underlying physical mechanism.

---

## 2. NARRATIVE CAMERA ARCS PER PROTOTYPE

### 2.1 Prototype A: Physical Technology (Dilution Refrigerator)
- **5-Stage Camera Sequence:**
  1. **$t \in [0.0\text{s}, 2.2\text{s}]$ (Establishing Wide View):** Camera at $(540, 780, 1.0\times)$. The entire physical chandelier fills 70% of canvas width ($W = 760\text{px}$). Top vacuum collar, titanium struts, 4 gold plates, and central cold column establish the monumental physical scale.
  2. **$t \in [2.2\text{s}, 4.4\text{s}]$ (Upper Thermal Stage Focus):** Camera pushes smoothly into $(520, 600, 1.40\times)$. An elbow leader annotation pops up on the right: `"50K THERMAL FLANGE // First-stage heat rejection"`.
  3. **$t \in [4.4\text{s}, 6.4\text{s}]$ (Coaxial Wire Loom Macro):** Camera zooms deep into the wire harness at $(500, 720, 1.65\times)$, revealing the individual silver NbTi coaxial cables and gold attenuators on the central column. Leader annotation: `"COAXIAL RF LOOM // NbTi superconducting wiring"`.
  4. **$t \in [6.4\text{s}, 7.8\text{s}]$ (Descent to Mixing Flange):** Camera cranes down to $(540, 940, 1.50\times)$, framing the gilded 15mK mixing plate and flanking RF amplifier cans.
  5. **$t \in [7.8\text{s}, 9.0\text{s}]$ (Protected Processor Revelation):** Extreme macro push into $(540, 1100, 1.90\times)$, revealing the cold finger tip and glowing Willow silicon processor package resting at 10 mK. Leader annotation: `"PROTECTED WILLOW DIE // 10 mK Base Environment"`.

### 2.2 Prototype B: Abstract Concept (Surface Code Lattice)
- **Macro Dive & Attentional Spotlight:**
  1. **$t \in [0.0\text{s}, 2.6\text{s}]$ (Lattice Overview):** Camera at $(540, 820, 1.0\times)$. Silicon substrate fills the width ($900\text{px}$). 4x4 array of data qubits and syndrome ancillas in calm coherence.
  2. **$t \in [2.6\text{s}, 5.0\text{s}]$ (The Decoherence Event & Macro Dive):** A physical data qubit at $(1, 1)$ flips. The camera executes a dynamic cubic-bezier dive ($1.0\times \to 2.05\times$), centering directly on the affected plaquette. **Attentional Spotlight:** Surrounding non-error nodes dim to 35% opacity, eliminating all competing visual clutter. The failing qubit pulses with crimson shockwaves. Leader annotation: `"PHASE-FLIP ERROR // Parity inverted at Node (1,1)"`.
  3. **$t \in [5.0\text{s}, 6.8\text{s}]$ (Topological Stabilizer Healing):** Translucent diamond parity wave sweeps outward. The syndrome ancilla lights up in golden amber and fires a focused cyan laser stabilizer beam directly into the failing qubit.
  4. **$t \in [6.8\text{s}, 8.5\text{s}]$ (Coherence Restoration):** Error node flips back to calm cyan, releasing an expanding ring of coherent particles. Camera pulls back smoothly to $(540, 820, 1.10\times)$, showing the entire lattice restored. Leader annotation: `"STABILIZER RESTORED // Cycle complete in 840 ns"`.

### 2.3 Prototype C: Real-World Documentary (Sequential Three-Act Arc)
- **Elimination of Simultaneous Clutter:**
  1. **Act 1 ($t \in [0.0\text{s}, 3.2\text{s}]$): Nature Manuscript Reveal.** Large, pristine journal presentation ($W = 936\text{px}, H = 680\text{px}$) slides in with smooth spring deceleration. Focus is 100% on peer-reviewed authority.
  2. **Act 2 ($t \in [3.2\text{s}, 6.8\text{s}]$): Dedicated Scaling Plot.** Act 1 gracefully transitions into a large, uncompromised blueprint graph ($W = 936\text{px}, H = 760\text{px}$). Curve draws progressively with a glowing cyan particle head from $d=3 \to d=5 \to d=7$, plummeting exponentially below the red threshold line ($\Lambda = 1.0$). Callout: `"LAMBDA = 2.14 // Exponential error suppression"`.
  3. **Act 3 ($t \in [6.8\text{s}, 9.5\text{s}]$): Cinematic Supremacy Contrast.** Full-canvas split comparison: Frontier Supercomputer ($10^{25}\text{ years}$) vs Google Willow ($< 5\text{ minutes}$), with accelerating digital progress bar resolving to completion.

---

## 3. MOTION CURVES & EASING MATHEMATICS

All spatial interpolations utilize **Cubic Bezier and Spring Easing Functions**:
$$S(u) = 3 u^2 - 2 u^3, \quad u \in [0, 1]$$
Overlaying continuous linear micro-drift:
$$Z(t) = Z_{key}(t) \cdot (1.0 + 0.015 \cdot t)$$
This guarantees that the human eye never perceives a paused or dead slide, while avoiding jerky or nauseating camera accelerations.
