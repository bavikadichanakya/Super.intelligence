"""
SUPER.INTELLIGENCEEE — Phase 15 Master Production Script
Character-Led 3D Educational Entertainment Prototype: 'How A GPU Works'
Total Duration: ~45.97s (1,381 frames @ 30 FPS)
Features:
- Canonical host Kavi with 5 distinct expressions and prop interactions
- Serial vs Parallel visual comparison (Sweating CPU professor vs 1,024-core GPU army)
- 3D Silicon microarchitecture & levitating glowing ALU core
- Synchronous SIMT (Single Instruction, Multiple Threads) instruction wave
- Warm studio takeaway with comedic coffee-drinking CPU professor
"""

from __future__ import annotations

import math
import subprocess
import sys
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from rendering.character.educational_host_rig import EducationalCharacterHost

PROD_DIR = WORKSPACE_ROOT / "output" / "phase15_prototype"
AUDIO_DIR = PROD_DIR / "audio"
FRAMES_DIR = PROD_DIR / "frames"
SCENES_DIR = PROD_DIR / "scenes"
KEYFRAMES_DIR = PROD_DIR / "keyframes"

for d in (PROD_DIR, AUDIO_DIR, FRAMES_DIR, SCENES_DIR, KEYFRAMES_DIR):
    d.mkdir(parents=True, exist_ok=True)

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
FPS = 30

# Sophisticated Color Palette
COLOR_OBSIDIAN = (10, 12, 18, 255)
COLOR_DEEP_SLATE = (16, 20, 30, 255)
COLOR_WORKBENCH = (24, 22, 28, 255)
COLOR_CHALKBOARD = (22, 38, 30, 255)
COLOR_SILICON = (14, 18, 26, 255)

ACCENT_AMBER = (255, 170, 0, 255)
ACCENT_ORANGE = (255, 107, 0, 255)
ACCENT_EMERALD = (16, 185, 129, 255)
ACCENT_CYAN = (0, 229, 255, 255)
ACCENT_RED_WARN = (239, 68, 68, 255)
ACCENT_GOLD = (245, 158, 11, 255)

TEXT_HEADLINE = (245, 247, 250, 255)
TEXT_MUTED = (140, 155, 180, 255)

