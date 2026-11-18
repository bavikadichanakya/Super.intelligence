"""
Generate an expanded 6-frame forensic contact sheet for Phase 4.3.3 visual verification.
Samples two frames per scene:
Scene 1: 3.0s, 7.0s
Scene 2: 12.0s, 18.0s
Scene 3: 24.0s, 29.0s
"""

from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

def generate_expanded_sheet():
    run_dir = Path("A:/SUPER.INTELLIGENCEEE/output/drafts/phase433_explainer_demo").resolve()
    captioned_mp4 = list((run_dir / "masters").glob("*_captioned_review.mp4"))[0]
    out_dir = run_dir / "qa"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    timestamps = [3.0, 7.5, 13.0, 18.5, 24.5, 29.5]
    labels = [
        "SCENE 1: Computing Infrastructure (M4 Nodes Ingress)",
        "SCENE 1: Hardware Cluster (Command Dispatch Pulse)",
        "SCENE 2: Zero-Trust Security Boundary (Policy Filter)",
        "SCENE 2: Interleaved Hardware Queue (Multi-Tenant)",
        "SCENE 3: Comparative Benchmark (38% -> 78% Duty Cycle)",
        "SCENE 3: Architectural Verdict & Engineering Synthesis"
    ]
    
    extracted_frames = []
    for i, ts in enumerate(timestamps):
        fp = out_dir / f"forensic_frame_{i+1:02d}_{ts:.1f}s.png"
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{ts:.2f}",
            "-i", str(captioned_mp4),
            "-vframes", "1",
            "-f", "image2",
            str(fp)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        extracted_frames.append((ts, fp))
    
    # Compose 2 rows x 3 columns contact sheet
    cols = 3
    rows = 2
    thumb_w = 480
    thumb_h = 853 # 9:16 aspect ratio
    margin = 30
    header_h = 100
    
    sheet_w = cols * thumb_w + (cols + 1) * margin
    sheet_h = header_h + rows * (thumb_h + 70) + (rows + 1) * margin
    
    sheet = Image.new("RGB", (sheet_w, sheet_h), (250, 247, 242)) # Warm ivory background
    draw = ImageDraw.Draw(sheet)
    
    # Title Header
    draw.text((margin, 24), "SUPER.INTELLIGENCEEE — PHASE 4.3.3 FORENSIC CONTACT SHEET", fill=(15, 23, 42))
    draw.text((margin, 58), "Target: arXiv:2611.17294v1 (Metal Sandbox) | Voice: Kokoro am_liam | Theme: Light-First Explainer", fill=(71, 85, 105))
    draw.line([(margin, 90), (sheet_w - margin, 90)], fill=(203, 213, 225), width=2)
    
    for i, (ts, fp) in enumerate(extracted_frames):
        c = i % cols
        r = i // cols
        
        x = margin + c * (thumb_w + margin)
        y = header_h + margin + r * (thumb_h + 70 + margin)
        
        with Image.open(fp) as im:
            thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y))
            # Border outline
            draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], outline=(2, 132, 199), width=2)
            
            # Label banner
            lbl = labels[i]
            draw.rounded_rectangle([(x, y + thumb_h + 8), (x + thumb_w, y + thumb_h + 52)], radius=6, fill=(15, 23, 42))
            draw.text((x + 12, y + thumb_h + 16), f"[{ts:04.1f}s] {lbl}", fill=(255, 255, 255))
            
    out_sheet_path = out_dir / "phase433_expanded_forensic_contact_sheet.png"
    sheet.save(out_sheet_path, format="PNG")
    print(f"Saved expanded forensic contact sheet: {out_sheet_path}")

if __name__ == "__main__":
    generate_expanded_sheet()
