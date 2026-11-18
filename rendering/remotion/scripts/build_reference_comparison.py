from PIL import Image, ImageDraw, ImageFont
import os

ref_path = "A:/SUPER.INTELLIGENCEEE/output/experiment_a3/reference_study/ref_face_closeup.png"
rec_path = "A:/SUPER.INTELLIGENCEEE/output/experiment_a3/character_front.png"
out_path = "A:/SUPER.INTELLIGENCEEE/output/experiment_a3/reference_comparison.png"

ref = Image.open(ref_path).convert("RGB")
rec = Image.open(rec_path).convert("RGB")

w, h = rec.size
crop_box = (60, 100, w - 60, 1500)
rec_cropped = rec.crop(crop_box)

target_h = 1000
rec_aspect = rec_cropped.width / rec_cropped.height
target_w_rec = int(target_h * rec_aspect)
rec_resized = rec_cropped.resize((target_w_rec, target_h), Image.Resampling.LANCZOS)

ref_aspect = ref.width / ref.height
target_w_ref = int(target_h * ref_aspect)
ref_resized = ref.resize((target_w_ref, target_h), Image.Resampling.LANCZOS)

header_h = 140
footer_h = 140
canvas_w = target_w_ref + target_w_rec + 30
canvas_h = target_h + header_h + footer_h

canvas = Image.new("RGB", (canvas_w, canvas_h), (20, 22, 28))
draw = ImageDraw.Draw(canvas)

# Paste images
canvas.paste(ref_resized, (10, header_h))
canvas.paste(rec_resized, (target_w_ref + 20, header_h))

# Draw border divider
draw.line([(target_w_ref + 15, header_h), (target_w_ref + 15, header_h + target_h)], fill=(60, 65, 78), width=3)

# Load font
try:
    font_title = ImageFont.truetype("arial.ttf", 34)
    font_label = ImageFont.truetype("arialbd.ttf", 26)
    font_sub = ImageFont.truetype("arial.ttf", 19)
except:
    font_title = font_label = font_sub = ImageFont.load_default()

# Header
draw.text((canvas_w // 2, 45), "SUPER.INTELLIGENCEEE — EXPERIMENT A.3", fill=(255, 255, 255), font=font_title, anchor="mm")
draw.text((canvas_w // 2, 85), "Reference-Accurate 3D Character Reconstruction vs Character 3D.mp4", fill=(255, 120, 30), font=font_sub, anchor="mm")

# Column Labels
draw.text((target_w_ref // 2 + 10, header_h - 25), "PRIMARY REFERENCE (Character 3D.mp4)", fill=(100, 220, 255), font=font_label, anchor="mm")
draw.text((target_w_ref + 20 + target_w_rec // 2, header_h - 25), "RECONSTRUCTED 3D ASSET (Kavi v3.4 GLB)", fill=(100, 255, 140), font=font_label, anchor="mm")

# Footer Callouts
f1 = "Fidelity: Open Forehead | Dense Organic Curly Locks | Hooded Almond Eyes | Acetate Spectacles"
f2 = "Conformal Groomed Beard | Standing Funnel Collar | Raglan Orange Trim | Spiral Reporter Notebook and Pencil"
draw.text((canvas_w // 2, canvas_h - 85), f1, fill=(200, 205, 215), font=font_sub, anchor="mm")
draw.text((canvas_w // 2, canvas_h - 50), f2, fill=(160, 165, 175), font=font_sub, anchor="mm")

canvas.save(out_path, quality=95)
print(f"Saved reference comparison to: {out_path} ({canvas_w}x{canvas_h})")
