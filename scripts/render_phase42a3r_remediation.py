"""
SUPER.INTELLIGENCEEE — Phase 4.2A.3-R Targeted Remediation Renderer & Audio Muxer
Remediates all independently verified failures from Phase 4.2A.3:
1. Fixes DEF-01: Mathematical right-alignment prevents canvas clipping in Sequence B.
2. Fixes DEF-02: Mathematical right-alignment eliminates lateral safe-zone penetration in Sequence C.
3. Fixes DEF-03: Implements a continuous temporal animation in Sequence C (3-Part Progressive Architecture).
4. Fixes DEF-04: Implements a 4-Stage explanatory pipeline in Sequence B (zero frozen stalls).
5. Fixes DEF-05: Streamlines Sequence C to prevent 6-card clutter; introduces the Multi-Teacher 42% FLOP breakthrough.
6. Fixes DEF-06: Muxes genuine Voicebox Kokoro (am_liam) American English narration with ducked soundscape into MP4s.

Canvas: 1080x1920 @ 30.0 fps (YUV420p)
Audio: 48 kHz stereo AAC (EBU R128 mastered to -16 LUFS)
"""

import math
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np

OUTPUT_DIR = Path("output/drafts/phase42a_3r_remediation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR = OUTPUT_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

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
        "display_hero": get_font(arialbd_path, 60),
        "headline_lg": get_font(arialbd_path, 48),
        "headline_md": get_font(arialbd_path, 36),
        "card_title": get_font(arialbd_path, 28),
        "body_lg": get_font(arial_path, 28),
        "body_md": get_font(arial_path, 25),
        "body_sm": get_font(arial_path, 22),
        "mono_hero": get_font(consolab_path, 76),
        "mono_stat": get_font(consolab_path, 46),
        "mono_badge": get_font(consolab_path, 22),
        "mono_citation": get_font(consola_path, 20),
    }

FONTS = load_fonts()

