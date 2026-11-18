"""
SUPER.INTELLIGENCEEE — Phase 14.2 Character Animation Demonstrations
Produces 3 distinct, professionally art-directed character demonstrations:
- Demo A: Documentary Presenter (Cinematic documentary studio environment, clean editorial lighting, zero dashboard UI)
- Demo B: Technology Investigator (Examining realistic 4nm semiconductor processor die, pointing kinematics)
- Demo C: Technical Explainer (Sidecar explainer beside Asynchronous Warp Specialization scientific dataflow)
Generates:
- Individual MP4 demonstration videos
- Master contact sheet combining keyframes from all 3 demonstrations
- Frame-level visual quality metrics
"""

from __future__ import annotations

import json
import math
import subprocess
import time
import wave
from pathlib import Path
import sys

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from typing import Any, Dict, List, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from core.character_scene_config import (
    CharacterSceneConfig,
    CharacterPose,
    CharacterExpression,
    CharacterScreenPosition,
    CharacterMovementPattern,
)
from rendering.animated_character_host import AnimatedCharacterHost

# ---------------------------------------------------------------------------
# Directories & Constants
# ---------------------------------------------------------------------------

PROD_DIR = WORKSPACE_ROOT / "output" / "phase14_2_demos"
AUDIO_DIR = PROD_DIR / "audio"
FRAMES_DIR = PROD_DIR / "frames"
VIDEOS_DIR = PROD_DIR / "videos"
KEYFRAMES_DIR = PROD_DIR / "keyframes"

for d in (PROD_DIR, AUDIO_DIR, FRAMES_DIR, VIDEOS_DIR, KEYFRAMES_DIR):
    d.mkdir(parents=True, exist_ok=True)

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
FPS = 30

# High-Fidelity Color Palette (Non-monotonous, editorial)
STUDIO_BG_TOP = (18, 22, 32, 255)
STUDIO_BG_BOT = (10, 12, 18, 255)
LAB_BG = (12, 16, 24, 255)
CLEANROOM_AMBER = (255, 171, 0, 255)

CYAN_CORE = (0, 229, 255, 255)
GOLD_WARM = (234, 179, 8, 255)
EMERALD_DATA = (16, 185, 129, 255)
PURPLE_WARP = (168, 85, 247, 255)
WHITE_EDITORIAL = (248, 250, 252, 255)
TEXT_MUTED = (148, 163, 184, 255)

