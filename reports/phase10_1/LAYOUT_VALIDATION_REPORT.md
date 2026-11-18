# PHASE 10.1 — AUTOMATED LAYOUT VALIDATION REPORT
## Forensic Mathematical Verification of All Text Elements, Containers & Safe Areas

**Date:** 2026-11-16  
**Document:** Layout Validation Report  
**Target Video:** `output/drafts/phase10_1_layout_repair/phase10_1_captioned_review_master.mp4`  
**Canvas Dimensions:** 1080 × 1920 (9:16 Portrait)  
**Theme:** Unified Scientific Light Theme (Pearl `#F8F9FA`)  
**Validator:** `rendering/automated_layout_validator.py`  

---

## 1. Automated Mathematical Audit Summary

Every text element across all 7 scenes was measured using real FreeType font glyph bounding boxes (`draw.textbbox`) and evaluated against strict layout rules:

| Rule Category | Description | Permitted Threshold | Measured Worst-Case | Pass / Fail Status |
|:---|:---|:---:|:---:|:---:|
| **Horizontal Safe Margin (Left)** | Distance from canvas left edge (`x=0`) to text left glyph | $\ge 60\text{px}$ (Headers), $\ge 90\text{px}$ (Subs) | $90\text{px}$ | **PASS** |
| **Horizontal Safe Margin (Right)** | Distance from text right glyph to canvas right edge (`x=1080`) | $\ge 60\text{px}$ (Headers), $\ge 90\text{px}$ (Subs) | $90\text{px}$ | **PASS** |
| **Vertical Safe Margin (Top)** | Distance from canvas top edge (`y=0`) to first text baseline | $\ge 60\text{px}$ | $90\text{px}$ | **PASS** |
| **Vertical Safe Margin (Bottom)** | Distance from lowest text glyph to canvas bottom (`y=1920`) | $\ge 80\text{px}$ | $140\text{px}$ | **PASS** |
| **Text-on-Text Collision** | Bounding box intersection between distinct text elements | $0\text{px}^2$ | $0\text{px}^2$ | **PASS** |
| **Container Overflow** | Any glyph exceeding parent card boundary $(x_0, y_0, w, h)$ | $0\text{px}$ | $0\text{px}$ | **PASS** |
| **Subtitle Line Count** | Maximum lines rendered per caption phrase | $\le 2$ lines | 2 lines max | **PASS** |
| **Mobile Readability (Main)** | Minimum font size for explanatory / data text | $\ge 20\text{pt}$ | $20\text{pt}$ (footnotes), $26\text{pt}$ (body) | **PASS** |
| **Mobile Readability (Subtitles)** | Font size for spoken narration captions | $\ge 32\text{pt}$ | $38\text{pt}$ (Sans), $32\text{pt}$ (Mono) | **PASS** |

---

## 2. Scene-by-Scene Layout Verification

### Scene 1: The Golden Chandelier (0.0s – 7.67s)
- **Header:** Tag `ORIGIN STORY // 01` at `(60, 90)`, Title `THE GOLDEN CHANDELIER` at `(60, 124)`, Subtitle at `(60, 178)`. Protected by cleanroom gradient mask `Y=0..235`.
- **Hardware Bounding:** Top flange at `Y=340` (105px clearance below header). Lowest QPU canister at `Y=1240`.
- **Subtitle Safe Zone:** Subtitle container `Y=1640..1780` (400px vertical clearance below apparatus). Width bounded at 900px across 2 lines:
  - Line 1: *"Ever wondered why the world's most powerful"* (width 742px, centered at $x=169$).
  - Line 2: *"quantum computers look like giant golden chandeliers?"* (width 856px, centered at $x=112$).
  - Zero left/right clipping. First glyph `E` at $x=169 \ge 90$; last glyph `?` at $x=968 \le 990$.

### Scene 2: The Coherence Crisis (7.67s – 18.17s)
- **Thermometer Scale Card:** Positioned at `(60, 260)` with width 120px and height 1140px. Temperature labels (`300 K` to `10 mK`) padded with 24px clearance from card ticks.
- **Central Mixing Stage Card:** Positioned at `(440, 540)` with width 480px, height 520px. Telemetry pill separated by 42px clearance below plate.
- **Subtitle Safe Zone:** Centered at `Y=1680`, width $\le 840$px, 2 lines. Zero collision.

### Scene 3: Google Willow (18.17s – 27.14s)
- **QPU Die Card:** Centered at `(60, 260)` with usable width 960px.
- **Wirebond Fingers:** 32 gold wirebonds positioned along perimeter pads with 46px pitch. Zero interference with inner transmon grid.
- **105 Transmon Grid:** 11 columns $\times$ 10 rows. Capacitor radius 15px with coplanar waveguide traces. Clean 50px bottom margin above telemetry badge.

### Scene 4: Real-Time Stabilizer Dynamics (27.14s – 37.57s)
- **5x5 Surface Code Lattice:** Node pitch 160px.
- **Bit-Flip Alert Pill:** `BIT-FLIP DETECTED` badge anchored at `pt_err + (48, -32)` within bounded safe zone, strictly clear of neighboring ancilla nodes.
- **Healed Pill:** `HEALED IN 840ns` badge anchored at identical location, providing seamless before/after transition.

### Scene 5: Below-Threshold Scaling (37.57s – 47.35s)
- **Nature Masthead:** Red `nature` logo at `(104, 296)` with volume metadata at `(270, 312)`, separated by clean architectural line at `Y=364`.
- **Axes & Tick Separation:**
  - Y-axis origin at $X=230$ (leaving 170px margin for logarithmic tick numbers `10^-2`, `10^-3`, `10^-4`).
  - X-axis tick labels (`d = 3`, `d = 5`, `d = 7`) anchored at `ax_y0 + 18` with qubit annotations at `ax_y0 + 62`.
  - Axis title `SURFACE CODE DISTANCE (d)` placed at `ax_y0 + 105` (43px clearance below qubit text). Zero collision.
- **Data Points & Error Bars:** 3 empirical points with 24px $1\sigma$ error bars and glowing below-threshold trendline ($\Lambda = 0.79 \pm 0.02$).

### Scene 6: Computational Supremacy Benchmark (47.35s – 56.47s)
- **Two-Column Card:** Width 960px, divided at $X=540$ by central vertical line.
- **Left Column (Frontier):** Width 436px. Main headline `10 SEPTILLION` at 36pt bold, subhead `YEARS (10^25 YR)` at 32pt bold. Line leading 55px prevents vertical crowding.
- **Right Column (Willow):** Width 436px. Main headline `< 5 MINUTES` at 36pt bold, subhead `(UNDER 300 SECONDS)` at 30pt bold. Progress bar animates smoothly to 100%.
- **Zero Horizontal Overlap:** Gutter width between columns is exactly **88px**.

### Scene 7: The Fault-Tolerant Horizon (56.47s – 63.89s)
- **Cleanroom Rack Array:** 3 dilution refrigerator nodes at $X = 240, 540, 840$.
- **Node Badges:** High-contrast emerald badges `NODE 01`, `NODE 02`, `NODE 03` with status `10 mK // OK` at 24pt bold.
- **Gold Verification Seal:** Centered at `Y=1140`, width 720px, height 160px.
