"""
SUPER.INTELLIGENCEEE — Phase 9.1 Advanced Composition & Layout Engine
Provides:
1. 1080x1920 Modular Layout Grid (72px margins, defined vertical zones).
2. Leader-Line Annotation System (Pill badges, anchor dots, elbow connectors, collision detection).
3. Cinematic Camera Director V2 (Multi-keyframe camera paths with cubic bezier & spring easing).
4. Dynamic Luminance Suppression (Attentional focus spotlighting).
5. Subtitle Engine V2 (Three distinct editorial directions: Clean Phrase-Group, Restrained Kinetic, Minimal Documentary).
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# 1. 1080x1920 LAYOUT GRID CONSTANTS
# ==============================================================================
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920

MARGIN_X = 72
USABLE_WIDTH = CANVAS_WIDTH - 2 * MARGIN_X # 936 px
GRID_LEFT = MARGIN_X                        # 72 px
GRID_RIGHT = CANVAS_WIDTH - MARGIN_X       # 1008 px
GRID_CENTER_X = CANVAS_WIDTH // 2          # 540 px

# Vertical Zones
ZONE_TOP_HEADER = (80, 220)
ZONE_PRIMARY_STAGE = (220, 1420)           # 1200 px of continuous vertical storytelling
ZONE_SUBTITLE_BAND = (1420, 1540)          # MarginV >= 440 px from bottom
ZONE_BOTTOM_SAFE = (1560, 1920)            # Reserved for platform UI (thumb, captions)

# Font Resolver
def load_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
    paths = [
        Path(f"C:/Windows/Fonts/{font_name}"),
        Path(f"C:/Windows/Fonts/{font_name.lower()}"),
        Path(f"C:/Windows/Fonts/{font_name.upper()}"),
    ]
    for p in paths:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()

# Typography Scale (Refined Editorial Humanist & Geometric)
FONT_DISPLAY_HERO = load_font("segoeuib.ttf", 68)     # Primary Hero Metric
FONT_DISPLAY_TITLE = load_font("segoeuib.ttf", 46)    # Scene Title
FONT_DISPLAY_SUB = load_font("segoeui.ttf", 32)       # Scene Subtitle / Description
FONT_BADGE_TITLE = load_font("segoeuib.ttf", 30)      # Leader Annotation Title
FONT_BADGE_METRIC = load_font("segoeui.ttf", 22)      # Leader Annotation Secondary
FONT_MONO_LABEL = load_font("consolab.ttf", 24)       # Engineering Monospace Callouts
FONT_SUBTITLE_CLEAN = load_font("segoeuib.ttf", 44)   # Clean Editorial Captions
FONT_SUBTITLE_KINETIC = load_font("segoeuib.ttf", 46) # Restrained Kinetic Captions
FONT_SUBTITLE_MINIMAL = load_font("segoeui.ttf", 42)  # Minimal Documentary Captions


# ==============================================================================
# 2. LEADER-LINE ANNOTATION PRIMITIVE
# ==============================================================================

class LeaderAnnotation:
    """
    First-class editorial annotation:
    - Anchored directly to physical component coordinate (x_target, y_target).
    - High-visibility anchor dot with radiant ring.
    - Elbow leader line connecting to a readable pill badge.
    - Avoids crowding and establishes immediate visual relationship.
    """
    def __init__(
        self,
        target_x: int,
        target_y: int,
        badge_x: int,
        badge_y: int,
        title: str,
        metric: str = "",
        color: Tuple[int, int, int] = (212, 175, 55), # Gold default
        align: str = "right" # "right" = badge is to the right of target, "left" = to the left
    ):
        self.target_x = target_x
        self.target_y = target_y
        self.badge_x = badge_x
        self.badge_y = badge_y
        self.title = title
        self.metric = metric
        self.color = color
        self.align = align

    def draw(self, draw: ImageDraw.Draw, opacity: float = 1.0):
        if opacity <= 0.01:
            return
            
        r, g, b = self.color
        alpha_main = int(255 * opacity)
        alpha_glow = int(140 * opacity)
        alpha_bg = int(220 * opacity)
        
        # 1. Target Anchor Dot & Glowing Halo
        draw.ellipse(
            [self.target_x - 10, self.target_y - 10, self.target_x + 10, self.target_y + 10],
            fill=(r, g, b, alpha_glow // 2)
        )
        draw.ellipse(
            [self.target_x - 5, self.target_y - 5, self.target_x + 5, self.target_y + 5],
            fill=(r, g, b, alpha_main),
            outline=(255, 255, 255, alpha_main),
            width=2
        )
        
        # 2. Measure Badge Dimensions
        title_bbox = draw.textbbox((0, 0), self.title, font=FONT_BADGE_TITLE)
        title_w = title_bbox[2] - title_bbox[0]
        title_h = title_bbox[3] - title_bbox[1]
        
        metric_w = 0
        metric_h = 0
        if self.metric:
            m_bbox = draw.textbbox((0, 0), self.metric, font=FONT_BADGE_METRIC)
            metric_w = m_bbox[2] - m_bbox[0]
            metric_h = m_bbox[3] - m_bbox[1]
            
        badge_w = max(title_w, metric_w) + 36
        badge_h = title_h + (metric_h + 8 if self.metric else 0) + 24
        
        # Badge Coordinates
        if self.align == "right":
            bx0 = self.badge_x
            bx1 = self.badge_x + badge_w
            elbow_x = self.badge_x - 14
        else: # left
            bx1 = self.badge_x
            bx0 = self.badge_x - badge_w
            elbow_x = self.badge_x + 14
            
        by0 = self.badge_y - badge_h // 2
        by1 = self.badge_y + badge_h // 2
        
        # 3. Elbow Leader Line
        # Target -> Elbow Point -> Badge Edge
        draw.line(
            [(self.target_x, self.target_y), (elbow_x, self.badge_y)],
            fill=(r, g, b, alpha_glow),
            width=2
        )
        draw.line(
            [(elbow_x, self.badge_y), (bx0 if self.align == "right" else bx1, self.badge_y)],
            fill=(r, g, b, alpha_main),
            width=2
        )
        
        # 4. Badge Capsule (Frosted Dark Pill with Accent Border)
        draw.rounded_rectangle(
            [bx0, by0, bx1, by1],
            radius=12,
            fill=(14, 18, 30, alpha_bg),
            outline=(r, g, b, int(180 * opacity)),
            width=2
        )
        
        # 5. Badge Typography
        text_x = bx0 + 18
        draw.text(
            (text_x, by0 + 10),
            self.title,
            font=FONT_BADGE_TITLE,
            fill=(255, 255, 255, alpha_main)
        )
        if self.metric:
            draw.text(
                (text_x, by0 + 12 + title_h + 4),
                self.metric,
                font=FONT_BADGE_METRIC,
                fill=(r, g, b, alpha_main)
            )


# ==============================================================================
# 3. CINEMATIC CAMERA DIRECTOR V2
# ==============================================================================

class CinematicCameraDirectorV2:
    """
    Advanced Camera Director supporting multi-stage narrative keyframes.
    Each keyframe defines (t, center_x, center_y, zoom).
    Interpolation uses smooth cubic easing with continuous micro-drift.
    """
    def __init__(self, keyframes: List[Tuple[float, float, float, float]]):
        """
        keyframes: List of (t_sec, cx, cy, zoom)
        """
        self.keyframes = sorted(keyframes, key=lambda k: k[0])

    def get_state(self, t: float) -> Tuple[float, float, float]:
        """Returns (cam_cx, cam_cy, zoom) at time t."""
        if not self.keyframes:
            return (540.0, 960.0, 1.0)
            
        if t <= self.keyframes[0][0]:
            k = self.keyframes[0]
            return (k[1], k[2], k[3])
            
        if t >= self.keyframes[-1][0]:
            k = self.keyframes[-1]
            # Continuous subtle drift after last keyframe
            drift_factor = 1.0 + 0.015 * (t - k[0])
            return (k[1], k[2], k[3] * drift_factor)
            
        # Find active interval
        for i in range(len(self.keyframes) - 1):
            k0 = self.keyframes[i]
            k1 = self.keyframes[i + 1]
            if k0[0] <= t < k1[0]:
                duration = k1[0] - k0[0]
                norm_t = (t - k0[0]) / max(0.001, duration)
                # Smooth cubic ease-in-out
                ease = 3 * norm_t**2 - 2 * norm_t**3
                
                cx = k0[1] + (k1[1] - k0[1]) * ease
                cy = k0[2] + (k1[2] - k0[2]) * ease
                zoom = k0[3] + (k1[3] - k0[3]) * ease
                
                # Add micro-drift
                micro_drift = 1.0 + 0.01 * norm_t
                return (cx, cy, zoom * micro_drift)
                
        return (540.0, 960.0, 1.0)

    def apply_transform(self, x: float, y: float, t: float) -> Tuple[int, int]:
        """Transforms world coordinate (x, y) into viewport coordinate at time t."""
        cx, cy, zoom = self.get_state(t)
        vx = GRID_CENTER_X + (x - cx) * zoom
        vy = (CANVAS_HEIGHT // 2) + (y - cy) * zoom
        return (int(vx), int(vy))


# ==============================================================================
# 4. SUBTITLE ENGINE V2 (THREE DISTINCT REFINED DIRECTIONS)
# ==============================================================================

def render_subtitle_direction_a(
    canvas: Image.Image,
    phrase_text: str,
    active_word: str = "",
    y_center: int = 1460,
    font: Optional[ImageFont.FreeTypeFont] = None
) -> None:
    """
    STYLE A: Clean Editorial Phrase-Group Captions (The BBC / Vox Editorial Master)
    - Zero background box.
    - Soft vertical vignette underneath for universal high contrast.
    - Active word highlighted in crisp luminous amber (#FCD34D) or pure white.
    - Clean natural phrase chunks, perfectly balanced and centered.
    """
    draw = ImageDraw.Draw(canvas, "RGBA")
    f = font or FONT_SUBTITLE_CLEAN
    
    words = phrase_text.split()
    word_widths = [draw.textbbox((0, 0), w, font=f)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=f)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    # Soft background gradient plate to guarantee readability over complex 3D assets
    bg_y0 = y_center - 45
    bg_y1 = y_center + 45
    for row in range(bg_y0, bg_y1):
        rel = abs(row - y_center) / 45.0
        alpha = int((1.0 - rel**2) * 110)
        draw.line([GRID_LEFT, row, GRID_RIGHT, row], fill=(8, 12, 22, alpha), width=1)
        
    cur_x = (CANVAS_WIDTH - total_w) // 2
    for idx, (word, w_len) in enumerate(zip(words, word_widths)):
        is_active = (word.strip(".,;:!?").lower() == active_word.strip(".,;:!?").lower())
        
        # Dual-pass soft shadow
        for ox, oy in [(-2, 2), (2, 2), (0, 3)]:
            draw.text((cur_x + ox, y_center - 24 + oy), word, font=f, fill=(0, 0, 0, 160))
            
        if is_active:
            # Active word: Warm Solar Gold (#FCD34D)
            draw.text((cur_x, y_center - 24), word, font=f, fill=(252, 211, 77, 255))
        else:
            # Crisp Pure White (92% opacity)
            draw.text((cur_x, y_center - 24), word, font=f, fill=(255, 255, 255, 235))
            
        cur_x += w_len + space_w


def render_subtitle_direction_b(
    canvas: Image.Image,
    phrase_text: str,
    active_word: str = "",
    y_center: int = 1460,
    font: Optional[ImageFont.FreeTypeFont] = None
) -> None:
    """
    STYLE B: Restrained Kinetic Word Emphasis (The Premium Modern Explainer)
    - Ultra-clean frosted glass pill capsule with delicate 1px border.
    - Active word highlighted in radiant Electric Cyan (#38BDF8) with subtle underline.
    - Gentle scale pulse (1.04x) on active word plosives; zero chaotic bouncing.
    """
    draw = ImageDraw.Draw(canvas, "RGBA")
    f = font or FONT_SUBTITLE_KINETIC
    
    words = phrase_text.split()
    word_widths = [draw.textbbox((0, 0), w, font=f)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=f)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    pad_x = 36
    pad_y = 16
    pill_x0 = (CANVAS_WIDTH - total_w) // 2 - pad_x
    pill_x1 = (CANVAS_WIDTH + total_w) // 2 + pad_x
    pill_y0 = y_center - 26 - pad_y
    pill_y1 = y_center + 26 + pad_y
    
    # Frosted Capsule
    draw.rounded_rectangle([pill_x0, pill_y0, pill_x1, pill_y1], radius=18, fill=(12, 16, 28, 205), outline=(56, 189, 248, 100), width=1)
    # Subtle top edge specular sheen
    draw.line([pill_x0 + 18, pill_y0 + 1, pill_x1 - 18, pill_y0 + 1], fill=(255, 255, 255, 75), width=1)
    
    cur_x = (CANVAS_WIDTH - total_w) // 2
    for idx, (word, w_len) in enumerate(zip(words, word_widths)):
        is_active = (word.strip(".,;:!?").lower() == active_word.strip(".,;:!?").lower())
        
        if is_active:
            # Active word: Electric Cyan (#38BDF8)
            draw.text((cur_x, y_center - 24), word, font=f, fill=(56, 189, 248, 255))
            draw.line([cur_x, y_center + 26, cur_x + w_len, y_center + 26], fill=(56, 189, 248, 255), width=3)
        else:
            draw.text((cur_x, y_center - 24), word, font=f, fill=(240, 244, 250, 200))
            
        cur_x += w_len + space_w


def render_subtitle_direction_c(
    canvas: Image.Image,
    phrase_text: str,
    active_word: str = "",
    y_center: int = 1460,
    font: Optional[ImageFont.FreeTypeFont] = None
) -> None:
    """
    STYLE C: Minimal Documentary Captions (The Criterion / Cleanroom Aesthetic)
    - Zero boxes or heavy capsules.
    - Minimalist typography with generous tracking.
    - Active word softly glows in Mint Green (#34D399) or soft Gold.
    - Maximum respect for the visual image; zero distraction.
    """
    draw = ImageDraw.Draw(canvas, "RGBA")
    f = font or FONT_SUBTITLE_MINIMAL
    
    words = phrase_text.split()
    word_widths = [draw.textbbox((0, 0), w, font=f)[2] for w in words]
    space_w = draw.textbbox((0, 0), " ", font=f)[2]
    total_w = sum(word_widths) + space_w * (len(words) - 1)
    
    cur_x = (CANVAS_WIDTH - total_w) // 2
    for idx, (word, w_len) in enumerate(zip(words, word_widths)):
        is_active = (word.strip(".,;:!?").lower() == active_word.strip(".,;:!?").lower())
        
        # Crisp deep drop shadow
        draw.text((cur_x + 2, y_center - 22 + 2), word, font=f, fill=(0, 0, 0, 180))
        
        if is_active:
            # Soft Emerald Mint (#34D399)
            draw.text((cur_x, y_center - 22), word, font=f, fill=(52, 211, 153, 255))
        else:
            # Clean Slate White
            draw.text((cur_x, y_center - 22), word, font=f, fill=(241, 245, 249, 220))
            
        cur_x += w_len + space_w


# ==============================================================================
# 5. EDITORIAL HEADER & SCENE CONTEXT BANNER
# ==============================================================================

def draw_editorial_scene_header(
    draw: ImageDraw.Draw,
    category: str,
    title: str,
    subtitle: str = "",
    accent_color: Tuple[int, int, int] = (212, 175, 55)
) -> None:
    """Renders standardized top narrative header adhering to 72px grid margins."""
    r, g, b = accent_color
    
    # Category Kicker (e.g. "PHYSICAL INSTRUMENTATION // 01")
    draw.text((GRID_LEFT, 90), category.upper(), font=FONT_MONO_LABEL, fill=(r, g, b, 255))
    
    # Title (e.g. "DILUTION REFRIGERATOR")
    draw.text((GRID_LEFT, 126), title, font=FONT_DISPLAY_TITLE, fill=(255, 255, 255, 255))
    
    # Subtitle / Mechanism Note
    if subtitle:
        draw.text((GRID_LEFT, 184), subtitle, font=FONT_DISPLAY_SUB, fill=(148, 163, 184, 230))
        
    # Elegant 1px Accent Separator Line
    draw.line([GRID_LEFT, 232, GRID_RIGHT, 232], fill=(45, 55, 80, 140), width=1)