# Fonts
def get_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    if mono:
        cand = ["C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]
    else:
        cand = ["C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    for fp in cand:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_HEADER = get_font(22, bold=True, mono=True)
FONT_HERO = get_font(42, bold=True)
FONT_TITLE = get_font(32, bold=True)
FONT_SUB = get_font(24, bold=False)
FONT_LABEL = get_font(20, bold=True)
FONT_MONO = get_font(18, bold=True, mono=True)
FONT_SUBTITLE = get_font(36, bold=True)

HOST_ENGINE = AnimatedCharacterHost(workspace_root=WORKSPACE_ROOT)

# ---------------------------------------------------------------------------
# Demonstration Specifications
# ---------------------------------------------------------------------------

DEMO_SPECS = [
    {
        "id": "demo_a_presenter",
        "title": "Demonstration A: Documentary Presenter",
        "audio_file": AUDIO_DIR / "demo_a_presenter_speech.wav",
        "text": "Welcome to Super Intelligence. Today we investigate a breakthrough that bridges human reasoning with silicon architectures.",
        "host_pos": CharacterScreenPosition.CENTER_HERO,
        "host_scale": 0.72,
        "gesture": "explaining",
        "target_xy": None,
    },
    {
        "id": "demo_b_investigator",
        "title": "Demonstration B: Technology Investigator",
        "audio_file": AUDIO_DIR / "demo_b_investigator_speech.wav",
        "text": "Under electron microscopy, this four nanometer compute die reveals sixty-four billion transistors operating in lockstep.",
        "host_pos": CharacterScreenPosition.LOWER_LEFT,
        "host_scale": 0.58,
        "gesture": "pointing",
        "target_xy": (760, 580),
        "target_label": "4nm COMPUTE CORE // 64B TRANSISTORS",
    },
    {
        "id": "demo_c_explainer",
        "title": "Demonstration C: Technical Explainer",
        "audio_file": AUDIO_DIR / "demo_c_explainer_speech.wav",
        "text": "By offloading memory bandwidth bottlenecks into asynchronous warp pipelines, execution stalls drop to near zero.",
        "host_pos": CharacterScreenPosition.LOWER_LEFT,
        "host_scale": 0.58,
        "gesture": "pointing",
        "target_xy": (720, 520),
        "target_label": "ASYNC PIPELINE OVERLAP",
    },
]

# ---------------------------------------------------------------------------
# Background Renderers (Zero Dashboard UI)
# ---------------------------------------------------------------------------

def render_demo_a_environment(canvas: Image.Image, t_sec: float) -> None:
    """
    Demo A: High-End Cinematic Documentary Studio.
    Warm architectural background with optical bokeh and gentle camera drift.
    ZERO dashboard UI, zero grid, zero neon cards.
    """
    draw = ImageDraw.Draw(canvas)
    # 1. Warm vertical architectural gradient
    for y in range(CANVAS_HEIGHT):
        ratio = y / float(CANVAS_HEIGHT)
        r = int(14 * (1.0 - ratio) + 8 * ratio)
        g = int(18 * (1.0 - ratio) + 10 * ratio)
        b = int(28 * (1.0 - ratio) + 14 * ratio)
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(r, g, b, 255))

    # 2. Warm optical studio bokeh circles (defocused lights)
    bokeh_lights = [
        (240, 320, 160, (255, 180, 80, 24)),
        (880, 260, 200, (220, 140, 60, 20)),
        (180, 780, 130, (255, 200, 120, 18)),
        (920, 850, 150, (200, 160, 100, 16)),
    ]
    bokeh_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bokeh_layer)
    for bx, by, br, bcol in bokeh_lights:
        # Subtle drift
        drift_x = 12 * math.sin(2.0 * math.pi * 0.1 * t_sec + bx)
        drift_y = 10 * math.cos(2.0 * math.pi * 0.1 * t_sec + by)
        bdraw.ellipse([bx - br + drift_x, by - br + drift_y, bx + br + drift_x, by + br + drift_y], fill=bcol)
    bokeh_layer = bokeh_layer.filter(ImageFilter.GaussianBlur(radius=40))
    canvas.alpha_composite(bokeh_layer)

    # 3. Clean editorial identification lower-third (Left aligned, elegant)
    draw.text((100, 140), "SUPER.INTELLIGENCEEE", font=FONT_HEADER, fill=GOLD_WARM)
    draw.text((100, 180), "SPECIAL DOCUMENTARY REPORT", font=FONT_HERO, fill=WHITE_EDITORIAL)
    draw.line([(100, 240), (450, 240)], fill=GOLD_WARM, width=2)
    draw.text((100, 255), "Lead Investigator: Kavi // Hardware Systems Unit", font=FONT_SUB, fill=TEXT_MUTED)