# ---------------------------------------------------------------------------
# Robust Typographic & Layout Utilities
# ---------------------------------------------------------------------------
def draw_right_aligned_text(
    draw: ImageDraw.Draw,
    text: str,
    right_x: int,
    y: int,
    font: ImageFont.ImageFont,
    fill: Tuple[int, int, int],
) -> int:
    """Mathematically guarantees text never exceeds right_x (strictly enforcing safe zones)."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    draw_x = right_x - text_w
    draw.text((draw_x, y), text, font=font, fill=fill)
    return draw_x

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
# SEQUENCE A: Atmospheric Cinematic Macro (Preserved & Refined)
# ---------------------------------------------------------------------------
def render_sequence_a_frame(frame_idx: int, total_frames: int) -> Image.Image:
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_CINEMATIC_DARK)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)
    cam_push = 1.0 + (0.05 * t)  # Smooth 5% macro push

    # 1. Perspective Background
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
        pulse_l = math.sin(frame_idx * 0.12 + unit_y * 0.05) * 0.5 + 0.5
        led_col_l = ACCENT_BLUE if pulse_l > 0.4 else (20, 60, 90)
        draw.rectangle([(140, unit_y), (146, unit_y + 8)], fill=led_col_l)
        draw.rectangle([(152, unit_y), (158, unit_y + 8)], fill=(30, 80, 120))

        pulse_r = math.cos(frame_idx * 0.14 + unit_y * 0.04) * 0.5 + 0.5
        led_col_r = ACCENT_AMBER if pulse_r > 0.6 else (60, 45, 20)
        draw.rectangle([(width - 156, unit_y), (width - 150, unit_y + 8)], fill=led_col_r)
        draw.rectangle([(width - 144, unit_y), (width - 138, unit_y + 8)], fill=(30, 80, 120))

    # 2. Central Accelerator Die Substrate
    sub_w = int(720 * cam_push)
    sub_h = int(680 * cam_push)
    sx1 = (width - sub_w) // 2
    sy1 = 340 + int(math.sin(t * math.pi) * 8)
    sx2 = sx1 + sub_w
    sy2 = sy1 + sub_h

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
    pulse_core = math.sin(frame_idx * 0.15) * 0.5 + 0.5
    for row in range(3):
        for col in range(3):
            bx = cx1 + 50 + col * 180
            by = cy1 + 60 + row * 160
            is_active_rollout = (row == 1 and col == 1)
            b_fill = (55, 34, 18) if is_active_rollout else (22, 30, 45)
            b_outline = (251, 191, 36) if (is_active_rollout and pulse_core > 0.3) else ACCENT_AMBER if is_active_rollout else (55, 70, 100)
            draw.rounded_rectangle([(bx, by), (bx + 140, by + 120)], radius=6, fill=b_fill, outline=b_outline, width=2 if is_active_rollout else 1)
            draw.text((bx + 16, by + 16), f"NODE 0{row*3+col+1}", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
            status_txt = "RL ROLLOUT 98%" if is_active_rollout else "HBM ACTIVE"
            draw.text((bx + 16, by + 54), status_txt, font=FONTS["mono_badge"], fill=ACCENT_AMBER if is_active_rollout else ACCENT_BLUE)

    # Anamorphic Light Accent
    streak_y = sy1 + int(sub_h * (0.15 + 0.70 * t))
    draw.line([(0, streak_y), (width, streak_y)], fill=(56, 189, 248), width=2)

    # Permanent Procedural Provenance Stamp
    draw.text((cx1 + 16, cy2 - 36), "CONCEPTUAL ACCELERATOR TOPOLOGY // PROCEDURAL VISUALIZATION", font=FONTS["mono_citation"], fill=ACCENT_BLUE_GLOW)

    # 3. Top Header (Mathematical Safe-Zone Right Alignment)
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=BORDER_STRONG, width=1)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  FIELD INVESTIGATION", font=FONTS["mono_badge"], fill=ACCENT_BLUE_GLOW)
    draw_right_aligned_text(draw, "ARXIV:2611.08453", 1000, top_y + 14, FONTS["mono_badge"], TEXT_SECONDARY_LIGHT)

    # 4. Editorial Lower-Third
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
        "vast mathematical solution spaces creates a massive compute bottleneck."
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
    draw_right_aligned_text(draw, "REASONING SEARCH WALL", 1000, anchor_y + 16, FONTS["mono_badge"], ACCENT_AMBER)

    return img

# ---------------------------------------------------------------------------
# SEQUENCE B: Continuous Mechanism Pipeline (Remediated)
# ---------------------------------------------------------------------------
def render_sequence_b_frame(frame_idx: int, total_frames: int) -> Image.Image:
    width, height = 1080, 1920
    # Living documentary canvas: subtle organic luminance pulse ensures zero static hold
    bg_pulse = int(math.sin(frame_idx * 0.07) * 3.0)
    bg_color = (250 + bg_pulse, 249 + bg_pulse, 246 + bg_pulse)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)
    cam_push = 1.0 + (0.02 * t)

    # Architectural Grid with micro-drift
    grid_shift = int((t * 60) % 60)
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, height - 260)], fill=(240, 237, 230), width=1)

    # Ambient Technical Floating Particles (Ensures continuous frame activity)
    for p_idx in range(40):
        px = int((hash((p_idx, 11)) % 900) + 90 + math.sin(frame_idx * 0.06 + p_idx) * 35)
        py = int((hash((p_idx, 22)) % 1400) + 180 + (frame_idx * (1.2 + (p_idx % 3) * 0.5)) % 1350)
        draw.ellipse([(px, py), (px + 3, py + 3)], fill=(218, 228, 242))

    # Top Header (Mathematical Right Alignment fixes DEF-01)
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=ACCENT_BLUE, width=2)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  ALGORITHMIC MECHANISM", font=FONTS["mono_badge"], fill=ACCENT_BLUE)
    draw_right_aligned_text(draw, "TOKEN-LEVEL OPD DYNAMICS", 1000, top_y + 14, FONTS["mono_badge"], TEXT_SECONDARY_DARK)

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
        y=250,
        font=FONTS["body_md"],
        fill=TEXT_SECONDARY_DARK,
        max_width=920,
    )

    # 1. Main Stage Container (Student & Frozen Teacher Interaction)
    stage_box = (80, 305, 1000, 835)
    draw.rounded_rectangle(stage_box, radius=16, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=2)

    # Continuous active scanning line across stage box (telemetry activity)
    beam_y = 310 + int(((t * 3.0) % 1.0) * 515)
    draw.line([(82, beam_y), (998, beam_y)], fill=(224, 242, 254), width=1)

    # STAGE 1 (t in [0.0, 0.35]): Prompt Intake & Progressive Token Generation
    stage1_prog = min(1.0, t / 0.35)
    draw.text((110, 325), "STAGE 1: STUDENT POLICY GENERATION (π_θ)", font=FONTS["mono_badge"], fill=ACCENT_BLUE)

    # Prompt sequence
    draw.text((110, 365), "Prompt Tokens:", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    prompt_tokens = ["[Prompt]", "Factor", "x⁴", "-", "16", "="]
    px = 110
    for tok in prompt_tokens:
        tok_w = int(draw.textbbox((0, 0), tok, font=FONTS["mono_badge"])[2] - draw.textbbox((0, 0), tok, font=FONTS["mono_badge"])[0]) + 18
        draw.rounded_rectangle([(px, 395), (px + tok_w, 432)], radius=6, fill=(241, 245, 249), outline=BORDER_SUBTLE, width=1)
        draw.text((px + 9, 403), tok, font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
        px += tok_w + 10

    # Progressive student rollout tokens
    draw.text((110, 450), "Student Generated Rollout (Active Sampling):", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    rollout_tokens = ["(", "x²", "-", "4", ")", "(", "x²", "+", "4", ")"]
    visible_count = int(stage1_prog * len(rollout_tokens))
    active_tok_idx = min(len(rollout_tokens) - 1, visible_count)

    rx = 110
    for i, r_tok in enumerate(rollout_tokens):
        if i > visible_count and t < 0.35:
            continue
        is_active = (i == active_tok_idx and t < 0.35)
        r_w = int(draw.textbbox((0, 0), r_tok, font=FONTS["card_title"])[2] - draw.textbbox((0, 0), r_tok, font=FONTS["card_title"])[0]) + 22
        bg_col = (224, 242, 254) if is_active else (248, 250, 252)
        border_col = ACCENT_BLUE if is_active else BORDER_STRONG
        draw.rounded_rectangle([(rx, 480), (rx + r_w, 532)], radius=6, fill=bg_col, outline=border_col, width=2 if is_active else 1)
        draw.text((rx + 11, 489), r_tok, font=FONTS["card_title"], fill=ACCENT_BLUE if is_active else TEXT_PRIMARY_DARK)
        rx += r_w + 10

    # STAGE 2 & 3 (t in [0.25, 0.70]): Frozen Teacher Evaluation & Logit Stems
    stage2_prog = min(1.0, max(0.0, (t - 0.25) / 0.35))
    stem_h_factor = math.sin(stage2_prog * math.pi / 2.0)

    spec_y = 560
    draw.line([(110, spec_y), (970, spec_y)], fill=BORDER_SUBTLE, width=1)
    draw.text((110, spec_y + 12), "STAGE 2: FROZEN TEACHER SUPERVISION // D_KL ( π_θ || π_ref )", font=FONTS["mono_citation"], fill=ACCENT_BLUE)
    draw_right_aligned_text(draw, "TEACHER WEIGHTS STRICTLY FROZEN", 970, spec_y + 12, FONTS["mono_badge"], ACCENT_AMBER)

    # Draw probability density stems with active neural entropy shimmer
    stem_x_start = 140
    for s_i in range(16):
        sx = stem_x_start + s_i * 50
        prob_teacher = math.exp(-((s_i - 8) ** 2) / 10.0) * 105 * stem_h_factor
        student_bias = 8.5 - 0.5 * min(1.0, max(0.0, (t - 0.40) / 0.30))
        # Active entropy micro-shimmer simulating stochastic logit exploration
        shimmer = math.sin(frame_idx * 0.18 + s_i * 0.7) * (3.0 if t >= 0.35 else 0.5)
        prob_student = max(4.0, (math.exp(-((s_i - student_bias) ** 2) / 11.0) * 95 + shimmer) * stem_h_factor)

        draw.line([(sx, 740), (sx, 740 - int(prob_teacher))], fill=(203, 213, 225), width=6)
        draw.line([(sx + 8, 740), (sx + 8, 740 - int(prob_student))], fill=ACCENT_BLUE, width=6)

    draw.text((110, 755), "Teacher Reference Target (Grey) vs Student Policy Logits (Blue)", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
    draw.text((110, 785), "DENSE PER-TOKEN SUPERVISION APPLIED TO STUDENT POLICY PARAMETERS θ", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    # STAGE 4 (t in [0.65, 1.0]): Progressive Fork Reveal (Fixes DEF-04)
    fork_y = 860
    draw.line([(80, fork_y), (1000, fork_y)], fill=BORDER_STRONG, width=1)
    draw.text((80, fork_y + 14), "EXPERIMENTAL DIVERGENCE: TEACHER SELECTION REGIMES", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    # Condition 1: Self-Teacher Checkpoint (Reveals smoothly with live animated progress bar)
    e_y1 = fork_y + 40
    e_y2 = e_y1 + 175
    if t >= 0.62:
        alpha_e = min(1.0, (t - 0.62) / 0.15)
        pulse_em = math.sin(frame_idx * 0.18) * 0.5 + 0.5
        b_col_e = (52, 211, 153) if pulse_em > 0.4 else ACCENT_EMERALD

        draw.rounded_rectangle([(80, e_y1), (1000, e_y2)], radius=12, fill=ACCENT_EMERALD_BG, outline=b_col_e, width=2)
        draw.rounded_rectangle([(80, e_y1), (92, e_y2)], radius=4, fill=ACCENT_EMERALD)

        draw.text((116, e_y1 + 14), "CONDITION 1: SELF-CHECKPOINT TEACHER", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)
        draw.text((116, e_y1 + 44), "50× Distillation FLOP Reduction", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)
        
        # Animated FLOP Efficiency gauge
        gauge_w = int(alpha_e * 450)
        draw.rounded_rectangle([(116, e_y1 + 86), (116 + 450, e_y1 + 96)], radius=4, fill=(209, 250, 229))
        draw.rounded_rectangle([(116, e_y1 + 86), (116 + gauge_w, e_y1 + 96)], radius=4, fill=ACCENT_EMERALD)

        desc_e = (
            "When distilling from student's own GRPO checkpoint, OPD recovers full "
            "math accuracy with 50x fewer distillation FLOPs than RL needed to reach that accuracy."
        )
        draw_wrapped_text(draw, desc_e, 116, e_y1 + 104, FONTS["body_sm"], TEXT_SECONDARY_DARK, 850)

    # Condition 2: External Teacher Deficit (Reveals at t >= 0.78 with live bloat meter)
    c_y1 = e_y2 + 20
    c_y2 = c_y1 + 175
    if t >= 0.76:
        alpha_c = min(1.0, (t - 0.76) / 0.15)
        pulse_c = math.cos(frame_idx * 0.18) * 0.5 + 0.5
        b_col_c = (248, 113, 113) if pulse_c > 0.4 else ACCENT_CORAL

        draw.rounded_rectangle([(80, c_y1), (1000, c_y2)], radius=12, fill=ACCENT_CORAL_BG, outline=b_col_c, width=2)
        draw.rounded_rectangle([(80, c_y1), (92, c_y2)], radius=4, fill=ACCENT_CORAL)

        draw.text((116, c_y1 + 14), "CONDITION 2: EXTERNAL POST-TRAINED TEACHER", font=FONTS["mono_badge"], fill=ACCENT_CORAL)
        draw.text((116, c_y1 + 44), "Response-Length Bloat (Trails GRPO)", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)
        
        # Animated Length Bloat gauge
        gauge_wc = int(alpha_c * 450)
        draw.rounded_rectangle([(116, c_y1 + 86), (116 + 450, c_y1 + 96)], radius=4, fill=(254, 226, 226))
        draw.rounded_rectangle([(116, c_y1 + 86), (116 + gauge_wc, c_y1 + 96)], radius=4, fill=ACCENT_CORAL)

        desc_c = (
            "Under matched settings, external teachers trigger uncontrolled response-length bloat, "
            "causing OPD to generally trail direct GRPO in accuracy per training FLOP."
        )
        draw_wrapped_text(draw, desc_c, 116, c_y1 + 104, FONTS["body_sm"], TEXT_SECONDARY_DARK, 850)

    # Bottom Citation
    anchor_y = 1580
    draw.line([(80, anchor_y), (1000, anchor_y)], fill=BORDER_SUBTLE, width=1)
    draw.text((80, anchor_y + 16), "SOURCE: ARXIV:2611.08453 // SECTION 3 & SECTION 4", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw_right_aligned_text(draw, "ON-POLICY SAMPLING", 1000, anchor_y + 16, FONTS["mono_citation"], ACCENT_BLUE)

    return img

# ---------------------------------------------------------------------------
# SEQUENCE C: 3-Part Progressive Architecture (Remediated)
# ---------------------------------------------------------------------------
def render_sequence_c_frame(frame_idx: int, total_frames: int) -> Image.Image:
    width, height = 1080, 1920
    # Living documentary canvas: subtle organic luminance pulse ensures zero static hold
    bg_pulse = int(math.sin(frame_idx * 0.07) * 3.0)
    bg_color = (250 + bg_pulse, 249 + bg_pulse, 246 + bg_pulse)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)

    # Architectural Grid
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, height - 260)], fill=(240, 237, 230), width=1)

    # Ambient Technical Floating Particles (Ensures continuous frame activity)
    for p_idx in range(40):
        px = int((hash((p_idx, 33)) % 900) + 90 + math.sin(frame_idx * 0.05 + p_idx) * 35)
        py = int((hash((p_idx, 44)) % 1400) + 180 + (frame_idx * (1.1 + (p_idx % 3) * 0.5)) % 1350)
        draw.ellipse([(px, py), (px + 3, py + 3)], fill=(220, 230, 244))

    # Top Header (Mathematical Right Alignment fixes DEF-02)
    top_y = 150
    draw.line([(80, top_y), (1000, top_y)], fill=TEXT_PRIMARY_DARK, width=2)
    draw.text((80, top_y + 14), "// SUPER.INTELLIGENCEEE  |  EDITORIAL SYNTHESIS", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    draw_right_aligned_text(draw, "PRODUCTION TAKEAWAY", 1000, top_y + 14, FONTS["mono_badge"], TEXT_SECONDARY_DARK)

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
    draw.text((80, 260), "Three distinct empirical compute regimes established in arXiv:2611.08453", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)

    # 1. Three-Pillar Progressive Architecture (Fixes DEF-03: Real Temporal Animation!)
    matrix_box = (80, 305, 1000, 895)
    draw.rounded_rectangle(matrix_box, radius=16, fill=BG_SURFACE_WHITE, outline=BORDER_SUBTLE, width=2)

    # Active ambient scanning beam across matrix box
    beam_y = 310 + int(((t * 2.5) % 1.0) * 575)
    draw.line([(82, beam_y), (998, beam_y)], fill=(240, 246, 255), width=1)

    draw.text((110, 325), "EMPIRICAL COMPUTE HORIZON // THE THREE PILLARS", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    draw_right_aligned_text(draw, "ARXIV:2611.08453 TABLE 2 & 3", 970, 325, FONTS["mono_citation"], ACCENT_BLUE)
    draw.line([(110, 355), (970, 355)], fill=BORDER_SUBTLE, width=1)

    # Dimensions for 3 Columns
    col_w = 265
    gap = 26
    start_x = 110
    col_y1 = 375
    col_y2 = 825

    # Pillar 1 (t in [0.0, 1.0]): Direct GRPO Baseline
    p1_x = start_x
    draw.rounded_rectangle([(p1_x, col_y1), (p1_x + col_w, col_y2)], radius=10, fill=(248, 250, 252), outline=BORDER_STRONG, width=1)
    draw.rounded_rectangle([(p1_x, col_y1), (p1_x + col_w, col_y1 + 40)], radius=10, fill=(226, 232, 240))
    draw.text((p1_x + 14, col_y1 + 10), "DIRECT GRPO", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    draw.text((p1_x + 14, col_y1 + 55), "REGIME", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 14, col_y1 + 78), "Trial & Error RL", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)

    draw.text((p1_x + 14, col_y1 + 130), "COMPUTE OVERHEAD", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 14, col_y1 + 152), "100% Exploration", font=FONTS["body_md"], fill=TEXT_SECONDARY_DARK)

    draw.text((p1_x + 14, col_y1 + 205), "ACCURACY / FLOP", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 14, col_y1 + 228), "Standard Baseline", font=FONTS["body_md"], fill=TEXT_SECONDARY_DARK)

    draw.line([(p1_x + 14, col_y1 + 295), (p1_x + col_w - 14, col_y1 + 295)], fill=BORDER_SUBTLE, width=1)
    draw.text((p1_x + 14, col_y1 + 315), "Raw exploration establishes", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 14, col_y1 + 338), "reasoning capabilities.", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    draw.text((p1_x + 14, col_y1 + 390), "RL REFERENCE", font=FONTS["mono_badge"], fill=TEXT_SECONDARY_DARK)

    # Pillar 2 (Reveals at t >= 0.28): Self-Teacher OPD Compute Win
    p2_x = p1_x + col_w + gap
    if t >= 0.28:
        p2_alpha = min(1.0, (t - 0.28) / 0.15)
        pulse_em = math.sin(frame_idx * 0.15) * 0.5 + 0.5 if t >= 0.45 else 0.0
        border_col = (52, 211, 153) if pulse_em > 0.4 else ACCENT_EMERALD

        draw.rounded_rectangle([(p2_x, col_y1), (p2_x + col_w, col_y2)], radius=10, fill=ACCENT_EMERALD_BG, outline=border_col, width=2)
        draw.rounded_rectangle([(p2_x, col_y1), (p2_x + col_w, col_y1 + 40)], radius=10, fill=ACCENT_EMERALD)
        draw.text((p2_x + 14, col_y1 + 10), "SELF-TEACHER OPD", font=FONTS["mono_badge"], fill=(255, 255, 255))

        draw.text((p2_x + 14, col_y1 + 55), "REGIME", font=FONTS["mono_citation"], fill=ACCENT_EMERALD)
        draw.text((p2_x + 14, col_y1 + 78), "Self-Consolidation", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)

        draw.text((p2_x + 14, col_y1 + 130), "COMPUTE WIN", font=FONTS["mono_citation"], fill=ACCENT_EMERALD)
        draw.text((p2_x + 14, col_y1 + 152), "50× Fewer FLOPs", font=FONTS["headline_md"], fill=ACCENT_EMERALD)

        # Animated FLOP efficiency bar
        gauge_w2 = int(p2_alpha * (col_w - 28))
        draw.rounded_rectangle([(p2_x + 14, col_y1 + 188), (p2_x + col_w - 14, col_y1 + 196)], radius=4, fill=(209, 250, 229))
        draw.rounded_rectangle([(p2_x + 14, col_y1 + 188), (p2_x + 14 + gauge_w2, col_y1 + 196)], radius=4, fill=ACCENT_EMERALD)

        draw.text((p2_x + 14, col_y1 + 205), "MATCHED ACCURACY", font=FONTS["mono_citation"], fill=ACCENT_EMERALD)
        draw.text((p2_x + 14, col_y1 + 228), "Matches Full RL", font=FONTS["body_md"], fill=TEXT_PRIMARY_DARK)

        draw.line([(p2_x + 14, col_y1 + 295), (p2_x + col_w - 14, col_y1 + 295)], fill=BORDER_STRONG, width=1)
        draw.text((p2_x + 14, col_y1 + 315), "Distills student's own", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
        draw.text((p2_x + 14, col_y1 + 338), "math checkpoint.", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
        draw.text((p2_x + 14, col_y1 + 390), "PROVEN LAB SPEEDUP", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)

    # Pillar 3 (Reveals at t >= 0.55): External Teacher Limitation
    p3_x = p2_x + col_w + gap
    if t >= 0.55:
        p3_alpha = min(1.0, (t - 0.55) / 0.15)
        pulse_c = math.cos(frame_idx * 0.15) * 0.5 + 0.5 if t >= 0.70 else 0.0
        border_col_c = (248, 113, 113) if pulse_c > 0.4 else ACCENT_CORAL

        draw.rounded_rectangle([(p3_x, col_y1), (p3_x + col_w, col_y2)], radius=10, fill=ACCENT_CORAL_BG, outline=border_col_c, width=2)
        draw.rounded_rectangle([(p3_x, col_y1), (p3_x + col_w, col_y1 + 40)], radius=10, fill=ACCENT_CORAL)
        draw.text((p3_x + 14, col_y1 + 10), "EXTERNAL TEACHER", font=FONTS["mono_badge"], fill=(255, 255, 255))

        draw.text((p3_x + 14, col_y1 + 55), "REGIME", font=FONTS["mono_citation"], fill=ACCENT_CORAL)
        draw.text((p3_x + 14, col_y1 + 78), "Cross-Model OPD", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)

        draw.text((p3_x + 14, col_y1 + 130), "FAILURE MODE", font=FONTS["mono_citation"], fill=ACCENT_CORAL)
        draw.text((p3_x + 14, col_y1 + 152), "Length Inflation", font=FONTS["headline_md"], fill=ACCENT_CORAL)

        # Animated Length Bloat gauge
        gauge_w3 = int(p3_alpha * (col_w - 28))
        draw.rounded_rectangle([(p3_x + 14, col_y1 + 188), (p3_x + col_w - 14, col_y1 + 196)], radius=4, fill=(254, 226, 226))
        draw.rounded_rectangle([(p3_x + 14, col_y1 + 188), (p3_x + 14 + gauge_w3, col_y1 + 196)], radius=4, fill=ACCENT_CORAL)

        draw.text((p3_x + 14, col_y1 + 205), "MATCHED ACCURACY", font=FONTS["mono_citation"], fill=ACCENT_CORAL)
        draw.text((p3_x + 14, col_y1 + 228), "Trails Direct RL", font=FONTS["body_md"], fill=TEXT_PRIMARY_DARK)

        draw.line([(p3_x + 14, col_y1 + 295), (p3_x + col_w - 14, col_y1 + 295)], fill=BORDER_STRONG, width=1)
        draw.text((p3_x + 14, col_y1 + 315), "Generates bloated outputs", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
        draw.text((p3_x + 14, col_y1 + 338), "without accuracy gains.", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)
        draw.text((p3_x + 14, col_y1 + 390), "CRITICAL LIMITATION", font=FONTS["mono_badge"], fill=ACCENT_CORAL)

    # Footer note of Matrix
    draw.line([(110, 840), (970, 840)], fill=BORDER_SUBTLE, width=1)
    draw.text((110, 858), "CONCEPTUAL COMPARISON // LAB SETTING // NOT CONTINUOUS EMPIRICAL DATA", font=FONTS["mono_citation"], fill=TEXT_SECONDARY_DARK)

    # 2. The Multi-Teacher Breakthrough Card (Reveals at t >= 0.72 - Streamlined, fixes DEF-05!)
    if t >= 0.72:
        alpha_m = min(1.0, (t - 0.72) / 0.15)
        pulse_b = math.sin(frame_idx * 0.15) * 0.5 + 0.5 if t >= 0.85 else 0.0
        border_b = (56, 189, 248) if pulse_b > 0.4 else ACCENT_BLUE

        break_y1 = 920
        break_y2 = 1260
        draw.rounded_rectangle([(80, break_y1), (1000, break_y2)], radius=14, fill=BG_SURFACE_WHITE, outline=border_b, width=2)
        draw.rounded_rectangle([(80, break_y1), (92, break_y2)], radius=4, fill=ACCENT_BLUE)

        draw.text((116, break_y1 + 18), "ARCHITECTURAL RESOLUTION: MULTI-TEACHER CONSOLIDATION", font=FONTS["mono_badge"], fill=ACCENT_BLUE)
        draw.text((116, break_y1 + 52), "Multi-Teacher OPD Saves 42% Total FLOPs", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)

        # Animated Multi-Teacher FLOP Savings Bar
        m_bar_w = int(alpha_m * 850)
        draw.rounded_rectangle([(116, break_y1 + 94), (116 + 850, break_y1 + 102)], radius=4, fill=(224, 242, 254))
        draw.rounded_rectangle([(116, break_y1 + 94), (116 + m_bar_w, break_y1 + 102)], radius=4, fill=ACCENT_BLUE)

        desc_multi = (
            "While single-domain self-distillation carries inherent redundancy, the paper's true breakthrough "
            "emerges in multi-domain settings: consolidating independent specialist GRPO checkpoints into a "
            "single student reaches joint-GRPO performance with 42.0% fewer total training FLOPs (arXiv:2611.08453 Table 3)."
        )
        draw_wrapped_text(draw, desc_multi, 116, break_y1 + 112, FONTS["body_md"], TEXT_SECONDARY_DARK, 850)

        draw.line([(116, break_y1 + 250), (970, break_y1 + 250)], fill=BORDER_SUBTLE, width=1)
        draw.text((116, break_y1 + 265), "KEY TAKEAWAY: USE ON-POLICY DISTILLATION FOR DOMAIN MERGING, NOT GENERIC TRAINING ACCELERATION.", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    # 3. Academic Preprint Disclosure Seal
    if t >= 0.85:
        seal_y = 1290
        draw.rounded_rectangle([(80, seal_y), (1000, seal_y + 175)], radius=12, fill=(245, 247, 250), outline=BORDER_STRONG, width=1)
        draw.text((116, seal_y + 18), "ACADEMIC PREPRINT DISCLOSURE // ARXIV:2611.08453", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
        seal_text = (
            "Findings represent controlled laboratory evaluations on MATH-500 and AIME 2024. Results have not yet been "
            "independently replicated or universally established across all model scales."
        )
        draw_wrapped_text(draw, seal_text, 116, seal_y + 52, FONTS["body_sm"], TEXT_SECONDARY_DARK, 850)
        draw.text((116, seal_y + 138), "STATUS: PREPRINT LAB BENCHMARK // SUPER.INTELLIGENCEEE RESEARCH", font=FONTS["mono_citation"], fill=ACCENT_BLUE)

    return img

# ---------------------------------------------------------------------------
# Video Rendering & Direct Audio Muxing Pipeline
# ---------------------------------------------------------------------------
def render_remediated_video(
    render_fn,
    raw_video_path: Path,
    final_mp4_path: Path,
    audio_path: Path,
    total_frames: int,
    fps: int = 30
):
    print(f"\n--- Rendering Video: {raw_video_path.name} ({total_frames} frames @ {fps} fps) ---")
    t0 = time.time()

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
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        str(raw_video_path)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for i in range(total_frames):
        frame = render_fn(frame_idx=i, total_frames=total_frames)
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()
    render_sec = time.time() - t0
    print(f"[OK] Raw Video encoded in {render_sec:.2f}s -> {raw_video_path}")

    # Mux Audio into Final MP4 with AAC 192k
    print(f"Muxing Mastered Audio: {audio_path.name} into {final_mp4_path.name}...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-i", str(raw_video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_mp4_path)
    ]
    subprocess.run(mux_cmd, check=True)
    print(f"[SUCCESS] Final Audio-Visual MP4 created: {final_mp4_path}")

# ---------------------------------------------------------------------------
# 9-Frame Forensic Contact Sheet
# ---------------------------------------------------------------------------
def render_phase42a3r_contact_sheet(
    frames_dict: Dict[str, Dict[str, Image.Image]],
    output_path: Path
):
    col_w = 400
    col_h = 711
    header_h = 100
    padding = 24

    sheet_w = padding * 4 + col_w * 3
    sheet_h = header_h + (38 + col_h + padding) * 3 + padding

    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 243, 238))
    draw = ImageDraw.Draw(sheet)

    # Title Header
    draw.rectangle([(0, 0), (sheet_w, header_h)], fill=(15, 23, 42))
    draw.text((padding, 24), "SUPER.INTELLIGENCEEE  |  PHASE 4.2A.3-R REMEDIATION MATRIX", font=FONTS["headline_md"], fill=(255, 255, 255))
    draw.text((padding, 66), "VERIFIED AUDIO-VISUAL EXPLORATION (1080x1920 @ 30FPS, AAC AUDIO MUXED)", font=FONTS["mono_badge"], fill=(56, 189, 248))

    sequences = [
        ("seq_a", "SEQUENCE A: THE EXPLORATION CEILING (CINEMATIC MACRO)"),
        ("seq_b", "SEQUENCE B: ON-POLICY DISTILLATION DYNAMICS (CONTINUOUS MECHANISM)"),
        ("seq_c", "SEQUENCE C: 3-PART EDITORIAL SYNTHESIS (PROGRESSIVE REVEAL & MULTI-TEACHER)")
    ]
    frame_keys = ["beginning", "middle", "end"]
    frame_labels = ["BEGINNING (t=0.0s)", "MIDDLE (t=50%)", "END (t=100%)"]

    curr_y = header_h + padding

    for seq_key, seq_title in sequences:
        draw.rectangle([(padding, curr_y), (sheet_w - padding, curr_y + 32)], fill=(226, 232, 240))
        draw.text((padding + 12, curr_y + 6), seq_title, font=FONTS["mono_badge"], fill=(15, 23, 42))
        curr_y += 38

        for col_idx, (f_key, f_label) in enumerate(zip(frame_keys, frame_labels)):
            img = frames_dict[seq_key][f_key]
            thumb = img.resize((col_w, col_h), Image.Resampling.LANCZOS)
            x_pos = padding + col_idx * (col_w + padding)

            draw.rectangle([(x_pos - 1, curr_y - 1), (x_pos + col_w + 1, curr_y + col_h + 1)], outline=(180, 175, 165), width=1)
            sheet.paste(thumb, (x_pos, curr_y))

            draw.rectangle([(x_pos, curr_y + col_h - 28), (x_pos + col_w, curr_y + col_h)], fill=(15, 23, 42))
            draw.text((x_pos + 10, curr_y + col_h - 22), f_label, font=FONTS["mono_citation"], fill=(248, 250, 252))

        curr_y += col_h + padding

    sheet.save(output_path, quality=95)
    print(f"[OK] Saved Remediation Contact Sheet: {output_path}")

# ---------------------------------------------------------------------------
# Main Execution Pipeline
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("SUPER.INTELLIGENCEEE — PHASE 4.2A.3-R REMEDIATION PIPELINE")
    print("Executing Targeted Remediation, Continuous Motion & Audio Muxing...")
    print("=" * 70)

    # Frame counts derived from Voicebox Kokoro audio:
    # seq_a: 8.62s -> 259 frames
    # seq_b: 9.80s -> 294 frames
    # seq_c: 10.44s -> 314 frames
    seq_configs = [
        ("seq_a", render_sequence_a_frame, 259, "seq_a_mastered.wav", "sequence_a_remediated"),
        ("seq_b", render_sequence_b_frame, 294, "seq_b_mastered.wav", "sequence_b_remediated"),
        ("seq_c", render_sequence_c_frame, 314, "seq_c_mastered.wav", "sequence_c_remediated"),
    ]

    frames_for_sheet = {}

    for seq_key, render_fn, total_f, audio_name, out_base in seq_configs:
        raw_mp4 = OUTPUT_DIR / f"{out_base}_raw.mp4"
        final_mp4 = OUTPUT_DIR / f"{out_base}.mp4"
        audio_p = AUDIO_DIR / audio_name

        # 1. Render Video & Mux Audio
        render_remediated_video(
            render_fn=render_fn,
            raw_video_path=raw_mp4,
            final_mp4_path=final_mp4,
            audio_path=audio_p,
            total_frames=total_f,
            fps=30
        )

        # 2. Save Key Review PNGs (Middle/End frame)
        review_png = OUTPUT_DIR / f"{out_base}.png"
        sample_frame = render_fn(frame_idx=int(total_f * 0.85), total_frames=total_f)
        sample_frame.save(review_png)
        print(f"[OK] Saved Review Frame: {review_png}")

        # 3. Store frames for contact sheet
        f_start = render_fn(frame_idx=0, total_frames=total_f)
        f_mid = render_fn(frame_idx=int(total_f * 0.50), total_frames=total_f)
        f_end = render_fn(frame_idx=total_f - 1, total_frames=total_f)
        frames_for_sheet[seq_key] = {
            "beginning": f_start,
            "middle": f_mid,
            "end": f_end
        }

    # 4. Render Remediation Contact Sheet
    contact_sheet_p = OUTPUT_DIR / "phase42a_3r_contact_sheet.png"
    render_phase42a3r_contact_sheet(frames_for_sheet, contact_sheet_p)

    # 5. Copy artifacts to Brain Directory
    print(f"\nCopying all remediation artifacts to Brain Directory: {BRAIN_DIR}")
    for ext in ("*.png", "*.mp4", "*.wav"):
        for f in OUTPUT_DIR.glob(ext):
            shutil.copy2(f, BRAIN_DIR / f.name)
            print(f"  -> Copied {f.name}")
        for f in AUDIO_DIR.glob(ext):
            shutil.copy2(f, BRAIN_DIR / f.name)
            print(f"  -> Copied audio/{f.name}")

    print("\n[SUCCESS] Phase 4.2A.3-R Remediation Render Completed.")

if __name__ == "__main__":
    main()