def get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidate_paths = [
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for p in candidate_paths:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

FONT_HERO = get_font(52, bold=True)
FONT_TITLE = get_font(40, bold=True)
FONT_HEADER = get_font(30, bold=True)
FONT_BODY = get_font(24, bold=False)
FONT_MONO = get_font(22, bold=False)
FONT_SUB = get_font(28, bold=True)
FONT_SUB_BODY = get_font(22, bold=False)

# ---------------------------------------------------------------------------
# Scene Renderers
# ---------------------------------------------------------------------------

def draw_subtitle_box(canvas: Image.Image, text: str):
    draw = ImageDraw.Draw(canvas)
    # Subtitle bar at bottom safe zone y in [1650, 1790]
    draw.rounded_rectangle([70, 1660, 1010, 1780], radius=16, fill=(12, 15, 22, 230), outline=(50, 60, 80, 255), width=2)
    # Split text if long
    words = text.split()
    line1 = " ".join(words[:len(words)//2])
    line2 = " ".join(words[len(words)//2:])
    draw.text((100, 1680), line1, font=FONT_SUB, fill=TEXT_HEADLINE)
    draw.text((100, 1722), line2, font=FONT_SUB, fill=ACCENT_AMBER)


def render_scene1_overload(canvas: Image.Image, t_sec: float, dur_sec: float):
    """Scene 1: Workshop Desk & The Overwhelming Task Avalanche."""
    draw = ImageDraw.Draw(canvas)
    # Background: Warm workshop desk with radial spotlight
    for y in range(CANVAS_HEIGHT):
        ratio = y / float(CANVAS_HEIGHT)
        r = int(22 * (1.0 - ratio) + 12 * ratio)
        g = int(24 * (1.0 - ratio) + 14 * ratio)
        b = int(32 * (1.0 - ratio) + 18 * ratio)
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(r, g, b, 255))

    # Overhead desk lamp cone
    lamp_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(lamp_layer)
    ldraw.polygon([(540, 0), (80, 1500), (1000, 1500)], fill=(255, 200, 120, 25))
    lamp_layer = lamp_layer.filter(ImageFilter.GaussianBlur(radius=60))
    canvas.alpha_composite(lamp_layer)

    # Top Header
    draw.text((80, 100), "THE WORKLOAD BOTTLENECK", font=FONT_HEADER, fill=ACCENT_ORANGE)
    draw.text((80, 140), "Rendering 4K at 60 FPS", font=FONT_HERO, fill=TEXT_HEADLINE)

    # The Cascade of 3D Pixel Calculation Blocks
    # 8,294,400 calculations
    blocks_count = min(12, int(t_sec * 2.2) + 1)
    bx = 520
    base_by = 1350
    wobble = math.sin(t_sec * 6.0) * 12.0

    for i in range(blocks_count):
        y_pos = base_by - (i * 75)
        b_wobble = wobble * (i / 12.0)
        col = ACCENT_RED_WARN if i % 2 == 0 else ACCENT_GOLD
        # Draw 3D cube block
        cx = int(bx + b_wobble)
        draw.rounded_rectangle([cx - 160, y_pos - 35, cx + 160, y_pos + 35], radius=10, fill=(35, 20, 25, 240), outline=col, width=2)
        draw.text((cx - 140, y_pos - 20), f"TASK BLOCK #{i*691200 + 1}", font=FONT_MONO, fill=col)
        draw.text((cx - 140, y_pos + 5), "Compute Color (R, G, B, A)", font=FONT_BODY, fill=TEXT_MUTED)

    # Big Total Math Label
    draw.rounded_rectangle([80, 230, 480, 370], radius=14, fill=(28, 18, 22, 230), outline=ACCENT_RED_WARN, width=2)
    draw.text((105, 250), "CALCULATIONS PER SECOND:", font=FONT_BODY, fill=TEXT_MUTED)
    draw.text((105, 280), "497,664,000", font=FONT_HERO, fill=ACCENT_RED_WARN)
    draw.text((105, 335), "8.3M pixels x 60 frames", font=FONT_BODY, fill=TEXT_HEADLINE)


def render_scene2_comparison(canvas: Image.Image, t_sec: float, dur_sec: float):
    """Scene 2: Humorous Visual Comparison (Serial Genius vs Parallel Army)."""
    draw = ImageDraw.Draw(canvas)
    # Dark arena background
    for y in range(CANVAS_HEIGHT):
        ratio = y / float(CANVAS_HEIGHT)
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(14, 16, 24, 255))

    # Header
    draw.text((80, 90), "THE ARCHITECTURAL SHOWDOWN", font=FONT_HEADER, fill=ACCENT_AMBER)
    draw.text((80, 130), "Serial vs. Parallel Processing", font=FONT_HERO, fill=TEXT_HEADLINE)

    # 1. Left Side: THE CPU (Chalkboard & Sweating Professor)
    lx, ly, lw, lh = 70, 220, 440, 800
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=COLOR_CHALKBOARD, outline=(80, 120, 90, 255), width=2)
    draw.text((lx + 25, ly + 25), "THE CPU (SERIAL)", font=FONT_TITLE, fill=(160, 230, 180, 255))
    draw.text((lx + 25, ly + 70), "One Olympic Math Genius", font=FONT_BODY, fill=TEXT_MUTED)
    draw.line([(lx + 25, ly + 105), (lx + lw - 25, ly + 105)], fill=(60, 90, 70, 255), width=1)

    # Chalk math scribbles
    chalk_math = [
        "P1:  2.4 * 0.7 = 1.68 [OK]",
        "P2:  3.1 * 0.2 = 0.62 [OK]",
        "P3:  0.9 * 0.8 = 0.72 [OK]",
        "P4:  1.5 * 0.4 = ... sweat!",
        "...",
        f"P{int(t_sec * 40 + 5)}: Calculating...",
        "STATUS: EXHAUSTED (8M to go)"
    ]
    my = ly + 125
    for cm in chalk_math:
        col = (230, 245, 230, 255) if "OK" in cm else ACCENT_RED_WARN
        draw.text((lx + 25, my), cm, font=FONT_MONO, fill=col)
        my += 45

    # Frantic ticking clock on CPU side
    clock_angle = t_sec * 720.0  # spinning fast
    cx, cy = lx + lw - 70, ly + 55
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(30, 40, 35, 255), outline=(200, 220, 200, 255), width=2)
    hx = cx + int(20 * math.cos(math.radians(clock_angle)))
    hy = cy + int(20 * math.sin(math.radians(clock_angle)))
    draw.line([(cx, cy), (hx, hy)], fill=ACCENT_RED_WARN, width=2)

    # 2. Right Side: THE GPU (Grid of 1,024 Parallel Paint Workers)
    rx, ry, rw, rh = 570, 220, 440, 800
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=(16, 24, 36, 255), outline=ACCENT_EMERALD, width=2)
    draw.text((rx + 25, ry + 25), "THE GPU (PARALLEL)", font=FONT_TITLE, fill=ACCENT_EMERALD)
    draw.text((rx + 25, ry + 70), "Army of 1,024 Workers", font=FONT_BODY, fill=TEXT_MUTED)
    draw.line([(rx + 25, ry + 105), (rx + rw - 25, ry + 105)], fill=(30, 60, 50, 255), width=1)

    # Grid of miniature worker dots painting simultaneously
    grid_rows, grid_cols = 12, 10
    gw = (rw - 50) // grid_cols
    gh = (lh - 200) // grid_rows
    # Wave of painted pixels
    wave_progress = (t_sec * 1.5) % 3.0
    for r in range(grid_rows):
        for c in range(grid_cols):
            dot_x = rx + 30 + c * gw
            dot_y = ry + 130 + r * gh
            painted = (c + r * 0.5) < (wave_progress * 8.0)
            dot_col = ACCENT_EMERALD if painted else (40, 55, 75, 255)
            draw.rounded_rectangle([dot_x, dot_y, dot_x + gw - 6, dot_y + gh - 6], radius=4, fill=dot_col)

    draw.rounded_rectangle([rx + 25, ry + lh - 70, rx + rw - 25, ry + lh - 20], radius=8, fill=(12, 45, 30, 255))
    draw.text((rx + 40, ry + lh - 55), "ALL PIXELS PAINTED IN 1 TICK", font=FONT_MONO, fill=ACCENT_EMERALD)


