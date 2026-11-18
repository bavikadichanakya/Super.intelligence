import hashlib
import json
import subprocess
from pathlib import Path

run_dir = Path("A:/SUPER.INTELLIGENCEEE/output/drafts/phase432c_production_run")
manifest_path = run_dir / "production_manifest.json"

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print("=" * 80)
print("PHASE 4.3.2C.1 — ARTIFACT INTEGRITY AUDIT")
print("=" * 80)
print(f"Manifest Status:     {manifest.get('status')}")
print(f"Job ID:              {manifest.get('job_id')}")
print(f"Approval ID:         {manifest.get('approval_id')}")
print(f"Topic Title:         {manifest.get('topic', {}).get('title')}")
print(f"Reported Duration:   {manifest.get('duration_seconds')}s")

def compute_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

media_targets = [
    ("Captioned Review Master", run_dir / "masters" / "reel_20261113_224800_metal_sandbox__isolated_execut_captioned_review.mp4"),
    ("Clean Archival Master", run_dir / "masters" / "reel_20261113_224800_metal_sandbox__isolated_execut_clean_master.mp4"),
    ("Master Narration (16 LUFS)", run_dir / "audio" / "master_narration_16lufs.wav"),
    ("Master Narration (Raw)", run_dir / "audio" / "master_narration_raw.wav"),
    ("Scene 1 Narration", run_dir / "audio" / "scene_01_narration.wav"),
    ("Scene 2 Narration", run_dir / "audio" / "scene_02_narration.wav"),
    ("Scene 3 Narration", run_dir / "audio" / "scene_03_narration.wav"),
    ("Scene 1 Stem", run_dir / "stems" / "reel_20261113_224800_metal_sandbox__isolated_execut_scene_01.mp4"),
    ("Scene 2 Stem", run_dir / "stems" / "reel_20261113_224800_metal_sandbox__isolated_execut_scene_02.mp4"),
    ("Scene 3 Stem", run_dir / "stems" / "reel_20261113_224800_metal_sandbox__isolated_execut_scene_03.mp4"),
    ("Visual Contact Sheet", run_dir / "qa" / "reel_20261113_224800_metal_sandbox__isolated_execut_contact_sheet.png"),
]

# Map manifest stem hashes
manifest_stems = {Path(s["path"]).name: s for s in manifest.get("stems", [])}

results = []

for label, p in media_targets:
    if not p.exists():
        print(f"\n[FAIL] {label}: MISSING at {p}")
        results.append({"label": label, "exists": False})
        continue

    file_size = p.stat().st_size
    actual_hash = compute_sha256(p)

    # Compare with manifest if available
    manifest_match = "N/A"
    if p.name in manifest_stems:
        expected_hash = manifest_stems[p.name].get("sha256")
        manifest_match = "MATCH" if actual_hash == expected_hash else f"MISMATCH (expected {expected_hash[:12]}...)"

    # ffprobe metadata
    cmd_probe = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=index,codec_name,codec_type,width,height,r_frame_rate,duration,channels,sample_rate",
        "-show_entries", "format=duration,size,bit_rate",
        "-of", "json",
        str(p)
    ]
    res_probe = subprocess.run(cmd_probe, capture_output=True, text=True)
    probe_data = json.loads(res_probe.stdout) if res_probe.returncode == 0 else {}

    # ffmpeg decode check
    cmd_decode = ["ffmpeg", "-v", "error", "-i", str(p), "-f", "null", "-"]
    res_decode = subprocess.run(cmd_decode, capture_output=True, text=True)
    decode_clean = (res_decode.returncode == 0 and len(res_decode.stderr.strip()) == 0)

    print(f"\n--- {label} ---")
    print(f"Path:            {p}")
    print(f"Size:            {file_size:,} bytes")
    print(f"SHA-256:         {actual_hash}")
    print(f"Manifest Match:  {manifest_match}")
    print(f"Decode Clean:    {decode_clean} {'(Errors: ' + res_decode.stderr.strip() + ')' if not decode_clean else ''}")
    format_info = probe_data.get("format", {})
    print(f"Format Duration: {format_info.get('duration')}s | Bitrate: {format_info.get('bit_rate')} bps")
    for s in probe_data.get("streams", []):
        ctype = s.get("codec_type")
        cname = s.get("codec_name")
        if ctype == "video":
            print(f"  Stream #{s.get('index')} (Video): {cname} | {s.get('width')}x{s.get('height')} | fps: {s.get('r_frame_rate')} | dur: {s.get('duration')}s")
        elif ctype == "audio":
            print(f"  Stream #{s.get('index')} (Audio): {cname} | {s.get('channels')} ch | {s.get('sample_rate')} Hz | dur: {s.get('duration')}s")

print("\n" + "=" * 80)

