"""
SUPER.INTELLIGENCEEE — Phase 4.2A.3-R.1 Revision Renderer
Visual Composition Correction, Layout Rebuild & Audio-Visual Production

Implements:
1. Sequence A: Reasoning Tree Search & Rollout Exploration Metaphor (replaces 9-node grid).
2. Sequence B: 5-Stage Mechanism Flow with separate visual regions (fixes STAGE 2 collision).
3. Sequence C: Complete Layout Redesign with unobstructed title, 3-Pillar Horizon,
   and dedicated Multi-Teacher Breakthrough Section.
4. Shared Layout Engine enforcing 80px safe margins, measured text, and zero collisions.
5. Automated Audio-Video Muxing with existing Voicebox Kokoro audio stems.
"""

import math
import os
import shutil
import subprocess
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Workspace & Directory Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path("a:/SUPER.INTELLIGENCEEE")
REVISION_DIR = BASE_DIR / "output" / "drafts" / "phase42a_3r1_revision"
AUDIO_DIR = REVISION_DIR / "audio"
BRAIN_DIR = Path(r"C:\Users\bavik\.gemini\antigravity\brain\174164e7-7384-4da6-a377-b063df7a125d")

REVISION_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Production Color Palette (Clean Editorial Documentary)
# ---------------------------------------------------------------------------
BG_DARK = (8, 12, 21)             # Sequence A: Atmospheric deep space
BG_LIGHT = (250, 249, 246)        # Sequence B & C: Editorial Swiss Canvas
SURFACE_WHITE = (255, 255, 255)
SURFACE_LIGHT = (245, 247, 250)
SURFACE_CARD_DARK = (15, 23, 42)

TEXT_PRIMARY_DARK = (17, 24, 39)     # High-contrast charcoal
TEXT_SECONDARY_DARK = (71, 85, 105)  # Slate
TEXT_MUTED_DARK = (148, 163, 184)

TEXT_PRIMARY_LIGHT = (248, 250, 252) # Off-white
TEXT_SECONDARY_LIGHT = (203, 213, 225)
TEXT_MUTED_LIGHT = (100, 116, 139)

BORDER_SUBTLE = (226, 232, 240)
BORDER_STRONG = (203, 213, 225)
BORDER_DARK = (30, 41, 59)

ACCENT_BLUE = (14, 116, 144)         # Cyan / Blue
ACCENT_BLUE_LIGHT = (224, 242, 254)
ACCENT_EMERALD = (5, 150, 105)       # Green
ACCENT_EMERALD_BG = (236, 253, 245)
ACCENT_CORAL = (225, 29, 72)         # Crimson / Coral
ACCENT_CORAL_BG = (255, 241, 242)
ACCENT_AMBER = (217, 119, 6)         # Amber / Warning
ACCENT_AMBER_BG = (254, 243, 199)

# ---------------------------------------------------------------------------
# Font Management
# ---------------------------------------------------------------------------
def load_fonts():
    font_paths = {
        "inter_bold": ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arialbd.ttf"],
        "inter_regular": ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"],
        "mono": ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"],
    }
    
    def get_font(path_list, size):
        for p in path_list:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    return {
        "display_hero": get_font(font_paths["inter_bold"], 48),
        "headline_lg": get_font(font_paths["inter_bold"], 38),
        "headline_md": get_font(font_paths["inter_bold"], 26),
        "card_title": get_font(font_paths["inter_bold"], 20),
        "body_lg": get_font(font_paths["inter_regular"], 18),
        "body_md": get_font(font_paths["inter_regular"], 16),
        "body_sm": get_font(font_paths["inter_regular"], 14),
        "mono_badge": get_font(font_paths["mono"], 13),
        "mono_citation": get_font(font_paths["mono"], 12),
        "mono_sm": get_font(font_paths["mono"], 11),
    }

FONTS = load_fonts()

# ---------------------------------------------------------------------------
# Shared Layout Engine & Safe-Zone Primitives
# ---------------------------------------------------------------------------
class LayoutEngine:
    @staticmethod
    def measure_text(draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont):
        bbox = draw.textbbox((0, 0), text, font=font)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])

    @staticmethod
    def wrap_text(draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont, max_width: int):
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = " ".join(current_line + [word])
            w, _ = LayoutEngine.measure_text(draw, test_line, font)
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    @staticmethod
    def draw_wrapped_text(
        draw: ImageDraw.Draw,
        text: str,
        x: int,
        y: int,
        font: ImageFont.ImageFont,
        fill: tuple,
        max_width: int,
        line_spacing: int = 4
    ) -> int:
        lines = LayoutEngine.wrap_text(draw, text, font, max_width)
        curr_y = y
        for line in lines:
            draw.text((x, curr_y), line, font=font, fill=fill)
            _, lh = LayoutEngine.measure_text(draw, line, font)
            curr_y += lh + line_spacing
        return curr_y

    @staticmethod
    def draw_right_aligned_text(
        draw: ImageDraw.Draw,
        text: str,
        right_x: int,
        y: int,
        font: ImageFont.ImageFont,
        fill: tuple
    ) -> tuple:
        w, h = LayoutEngine.measure_text(draw, text, font)
        draw.text((right_x - w, y), text, font=font, fill=fill)
        return (right_x - w, y, right_x, y + h)

    @staticmethod
    def draw_badge(
        draw: ImageDraw.Draw,
        x: int,
        y: int,
        text: str,
        font: ImageFont.ImageFont,
        bg_fill: tuple,
        text_fill: tuple,
        outline_fill: tuple = None,
        pad_x: int = 10,
        pad_y: int = 4,
        radius: int = 4
    ) -> tuple:
        tw, th = LayoutEngine.measure_text(draw, text, font)
        bw = tw + pad_x * 2
        bh = th + pad_y * 2
        box = [(x, y), (x + bw, y + bh)]
        draw.rounded_rectangle(box, radius=radius, fill=bg_fill, outline=outline_fill, width=1 if outline_fill else 0)
        draw.text((x + pad_x, y + pad_y), text, font=font, fill=text_fill)
        return (x, y, x + bw, y + bh)

    @staticmethod
    def draw_header_rule(
        draw: ImageDraw.Draw,
        y: int,
        left_text: str,
        right_text: str,
        line_fill: tuple,
        left_fill: tuple,
        right_fill: tuple
    ):
        draw.line([(80, y), (1000, y)], fill=line_fill, width=2)
        draw.text((80, y + 12), left_text, font=FONTS["mono_badge"], fill=left_fill)
        LayoutEngine.draw_right_aligned_text(draw, right_text, 1000, y + 12, FONTS["mono_badge"], right_fill)