def render_scene3_silicon(canvas: Image.Image, t_sec: float, dur_sec: float):
    """Scene 3: Inside the Silicon Die (Microarchitecture Exploration)."""
    draw = ImageDraw.Draw(canvas)
    # Silicon die wafer background
    for y in range(CANVAS_HEIGHT):
        ratio = y / float(CANVAS_HEIGHT)
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(12, 16, 22, 255))

    # Metallic PCB / Silicon trace lines
    for i in range(12):
        ty = 180 + i * 80
        draw.line([(60, ty), (1020, ty)], fill=(25, 35, 48, 180), width=1)
    for j in range(8):
        tx = 120 + j * 120
        draw.line([(tx, 150), (tx, 1150)], fill=(25, 35, 48, 180), width=1)

    # Header
    draw.text((80, 90), "INSIDE THE SILICON DIE", font=FONT_HEADER, fill=ACCENT_CYAN)
    draw.text((80, 130), "Streaming Multiprocessors", font=FONT_HERO, fill=TEXT_HEADLINE)

    # Silicon SM Block Diagram
    sx, sy, sw, sh = 480, 220, 530, 840
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=18, fill=(16, 22, 32, 250), outline=ACCENT_CYAN, width=2)
    draw.text((sx + 30, sy + 30), "STREAMING MULTIPROCESSOR (SM)", font=FONT_TITLE, fill=ACCENT_CYAN)

    # Memory bus at top
    draw.rounded_rectangle([sx + 30, sy + 85, sx + sw - 30, sy + 155], radius=10, fill=(24, 32, 48, 255), outline=(0, 229, 255, 120), width=1)
    draw.text((sx + 45, sy + 105), "HIGH-BANDWIDTH MEMORY BUS (HBM3)", font=FONT_MONO, fill=ACCENT_CYAN)

    # Warp Schedulers
    draw.rounded_rectangle([sx + 30, sy + 175, sx + sw - 30, sy + 245], radius=10, fill=(28, 38, 56, 255), outline=ACCENT_GOLD, width=1)
    draw.text((sx + 45, sy + 195), "4x WARP SCHEDULERS & DISPATCH", font=FONT_MONO, fill=ACCENT_GOLD)

    # Dense ALU Grid (128 Cores)
    draw.text((sx + 30, sy + 270), "128 ARITHMETIC LOGIC UNITS (ALUs):", font=FONT_BODY, fill=TEXT_MUTED)
    core_rows, core_cols = 8, 8
    cw = (sw - 60) // core_cols
    ch = (sh - 410) // core_rows
    pulse = int(10 * math.sin(t_sec * 4.0))

    for r in range(core_rows):
        for c in range(core_cols):
            cx = sx + 30 + c * cw
            cy = sy + 310 + r * ch
            glow_c = (16, 185, 129, 220) if (c + r) % 2 == 0 else (52, 211, 153, 180)
            draw.rounded_rectangle([cx, cy, cx + cw - 4, cy + ch - 4], radius=4, fill=(18, 30, 36, 255), outline=glow_c, width=1)

    # Callout card for stripped bureaucracy
    draw.rounded_rectangle([sx + 30, sy + sh - 80, sx + sw - 30, sy + sh - 20], radius=10, fill=(16, 36, 28, 255))
    draw.text((sx + 45, sy + sh - 60), "NO BRANCH PREDICTORS: RAW MATH", font=FONT_MONO, fill=ACCENT_EMERALD)


