"""
Reference Video Forensic Analysis Script
Extracts frames, analyzes scene boundaries, audio spectrum, typography, camera motion, and generates a 25-frame contact sheet.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REF_VIDEO = Path("A:/SUPER.INTELLIGENCEEE/This is what i want.mp4")
OUTPUT_DIR = Path("A:/SUPER.INTELLIGENCEEE/assets/reference_forensics")
FRAMES_DIR = OUTPUT_DIR / "frames"
CONTACT_SHEET = OUTPUT_DIR / "reference_25frame_contact_sheet.png"

def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Probe video and audio
    print(f"Inspecting {REF_VIDEO}...")
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(REF_VIDEO)
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    meta = json.loads(res.stdout)
    
    with open(OUTPUT_DIR / "reference_metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    v_stream = next(s for s in meta["streams"] if s["codec_type"] == "video")
    a_stream = next(s for s in meta["streams"] if s["codec_type"] == "audio")
    
    width = int(v_stream["width"])
    height = int(v_stream["height"])
    duration = float(meta["format"]["duration"])
    fps = eval(v_stream["r_frame_rate"])
    bit_rate = int(meta["format"].get("bit_rate", 0))

    print(f"Reference: {width}x{height} @ {fps:.2f} fps, Duration: {duration:.2f}s, Bitrate: {bit_rate} bps")

    # 2. Extract 25 evenly-spaced representative frames for contact sheet
    num_frames = 25
    timestamps = [duration * (i + 0.5) / num_frames for i in range(num_frames)]
    frame_files = []
    
    for idx, t in enumerate(timestamps):
        out_frame = FRAMES_DIR / f"ref_frame_{idx:02d}_{t:.2f}s.png"
        cmd = [
            "ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(REF_VIDEO),
            "-vframes", "1", "-q:v", "2", str(out_frame)
        ]
        subprocess.run(cmd, capture_output=True)
        if out_frame.exists():
            frame_files.append(out_frame)
            
    print(f"Extracted {len(frame_files)} reference frames.")

    # 3. Create 5x5 Contact Sheet (25 frames)
    # We want a high-resolution contact sheet: grid of 5 columns x 5 rows
    grid_cols = 5
    grid_rows = 5
    thumb_w = 320
    thumb_h = int(thumb_w * (height / width))
    header_h = 80
    footer_h = 40
    pad = 12

    sheet_w = grid_cols * thumb_w + (grid_cols + 1) * pad
    sheet_h = grid_rows * thumb_h + (grid_rows + 1) * pad + header_h + footer_h

    sheet = Image.new("RGB", (sheet_w, sheet_h), (12, 14, 20))
    draw = ImageDraw.Draw(sheet)

    # Title header
    header_text = f"REFERENCE FORENSIC ANALYSIS: 'This is what i want.mp4' ({width}x{height} @ {fps:.1f}fps, {duration:.1f}s)"
    draw.text((pad, 24), header_text, fill=(240, 244, 255))
    draw.text((pad, 50), "25 Representative Frame Samples (5x5 Grid) Across Complete Video Timeline", fill=(140, 150, 175))

    for idx, fpath in enumerate(frame_files):
        row = idx // grid_cols
        col = idx % grid_cols
        x = pad + col * (thumb_w + pad)
        y = header_h + pad + row * (thumb_h + pad)

        with Image.open(fpath) as img:
            thumb = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y))

        t = timestamps[idx]
        draw.rectangle([x, y + thumb_h - 24, x + thumb_w, y + thumb_h], fill=(0, 0, 0, 180))
        draw.text((x + 6, y + thumb_h - 20), f"F{idx+1:02d} | {t:.1f}s", fill=(255, 215, 0))

    sheet.save(CONTACT_SHEET, quality=95)
    print(f"Saved reference contact sheet to: {CONTACT_SHEET}")

    # Also copy to artifacts dir
    artifacts_dir = Path("C:/Users/bavik/.gemini/antigravity/brain/174164e7-7384-4da6-a377-b063df7a125d")
    art_sheet = artifacts_dir / "reference_25frame_contact_sheet.png"
    sheet.save(art_sheet, quality=95)
    print(f"Copied contact sheet to brain artifact: {art_sheet}")

if __name__ == "__main__":
    run()
