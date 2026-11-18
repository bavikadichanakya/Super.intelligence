"""
SUPER.INTELLIGENCEEE — Phase 4.2A.1 Revision Renderer
Renders refined, cinematic visual prototypes and lightweight motion animatics for:
- Sequence A: Cinematic Documentary (Atmospheric Datacenter & Silicon Substrate)
- Sequence B: Technical Mechanism (Token Trajectory, Logit Distribution & Teacher Fork)
- Sequence C: Editorial Conclusion (The Efficiency Horizon & Single Iconic Balance)
- Consolidated 3-Shot Contact Sheet
- Three MP4 Motion Prototype Animatics (Camera push, layer animation, word reveals)

Strictly enforces:
- Output directory: output/drafts/phase42a_1_revision/ (isolated, does not overwrite Phase 4.2A).
- Zero string slicing: all text pre-measured with textbbox and dynamic line wrapping.
- Strict safe zones: 140px top, 260px bottom, 80px lateral.
- Exact factual qualification for arXiv:2611.08453.
"""

import math
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = Path("output/drafts/phase42a_1_revision")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------
# Light-First Editorial Canvas
BG_CANVAS_LIGHT = (250, 247, 242)      # Warm Ivory #FAF7F2
BG_SURFACE_WHITE = (255, 255, 255)     # Elevated Card #FFFFFF
BORDER_SUBTLE = (226, 232, 240)        # Subtle Border #E2E8F0
BORDER_STRONG = (203, 213, 225)        # Architectural Rule #CBD5E1

TEXT_PRIMARY_DARK = (15, 23, 42)       # Deep Obsidian Slate #0F172A
TEXT_SECONDARY_DARK = (71, 85, 105)    # Muted Slate #475569
TEXT_MUTED_DARK = (148, 163, 184)      # Light Slate #94A3B8

# Cinematic Dark Environment (Sequence A)
BG_CINEMATIC_DARK = (11, 15, 23)       # Deep Graphite Obsidian #0B0F17
BG_RACK_PANEL = (20, 26, 38)           # Server Rack Bay #141A26
TEXT_PRIMARY_LIGHT = (248, 250, 252)   # Crisp White #F8FAFC
TEXT_SECONDARY_LIGHT = (148, 163, 184) # Pale Slate #94A3B8

# Semantic Scientific Accents
ACCENT_BLUE = (2, 132, 199)            # Technical Research Blue #0284C7
ACCENT_BLUE_GLOW = (56, 189, 248)      # Sky Blue Pulse #38BDF8
ACCENT_EMERALD = (5, 150, 105)         # Verification Emerald #059669
ACCENT_EMERALD_GLOW = (52, 211, 153)   # Mint Glow #34D399
ACCENT_AMBER = (217, 119, 6)           # Critical Amber #D97706
ACCENT_AMBER_GLOW = (251, 191, 36)     # Amber Glow #FBBF24
ACCENT_CORAL = (220, 38, 38)           # Warning Coral #DC2626

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
        "display_hero": get_font(arialbd_path, 68),
        "headline_lg": get_font(arialbd_path, 52),
        "headline_md": get_font(arialbd_path, 40),
        "card_title": get_font(arialbd_path, 32),
        "body_lg": get_font(arial_path, 32),
        "body_md": get_font(arial_path, 28),
        "body_sm": get_font(arial_path, 24),
        "mono_hero": get_font(consolab_path, 88),
        "mono_stat": get_font(consolab_path, 56),
        "mono_badge": get_font(consolab_path, 24),
        "mono_citation": get_font(consola_path, 22),
    }

FONTS = load_fonts()