def render_scene4_simt(canvas: Image.Image, t_sec: float, dur_sec: float):
    """Scene 4: The Scientific Payoff (SIMT Execution)."""
    draw = ImageDraw.Draw(canvas)
    for y in range(CANVAS_HEIGHT):
        ratio = y / float(CANVAS_HEIGHT)
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(10, 14, 20, 255))

    # Header
    draw.text((80, 90), "THE SCIENTIFIC PRINCIPLE", font=FONT_HEADER, fill=ACCENT_EMERALD)
    draw.text((80, 130), "Single Instruction, Multiple Threads", font=FONT_HERO, fill=TEXT_HEADLINE)

    # Warp Instruction Broadcast Box
    ix, iy, iw, ih = 80, 220, 920, 140
    draw.rounded_rectangle([ix, iy, ix + iw, iy + ih], radius=16, fill=(20, 32, 28, 255), outline=ACCENT_EMERALD, width=2)
    draw.text((ix + 35, iy + 25), "WARP INSTRUCTION BROADCAST:", font=FONT_TITLE, fill=ACCENT_EMERALD)
    draw.text((ix + 35, iy + 75), "INSTRUCTION: FMA(Matrix_A[i], Matrix_B[i]) -> 32 Threads", font=FONT_MONO, fill=(200, 255, 230, 255))

    # Downward Synchronous Pulse Wave
    wave_y = iy + ih + int((t_sec * 320.0) % 600.0)
    wave_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    wdraw = ImageDraw.Draw(wave_layer)
    wdraw.line([(80, wave_y), (1000, wave_y)], fill=(52, 211, 153, 200), width=6)
    wdraw.line([(80, wave_y - 10), (1000, wave_y - 10)], fill=(16, 185, 129, 80), width=20)
    canvas.alpha_composite(wave_layer)

    # 32 Thread Execution Lanes
    lanes_y = iy + ih + 60
    lane_h = 480
    num_lanes = 16  # visual representation
    lane_w = (920 - (num_lanes * 8)) // num_lanes

    for l in range(num_lanes):
        lx = 80 + l * (lane_w + 8)
        # Is wave currently passing this lane?
        active = (wave_y >= lanes_y and wave_y <= lanes_y + lane_h)
        col = ACCENT_EMERALD if active else (24, 36, 48, 255)
        out_col = (52, 211, 153, 255) if active else (40, 55, 75, 255)
        draw.rounded_rectangle([lx, lanes_y, lx + lane_w, lanes_y + lane_h], radius=6, fill=col, outline=out_col, width=1)
        # Thread Label
        draw.text((lx + 2, lanes_y + 10), f"T{l}", font=FONT_MONO, fill=TEXT_HEADLINE)
        # Progress bar inside lane
        fill_pct = min(1.0, max(0.0, (wave_y - lanes_y) / float(lane_h))) if wave_y > lanes_y else 0.0
        bar_bottom = lanes_y + lane_h - 4
        bar_top = max(lanes_y + 4, int(bar_bottom - (fill_pct * (lane_h - 40))))
        if bar_top < bar_bottom:
            draw.rectangle([lx + 4, bar_top, lx + lane_w - 4, bar_bottom], fill=ACCENT_EMERALD)

    # Lockstep Banner
    draw.rounded_rectangle([80, lanes_y + lane_h + 30, 1000, lanes_y + lane_h + 100], radius=12, fill=(16, 24, 34, 255), outline=ACCENT_GOLD, width=2)
    draw.text((110, lanes_y + lane_h + 48), "LOCKSTEP EXECUTION // ZERO DIVERGENCE PENALTY", font=FONT_TITLE, fill=ACCENT_GOLD)


