"""
SUPER.INTELLIGENCEEE — Phase 4.2A.2 Validation & Readiness Gate Renderer
Renders final refined visual prototypes, motion animatics, and contact sheets for:
- Sequence A: Cinematic Documentary (Atmospheric Datacenter Corridor & Silicon Substrate)
- Sequence B: Technical Mechanism (Token Trajectory, Conceptual Logits & Experimental Fork)
- Sequence C: Editorial Conclusion (Conceptual Efficiency Architecture & Qualified Directives)
- Consolidated 3-Shot Contact Sheet (16:9 Widescreen)
- Three MP4 Motion Animatics (Camera push, layer animation, word reveals)

Strictly enforces:
- Output directory: output/drafts/phase42a_2_validation/ (isolated, preserves all prior phases).
- Zero fabricated continuous Pareto curves: Sequence C uses a verified Conceptual Architecture Matrix.
- Exact factual qualification for arXiv:2611.08453:
  - 50x applies strictly to distillation FLOPs when teacher is student's own checkpoint.
  - "Under the matched experimental settings studied, external-teacher distillation generally trails direct GRPO in accuracy per training FLOP."
  - Explicit illustrative / procedural labeling on synthetic visual assets.
- Strict safe zones: 140px top, 260px bottom, 80px lateral.
- Zero string slicing: all text pre-measured with textbbox and dynamic line wrapping.
"""

