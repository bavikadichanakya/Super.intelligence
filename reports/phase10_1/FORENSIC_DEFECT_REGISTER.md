# PHASE 10.1 — FORENSIC TYPOGRAPHY, SUBTITLE & COMPOSITION DEFECT REGISTER
## Comprehensive Frame-by-Frame Audit of Phase 10 Flagship Documentary

**Document:** Forensic Defect Register  
**Audit Date:** 2026-11-16  
**Reference Video:** `output/drafts/phase10_flagship/phase10_flagship_documentary.mp4`  
**Canvas Resolution:** 1080 × 1920 (9:16 Portrait)  
**Target Delivery:** `output/drafts/phase10_1_layout_repair/`  
**Theme Mandate:** **Unified Light Theme** across all scenes with harmonious scientific color principles  

---

## 1. Executive Summary of Audit Findings

The Phase 10 flagship documentary demonstrated major progress in technical content, voice synchronization, and 64-second runtime. However, a forensic frame-by-frame inspection revealed systemic layout defects:
1. **Critical Subtitle Clipping Across All 7 Scenes:** The subtitle engine lacked automatic line wrapping. Any subtitle phrase exceeding ~50 characters exceeded the 1080px canvas width (e.g. `1250px` width at 42pt), causing the horizontal center formula `(1080 - width) // 2` to evaluate to negative values (`-85px`). Consequently, the opening and closing words of every long sentence were severely clipped off the screen edges.
2. **Inconsistent Container Padding & Edge Crowding:** Several cards and HUD elements extended too close to the canvas boundary, violating mobile safe areas (90px left/right margins).
3. **Hardware & Annotation Proximity:** In Scene 1 and Scene 2, annotations lacked dynamic leader lines that maintained fixed offsets during camera moves.
4. **Theme Harmonization (User Mandate):** The user explicitly mandated a **Light Theme in the background** with all elements in sync, maintaining scientific color principles and colors that look good together.

---

## 2. Complete Forensic Defect Register

