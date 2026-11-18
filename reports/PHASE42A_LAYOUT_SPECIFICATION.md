# SUPER.INTELLIGENCEEE — Phase 4.2A Layout & Typography Specification
**Document ID:** SEC-P42A-LAY-20261107  
**Specification Level:** Studio Standard / Release-Blocking  
**Target Canvas:** 1080 × 1920 (9:16 Vertical Social Video)  

---

## 1. Canvas Architecture & Safe-Zone Geometry

Every frame rendered for SUPER.INTELLIGENCEEE must conform to strict safe-zone boundaries designed to prevent collisions with mobile platform interface overlays (TikTok, Instagram Reels, YouTube Shorts).

```
   0 px ┌─────────────────────────────────────────────────────────┐
        │                 TOP UNSAFE ZONE (140 px)                │
        │       (Platform status bar, search icons, account UI)    │
 140 px ├─────────────────────────────────────────────────────────┤
        │ 80 px │                                         │ 80 px │
        │ LATERAL│                                         │LATERAL│
        │ MARGIN│         ACTIVE EDITORIAL CONTENT        │ MARGIN│
        │       │                 ZONE                    │       │
        │       │                                         │ (Right│
        │       │          Width: 920 px                  │  side │
        │       │          Height: 1520 px                │  like/│
        │       │          X: 80 px to 1000 px            │ share │
        │       │          Y: 140 px to 1660 px           │icons) │
        │       │                                         │       │
1660 px ├─────────────────────────────────────────────────────────┤
        │               BOTTOM UNSAFE ZONE (260 px)               │
        │  (Platform captions, scrubber bar, audio disc, CTAs)    │
1920 px └─────────────────────────────────────────────────────────┘
        0 px                                                    1080 px
```

### Safe-Zone Rules
1. **Top Safe Margin ($0\text{ to }140\text{ px}$):** No critical text, logos, or primary data graphics. Only subtle background textures, ambient hairlines, or canvas tint may extend into this region.
2. **Bottom Safe Margin ($1660\text{ to }1920\text{ px}$):** Strictly reserved for burned captions and mobile platform interaction elements. No primary typography or chart baselines may fall below $Y = 1660\text{ px}$.
3. **Lateral Margins ($0\text{ to }80\text{ px}$ and $1000\text{ to }1080\text{ px}$):** Content must stay within $X \in [80, 1000]\text{ px}$ (width $920\text{ px}$) to avoid collision with right-side action buttons (likes, comments, bookmarks, share icons).

---

## 2. Layout Composition Families

To eliminate the repetitive "3-box template" syndrome diagnosed in the forensic audit, the layout engine introduces five distinct composition families:

### Family 1: Macro Cinematography & Architectural Focus
- **Visual Subject:** Full-bleed or framed hardware/die substrate occupying the central viewport ($Y = 280\text{ to }1180\text{ px}$).
- **Typography Structure:** High-clarity editorial lower-third ($Y = 1240\text{ to }1620\text{ px}$) featuring an open hairline divider, primary headline, two-line deck, and metadata attribution badge.
- **Usage:** Opening contextual hooks, hardware scale, data-center infrastructure.

### Family 2: Technical Vector Diagram & Mechanism
- **Visual Subject:** Multi-node schematic flow with directional particle tracks, signal buses, and mathematical operator gates ($Y = 320\text{ to }1220\text{ px}$).
- **Typography Structure:** Top technical badge ($Y = 160\text{ px}$), clean section headline ($Y = 220\text{ px}$), with inline node labels dynamically positioned relative to diagram elements.
- **Usage:** Explaining algorithmic workflows (e.g. GRPO rollout vs. teacher logit supervision).

### Family 3: Comparative Data Ablation
- **Visual Subject:** Side-by-side or stacked comparative metric cards ($Y = 340\text{ to }1260\text{ px}$) contrasting baseline vs. breakthrough or self-teacher vs. external teacher.
- **Typography Structure:** Clear metric values typeset in monospace bold ($110\text{--}130\text{ px}$), unit subtitles, and a bottom empirical qualification card.
- **Usage:** Head-to-head performance evaluations, FLOP scaling curves, ablation studies.

### Family 4: Editorial Kinetic Typography
- **Visual Subject:** Bold, staggered word-by-word display typography dominating the upper-to-middle canvas ($Y = 260\text{ to }880\text{ px}$) over warm ivory canvas with active scanning rules.
- **Typography Structure:** Giant hero word ($88\text{ px}$), explanatory thesis deck ($36\text{ px}$), and anchored academic citation footer ($Y = 1580\text{ px}$).
- **Usage:** Narrative turning points, key questions, dramatic thesis statements.

### Family 5: Executive Verdict Balance Sheet
- **Visual Subject:** A multi-tier structured decision plate ($Y = 280\text{ to }1620\text{ px}$) organizing key findings, deployment constraints, and preprint boundaries.
- **Typography Structure:** High-contrast verdict seal, 3 distinct takeaway cards with colored indicator pills (Emerald, Blue, Amber), and formal DOI provenance footer.
- **Usage:** Concluding synthesis and actionable engineering takeaways.

---

## 3. Responsive Text Measurement & Wrapping Engine

Text clipping and truncation are treated as release-blocking defects. All typography must be rendered through the following automated layout pipeline:

```
[Raw String] ──► [Normalize & Tokenize]
                        │
                        ▼
            [Calculate Font Bounding Box (textbbox)]
                        │
                        ▼
            [Does Width Exceed max_width (920 px)?]
                 ├─► YES: Word-wrap into line array
                 └─► NO:  Single line
                        │
                        ▼
            [Does Total Height Exceed Container Limit?]
                 ├─► YES: Reduce font size iteratively (step: -2px)
                 │        until text fits within bounds
                 └─► NO:  Proceed to render
                        │
                        ▼
            [Safe-Area Collision Check] ──► Render to Canvas
```

### Algorithmic Requirements
1. **Dynamic Font Scaling:** If a headline exceeds its allocated vertical container height at nominal size ($72\text{ px}$), the engine decreases font size in $2\text{ px}$ increments down to a minimum floor ($48\text{ px}$). If it still overflows, an exception is raised during QA.
2. **Explicit Line Spacing:** Line height is calculated dynamically as $\text{line\_height} = \text{font\_size} \times 1.25$ to preserve visual breathing room.
3. **Contrast Assurance:** For every rendered string, the contrast ratio between foreground and background is evaluated:
   $$\text{Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05}$$
   Where $L$ is the WCAG 2.1 relative luminance. Text is rejected if $\text{Ratio} < 7.0:1$.

---

## 4. Acceptance Criteria for Rendered Frames

Every rendered frame must pass the following automated acceptance gates:
- **Rule 1 (Zero Clipping):** No text glyph or bounding box intersects with canvas edges ($X < 80$, $X > 1000$, $Y < 140$, $Y > 1660$).
- **Rule 2 (Zero Truncation):** No string may contain ellipses (`...`) or slice cuts resulting from programmatic string slicing.
- **Rule 3 (Zero Overlap):** No text element may collide with another text element or visual diagram node (minimum $24\text{ px}$ margin).
- **Rule 4 (Readability Floor):** Body text must never scale below $28\text{ px}$; citations below $22\text{ px}$.
- **Rule 5 (Light-Theme Balance):** Mean background luminance across the active content zone must remain $> 0.80$ (Warm Ivory `#FAF7F2` standard).

