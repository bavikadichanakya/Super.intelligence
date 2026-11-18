# SUBTITLE & TYPOGRAPHY SPECIFICATION V2
## SUPER.INTELLIGENCEEE — Phase 9.2 Flagship Production Standards

**Project:** SUPER.INTELLIGENCEEE  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Documentary:** *Google Willow: Real-Time Quantum Error Correction Below Threshold*  
**Date:** November 2026  
**Standards Owner:** Lead Motion Designer & Typography Specialist  

---

## 1. EXECUTIVE SUMMARY & TYPOGRAPHY MANDATE

Subtitles and on-screen typography are not passive text overlays—in technical documentary filmmaking, they establish narrative authority, guide cognitive focus, and clarify intricate scientific principles.

In previous phases, typography suffered from three major flaws:
1. **The Opaque Box Barrier:** Subtitles were enclosed in solid or semi-opaque black rounded rectangles that occluded lower diagram details and looked like cheap video player captioning.
2. **Kinetic Over-Excitement:** Rapid single-word bouncing, pulsing, or hyperactive rainbow text created visual fatigue and clashed with serious technical communication.
3. **Contrast Failure on Diverse Backgrounds:** Subtitles designed for pure black voids became unreadable when transitions introduced light studio backgrounds.

Phase 9.2 establishes a comprehensive Subtitle Architecture V2 and Typography Hierarchy that guarantees 100% legibility across both dark obsidian voids and warm architectural stone canvases.

---

## 2. THE THREE SUBTITLE DIRECTIONS EVALUATED

To resolve the subtitle dilemma scientifically, three distinct subtitle directions were prototyped and evaluated against actual rendered footage of Google Willow:

```
+--------------------------------------------------------------------------------------------------+
| STYLE A: CLEAN EDITORIAL PHRASE-GROUP (WINNER)                                                    |
| "Willow is suspended inside a [dilution refrigerator]."                                          |
| - Architecture: Natural 4-7 word phrase groups matching human speech pauses.                     |
| - Background: Zero hard box. Seamless radial luminance vignette (alpha 110 -> 0) spanning Y=1380-|
|   1540px, ensuring high-contrast legibility across both light and dark footage.                   |
| - Active Word: Luminous warm gold (#FCD34D / #D4AF37) with subtle 1.05x optical emphasis.       |
| - Inactive Words: Crisp off-white (#F8FAFC) on dark void / deep slate (#0F172A) on warm stone.   |
+--------------------------------------------------------------------------------------------------+
| STYLE B: RESTRAINED KINETIC WORD EMPHASIS                                                        |
| "Willow is suspended inside a [dilution refrigerator]."                                          |
| - Architecture: Compact frosted glass capsule (#0F172A at 65% opacity, 1px border #38BDF8).     |
| - Active Word: Electric cyan (#38BDF8) with a 2px horizontal underline tracking the active token.|
| - Assessment: High tech appeal, but the horizontal bounding capsule creates visual occlusion.    |
+--------------------------------------------------------------------------------------------------+
| STYLE C: MINIMAL DOCUMENTARY CAPTIONS                                                            |
| "Willow is suspended inside a [dilution refrigerator]."                                          |
| - Architecture: Traditional broadcast documentary styling; ultra-clean sans-serif.               |
| - Active Word: Soft emerald mint (#34D399) with no geometric ornamentation.                      |
| - Assessment: Highly understated, but lacks sufficient contrast over complex wireframes.         |
+--------------------------------------------------------------------------------------------------+
```

### The Winning Style: Style A (Clean Editorial Phrase-Group)
Style A was selected as the flagship documentary standard based on:
1. **Zero Graphic Clutter:** By eliminating the bounding capsule, the underlying visual composition breathes naturally without artificial borders.
2. **Cognitive Synchronization:** Presenting complete syntactic units (4–7 words) matches human reading psychology, while the warm gold highlight allows viewers to instantly track speech progression.
3. **Dual-Canvas Adaptability:** The subtle soft radial backing adapts seamlessly to both dark cryostat scenes and bright warm stone architectural scenes.

---

## 3. MASTER TYPOGRAPHY SCALE

The production engine employs a strictly governed typographic hierarchy rendered via TrueType fonts loaded dynamically from the Windows system repository:

