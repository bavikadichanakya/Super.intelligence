"""
SUPER.INTELLIGENCEEE — Phase 4.2A.3 Independent Visual & Motion Audit Script
Extracts frames, analyzes motion dynamics, performs safe-zone text-boundary checks,
and generates the 9-frame forensic contact sheet for Phase 4.2A.2 prototypes.
"""

import math
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont
import numpy as np

AUDIT_DIR = Path("output/drafts/phase42a_3_audit")
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

PROTOTYPES_DIR = Path("output/drafts/phase42a_2_validation")
BRAIN_DIR = Path("C:/Users/bavik/.gemini/antigravity/brain/174164e7-7384-4da6-a377-b063df7a125d")

FONT_PATH_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")
FONT_PATH_REG = Path("C:/Windows/Fonts/arial.ttf")
FONT_PATH_MONO = Path("C:/Windows/Fonts/consola.ttf")

def get_font(path: Path, size: int):
    if path.exists():
        try:
            return ImageFont.truetype(str(path), size)
        except Exception:
            pass
    return ImageFont.load_default()

FONT_TITLE = get_font(FONT_PATH_BOLD, 32)
FONT_LABEL = get_font(FONT_PATH_MONO, 22)
FONT_BADGE = get_font(FONT_PATH_BOLD, 20)

# ---------------------------------------------------------------------------
# 1. Extract Representative Frames via FFmpeg
# ---------------------------------------------------------------------------
def extract_frames_from_video(video_path: Path, prefix: str) -> Dict[str, Image.Image]:
    extracted = {}
    frame_indices = [0, 45, 89]
    frame_names = ["beginning_f00", "middle_f45", "end_f89"]
    
    for idx, name in zip(frame_indices, frame_names):
        out_png = AUDIT_DIR / f"{prefix}_{name}.png"
        cmd = [
            "ffmpeg", "-y",
            "-loglevel", "error",
            "-i", str(video_path),
            "-vf", f"select=eq(n\\,{idx})",
            "-vframes", "1",
            str(out_png)
        ]
        subprocess.run(cmd, check=True)
        img = Image.open(out_png)
        extracted[name] = img
        print(f"[OK] Extracted {prefix} frame {idx} -> {out_png}")
    return extracted