def render_demo_b_environment(canvas: Image.Image, t_sec: float) -> None:
    """
    Demo B: Cleanroom Semiconductor Microscopy Environment.
    Realistic 4nm processor die with logic clusters, HBM channels, and microscope optics.
    Character examines and points toward the compute core.
    """
    draw = ImageDraw.Draw(canvas)
    # Dark cleanroom backdrop
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], fill=(10, 13, 20, 255))

    # Top editorial header
    draw.text((100, 120), "MICROSCOPY HARDWARE INSPECTION", font=FONT_HEADER, fill=CYAN_CORE)
    draw.text((100, 160), "4nm Silicon Microarchitecture", font=FONT_HERO, fill=WHITE_EDITORIAL)

    # Realistic Semiconductor Die Package (Center-Right Hero)
    die_x, die_y = 480, 360
    die_w, die_h = 520, 520

    # Silicon substrate bevel
    draw.rounded_rectangle([die_x - 15, die_y - 15, die_x + die_w + 15, die_y + die_h + 15], radius=16, fill=(24, 30, 42, 255), outline=(50, 65, 90, 255), width=2)
    # Active silicon die surface
    draw.rectangle([die_x, die_y, die_x + die_w, die_y + die_h], fill=(18, 22, 34, 255), outline=CYAN_CORE, width=2)

    # Internal Logic Clusters (4 Quadrants)
    quad_w = 210
    quad_h = 210
    clusters = [
        (die_x + 30, die_y + 30, "LOGIC ARRAY A // TENSOR CORES"),
        (die_x + 280, die_y + 30, "LOGIC ARRAY B // VECTOR REGISTERS"),
        (die_x + 30, die_y + 280, "L2 CACHE // 96MB HIGH BANDWIDTH"),
        (die_x + 280, die_y + 280, "LOGIC ARRAY C // ASYNC WARPS"),
    ]

    for qx, qy, qlabel in clusters:
        draw.rectangle([qx, qy, qx + quad_w, qy + quad_h], fill=(26, 34, 52, 255), outline=(0, 229, 255, 120), width=1)
        # Microscopic transistor circuit trace lines
        for ly in range(qy + 15, qy + quad_h, 25):
            draw.line([(qx + 10, ly), (qx + quad_w - 10, ly)], fill=(0, 229, 255, 50), width=1)
        draw.text((qx + 12, qy + 12), qlabel[:14], font=FONT_MONO, fill=CYAN_CORE)

    # Central interconnect bridge (Target of host pointer)
    bridge_box = [die_x + 200, die_y + 200, die_x + 320, die_y + 320]
    pulse = 0.6 + 0.4 * math.sin(2.0 * math.pi * 1.5 * t_sec)
    draw.rectangle(bridge_box, fill=(255, 171, 0, 40), outline=(255, 171, 0, int(255 * pulse)), width=2)
    draw.text((die_x + 215, die_y + 250), "NOC BUS", font=FONT_LABEL, fill=GOLD_WARM)

    # High-Bandwidth Memory (HBM3e) stacks flanking die
    for hy in [die_y + 40, die_y + 300]:
        draw.rounded_rectangle([die_x + die_w + 35, hy, die_x + die_w + 75, hy + 160], radius=6, fill=(35, 45, 65, 255), outline=GOLD_WARM, width=1)
        draw.text((die_x + die_w + 42, hy + 60), "HBM", font=FONT_MONO, fill=WHITE_EDITORIAL)

    # Editorial Callout leader line
    draw.line([(die_x + 260, die_y + 260), (die_x + 260, die_y + 60), (die_x + 120, die_y + 60)], fill=GOLD_WARM, width=2)
    draw.text((die_x - 140, die_y + 48), "64 BILLION TRANSISTORS", font=FONT_LABEL, fill=GOLD_WARM)