def render_scene5_conclusion(canvas: Image.Image, t_sec: float, dur_sec: float):
    """Scene 5: Warm Studio Takeaway with Coffee-Sipping CPU."""
    draw = ImageDraw.Draw(canvas)
    # Warm architectural studio gradient
    for y in range(CANVAS_HEIGHT):
        ratio = y / float(CANVAS_HEIGHT)
        r = int(24 * (1.0 - ratio) + 10 * ratio)
        g = int(22 * (1.0 - ratio) + 12 * ratio)
        b = int(32 * (1.0 - ratio) + 18 * ratio)
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(r, g, b, 255))

    # Studio Bokeh Highlights
    bokeh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bokeh)
    bdraw.ellipse([120, 260, 420, 560], fill=(255, 170, 0, 25))
    bdraw.ellipse([700, 320, 1020, 640], fill=(16, 185, 129, 22))
    bokeh = bokeh.filter(ImageFilter.GaussianBlur(radius=50))
    canvas.alpha_composite(bokeh)

    # Comedic Background Vignette: Relaxed CPU sipping coffee
    draw.rounded_rectangle([80, 240, 440, 480], radius=16, fill=(24, 28, 40, 220), outline=ACCENT_GOLD, width=2)
    draw.text((105, 265), "CPU: TASK STRATEGY", font=FONT_HEADER, fill=ACCENT_GOLD)
    draw.text((105, 305), "Operating system running smooth.", font=FONT_BODY, fill=TEXT_MUTED)
    # Coffee cup drawing
    draw.rectangle([140, 370, 220, 430], fill=(240, 240, 240, 255), outline=(100, 100, 100, 255), width=2)
    draw.arc([200, 380, 250, 420], start=270, end=90, fill=(240, 240, 240, 255), width=6)
    # Steam wobble
    steam_dy = int(5 * math.sin(t_sec * 5.0))
    draw.line([(160, 360 + steam_dy), (160, 345 + steam_dy)], fill=(200, 200, 200, 180), width=3)
    draw.line([(180, 355 - steam_dy), (180, 340 - steam_dy)], fill=(200, 200, 200, 180), width=3)
    draw.text((250, 385), "STATUS: RELAXED", font=FONT_MONO, fill=ACCENT_EMERALD)

    # Editorial Branding Signature
    draw.text((80, 100), "SUPER.INTELLIGENCEEE", font=FONT_HEADER, fill=ACCENT_AMBER)
    draw.text((80, 140), "Understand What's Next.", font=FONT_HERO, fill=TEXT_HEADLINE)
    draw.line([(80, 205), (550, 205)], fill=ACCENT_AMBER, width=2)


# ---------------------------------------------------------------------------
# Master Scene Configurations
# ---------------------------------------------------------------------------

