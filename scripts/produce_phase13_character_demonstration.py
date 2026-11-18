"""
SUPER.INTELLIGENCEEE — Phase 13 Character Host Demonstration Producer
Renders 3 distinct demonstration scenes featuring the canonical host:
1. The Presenter (center hero, documentary studio environment)
2. The Investigator (examining NVIDIA GH100 semiconductor processor)
3. The Explainer (sidecar host explaining Asynchronous Warp Specialization)
Compiles all 3 scenes into a unified preview video with forensic keyframe contact sheet.
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
from PIL import Image, ImageDraw, ImageFont

from core.character_scene_config import (
    CharacterSceneConfig,
    CharacterPose,
    CharacterExpression,
    CharacterScreenPosition,
    CharacterMovementPattern,
)
from rendering.character_host_engine import CharacterHostEngine
from rendering.advanced_subtitle_engine import AdvancedSubtitleEngine

# ---------------------------------------------------------------------------
# Global Constants & Paths
# ---------------------------------------------------------------------------

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = WORKSPACE_ROOT / "output" / "phase13_demonstration"
AUDIO_DIR = OUTPUT_DIR / "audio"
FRAMES_DIR = OUTPUT_DIR / "frames"
SCENES_DIR = OUTPUT_DIR / "scenes"
KEYFRAMES_DIR = OUTPUT_DIR / "keyframes"

for d in (OUTPUT_DIR, AUDIO_DIR, FRAMES_DIR, SCENES_DIR, KEYFRAMES_DIR):
    d.mkdir(parents=True, exist_ok=True)

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
FPS = 30

# Color Palette
BG_STUDIO = (11, 15, 23, 255)
BG_CHIP = (8, 10, 14, 255)
BG_DIAGRAM = (10, 13, 20, 255)

CYAN_PRIMARY = (0, 229, 255, 255)
AMBER_ACCENT = (255, 171, 0, 255)
ORANGE_HOST = (255, 107, 0, 255)
GREEN_TECH = (16, 185, 129, 255)
PURPLE_WARP = (168, 85, 247, 255)
RED_CHOKE = (239, 68, 68, 255)
WHITE_BRIGHT = (248, 250, 252, 255)
TEXT_MUTED = (148, 163, 184, 255)
BORDER_DARK = (30, 41, 59, 255)

# Fonts
def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    sys_fonts = [
        "C:/Windows/Fonts/segoeui.ttf" if not bold else "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for fp in sys_fonts:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_HEADER_TAG = get_font(22, bold=True)
FONT_HEADER_TITLE = get_font(28, bold=True)
FONT_HERO = get_font(42, bold=True)
FONT_SUB = get_font(26, bold=False)
FONT_MONO = get_font(20, bold=True)
FONT_LABEL = get_font(18, bold=True)

# Engines
HOST_ENGINE = CharacterHostEngine()
SUBTITLE_ENGINE = AdvancedSubtitleEngine()

# Demonstration Scene Data
DEMO_SCENES = [
    {
        "id": "scene1_presenter",
        "name": "The Presenter",
        "tag": "DOCUMENTARY HOST INTRODUCTION",
        "tag_color": AMBER_ACCENT,
        "title": "SUPER.INTELLIGENCEEE // RESEARCH EXPEDITION",
        "spoken": "Welcome to Super Intelligence. Today, we are breaking down how the next generation of artificial intelligence is breaking free from the cloud.",
        "config": CharacterSceneConfig(
            appears=True,
            editorial_reason="Host welcomes viewer directly and outlines research thesis",
            pose=CharacterPose.PRESENTER_DIRECT,
            expression=CharacterExpression.CURIOUS_INQUIRY,
            screen_position=CharacterScreenPosition.CENTER_HERO,
            movement_pattern=CharacterMovementPattern.NATURAL_BREATHING_AND_BLINK,
            scale=0.70
        )
    },
    {
        "id": "scene2_investigator",
        "name": "The Investigator",
        "tag": "HARDWARE ARCHITECTURE FORENSICS",
        "tag_color": ORANGE_HOST,
        "title": "NVIDIA GH100 HOPPER // 80B TRANSISTOR SILICON DIE",
        "spoken": "Take a look inside the NVIDIA H100. This silicon die contains eighty billion transistors, but its biggest bottleneck is the memory bus.",
        "config": CharacterSceneConfig(
            appears=True,
            editorial_reason="Host examines physical silicon die and indicates HBM3 bus bottleneck",
            pose=CharacterPose.INVESTIGATOR_EXAMINING,
            expression=CharacterExpression.FOCUSED_ANALYSIS,
            screen_position=CharacterScreenPosition.LOWER_LEFT,
            movement_pattern=CharacterMovementPattern.NATURAL_BREATHING_AND_BLINK,
            scale=0.62
        )
    },
    {
        "id": "scene3_explainer",
        "name": "The Explainer",
        "tag": "SYSTEMS ALGORITHM DEMONSTRATION",
        "tag_color": CYAN_PRIMARY,
        "title": "ASYNCHRONOUS WARP SPECIALIZATION // TMA CONCURRENCY",
        "spoken": "This is Asynchronous Warp Specialization. Instead of stalling the whole GPU, one warp fetches data while another computes matrix math in parallel.",
        "config": CharacterSceneConfig(
            appears=True,
            editorial_reason="Host stands beside systems diagram and guides viewer through warp overlap",
            pose=CharacterPose.EXPLAINER_GESTURE,
            expression=CharacterExpression.AHA_REVELATION,
            screen_position=CharacterScreenPosition.LOWER_RIGHT,
            movement_pattern=CharacterMovementPattern.NATURAL_BREATHING_AND_BLINK,
            scale=0.60
        )
    }
]


# ---------------------------------------------------------------------------
# Audio Processing & Mastering
# ---------------------------------------------------------------------------

def master_scene_audio() -> Dict[str, Dict[str, Any]]:
    """Normalizes raw Kokoro audio to EBU R128 (-16 LUFS) and mixes subtle lab drone."""
    print("\n--- MASTERING AUDIO STEMS (EBU R128 -16 LUFS) ---")
    stems_meta = {}

    for s in DEMO_SCENES:
        sid = s["id"]
        raw_wav = AUDIO_DIR / f"{sid}_raw.wav"
        voice_wav = AUDIO_DIR / f"{sid}_voice.wav"
        master_wav = AUDIO_DIR / f"{sid}_master.wav"

        # 1. Normalize voiceover
        cmd_norm = [
            "ffmpeg", "-y", "-i", str(raw_wav),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar", "44100", "-ac", "2",
            str(voice_wav)
        ]
        subprocess.run(cmd_norm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        with wave.open(str(voice_wav), "rb") as wf:
            dur = wf.getnframes() / float(wf.getframerate())

        scene_dur = round(dur + 0.6, 2)  # 0.6s tail pad for clean pacing

        # 2. Mix with subtle ambient laboratory drone
        cmd_mix = [
            "ffmpeg", "-y",
            "-i", str(voice_wav),
            "-f", "lavfi", "-t", str(scene_dur),
            "-i", "anoisesrc=c=pink:r=44100:a=0.008,lowpass=f=220,volume=-32dB",
            "-filter_complex",
            f"[0:a]apad=pad_dur=0.6[vpad];[vpad][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout];[aout]loudnorm=I=-16:TP=-1.5:LRA=11[master]",
            "-map", "[master]",
            "-ar", "44100", "-ac", "2",
            str(master_wav)
        ]
        subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        stems_meta[sid] = {
            "voice_duration": dur,
            "scene_duration": scene_dur,
            "master_wav": str(master_wav)
        }
        print(f"  [{sid}] Voice: {dur:.2f}s | Scene Duration: {scene_dur:.2f}s")

    return stems_meta


# ---------------------------------------------------------------------------
# Scene Renderers
# ---------------------------------------------------------------------------

def draw_header_banner(draw: ImageDraw.ImageDraw, tag: str, title: str, tag_col: Tuple[int, int, int, int]):
    """Standard documentary header banner."""
    draw.rectangle([40, 60, 1040, 200], fill=(15, 23, 42, 220), outline=BORDER_DARK, width=2)
    # Tag capsule
    draw.rounded_rectangle([70, 85, 70 + int(len(tag)*13) + 20, 120], radius=4, fill=(tag_col[0]//5, tag_col[1]//5, tag_col[2]//5, 255), outline=tag_col, width=1)
    draw.text((80, 92), tag, font=FONT_HEADER_TAG, fill=tag_col)
    # Title
    draw.text((70, 138), title, font=FONT_HEADER_TITLE, fill=WHITE_BRIGHT)


def render_scene_1(canvas: Image.Image, progress: float, t_sec: float, scene_info: Dict[str, Any]):
    """Scene 1: The Presenter — Centered hero host in documentary studio."""
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_header_banner(draw, scene_info["tag"], scene_info["title"], scene_info["tag_color"])

    # 1. Perspective grid floor
    for y_line in range(1200, 1850, 60):
        alpha = int(25 + ((y_line - 1200) / 650.0) * 45)
        draw.line([40, y_line, 1040, y_line], fill=(30, 41, 59, alpha), width=1)

    # 2. Studio telemetry display behind host
    card_box = [160, 260, 920, 780]
    draw.rounded_rectangle(card_box, radius=12, fill=(15, 23, 42, 200), outline=BORDER_DARK, width=2)
    draw.text((200, 300), "AUTONOMOUS RESEARCH EXPEDITIONS", font=FONT_MONO, fill=CYAN_PRIMARY)
    draw.text((200, 340), "Local Silicon // Open Weights // Neural Architecture", font=FONT_LABEL, fill=TEXT_MUTED)

    # Live telemetry waveform
    pulse_pts = []
    for x in range(200, 880, 15):
        wy = 480 + int(35 * math.sin((x * 0.03) + (progress * 12.0)) * math.cos(x * 0.01))
        pulse_pts.append((x, wy))
    draw.line(pulse_pts, fill=CYAN_PRIMARY, width=3)

    # Metric blocks
    draw.rounded_rectangle([200, 560, 500, 720], radius=8, fill=(24, 32, 47, 255), outline=BORDER_DARK, width=1)
    draw.text((220, 580), "HARDWARE TARGET:", font=FONT_LABEL, fill=TEXT_MUTED)
    draw.text((220, 615), "H100 SXM5 80GB", font=FONT_HERO, fill=WHITE_BRIGHT)
    draw.text((220, 675), "80 Billion Transistors", font=FONT_LABEL, fill=AMBER_ACCENT)

    draw.rounded_rectangle([540, 560, 880, 720], radius=8, fill=(24, 32, 47, 255), outline=BORDER_DARK, width=1)
    draw.text((560, 580), "DISTRIBUTION CHURN:", font=FONT_LABEL, fill=TEXT_MUTED)
    draw.text((560, 615), "100% On-Device", font=FONT_HERO, fill=GREEN_TECH)
    draw.text((560, 675), "Zero Cloud Dependency", font=FONT_LABEL, fill=CYAN_PRIMARY)

    # 3. Composite Host Character
    HOST_ENGINE.composite_onto_canvas(
        canvas, scene_info["config"], t_sec=t_sec, ambient_tint_hex="#00E5FF"
    )


def render_scene_2(canvas: Image.Image, progress: float, t_sec: float, scene_info: Dict[str, Any]):
    """Scene 2: The Investigator — Examining physical silicon die."""
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_header_banner(draw, scene_info["tag"], scene_info["title"], scene_info["tag_color"])

    # Semiconductor Processor Hero Visual (Upper Right: x=340..1020, y=260..980)
    chip_box = [340, 260, 1020, 940]
    draw.rounded_rectangle(chip_box, radius=16, fill=(16, 22, 34, 255), outline=(51, 65, 85, 255), width=3)

    # Laser-etched text on titanium frame
    draw.text((370, 285), "NVIDIA GH100-800-A1 // TSMC 4N 814mm²", font=FONT_MONO, fill=AMBER_ACCENT)

    # Central Logic Die
    die_box = [460, 350, 900, 750]
    draw.rounded_rectangle(die_box, radius=8, fill=(24, 32, 47, 255), outline=(71, 85, 105, 255), width=2)
    # Silicon wafer grid texture
    for gx in range(480, 880, 30):
        draw.line([gx, 360, gx, 740], fill=(40, 53, 76, 180), width=1)
    for gy in range(370, 730, 30):
        draw.line([470, gy, 890, gy], fill=(40, 53, 76, 180), width=1)
    draw.text((530, 530), "COMPUTE CORE DIE", font=FONT_MONO, fill=CYAN_PRIMARY)
    draw.text((535, 565), "80,000,000,000 Transistors", font=FONT_LABEL, fill=WHITE_BRIGHT)

    # 6 HBM3 Stacks surrounding the logic die
    hbm_rects = [
        ([370, 360, 430, 520], "HBM3 #1"),
        ([370, 560, 430, 720], "HBM3 #2"),
        ([930, 360, 990, 520], "HBM3 #3"),
        ([930, 560, 990, 720], "HBM3 #4"),
        ([500, 770, 660, 830], "HBM3 #5"),
        ([700, 770, 860, 830], "HBM3 #6"),
    ]
    for hb, hblabel in hbm_rects:
        draw.rounded_rectangle(hb, radius=4, fill=(30, 41, 59, 255), outline=AMBER_ACCENT, width=1)
        draw.text((hb[0] + 5, hb[1] + 15), hblabel, font=FONT_LABEL, fill=AMBER_ACCENT)

    # Pulsing red bottleneck callout
    pulse_w = int(2 + 2 * math.sin(progress * 15.0))
    draw.line([430, 440, 460, 440], fill=RED_CHOKE, width=pulse_w + 3)
    draw.line([430, 640, 460, 640], fill=RED_CHOKE, width=pulse_w + 3)
    draw.line([900, 440, 930, 440], fill=RED_CHOKE, width=pulse_w + 3)
    draw.line([900, 640, 930, 640], fill=RED_CHOKE, width=pulse_w + 3)

    # Hardware Chokepoint Callout Bar
    draw.rounded_rectangle([360, 860, 1000, 920], radius=6, fill=(239, 68, 68, 40), outline=RED_CHOKE, width=2)
    draw.text((380, 875), "MEMORY BUS BOTTLENECK: 3.35 TB/s CHOKEPOINT", font=FONT_MONO, fill=RED_CHOKE)

    # Composite Host (Lower Left, investigating the processor)
    HOST_ENGINE.composite_onto_canvas(
        canvas, scene_info["config"], t_sec=t_sec, ambient_tint_hex="#FF9800"
    )


def render_scene_3(canvas: Image.Image, progress: float, t_sec: float, scene_info: Dict[str, Any]):
    """Scene 3: The Explainer — Explaining Asynchronous Warp Specialization."""
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_header_banner(draw, scene_info["tag"], scene_info["title"], scene_info["tag_color"])

    # Technical Architecture Diagram (Upper Left: x=60..740, y=260..1020)
    diag_box = [60, 260, 740, 1020]
    draw.rounded_rectangle(diag_box, radius=14, fill=(15, 23, 42, 230), outline=BORDER_DARK, width=2)

    # 1. Producer Warp TMA Lane
    draw.text((90, 290), "PRODUCER WARP (TMA MEMORY ENGINE):", font=FONT_MONO, fill=PURPLE_WARP)
    w_prod = int(progress * 580)
    draw.rectangle([90, 330, 90 + w_prod, 400], fill=(168, 85, 247, 80), outline=PURPLE_WARP, width=2)
    draw.text((110, 350), "Async Hardware Prefetch HBM -> SRAM...", font=FONT_SUB, fill=WHITE_BRIGHT)

    # 2. Consumer Warp Tensor Core Lane
    draw.text((90, 430), "CONSUMER WARP (TENSOR CORE COMPUTE):", font=FONT_MONO, fill=GREEN_TECH)
    w_cons = int(progress * 580)
    draw.rectangle([90, 470, 90 + w_cons, 540], fill=(16, 185, 129, 80), outline=GREEN_TECH, width=2)
    draw.text((110, 490), "WGMMA Matrix Multiply Simultaneous...", font=FONT_SUB, fill=WHITE_BRIGHT)

    # 3. Concurrency Overlap Timeline
    draw.rounded_rectangle([90, 580, 710, 780], radius=8, fill=(24, 32, 47, 255), outline=CYAN_PRIMARY, width=2)
    draw.text((110, 605), "ZERO-IDLE CONCURRENCY TIMELINE:", font=FONT_MONO, fill=CYAN_PRIMARY)
    draw.text((110, 645), "Memory latency hidden behind tensor core math.", font=FONT_SUB, fill=WHITE_BRIGHT)
    draw.text((110, 690), "No warp stalling. Hardware saturation: 75% peak.", font=FONT_LABEL, fill=TEXT_MUTED)

    # 4. Result Metrics Box
    draw.rounded_rectangle([90, 810, 710, 980], radius=8, fill=(16, 185, 129, 30), outline=GREEN_TECH, width=2)
    draw.text((110, 835), "MEASURED THROUGHPUT:", font=FONT_MONO, fill=GREEN_TECH)
    draw.text((110, 875), "740 TFLOPs / s", font=FONT_HERO, fill=WHITE_BRIGHT)
    draw.text((110, 935), "2.1x Speedup over FlashAttention-2", font=FONT_LABEL, fill=AMBER_ACCENT)

    # Composite Host (Lower Right, flipped left to explain the diagram)
    HOST_ENGINE.composite_onto_canvas(
        canvas, scene_info["config"], t_sec=t_sec, ambient_tint_hex="#00E5FF"
    )


# ---------------------------------------------------------------------------
# Master Production Pipeline
# ---------------------------------------------------------------------------

def produce_demonstration():
    """Renders all 3 demonstration scenes and assembles master preview video."""
    print("=" * 80)
    print("PHASE 13: CHARACTER INTEGRATION & DEMONSTRATION PIPELINE")
    print("=" * 80)

    # Step 1: Master Audio
    stems_meta = master_scene_audio()

    scene_renderers = {
        "scene1_presenter": render_scene_1,
        "scene2_investigator": render_scene_2,
        "scene3_explainer": render_scene_3,
    }

    scene_mp4s = []

    # Step 2: Render Scenes
    print("\n--- RENDERING 1080x1920 VIDEO SCENES (30 FPS) ---")
    for idx, s in enumerate(DEMO_SCENES, 1):
        sid = s["id"]
        meta = stems_meta[sid]
        scene_dur = meta["scene_duration"]
        total_frames = int(scene_dur * FPS)
        print(f"\n[{idx}/3] Rendering {sid} ({scene_dur}s, {total_frames} frames)...")

        scene_frames_dir = FRAMES_DIR / sid
        scene_frames_dir.mkdir(parents=True, exist_ok=True)
        renderer = scene_renderers[sid]

        words = s["spoken"].split()
        voice_dur = meta["voice_duration"]

        for f_idx in range(total_frames):
            t_sec = f_idx / float(FPS)
            progress = min(1.0, f_idx / max(1, total_frames - 1))

            # Base Canvas
            bg_col = BG_STUDIO if sid == "scene1_presenter" else (BG_CHIP if sid == "scene2_investigator" else BG_DIAGRAM)
            canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), bg_col)

            # Render Scene Graphics and Host
            renderer(canvas, progress, t_sec, s)

            # Subtitles with active word highlighting
            w_idx = min(len(words) - 1, int((t_sec / voice_dur) * len(words)))
            active_word = words[w_idx]
            SUBTITLE_ENGINE.render_subtitle(canvas, s["spoken"], active_word=active_word, y_center=1680)

            # Save frame
            f_path = scene_frames_dir / f"frame_{f_idx:05d}.png"
            canvas.save(f_path)

        # Compile Scene MP4
        scene_mp4 = SCENES_DIR / f"{sid}.mp4"
        cmd_scene = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", str(scene_frames_dir / "frame_%05d.png"),
            "-i", meta["master_wav"],
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(scene_mp4)
        ]
        subprocess.run(cmd_scene, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        scene_mp4s.append(scene_mp4)
        print(f"  Scene compiled: {scene_mp4.name} ({scene_mp4.stat().st_size / (1024*1024):.2f} MB)")

    # Step 3: Concat Master Preview Video
    print("\n--- ASSEMBLING CHARACTER INTEGRATION PREVIEW MP4 ---")
    concat_list = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for sm in scene_mp4s:
            f.write(f"file '{sm.resolve().as_posix()}'\n")

    master_mp4 = OUTPUT_DIR / "character_integration_preview.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(master_mp4)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"PREVIEW MP4 EXPORTED: {master_mp4.name} ({master_mp4.stat().st_size / (1024*1024):.2f} MB)")

    # Step 4: Multi-Timestamp Forensic Keyframes & Contact Sheet
    print("\n--- PERFORMING MULTI-TIMESTAMP FORENSIC INSPECTION ---")
    timestamps = [1.5, 4.0, 10.5, 14.0, 19.5, 24.0]
    extracted_frames = []

    for ts in timestamps:
        out_f = KEYFRAMES_DIR / f"forensic_{ts:04.1f}s.png"
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(ts),
            "-i", str(master_mp4),
            "-vframes", "1",
            str(out_f)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        extracted_frames.append(out_f)
        print(f"  Verified frame at {ts:04.1f}s -> {out_f.name}")

    # Build 6-frame contact sheet (3 cols x 2 rows)
    thumb_w, thumb_h = 360, 640
    contact_w = thumb_w * 3
    contact_h = thumb_h * 2
    contact_im = Image.new("RGBA", (contact_w, contact_h), (15, 23, 42, 255))
    draw_c = ImageDraw.Draw(contact_im)

    for i, ef in enumerate(extracted_frames):
        im_k = Image.open(ef).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        col = i % 3
        row = i // 3
        px = col * thumb_w
        py = row * thumb_h
        contact_im.paste(im_k, (px, py))
        draw_c.rectangle([px, py, px + thumb_w, py + thumb_h], outline=(51, 65, 85, 255), width=2)
        draw_c.rectangle([px + 10, py + 10, px + 120, py + 35], fill=(0, 0, 0, 200))
        draw_c.text((px + 15, py + 14), f"t = {timestamps[i]:04.1f}s", font=FONT_LABEL, fill=CYAN_PRIMARY)

    contact_path = OUTPUT_DIR / "character_demonstration_contact_sheet.png"
    contact_im.save(contact_path)
    print(f"Forensic contact sheet saved: {contact_path.name}")

    # Step 5: Save Demonstration Manifest
    manifest = {
        "manifest_version": "1.0.0",
        "phase": "PHASE_13_CHARACTER_INTEGRATION",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "host_identity": {
            "provisional_name": "Kavi",
            "canonical_reference": "character.me.png",
            "voice_model": "Kokoro-82M am_liam (General American)",
            "voice_normalized_loudness": "-16 LUFS (EBU R128)"
        },
        "demonstration_scenes": [
            {
                "scene_id": s["id"],
                "name": s["name"],
                "editorial_role": s["config"].editorial_reason,
                "pose": s["config"].pose.value,
                "screen_position": s["config"].screen_position.value,
                "duration_seconds": stems_meta[s["id"]]["scene_duration"],
                "video_file": str((SCENES_DIR / f"{s['id']}.mp4").as_posix())
            }
            for s in DEMO_SCENES
        ],
        "preview_video": str(master_mp4.as_posix()),
        "forensic_contact_sheet": str(contact_path.as_posix()),
        "total_runtime_seconds": sum(stems_meta[s["id"]]["scene_duration"] for s in DEMO_SCENES),
        "publishing_safety": "RESTRICTED (Demo output only - zero public distribution)"
    }

    manifest_file = OUTPUT_DIR / "demonstration_manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written: {manifest_file.name}")
    print("\n" + "=" * 80)
    print("PHASE 13 DEMONSTRATION RENDERING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    produce_demonstration()
