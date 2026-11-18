# SUPER.INTELLIGENCEEE — Phase 4.2A.1 Storyboard Revision & Shot Architecture
**Document ID:** SEC-P42A1-SBR-20261107  
**Document Type:** Directed Shot List & Storyboard Blueprint  
**Topic:** Unpacking the Compute Efficiency of Strong-to-Weak OPD against GRPO (arXiv:2611.08453)  
**Aspect Ratio:** 9:16 Vertical Portrait (1080 × 1920)  

---

## 1. Sequence Overview & Narrative Arc

The revised storyboard structures the documentary around three distinct cinematic shots:

```
┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│           SEQUENCE A            │           SEQUENCE B            │           SEQUENCE C            │
│  "THE EXPLORATION CEILING"      │  "ANATOMY OF TOKEN SUPERVISION" │  "THE EFFICIENCY HORIZON"       │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ Role: The Compute Friction      │ Role: The Mechanistic Solution  │ Role: The Authoritative Verdict │
│ Style: Atmospheric Datacenter   │ Style: Swiss Technical Studio   │ Style: Monumental Horizon       │
│ Camera: Push-In Slow (1.04x)    │ Camera: Dynamic Token Reveal    │ Camera: Pull-Back Steady        │
│ Runtime: 10.5 seconds           │ Runtime: 14.0 seconds           │ Runtime: 15.0 seconds           │
└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

---

## 2. Sequence A: Cinematic Documentary — The Exploration Compute Ceiling

- **Target Duration:** 10.5 seconds.
- **Narration:**  
  *"Training reasoning models with reinforcement learning hits a massive compute ceiling. Group Relative Policy Optimization delivers frontier accuracy, but the exploration FLOPs are staggering."*
- **Composition Style:** Atmospheric Datacenter & Silicon Accelerator Substrate.

### Shot Architecture:
- **Shot A.1: The Datacenter Horizon (0.0s – 4.5s)**
  - *Visual Description:* A dark graphite datacenter server bay (`#0B0F17`) receding into atmospheric perspective. Vertical rack bays on either side pulse with subtle cyan and amber telemetry LED activity. An anamorphic blue lens sweep passes gently across the frame.
  - *Camera Movement:* Steady push-in forward (`push_in_slow`, scale $1.00 \rightarrow 1.04$).
  - *Sound Design:* Deep sub-bass analog drone bed ($-24\text{ dB}$) with soft electronic hum.
- **Shot A.2: Silicon Core Saturation & Editorial Lower-Third (4.5s – 10.5s)**
  - *Visual Description:* Camera settles into macro focus on a monolithic compute accelerator substrate. Copper/gold bus traces frame tensor clusters; the central exploration cores glow in warm amber (`#D97706`), communicating saturated memory bandwidth.
  - *Typography Overlay (Y = 1220 to 1640):*
    - Header: `"// SUPER.INTELLIGENCEEE | FIELD INVESTIGATION"`
    - Headline: `"The Exploration Compute Ceiling"` (White, $68\text{ px}$)
    - Deck: `"Group Relative Policy Optimization delivers frontier reasoning, but searching solution spaces requires thousands of rollouts per checkpoint."`
    - Telemetry Anchor: `"ARXIV:2611.08453 // REASONING COMPUTE BARRIER"`
  - *Transition:* Smooth directional wipe-left (`0.35s`) as we cut to the algorithmic mechanism.

---

## 3. Sequence B: Technical Mechanism — On-Policy Distillation Dynamics

- **Target Duration:** 14.0 seconds.
- **Narration:**  
  *"A new academic preprint evaluates On-Policy Distillation as an alternative. By supervising student rollouts with a frozen teacher, it sidesteps RL search. Crucially, the authors report that efficiency hinges entirely on teacher selection."*
- **Composition Style:** Swiss Technical Studio on Warm Ivory Canvas (`#FAF7F2`).

### Shot Architecture:
- **Shot B.1: The Token Trajectory (0.0s – 5.0s)**
  - *Visual Description:* Prompt tokens enter at the top (`[Prompt] Factor x⁴ - 16 =`). Below, the student model generates candidate reasoning tokens step-by-step: `( x² - 4 ) ( x² + 4 )`.
  - *Camera Movement:* Slight pan following active token generation.
  - *Visual Cue:* The active token $y_t$ pulses in Technical Blue (`#0284C7`), showing on-policy sampling.
- **Shot B.2: The Logit Probability Spectrum (5.0s – 9.0s)**
  - *Visual Description:* Directly above the generated tokens, the frozen teacher's probability distribution rises as vertical target density stems (grey). The student's active logits (blue) are pulled toward the teacher via directional KL divergence gradient vectors: $D_{\text{KL}}(\pi_\theta \,||\, \pi_{\text{ref}})$.
  - *Sound Design:* Delicate mechanical UI clicks synchronized to token appearances.
- **Shot B.3: The Empirical Fork (9.0s – 14.0s)**
  - *Visual Description:* The mechanism cleanly branches into two comparative outcomes:
    1. *Emerald Branch:* **Self-Teacher (Own Checkpoint)**  
       $\rightarrow$ Trajectory overlap $> 94\%$. **50× Distillation FLOP Reduction** (matches checkpoint math accuracy with 50x fewer distillation FLOPs).
    2. *Coral Branch:* **External Post-Trained Teacher**  
       $\rightarrow$ Distribution divergence. **Loses to Direct GRPO** in accuracy per training FLOP.
  - *Transition:* Cross-dissolve (`0.40s`) into the concluding synthesis.

---

## 4. Sequence C: Editorial Conclusion — The Efficiency Horizon

- **Target Duration:** 15.0 seconds.
- **Narration:**  
  *"The takeaway is decisive: on-policy distillation is not a universal acceleration law. While self-teacher consolidation saves compute, external distillation fails to beat RL. As a preprint, real-world deployment requires independent replication."*
- **Composition Style:** Monumental Efficiency Horizon & Balanced Synthesis.

### Shot Architecture:
- **Shot C.1: The Efficiency Horizon Coordinate Plane (0.0s – 7.5s)**
  - *Visual Description:* A single monumental coordinate system on warm ivory canvas. The vertical axis represents **Accuracy per Training FLOP**; the horizontal axis represents **Distillation Compute Budget**. A charcoal curve traces the GRPO Pareto frontier.
  - *Data Point A:* An emerald diamond locks in high above the frontier: `"SELF-CHECKPOINT TEACHER // 50× FEWER FLOPs"`.
  - *Data Point B:* An amber triangle drops into place below the frontier: `"EXTERNAL TEACHER // SUB-GRPO FLOP EFFICIENCY"`.
  - *Camera Movement:* Slow, steady camera pull-back ($0.5\%\text{ per second}$), expanding spatial gravity.
- **Shot C.2: Qualified Directives & Preprint Disclosure (7.5s – 15.0s)**
  - *Visual Description:* Below the horizon, two restrained takeaway cards define the engineering boundaries:
    1. *The 50× Scope:* Strictly applies to self-checkpoint distillation on math benchmarks.
    2. *The External Ceiling:* External distillation generally underperforms direct GRPO under matched settings.
  - *Academic Seal:* An official preprint governance box anchors the base:
    `"ACADEMIC PREPRINT DISCLOSURE // ARXIV:2611.08453 // REPLICATION MANDATE"`
  - *Sound Design:* Ambient drone settles into a clean, resonant conclusion tone.

---

## 5. Storyboard Validation Summary

The revised storyboard completely eliminates generic slides. It provides a cohesive, multi-layered visual journey from physical compute friction, through algorithmic token mechanics, to an authoritative, mathematically qualified conclusion.