| Role | Font Family | Size (pt) | Weight | Leading | Tracking | Color Hex | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Display** | Georgia / Times New Roman | $54\text{ pt}$ | Bold | $64\text{ pt}$ | $+1.5\text{px}$ | `#FFFFFF` / `#0F172A` | Scene hero titles, primary numbers (`10 SEPTILLION`) |
| **Editorial Title** | Georgia / Garamond | $42\text{ pt}$ | Bold | $50\text{ pt}$ | $+1.0\text{px}$ | `#F1F5F9` / `#0F172A` | Secondary scene titles, publication headlines |
| **Section Kicker** | DejaVu Sans Mono / Consolas | $22\text{ pt}$ | Bold | $28\text{ pt}$ | $+3.0\text{px}$ | `#D4AF37` / `#0284C7` | Category badges (`PHYSICAL HARDWARE // 01`) |
| **Subtitle Text** | Segoe UI / Arial / Trebuchet | $34\text{ pt}$ | Semi-Bold | $44\text{ pt}$ | $+0.5\text{px}$ | `#F8FAFC` / `#0F172A` | Narration synchronized phrase groups |
| **Subtitle Active** | Segoe UI / Arial / Trebuchet | $36\text{ pt}$ | Bold | $44\text{ pt}$ | $+0.8\text{px}$ | `#FCD34D` (Gold) | Current spoken word token |
| **Leader Badge** | Segoe UI / Arial / Trebuchet | $24\text{ pt}$ | Bold | $30\text{ pt}$ | $+0.5\text{px}$ | `#F1F5F9` | Diagram callout titles (`COLD FINGER`) |
| **Leader Metric** | Segoe UI / Arial / Trebuchet | $20\text{ pt}$ | Regular | $26\text{ pt}$ | $0.0\text{px}$ | `#94A3B8` | Technical specs (`10 mK Operating Temp`) |
| **Scientific Mono**| DejaVu Sans Mono / Consolas | $18\text{ pt}$ | Medium | $24\text{ pt}$ | $+1.0\text{px}$ | `#38BDF8` / `#34D399` | Timestamps, error rates ($\Lambda = 0.79$) |

---

## 4. SUBTITLE SAFE-ZONE & SYNCHRONIZATION RULES

### 4.1 Safe-Zone Enforcement
- **Baseline Y-Coordinate:** Fixed at $Y = 1460\text{ px}$.
- **Vertical Bounding Span:** $Y \in [1420\text{px}, 1505\text{px}]$ (Height = $85\text{px}$).
- **Horizontal Margins:** Centered at $X = 540\text{ px}$, with maximum text block width constrained to $W \le 900\text{ px}$.
- **Clearance Margins:**
  - Clearance below Hero Subject: Minimum $80\text{ px}$ separation from any diagram geometry.
  - Clearance above Mobile UI: Minimum $260\text{ px}$ separation from the screen bottom ($1920\text{ px}$), placing subtitles completely clear of TikTok/Reels/Shorts bottom engagement buttons, progress bars, and creator handles.

### 4.2 Narration Synchronization Standard
1. **Phrasing Windows:** No subtitle chunk shall remain on screen for less than $1.2\text{s}$ or more than $3.5\text{s}$.
2. **Word Highlighting:** The active word transitions synchronously with the Kokoro-82M audio waveform at predetermined phoneme boundaries.
3. **Line Breaks:** Punctuation marks (commas, colons, periods) dictate phrase segmentation to maintain grammatical flow.

---

## 5. DUAL-MASTER REPRODUCIBILITY

To serve both social media publishing and high-end archival distribution, the pipeline renders two synchronized master video streams simultaneously:

1. **Captioned Review Master (`willow_quantum_flagship_captioned_review.mp4`):**
   - Features the complete Style A subtitle architecture with synchronized gold highlighting.
   - Ideal for human editorial review, mobile previewing, and direct closed-captioned distribution.
2. **Clean Archival Master (`willow_quantum_flagship_clean_master.mp4`):**
   - Features 100% identical camera choreography, lighting, and technical diagrams with **zero** burned-in subtitles.
   - Ideal for multi-language localization, high-resolution broadcast remastering, and museum/exhibition display.
