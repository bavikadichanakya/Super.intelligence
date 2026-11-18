"""
SUPER.INTELLIGENCEEE — Phase 14.1 Reconstructed Cinematic Documentary
Topic: "Browser-Use: The Autonomous Web Operating Agent"
Duration: ~46-48 seconds (6 Reconstructed Scenes)
Core Mandates:
- ZERO default dashboard UI, zero cyan grid, zero floating neon boxes
- Meaningful physical & software environments (Workstation, Browser Viewport, Exploded DOM, IDE Code, Ecosystem Metaphor, Studio)
- Reconstructed host character participation: selective narrative entry (Scene 1, Scene 3, Scene 6)
- Accurate pencil tip tracking with outward pointing beam (zero face overlap)
- Large, high-contrast, safe-area editorial subtitles (safe area y=1640..1820)
- Verified technical facts (zero fabricated benchmarks)
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

from typing import Any, Dict, List, Tuple, Optional
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

PROD_DIR = WORKSPACE_ROOT / "output" / "phase14_1_cinematic"
AUDIO_DIR = PROD_DIR / "audio"
FRAMES_DIR = PROD_DIR / "frames"
SCENES_DIR = PROD_DIR / "scenes"
KEYFRAMES_DIR = PROD_DIR / "keyframes"

for d in (PROD_DIR, AUDIO_DIR, FRAMES_DIR, SCENES_DIR, KEYFRAMES_DIR):
    d.mkdir(parents=True, exist_ok=True)

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
FPS = 30

# Sophisticated Editorial Color Palette
COLOR_OBSIDIAN = (10, 12, 18, 255)
COLOR_DEEP_SLATE = (16, 20, 30, 255)
COLOR_WARM_STUDIO = (20, 18, 16, 255)

ACCENT_GOLD = (234, 179, 8, 255)
ACCENT_AMBER = (255, 171, 0, 255)
ACCENT_CYAN = (0, 229, 255, 255)
ACCENT_EMERALD = (16, 185, 129, 255)
ACCENT_PURPLE = (168, 85, 247, 255)
ACCENT_RED_WARN = (239, 68, 68, 255)

TEXT_HEADLINE = (248, 250, 252, 255)
TEXT_MUTED = (148, 163, 184, 255)
BORDER_EDITORIAL = (45, 55, 75, 200)

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

FONT_HEADER = get_font(20, bold=True, mono=True)
FONT_HERO = get_font(42, bold=True)
FONT_TITLE = get_font(32, bold=True)
FONT_SUB = get_font(24, bold=False)
FONT_LABEL = get_font(20, bold=True)
FONT_MONO = get_font(18, bold=True, mono=True)
FONT_SUBTITLE = get_font(34, bold=True)

HOST_ENGINE = AnimatedCharacterHost(workspace_root=WORKSPACE_ROOT)

# ---------------------------------------------------------------------------
# Reconstructed 6-Scene Specifications
# ---------------------------------------------------------------------------

SCENE_SPECS = [
    {
        "id": "scene1_problem",
        "title": "Scene 1: The Problem — Repetitive Browser Friction",
        "audio_file": AUDIO_DIR / "scene1_problem_speech.wav",
        "text": "Every day, millions of people waste hours clicking, scrolling, and copying data between repetitive web forms.",
        "has_character": True,
        "host_pos": CharacterScreenPosition.LOWER_RIGHT,
        "host_scale": 0.58,
        "gesture": "explaining",
        "target_xy": None,
    },
    {
        "id": "scene2_discovery",
        "title": "Scene 2: The Discovery — Enter Browser-Use",
        "audio_file": AUDIO_DIR / "scene2_discovery_speech.wav",
        "text": "Enter Browser Use, the open source project that gives large language models direct control over a live web browser.",
        "has_character": False, # Technology is hero
        "host_pos": None,
        "host_scale": None,
        "gesture": "idle",
        "target_xy": None,
    },
    {
        "id": "scene3_mechanism",
        "title": "Scene 3: How It Works — Vision-Coordinate DOM Tagging",
        "audio_file": AUDIO_DIR / "scene3_mechanism_speech.wav",
        "text": "The engine extracts the browsers accessibility tree, indexes interactive elements with coordinate tags, and translates model decisions into native Chrome DevTools actions.",
        "has_character": True,
        "host_pos": CharacterScreenPosition.LOWER_LEFT,
        "host_scale": 0.58,
        "gesture": "pointing",
        "target_xy": (780, 560), # Clean target on coordinate tag [2]
        "target_label": "TAG [2]: ACCESSIBILITY NODE",
    },
    {
        "id": "scene4_workflow",
        "title": "Scene 4: Real Demonstration — Python Agent Execution",
        "audio_file": AUDIO_DIR / "scene4_workflow_speech.wav",
        "text": "With just a single Python command, the agent navigates complex multi-step workflows, handling authenticated sessions and unexpected page states.",
        "has_character": False, # Code takes full visual focus
        "host_pos": None,
        "host_scale": None,
        "gesture": "idle",
        "target_xy": None,
    },
    {
        "id": "scene5_significance",
        "title": "Scene 5: What Makes It Important — The Autonomous Leap",
        "audio_file": AUDIO_DIR / "scene5_significance_speech.wav",
        "text": "This marks the fundamental shift from passive chatbots that can only write text, to active agents that interact with the physical and digital world.",
        "has_character": False, # Macro visual metaphor
        "host_pos": None,
        "host_scale": None,
        "gesture": "idle",
        "target_xy": None,
    },
    {
        "id": "scene6_closing",
        "title": "Scene 6: Closing Takeaway — The Production Era",
        "audio_file": AUDIO_DIR / "scene6_closing_speech.wav",
        "text": "The autonomous future is no longer a research paper—it is running in production code. Follow Super Intelligence to understand whats next.",
        "has_character": True,
        "host_pos": CharacterScreenPosition.CENTER_HERO,
        "host_scale": 0.70,
        "gesture": "explaining",
        "target_xy": None,
    },
]

# ---------------------------------------------------------------------------
# Reconstructed Cinematic Visual Environments
# ---------------------------------------------------------------------------

def draw_safe_subtitles(canvas: Image.Image, text: str, t_sec: float, total_dur: float) -> None:
    """Renders elegant, large editorial subtitles in the guaranteed safe area."""
    draw = ImageDraw.Draw(canvas)
    words = text.split()
    if not words:
        return

    progress = max(0.0, min(1.0, t_sec / max(0.1, total_dur)))
    active_idx = int(progress * len(words))

    # Split into 2 lines
    half = len(words) // 2 if len(words) > 6 else len(words)
    line1 = words[:half]
    line2 = words[half:]

    # Translucent pill in safe area (y: 1660..1800)
    draw.rounded_rectangle([80, 1660, 1000, 1800], radius=16, fill=(12, 15, 22, 230), outline=(255, 171, 0, 70), width=1)

    x1 = 110
    y1 = 1685
    for i, w in enumerate(line1):
        color = ACCENT_AMBER if i == active_idx else (TEXT_HEADLINE if i < active_idx else TEXT_MUTED)
        bbox = draw.textbbox((x1, y1), w + " ", font=FONT_SUBTITLE)
        draw.text((x1, y1), w, font=FONT_SUBTITLE, fill=color)
        x1 = bbox[2]

    if line2:
        x2 = 110
        y2 = 1735
        for i, w in enumerate(line2, start=half):
            color = ACCENT_AMBER if i == active_idx else (TEXT_HEADLINE if i < active_idx else TEXT_MUTED)
            bbox = draw.textbbox((x2, y2), w + " ", font=FONT_SUBTITLE)
            draw.text((x2, y2), w, font=FONT_SUBTITLE, fill=color)
            x2 = bbox[2]

def render_scene1_problem(canvas: Image.Image, t_sec: float) -> None:
    """Scene 1: Repetitive Desktop Workstation & Manual Form Friction."""
    draw = ImageDraw.Draw(canvas)
    # 1. Warm workstation lighting gradient
    for y in range(CANVAS_HEIGHT):
        ratio = y / float(CANVAS_HEIGHT)
        r = int(22 * (1.0 - ratio) + 12 * ratio)
        g = int(20 * (1.0 - ratio) + 14 * ratio)
        b = int(26 * (1.0 - ratio) + 18 * ratio)
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(r, g, b, 255))

    # Header
    draw.text((90, 120), "CASE STUDY: THE WORKFORCE FRICTION", font=FONT_HEADER, fill=ACCENT_AMBER)
    draw.text((90, 155), "Repetitive Manual Browser Work", font=FONT_HERO, fill=TEXT_HEADLINE)

    # Realistic Web Application Form on Desktop Monitor
    mon_x, mon_y = 90, 240
    mon_w, mon_h = 900, 720
    draw.rounded_rectangle([mon_x, mon_y, mon_x + mon_w, mon_y + mon_h], radius=16, fill=(24, 28, 40, 255), outline=BORDER_EDITORIAL, width=2)
    # Browser Tab Strip
    draw.rounded_rectangle([mon_x, mon_y, mon_x + mon_w, mon_y + 55], radius=16, fill=(18, 22, 32, 255))
    draw.ellipse([mon_x + 25, mon_y + 20, mon_x + 37, mon_y + 32], fill=(239, 68, 68, 255))
    draw.ellipse([mon_x + 45, mon_y + 20, mon_x + 57, mon_y + 32], fill=(245, 158, 11, 255))
    draw.ellipse([mon_x + 65, mon_y + 20, mon_x + 77, mon_y + 32], fill=(16, 185, 129, 255))
    draw.text((mon_x + 95, mon_y + 18), "Enterprise Procurement Portal — Order #84291", font=FONT_MONO, fill=TEXT_MUTED)

    # Form Fields (Visualizing the tedious friction)
    fields = [
        ("Vendor Tax ID", "US-9428104812", True),
        ("Billing Subledger Code", "GL-9820-EX-CORP", True),
        ("Approval Authorization Token", "AUTH-99214-X0", True),
        ("Line Item Category", "Hardware Compute Lease", True),
        ("Destination Cost Center", "ENGINEERING // R&D 04", False),
    ]

    fy = mon_y + 80
    for label, val, is_filled in fields:
        draw.text((mon_x + 40, fy), label, font=FONT_LABEL, fill=TEXT_MUTED)
        box_y = fy + 28
        draw.rounded_rectangle([mon_x + 40, box_y, mon_x + mon_w - 40, box_y + 50], radius=8, fill=(16, 20, 30, 255), outline=BORDER_EDITORIAL, width=1)
        if is_filled:
            draw.text((mon_x + 60, box_y + 14), val, font=FONT_SUB, fill=TEXT_HEADLINE)
        else:
            # Active blinking cursor
            cur_pulse = 0.5 + 0.5 * math.sin(2.0 * math.pi * 3.0 * t_sec)
            c_alpha = int(255 * cur_pulse)
            draw.text((mon_x + 60, box_y + 14), "Typing: Enterprise San Francisco Branch...", font=FONT_SUB, fill=ACCENT_AMBER)
            draw.line([(mon_x + 480, box_y + 12), (mon_x + 480, box_y + 38)], fill=(255, 171, 0, c_alpha), width=2)
        fy += 105

    # Human Friction Callout
    draw.rounded_rectangle([mon_x + 40, mon_y + mon_h - 90, mon_x + mon_w - 40, mon_y + mon_h - 30], radius=8, fill=(239, 68, 68, 30), outline=ACCENT_RED_WARN, width=1)
    draw.text((mon_x + 60, mon_y + mon_h - 72), "⚠ Human Operator: 42 Form Fields Remaining across 18 Tabs", font=FONT_LABEL, fill=ACCENT_RED_WARN)

def render_scene2_discovery(canvas: Image.Image, t_sec: float) -> None:
    """Scene 2: Authentic Browser Viewport & Natural Language Agent Directive."""
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], fill=COLOR_DEEP_SLATE)

    # Header
    draw.text((90, 120), "TECHNOLOGY BREAKTHROUGH", font=FONT_HEADER, fill=ACCENT_CYAN)
    draw.text((90, 155), "Browser-Use: Autonomous Agent", font=FONT_HERO, fill=TEXT_HEADLINE)

    # Authentic Chromium Window
    win_x, win_y = 80, 240
    win_w, win_h = 920, 960
    draw.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + win_h], radius=16, fill=(20, 25, 38, 255), outline=(0, 229, 255, 120), width=2)
    # Nav bar
    draw.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + 60], radius=16, fill=(14, 18, 28, 255))
    draw.ellipse([win_x + 25, win_y + 22, win_x + 37, win_y + 34], fill=(239, 68, 68, 255))
    draw.ellipse([win_x + 45, win_y + 22, win_x + 57, win_y + 34], fill=(245, 158, 11, 255))
    draw.ellipse([win_x + 65, win_y + 22, win_x + 77, win_y + 34], fill=(16, 185, 129, 255))
    # URL bar
    draw.rounded_rectangle([win_x + 100, win_y + 12, win_x + win_w - 30, win_y + 48], radius=8, fill=(10, 12, 18, 255))
    draw.text((win_x + 120, win_y + 20), "🔒 https://booking.railway.internal/search", font=FONT_MONO, fill=ACCENT_CYAN)

    # Natural Language Agent Directive Bar (Pulsing prompt)
    prompt_y = win_y + 85
    draw.rounded_rectangle([win_x + 30, prompt_y, win_x + win_w - 30, prompt_y + 85], radius=12, fill=(0, 229, 255, 20), outline=ACCENT_CYAN, width=2)
    draw.text((win_x + 50, prompt_y + 16), "AGENT INSTRUCTION", font=FONT_HEADER, fill=ACCENT_AMBER)
    draw.text((win_x + 50, prompt_y + 45), "Task: 'Find and reserve the fastest morning train from London to Edinburgh.'", font=FONT_SUB, fill=TEXT_HEADLINE)

    # Real web search UI
    ui_y = prompt_y + 120
    draw.text((win_x + 50, ui_y), "RAIL JOURNEY PLANNER", font=FONT_TITLE, fill=TEXT_HEADLINE)
    
    # Origin Card
    draw.rounded_rectangle([win_x + 50, ui_y + 50, win_x + win_w - 50, ui_y + 140], radius=10, fill=(28, 35, 52, 255), outline=BORDER_EDITORIAL, width=1)
    draw.text((win_x + 75, ui_y + 65), "Origin Station: London Kings Cross (KGX)", font=FONT_LABEL, fill=TEXT_HEADLINE)
    draw.text((win_x + 75, ui_y + 98), "Departure: 08:30 AM — Platform 9", font=FONT_MONO, fill=TEXT_MUTED)

    # Destination Card
    draw.rounded_rectangle([win_x + 50, ui_y + 160, win_x + win_w - 50, ui_y + 250], radius=10, fill=(28, 35, 52, 255), outline=BORDER_EDITORIAL, width=1)
    draw.text((win_x + 75, ui_y + 175), "Destination: Edinburgh Waverley (EDB)", font=FONT_LABEL, fill=TEXT_HEADLINE)
    draw.text((win_x + 75, ui_y + 208), "Arrival: 12:48 PM — Duration: 4h 18m", font=FONT_MONO, fill=TEXT_MUTED)

    # Live Agent Status badge
    draw.rounded_rectangle([win_x + 50, ui_y + 280, win_x + win_w - 50, ui_y + 360], radius=12, fill=(16, 185, 129, 30), outline=ACCENT_EMERALD, width=2)
    draw.text((win_x + 75, ui_y + 300), "✔ AUTONOMOUS CDP BROWSER CONTROLLER: ACTIVE", font=FONT_LABEL, fill=ACCENT_EMERALD)
    draw.text((win_x + 75, ui_y + 328), "Protocol: Chrome DevTools Protocol v1.3 // Direct Socket Connection", font=FONT_MONO, fill=TEXT_MUTED)

def render_scene3_mechanism(canvas: Image.Image, t_sec: float) -> None:
    """Scene 3: Scientific Exploded DOM Tree & Coordinate Tagging [1], [2], [3]."""
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], fill=(12, 16, 26, 255))

    # Header
    draw.text((90, 120), "SCIENTIFIC ARCHITECTURE", font=FONT_HEADER, fill=ACCENT_AMBER)
    draw.text((90, 155), "Accessibility Tree & Coordinate Tags", font=FONT_HERO, fill=TEXT_HEADLINE)

    # Exploded Architecture Container (Hero on right)
    box_x, box_y = 380, 250
    box_w, box_h = 620, 680
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=16, fill=(18, 24, 38, 255), outline=BORDER_EDITORIAL, width=2)

    draw.text((box_x + 30, box_y + 25), "ACCESSIBILITY DOM EXTRACTION", font=FONT_HEADER, fill=ACCENT_CYAN)

    # Coordinate Tag [1]
    draw.rounded_rectangle([box_x + 30, box_y + 70, box_x + box_w - 30, box_y + 155], radius=10, fill=(26, 34, 52, 255), outline=ACCENT_CYAN, width=1)
    draw.rectangle([box_x + 30, box_y + 70, box_x + 75, box_y + 105], fill=ACCENT_CYAN)
    draw.text((box_x + 40, box_y + 78), "[1]", font=FONT_MONO, fill=(0, 0, 0, 255))
    draw.text((box_x + 90, box_y + 88), "origin_input // London Kings Cross", font=FONT_LABEL, fill=TEXT_HEADLINE)
    draw.text((box_x + 90, box_y + 118), "role: combobox | aria-expanded: false", font=FONT_MONO, fill=TEXT_MUTED)

    # Coordinate Tag [2] (Hero Pointed Target)
    tag2_pulse = 0.7 + 0.3 * math.sin(2.0 * math.pi * 2.0 * t_sec)
    draw.rounded_rectangle([box_x + 30, box_y + 175, box_x + box_w - 30, box_y + 260], radius=10, fill=(255, 171, 0, 30), outline=ACCENT_AMBER, width=2)
    draw.rectangle([box_x + 30, box_y + 175, box_x + 75, box_y + 210], fill=ACCENT_AMBER)
    draw.text((box_x + 40, box_y + 183), "[2]", font=FONT_MONO, fill=(0, 0, 0, 255))
    draw.text((box_x + 90, box_y + 193), "destination_input // Edinburgh Waverley", font=FONT_LABEL, fill=TEXT_HEADLINE)
    draw.text((box_x + 90, box_y + 223), "role: combobox | coordinate: (480, 210)", font=FONT_MONO, fill=ACCENT_AMBER)

    # Coordinate Tag [3]
    draw.rounded_rectangle([box_x + 30, box_y + 280, box_x + box_w - 30, box_y + 365], radius=10, fill=(26, 34, 52, 255), outline=ACCENT_EMERALD, width=1)
    draw.rectangle([box_x + 30, box_y + 280, box_x + 75, box_y + 315], fill=ACCENT_EMERALD)
    draw.text((box_x + 40, box_y + 288), "[3]", font=FONT_MONO, fill=(0, 0, 0, 255))
    draw.text((box_x + 90, box_y + 298), "submit_search_button // Confirm Booking", font=FONT_LABEL, fill=TEXT_HEADLINE)
    draw.text((box_x + 90, box_y + 328), "role: button | state: enabled", font=FONT_MONO, fill=ACCENT_EMERALD)

    # Model Decision Loop Box below
    draw.rounded_rectangle([box_x + 30, box_y + 395, box_x + box_w - 30, box_y + 640], radius=12, fill=(12, 16, 26, 255), outline=BORDER_EDITORIAL, width=1)
    draw.text((box_x + 50, box_y + 415), "MULTIMODAL DECISION LOOP", font=FONT_HEADER, fill=ACCENT_AMBER)
    draw.text((box_x + 50, box_y + 450), "> Ingest: Screenshot + Accessibility Tree", font=FONT_MONO, fill=TEXT_MUTED)
    draw.text((box_x + 50, box_y + 485), "> Action: type_text(coordinate=2, 'Edinburgh')", font=FONT_MONO, fill=ACCENT_CYAN)
    draw.text((box_x + 50, box_y + 520), "> Action: click_element(coordinate=3)", font=FONT_MONO, fill=ACCENT_EMERALD)
    draw.text((box_x + 50, box_y + 555), "> Result: HTTP 200 OK | Verified via CDP", font=FONT_MONO, fill=TEXT_HEADLINE)
    draw.text((box_x + 50, box_y + 590), "> Execution: 100% Deterministic Browser Protocol", font=FONT_MONO, fill=ACCENT_AMBER)

def render_scene4_workflow(canvas: Image.Image, t_sec: float) -> None:
    """Scene 4: Real Developer IDE & Authentic Python Code Demonstration."""
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], fill=(14, 17, 24, 255))

    # Header
    draw.text((90, 120), "PRODUCTION IMPLEMENTATION", font=FONT_HEADER, fill=ACCENT_EMERALD)
    draw.text((90, 155), "Authentic Python Agent API", font=FONT_HERO, fill=TEXT_HEADLINE)

    # VS Code Editor Window
    ide_x, ide_y = 80, 240
    ide_w, ide_h = 920, 940
    draw.rounded_rectangle([ide_x, ide_y, ide_x + ide_w, ide_y + ide_h], radius=16, fill=(24, 28, 40, 255), outline=BORDER_EDITORIAL, width=2)
    # Tab
    draw.rounded_rectangle([ide_x, ide_y, ide_x + ide_w, ide_y + 50], radius=16, fill=(18, 22, 32, 255))
    draw.text((ide_x + 30, ide_y + 15), "📄 run_agent.py — Python 3.11", font=FONT_MONO, fill=ACCENT_EMERALD)

    # Authentic Python Code Lines
    code_lines = [
        ("import asyncio", ACCENT_PURPLE),
        ("from browser_use import Agent", ACCENT_CYAN),
        ("from langchain_openai import ChatOpenAI", ACCENT_CYAN),
        ("", TEXT_MUTED),
        ("async def main():", ACCENT_AMBER),
        ("    # Instantiate verified autonomous web controller", TEXT_MUTED),
        ("    agent = Agent(", TEXT_HEADLINE),
        ("        task='Book fastest morning train to Edinburgh',", ACCENT_AMBER),
        ("        llm=ChatOpenAI(model='gpt-4o'),", ACCENT_CYAN),
        ("        use_vision=True,", ACCENT_EMERALD),
        ("    )", TEXT_HEADLINE),
        ("    history = await agent.run()", ACCENT_PURPLE),
        ("    print(f'Execution completed: {history.is_done()}')", TEXT_HEADLINE),
        ("", TEXT_MUTED),
        ("asyncio.run(main())", ACCENT_PURPLE),
    ]

    cy = ide_y + 75
    for line, color in code_lines:
        draw.text((ide_x + 40, cy), line, font=FONT_MONO, fill=color)
        cy += 32

    # Integrated Terminal View below editor
    term_y = cy + 30
    draw.rounded_rectangle([ide_x + 20, term_y, ide_x + ide_w - 20, ide_y + ide_h - 25], radius=12, fill=(10, 12, 18, 255), outline=ACCENT_EMERALD, width=1)
    draw.text((ide_x + 40, term_y + 18), "TERMINAL: local_environment (zsh)", font=FONT_HEADER, fill=TEXT_MUTED)

    term_logs = [
        ("$ python run_agent.py", TEXT_HEADLINE),
        ("[INFO] Connected to Playwright Chromium instance on 127.0.0.1:9222", ACCENT_CYAN),
        ("[STEP 01] Extracted accessibility tree: 84 interactive elements", TEXT_MUTED),
        ("[STEP 02] Dispatched CDP input: London Kings Cross -> 200 OK", ACCENT_EMERALD),
        ("[STEP 03] Dispatched CDP click: [Confirm Ticket] -> 200 OK", ACCENT_EMERALD),
        ("[SUCCESS] Task completed in 4 steps. Zero human intervention.", ACCENT_AMBER),
    ]

    ty = term_y + 55
    for t_line, t_col in term_logs:
        draw.text((ide_x + 40, ty), t_line, font=FONT_MONO, fill=t_col)
        ty += 32

def render_scene5_significance(canvas: Image.Image, t_sec: float) -> None:
    """Scene 5: Spatial Ecosystem Metaphor — The Leap to Autonomous Action."""
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], fill=COLOR_OBSIDIAN)

    # Header
    draw.text((90, 120), "TECHNOLOGY IMPLICATIONS", font=FONT_HEADER, fill=ACCENT_PURPLE)
    draw.text((90, 155), "From Chatbots to Operating Systems", font=FONT_HERO, fill=TEXT_HEADLINE)

    # Central Diagram Comparing Chatbot vs Autonomous Agent
    cx, cy = 90, 260
    cw, ch = 900, 780
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=20, fill=(18, 22, 34, 255), outline=BORDER_EDITORIAL, width=2)

    # 1. Old Paradigm: Passive Chatbot
    draw.rounded_rectangle([cx + 40, cy + 50, cx + cw - 40, cy + 240], radius=14, fill=(26, 32, 48, 255), outline=(60, 75, 100, 255), width=1)
    draw.text((cx + 70, cy + 75), "TRADITIONAL GENERATIVE AI (2022–2024)", font=FONT_LABEL, fill=TEXT_MUTED)
    draw.text((cx + 70, cy + 115), "• Trapped inside conversational text window", font=FONT_SUB, fill=TEXT_HEADLINE)
    draw.text((cx + 70, cy + 155), "• Can only generate tokens; zero actuators", font=FONT_SUB, fill=TEXT_HEADLINE)
    draw.text((cx + 70, cy + 195), "• Human must manually copy, paste, and execute", font=FONT_SUB, fill=ACCENT_RED_WARN)

    # Transition Arrow
    draw.text((cx + cw//2 - 20, cy + 265), "▼", font=FONT_HERO, fill=ACCENT_AMBER)

    # 2. New Paradigm: Autonomous OS Agent
    draw.rounded_rectangle([cx + 40, cy + 340, cx + cw - 40, cy + 620], radius=14, fill=(16, 185, 129, 20), outline=ACCENT_EMERALD, width=2)
    draw.text((cx + 70, cy + 365), "AUTONOMOUS OPERATING AGENT (2026+)", font=FONT_TITLE, fill=ACCENT_EMERALD)
    
    features = [
        ("Live Chromium DOM Actuation", "Clicks, scrolls, types, navigates native browsers"),
        ("Session Cookie & Auth Persistence", "Operates within authenticated enterprise environments"),
        ("Closed-Loop Feedback Verification", "Inspects DOM state after every action to confirm success"),
    ]

    fy = cy + 420
    for f_title, f_desc in features:
        draw.text((cx + 70, fy), f"✔ {f_title}", font=FONT_LABEL, fill=TEXT_HEADLINE)
        draw.text((cx + 95, fy + 26), f_desc, font=FONT_MONO, fill=TEXT_MUTED)
        fy += 65

    # Bottom Callout
    draw.text((cx + 70, cy + 680), "The threshold where software begins to execute on its own.", font=FONT_SUB, fill=ACCENT_GOLD)

def render_scene6_closing(canvas: Image.Image, t_sec: float) -> None:
    """Scene 6: Warm Cinematic Documentary Studio & Authoritative Takeaway."""
    draw = ImageDraw.Draw(canvas)

    # Warm architectural studio lighting
    for y in range(CANVAS_HEIGHT):
        ratio = y / float(CANVAS_HEIGHT)
        r = int(16 * (1.0 - ratio) + 8 * ratio)
        g = int(20 * (1.0 - ratio) + 10 * ratio)
        b = int(32 * (1.0 - ratio) + 16 * ratio)
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(r, g, b, 255))

    # Optical bokeh highlights
    bokeh_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bokeh_layer)
    bdraw.ellipse([140, 280, 420, 560], fill=(255, 180, 80, 22))
    bdraw.ellipse([720, 340, 1020, 640], fill=(0, 229, 255, 18))
    bokeh_layer = bokeh_layer.filter(ImageFilter.GaussianBlur(radius=50))
    canvas.alpha_composite(bokeh_layer)

    # Restrained Editorial Branding
    draw.text((100, 140), "SUPER.INTELLIGENCEEE", font=FONT_HEADER, fill=ACCENT_AMBER)
    draw.text((100, 180), "Understand What's Next.", font=FONT_HERO, fill=TEXT_HEADLINE)
    draw.line([(100, 240), (450, 240)], fill=ACCENT_AMBER, width=2)
    draw.text((100, 260), "Documentary Investigation // Autonomous Systems", font=FONT_SUB, fill=TEXT_MUTED)

# ---------------------------------------------------------------------------
# Master Scene Render Execution
# ---------------------------------------------------------------------------

SCENE_ENV_FUNCS = {
    "scene1_problem": render_scene1_problem,
    "scene2_discovery": render_scene2_discovery,
    "scene3_mechanism": render_scene3_mechanism,
    "scene4_workflow": render_scene4_workflow,
    "scene5_significance": render_scene5_significance,
    "scene6_closing": render_scene6_closing,
}

def render_scene(spec: Dict[str, Any]) -> Tuple[Path, Path]:
    scene_id = spec["id"]
    audio_path = spec["audio_file"]

    with wave.open(str(audio_path), "rb") as wf:
        total_dur = wf.getnframes() / float(wf.getframerate())
    total_frames = int(math.ceil(total_dur * FPS))

    print(f"\n[SCENE: {scene_id}] Frames: {total_frames} | Duration: {total_dur:.2f}s")
    frames_dir = FRAMES_DIR / scene_id
    frames_dir.mkdir(parents=True, exist_ok=True)

    env_func = SCENE_ENV_FUNCS[scene_id]
    mid_kf_path = KEYFRAMES_DIR / f"{scene_id}_mid_keyframe.png"

    char_config = None
    if spec["has_character"]:
        char_config = CharacterSceneConfig(
            screen_position=spec["host_pos"],
            scale=spec["host_scale"],
            editorial_reason=f"Phase 14.1 {scene_id}"
        )

    t0 = time.time()
    for frame_idx in range(total_frames):
        t_sec = frame_idx / float(FPS)
        frame = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 255))

        # 1. Render Cinematic Environment
        env_func(frame, t_sec)

        # 2. Render Host Character (Only when narratively specified)
        if spec["has_character"] and char_config:
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
                ambient_tint_hex="#FFE0B2" if scene_id in ("scene1_problem", "scene6_closing") else "#00E5FF"
            )

        # 3. Editorial Safe-Area Subtitles
        draw_safe_subtitles(frame, spec["text"], t_sec, total_dur)

        # Save Frame
        frame_file = frames_dir / f"frame_{frame_idx:05d}.png"
        frame.save(frame_file)

        # Mid keyframe
        if frame_idx == total_frames // 2:
            frame.save(mid_kf_path)
            print(f"  [KEYFRAME] Saved: {mid_kf_path}")

        if frame_idx % 60 == 0:
            print(f"  Frame {frame_idx}/{total_frames}...")

    print(f"[SCENE: {scene_id}] Rendered in {time.time() - t0:.1f}s")

    # Encode with FFmpeg
    video_mp4 = SCENES_DIR / f"{scene_id}.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%05d.png"),
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
    print(f"[SCENE: {scene_id}] MP4 encoded: {video_mp4}")
    return video_mp4, mid_kf_path

def compile_master(scene_mp4s: List[Path]) -> Path:
    concat_txt = PROD_DIR / "concat_list.txt"
    with open(concat_txt, "w") as f:
        for p in scene_mp4s:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    master_mp4 = PROD_DIR / "browser_use_cinematic_documentary_master.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(master_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\n[MASTER] Cinematic Master Compiled: {master_mp4}")
    return master_mp4

def generate_contact_sheet(keyframes: List[Path]) -> Path:
    thumbs = [Image.open(kf).resize((360, 640), Image.Resampling.LANCZOS) for kf in keyframes]
    cols = 3
    rows = 2
    sheet = Image.new("RGBA", (cols * 360, rows * 640), (8, 12, 18, 255))
    for i, thumb in enumerate(thumbs):
        gx = (i % cols) * 360
        gy = (i // cols) * 640
        sheet.paste(thumb, (gx, gy))

    sheet_p = PROD_DIR / "phase14_1_cinematic_contact_sheet.png"
    sheet.save(sheet_p)
    print(f"[CONTACT SHEET] Generated: {sheet_p}")
    return sheet_p

def main():
    print("=" * 80)
    print("SUPER.INTELLIGENCEEE — PHASE 14.1 CINEMATIC DOCUMENTARY PRODUCTION")
    print("=" * 80)

    keyframes = []
    scenes = []

    for spec in SCENE_SPECS:
        v_path, kf_path = render_scene(spec)
        scenes.append(v_path)
        keyframes.append(kf_path)

    master_mp4 = compile_master(scenes)
    contact_sheet = generate_contact_sheet(keyframes)

    print("\n" + "=" * 80)
    print("CINEMATIC DOCUMENTARY MASTER COMPLETED SUCCESSFULLY!")
    print(f"Master Video: {master_mp4}")
    print(f"Contact Sheet: {contact_sheet}")
    print("=" * 80)

if __name__ == "__main__":
    main()
