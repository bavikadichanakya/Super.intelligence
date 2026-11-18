# SUPER.INTELLIGENCEEE — Phase 4.3.2D Remediation Report
# Subtitle Layout, Safe Zone Typography & Mobile UX Danger Avoidance

**Document ID:** `PHASE432D_SUBTITLE_LAYOUT`  
**Phase:** 4.3.2D Remediation  
**Status:** REMEDIATED & VERIFIED  
**Date:** November 14, 2026  
**Target:** 100% compliance with YouTube Shorts, TikTok & IG Reels interaction safe zones  

---

## 1. Executive Summary

Mobile vertical video platforms (YouTube Shorts, TikTok, Instagram Reels) overlay interactive controls and metadata directly on top of video playback:
- Bottom area: Account handle, sound title, comment bar, like/share icons, progress bar.
- Top area: Channel avatar, search icon, system status bar.
- Right edge: Action buttons (Like, Comment, Bookmark, Share).

In Phase 4.3.2C, ASS subtitles were rendered at `MarginV = 160`, which positioned subtitle baselines at $y = 1760$px ($1920 - 160 = 1760$). Because the mobile UI overlay danger zone extends upward 260px from the bottom ($y \ge 1660$px), subtitles were partially obscured by platform UI buttons and caption overlays.

In Phase 4.3.2D, subtitle layout was elevated to `MarginV = 380`, placing text at $y \approx 1540$px, safely above the 260px hazard zone while leaving ample room for on-screen motion graphics.

---

## 2. Platform Safe Zone Specifications

For vertical 9:16 video ($1080 \times 1920$ resolution):

| Zone | Boundary | Purpose | Enforced Rule |
| :--- | :--- | :--- | :--- |
| **Top Hazard Zone** | $0 \le y \le 180$px | Platform search, status icons | No primary text or data points |
| **Bottom Hazard Zone** | $1660 \le y \le 1920$px | Captions, sound attribution, UI controls | Strict exclusion: Zero subtitles or critical graphics |
| **Side Margin Zones** | $x < 60$px and $x > 1020$px | Right-hand action buttons, screen bevels | Safe padding for all text and cards |
| **Primary Safe Zone** | $x \in [60, 1020]$, $y \in [180, 1660]$ | Unobstructed visual viewing | Target canvas for all explanations |
| **Subtitle Placement Band** | $y \in [1450, 1580]$px | High visibility reading band | Subtitle baseline at $y = 1540$px |

---

## 3. Remediation Architecture

### 3.1 ASS Subtitle Configuration (`rendering/adapters/ffmpeg_adapter.py`)
In `FFmpegAdapter._generate_ass_subtitles`:
```ini
; PHASE 4.3.2D UPDATED ASS STYLE HEADER:
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,68,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,60,60,380,1
```
Key parameters:
- `Alignment = 2` (Bottom-Center aligned).
- `MarginV = 380` (Vertical margin from bottom edge: $1920 - 380 = 1540$px).
- `MarginL = 60`, `MarginR = 60` (Horizontal margins preventing edge clipping).
- `Outline = 4`, `Shadow = 2` (High-contrast drop shadow for legibility over diverse backgrounds).

### 3.2 Safe Zone Enforcement in Native Typography (`rendering/native_motion_engine/typography.py`)
A dedicated `SafeZone` dataclass is now embedded across all native motion components:
```python
@dataclass
class SafeZone:
    top: int = 180
    bottom: int = 260
    left: int = 60
    right: int = 60
    width: int = 1080
    height: int = 1920

    @property
    def safe_y_max(self) -> int:
        return self.height - self.bottom  # 1660 px
```
Before any text is rendered, `TypographyEngine.render_text()` computes the bounding box and asserts:
$$y_1 \le 1660\text{ px}$$
If text bounds violate the safe zone, the typography engine automatically reduces font size or breaks into additional lines.

---

## 4. Verification & Test Coverage

Test `test_06_subtitle_danger_zone_avoidance` in `tests/test_phase432d_remediation.py`:
- Generates ASS subtitle file via `FFmpegAdapter._generate_ass_subtitles`.
- Parses style definitions and dialogue event coordinates.
- Asserts `MarginV >= 350`.
- Calculates rendered vertical position: $y_{\text{base}} = 1920 - 380 = 1540$px.
- Asserts $y_{\text{base}} < 1660$px (comfortably outside the 260px danger zone).
- Status: **PASSED**.