SCENE_SPECS = [
    {
        "id": "scene1_overload",
        "audio_file": AUDIO_DIR / "scene1_overload_speech.wav",
        "render_bg": render_scene1_overload,
        "expression_id": "overwhelmed",
        "prop_mode": "none",
        "gesture_mode": "explaining",
        "host_pos": (300, 1560, 0.65),  # center_x, bottom_y, scale
        "flip_h": False,
        "subtitle": "To render just one frame in 4K, your computer must calculate eight million color values. Sixty times every single second.",
    },
    {
        "id": "scene2_comparison",
        "audio_file": AUDIO_DIR / "scene2_comparison_speech.wav",
        "render_bg": render_scene2_comparison,
        "expression_id": "smug_sarcastic",
        "prop_mode": "none",
        "gesture_mode": "pointing",
        "host_pos": (540, 1560, 0.62),
        "flip_h": False,
        "subtitle": "A CPU is an Olympic math genius solving one problem at a time. A GPU is an army of thousands of workers painting every pixel simultaneously.",
    },
    {
        "id": "scene3_silicon",
        "audio_file": AUDIO_DIR / "scene3_silicon_speech.wav",
        "render_bg": render_scene3_silicon,
        "expression_id": "focused_insight",
        "prop_mode": "glowing_alu_core",
        "gesture_mode": "explaining",
        "host_pos": (280, 1560, 0.65),
        "flip_h": False,
        "subtitle": "Inside the silicon die, complex control logic is stripped away. Instead, thousands of raw Arithmetic Logic Units are packed into Streaming Multiprocessors.",
    },
    {
        "id": "scene4_simt",
        "audio_file": AUDIO_DIR / "scene4_simt_speech.wav",
        "render_bg": render_scene4_simt,
        "expression_id": "triumphant",
        "prop_mode": "none",
        "gesture_mode": "pointing",
        "host_pos": (820, 1560, 0.65),
        "flip_h": False,
        "subtitle": "This is SIMT: Single Instruction, Multiple Threads. One command executes across an entire warp of cores in lockstep, crunching matrices instantly.",
    },
    {
        "id": "scene5_conclusion",
        "audio_file": AUDIO_DIR / "scene5_conclusion_speech.wav",
        "render_bg": render_scene5_conclusion,
        "expression_id": "confident_host",
        "prop_mode": "none",
        "gesture_mode": "explaining",
        "host_pos": (540, 1560, 0.68),
        "flip_h": False,
        "subtitle": "Let your CPU plan the strategy, and let the GPU do the heavy lifting. Super Intelligence. Understand what's next.",
    },
]