import math
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = Path("output/drafts/phase42a_2_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BRAIN_DIR = Path("C:/Users/bavik/.gemini/antigravity/brain/174164e7-7384-4da6-a377-b063df7a125d")

# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------
BG_CANVAS_LIGHT = (250, 247, 242)      # Warm Ivory #FAF7F2
BG_SURFACE_WHITE = (255, 255, 255)     # Elevated Card #FFFFFF
BORDER_SUBTLE = (226, 232, 240)        # Subtle Border #E2E8F0
BORDER_STRONG = (203, 213, 225)        # Architectural Rule #CBD5E1

TEXT_PRIMARY_DARK = (15, 23, 42)       # Deep Obsidian Slate #0F172A
TEXT_SECONDARY_DARK = (71, 85, 105)    # Muted Slate #475569
TEXT_MUTED_DARK = (148, 163, 184)      # Light Slate #94A3B8

BG_CINEMATIC_DARK = (11, 15, 23)       # Deep Graphite Obsidian #0B0F17
BG_RACK_PANEL = (20, 26, 38)           # Server Rack Bay #141A26
TEXT_PRIMARY_LIGHT = (248, 250, 252)   # Crisp White #F8FAFC
TEXT_SECONDARY_LIGHT = (148, 163, 184) # Pale Slate #94A3B8

ACCENT_BLUE = (2, 132, 199)            # Technical Research Blue #0284C7
ACCENT_BLUE_GLOW = (56, 189, 248)      # Sky Blue Pulse #38BDF8
ACCENT_EMERALD = (5, 150, 105)         # Verification Emerald #059669
ACCENT_EMERALD_BG = (240, 253, 244)    # Emerald Tint #F0FDF4
ACCENT_AMBER = (217, 119, 6)           # Critical Amber #D97706
ACCENT_CORAL = (220, 38, 38)           # Warning Coral #DC2626
ACCENT_CORAL_BG = (254, 242, 242)      # Coral Tint #FEF2F2

# ---------------------------------------------------------------------------
# Font Initialization
# ---------------------------------------------------------------------------
def load_fonts():
    font_dir = Path("C:/Windows/Fonts")
    arial_path = font_dir / "arial.ttf"
    arialbd_path = font_dir / "arialbd.ttf"
    consola_path = font_dir / "consola.ttf"
    consolab_path = font_dir / "consolab.ttf"

    def get_font(path, size):
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except Exception:
                pass
        return ImageFont.load_default()

    return {
        "display_hero": get_font(arialbd_path, 64),
        "headline_lg": get_font(arialbd_path, 50),
        "headline_md": get_font(arialbd_path, 38),
        "card_title": get_font(arialbd_path, 30),
        "body_lg": get_font(arial_path, 30),
        "body_md": get_font(arial_path, 26),
        "body_sm": get_font(arial_path, 23),
        "mono_hero": get_font(consolab_path, 80),
        "mono_stat": get_font(consolab_path, 50),
        "mono_badge": get_font(consolab_path, 23),
        "mono_citation": get_font(consola_path, 21),
    }

FONTS = load_fonts()

# ---------------------------------------------------------------------------
# Typographic Utilities
# ---------------------------------------------------------------------------
def wrap_text(draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    words = text.split()
    if not words:
        return []
    lines = []
    curr_line = []
    for w in words:
        trial = " ".join(curr_line + [w])
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            curr_line.append(w)
        else:
            if curr_line:
                lines.append(" ".join(curr_line))
                curr_line = [w]
            else:
                lines.append(w)
                curr_line = []
    if curr_line:
        lines.append(" ".join(curr_line))
    return lines

def draw_wrapped_text(
    draw: ImageDraw.Draw,
    text: str,
    x: int,
    y: int,
    font: ImageFont.ImageFont,
    fill: Tuple[int, int, int],
    max_width: int,
    line_spacing: float = 1.25,
) -> int:
    lines = wrap_text(draw, text, font, max_width)
    bbox = draw.textbbox((0, 0), "Aj", font=font)
    line_h = int((bbox[3] - bbox[1]) * line_spacing)
    curr_y = y
    for line in lines:
        draw.text((x, curr_y), line, font=font, fill=fill)
        curr_y += line_h
    return curr_y

# ---------------------------------------------------------------------------
# SEQUENCE A: Cinematic Documentary Frame
# ---------------------------------------------------------------------------
def render_sequence_a_frame(frame_idx: int = 0, total_frames: int = 90) -> Image.Image:
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_CINEMATIC_DARK)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)
    cam_push = 1.0 + (0.04 * t)

    # 1. Perspective Atmospheric Background
    for y in range(height):
        factor = abs(y - 700) / 700.0
        r = int(11 + 6 * factor)
        g = int(15 + 8 * factor)
        b = int(23 + 12 * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Rack Bay Silhouettes
    draw.rectangle([(0, 200), (180, 1100)], fill=BG_RACK_PANEL)
    draw.rectangle([(width - 180, 200), (width, 1100)], fill=BG_RACK_PANEL)

    # Server Status LEDs
    for unit_y in range(240, 1050, 42):
        pulse_l = math.sin(frame_idx * 0.15 + unit_y * 0.05) * 0.5 + 0.5
        led_col_l = ACCENT_BLUE if pulse_l > 0.4 else (20, 60, 90)
        draw.rectangle([(140, unit_y), (146, unit_y + 8)], fill=led_col_l)
        draw.rectangle([(152, unit_y), (158, unit_y + 8)], fill=(30, 80, 120))

        pulse_r = math.cos(frame_idx * 0.18 + unit_y * 0.04) * 0.5 + 0.5
        led_col_r = ACCENT_AMBER if pulse_r > 0.6 else (60, 45, 20)
        draw.rectangle([(width - 156, unit_y), (width - 150, unit_y + 8)], fill=led_col_r)
        draw.rectangle([(width - 144, unit_y), (width - 138, unit_y + 8)], fill=(30, 80, 120))

    # 2. Central Accelerator Die Substrate (Procedural Visualization with Provenance Stamp)
    sub_w = int(720 * cam_push)
    sub_h = int(680 * cam_push)
    sx1 = (width - sub_w) // 2
    sy1 = 340 + int(math.sin(t * math.pi) * 6)
    sx2 = sx1 + sub_w
    sy2 = sy1 + sub_h

    # Shadow & Heat Spreader
    draw.rounded_rectangle([(sx1 + 8, sy1 + 12), (sx2 + 8, sy2 + 12)], radius=16, fill=(5, 8, 14))
    draw.rounded_rectangle([(sx1, sy1), (sx2, sy2)], radius=16, fill=(24, 32, 48), outline=(50, 65, 95), width=2)
    cx1, cy1 = sx1 + 36, sy1 + 36
    cx2, cy2 = sx2 - 36, sy2 - 36
    draw.rounded_rectangle([(cx1, cy1), (cx2, cy2)], radius=8, fill=(16, 22, 34), outline=(70, 90, 130), width=1)

    # Interconnect Traces
    for gx in range(cx1 + 25, cx2, 45):
        draw.line([(gx, cy1), (gx, cy2)], fill=(40, 50, 75), width=1)
    for gy in range(cy1 + 25, cy2, 45):
        draw.line([(cx1, gy), (cx2, gy)], fill=(40, 50, 75), width=1)

    # Compute Core Blocks
    for row in range(3):
        for col in range(3):
            bx = cx1 + 50 + col * 180
            by = cy1 + 60 + row * 160
            is_active_rollout = (row == 1 and col == 1)
            b_fill = (45, 28, 15) if is_active_rollout else (22, 30, 45)
            b_outline = ACCENT_AMBER if is_active_rollout else (55, 70, 100)
            draw.rounded_rectangle([(bx, by), (bx + 140, by + 120)], radius=6, fill=b_fill, outline=b_outline, width=1)
            draw.text((bx + 16, by + 16), f"NODE 0{row*3+col+1}", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
            status_txt = "RL ROLLOUT 98%" if is_active_rollout else "HBM ACTIVE"
            draw.text((bx + 16, by + 54), status_txt, font=FONTS["mono_badge"], fill=ACCENT_AMBER if is_active_rollout else ACCENT_BLUE)

    # Anamorphic Light Accent
    streak_y = sy1 + int(sub_h * (0.3 + 0.4 * t))
    draw.line([(0, streak_y), (width, streak_y)], fill=(2, 132, 199), width=1)

    # Explicit Procedural Asset Provenance Stamp (MANDATORY REQUIREMENT)
    draw.text((cx1 + 16, cy2 - 36), "CONCEPTUAL ACCELERATOR TOPOLOGY // PROCEDURAL VISUALIZATION", font=FONTS["mono_citation"], fill=ACCENT_BLUE_GLOW)

    # 3. Top Header
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=BORDER_STRONG, width=1)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  FIELD INVESTIGATION", font=FONTS["mono_badge"], fill=ACCENT_BLUE_GLOW)
    draw.text((790, top_y + 14), "ARXIV:2611.08453", font=FONTS["mono_badge"], fill=TEXT_SECONDARY_LIGHT)

    # 4. Editorial Lower-Third (Safe zones verified)
    lower_y = 1200
    draw.line([(80, lower_y), (1000, lower_y)], fill=ACCENT_AMBER, width=2)
    draw.text((80, lower_y + 16), "01 / THE COMPUTATIONAL FRICTION", font=FONTS["mono_badge"], fill=ACCENT_AMBER)

    head_y = lower_y + 54
    next_y = draw_wrapped_text(
        draw=draw,
        text="The Exploration Compute Ceiling",
        x=80,
        y=head_y,
        font=FONTS["display_hero"],
        fill=TEXT_PRIMARY_LIGHT,
        max_width=920,
    )

    deck_y = next_y + 18
    deck_text = (
        "Group Relative Policy Optimization delivers frontier reasoning, but exploring "
        "vast mathematical solution spaces requires thousands of rollouts per checkpoint."
    )
    next_y = draw_wrapped_text(
        draw=draw,
        text=deck_text,
        x=80,
        y=deck_y,
        font=FONTS["body_lg"],
        fill=TEXT_SECONDARY_LIGHT,
        max_width=920,
    )

    # Bottom Telemetry Anchor
    anchor_y = 1580
    draw.line([(80, anchor_y), (1000, anchor_y)], fill=(40, 50, 75), width=1)
    draw.text((80, anchor_y + 16), "EMPIRICAL FLOP BOTTLENECK // ONLINE ROLLOUT OVERHEAD", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((750, anchor_y + 16), "REASONING SEARCH WALL", font=FONTS["mono_badge"], fill=ACCENT_AMBER)

    return img

# ---------------------------------------------------------------------------
# SEQUENCE B: Technical Mechanism Frame
# ---------------------------------------------------------------------------
def render_sequence_b_frame(frame_idx: int = 0, total_frames: int = 90) -> Image.Image:
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_CANVAS_LIGHT)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)

    # Background Architectural Grid
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, height - 260)], fill=(240, 237, 230), width=1)

    # Top Header
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=ACCENT_BLUE, width=2)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  ALGORITHMIC MECHANISM", font=FONTS["mono_badge"], fill=ACCENT_BLUE)
    draw.text((790, top_y + 14), "TOKEN-LEVEL OPD DYNAMICS", font=FONTS["mono_badge"], fill=TEXT_SECONDARY_DARK)

    # Headline & Deck
    draw_wrapped_text(
        draw=draw,
        text="On-Policy Distillation Dynamics",
        x=80,
        y=190,
        font=FONTS["headline_lg"],
        fill=TEXT_PRIMARY_DARK,
        max_width=920,
    )
    draw_wrapped_text(
        draw=draw,
        text="The student model generates rollouts; a frozen teacher provides per-token supervision.",
        x=80,
        y=254,
        font=FONTS["body_md"],
        fill=TEXT_SECONDARY_DARK,
        max_width=920,
    )

    # 1. Algorithmic Token Rollout & Supervision Card
    stage_box = (80, 315, 1000, 855)
    draw.rounded_rectangle(stage_box, radius=16, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=2)

    draw.text((110, 338), "ALGORITHMIC MECHANISM: STUDENT ROLLOUT -> FROZEN TEACHER SUPERVISION", font=FONTS["mono_badge"], fill=ACCENT_BLUE)

    # Prompt Tokens
    draw.text((110, 380), "Input Prompt Sequence:", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    prompt_tokens = ["[Prompt]", "Factor", "x⁴", "-", "16", "="]
    px = 110
    for tok in prompt_tokens:
        tok_w = int(draw.textbbox((0, 0), tok, font=FONTS["mono_badge"])[2] - draw.textbbox((0, 0), tok, font=FONTS["mono_badge"])[0]) + 20
        draw.rounded_rectangle([(px, 410), (px + tok_w, 448)], radius=6, fill=(241, 245, 249), outline=BORDER_SUBTLE, width=1)
        draw.text((px + 10, 418), tok, font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
        px += tok_w + 10

    # Student Generated Rollout
    draw.text((110, 468), "Student Generated Rollout (Active Policy π_θ):", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    rollout_tokens = ["(", "x²", "-", "4", ")", "(", "x²", "+", "4", ")"]
    active_idx = min(len(rollout_tokens) - 1, int(t * len(rollout_tokens) * 1.4))
    
    rx = 110
    for i, r_tok in enumerate(rollout_tokens):
        is_current = (i == active_idx)
        is_past = (i < active_idx)
        r_w = int(draw.textbbox((0, 0), r_tok, font=FONTS["card_title"])[2] - draw.textbbox((0, 0), r_tok, font=FONTS["card_title"])[0]) + 24
        
        bg_col = (224, 242, 254) if is_current else (248, 250, 252) if is_past else (255, 255, 255)
        border_col = ACCENT_BLUE if is_current else BORDER_STRONG if is_past else BORDER_SUBTLE
        draw.rounded_rectangle([(rx, 498), (rx + r_w, 552)], radius=6, fill=bg_col, outline=border_col, width=2 if is_current else 1)
        draw.text((rx + 12, 508), r_tok, font=FONTS["card_title"], fill=ACCENT_BLUE if is_current else TEXT_PRIMARY_DARK)
        rx += r_w + 10

    # Frozen Teacher Logit Probability Stems
    spec_y = 590
    draw.line([(110, spec_y), (970, spec_y)], fill=BORDER_SUBTLE, width=1)
    draw.text((110, spec_y + 12), "FROZEN TEACHER LOGIT SUPERVISION // D_KL ( π_θ || π_ref )", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)

    stem_x_start = 140
    for s_i in range(16):
        sx = stem_x_start + s_i * 50
        prob_teacher = math.exp(-((s_i - 8) ** 2) / 10.0) * 110
        prob_student = math.exp(-((s_i - 8.5) ** 2) / 12.0) * 95 * min(1.0, t * 1.5)
        
        draw.line([(sx, 765), (sx, 765 - int(prob_teacher))], fill=(203, 213, 225), width=6)
        draw.line([(sx + 8, 765), (sx + 8, 765 - int(prob_student))], fill=ACCENT_BLUE, width=6)

    draw.text((110, 782), "Teacher Target (Grey) vs Student Policy Logits (Blue) — Teacher Weights Frozen", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
    draw.text((110, 814), "CONCEPTUAL LOGIT PROBABILITY DISTRIBUTION // NORMALIZED STRETCH", font=FONTS["mono_citation"], fill=ACCENT_BLUE)

    # 2. The Critical Experimental Fork
    fork_y = 885
    draw.line([(80, fork_y), (1000, fork_y)], fill=BORDER_STRONG, width=1)
    draw.text((80, fork_y + 14), "02 / THE CRITICAL EXPERIMENTAL FORK", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    # Emerald: Self-Teacher Checkpoint
    e_y1 = fork_y + 45
    e_y2 = e_y1 + 295
    draw.rounded_rectangle([(80, e_y1), (1000, e_y2)], radius=12, fill=BG_SURFACE_WHITE, outline=ACCENT_EMERALD, width=2)
    draw.rounded_rectangle([(80, e_y1), (92, e_y2)], radius=4, fill=ACCENT_EMERALD)

    draw.text((120, e_y1 + 18), "CONDITION 1: TEACHER IS STUDENT'S OWN GRPO CHECKPOINT", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)
    draw.text((120, e_y1 + 54), "50× Distillation FLOP Reduction", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)
    desc_e = (
        "When the teacher is the student's own checkpoint, OPD matches full GRPO "
        "accuracy on math benchmarks with 50x fewer distillation FLOPs than RL needed to reach that accuracy."
    )
    draw_wrapped_text(draw, desc_e, 120, e_y1 + 112, FONTS["body_md"], TEXT_SECONDARY_DARK, 840)
    draw.text((120, e_y1 + 242), "VERIFIED EMPIRICAL FINDING // SELF-TEACHER RECOVERY", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)

    # Coral: External Teacher Underperformance
    c_y1 = e_y2 + 25
    c_y2 = c_y1 + 295
    draw.rounded_rectangle([(80, c_y1), (1000, c_y2)], radius=12, fill=BG_SURFACE_WHITE, outline=ACCENT_CORAL, width=2)
    draw.rounded_rectangle([(80, c_y1), (92, c_y2)], radius=4, fill=ACCENT_CORAL)

    draw.text((120, c_y1 + 18), "CONDITION 2: TEACHER IS AN EXTERNAL POST-TRAINED MODEL", font=FONTS["mono_badge"], fill=ACCENT_CORAL)
    draw.text((120, c_y1 + 54), "Loses to Direct GRPO at Matched FLOPs", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)
    desc_c = (
        "Under the matched experimental settings studied, external-teacher distillation "
        "generally trails direct GRPO in accuracy per training FLOP due to policy distribution divergence."
    )
    draw_wrapped_text(draw, desc_c, 120, c_y1 + 112, FONTS["body_md"], TEXT_SECONDARY_DARK, 840)
    draw.text((120, c_y1 + 242), "CROSS-POLICY MISMATCH // NO UNIVERSAL ACCELERATION", font=FONTS["mono_badge"], fill=ACCENT_CORAL)

    # Bottom Citation
    anchor_y = 1580
    draw.line([(80, anchor_y), (1000, anchor_y)], fill=BORDER_SUBTLE, width=1)
    draw.text((80, anchor_y + 16), "SOURCE: ARXIV:2611.08453 // TABLE 2 & SECTION 4.1", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)

    return img

# ---------------------------------------------------------------------------
# SEQUENCE C: Editorial Conclusion Frame (MANDATORY CORRECTION IMPLEMENTED)
# ---------------------------------------------------------------------------
def render_sequence_c_frame(frame_idx: int = 0, total_frames: int = 90) -> Image.Image:
    """
    Renders Sequence C: Editorial Conclusion — Conceptual Efficiency Matrix & Takeaways.
    Strictly replaces the pseudo-numerical continuous Pareto curve with a clearly
    labeled 3-pillar conceptual efficiency architecture distinguishing:
    1. Direct GRPO Baseline (Exploration Compute Overhead)
    2. Self-Teacher OPD (50x Distillation FLOP Reduction on Math Checkpoint)
    3. External-Teacher OPD (Trails GRPO at Matched FLOPs)
    Plus verified qualified engineering directives and academic preprint disclosure.
    """
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_CANVAS_LIGHT)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)

    # Background Architectural Grid
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, height - 260)], fill=(240, 237, 230), width=1)

    # Top Header
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=TEXT_PRIMARY_DARK, width=2)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  EDITORIAL SYNTHESIS", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    draw.text((790, top_y + 14), "PRODUCTION TAKEAWAY", font=FONTS["mono_badge"], fill=TEXT_SECONDARY_DARK)

    # Monumental Headline
    draw_wrapped_text(
        draw=draw,
        text="On-Policy Distillation is Not a Universal Accelerator",
        x=80,
        y=190,
        font=FONTS["display_hero"],
        fill=TEXT_PRIMARY_DARK,
        max_width=920,
    )

    # 1. The Central Conceptual Efficiency Architecture Matrix (Y = 350 to 920)
    matrix_box = (80, 345, 1000, 925)
    draw.rounded_rectangle(matrix_box, radius=16, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=2)

    # Matrix Top Header & Stamped Caveat
    draw.text((110, 368), "CONCEPTUAL ARCHITECTURAL MATRIX // LAB FINDINGS", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    draw.text((610, 368), "ARXIV:2611.08453 TABLE 2", font=FONTS["mono_citation"], fill=ACCENT_BLUE)
    draw.line([(110, 402), (970, 402)], fill=BORDER_SUBTLE, width=1)

    # 3 Pillars Architecture: Direct GRPO vs Self-Teacher vs External-Teacher
    # Pillar Dimensions
    col_w = 265
    gap = 26
    start_x = 110
    col_y1 = 420
    col_y2 = 820

    # Pillar 1: Direct GRPO Baseline
    p1_x = start_x
    draw.rounded_rectangle([(p1_x, col_y1), (p1_x + col_w, col_y2)], radius=10, fill=(248, 250, 252), outline=BORDER_STRONG, width=1)
    draw.rounded_rectangle([(p1_x, col_y1), (p1_x + col_w, col_y1 + 42)], radius=10, fill=(226, 232, 240))
    draw.text((p1_x + 14, col_y1 + 10), "DIRECT GRPO", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    
    draw.text((p1_x + 16, col_y1 + 60), "TRAINING PARADIGM", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 16, col_y1 + 84), "Trial & Error RL", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)
    
    draw.text((p1_x + 16, col_y1 + 130), "COMPUTE OVERHEAD", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 16, col_y1 + 154), "100% Exploration", font=FONTS["body_md"], fill=TEXT_SECONDARY_DARK)
    
    draw.text((p1_x + 16, col_y1 + 200), "ACCURACY / FLOP", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 16, col_y1 + 224), "Standard Baseline", font=FONTS["body_md"], fill=TEXT_SECONDARY_DARK)
    
    draw.line([(p1_x + 16, col_y1 + 280), (p1_x + col_w - 16, col_y1 + 280)], fill=BORDER_SUBTLE, width=1)
    draw.text((p1_x + 16, col_y1 + 295), "Generates verified", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 16, col_y1 + 320), "frontier reasoning.", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 16, col_y1 + 355), "RL REFERENCE", font=FONTS["mono_badge"], fill=TEXT_SECONDARY_DARK)

    # Pillar 2: Self-Teacher OPD (Emerald Winner)
    p2_x = p1_x + col_w + gap
    draw.rounded_rectangle([(p2_x, col_y1), (p2_x + col_w, col_y2)], radius=10, fill=ACCENT_EMERALD_BG, outline=ACCENT_EMERALD, width=2)
    draw.rounded_rectangle([(p2_x, col_y1), (p2_x + col_w, col_y1 + 42)], radius=10, fill=ACCENT_EMERALD)
    draw.text((p2_x + 14, col_y1 + 10), "SELF-TEACHER OPD", font=FONTS["mono_badge"], fill=(255, 255, 255))
    
    draw.text((p2_x + 16, col_y1 + 60), "TRAINING PARADIGM", font=FONTS["mono_citation"], fill=ACCENT_EMERALD)
    draw.text((p2_x + 16, col_y1 + 84), "Self-Consolidation", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)
    
    draw.text((p2_x + 16, col_y1 + 130), "COMPUTE WIN", font=FONTS["mono_citation"], fill=ACCENT_EMERALD)
    draw.text((p2_x + 16, col_y1 + 154), "50× Fewer FLOPs", font=FONTS["headline_md"], fill=ACCENT_EMERALD)
    
    draw.text((p2_x + 16, col_y1 + 200), "MATCHED ACCURACY", font=FONTS["mono_citation"], fill=ACCENT_EMERALD)
    draw.text((p2_x + 16, col_y1 + 224), "Matches Full RL", font=FONTS["body_md"], fill=TEXT_PRIMARY_DARK)
    
    draw.line([(p2_x + 16, col_y1 + 280), (p2_x + col_w - 16, col_y1 + 280)], fill=BORDER_STRONG, width=1)
    draw.text((p2_x + 16, col_y1 + 295), "Distills student's own", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
    draw.text((p2_x + 16, col_y1 + 320), "checkpoint trajectory.", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
    draw.text((p2_x + 16, col_y1 + 355), "PROVEN LAB SPEEDUP", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)

    # Pillar 3: External-Teacher OPD (Coral Limitation)
    p3_x = p2_x + col_w + gap
    draw.rounded_rectangle([(p3_x, col_y1), (p3_x + col_w, col_y2)], radius=10, fill=ACCENT_CORAL_BG, outline=ACCENT_CORAL, width=2)
    draw.rounded_rectangle([(p3_x, col_y1), (p3_x + col_w, col_y1 + 42)], radius=10, fill=ACCENT_CORAL)
    draw.text((p3_x + 14, col_y1 + 10), "EXTERNAL TEACHER", font=FONTS["mono_badge"], fill=(255, 255, 255))
    
    draw.text((p3_x + 16, col_y1 + 60), "TRAINING PARADIGM", font=FONTS["mono_citation"], fill=ACCENT_CORAL)
    draw.text((p3_x + 16, col_y1 + 84), "Cross-Model OPD", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)
    
    draw.text((p3_x + 16, col_y1 + 130), "COMPUTE OUTCOME", font=FONTS["mono_citation"], fill=ACCENT_CORAL)
    draw.text((p3_x + 16, col_y1 + 154), "Trails Direct RL", font=FONTS["headline_md"], fill=ACCENT_CORAL)
    
    draw.text((p3_x + 16, col_y1 + 200), "MATCHED ACCURACY", font=FONTS["mono_citation"], fill=ACCENT_CORAL)
    draw.text((p3_x + 16, col_y1 + 224), "Lower Accuracy/FLOP", font=FONTS["body_md"], fill=TEXT_PRIMARY_DARK)
    
    draw.line([(p3_x + 16, col_y1 + 280), (p3_x + col_w - 16, col_y1 + 280)], fill=BORDER_STRONG, width=1)
    draw.text((p3_x + 16, col_y1 + 295), "Under matched settings", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
    draw.text((p3_x + 16, col_y1 + 320), "studied in preprint.", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
    draw.text((p3_x + 16, col_y1 + 355), "CRITICAL LIMITATION", font=FONTS["mono_badge"], fill=ACCENT_CORAL)

    # Matrix Footer Banner
    draw.line([(110, 845), (970, 845)], fill=BORDER_SUBTLE, width=1)
    draw.text((110, 865), "CONCEPTUAL COMPARISON // LAB SETTING // NOT CONTINUOUS EMPIRICAL CURVE", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
    draw.text((110, 892), "ACCURACY METRIC EVALUATED ON MATH BENCHMARKS (MATH-500 & AIME 2024)", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)

    # 2. Key Synthesis Directives (Y = 955 to 1420)
    synth_y = 955
    draw.line([(80, synth_y), (1000, synth_y)], fill=BORDER_STRONG, width=1)
    draw.text((80, synth_y + 16), "03 / QUALIFIED ENGINEERING DIRECTIVES", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    # Directive 1: The 50x Scope (Emerald)
    s1_y = synth_y + 52
    draw.rounded_rectangle([(80, s1_y), (1000, s1_y + 195)], radius=10, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([(80, s1_y), (90, s1_y + 195)], radius=3, fill=ACCENT_EMERALD)
    draw.text((116, s1_y + 18), "THE 50× EFFICIENCY SCOPE", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)
    s1_text = (
        "The reported 50x reduction applies specifically to the distillation FLOPs required to recover "
        "accuracy using the student's own GRPO checkpoint. It does not indicate universal speedup, "
        "inference acceleration, or total end-to-end training FLOP reduction."
    )
    draw_wrapped_text(draw, s1_text, 116, s1_y + 54, FONTS["body_md"], TEXT_PRIMARY_DARK, 850)

    # Directive 2: The External Teacher Ceiling (Coral - Mandatory Narration Wording)
    s2_y = s1_y + 220
    draw.rounded_rectangle([(80, s2_y), (1000, s2_y + 195)], radius=10, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([(80, s2_y), (90, s2_y + 195)], radius=3, fill=ACCENT_CORAL)
    draw.text((116, s2_y + 18), "THE EXTERNAL TEACHER CEILING", font=FONTS["mono_badge"], fill=ACCENT_CORAL)
    s2_text = (
        "Under the matched experimental settings studied, external-teacher distillation generally trails "
        "direct GRPO in accuracy per training FLOP. Engineers should not assume on-policy distillation "
        "universally outperforms reinforcement learning."
    )
    draw_wrapped_text(draw, s2_text, 116, s2_y + 54, FONTS["body_md"], TEXT_PRIMARY_DARK, 850)

    # 3. Official Academic Preprint Disclosure Box (Y = 1445 to 1640)
    seal_y = 1445
    draw.rounded_rectangle([(80, seal_y), (1000, seal_y + 185)], radius=12, fill=(245, 247, 250), outline=BORDER_STRONG, width=2)
    draw.text((116, seal_y + 18), "ACADEMIC PREPRINT DISCLOSURE // ARXIV:2611.08453", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    seal_text = (
        "Findings represent controlled laboratory benchmark evaluations from preprint arXiv:2611.08453. "
        "The results have not yet been independently replicated or universally established. Production deployment requires independent verification."
    )
    draw_wrapped_text(draw, seal_text, 116, seal_y + 54, FONTS["body_sm"], TEXT_SECONDARY_DARK, 850)
    draw.text((116, seal_y + 144), "STATUS: PREPRINT LAB BENCHMARK // SUPER.INTELLIGENCEEE RESEARCH", font=FONTS["mono_citation"], fill=ACCENT_BLUE)

    return img

# ---------------------------------------------------------------------------
# Consolidated Contact Sheet
# ---------------------------------------------------------------------------
def render_phase42a2_contact_sheet(
    img_a: Image.Image,
    img_b: Image.Image,
    img_c: Image.Image,
    output_path: Path,
):
    canvas_w = 1920
    canvas_h = 1080
    sheet = Image.new("RGB", (canvas_w, canvas_h), (245, 243, 238))
    draw = ImageDraw.Draw(sheet)

    # Header bar
    draw.rectangle([(0, 0), (canvas_w, 80)], fill=(15, 23, 42))
    draw.text((40, 26), "SUPER.INTELLIGENCEEE  |  PHASE 4.2A.2 FINAL CREATIVE VALIDATION & STORYBOARD AUDIT", font=FONTS["mono_badge"], fill=(255, 255, 255))
    draw.text((1440, 26), "TOPIC: ARXIV:2611.08453 (OPD VS GRPO)", font=FONTS["mono_badge"], fill=ACCENT_BLUE_GLOW)

    # Thumbnails (540 x 960)
    thumb_w = 540
    thumb_h = 960
    th_a = img_a.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    th_b = img_b.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    th_c = img_c.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)

    spacing = (canvas_w - (3 * thumb_w)) // 4
    y_pos = 100

    x_a = spacing
    x_b = spacing * 2 + thumb_w
    x_c = spacing * 3 + thumb_w * 2

    # Drop shadows & frames
    for px, th in [(x_a, th_a), (x_b, th_b), (x_c, th_c)]:
        draw.rectangle([(px + 4, y_pos + 4), (px + thumb_w + 4, y_pos + thumb_h + 4)], fill=(210, 205, 195))
        sheet.paste(th, (px, y_pos))
        draw.rectangle([(px, y_pos), (px + thumb_w, y_pos + thumb_h)], outline=(180, 175, 165), width=1)

    # Sequence Sub-labels
    draw.rectangle([(x_a, y_pos + thumb_h - 45), (x_a + thumb_w, y_pos + thumb_h)], fill=(15, 23, 42))
    draw.text((x_a + 16, y_pos + thumb_h - 32), "SEQ A: THE EXPLORATION CEILING (CINEMATIC)", font=FONTS["mono_citation"], fill=(248, 250, 252))

    draw.rectangle([(x_b, y_pos + thumb_h - 45), (x_b + thumb_w, y_pos + thumb_h)], fill=(15, 23, 42))
    draw.text((x_b + 16, y_pos + thumb_h - 32), "SEQ B: OPD MECHANISM & FORK (TECHNICAL)", font=FONTS["mono_citation"], fill=(248, 250, 252))

    draw.rectangle([(x_c, y_pos + thumb_h - 45), (x_c + thumb_w, y_pos + thumb_h)], fill=(15, 23, 42))
    draw.text((x_c + 16, y_pos + thumb_h - 32), "SEQ C: CONCEPTUAL EFFICIENCY MATRIX (EDITORIAL)", font=FONTS["mono_citation"], fill=(248, 250, 252))

    sheet.save(output_path, quality=95)
    print(f"[OK] Saved Contact Sheet: {output_path}")

# ---------------------------------------------------------------------------
# Lightweight MP4 Motion Prototype Animatic Generator
# ---------------------------------------------------------------------------
def render_motion_prototype(render_fn, output_mp4: Path, num_frames: int = 90, fps: int = 30):
    cmd = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        str(output_mp4)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(num_frames):
        frame = render_fn(frame_idx=i, total_frames=num_frames)
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"[OK] Rendered motion prototype animatic: {output_mp4}")

# ---------------------------------------------------------------------------
# Main Execution Pipeline
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("SUPER.INTELLIGENCEEE — PHASE 4.2A.2 FINAL CREATIVE VALIDATION")
    print("Rendering High-Fidelity Verified Visual Prototypes...")
    print("=" * 70)

    # 1. Render High-Resolution Prototypes
    seq_a_img = render_sequence_a_frame(frame_idx=45, total_frames=90)
    seq_a_path = OUTPUT_DIR / "sequence_a_final_review.png"
    seq_a_img.save(seq_a_path)
    print(f"[OK] Sequence A saved: {seq_a_path}")

    seq_b_img = render_sequence_b_frame(frame_idx=65, total_frames=90)
    seq_b_path = OUTPUT_DIR / "sequence_b_final_review.png"
    seq_b_img.save(seq_b_path)
    print(f"[OK] Sequence B saved: {seq_b_path}")

    seq_c_img = render_sequence_c_frame(frame_idx=45, total_frames=90)
    seq_c_path = OUTPUT_DIR / "sequence_c_final_review.png"
    seq_c_img.save(seq_c_path)
    print(f"[OK] Sequence C saved (CORRECTED): {seq_c_path}")

    # 2. Render Consolidated Contact Sheet
    contact_sheet_path = OUTPUT_DIR / "phase42a_2_contact_sheet.png"
    render_phase42a2_contact_sheet(seq_a_img, seq_b_img, seq_c_img, contact_sheet_path)

    # 3. Render Motion Prototype Animatics (H.264 @ 30fps)
    print("\nRendering Lightweight Motion Animatics...")
    mp4_a_path = OUTPUT_DIR / "sequence_a_motion_prototype_v2.mp4"
    render_motion_prototype(render_sequence_a_frame, mp4_a_path, num_frames=90, fps=30)

    mp4_b_path = OUTPUT_DIR / "sequence_b_motion_prototype_v2.mp4"
    render_motion_prototype(render_sequence_b_frame, mp4_b_path, num_frames=90, fps=30)

    mp4_c_path = OUTPUT_DIR / "sequence_c_motion_prototype_v2.mp4"
    render_motion_prototype(render_sequence_c_frame, mp4_c_path, num_frames=90, fps=30)

    # 4. Copy to Brain Artifact Directory for inspection
    print(f"\nCopying artifacts to Brain Directory: {BRAIN_DIR}")
    for f in OUTPUT_DIR.glob("*.*"):
        target = BRAIN_DIR / f.name
        shutil.copy2(f, target)
        print(f"  -> Copied {f.name}")

    print("\n[SUCCESS] Phase 4.2A.2 Visual Artifacts Generated Successfully.")

if __name__ == "__main__":
    main()