# ---------------------------------------------------------------------------
# 2. Frame-by-Frame Motion & Delta Analysis
# ---------------------------------------------------------------------------
def analyze_video_motion(video_path: Path) -> Dict[str, any]:
    """
    Extracts all 90 frames to memory and computes:
    - Mean pixel absolute difference between consecutive frames.
    - Motion distribution (active movement vs static holds).
    - Camera push measurement.
    """
    cmd = [
        "ffmpeg",
        "-loglevel", "error",
        "-i", str(video_path),
        "-f", "image2pipe",
        "-pix_fmt", "rgb24",
        "-vcodec", "rawvideo",
        "-"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    w, h = 1080, 1920
    frame_bytes = w * h * 3
    frames = []
    
    while True:
        raw = proc.stdout.read(frame_bytes)
        if len(raw) < frame_bytes:
            break
        arr = np.frombuffer(raw, dtype=np.uint8).reshape((h, w, 3))
        frames.append(arr)
        
    proc.wait()
    total_frames = len(frames)
    
    deltas = []
    for i in range(total_frames - 1):
        diff = np.abs(frames[i+1].astype(np.float32) - frames[i].astype(np.float32))
        deltas.append(float(np.mean(diff)))
        
    static_frames = sum(1 for d in deltas if d < 0.05)
    active_frames = sum(1 for d in deltas if d >= 0.05)
    
    # Analyze region of motion (Top, Middle, Bottom)
    top_diff = []
    mid_diff = []
    bot_diff = []
    for i in range(total_frames - 1):
        diff = np.abs(frames[i+1].astype(np.float32) - frames[i].astype(np.float32))
        top_diff.append(float(np.mean(diff[0:400, :, :])))
        mid_diff.append(float(np.mean(diff[400:1300, :, :])))
        bot_diff.append(float(np.mean(diff[1300:1920, :, :])))
        
    return {
        "total_frames": total_frames,
        "mean_consecutive_delta": float(np.mean(deltas)),
        "max_delta": float(np.max(deltas)),
        "min_delta": float(np.min(deltas)),
        "static_frame_count": static_frames,
        "active_frame_count": active_frames,
        "top_mean_delta": float(np.mean(top_diff)),
        "mid_mean_delta": float(np.mean(mid_diff)),
        "bot_mean_delta": float(np.mean(bot_diff)),
    }

# ---------------------------------------------------------------------------
# 3. Static Text-Boundary and Safe-Zone Audit
# ---------------------------------------------------------------------------
def audit_static_image(img_path: Path) -> Dict[str, any]:
    img = Image.open(img_path)
    w, h = img.size
    arr = np.array(img)
    
    # Safe zone bounds: Top 140px, Bottom 260px (Y <= 1660), Lateral 80px
    # Let's check non-background pixel distribution in the margins
    # Background color is estimated from corners
    corner_pixels = [arr[10, 10], arr[10, w-10], arr[h-10, 10], arr[h-10, w-10]]
    bg_est = np.median(corner_pixels, axis=0)
    
    diff = np.sum(np.abs(arr.astype(np.float32) - bg_est), axis=2)
    # Binary mask of foreground content
    fg_mask = diff > 25.0
    
    # Check top margin violations (Y < 140)
    top_violations = np.sum(fg_mask[0:140, :])
    # Check bottom margin violations (Y > 1660)
    bottom_violations = np.sum(fg_mask[1660:1920, :])
    # Check left margin violations (X < 80)
    left_violations = np.sum(fg_mask[:, 0:80])
    # Check right margin violations (X > 1000)
    right_violations = np.sum(fg_mask[:, 1000:1080])
    
    # Identify content bounding box
    y_indices, x_indices = np.where(fg_mask)
    if len(y_indices) > 0:
        min_y, max_y = int(np.min(y_indices)), int(np.max(y_indices))
        min_x, max_x = int(np.min(x_indices)), int(np.max(x_indices))
    else:
        min_y, max_y, min_x, max_x = 0, h, 0, w

    return {
        "dimensions": (w, h),
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "top_margin_px": min_y,
        "bottom_margin_px": h - max_y,
        "left_margin_px": min_x,
        "right_margin_px": w - max_x,
        "top_violations_pixels": int(top_violations),
        "bottom_violations_pixels": int(bottom_violations),
        "left_violations_pixels": int(left_violations),
        "right_violations_pixels": int(right_violations),
    }

# ---------------------------------------------------------------------------
# 4. Generate 9-Frame Forensic Contact Sheet
# ---------------------------------------------------------------------------
def generate_forensic_contact_sheet(
    frames_dict: Dict[str, Dict[str, Image.Image]],
    output_path: Path
):
    """
    Constructs a 3x3 matrix showing:
    Row 1: Sequence A (Beginning f0, Mid f45, End f89)
    Row 2: Sequence B (Beginning f0, Mid f45, End f89)
    Row 3: Sequence C (Beginning f0, Mid f45, End f89)
    """
    col_w = 400
    col_h = 711  # 9:16 ratio scaled down
    header_h = 100
    subhead_h = 40
    padding = 24
    
    sheet_w = padding * 4 + col_w * 3
    sheet_h = header_h + (subhead_h + col_h + padding) * 3 + padding
    
    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 243, 238))
    draw = ImageDraw.Draw(sheet)
    
    # Title Header
    draw.rectangle([(0, 0), (sheet_w, header_h)], fill=(15, 23, 42))
    draw.text((padding, 24), "SUPER.INTELLIGENCEEE  |  PHASE 4.2A.3 INDEPENDENT FORENSIC AUDIT", font=FONT_TITLE, fill=(255, 255, 255))
    draw.text((padding, 66), "FRAME PROGRESSION ANALYSIS // 9-FRAME AUDIT MATRIX (1080x1920 @ 30FPS)", font=FONT_LABEL, fill=(56, 189, 248))
    
    sequences = [
        ("seq_a", "SEQUENCE A: THE EXPLORATION CEILING (CINEMATIC MACRO)"),
        ("seq_b", "SEQUENCE B: ON-POLICY DISTILLATION DYNAMICS (ALGORITHMIC)"),
        ("seq_c", "SEQUENCE C: CONCEPTUAL EFFICIENCY MATRIX (EDITORIAL)")
    ]
    frame_keys = ["beginning_f00", "middle_f45", "end_f89"]
    frame_labels = ["FRAME 000 (t=0.00s)", "FRAME 045 (t=1.50s)", "FRAME 089 (t=2.97s)"]
    
    curr_y = header_h + padding
    
    for seq_key, seq_title in sequences:
        # Row Header
        draw.rectangle([(padding, curr_y), (sheet_w - padding, curr_y + 32)], fill=(226, 232, 240))
        draw.text((padding + 12, curr_y + 6), seq_title, font=FONT_BADGE, fill=(15, 23, 42))
        curr_y += 38
        
        for col_idx, (f_key, f_label) in enumerate(zip(frame_keys, frame_labels)):
            img = frames_dict[seq_key][f_key]
            thumb = img.resize((col_w, col_h), Image.Resampling.LANCZOS)
            x_pos = padding + col_idx * (col_w + padding)
            
            # Draw thumbnail with border
            draw.rectangle([(x_pos - 1, curr_y - 1), (x_pos + col_w + 1, curr_y + col_h + 1)], outline=(180, 175, 165), width=1)
            sheet.paste(thumb, (x_pos, curr_y))
            
            # Sub-label bar
            draw.rectangle([(x_pos, curr_y + col_h - 28), (x_pos + col_w, curr_y + col_h)], fill=(15, 23, 42))
            draw.text((x_pos + 10, curr_y + col_h - 22), f_label, font=FONT_LABEL, fill=(248, 250, 252))
            
        curr_y += col_h + padding
        
    sheet.save(output_path, quality=95)
    print(f"[OK] Saved 9-Frame Forensic Contact Sheet: {output_path}")

# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("SUPER.INTELLIGENCEEE — PHASE 4.2A.3 INDEPENDENT AUDIT EXECUTION")
    print("=" * 70)
    
    # 1. Extract frames
    frames_dict = {}
    for seq_key, vid_name in [
        ("seq_a", "sequence_a_motion_prototype_v2.mp4"),
        ("seq_b", "sequence_b_motion_prototype_v2.mp4"),
        ("seq_c", "sequence_c_motion_prototype_v2.mp4")
    ]:
        vid_p = PROTOTYPES_DIR / vid_name
        frames_dict[seq_key] = extract_frames_from_video(vid_p, seq_key)
        
    # 2. Motion Analysis
    print("\nExecuting Frame-by-Frame Motion Analysis...")
    motion_results = {}
    for seq_key, vid_name in [
        ("seq_a", "sequence_a_motion_prototype_v2.mp4"),
        ("seq_b", "sequence_b_motion_prototype_v2.mp4"),
        ("seq_c", "sequence_c_motion_prototype_v2.mp4")
    ]:
        vid_p = PROTOTYPES_DIR / vid_name
        res = analyze_video_motion(vid_p)
        motion_results[seq_key] = res
        print(f"[{seq_key.upper()}] Motion Analysis:")
        print(f"  Total Frames: {res['total_frames']}")
        print(f"  Mean Frame Delta: {res['mean_consecutive_delta']:.4f}")
        print(f"  Top/Mid/Bot Delta: {res['top_mean_delta']:.4f} / {res['mid_mean_delta']:.4f} / {res['bot_mean_delta']:.4f}")
        print(f"  Active vs Static Frames: {res['active_frame_count']} / {res['static_frame_count']}")

    # 3. Static Text-Boundary Analysis
    print("\nExecuting Static Safe-Zone & Clipping Analysis...")
    static_results = {}
    for seq_key, img_name in [
        ("seq_a", "sequence_a_final_review.png"),
        ("seq_b", "sequence_b_final_review.png"),
        ("seq_c", "sequence_c_final_review.png")
    ]:
        img_p = PROTOTYPES_DIR / img_name
        res = audit_static_image(img_p)
        static_results[seq_key] = res
        print(f"[{seq_key.upper()}] Static Bounds:")
        print(f"  Bounding Box: Y=[{res['min_y']}, {res['max_y']}], X=[{res['min_x']}, {res['max_x']}]")
        print(f"  Top Margin: {res['top_margin_px']}px (Safe >= 140)")
        print(f"  Bottom Margin: {res['bottom_margin_px']}px (Safe >= 260)")
        print(f"  Lateral Margin: Left={res['left_margin_px']}px, Right={res['right_margin_px']}px (Safe >= 80)")
        
    # 4. Generate 9-Frame Contact Sheet
    contact_sheet_path = AUDIT_DIR / "phase42a_3_contact_sheet.png"
    generate_forensic_contact_sheet(frames_dict, contact_sheet_path)
    
    # 5. Copy artifacts to Brain Directory
    print(f"\nCopying audit artifacts to Brain Directory: {BRAIN_DIR}")
    for f in AUDIT_DIR.glob("*.*"):
        shutil.copy2(f, BRAIN_DIR / f.name)
        print(f"  -> Copied {f.name}")
        
    print("\n[SUCCESS] Phase 4.2A.3 Audit Extraction and Analysis Completed.")

if __name__ == "__main__":
    main()
