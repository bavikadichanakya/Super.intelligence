"""
Phase 4.3.2C.1 Visual & Audio Analysis Script
Extracts 12 representative frames, generates an expanded contact sheet,
and runs EBU R128 audio analysis on the masters and audio stems.
"""
import os
import subprocess
import json
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path("A:/SUPER.INTELLIGENCEEE")
PRODUCTION_DIR = PROJECT_ROOT / "output" / "drafts" / "phase432c_production_run"
MASTERS_DIR = PRODUCTION_DIR / "masters"
AUDIO_DIR = PRODUCTION_DIR / "audio"
QA_DIR = PRODUCTION_DIR / "qa"
FRAMES_DIR = QA_DIR / "audit_frames"

CAPTIONS_MASTER = MASTERS_DIR / "reel_20261113_224800_metal_sandbox__isolated_execut_captioned_review.mp4"
CLEAN_MASTER = MASTERS_DIR / "reel_20261113_224800_metal_sandbox__isolated_execut_clean_master.mp4"
MASTER_AUDIO = AUDIO_DIR / "master_narration_16lufs.wav"

TIMESTAMPS = [
    (1.0, "scene1_opening"),
    (3.0, "scene1_problem"),
    (7.0, "scene1_setup"),
    (10.0, "scene1_handoff"),
    (11.5, "scene2_manim_intro"),
    (15.0, "scene2_manim_graph_curve"),
    (18.0, "scene2_manim_efficiency"),
    (20.0, "scene2_manim_peak"),
    (22.0, "scene2_transition"),
    (25.0, "scene3_verdict_start"),
    (29.0, "scene3_verdict_content"),
    (33.0, "scene3_outro"),
]

def extract_frames():
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    extracted = []
    
    for ts, label in TIMESTAMPS:
        out_name = f"frame_{ts:05.1f}s_{label}.png"
        out_path = FRAMES_DIR / out_name
        cmd = [
            "ffmpeg", "-y", "-ss", str(ts),
            "-i", str(CAPTIONS_MASTER),
            "-frames:v", "1",
            "-q:v", "2",
            str(out_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if out_path.exists():
            extracted.append((ts, label, out_path))
            print(f"[OK] Extracted {out_name} at {ts}s")
        else:
            print(f"[FAIL] Could not extract frame at {ts}s: {res.stderr}")

    return extracted

def build_expanded_contact_sheet(extracted):
    if not extracted:
        return
    # 4 columns, 3 rows = 12 images
    cols = 4
    rows = 3
    thumb_w = 360
    thumb_h = 640
    header_h = 40
    
    sheet_w = cols * thumb_w
    sheet_h = rows * (thumb_h + header_h)
    
    sheet = Image.new("RGB", (sheet_w, sheet_h), color=(15, 17, 23))
    
    # We can use Pillow's ImageDraw if needed, or simple collage
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(sheet)
    
    for idx, (ts, label, path) in enumerate(extracted[:12]):
        c = idx % cols
        r = idx // cols
        
        x = c * thumb_w
        y = r * (thumb_h + header_h)
        
        with Image.open(path) as img:
            thumb = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y + header_h))
            
        # Draw label header
        draw.rectangle([x, y, x + thumb_w, y + header_h], fill=(24, 28, 38))
        draw.text((x + 10, y + 12), f"t={ts:.1f}s | {label}", fill=(220, 225, 235))
        
    out_sheet_path = QA_DIR / "phase432c1_expanded_contact_sheet.png"
    sheet.save(out_sheet_path)
    print(f"[OK] Saved expanded contact sheet: {out_sheet_path} ({sheet_w}x{sheet_h})")

def analyze_audio_loudness(audio_path):
    print(f"\n--- Analyzing Loudness for: {audio_path.name} ---")
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    # Extract Summary from stderr
    stderr = res.stderr
    summary_idx = stderr.rfind("Summary:")
    if summary_idx != -1:
        summary_text = stderr[summary_idx:]
        print(summary_text)
    else:
        print("No EBU R128 summary found in stderr.")

if __name__ == "__main__":
    extracted = extract_frames()
    build_expanded_contact_sheet(extracted)
    analyze_audio_loudness(MASTER_AUDIO)
    analyze_audio_loudness(CAPTIONS_MASTER)