| Scene ID | Timestamp | Element | Defect Description | Root Cause | Correction | Verification Method |
|:---|:---:|:---|:---|:---|:---|:---:|
| **Scene 1** | `00:00.80` | Subtitle | The words `"Ever w..."` and `"...puters"` are truncated at screen edges | Subtitle rendered on a single line (`width=1240px > 1080px`); no line wrapping | Implement intelligent 2-line wrapping with max width 900px | Check left-most glyph `E` (x >= 90) and right-most `?` (x <= 990) |
| **Scene 1** | `00:03.50` | Hardware Annotation | `STAGE 05: MIXING CHAMBER` callout leader line drifts during zoom | Fixed screen-space offset instead of affine world-space projection | Bind leader start coordinate to QPU plate anchor in world coordinates | Verify leader line tracks plate precisely across all frames |
| **Scene 1** | `00:00.00` | Background Theme | Deep cryo void (`#080C14`) dark theme conflicts with user mandate | Dark theme used in Phase 10; user requested cohesive light theme | Implement Unified Scientific Light Theme: Architectural Pearl `#F8F9FA` | Verify all 7 scenes share unified light theme and WCAG AAA contrast |
| **Scene 2** | `00:08.50` | Subtitle | Subtitle line 1 is clipped on both margins | Sentence has 59 chars; renders as 1180px line | Wrap into 2 balanced lines: line 1 (32 chars), line 2 (27 chars) | Verify bounding box width <= 900px |
| **Scene 2** | `00:10.00` | Thermometer Scale | `300 K` label crowded against top edge of thermometer card | Card top margin was only 20px; tick mark text had 10px offset | Expand thermometer card height to 1020px; anchor labels with 32px padding | Verify minimum 24px vertical clearance above `300 K` |
| **Scene 2** | `00:13.00` | Telemetry Pill | `T = 0.010 K` pill overlaps bottom thermal vibration field | Central mixing chamber circle diameter too large for 1080x1920 layout | Scale down mixing chamber circle to radius 200px; separate telemetry card | Check vertical gap >= 36px between circle and pill |
| **Scene 3** | `00:19.50` | Subtitle | `"Suspended at the bottom of the cryostat..."` clipped on both sides | 70-character sentence rendered on 1 line (1380px wide) | Wrap at natural pause: `"Suspended at the bottom of the cryostat"` / `"sits Google's Willow processor"` | Verify bounding box within safe area |
| **Scene 3** | `00:22.00` | Qubit Grid | 105 transmon dots too small on mobile screen | 11x10 grid with 42px pitch was too dense for mobile portrait view | Increase transmon capacitor radius to 18px with gold wirebond accents | Verify visibility on mobile 360x640 simulated viewport |
| **Scene 4** | `00:28.00` | Subtitle | `"adjacent syndrome ancillas detect the disturbance,"` cut off | Single-line text exceeding safe width | Break into 2 lines at syntactic boundary | Check both lines inside 900px container |
| **Scene 4** | `00:30.50` | Error Badge | `BIT-FLIP DETECTED` card crowds adjacent column waveguide | Badge placed at fixed `pt_err[0] + 34` without boundary clamp | Clamp badge X coordinate within lattice safe region | Verify clearance >= 20px from lattice perimeter |
| **Scene 5** | `00:39.00` | Subtitle | `"expanding the surface code from distance three..."` clipped | Single-line rendering of 62-char sentence | Wrap into 2 balanced lines | Safe margins >= 90px verified |
| **Scene 5** | `00:41.00` | Nature Masthead | `nature` logo and citation text too close to top border | Card padding was 36px; red logo crowded against border | Increase top padding to 48px; increase subtitle font to 32pt | Verify 32px breathing room above and below masthead line |
| **Scene 5** | `00:43.50` | Graph Y-Axis | Logarithmic tick labels (`10^-2`, `10^-3`) close to card left border | Axis left margin was only 140px inside card | Set axis origin to `x0 + 170px`; pad Y labels with 80px space | Minimum 40px margin between Y labels and card border |
| **Scene 6** | `00:49.00` | Subtitle | `"in under five minutes that would take Frontier,"` clipped | Single-line rendering | Wrap into 2 balanced lines | Safe margins >= 90px verified |
| **Scene 6** | `00:52.00` | Comparison Columns | `CLASSICAL BENCHMARK` column text crowded on mobile | Text sizes (36pt, 32pt) lacked relative line-height leading | Rebuild two-column card with 440px column width and 24px line-heights | Verify zero text overlap between columns |
| **Scene 7** | `00:58.00` | Subtitle | `"faster than they accumulate, we have officially crossed"` clipped | Single-line rendering | Wrap into 2 balanced lines | Safe margins >= 90px verified |
| **Scene 7** | `01:00.50` | Node Labels | `NODE 01`, `10 mK // OK` labels too small (20pt) for mobile view | Small font size on 3-node rack array | Increase node labels to 26pt bold with high-contrast emerald badge | Check readability at mobile screen scale |

---

## 3. Root Cause Analysis: The Core Defect Mechanism

The defects documented above all stem from **three systemic architecture gaps**:
1. **Lack of Text Wrapping & Layout Container Model:** The previous code called `draw.text((x, y), string)` directly without measuring whether `string` fits within the usable canvas width.
2. **Absence of a Unified Typography Hierarchy:** Font sizes were chosen ad-hoc per scene (`36pt`, `40pt`, `44pt`, `26pt`, `24pt`), creating visual inconsistency.
3. **Hardcoded Subtitle Coordinate:** Subtitles were placed at a fixed single Y-coordinate with zero multi-line capacity.

Phase 10.1 resolves every one of these issues by introducing:
1. `rendering/text_layout_engine.py`: A formal text container system with real font metrics, word-boundary wrapping, and overflow prevention.
2. `rendering/advanced_subtitle_engine.py`: A mobile-safe, 2-line intelligent subtitle engine with 100% transparent backing and Kokoro audio synchronization.
3. Unified Scientific Light Theme: Architectural Pearl `#F8F9FA`, Pure White drafting cards `#FFFFFF`, Deep Obsidian typography `#0F172A`, rich OFHC Gold `#D97706`, 316L Stainless Steel `#475569`, Technical Green `#059669`, and Electric Sapphire `#0284C7`.