def render_demo_c_environment(canvas: Image.Image, t_sec: float) -> None:
    """
    Demo C: Scientific Pipeline Visualization.
    Asynchronous Warp Specialization dataflow timeline showing compute/transfer overlap.
    Character explains the latency-hiding mechanism.
    """
    draw = ImageDraw.Draw(canvas)
    # Deep slate architectural background
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], fill=(11, 14, 22, 255))

    # Header
    draw.text((100, 120), "SCIENTIFIC PIPELINE ANALYSIS", font=FONT_HEADER, fill=EMERALD_DATA)
    draw.text((100, 160), "Asynchronous Warp Specialization", font=FONT_HERO, fill=WHITE_EDITORIAL)

    # Timeline comparison container
    chart_x, chart_y = 380, 280
    chart_w, chart_h = 630, 560

    draw.rounded_rectangle([chart_x, chart_y, chart_x + chart_w, chart_y + chart_h], radius=16, fill=(18, 23, 36, 255), outline=(40, 52, 75, 255), width=2)

    # 1. Traditional Stalled Pipeline (Top half)
    draw.text((chart_x + 30, chart_y + 30), "TRADITIONAL SYNCHRONOUS PIPELINE", font=FONT_LABEL, fill=TEXT_MUTED)
    # Stage bars
    bar_y = chart_y + 70
    draw.rounded_rectangle([chart_x + 30, bar_y, chart_x + 220, bar_y + 50], radius=8, fill=(30, 40, 60, 255))
    draw.text((chart_x + 50, bar_y + 15), "Memory Load", font=FONT_MONO, fill=TEXT_MUTED)

    # Stall Gap (Red highlight)
    draw.rounded_rectangle([chart_x + 230, bar_y, chart_x + 390, bar_y + 50], radius=8, fill=(239, 68, 68, 40), outline=(239, 68, 68, 200), width=2)
    draw.text((chart_x + 250, bar_y + 15), "STALL GAP", font=FONT_MONO, fill=(239, 68, 68, 255))

    draw.rounded_rectangle([chart_x + 400, bar_y, chart_x + 590, bar_y + 50], radius=8, fill=(30, 40, 60, 255))
    draw.text((chart_x + 420, bar_y + 15), "Tensor Math", font=FONT_MONO, fill=TEXT_MUTED)

    # 2. Asynchronous Overlapping Pipeline (Bottom half - Hero Target)
    draw.text((chart_x + 30, chart_y + 180), "ASYNC WARP SPECIALIZED PIPELINE (ZERO STALL)", font=FONT_LABEL, fill=EMERALD_DATA)

    # Warp A (Producer / Memory)
    p_bar_y = chart_y + 220
    draw.rounded_rectangle([chart_x + 30, p_bar_y, chart_x + 590, p_bar_y + 50], radius=8, fill=(16, 185, 129, 30), outline=EMERALD_DATA, width=2)
    draw.text((chart_x + 45, p_bar_y + 15), "Warp A (Producer): Continuous Global -> Shared Async Prefetch", font=FONT_MONO, fill=EMERALD_DATA)

    # Warp B (Consumer / Compute - Overlapping seamlessly)
    c_bar_y = chart_y + 290
    draw.rounded_rectangle([chart_x + 110, c_bar_y, chart_x + 590, c_bar_y + 50], radius=8, fill=(168, 85, 247, 40), outline=PURPLE_WARP, width=2)
    draw.text((chart_x + 130, c_bar_y + 15), "Warp B (Consumer): Tensor Core Math (100% Latency Hidden)", font=FONT_MONO, fill=PURPLE_WARP)

    # Animated Async Barrier Marker
    barrier_x = chart_x + 110 + int(30 * math.sin(2.0 * math.pi * 1.2 * t_sec))
    draw.line([(barrier_x, p_bar_y - 10), (barrier_x, c_bar_y + 60)], fill=GOLD_WARM, width=3)
    draw.text((barrier_x - 35, c_bar_y + 75), "ASYNC BARRIER", font=FONT_HEADER, fill=GOLD_WARM)

    # Scientific Performance Payoff Metric
    draw.rounded_rectangle([chart_x + 30, chart_y + 440, chart_x + 600, chart_y + 520], radius=12, fill=(14, 18, 28, 255), outline=EMERALD_DATA, width=1)
    draw.text((chart_x + 50, chart_y + 460), "EXECUTION STALLS REDUCTION:", font=FONT_LABEL, fill=WHITE_EDITORIAL)
    draw.text((chart_x + 370, chart_y + 452), "-84.6%", font=FONT_HERO, fill=EMERALD_DATA)

# ---------------------------------------------------------------------------
# Master Demonstration Render Loop
# ---------------------------------------------------------------------------

DEMO_ENV_FUNCS = {
    "demo_a_presenter": render_demo_a_environment,
    "demo_b_investigator": render_demo_b_environment,
    "demo_c_explainer": render_demo_c_environment,
}