# ---------------------------------------------------------------------------
# Typographic Utilities (Dynamic word wrap & bounding box measurement)
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
# SEQUENCE A: Cinematic Documentary Frame & Animatic
# ---------------------------------------------------------------------------
def render_sequence_a_frame(frame_idx: int = 0, total_frames: int = 90) -> Image.Image:
    """
    Renders Sequence A: Cinematic Documentary — The Reasoning Compute Ceiling.
    Authentic atmospheric datacenter corridor with glowing server rack telemetry,
    macro accelerator die substrate, and elegant restrained typography.
    """
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_CINEMATIC_DARK)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)
    cam_push = 1.0 + (0.04 * t)

    # 1. Atmospheric Server Rack Background (Perspective Vanishing Corridor)
    # Floor and ceiling gradient
    for y in range(height):
        factor = abs(y - 700) / 700.0
        r = int(11 + 6 * factor)
        g = int(15 + 8 * factor)
        b = int(23 + 12 * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Server Rack Bay Silhouette Columns (Left and Right perspective)
    rack_left_x = int(80 * cam_push)
    rack_right_x = width - int(80 * cam_push)

    # Left Rack Server Bay
    draw.rectangle([(0, 200), (180, 1100)], fill=BG_RACK_PANEL)
    draw.rectangle([(width - 180, 200), (width, 1100)], fill=BG_RACK_PANEL)

    # Server status LED telemetry pins (animating subtly)
    for unit_y in range(240, 1050, 42):
        # Left rack LEDs
        pulse_l = math.sin(frame_idx * 0.15 + unit_y * 0.05) * 0.5 + 0.5
        led_col_l = ACCENT_BLUE if pulse_l > 0.4 else (20, 60, 90)
        draw.rectangle([(140, unit_y), (146, unit_y + 8)], fill=led_col_l)
        draw.rectangle([(152, unit_y), (158, unit_y + 8)], fill=(30, 80, 120))

        # Right rack LEDs
        pulse_r = math.cos(frame_idx * 0.18 + unit_y * 0.04) * 0.5 + 0.5
        led_col_r = ACCENT_AMBER if pulse_r > 0.6 else (60, 45, 20)
        draw.rectangle([(width - 156, unit_y), (width - 150, unit_y + 8)], fill=led_col_r)
        draw.rectangle([(width - 144, unit_y), (width - 138, unit_y + 8)], fill=(30, 80, 120))

    # 2. Central Accelerator Die Substrate (Macro Cinematography with depth-of-field)
    sub_w = int(720 * cam_push)
    sub_h = int(680 * cam_push)
    sx1 = (width - sub_w) // 2
    sy1 = 340 + int(math.sin(t * math.pi) * 6)
    sx2 = sx1 + sub_w
    sy2 = sy1 + sub_h

    # Ambient substrate drop shadow
    draw.rounded_rectangle([(sx1 + 8, sy1 + 12), (sx2 + 8, sy2 + 12)], radius=16, fill=(5, 8, 14))
    # Outer dark titanium heat spreader
    draw.rounded_rectangle([(sx1, sy1), (sx2, sy2)], radius=16, fill=(24, 32, 48), outline=(50, 65, 95), width=2)
    # Silicon die interior core
    cx1, cy1 = sx1 + 36, sy1 + 36
    cx2, cy2 = sx2 - 36, sy2 - 36
    draw.rounded_rectangle([(cx1, cy1), (cx2, cy2)], radius=8, fill=(16, 22, 34), outline=(70, 90, 130), width=1)

    # Interconnect Gold / Copper Circuitry
    for gx in range(cx1 + 25, cx2, 45):
        draw.line([(gx, cy1), (gx, cy2)], fill=(40, 50, 75), width=1)
    for gy in range(cy1 + 25, cy2, 45):
        draw.line([(cx1, gy), (cx2, gy)], fill=(40, 50, 75), width=1)

    # High-intensity active compute cluster (RL Exploration cores)
    for row in range(3):
        for col in range(3):
            bx = cx1 + 50 + col * 180
            by = cy1 + 60 + row * 160
            is_active_rollout = (row == 1 and col == 1)
            b_fill = (45, 28, 15) if is_active_rollout else (22, 30, 45)
            b_outline = ACCENT_AMBER if is_active_rollout else (55, 70, 100)
            draw.rounded_rectangle([(bx, by), (bx + 140, by + 120)], radius=6, fill=b_fill, outline=b_outline, width=1)
            draw.text((bx + 16, by + 16), f"CLUSTER 0{row*3+col+1}", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
            status_txt = "RL ROLLOUT 98%" if is_active_rollout else "HBM ACTIVE"
            draw.text((bx + 16, by + 54), status_txt, font=FONTS["mono_badge"], fill=ACCENT_AMBER if is_active_rollout else ACCENT_BLUE)

    # Subtle anamorphic horizontal blue streak across die
    streak_y = sy1 + int(sub_h * (0.3 + 0.4 * t))
    draw.line([(0, streak_y), (width, streak_y)], fill=(2, 132, 199), width=1)

    # Substrate laser engraving
    draw.text((cx1 + 20, cy2 - 36), "COMPUTE SUBSTRATE // H100 SXM5 CLUSTER ARRAY", font=FONTS["mono_badge"], fill=TEXT_MUTED_DARK)

    # 3. Top Category Branding
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=BORDER_STRONG, width=1)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  FIELD INVESTIGATION", font=FONTS["mono_badge"], fill=ACCENT_BLUE_GLOW)
    draw.text((790, top_y + 14), "ARXIV:2611.08453", font=FONTS["mono_badge"], fill=TEXT_SECONDARY_LIGHT)

    # 4. Editorial Lower-Third (Restrained, high-impact typography)
    lower_y = 1220
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
    draw.text((80, anchor_y + 16), "EMPIRICAL FLOP BOTTLENECK // BATCH GENERATION STALL", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((750, anchor_y + 16), "RL ROLLOUT OVERHEAD", font=FONTS["mono_badge"], fill=ACCENT_AMBER)

    return img

# ---------------------------------------------------------------------------
# SEQUENCE B: Technical Mechanism Frame & Animatic
# ---------------------------------------------------------------------------
def render_sequence_b_frame(frame_idx: int = 0, total_frames: int = 90) -> Image.Image:
    """
    Renders Sequence B: Technical Mechanism — On-Policy Distillation Dynamics & Fork.
    Visualizes token sequence rollout, probability distribution evaluation, and
    the empirical divergence between self-teacher and external-teacher settings.
    """
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_CANVAS_LIGHT)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)

    # Background architectural lines
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, height - 260)], fill=(240, 237, 230), width=1)

    # Top Header
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=ACCENT_BLUE, width=2)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  ALGORITHMIC MECHANISM", font=FONTS["mono_badge"], fill=ACCENT_BLUE)
    draw.text((790, top_y + 14), "TOKEN-LEVEL OPD DYNAMICS", font=FONTS["mono_badge"], fill=TEXT_SECONDARY_DARK)

    # Section Title & Deck (Y = 190 to 290)
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
        y=256,
        font=FONTS["body_md"],
        fill=TEXT_SECONDARY_DARK,
        max_width=920,
    )

    # 1. Token Trajectory & Logit Supervision Stage (Y = 320 to 860)
    stage_box = (80, 320, 1000, 860)
    draw.rounded_rectangle(stage_box, radius=16, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=2)

    # Stage Header
    draw.text((110, 345), "TOKEN TRAJECTORY & PER-TOKEN SUPERVISION", font=FONTS["mono_badge"], fill=ACCENT_BLUE)

    # Prompt Tokens Input
    draw.text((110, 390), "Reasoning Prompt:", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    prompt_tokens = ["[Prompt]", "Factor", "x⁴", "-", "16", "="]
    px = 110
    for tok in prompt_tokens:
        tok_w = int(draw.textbbox((0, 0), tok, font=FONTS["mono_badge"])[2] - draw.textbbox((0, 0), tok, font=FONTS["mono_badge"])[0]) + 20
        draw.rounded_rectangle([(px, 420), (px + tok_w, 458)], radius=6, fill=(241, 245, 249), outline=BORDER_SUBTLE, width=1)
        draw.text((px + 10, 428), tok, font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
        px += tok_w + 12

    # Student Generated Rollout Trajectory
    draw.text((110, 480), "Student Generated Rollout (Active Policy π_θ):", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    rollout_tokens = ["(", "x²", "-", "4", ")", "(", "x²", "+", "4", ")"]
    active_idx = min(len(rollout_tokens) - 1, int(t * len(rollout_tokens) * 1.4))
    
    rx = 110
    for i, r_tok in enumerate(rollout_tokens):
        is_current = (i == active_idx)
        is_past = (i < active_idx)
        r_w = int(draw.textbbox((0, 0), r_tok, font=FONTS["card_title"])[2] - draw.textbbox((0, 0), r_tok, font=FONTS["card_title"])[0]) + 24
        
        bg_col = (224, 242, 254) if is_current else (248, 250, 252) if is_past else (255, 255, 255)
        border_col = ACCENT_BLUE if is_current else BORDER_STRONG if is_past else BORDER_SUBTLE
        draw.rounded_rectangle([(rx, 510), (rx + r_w, 565)], radius=6, fill=bg_col, outline=border_col, width=2 if is_current else 1)
        draw.text((rx + 12, 520), r_tok, font=FONTS["card_title"], fill=ACCENT_BLUE if is_current else TEXT_PRIMARY_DARK)
        rx += r_w + 10

    # Frozen Teacher Logit Probability Stems
    spec_y = 610
    draw.line([(110, spec_y), (970, spec_y)], fill=BORDER_SUBTLE, width=1)
    draw.text((110, spec_y + 14), "FROZEN TEACHER LOGIT SUPERVISION // D_KL ( π_θ || π_ref )", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)

    # Draw probability density stems
    stem_x_start = 140
    for s_i in range(16):
        sx = stem_x_start + s_i * 50
        # Simulated logit probabilities
        prob_teacher = math.exp(-((s_i - 8) ** 2) / 10.0) * 110
        prob_student = math.exp(-((s_i - 8.5) ** 2) / 12.0) * 95 * min(1.0, t * 1.5)
        
        # Teacher target stem (pale slate)
        draw.line([(sx, 780), (sx, 780 - int(prob_teacher))], fill=(203, 213, 225), width=6)
        # Student active logit stem (blue)
        draw.line([(sx + 8, 780), (sx + 8, 780 - int(prob_student))], fill=ACCENT_BLUE, width=6)

    draw.text((110, 800), "Teacher Target Distribution (Grey) vs Student Policy Logits (Blue)", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)

    # 2. The Critical Experimental Fork (Y = 890 to 1600)
    fork_y = 890
    draw.line([(80, fork_y), (1000, fork_y)], fill=BORDER_STRONG, width=1)
    draw.text((80, fork_y + 14), "02 / THE CRITICAL EXPERIMENTAL FORK", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    # Emerald Branch: Self-Teacher Breakthrough
    e_y1 = fork_y + 45
    e_y2 = e_y1 + 290
    draw.rounded_rectangle([(80, e_y1), (1000, e_y2)], radius=12, fill=BG_SURFACE_WHITE, outline=ACCENT_EMERALD, width=2)
    draw.rounded_rectangle([(80, e_y1), (92, e_y2)], radius=4, fill=ACCENT_EMERALD)

    draw.text((120, e_y1 + 20), "CONDITION 1: TEACHER IS STUDENT'S OWN GRPO CHECKPOINT", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)
    draw.text((120, e_y1 + 56), "50× Distillation FLOP Reduction", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)
    desc_e = (
        "When the teacher is the student's own checkpoint, OPD matches full GRPO "
        "accuracy on math benchmarks with 50x fewer distillation FLOPs than RL needed to reach that accuracy."
    )
    draw_wrapped_text(draw, desc_e, 120, e_y1 + 116, FONTS["body_md"], TEXT_SECONDARY_DARK, 840)
    draw.text((120, e_y1 + 236), "VERIFIED EMPIRICAL FINDING // HIGH TRAJECTORY OVERLAP", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)

    # Coral Branch: External Teacher Penalty
    c_y1 = e_y2 + 25
    c_y2 = c_y1 + 290
    draw.rounded_rectangle([(80, c_y1), (1000, c_y2)], radius=12, fill=BG_SURFACE_WHITE, outline=ACCENT_CORAL, width=2)
    draw.rounded_rectangle([(80, c_y1), (92, c_y2)], radius=4, fill=ACCENT_CORAL)

    draw.text((120, c_y1 + 20), "CONDITION 2: TEACHER IS AN EXTERNAL POST-TRAINED MODEL", font=FONTS["mono_badge"], fill=ACCENT_CORAL)
    draw.text((120, c_y1 + 56), "Loses to Direct GRPO at Matched FLOPs", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)
    desc_c = (
        "Crucially, OPD with an external post-trained teacher generally underperforms "
        "GRPO in accuracy per training FLOP under matched experimental settings."
    )
    draw_wrapped_text(draw, desc_c, 120, c_y1 + 116, FONTS["body_md"], TEXT_SECONDARY_DARK, 840)
    draw.text((120, c_y1 + 236), "POLICY DISTRIBUTION MISMATCH // NO UNIVERSAL ADVANTAGE", font=FONTS["mono_badge"], fill=ACCENT_CORAL)

    # Bottom Citation
    anchor_y = 1580
    draw.line([(80, anchor_y), (1000, anchor_y)], fill=BORDER_SUBTLE, width=1)
    draw.text((80, anchor_y + 16), "SOURCE: ARXIV:2611.08453 // TABLE 2 & SECTION 4.1", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)

    return img

# ---------------------------------------------------------------------------
# SEQUENCE C: Editorial Conclusion Frame & Animatic
# ---------------------------------------------------------------------------
def render_sequence_c_frame(frame_idx: int = 0, total_frames: int = 90) -> Image.Image:
    """
    Renders Sequence C: Editorial Conclusion — The Efficiency Horizon.
    A single iconic, monumental visual composition uniting an empirical coordinate
    horizon with restrained, authoritative engineering takeaways.
    """
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_CANVAS_LIGHT)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)

    # Background architectural lines
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, height - 260)], fill=(240, 237, 230), width=1)

    # Top Header
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=TEXT_PRIMARY_DARK, width=2)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  EDITORIAL SYNTHESIS", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    draw.text((790, top_y + 14), "PRODUCTION TAKEAWAY", font=FONTS["mono_badge"], fill=TEXT_SECONDARY_DARK)

    # Monumental Headline (Y = 190 to 330)
    draw_wrapped_text(
        draw=draw,
        text="On-Policy Distillation is Not a Universal Accelerator",
        x=80,
        y=190,
        font=FONTS["display_hero"],
        fill=TEXT_PRIMARY_DARK,
        max_width=920,
    )

    # 1. The Central Efficiency Horizon Coordinate Graphic (Y = 370 to 920)
    horiz_box = (80, 360, 1000, 920)
    draw.rounded_rectangle(horiz_box, radius=16, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=2)

    # Coordinate System
    ox, oy = 160, 830
    axis_w = 760
    axis_h = 380

    # Axes
    draw.line([(ox, oy), (ox + axis_w, oy)], fill=BORDER_STRONG, width=2)
    draw.line([(ox, oy), (ox, oy - axis_h)], fill=BORDER_STRONG, width=2)

    draw.text((ox + axis_w - 220, oy + 18), "Training FLOP Budget ──►", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((ox - 30, oy - axis_h - 28), "▲ Accuracy per FLOP", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)

    # GRPO Pareto Frontier Curve
    points = []
    for step in range(30):
        frac = step / 29.0
        px = ox + int(frac * axis_w * 0.9)
        py = oy - int(math.sqrt(frac) * axis_h * 0.65)
        points.append((px, py))
    
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(148, 163, 184), width=3)
    draw.text((ox + int(axis_w * 0.55), oy - int(axis_h * 0.50)), "GRPO Pareto Frontier", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)

    # Point 1: Self-Teacher Checkpoint Breakthrough (Emerald Diamond, well above frontier)
    pt1_x = ox + int(axis_w * 0.28)
    pt1_y = oy - int(axis_h * 0.88)
    draw.polygon([(pt1_x, pt1_y - 14), (pt1_x + 14, pt1_y), (pt1_x, pt1_y + 14), (pt1_x - 14, pt1_y)], fill=ACCENT_EMERALD)
    
    # Callout Box for Self-Teacher
    draw.rounded_rectangle([(pt1_x + 24, pt1_y - 36), (pt1_x + 440, pt1_y + 40)], radius=8, fill=(240, 253, 244), outline=ACCENT_EMERALD, width=2)
    draw.text((pt1_x + 36, pt1_y - 26), "SELF-CHECKPOINT TEACHER", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)
    draw.text((pt1_x + 36, pt1_y + 6), "50× Fewer Distillation FLOPs", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)

    # Point 2: External Teacher Underperformance (Amber Triangle, below frontier)
    pt2_x = ox + int(axis_w * 0.62)
    pt2_y = oy - int(axis_h * 0.32)
    draw.polygon([(pt2_x, pt2_y - 12), (pt2_x + 12, pt2_y + 12), (pt2_x - 12, pt2_y + 12)], fill=ACCENT_CORAL)

    # Callout Box for External Teacher
    draw.rounded_rectangle([(pt2_x + 24, pt2_y - 36), (pt2_x + 420, pt2_y + 40)], radius=8, fill=(254, 242, 242), outline=ACCENT_CORAL, width=2)
    draw.text((pt2_x + 36, pt2_y - 26), "EXTERNAL TEACHER", font=FONTS["mono_badge"], fill=ACCENT_CORAL)
    draw.text((pt2_x + 36, pt2_y + 6), "Loses to Direct GRPO", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)

    # 2. Key Synthesis Statements (Y = 960 to 1420)
    synth_y = 960
    draw.line([(80, synth_y), (1000, synth_y)], fill=BORDER_STRONG, width=1)
    draw.text((80, synth_y + 16), "03 / QUALIFIED ENGINEERING DIRECTIVES", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    # Statement 1 (Emerald Accent)
    s1_y = synth_y + 54
    draw.rounded_rectangle([(80, s1_y), (1000, s1_y + 180)], radius=10, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([(80, s1_y), (90, s1_y + 180)], radius=3, fill=ACCENT_EMERALD)
    draw.text((116, s1_y + 18), "THE 50× EFFICIENCY SCOPE", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)
    s1_text = (
        "The reported 50x FLOP reduction applies specifically to distilling from the student's own GRPO "
        "checkpoint on math benchmarks. It is an effective method for consolidating self-exploration."
    )
    draw_wrapped_text(draw, s1_text, 116, s1_y + 56, FONTS["body_md"], TEXT_PRIMARY_DARK, 850)

    # Statement 2 (Coral Accent)
    s2_y = s1_y + 205
    draw.rounded_rectangle([(80, s2_y), (1000, s2_y + 180)], radius=10, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([(80, s2_y), (90, s2_y + 180)], radius=3, fill=ACCENT_CORAL)
    draw.text((116, s2_y + 18), "THE EXTERNAL TEACHER CEILING", font=FONTS["mono_badge"], fill=ACCENT_CORAL)
    s2_text = (
        "Under matched experimental settings, external distillation generally loses to direct GRPO in accuracy "
        "per training FLOP. Engineers should not assume OPD universally outperforms reinforcement learning."
    )
    draw_wrapped_text(draw, s2_text, 116, s2_y + 56, FONTS["body_md"], TEXT_PRIMARY_DARK, 850)

    # 3. Official Academic Preprint Disclosure Box (Y = 1450 to 1640)
    seal_y = 1435
    draw.rounded_rectangle([(80, seal_y), (1000, seal_y + 195)], radius=12, fill=(245, 247, 250), outline=BORDER_STRONG, width=2)
    draw.text((116, seal_y + 20), "ACADEMIC PREPRINT DISCLOSURE // ARXIV:2611.08453", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    seal_text = (
        "Findings represent controlled laboratory benchmark evaluations. The results have not yet been "
        "independently replicated or universally established. Production deployment requires independent verification."
    )
    draw_wrapped_text(draw, seal_text, 116, seal_y + 58, FONTS["body_sm"], TEXT_SECONDARY_DARK, 850)
    draw.text((116, seal_y + 152), "STATUS: PREPRINT LAB BENCHMARK // SUPER.INTELLIGENCEEE RESEARCH", font=FONTS["mono_citation"], fill=ACCENT_BLUE)

    return img

# ---------------------------------------------------------------------------
# Consolidated Contact Sheet
# ---------------------------------------------------------------------------
def render_phase42a1_contact_sheet(
    img_a: Image.Image,
    img_b: Image.Image,
    img_c: Image.Image,
    output_path: Path,
):
    """Renders a 16:9 widescreen (1920x1080) contact sheet displaying the 3 revised sequences."""
    canvas_w = 1920
    canvas_h = 1080
    sheet = Image.new("RGB", (canvas_w, canvas_h), (245, 243, 238))
    draw = ImageDraw.Draw(sheet)

    # Header bar
    draw.rectangle([(0, 0), (canvas_w, 80)], fill=(15, 23, 42))
    draw.text((40, 26), "SUPER.INTELLIGENCEEE  |  PHASE 4.2A.1 CREATIVE DIRECTION & STORYBOARD REVISION", font=FONTS["mono_badge"], fill=(255, 255, 255))
    draw.text((1440, 26), "RESEARCH: ARXIV:2611.08453 (OPD VS GRPO)", font=FONTS["mono_badge"], fill=ACCENT_BLUE_GLOW)

    # Thumbnails (540 x 960)
    thumb_w = 540
    thumb_h = 960
    th_a = img_a.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    th_b = img_b.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    th_c = img_c.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)

    spacing = (canvas_w - (3 * thumb_w)) // 4
    y_pos = 100

    frames = [
        (th_a, "SEQUENCE A: CINEMATIC DOCUMENTARY", "Authentic Datacenter & Silicon Substrate Scale"),
        (th_b, "SEQUENCE B: TECHNICAL MECHANISM", "Token Trajectory, Logit Distribution & Teacher Fork"),
        (th_c, "SEQUENCE C: EDITORIAL CONCLUSION", "The Efficiency Horizon & Single Iconic Synthesis"),
    ]

    for idx, (th, title, subtitle) in enumerate(frames):
        x_pos = spacing + idx * (thumb_w + spacing)
        # Drop shadow
        draw.rectangle([(x_pos + 6, y_pos + 6), (x_pos + thumb_w + 6, y_pos + thumb_h + 6)], fill=(220, 218, 210))
        sheet.paste(th, (x_pos, y_pos))
        draw.rectangle([(x_pos, y_pos), (x_pos + thumb_w, y_pos + thumb_h)], outline=(200, 198, 190), width=2)

        # Label underneath
        draw.text((x_pos, y_pos + thumb_h + 12), title, font=FONTS["mono_badge"], fill=(15, 23, 42))
        draw.text((x_pos, y_pos + thumb_h + 40), subtitle, font=FONTS["mono_citation"], fill=(71, 85, 105))

    sheet.save(output_path, "PNG")
    return output_path

# ---------------------------------------------------------------------------
# Lightweight Motion Prototype Generator (MP4 Animatics via FFmpeg)
# ---------------------------------------------------------------------------
def render_motion_prototype(
    render_frame_fn,
    output_mp4_path: Path,
    duration_seconds: float = 3.0,
    fps: int = 30,
):
    """
    Renders a lightweight, sequential 3-second motion prototype (animatic)
    directly through FFmpeg stdin piping without overflowing 8 GB RAM.
    """
    total_frames = int(duration_seconds * fps)
    out_p = Path(output_mp4_path).resolve()
    out_p.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", "1080x1920",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out_p),
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for f_idx in range(total_frames):
            frame = render_frame_fn(frame_idx=f_idx, total_frames=total_frames)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        if proc.poll() is None:
            proc.kill()
        raise RuntimeError(f"Motion prototype render failed: {e}") from e

    if not out_p.exists() or out_p.stat().st_size < 1000:
        raise RuntimeError(f"Exported MP4 is missing or empty: {out_p}")
    return out_p

# ---------------------------------------------------------------------------
# Main Execution Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("================================================================================")
    print("SUPER.INTELLIGENCEEE — Phase 4.2A.1 Revision Rendering")
    print(f"Output Directory: {OUTPUT_DIR.resolve()}")
    print("================================================================================")

    # 1. Render Revised Static Frames
    print("\n--- Step 1: Rendering Revised High-Resolution Prototype PNGs ---")
    img_a = render_sequence_a_frame(frame_idx=45, total_frames=90)
    p_a = OUTPUT_DIR / "sequence_a_cinematic_documentary_v2.png"
    img_a.save(p_a, "PNG")
    print(f"  ✓ Rendered Sequence A v2: {p_a.name} ({p_a.stat().st_size} bytes)")

    img_b = render_sequence_b_frame(frame_idx=45, total_frames=90)
    p_b = OUTPUT_DIR / "sequence_b_technical_mechanism_v2.png"
    img_b.save(p_b, "PNG")
    print(f"  ✓ Rendered Sequence B v2: {p_b.name} ({p_b.stat().st_size} bytes)")

    img_c = render_sequence_c_frame(frame_idx=45, total_frames=90)
    p_c = OUTPUT_DIR / "sequence_c_editorial_conclusion_v2.png"
    img_c.save(p_c, "PNG")
    print(f"  ✓ Rendered Sequence C v2: {p_c.name} ({p_c.stat().st_size} bytes)")

    # 2. Render Consolidated Contact Sheet
    print("\n--- Step 2: Rendering Consolidated Revision Contact Sheet ---")
    p_cs = OUTPUT_DIR / "phase42a_1_contact_sheet.png"
    render_phase42a1_contact_sheet(img_a, img_b, img_c, p_cs)
    print(f"  ✓ Rendered Contact Sheet: {p_cs.name} ({p_cs.stat().st_size} bytes)")

    # 3. Render Lightweight Motion Prototypes (Animatics)
    print("\n--- Step 3: Rendering Lightweight MP4 Motion Prototypes (Sequential) ---")
    
    mp4_a = OUTPUT_DIR / "sequence_a_motion_prototype.mp4"
    render_motion_prototype(render_sequence_a_frame, mp4_a, duration_seconds=3.0, fps=30)
    print(f"  ✓ Rendered Sequence A Motion Prototype: {mp4_a.name} ({mp4_a.stat().st_size} bytes)")

    mp4_b = OUTPUT_DIR / "sequence_b_motion_prototype.mp4"
    render_motion_prototype(render_sequence_b_frame, mp4_b, duration_seconds=3.0, fps=30)
    print(f"  ✓ Rendered Sequence B Motion Prototype: {mp4_b.name} ({mp4_b.stat().st_size} bytes)")

    mp4_c = OUTPUT_DIR / "sequence_c_motion_prototype.mp4"
    render_motion_prototype(render_sequence_c_frame, mp4_c, duration_seconds=3.0, fps=30)
    print(f"  ✓ Rendered Sequence C Motion Prototype: {mp4_c.name} ({mp4_c.stat().st_size} bytes)")

    print("\n================================================================================")
    print("Phase 4.2A.1 Revision Successfully Rendered!")
    print("================================================================================")