def render_scene(spec: Dict[str, Any], host: EducationalCharacterHost) -> Path:
    sid = spec["id"]
    wav_path = spec["audio_file"]
    scene_mp4 = SCENES_DIR / f"{sid}.mp4"

    if scene_mp4.exists() and scene_mp4.stat().st_size > 100000:
        print(f"[SCENE: {sid}] Already rendered and verified ({scene_mp4.name}), skipping.", flush=True)
        return scene_mp4

    with wave.open(str(wav_path), "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration_sec = frames / float(rate)

    num_frames = int(math.ceil(duration_sec * FPS))
    scene_frames_dir = FRAMES_DIR / sid
    scene_frames_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[SCENE: {sid}] Duration: {duration_sec:.2f}s | Frames: {num_frames}", flush=True)

    hx, hy, hscale = spec["host_pos"]
    target_h = int(1755 * hscale)

    for fi in range(num_frames):
        t_sec = fi / float(FPS)
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), COLOR_OBSIDIAN)

        # 1. Background Environment
        spec["render_bg"](canvas, t_sec, duration_sec)

        # 2. Host Character Sprite with Expression & Props
        sprite, kin = host.render_educational_sprite(
            t_sec=t_sec,
            target_height=target_h,
            expression_id=spec["expression_id"],
            is_speaking=True,
            gesture_mode=spec["gesture_mode"],
            prop_mode=spec["prop_mode"],
            flip_h=spec["flip_h"]
        )

        sw, sh = sprite.size
        # Anchor sprite at bottom
        pos_x = hx - sw // 2
        pos_y = hy - sh + int(kin["breath_dy"])

        # Ground Drop Shadow
        shadow_w = int(sw * 0.70)
        shadow_h = int(shadow_w * 0.22)
        shadow_img = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow_img)
        sdraw.ellipse([0, 0, shadow_w, shadow_h], fill=(0, 0, 0, 130))
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=18))
        canvas.alpha_composite(shadow_img, (pos_x + (sw - shadow_w) // 2, hy - shadow_h // 2))

        # Composite Sprite
        canvas.alpha_composite(sprite, (pos_x, pos_y))

        # 3. Subtitles
        draw_subtitle_box(canvas, spec["subtitle"])

        # Save Frame
        frame_path = scene_frames_dir / f"frame_{fi:05d}.png"
        canvas.convert("RGB").save(frame_path)

        # Save Mid-Keyframe
        if fi == num_frames // 2:
            kf_path = KEYFRAMES_DIR / f"{sid}_mid_keyframe.png"
            canvas.convert("RGB").save(kf_path)
            print(f"  [KEYFRAME] Saved: {kf_path.name}", flush=True)

        if fi % 60 == 0:
            print(f"  Frame {fi}/{num_frames}...", flush=True)

    # Encode Scene MP4
    scene_mp4 = SCENES_DIR / f"{sid}.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(scene_frames_dir / "frame_%05d.png"),
        "-i", str(wav_path),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(scene_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[SCENE: {sid}] MP4 encoded: {scene_mp4.name}", flush=True)
    return scene_mp4


def compile_master_prototype(scene_mp4s: List[Path]) -> Path:
    concat_list = PROD_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in scene_mp4s:
            escaped_p = str(p.resolve()).replace("\\", "/")
            f.write(f"file '{escaped_p}'\n")

    master_mp4 = PROD_DIR / "gpu_educational_entertainment_prototype.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(master_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\n[MASTER PROTOTYPE] Compiled: {master_mp4.name}", flush=True)
    return master_mp4


def create_contact_sheet():
    kf_files = [
        KEYFRAMES_DIR / "scene1_overload_mid_keyframe.png",
        KEYFRAMES_DIR / "scene2_comparison_mid_keyframe.png",
        KEYFRAMES_DIR / "scene3_silicon_mid_keyframe.png",
        KEYFRAMES_DIR / "scene4_simt_mid_keyframe.png",
        KEYFRAMES_DIR / "scene5_conclusion_mid_keyframe.png",
    ]

    panel_w, panel_h = 432, 768
    total_w = 5 * panel_w + (6 * 20)
    total_h = panel_h + 160

    sheet = Image.new("RGBA", (total_w, total_h), (12, 14, 20, 255))
    sdraw = ImageDraw.Draw(sheet)

    sdraw.text((30, 30), "SUPER.INTELLIGENCEEE // PHASE 15 PROTOTYPE: HOW A GPU WORKS", font=FONT_TITLE, fill=ACCENT_AMBER)
    sdraw.text((30, 80), "Character-Led 3D Educational Entertainment Engine // 5 Key Narrative Beats", font=FONT_HEADER, fill=TEXT_MUTED)

    titles = [
        "1. THE TASK OVERLOAD (8M Pixels)",
        "2. SERIAL VS. PARALLEL (CPU vs GPU)",
        "3. SILICON MICROARCHITECTURE (ALUs)",
        "4. SCIENTIFIC PRINCIPLE (SIMT Wave)",
        "5. STRATEGIC TAKEAWAY (Relaxed CPU)",
    ]

    for i, (kp, title) in enumerate(zip(kf_files, titles)):
        if kp.exists():
            im = Image.open(kp).resize((panel_w, panel_h), Image.Resampling.LANCZOS)
            x = 20 + i * (panel_w + 20)
            y = 130
            sheet.paste(im, (x, y))
            sdraw.rectangle([x, y, x + panel_w, y + panel_h], outline=(60, 75, 100, 255), width=2)
            sdraw.text((x + 10, y + panel_h - 40), title, font=FONT_BODY, fill=ACCENT_AMBER)

    contact_path = PROD_DIR / "phase15_prototype_contact_sheet.png"
    sheet.save(contact_path)
    print(f"[CONTACT SHEET] Generated: {contact_path.name}", flush=True)


def main():
    print("=" * 80)
    print("SUPER.INTELLIGENCEEE — PHASE 15 PROTOTYPE VIDEO PRODUCTION")
    print("Topic: How A GPU Works (Serial vs. Parallel Microarchitectures)")
    print("Target Duration: ~45.97s (5 Scenes, 1,381 Frames @ 30 FPS)")
    print("=" * 80)

    host = EducationalCharacterHost(workspace_root=WORKSPACE_ROOT)

    scene_mp4s = []
    for spec in SCENE_SPECS:
        mp4_path = render_scene(spec, host)
        scene_mp4s.append(mp4_path)

    master_path = compile_master_prototype(scene_mp4s)
    create_contact_sheet()

    print("\n" + "=" * 80)
    print("PHASE 15 PROTOTYPE VIDEO PRODUCED SUCCESSFULLY!")
    print(f"Master: {master_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