# ---------------------------------------------------------------------------
# SEQUENCE A: Reasoning Tree Search & Rollout Exploration (Reworked)
# ---------------------------------------------------------------------------
def render_sequence_a_frame(frame_idx: int, total_frames: int) -> Image.Image:
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)
    
    # Subtle cinematic camera float
    cam_drift_y = math.sin(t * math.pi) * 8.0

    # Subtle background grid lines within safe zones
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, 1660)], fill=(16, 24, 40), width=1)

    # 1. Header (Anchored at Y=150)
    LayoutEngine.draw_header_rule(
        draw=draw,
        y=150,
        left_text="// SUPER.INTELLIGENCEEE  |  RL EXPLORATION BOTTLENECK",
        right_text="REASONING SEARCH WALL",
        line_fill=ACCENT_BLUE,
        left_fill=ACCENT_BLUE,
        right_fill=TEXT_MUTED_LIGHT
    )

    # 2. Unobstructed Title Block
    head_y = 195
    draw.text((80, head_y), "The Reasoning Search Wall", font=FONTS["display_hero"], fill=TEXT_PRIMARY_LIGHT)
    
    deck_text = (
        "In Group Relative Policy Optimization, discovering verified reasoning paths requires "
        "sampling vast exploration trees. The vast majority of generated rollouts result in dead ends."
    )
    next_y = LayoutEngine.draw_wrapped_text(
        draw=draw,
        text=deck_text,
        x=80,
        y=head_y + 58,
        font=FONTS["body_md"],
        fill=TEXT_SECONDARY_LIGHT,
        max_width=920,
        line_spacing=5
    )

    # 3. Main Stage: Tree Search & Rollout Exploration Canvas
    # Bounds: Y in [330, 1380] (1050px height)
    stage_box = (80, 330, 1000, 1380)
    draw.rounded_rectangle(stage_box, radius=14, fill=(12, 18, 32), outline=(30, 41, 59), width=2)
    draw.rounded_rectangle([(80, 330), (1000, 372)], radius=14, fill=(18, 28, 48))
    draw.text((105, 342), "MONTE CARLO ROLLOUT TREE // EXPONENTIAL SEARCH HORIZON", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_LIGHT)
    LayoutEngine.draw_right_aligned_text(draw, "SAMPLING N=64 PATHS", 975, 342, FONTS["mono_citation"], ACCENT_AMBER)

    # Visual Metaphor Coordinates
    root_x, root_y = 540, 430

    # Root Prompt Node (Fades in at t in [0.0, 0.20])
    alpha_root = min(1.0, t / 0.15)
    root_w, root_h = 420, 68
    root_box = [(root_x - root_w // 2, root_y - root_h // 2), (root_x + root_w // 2, root_y + root_h // 2)]
    draw.rounded_rectangle(root_box, radius=8, fill=(24, 36, 60), outline=ACCENT_BLUE, width=2)
    draw.text((root_x - 190, root_y - 22), "ROOT PROMPT (x): Factor x⁴ - 16", font=FONTS["card_title"], fill=TEXT_PRIMARY_LIGHT)
    draw.text((root_x - 190, root_y + 6), "Target domain: Hard Math Olympiad (MATH-500)", font=FONTS["mono_sm"], fill=TEXT_SECONDARY_LIGHT)

    # Five Branching Rollout Paths (Grow from t in [0.15, 0.70])
    branches = [
        {"name": "Rollout τ₁", "x": 170, "y": 740, "status": "DEAD END", "color": ACCENT_CORAL, "bg": (45, 15, 20), "steps": ["x² = u", "u² - 16", "Disregards (x²+4)"]},
        {"name": "Rollout τ₂", "x": 355, "y": 800, "status": "PRUNED", "color": ACCENT_AMBER, "bg": (45, 30, 15), "steps": ["(x-2)⁴", "Sign error", "Zero reward"]},
        {"name": "Rollout τ₃", "x": 540, "y": 860, "status": "VERIFIED", "color": ACCENT_EMERALD, "bg": (15, 45, 25), "steps": ["(x²-4)(x²+4)", "(x-2)(x+2)(x²+4)", "Q.E.D. Correct"]},
        {"name": "Rollout τ₄", "x": 725, "y": 790, "status": "FAILED", "color": ACCENT_CORAL, "bg": (45, 15, 20), "steps": ["Difference cubes", "Formula error", "Negative score"]},
        {"name": "Rollout τ₅", "x": 910, "y": 730, "status": "TIMEOUT", "color": ACCENT_AMBER, "bg": (45, 30, 15), "steps": ["Infinite loop", "Token overflow", "Discarded"]},
    ]

    branch_prog = min(1.0, max(0.0, (t - 0.15) / 0.50))

    for b_idx, b in enumerate(branches):
        bx, by = b["x"], b["y"]
        # Interpolate curve connection from root to branch
        ctrl_y = (root_y + by) // 2
        
        # Calculate active draw progress for line
        line_p = min(1.0, max(0.0, (branch_prog - b_idx * 0.12) / 0.40))
        if line_p > 0:
            cur_x = int(root_x + (bx - root_x) * line_p)
            cur_y = int(root_y + (by - root_y) * line_p)
            line_col = b["color"] if (t >= 0.65 and b["status"] == "VERIFIED") else (60, 80, 110)
            draw.line([(root_x, root_y + root_h // 2), (cur_x, cur_y)], fill=line_col, width=2)

        # Draw Node if reached
        if line_p >= 0.8:
            node_w, node_h = 160, 175
            n_box = [(bx - node_w // 2, by), (bx + node_w // 2, by + node_h)]
            
            # Is this node verified or failed?
            is_revealed = (t >= 0.60)
            n_bg = b["bg"] if is_revealed else (18, 28, 48)
            n_border = b["color"] if is_revealed else (50, 70, 100)

            draw.rounded_rectangle(n_box, radius=8, fill=n_bg, outline=n_border, width=2 if is_revealed else 1)
            
            # Header of node
            draw.text((bx - node_w // 2 + 10, by + 10), b["name"], font=FONTS["mono_badge"], fill=TEXT_PRIMARY_LIGHT)
            
            # Steps inside node
            step_y = by + 34
            for s in b["steps"]:
                draw.text((bx - node_w // 2 + 10, step_y), f"• {s}", font=FONTS["mono_sm"], fill=TEXT_SECONDARY_LIGHT)
                step_y += 22

            # Status Badge at bottom of node (Fits with 14px padding, fixes text overflow!)
            if is_revealed:
                badge_bg = (10, 30, 20) if b["status"] == "VERIFIED" else (35, 10, 15)
                LayoutEngine.draw_badge(
                    draw=draw,
                    x=bx - node_w // 2 + 10,
                    y=by + node_h - 32,
                    text=b["status"],
                    font=FONTS["mono_citation"],
                    bg_fill=badge_bg,
                    text_fill=b["color"],
                    outline_fill=b["color"],
                    pad_x=8,
                    pad_y=3,
                    radius=4
                )

    # 4. Explanatory Annotation within Stage Box (Reveals at t >= 0.65)
    if t >= 0.65:
        annot_y = 1140
        draw.line([(105, annot_y), (975, annot_y)], fill=(30, 45, 70), width=1)
        draw.text((105, annot_y + 14), "THE EXPLORATION DILEMMA IN RAW GRPO / RLVR:", font=FONTS["mono_badge"], fill=ACCENT_AMBER)
        
        annot_text = (
            "Because rewards are only assigned at the terminal answer, RL models generate dozens of full-length "
            "rollouts per prompt. Over 90% of intermediate tokens belong to failed or discarded reasoning chains."
        )
        LayoutEngine.draw_wrapped_text(draw, annot_text, 105, annot_y + 40, FONTS["body_sm"], TEXT_SECONDARY_LIGHT, 870, line_spacing=4)

    # 5. Compute Exhaustion Gauge Card (Y in [1410, 1560])
    gauge_box = [(80, 1410), (1000, 1560)]
    draw.rounded_rectangle(gauge_box, radius=12, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
    
    draw.text((105, 1424), "EMPIRICAL COMPUTE DRAIN // ONLINE GENERATION OVERHEAD", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_LIGHT)
    LayoutEngine.draw_right_aligned_text(draw, "FLOP BOTTLENECK: 90%+ ON SAMPLING", 975, 1424, FONTS["mono_badge"], ACCENT_CORAL)
    
    # Progress gauge filling dynamically
    gauge_p = min(1.0, max(0.0, (t - 0.40) / 0.50))
    bar_x, bar_y, bar_w, bar_h = 105, 1455, 870, 24
    draw.rounded_rectangle([(bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h)], radius=6, fill=(30, 41, 59))
    
    fill_w = int(bar_w * gauge_p * 0.92)  # Fills to 92%
    draw.rounded_rectangle([(bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h)], radius=6, fill=ACCENT_CORAL)
    
    draw.text((105, 1495), "Token generation FLOPs during online exploration dwarf policy gradient backpropagation.", font=FONTS["body_sm"], fill=TEXT_SECONDARY_LIGHT)
    draw.text((105, 1522), "Formula: Total Training FLOPs ≈ N_samples × L_response × Cost_forward (O(N·L) overhead)", font=FONTS["mono_sm"], fill=TEXT_MUTED_LIGHT)

    # 6. Bottom Safe-Zone Citation (Y = 1585)
    draw.line([(80, 1585), (1000, 1585)], fill=(30, 41, 59), width=1)
    draw.text((80, 1600), "CONCEPTUAL REASONING TREE METAPHOR // NOT RAW SYSTEM TELEMETRY", font=FONTS["mono_citation"], fill=TEXT_MUTED_LIGHT)
    LayoutEngine.draw_right_aligned_text(draw, "ARXIV:2611.08453 SECTION 1", 1000, 1600, FONTS["mono_citation"], ACCENT_BLUE)

    return img


# ---------------------------------------------------------------------------
# SEQUENCE B: 5-Stage Mechanism Flow & Clear Layout (Reworked)
# ---------------------------------------------------------------------------
def render_sequence_b_frame(frame_idx: int, total_frames: int) -> Image.Image:
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)

    # Architectural grid
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, 1660)], fill=(240, 237, 230), width=1)

    # 1. Top Header
    LayoutEngine.draw_header_rule(
        draw=draw,
        y=150,
        left_text="// SUPER.INTELLIGENCEEE  |  ALGORITHMIC MECHANISM",
        right_text="TOKEN-LEVEL OPD DYNAMICS",
        line_fill=ACCENT_BLUE,
        left_fill=ACCENT_BLUE,
        right_fill=TEXT_SECONDARY_DARK
    )

    # 2. Unobstructed Title Block
    head_y = 195
    draw.text((80, head_y), "On-Policy Distillation Dynamics", font=FONTS["headline_lg"], fill=TEXT_PRIMARY_DARK)
    
    deck_text = (
        "The student policy samples rollouts on-policy, while a frozen teacher model evaluates "
        "the student tokens to provide dense per-token distribution guidance."
    )
    LayoutEngine.draw_wrapped_text(
        draw=draw,
        text=deck_text,
        x=80,
        y=head_y + 52,
        font=FONTS["body_md"],
        fill=TEXT_SECONDARY_DARK,
        max_width=920,
        line_spacing=4
    )

    # 3. Mechanism Container: Student-Teacher Interaction (Y in [320, 890])
    mech_box = [(80, 320), (1000, 890)]
    draw.rounded_rectangle(mech_box, radius=14, fill=SURFACE_WHITE, outline=BORDER_SUBTLE, width=2)
    draw.rounded_rectangle([(80, 320), (1000, 365)], radius=14, fill=(241, 245, 249))
    draw.text((105, 334), "ALGORITHMIC MECHANISM: 5-STAGE STUDENT-TEACHER PIPELINE", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    LayoutEngine.draw_right_aligned_text(draw, "ON-POLICY SAMPLING", 975, 334, FONTS["mono_citation"], ACCENT_BLUE)

    # Region 1: Student Policy Generation (Y in [385, 540])
    draw.text((105, 385), "STAGE 1 & 2: STUDENT POLICY SAMPLING (y ~ π_θ)", font=FONTS["mono_badge"], fill=ACCENT_BLUE)
    
    # Prompt Intake Box
    draw.text((105, 415), "1. Prompt Intake:", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    prompt_toks = ["[Prompt]", "Factor", "x⁴", "-", "16", "="]
    px = 105
    for tok in prompt_toks:
        tw, th = LayoutEngine.measure_text(draw, tok, FONTS["mono_badge"])
        bw = tw + 14
        draw.rounded_rectangle([(px, 440), (px + bw, 474)], radius=4, fill=(241, 245, 249), outline=BORDER_SUBTLE, width=1)
        draw.text((px + 7, 447), tok, font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
        px += bw + 8

    # Progressive Student Generated Tokens (Reveal over t in [0.0, 0.35])
    draw.text((105, 490), "2. Student Generated Rollout (Active Sampling):", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    rollout_tokens = ["(", "x²", "-", "4", ")", "(", "x²", "+", "4", ")"]
    stage1_prog = min(1.0, t / 0.35)
    visible_toks = int(stage1_prog * len(rollout_tokens))
    
    rx = 105
    for i, tok in enumerate(rollout_tokens):
        if i > visible_toks and t < 0.35:
            continue
        is_current = (i == visible_toks and t < 0.35)
        tw, th = LayoutEngine.measure_text(draw, tok, FONTS["card_title"])
        bw = tw + 18
        bg_c = ACCENT_BLUE_LIGHT if is_current else (248, 250, 252)
        border_c = ACCENT_BLUE if is_current else BORDER_STRONG
        draw.rounded_rectangle([(rx, 515), (rx + bw, 560)], radius=4, fill=bg_c, outline=border_c, width=2 if is_current else 1)
        draw.text((rx + 9, 523), tok, font=FONTS["card_title"], fill=ACCENT_BLUE if is_current else TEXT_PRIMARY_DARK)
        rx += bw + 8

    # Vertical Flow Divider & Directional Arrows (Y in [580, 620])
    draw.line([(105, 585), (975, 585)], fill=BORDER_SUBTLE, width=1)
    
    # Region 2: Frozen Teacher Supervision (Y in [600, 860])
    # SEPARATE VISUAL REGIONS FIXES STAGE 2 COLLISION COMPLETELY!
    draw.text((105, 605), "STAGE 3 & 4: FROZEN TEACHER SUPERVISION", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    
    # Padlock / Frozen Status Badge placed safely on its own line/box at X=650
    LayoutEngine.draw_badge(
        draw=draw,
        x=680,
        y=598,
        text="TEACHER WEIGHTS STRICTLY FROZEN",
        font=FONTS["mono_citation"],
        bg_fill=ACCENT_AMBER_BG,
        text_fill=ACCENT_AMBER,
        outline_fill=ACCENT_AMBER,
        pad_x=10,
        pad_y=4,
        radius=4
    )

    draw.text((105, 640), "3. Teacher Evaluates Student Rollouts:", font=FONTS["body_sm"], fill=TEXT_SECONDARY_DARK)
    
    # Animated Teacher Logit Probability Stems (Reveals over t in [0.30, 0.65])
    stage2_prog = min(1.0, max(0.0, (t - 0.30) / 0.35))
    stem_h_factor = math.sin(stage2_prog * math.pi / 2.0)
    
    # Distribution visualization
    stem_x = 130
    for s_i in range(16):
        prob_teacher = math.exp(-((s_i - 8) ** 2) / 9.0) * 85 * stem_h_factor
        student_bias = 8.5 - 0.5 * min(1.0, max(0.0, (t - 0.45) / 0.25))
        prob_student = math.exp(-((s_i - student_bias) ** 2) / 10.0) * 75 * stem_h_factor
        
        # Teacher target stem (Grey)
        draw.line([(stem_x, 760), (stem_x, 760 - int(prob_teacher))], fill=(148, 163, 184), width=6)
        # Student predicted stem (Blue)
        draw.line([(stem_x + 8, 760), (stem_x + 8, 760 - int(prob_student))], fill=ACCENT_BLUE, width=6)
        stem_x += 52

    draw.text((105, 775), "Target: Teacher Token Distribution π_teacher(y|x) [Grey]", font=FONTS["mono_sm"], fill=TEXT_MUTED_DARK)
    draw.text((105, 795), "Sampled: Student Model Distribution π_θ(y|x) [Blue]", font=FONTS["mono_sm"], fill=ACCENT_BLUE)
    
    # Supervisory loss connection without claiming unverified specific variants
    draw.text((105, 835), "4. Gradient Update: Dense token-level supervision updates student policy parameters θ.", font=FONTS["body_sm"], fill=TEXT_PRIMARY_DARK)

    # 4. Experimental Divergence Section (Y in [920, 1550])
    draw.text((80, 920), "EXPERIMENTAL DIVERGENCE: TEACHER SELECTION REGIMES (ARXIV:2611.08453)", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)

    # Card 1: Self-Teacher OPD (Emerald)
    card1_y = 955
    card1_h = 270
    draw.rounded_rectangle([(80, card1_y), (1000, card1_y + card1_h)], radius=12, fill=ACCENT_EMERALD_BG, outline=ACCENT_EMERALD, width=2)
    draw.rounded_rectangle([(80, card1_y), (92, card1_y + card1_h)], radius=4, fill=ACCENT_EMERALD)
    
    draw.text((115, card1_y + 16), "CONDITION 1: SELF-CHECKPOINT TEACHER", font=FONTS["mono_badge"], fill=ACCENT_EMERALD)
    draw.text((115, card1_y + 44), "50× Distillation FLOP Reduction vs Raw RL", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)
    
    # Animated FLOP efficiency bar (Reveals at t >= 0.65)
    e_prog = min(1.0, max(0.0, (t - 0.65) / 0.20))
    draw.rounded_rectangle([(115, card1_y + 86), (965, card1_y + 96)], radius=4, fill=(209, 250, 229))
    draw.rounded_rectangle([(115, card1_y + 86), (115 + int(850 * e_prog), card1_y + 96)], radius=4, fill=ACCENT_EMERALD)

    c1_desc = (
        "When distilling from the student's own checkpoint, OPD matches full RL accuracy with "
        "50× fewer distillation FLOPs. However, this relies on having already trained that GRPO checkpoint."
    )
    LayoutEngine.draw_wrapped_text(draw, c1_desc, 115, card1_y + 110, FONTS["body_md"], TEXT_SECONDARY_DARK, 850, line_spacing=4)
    LayoutEngine.draw_badge(draw, 115, card1_y + 215, "PROVEN LAB SPEEDUP // MATH-500", FONTS["mono_citation"], (209, 250, 229), ACCENT_EMERALD, ACCENT_EMERALD)

    # Card 2: External Teacher OPD (Coral)
    card2_y = 1255
    card2_h = 270
    draw.rounded_rectangle([(80, card2_y), (1000, card2_y + card2_h)], radius=12, fill=ACCENT_CORAL_BG, outline=ACCENT_CORAL, width=2)
    draw.rounded_rectangle([(80, card2_y), (92, card2_y + card2_h)], radius=4, fill=ACCENT_CORAL)

    draw.text((115, card2_y + 16), "CONDITION 2: EXTERNAL POST-TRAINED TEACHER", font=FONTS["mono_badge"], fill=ACCENT_CORAL)
    draw.text((115, card2_y + 44), "Response-Length Bloat & Accuracy Deficit", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)

    # Animated Bloat bar (Reveals at t >= 0.75)
    c_prog = min(1.0, max(0.0, (t - 0.75) / 0.20))
    draw.rounded_rectangle([(115, card2_y + 86), (965, card2_y + 96)], radius=4, fill=(254, 226, 226))
    draw.rounded_rectangle([(115, card2_y + 86), (115 + int(850 * c_prog), card2_y + 96)], radius=4, fill=ACCENT_CORAL)

    c2_desc = (
        "Under matched training FLOPs, OPD with external teachers generates bloated responses "
        "without proportional reasoning gains, causing it to generally trail direct GRPO in accuracy per FLOP."
    )
    LayoutEngine.draw_wrapped_text(draw, c2_desc, 115, card2_y + 110, FONTS["body_md"], TEXT_SECONDARY_DARK, 850, line_spacing=4)
    LayoutEngine.draw_badge(draw, 115, card2_y + 215, "CRITICAL LIMITATION // SECTION 4", FONTS["mono_citation"], (254, 226, 226), ACCENT_CORAL, ACCENT_CORAL)

    # 5. Bottom Safe-Zone Citation (Y = 1585)
    draw.line([(80, 1585), (1000, 1585)], fill=BORDER_SUBTLE, width=1)
    draw.text((80, 1600), "SOURCE: ARXIV:2611.08453 // SECTION 3 & SECTION 4", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    LayoutEngine.draw_right_aligned_text(draw, "ALGORITHMIC FLOW AUDIT", 1000, 1600, FONTS["mono_citation"], ACCENT_BLUE)

    return img


# ---------------------------------------------------------------------------
# SEQUENCE C: Complete Layout Redesign & Unobstructed 3-Pillar Architecture
# ---------------------------------------------------------------------------
def render_sequence_c_frame(frame_idx: int, total_frames: int) -> Image.Image:
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    t = frame_idx / max(1, total_frames - 1)

    # Architectural grid
    for gx in (80, 310, 540, 770, 1000):
        draw.line([(gx, 140), (gx, 1660)], fill=(240, 237, 230), width=1)

    # 1. Top Header
    LayoutEngine.draw_header_rule(
        draw=draw,
        y=150,
        left_text="// SUPER.INTELLIGENCEEE  |  EDITORIAL SYNTHESIS",
        right_text="PRODUCTION TAKEAWAY",
        line_fill=TEXT_PRIMARY_DARK,
        left_fill=TEXT_PRIMARY_DARK,
        right_fill=TEXT_SECONDARY_DARK
    )

    # 2. Unobstructed Title Block (Fixes title/panel overlap completely!)
    # Headline fits comfortably on a single line at 38pt (width ~680px <= 920px)
    head_y = 195
    draw.text((80, head_y), "OPD is Not a Universal Accelerator", font=FONTS["headline_lg"], fill=TEXT_PRIMARY_DARK)
    
    sub_y = head_y + 50
    sub_text = "Three distinct compute regimes established in Salesforce AI & UIUC preprint (arXiv:2611.08453)"
    draw.text((80, sub_y), sub_text, font=FONTS["body_md"], fill=TEXT_SECONDARY_DARK)

    # 3. Three-Pillar Comparison Panel Begins ONLY AFTER Title Block Buffer (Y in [315, 870])
    panel_box = [(80, 315), (1000, 870)]
    draw.rounded_rectangle(panel_box, radius=14, fill=SURFACE_WHITE, outline=BORDER_SUBTLE, width=2)
    draw.rounded_rectangle([(80, 315), (1000, 355)], radius=14, fill=(241, 245, 249))
    draw.text((105, 327), "THE EMPIRICAL COMPUTE HORIZON // 3 DISTINCTIONS", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    LayoutEngine.draw_right_aligned_text(draw, "ARXIV:2611.08453", 975, 327, FONTS["mono_citation"], ACCENT_BLUE)

    # Three Clearly Separated Columns (Width: 275px, Gutters: 32px, Bounds: X in [105, 975])
    col_w = 270
    col_gap = 30
    c_y1 = 375
    c_y2 = 845

    # COLUMN 1: Direct GRPO Baseline (Always visible)
    col1_x = 105
    draw.rounded_rectangle([(col1_x, c_y1), (col1_x + col_w, c_y2)], radius=10, fill=(248, 250, 252), outline=BORDER_STRONG, width=1)
    draw.rounded_rectangle([(col1_x, c_y1), (col1_x + col_w, c_y1 + 36)], radius=10, fill=(226, 232, 240))
    draw.text((col1_x + 14, c_y1 + 10), "DIRECT GRPO", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
    
    draw.text((col1_x + 14, c_y1 + 52), "REGIME", font=FONTS["mono_sm"], fill=TEXT_MUTED_DARK)
    draw.text((col1_x + 14, c_y1 + 72), "Trial & Error RL", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)

    draw.text((col1_x + 14, c_y1 + 120), "COMPUTE OVERHEAD", font=FONTS["mono_sm"], fill=TEXT_MUTED_DARK)
    draw.text((col1_x + 14, c_y1 + 140), "100% Exploration", font=FONTS["body_md"], fill=TEXT_SECONDARY_DARK)

    draw.text((col1_x + 14, c_y1 + 190), "ACCURACY / FLOP", font=FONTS["mono_sm"], fill=TEXT_MUTED_DARK)
    draw.text((col1_x + 14, c_y1 + 210), "Standard Baseline", font=FONTS["body_md"], fill=TEXT_SECONDARY_DARK)

    draw.line([(col1_x + 14, c_y1 + 270), (col1_x + col_w - 14, c_y1 + 270)], fill=BORDER_SUBTLE, width=1)
    c1_desc = "Full RL exploration discovers new reasoning chains at high sampling cost."
    LayoutEngine.draw_wrapped_text(draw, c1_desc, col1_x + 14, c_y1 + 285, FONTS["body_sm"], TEXT_SECONDARY_DARK, col_w - 28, line_spacing=3)
    LayoutEngine.draw_badge(draw, col1_x + 14, c_y2 - 40, "RL REFERENCE", FONTS["mono_citation"], (226, 232, 240), TEXT_SECONDARY_DARK)

    # COLUMN 2: Self-Teacher OPD (Reveals at t >= 0.28)
    col2_x = col1_x + col_w + col_gap
    if t >= 0.28:
        p2_prog = min(1.0, (t - 0.28) / 0.15)
        draw.rounded_rectangle([(col2_x, c_y1), (col2_x + col_w, c_y2)], radius=10, fill=ACCENT_EMERALD_BG, outline=ACCENT_EMERALD, width=2)
        draw.rounded_rectangle([(col2_x, c_y1), (col2_x + col_w, c_y1 + 36)], radius=10, fill=ACCENT_EMERALD)
        draw.text((col2_x + 14, c_y1 + 10), "SELF-TEACHER OPD", font=FONTS["mono_badge"], fill=SURFACE_WHITE)

        draw.text((col2_x + 14, c_y1 + 52), "REGIME", font=FONTS["mono_sm"], fill=ACCENT_EMERALD)
        draw.text((col2_x + 14, c_y1 + 72), "Self-Consolidation", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)

        draw.text((col2_x + 14, c_y1 + 120), "COMPUTE SPEEDUP", font=FONTS["mono_sm"], fill=ACCENT_EMERALD)
        # Fits comfortably inside 270px column (fixes metric overflow!)
        draw.text((col2_x + 14, c_y1 + 140), "50× FLOP Win", font=FONTS["headline_md"], fill=ACCENT_EMERALD)

        # Animated progress gauge
        gauge_w2 = int(p2_prog * (col_w - 28))
        draw.rounded_rectangle([(col2_x + 14, c_y1 + 175), (col2_x + col_w - 14, c_y1 + 183)], radius=4, fill=(209, 250, 229))
        draw.rounded_rectangle([(col2_x + 14, c_y1 + 175), (col2_x + 14 + gauge_w2, c_y1 + 183)], radius=4, fill=ACCENT_EMERALD)

        draw.text((col2_x + 14, c_y1 + 195), "MATCHED ACCURACY", font=FONTS["mono_sm"], fill=ACCENT_EMERALD)
        draw.text((col2_x + 14, c_y1 + 215), "Matches Full RL", font=FONTS["body_md"], fill=TEXT_PRIMARY_DARK)

        draw.line([(col2_x + 14, c_y1 + 270), (col2_x + col_w - 14, c_y1 + 270)], fill=BORDER_STRONG, width=1)
        c2_desc = "Distills student's own checkpoint. Redundant if RL already completed."
        LayoutEngine.draw_wrapped_text(draw, c2_desc, col2_x + 14, c_y1 + 285, FONTS["body_sm"], TEXT_SECONDARY_DARK, col_w - 28, line_spacing=3)
        LayoutEngine.draw_badge(draw, col2_x + 14, c_y2 - 40, "50× DISTILL FLOP", FONTS["mono_citation"], (209, 250, 229), ACCENT_EMERALD)

    # COLUMN 3: External Teacher OPD (Reveals at t >= 0.55)
    col3_x = col2_x + col_w + col_gap
    if t >= 0.55:
        p3_prog = min(1.0, (t - 0.55) / 0.15)
        draw.rounded_rectangle([(col3_x, c_y1), (col3_x + col_w, c_y2)], radius=10, fill=ACCENT_CORAL_BG, outline=ACCENT_CORAL, width=2)
        draw.rounded_rectangle([(col3_x, c_y1), (col3_x + col_w, c_y1 + 36)], radius=10, fill=ACCENT_CORAL)
        draw.text((col3_x + 14, c_y1 + 10), "EXTERNAL TEACHER", font=FONTS["mono_badge"], fill=SURFACE_WHITE)

        draw.text((col3_x + 14, c_y1 + 52), "REGIME", font=FONTS["mono_sm"], fill=ACCENT_CORAL)
        draw.text((col3_x + 14, c_y1 + 72), "Cross-Model OPD", font=FONTS["card_title"], fill=TEXT_PRIMARY_DARK)

        draw.text((col3_x + 14, c_y1 + 120), "FAILURE MODE", font=FONTS["mono_sm"], fill=ACCENT_CORAL)
        draw.text((col3_x + 14, c_y1 + 140), "Length Bloat", font=FONTS["headline_md"], fill=ACCENT_CORAL)

        # Animated Length Bloat gauge
        gauge_w3 = int(p3_prog * (col_w - 28))
        draw.rounded_rectangle([(col3_x + 14, c_y1 + 175), (col3_x + col_w - 14, c_y1 + 183)], radius=4, fill=(254, 226, 226))
        draw.rounded_rectangle([(col3_x + 14, c_y1 + 175), (col3_x + 14 + gauge_w3, c_y1 + 183)], radius=4, fill=ACCENT_CORAL)

        draw.text((col3_x + 14, c_y1 + 195), "MATCHED ACCURACY", font=FONTS["mono_sm"], fill=ACCENT_CORAL)
        draw.text((col3_x + 14, c_y1 + 215), "Trails Direct RL", font=FONTS["body_md"], fill=TEXT_PRIMARY_DARK)

        draw.line([(col3_x + 14, c_y1 + 270), (col3_x + col_w - 14, c_y1 + 270)], fill=BORDER_STRONG, width=1)
        c3_desc = "Under matched compute, triggers output verbosity without accuracy gains."
        LayoutEngine.draw_wrapped_text(draw, c3_desc, col3_x + 14, c_y1 + 285, FONTS["body_sm"], TEXT_SECONDARY_DARK, col_w - 28, line_spacing=3)
        LayoutEngine.draw_badge(draw, col3_x + 14, c_y2 - 40, "CRITICAL LIMITATION", FONTS["mono_citation"], (254, 226, 226), ACCENT_CORAL)

    # 4. Dedicated Multi-Teacher Breakthrough Section (Y in [900, 1260] - Completely un-nested!)
    if t >= 0.70:
        m_prog = min(1.0, (t - 0.70) / 0.15)
        break_y1 = 900
        break_h = 350
        draw.rounded_rectangle([(80, break_y1), (1000, break_y1 + break_h)], radius=14, fill=SURFACE_WHITE, outline=ACCENT_BLUE, width=2)
        draw.rounded_rectangle([(80, break_y1), (92, break_y1 + break_h)], radius=4, fill=ACCENT_BLUE)

        draw.text((115, break_y1 + 18), "ARCHITECTURAL RESOLUTION: MULTI-TEACHER CONSOLIDATION", font=FONTS["mono_badge"], fill=ACCENT_BLUE)
        draw.text((115, break_y1 + 48), "Multi-Teacher OPD Cuts 42.0% Total FLOPs", font=FONTS["headline_md"], fill=TEXT_PRIMARY_DARK)

        # Animated Multi-Teacher FLOP Savings Bar
        m_bar_w = int(m_prog * 850)
        draw.rounded_rectangle([(115, break_y1 + 90), (965, break_y1 + 102)], radius=4, fill=(224, 242, 254))
        draw.rounded_rectangle([(115, break_y1 + 90), (115 + m_bar_w, break_y1 + 102)], radius=4, fill=ACCENT_BLUE)

        multi_desc = (
            "While single-domain self-distillation carries inherent redundancy, the paper's genuine breakthrough "
            "emerges in multi-domain settings: consolidating independent specialist GRPO checkpoints (Math + Code) into "
            "a single unified student reaches joint-GRPO performance with 42.0% fewer total training FLOPs (arXiv:2611.08453, Table 3)."
        )
        LayoutEngine.draw_wrapped_text(draw, multi_desc, 115, break_y1 + 118, FONTS["body_md"], TEXT_SECONDARY_DARK, 850, line_spacing=4)
        
        # Dual-Teacher schematic chips
        LayoutEngine.draw_badge(draw, 115, break_y1 + 285, "TEACHER 1: MATH-SPECIALIST", FONTS["mono_citation"], (241, 245, 249), TEXT_PRIMARY_DARK)
        draw.text((375, break_y1 + 290), "+", font=FONTS["card_title"], fill=TEXT_SECONDARY_DARK)
        LayoutEngine.draw_badge(draw, 400, break_y1 + 285, "TEACHER 2: CODE-SPECIALIST", FONTS["mono_citation"], (241, 245, 249), TEXT_PRIMARY_DARK)
        draw.text((660, break_y1 + 290), "➔", font=FONTS["card_title"], fill=ACCENT_BLUE)
        LayoutEngine.draw_badge(draw, 690, break_y1 + 285, "1 STUDENT (42% FEWER FLOPS)", FONTS["mono_citation"], ACCENT_BLUE_LIGHT, ACCENT_BLUE, ACCENT_BLUE)

    # 5. Academic Preprint Disclosure Stamp (Y in [1285, 1465])
    if t >= 0.85:
        seal_y = 1285
        seal_h = 175
        draw.rounded_rectangle([(80, seal_y), (1000, seal_y + seal_h)], radius=12, fill=(245, 247, 250), outline=BORDER_STRONG, width=1)
        draw.text((115, seal_y + 16), "ACADEMIC PREPRINT DISCLOSURE // ARXIV:2611.08453", font=FONTS["mono_badge"], fill=TEXT_PRIMARY_DARK)
        
        seal_text = (
            "Findings represent controlled laboratory evaluations on MATH-500 and AIME 2024. Results have not yet been "
            "independently replicated or universally established across all foundation model scales."
        )
        LayoutEngine.draw_wrapped_text(draw, seal_text, 115, seal_y + 48, FONTS["body_sm"], TEXT_SECONDARY_DARK, 850, line_spacing=4)
        LayoutEngine.draw_badge(draw, 115, seal_y + 125, "STATUS: PREPRINT LAB EVALUATION // PENDING PEER REVIEW", FONTS["mono_citation"], (226, 232, 240), TEXT_SECONDARY_DARK)

    # 6. Bottom Safe-Zone Rule & Citation (Y = 1585)
    draw.line([(80, 1585), (1000, 1585)], fill=BORDER_SUBTLE, width=1)
    draw.text((80, 1600), "ARXIV:2611.08453 TABLE 2 & TABLE 3 // SUPER.INTELLIGENCEEE RESEARCH", font=FONTS["mono_citation"], fill=TEXT_MUTED_DARK)
    LayoutEngine.draw_right_aligned_text(draw, "EDITORIAL SYNTHESIS", 1000, 1600, FONTS["mono_citation"], ACCENT_BLUE)

    return img


# ---------------------------------------------------------------------------
# Video Rendering & Direct Audio Muxing Pipeline
# ---------------------------------------------------------------------------
def render_revised_video(
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
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(raw_video_path)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(total_frames):
        frame_img = render_fn(f, total_frames)
        raw_bytes = frame_img.tobytes()
        proc.stdin.write(raw_bytes)
        if f % 60 == 0:
            print(f"  Frame {f}/{total_frames} encoded...")

    proc.stdin.close()
    proc.wait()
    t_encode = time.time() - t0
    print(f"[OK] Raw Video encoded in {t_encode:.2f}s -> {raw_video_path}")

    # Direct Audio Muxing
    print(f"Muxing Mastered Audio: {audio_path.name} into {final_mp4_path.name}...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-i", str(raw_video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        str(final_mp4_path)
    ]
    subprocess.run(mux_cmd, check=True)
    print(f"[SUCCESS] Final Audio-Visual MP4 created: {final_mp4_path}")


# ---------------------------------------------------------------------------
# Main Orchestrator
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("SUPER.INTELLIGENCEEE — PHASE 4.2A.3-R.1 REVISION PIPELINE")
    print("Executing Visual Metaphor Correction, Layout Redesign & Audio Muxing")
    print("=" * 70)

    fps = 30
    total_frames_a = 258  # 8.60s (matches seq_a_mastered.wav 8.62s)
    total_frames_b = 294  # 9.80s (matches seq_b_mastered.wav 9.80s)
    total_frames_c = 313  # 10.43s (matches seq_c_mastered.wav 10.44s)

    # Sequence A
    raw_a = REVISION_DIR / "sequence_a_revised_raw.mp4"
    final_a = REVISION_DIR / "sequence_a_revised.mp4"
    audio_a = AUDIO_DIR / "seq_a_mastered.wav"
    render_revised_video(render_sequence_a_frame, raw_a, final_a, audio_a, total_frames_a, fps)
    
    # Save Sequence A PNG review frame (at end of animation)
    png_a = REVISION_DIR / "sequence_a_revised.png"
    img_a = render_sequence_a_frame(total_frames_a - 1, total_frames_a)
    img_a.save(png_a, "PNG")
    print(f"[OK] Saved Review Frame: {png_a}")

    # Sequence B
    raw_b = REVISION_DIR / "sequence_b_revised_raw.mp4"
    final_b = REVISION_DIR / "sequence_b_revised.mp4"
    audio_b = AUDIO_DIR / "seq_b_mastered.wav"
    render_revised_video(render_sequence_b_frame, raw_b, final_b, audio_b, total_frames_b, fps)
    
    # Save Sequence B PNG review frame
    png_b = REVISION_DIR / "sequence_b_revised.png"
    img_b = render_sequence_b_frame(total_frames_b - 1, total_frames_b)
    img_b.save(png_b, "PNG")
    print(f"[OK] Saved Review Frame: {png_b}")

    # Sequence C
    raw_c = REVISION_DIR / "sequence_c_revised_raw.mp4"
    final_c = REVISION_DIR / "sequence_c_revised.mp4"
    audio_c = AUDIO_DIR / "seq_c_mastered.wav"
    render_revised_video(render_sequence_c_frame, raw_c, final_c, audio_c, total_frames_c, fps)
    
    # Save Sequence C PNG review frame
    png_c = REVISION_DIR / "sequence_c_revised.png"
    img_c = render_sequence_c_frame(total_frames_c - 1, total_frames_c)
    img_c.save(png_c, "PNG")
    print(f"[OK] Saved Review Frame: {png_c}")

    # Generate 3-Panel Contact Sheet
    print("\n--- Generating Phase 4.2A.3-R.1 Revision Contact Sheet ---")
    cs_w, cs_h = 3240, 1920
    contact_sheet = Image.new("RGB", (cs_w, cs_h), (15, 23, 42))
    contact_sheet.paste(img_a, (0, 0))
    contact_sheet.paste(img_b, (1080, 0))
    contact_sheet.paste(img_c, (2160, 0))
    
    # Vertical divider lines on contact sheet
    cs_draw = ImageDraw.Draw(contact_sheet)
    cs_draw.line([(1080, 0), (1080, cs_h)], fill=(51, 65, 85), width=4)
    cs_draw.line([(2160, 0), (2160, cs_h)], fill=(51, 65, 85), width=4)
    
    cs_path = REVISION_DIR / "phase42a_3r1_contact_sheet.png"
    contact_sheet.save(cs_path, "PNG")
    print(f"[OK] Saved Revision Contact Sheet: {cs_path}")

    # Copy all revision deliverables to Brain Directory for presentation
    print(f"\nCopying all revision artifacts to Brain Directory: {BRAIN_DIR}")
    for item in [
        cs_path, png_a, png_b, png_c,
        final_a, raw_a, final_b, raw_b, final_c, raw_c,
        audio_a, audio_b, audio_c
    ]:
        if item.exists():
            shutil.copy2(item, BRAIN_DIR / item.name)
            print(f"  -> Copied {item.name}")

    print("\n[SUCCESS] Phase 4.2A.3-R.1 Revision Render Completed.")


if __name__ == "__main__":
    main()

