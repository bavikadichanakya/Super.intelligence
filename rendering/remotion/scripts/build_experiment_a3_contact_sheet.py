import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

video_path = "A:/SUPER.INTELLIGENCEEE/output/experiment_a3/character_3d_validation.mp4"
frames_dir = "A:/SUPER.INTELLIGENCEEE/output/experiment_a3/frames"
artifact_dir = "C:/Users/bavik/.gemini/antigravity/brain/174164e7-7384-4da6-a377-b063df7a125d"
out_contact = "A:/SUPER.INTELLIGENCEEE/output/experiment_a3/experiment_a3_contact_sheet.png"

os.makedirs(frames_dir, exist_ok=True)

keyframe_defs = [
    {"frame": 20, "name": "f01_neutral", "title": "1. Neutral Standing Pose", "time": "0.7s"},
    {"frame": 68, "name": "f02_head_rotation", "title": "2. Head Rotation (3D Vol)", "time": "2.3s"},
    {"frame": 115, "name": "f03_eye_tracking", "title": "3. Eye Tracking Gaze", "time": "3.8s"},
    {"frame": 160, "name": "f04_blink", "title": "4. Natural Blink Cycle", "time": "5.3s"},
    {"frame": 210, "name": "f05_curious", "title": "5. Curious Expression", "time": "7.0s"},
    {"frame": 265, "name": "f06_surprised", "title": "6. Surprised Expression", "time": "8.8s"},
    {"frame": 335, "name": "f07_explaining", "title": "7. Explaining Gesture", "time": "11.2s"},
    {"frame": 405, "name": "f08_both_arms", "title": "8. Both-Arm Movement", "time": "13.5s"},
    {"frame": 460, "name": "f09_notebook_interaction", "title": "9. Notebook Writing", "time": "15.3s"},
    {"frame": 520, "name": "f10_resolution", "title": "10. Hero Resolution", "time": "17.3s"},
]

print("Extracting 10 keyframes from character_3d_validation.mp4...")
extracted_images = []

for kf in keyframe_defs:
    f_num = kf["frame"]
    out_f = os.path.join(frames_dir, f"{kf['name']}.png")
    # ffmpeg extract specific frame
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"select=eq(n\\,{f_num})",
        "-vframes", "1",
        out_f
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    img = Image.open(out_f).convert("RGB")
    extracted_images.append((img, kf))
    
    # Also copy to artifact dir
    art_path = os.path.join(artifact_dir, f"{kf['name']}.png")
    img.save(art_path)
    print(f"Extracted {kf['name']} (frame {f_num})")

# Build 2-row x 5-column contact sheet
# Each frame is 1080x1920 (aspect ratio 9:16)
# Thumbnail size: width 360, height 640
thumb_w = 360
thumb_h = 640
cols = 5
rows = 2
margin = 20
header_h = 130
label_h = 50

canvas_w = cols * thumb_w + (cols + 1) * margin
canvas_h = header_h + rows * (thumb_h + label_h) + (rows + 1) * margin

canvas = Image.new("RGB", (canvas_w, canvas_h), (18, 20, 26))
draw = ImageDraw.Draw(canvas)

try:
    font_title = ImageFont.truetype("arial.ttf", 36)
    font_sub = ImageFont.truetype("arial.ttf", 22)
    font_label = ImageFont.truetype("arialbd.ttf", 17)
    font_time = ImageFont.truetype("arial.ttf", 15)
except:
    font_title = font_sub = font_label = font_time = ImageFont.load_default()

# Header
draw.text((canvas_w // 2, 45), "SUPER.INTELLIGENCEEE — EXPERIMENT A.3 VALIDATION CONTACT SHEET", fill=(255, 255, 255), font=font_title, anchor="mm")
draw.text((canvas_w // 2, 85), "10-Step Deterministic Kinematic & Expression Progression (18.0s @ 30 FPS)", fill=(255, 120, 30), font=font_sub, anchor="mm")

for idx, (img, kf) in enumerate(extracted_images):
    r = idx // cols
    c = idx % cols
    x = margin + c * (thumb_w + margin)
    y = header_h + margin + r * (thumb_h + label_h + margin)
    
    thumb = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    canvas.paste(thumb, (x, y))
    
    # Border around thumbnail
    draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(55, 60, 72), width=2)
    
    # Label bar
    bar_y = y + thumb_h + 8
    draw.text((x + thumb_w // 2, bar_y + 12), kf["title"], fill=(230, 235, 245), font=font_label, anchor="mm")
    draw.text((x + thumb_w // 2, bar_y + 32), f"Frame {kf['frame']} ({kf['time']})", fill=(130, 140, 160), font=font_time, anchor="mm")

canvas.save(out_contact, quality=95)
canvas.save(os.path.join(artifact_dir, "experiment_a3_contact_sheet.png"), quality=95)
print(f"Saved contact sheet to: {out_contact} ({canvas_w}x{canvas_h})")
