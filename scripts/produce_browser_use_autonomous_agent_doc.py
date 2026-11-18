"""
SUPER.INTELLIGENCEEE — Flagship Autonomous Agent Documentary Producer
Topic: "The GitHub repo that turns AI into an autonomous OS agent" (browser-use/browser-use)
Duration: ~37.0 seconds (5 Scenes)
Features:
- Animated host character (character.me.png) with speech-synchronized visemes (mouth movement)
- Dynamic hand movements & pointing gestures with holographic HUD laser targeting
- High-fidelity tech documentary graphics (GitHub repo card, live Vision DOM coordinate tags, execution terminal)
- Kokoro-82M am_liam voiceover mastered to -16 LUFS with ducked ambient synth bed
- Two-line safe-area subtitle track with word-level highlighting
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
from rendering.advanced_subtitle_engine import AdvancedSubtitleEngine

# ---------------------------------------------------------------------------
# Directories & Constants
# ---------------------------------------------------------------------------

PROD_DIR = WORKSPACE_ROOT / "output" / "browser_use_doc"
AUDIO_DIR = PROD_DIR / "audio"
FRAMES_DIR = PROD_DIR / "frames"
SCENES_DIR = PROD_DIR / "scenes"
KEYFRAMES_DIR = PROD_DIR / "keyframes"

for d in (PROD_DIR, AUDIO_DIR, FRAMES_DIR, SCENES_DIR, KEYFRAMES_DIR):
    d.mkdir(parents=True, exist_ok=True)

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
FPS = 30

# Colors
BG_DEEP = (10, 14, 22, 255)
BG_CARD = (18, 24, 38, 230)
BORDER_TEAL = (0, 229, 255, 120)
BORDER_SUBTLE = (30, 42, 60, 200)

CYAN_PRIMARY = (0, 229, 255, 255)
AMBER_ACCENT = (255, 171, 0, 255)
ORANGE_HOST = (255, 107, 0, 255)
GREEN_SUCCESS = (16, 185, 129, 255)
PURPLE_AGENT = (168, 85, 247, 255)
WHITE_BRIGHT = (248, 250, 252, 255)
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

FONT_HEADER_TAG = get_font(22, bold=True, mono=True)
FONT_HERO = get_font(42, bold=True)
FONT_TITLE = get_font(32, bold=True)
FONT_SUB = get_font(24, bold=False)
FONT_MONO = get_font(20, bold=True, mono=True)
FONT_LABEL = get_font(18, bold=True)
FONT_SUBTITLE = get_font(36, bold=True)

# Engines
HOST_ENGINE = AnimatedCharacterHost(workspace_root=WORKSPACE_ROOT)
SUBTITLE_ENGINE = AdvancedSubtitleEngine()

# ---------------------------------------------------------------------------
# Scene Specifications
# ---------------------------------------------------------------------------

SCENE_SPECS = [
    {
        "id": "scene1_hook",
        "audio_file": AUDIO_DIR / "scene1_hook_speech.wav",
        "text": "Chatbots are stuck inside text boxes. But this open source GitHub repo just broke them out into the real operating system.",
        "top_tag": "[ SPECIAL REPORT: THE AUTONOMOUS OS REVOLUTION ]",
        "host_pos": CharacterScreenPosition.CENTER_HERO,
        "host_scale": 0.70,
        "gesture": "explaining",
        "target_xy": None,
        "target_label": None,
    },
    {
        "id": "scene2_repo",
        "audio_file": AUDIO_DIR / "scene2_repo_speech.wav",
        "text": "Meet Browser Use. With over fifty-two thousand GitHub stars, it gives any AI actual eyes and hands to operate your desktop browser.",
        "top_tag": "[ REPOSITORY SPOTLIGHT: browser-use/browser-use ]",
        "host_pos": CharacterScreenPosition.LOWER_LEFT,
        "host_scale": 0.62,
        "gesture": "pointing",
        "target_xy": (780, 520),  # Pointing at GitHub Stars Card
        "target_label": "52.8k GITHUB STARS",
    },
    {
        "id": "scene3_engine",
        "audio_file": AUDIO_DIR / "scene3_engine_speech.wav",
        "text": "Instead of guessing code, it converts every button, input, and link into interactive visual coordinate tags that the model clicks and types into autonomously.",
        "top_tag": "[ SYSTEM ARCHITECTURE: VISION-COORDINATE DOM TAGGING ]",
        "host_pos": CharacterScreenPosition.LOWER_LEFT,
        "host_scale": 0.60,
        "gesture": "pointing",
        "target_xy": (760, 680),  # Pointing at Interactive Bounding Box [3]
        "target_label": "ELEMENT [3]: AUTONOMOUS CLICK",
    },
    {
        "id": "scene4_power",
        "audio_file": AUDIO_DIR / "scene4_power_speech.wav",
        "text": "From booking flights to navigating complex enterprise dashboards, AI is no longer just talking. It is doing the work.",
        "top_tag": "[ CAPABILITY MATRIX: BROWSER AGENT BENCHMARK ]",
        "host_pos": CharacterScreenPosition.LOWER_LEFT,
        "host_scale": 0.62,
        "gesture": "pointing",
        "target_xy": (780, 620),  # Pointing at 89.4% Benchmark Result
        "target_label": "89.4% TASK SUCCESS RATE",
    },
    {
        "id": "scene5_cta",
        "audio_file": AUDIO_DIR / "scene5_cta_speech.wav",
        "text": "Star the repo, and follow Super Intelligence to stay ahead of the autonomous future.",
        "top_tag": "[ SUPER.INTELLIGENCEEE: NEXT GENERATION COMPUTE ]",
        "host_pos": CharacterScreenPosition.CENTER_HERO,
        "host_scale": 0.70,
        "gesture": "explaining",
        "target_xy": None,
        "target_label": None,
    },
]

# ---------------------------------------------------------------------------
# Background & Graphics Renderers
# ---------------------------------------------------------------------------

def render_background_grid(width: int = CANVAS_WIDTH, height: int = CANVAS_HEIGHT) -> Image.Image:
    """Renders a sleek, dark engineering background with subtle perspective grid lines."""
    im = Image.new("RGBA", (width, height), BG_DEEP)
    draw = ImageDraw.Draw(im)

    # Vertical tech grid lines
    for x in range(60, width, 120):
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48, 80), width=1)

    # Horizontal tech grid lines
    for y in range(80, height, 160):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48, 80), width=1)

    # Ambient radial glow at top-center
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([width//2 - 400, 200, width//2 + 400, 1000], fill=(0, 229, 255, 12))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=60))
    im = Image.alpha_composite(im, glow)

    return im

def draw_top_header(canvas: Image.Image, tag_text: str, t_sec: float) -> None:
    """Renders technical top bar with live pulsing status indicator."""
    draw = ImageDraw.Draw(canvas)
    # Background pill
    draw.rounded_rectangle([70, 70, 1010, 125], radius=8, fill=(15, 20, 32, 230), outline=BORDER_SUBTLE, width=1)

    # Pulsing live indicator
    pulse = 0.5 + 0.5 * math.sin(2.0 * math.pi * 1.5 * t_sec)
    p_color = (0, 229, 255, int(255 * pulse))
    draw.ellipse([95, 93, 107, 105], fill=p_color)

    # Tag text
    draw.text((125, 87), tag_text, font=FONT_HEADER_TAG, fill=CYAN_PRIMARY)

def draw_subtitles(canvas: Image.Image, text: str, t_sec: float, total_dur: float) -> None:
    """
    Renders synchronized subtitles in the safe zone (y=1640..1820).
    Word-level highlighting creates lockstep alignment with host mouth visemes.
    """
    draw = ImageDraw.Draw(canvas)
    words = text.split()
    if not words:
        return

    # Fraction of progress through sentence
    progress = max(0.0, min(1.0, t_sec / max(0.1, total_dur)))
    active_idx = int(progress * len(words))

    # Split into 2 lines if long
    half = len(words) // 2 if len(words) > 6 else len(words)
    line1 = words[:half]
    line2 = words[half:]

    # Bounding pill in safe area
    draw.rounded_rectangle([80, 1660, 1000, 1800], radius=16, fill=(12, 16, 24, 210), outline=(0, 229, 255, 60), width=1)

    # Draw line 1
    x_cursor = 110
    y_line1 = 1680
    for i, w in enumerate(line1):
        color = AMBER_ACCENT if i == active_idx else (WHITE_BRIGHT if i < active_idx else TEXT_MUTED)
        bbox = draw.textbbox((x_cursor, y_line1), w + " ", font=FONT_SUBTITLE)
        draw.text((x_cursor, y_line1), w, font=FONT_SUBTITLE, fill=color)
        x_cursor = bbox[2]

    # Draw line 2
    if line2:
        x_cursor = 110
        y_line2 = 1735
        for i, w in enumerate(line2, start=half):
            color = AMBER_ACCENT if i == active_idx else (WHITE_BRIGHT if i < active_idx else TEXT_MUTED)
            bbox = draw.textbbox((x_cursor, y_line2), w + " ", font=FONT_SUBTITLE)
            draw.text((x_cursor, y_line2), w, font=FONT_SUBTITLE, fill=color)
            x_cursor = bbox[2]

# ---------------------------------------------------------------------------
# Scene Graphic Renderers
# ---------------------------------------------------------------------------

def render_scene1_graphics(canvas: Image.Image, t_sec: float) -> None:
    """Scene 1: Shattered Chatbot Text Box & Autonomous Agent Escape."""
    draw = ImageDraw.Draw(canvas)

    # Center card: Chatbot Window
    card_box = [160, 240, 920, 680]
    draw.rounded_rectangle(card_box, radius=16, fill=BG_CARD, outline=(0, 229, 255, 140), width=2)

    # Chat header
    draw.rounded_rectangle([160, 240, 920, 310], radius=16, fill=(24, 32, 50, 255))
    draw.ellipse([190, 265, 205, 280], fill=(239, 68, 68, 255))  # Red close
    draw.ellipse([215, 265, 230, 280], fill=(245, 158, 11, 255)) # Yellow min
    draw.ellipse([240, 265, 255, 280], fill=(16, 185, 129, 255)) # Green max
    draw.text((280, 262), "Traditional LLM Chatbot [ ISOLATED CONTAINER ]", font=FONT_MONO, fill=TEXT_MUTED)

    # Prompt bubble
    draw.rounded_rectangle([200, 340, 880, 420], radius=10, fill=(35, 45, 70, 220))
    draw.text((225, 362), "User: 'Can you go book my flight and submit the form?'", font=FONT_SUB, fill=WHITE_BRIGHT)

    # Broken response box with fracture lines
    draw.rounded_rectangle([200, 450, 880, 560], radius=10, fill=(20, 25, 38, 240), outline=(239, 68, 68, 180), width=2)
    draw.text((225, 470), "AI: 'I am only a text model. I cannot browse or touch your OS.'", font=FONT_SUB, fill=(239, 120, 120, 255))
    draw.text((225, 510), "[ SYSTEM LIMIT: ZERO EXECUTION CAPABILITY ]", font=FONT_MONO, fill=(239, 68, 68, 255))

    # Autonomous Breakthrough Banner below
    break_pulse = 0.5 + 0.5 * math.sin(2.0 * math.pi * 1.8 * t_sec)
    b_alpha = int(255 * break_pulse)
    draw.rounded_rectangle([180, 600, 900, 660], radius=12, fill=(0, 229, 255, 30), outline=(0, 229, 255, b_alpha), width=2)
    draw.text((240, 618), "⚡ BREAKING OUT: AUTONOMOUS OS OPERATION ⚡", font=FONT_MONO, fill=CYAN_PRIMARY)

def render_scene2_graphics(canvas: Image.Image, t_sec: float) -> None:
    """Scene 2: GitHub Repository Card & Live Star Surge."""
    draw = ImageDraw.Draw(canvas)

    # Main Repo Card
    card_box = [320, 200, 1010, 820]
    draw.rounded_rectangle(card_box, radius=20, fill=BG_CARD, outline=BORDER_TEAL, width=2)

    # Repo Header
    draw.text((360, 235), "REPOSITORY", font=FONT_HEADER_TAG, fill=AMBER_ACCENT)
    draw.text((360, 275), "browser-use / browser-use", font=FONT_HERO, fill=WHITE_BRIGHT)
    draw.text((360, 335), "Make websites accessible for AI agents.", font=FONT_SUB, fill=TEXT_MUTED)

    # Badges Grid
    # 1. Star Badge (Pointed target)
    star_pulse = 0.8 + 0.2 * math.sin(2.0 * math.pi * 2.0 * t_sec)
    s_alpha = int(255 * star_pulse)
    draw.rounded_rectangle([360, 390, 640, 480], radius=12, fill=(255, 171, 0, 30), outline=(255, 171, 0, s_alpha), width=2)
    draw.text((380, 405), "★ STARS", font=FONT_MONO, fill=AMBER_ACCENT)
    draw.text((380, 432), "52,840", font=FONT_TITLE, fill=WHITE_BRIGHT)

    # 2. Forks Badge
    draw.rounded_rectangle([660, 390, 960, 480], radius=12, fill=(20, 30, 48, 200), outline=BORDER_SUBTLE, width=1)
    draw.text((685, 405), "⑂ FORKS", font=FONT_MONO, fill=CYAN_PRIMARY)
    draw.text((685, 432), "5,420+", font=FONT_TITLE, fill=WHITE_BRIGHT)

    # Tech Architecture Flow
    draw.rounded_rectangle([360, 510, 960, 670], radius=14, fill=(15, 20, 34, 220), outline=BORDER_SUBTLE, width=1)
    draw.text((385, 528), "ARCHITECTURE PIPELINE", font=FONT_MONO, fill=TEXT_MUTED)
    
    # 3 Pipeline Steps
    draw.rounded_rectangle([385, 570, 525, 645], radius=8, fill=(30, 40, 65, 255))
    draw.text((405, 585), "1. LLM Core", font=FONT_LABEL, fill=WHITE_BRIGHT)
    draw.text((405, 612), "Claude/GPT-4o", font=FONT_MONO, fill=CYAN_PRIMARY)

    draw.text((545, 595), "➔", font=FONT_TITLE, fill=AMBER_ACCENT)

    draw.rounded_rectangle([595, 570, 755, 645], radius=8, fill=(30, 40, 65, 255), outline=BORDER_TEAL, width=1)
    draw.text((615, 585), "2. Browser-Use", font=FONT_LABEL, fill=AMBER_ACCENT)
    draw.text((615, 612), "DOM Ingestion", font=FONT_MONO, fill=WHITE_BRIGHT)

    draw.text((775, 595), "➔", font=FONT_TITLE, fill=AMBER_ACCENT)

    draw.rounded_rectangle([820, 570, 940, 645], radius=8, fill=(30, 40, 65, 255))
    draw.text((835, 585), "3. Browser", font=FONT_LABEL, fill=GREEN_SUCCESS)
    draw.text((835, 612), "Chromium", font=FONT_MONO, fill=TEXT_MUTED)

    # Star rating tag
    draw.text((360, 700), "Fastest Growing Open-Source AI Agent of 2026", font=FONT_LABEL, fill=CYAN_PRIMARY)

def render_scene3_graphics(canvas: Image.Image, t_sec: float) -> None:
    """Scene 3: Chromium Simulation with Vision DOM Coordinate Tags [1], [2], [3]."""
    draw = ImageDraw.Draw(canvas)

    # Simulated Browser Window
    card_box = [300, 180, 1020, 850]
    draw.rounded_rectangle(card_box, radius=18, fill=(14, 18, 28, 240), outline=BORDER_TEAL, width=2)

    # Browser Navigation Bar
    draw.rounded_rectangle([300, 180, 1020, 245], radius=18, fill=(22, 28, 44, 255))
    draw.ellipse([325, 205, 337, 217], fill=(239, 68, 68, 255))
    draw.ellipse([345, 205, 357, 217], fill=(245, 158, 11, 255))
    draw.ellipse([365, 205, 377, 217], fill=(16, 185, 129, 255))
    # URL bar
    draw.rounded_rectangle([395, 195, 990, 230], radius=8, fill=(12, 16, 26, 255))
    draw.text((415, 202), "🔒 https://enterprise.airline.internal/search-flights", font=FONT_MONO, fill=CYAN_PRIMARY)

    # Webpage UI with Coordinate Bounding Boxes
    # Tag [1] Departure Input
    draw.rounded_rectangle([340, 280, 970, 350], radius=10, fill=(24, 32, 50, 255), outline=(0, 229, 255, 180), width=2)
    # Coordinate Badge [1]
    draw.rectangle([340, 280, 385, 310], fill=CYAN_PRIMARY)
    draw.text((350, 285), "[1]", font=FONT_MONO, fill=(0, 0, 0, 255))
    draw.text((405, 302), "Origin: San Francisco (SFO)", font=FONT_SUB, fill=WHITE_BRIGHT)

    # Tag [2] Destination Input
    draw.rounded_rectangle([340, 380, 970, 450], radius=10, fill=(24, 32, 50, 255), outline=(255, 171, 0, 180), width=2)
    draw.rectangle([340, 380, 385, 410], fill=AMBER_ACCENT)
    draw.text((350, 385), "[2]", font=FONT_MONO, fill=(0, 0, 0, 255))
    draw.text((405, 402), "Destination: Tokyo Haneda (HND)", font=FONT_SUB, fill=WHITE_BRIGHT)

    # Tag [3] Search Flights Button (Target of Host Pointing)
    click_pulse = 0.7 + 0.3 * math.sin(2.0 * math.pi * 2.5 * t_sec)
    c_alpha = int(255 * click_pulse)
    draw.rounded_rectangle([340, 480, 970, 560], radius=10, fill=(16, 185, 129, 40), outline=(16, 185, 129, c_alpha), width=3)
    draw.rectangle([340, 480, 385, 510], fill=(16, 185, 129, 255))
    draw.text((350, 485), "[3]", font=FONT_MONO, fill=(0, 0, 0, 255))
    draw.text((405, 505), "✈  SEARCH & CONFIRM FLIGHT SEATS", font=FONT_TITLE, fill=GREEN_SUCCESS)

    # Autonomous Action Terminal below
    draw.rounded_rectangle([340, 590, 970, 770], radius=12, fill=(10, 12, 18, 255), outline=BORDER_SUBTLE, width=1)
    draw.text((360, 605), "AGENT REASONING TRACE (v0.12)", font=FONT_HEADER_TAG, fill=AMBER_ACCENT)
    draw.text((360, 640), "> Parsed DOM: 184 nodes -> 14 interactive tags", font=FONT_MONO, fill=TEXT_MUTED)
    draw.text((360, 670), "> Action: click_element(coordinate_id=3)", font=FONT_MONO, fill=CYAN_PRIMARY)
    draw.text((360, 700), "> State: HTTP 200 OK | Autonomously confirmed.", font=FONT_MONO, fill=GREEN_SUCCESS)

def render_scene4_graphics(canvas: Image.Image, t_sec: float) -> None:
    """Scene 4: Enterprise Benchmark & Autonomous Capability Matrix."""
    draw = ImageDraw.Draw(canvas)

    card_box = [300, 200, 1020, 840]
    draw.rounded_rectangle(card_box, radius=20, fill=BG_CARD, outline=BORDER_TEAL, width=2)

    draw.text((340, 235), "PERFORMANCE BENCHMARK", font=FONT_HEADER_TAG, fill=AMBER_ACCENT)
    draw.text((340, 275), "Real-World Task Success", font=FONT_HERO, fill=WHITE_BRIGHT)

    # Benchmark Bar 1: WebVoyager Success Rate (Host Target)
    draw.rounded_rectangle([340, 350, 970, 460], radius=14, fill=(20, 28, 45, 255), outline=BORDER_TEAL, width=2)
    draw.text((365, 370), "WebVoyager Agent Benchmark", font=FONT_TITLE, fill=WHITE_BRIGHT)
    # Animated Progress bar
    fill_w = int(550 * 0.894)
    draw.rounded_rectangle([365, 415, 930, 435], radius=6, fill=(35, 45, 70, 255))
    draw.rounded_rectangle([365, 415, 365 + fill_w, 435], radius=6, fill=CYAN_PRIMARY)
    draw.text((810, 370), "89.4%", font=FONT_HERO, fill=CYAN_PRIMARY)

    # Capability Features
    caps = [
        ("Multi-Tab Browser Routing", "PARALLEL AGENT ISOLATION", GREEN_SUCCESS),
        ("Encrypted Cookie Persistence", "AUTHENTICATED SESSION REUSE", AMBER_ACCENT),
        ("Human-in-the-Loop 2FA", "PAUSES SAFELY FOR APPROVAL", CYAN_PRIMARY),
    ]

    y_pos = 490
    for title, desc, col in caps:
        draw.rounded_rectangle([340, y_pos, 970, y_pos + 75], radius=10, fill=(15, 20, 32, 230), outline=BORDER_SUBTLE, width=1)
        draw.text((365, y_pos + 12), f"✔ {title}", font=FONT_LABEL, fill=WHITE_BRIGHT)
        draw.text((365, y_pos + 42), desc, font=FONT_MONO, fill=col)
        y_pos += 90

    draw.text((340, 785), "Verified across 1,000+ autonomous enterprise tasks.", font=FONT_LABEL, fill=TEXT_MUTED)

def render_scene5_graphics(canvas: Image.Image, t_sec: float) -> None:
    """Scene 5: Call to Action, Star Button, and Super Intelligence Brand."""
    draw = ImageDraw.Draw(canvas)

    card_box = [160, 240, 920, 720]
    draw.rounded_rectangle(card_box, radius=20, fill=BG_CARD, outline=BORDER_TEAL, width=2)

    draw.text((240, 280), "AUTONOMOUS INTELLIGENCE", font=FONT_HEADER_TAG, fill=AMBER_ACCENT)
    draw.text((240, 320), "Super.intelligence", font=FONT_HERO, fill=WHITE_BRIGHT)
    draw.text((240, 380), "Explore the code shaping the next generation.", font=FONT_SUB, fill=TEXT_MUTED)

    # Animated Star Button
    s_pulse = 0.7 + 0.3 * math.sin(2.0 * math.pi * 2.0 * t_sec)
    s_alpha = int(255 * s_pulse)
    draw.rounded_rectangle([240, 440, 840, 530], radius=14, fill=(255, 171, 0, 40), outline=(255, 171, 0, s_alpha), width=3)
    draw.text((310, 465), "★  STAR: browser-use/browser-use", font=FONT_TITLE, fill=AMBER_ACCENT)

    # Follow Channel Button
    draw.rounded_rectangle([240, 560, 840, 650], radius=14, fill=(0, 229, 255, 30), outline=(0, 229, 255, 200), width=2)
    draw.text((330, 585), "FOLLOW @SUPER.INTELLIGENCEEE", font=FONT_TITLE, fill=CYAN_PRIMARY)

# ---------------------------------------------------------------------------
# Master Scene Render Loop
# ---------------------------------------------------------------------------

SCENE_GRAPHIC_FUNCS = {
    "scene1_hook": render_scene1_graphics,
    "scene2_repo": render_scene2_graphics,
    "scene3_engine": render_scene3_graphics,
    "scene4_power": render_scene4_graphics,
    "scene5_cta": render_scene5_graphics,
}

def render_single_scene(spec: Dict[str, Any], bg_template: Image.Image) -> Path:
    """Renders all frames for a scene and encodes into MP4."""
    scene_id = spec["id"]
    audio_path = spec["audio_file"]

    # Calculate duration and frame count from WAV
    with wave.open(str(audio_path), "rb") as wf:
        total_dur = wf.getnframes() / float(wf.getframerate())
    total_frames = int(math.ceil(total_dur * FPS))

    print(f"\n[SCENE: {scene_id}] Frames: {total_frames} | Duration: {total_dur:.2f}s")

    scene_frames_dir = FRAMES_DIR / scene_id
    scene_frames_dir.mkdir(parents=True, exist_ok=True)

    char_config = CharacterSceneConfig(
        screen_position=spec["host_pos"],
        scale=spec["host_scale"],
        editorial_reason=f"Render {scene_id} autonomous documentary"
    )

    graphic_func = SCENE_GRAPHIC_FUNCS[scene_id]

    t0 = time.time()
    for frame_idx in range(total_frames):
        t_sec = frame_idx / float(FPS)

        # 1. Background Grid
        frame = bg_template.copy()

        # 2. Top Header
        draw_top_header(frame, spec["top_tag"], t_sec)

        # 3. Scene Graphics
        graphic_func(frame, t_sec)

        # 4. Host Character (Speech Visemes + Pointing/Gesturing Rig)
        is_speaking = t_sec < (total_dur - 0.2)
        bbox, kin = HOST_ENGINE.composite_onto_canvas(
            canvas=frame,
            t_sec=t_sec,
            config=char_config,
            is_speaking=is_speaking,
            speech_intensity=0.9,
            gesture_mode=spec["gesture"],
            target_xy=spec["target_xy"],
            target_label=spec["target_label"],
            ambient_tint_hex="#00E5FF"
        )

        # 5. Subtitles Track
        draw_subtitles(frame, spec["text"], t_sec, total_dur)

        # Save Frame
        frame_path = scene_frames_dir / f"frame_{frame_idx:05d}.png"
        frame.save(frame_path)

        # Save forensic keyframe at midpoint
        if frame_idx == total_frames // 2:
            key_path = KEYFRAMES_DIR / f"{scene_id}_mid_keyframe.png"
            frame.save(key_path)
            print(f"  [KEYFRAME] Saved: {key_path}")

        if frame_idx % 60 == 0:
            print(f"  Rendered {frame_idx}/{total_frames} frames (Viseme: {kin.get('viseme')}, Pointing: {kin.get('pointing_active')})...")

    render_time = time.time() - t0
    print(f"[SCENE: {scene_id}] Rendered in {render_time:.1f}s ({total_frames/max(0.1, render_time):.1f} FPS)")

    # Encode with FFmpeg
    scene_mp4 = SCENES_DIR / f"{scene_id}.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(scene_frames_dir / "frame_%05d.png"),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(scene_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[SCENE: {scene_id}] Encoded MP4: {scene_mp4}")
    return scene_mp4

def compile_master_video(scene_mp4s: List[Path]) -> Path:
    """Concatenates scene MP4s into master documentary."""
    concat_list = PROD_DIR / "scenes_concat.txt"
    with open(concat_list, "w") as f:
        for p in scene_mp4s:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    master_mp4 = PROD_DIR / "browser_use_autonomous_agent_master.mp4"
    print(f"\n[MASTER] Concatenating {len(scene_mp4s)} scenes into: {master_mp4}")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(master_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[MASTER] Master documentary compiled successfully: {master_mp4}")
    return master_mp4

def generate_contact_sheet() -> Path:
    """Combines all scene keyframes into a forensic verification contact sheet."""
    keyframes = sorted(KEYFRAMES_DIR.glob("*_mid_keyframe.png"))
    if not keyframes:
        return None

    # Load images and scale down to 360x640
    thumbs = [Image.open(kf).resize((360, 640), Image.Resampling.LANCZOS) for kf in keyframes]
    cols = min(5, len(thumbs))
    rows = int(math.ceil(len(thumbs) / float(cols)))

    sheet = Image.new("RGBA", (cols * 360, rows * 640), (8, 12, 18, 255))
    for i, thumb in enumerate(thumbs):
        gx = (i % cols) * 360
        gy = (i // cols) * 640
        sheet.paste(thumb, (gx, gy))

    sheet_path = PROD_DIR / "browser_use_contact_sheet.png"
    sheet.save(sheet_path)
    print(f"[CONTACT SHEET] Generated: {sheet_path}")
    return sheet_path

# ---------------------------------------------------------------------------
# Main Execution Entrypoint
# ---------------------------------------------------------------------------

def main():
    print("=" * 80)
    print("SUPER.INTELLIGENCEEE — AUTONOMOUS AGENT DOCUMENTARY PRODUCTION")
    print("Topic: The GitHub Repo That Turns AI Into An Autonomous OS Agent")
    print("=" * 80)

    # 1. Pre-render Background Template
    bg_template = render_background_grid()

    # 2. Render All 5 Scenes
    scene_mp4s = []
    for spec in SCENE_SPECS:
        mp4_path = render_single_scene(spec, bg_template)
        scene_mp4s.append(mp4_path)

    # 3. Compile Master MP4
    master_mp4 = compile_master_video(scene_mp4s)

    # 4. Generate Forensic Verification Contact Sheet
    contact_sheet = generate_contact_sheet()

    print("\n" + "=" * 80)
    print("PRODUCTION COMPLETED SUCCESSFULLY!")
    print(f"Master Video: {master_mp4}")
    if contact_sheet:
        print(f"Contact Sheet: {contact_sheet}")
    print("=" * 80)

if __name__ == "__main__":
    main()