def render_demo(spec: Dict[str, Any]) -> Tuple[Path, Path]:
    demo_id = spec["id"]
    audio_path = spec["audio_file"]

    with wave.open(str(audio_path), "rb") as wf:
        total_dur = wf.getnframes() / float(wf.getframerate())
    total_frames = int(math.ceil(total_dur * FPS))

    print(f"\n[DEMO: {demo_id}] Total frames: {total_frames} | Duration: {total_dur:.2f}s")
    demo_frames_dir = FRAMES_DIR / demo_id
    demo_frames_dir.mkdir(parents=True, exist_ok=True)

    char_config = CharacterSceneConfig(
        screen_position=spec["host_pos"],
        scale=spec["host_scale"],
        editorial_reason=f"Render Phase 14.2 {demo_id}"
    )

    env_func = DEMO_ENV_FUNCS[demo_id]
    mid_keyframe_path = KEYFRAMES_DIR / f"{demo_id}_mid_keyframe.png"

    t0 = time.time()
    for frame_idx in range(total_frames):
        t_sec = frame_idx / float(FPS)
        frame = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 255))

        # 1. Render Cinematic Environment (Zero Dashboard UI)
        env_func(frame, t_sec)

        # 2. Render Animated Character Host (Lip sync + Pointing/Gesturing)
        is_speaking = t_sec < (total_dur - 0.2)
        bbox, kin = HOST_ENGINE.composite_onto_canvas(
            canvas=frame,
            t_sec=t_sec,
            config=char_config,
            is_speaking=is_speaking,
            speech_intensity=0.9,
            gesture_mode=spec["gesture"],
            target_xy=spec.get("target_xy"),
            target_label=spec.get("target_label"),
            ambient_tint_hex="#FFE0B2" if demo_id == "demo_a_presenter" else "#00E5FF"
        )

        # 3. Subtitles in Safe Area
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([80, 1660, 1000, 1790], radius=14, fill=(12, 16, 24, 210), outline=(255, 171, 0, 60), width=1)
        # Render clean text wrapped
        draw.text((110, 1685), spec["text"][:55], font=FONT_SUBTITLE, fill=WHITE_EDITORIAL)
        if len(spec["text"]) > 55:
            draw.text((110, 1735), spec["text"][55:110], font=FONT_SUBTITLE, fill=GOLD_WARM)

        # Save Frame
        frame_file = demo_frames_dir / f"frame_{frame_idx:05d}.png"
        frame.save(frame_file)

        # Mid keyframe
        if frame_idx == total_frames // 2:
            frame.save(mid_keyframe_path)
            print(f"  [KEYFRAME] Saved: {mid_keyframe_path}")

        if frame_idx % 45 == 0:
            print(f"  Frame {frame_idx}/{total_frames} (viseme: {kin.get('viseme')}, arm_rot: {kin.get('arm_rot_deg'):.1f}°)...")

    print(f"[DEMO: {demo_id}] Frames rendered in {time.time() - t0:.1f}s")

    # Encode MP4 with FFmpeg
    video_mp4 = VIDEOS_DIR / f"{demo_id}.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(demo_frames_dir / "frame_%05d.png"),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(video_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[DEMO: {demo_id}] Video MP4 encoded: {video_mp4}")
    return video_mp4, mid_keyframe_path

def generate_three_demo_contact_sheet(keyframes: List[Path]) -> Path:
    """Generates 3-panel contact sheet across Demo A, Demo B, Demo C."""
    thumbs = [Image.open(kf).resize((360, 640), Image.Resampling.LANCZOS) for kf in keyframes]
    sheet = Image.new("RGBA", (len(thumbs) * 360, 640), (8, 12, 18, 255))
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, (i * 360, 0))

    sheet_p = PROD_DIR / "phase14_2_three_demonstrations_contact_sheet.png"
    sheet.save(sheet_p)
    print(f"\n[CONTACT SHEET] Saved: {sheet_p}")
    return sheet_p

def main():
    print("=" * 80)
    print("SUPER.INTELLIGENCEEE — PHASE 14.2 CHARACTER ANIMATION DEMONSTRATIONS")
    print("=" * 80)

    keyframes = []
    videos = []

    for spec in DEMO_SPECS:
        v_path, kf_path = render_demo(spec)
        videos.append(v_path)
        keyframes.append(kf_path)

    contact_sheet = generate_three_demo_contact_sheet(keyframes)

    print("\n" + "=" * 80)
    print("ALL 3 CHARACTER DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
    for v in videos:
        print(f"  - Video: {v}")
    print(f"  - Master Contact Sheet: {contact_sheet}")
    print("=" * 80)

if __name__ == "__main__":
    main()
