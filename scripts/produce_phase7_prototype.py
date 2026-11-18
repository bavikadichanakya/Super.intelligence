"""
SUPER.INTELLIGENCEEE — Phase 7.1 Visual Proof-of-Style Prototype Runner
Renders 12-15 second proof-of-style MP4 containing three genuinely distinct physical compositions:
1. Prototype A — Physical Concept (Volumetric Weight Discretization into Ternary States)
2. Prototype B — Physical Comparison (Datapath Mechanism & Qualified Arithmetic Energy Ratio)
3. Prototype C — Evidence and Reality (Official Microsoft Research Document & Published Benchmarks)

Strict Standards:
- Light-first editorial studio surface (#F5F3ED / #FAFAF8 / #E8E6E0)
- Hero objects commanding 65%-85% canvas width with real soft contact shadows
- Clean editorial typography (Sans Bold + Georgia Italic)
- Zero cyber grids, zero HUD corner reticles, zero card borders
- 1080x1920 @ 30fps High Profile, Kokoro am_liam voice, EBU R128 audio
- Deadlock-free direct memory pipe to FFmpeg
"""

from __future__ import annotations

import sys
from pathlib import Path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

import os
import time
import json
import hashlib
import sqlite3
import subprocess
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont

from core.universal_scene_contract import (
    UniversalSceneContract,
    VideoStoryboardContract,
    SceneType,
    RenderingEngine,
    FactClaimEvidence,
)
from audio.providers.kokoro_direct import KokoroDirectRunner
from audio.reference_sound_designer import ReferenceSoundDesigner
from rendering.physical_explainer_engine import (
    PhysicalConceptQuantizationComposition,
    PhysicalComparisonEnergyComposition,
    EvidenceRealityDocumentComposition,
)
from rendering.adapters.ffmpeg_adapter import FFmpegAdapter
from rendering.execution_context import ExecutionContext
from rendering.resource_guard import ResourceGuard


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def generate_25frame_contact_sheet(video_path: Path, output_path: Path, title: str) -> Path:
    """Extracts 25 evenly distributed frames and builds a 5x5 forensic contact sheet."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    duration = float(res.stdout.strip())

    num_frames = 25
    timestamps = [duration * (i + 0.5) / num_frames for i in range(num_frames)]

    temp_frames = []
    temp_dir = output_path.parent / f"temp_frames_{output_path.stem}"
    temp_dir.mkdir(parents=True, exist_ok=True)

    for i, ts in enumerate(timestamps):
        frame_file = temp_dir / f"frame_{i:02d}.png"
        extract_cmd = [
            "ffmpeg", "-y", "-ss", f"{ts:.3f}",
            "-i", str(video_path),
            "-vframes", "1",
            "-vf", "scale=360:640",
            str(frame_file)
        ]
        subprocess.run(extract_cmd, capture_output=True, check=True)
        temp_frames.append((frame_file, ts))

    grid_cols = 5
    grid_rows = 5
    thumb_w = 360
    thumb_h = 640
    header_h = 100
    footer_h = 60
    sheet_w = grid_cols * thumb_w
    sheet_h = header_h + (grid_rows * thumb_h) + footer_h

    sheet = Image.new("RGBA", (sheet_w, sheet_h), (245, 243, 237, 255))
    draw = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_ts = ImageFont.truetype("consola.ttf", 20)
        font_footer = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font_title = font_ts = font_footer = ImageFont.load_default()

    draw.rectangle([0, 0, sheet_w, header_h], fill=(15, 23, 42, 255))
    draw.text((30, 20), f"PHASE 7.1 VISUAL PROOF-OF-STYLE: {title.upper()}", fill=(241, 245, 249), font=font_title)
    draw.text((30, 64), f"Duration: {duration:.2f}s | Resolution: 1080x1920 @ 30fps | Surface: Light Editorial Studio | Zero Cyber Grids", fill=(56, 189, 248), font=font_footer)

    for idx, (frame_path, ts) in enumerate(temp_frames):
        c = idx % grid_cols
        r = idx // grid_cols
        x = c * thumb_w
        y = header_h + r * thumb_h

        img = Image.open(frame_path)
        sheet.paste(img, (x, y))

        draw.rectangle([x + 10, y + thumb_h - 36, x + 120, y + thumb_h - 10], fill=(0, 0, 0, 200))
        draw.text((x + 16, y + thumb_h - 34), f"{ts:05.2f}s", fill=(255, 255, 255), font=font_ts)

    draw.rectangle([0, sheet_h - footer_h, sheet_w, sheet_h], fill=(15, 23, 42, 255))
    draw.text((30, sheet_h - 42), "Phase 7.1 Art Direction: Volumetric 3D Geometry | Real Contact Shadows | Authentic Research Provenance", fill=(148, 163, 184), font=font_footer)

    sheet.save(output_path, "PNG")

    for f, _ in temp_frames:
        if f.exists():
            f.unlink()
    if temp_dir.exists():
        temp_dir.rmdir()

    return output_path


def render_composition_to_mp4(comp, output_mp4: Path, fps: float = 30.0) -> Path:
    """Streams in-memory RGBA frames directly to FFmpeg H.264 High Profile with deadlock protection."""
    w, h = comp.width, comp.height
    duration = comp.duration
    total_frames = int(round(duration * fps))

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{w}x{h}",
        "-pix_fmt", "rgba",
        "-r", f"{fps}",
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-profile:v", "high",
        "-pix_fmt", "yuv420p",
        "-b:v", "5000k",
        "-maxrate", "7000k",
        "-bufsize", "10000k",
        "-crf", "18",
        str(output_mp4)
    ]

    # Explicitly redirect stderr to DEVNULL with large buffer to prevent Windows pipe deadlock
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        bufsize=10**7,
    )
    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = comp.render_frame(t)
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg render failed with return code {proc.returncode}")

    return output_mp4


def run_prototype_production() -> Dict[str, Any]:
    print("\n" + "=" * 80)
    print("PHASE 7.1 VISUAL PROOF-OF-STYLE: 12-15S PHYSICAL EXPLAINER PROTOTYPE")
    print("=" * 80)

    out_base = WORKSPACE_ROOT / "output" / "drafts" / "phase7_visual_prototype"
    stems_dir = out_base / "stems"
    audio_dir = out_base / "audio"
    inspection_dir = WORKSPACE_ROOT / "reports" / "phase7_1" / "visual_inspection"

    stems_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    inspection_dir.mkdir(parents=True, exist_ok=True)

    # 1. Prototype Scenes Definition
    prototype_scenes = [
        {
            "id": "proto_concept",
            "name": "Prototype A — Physical Concept",
            "headline": "WEIGHT PRECISION",
            "subheadline": "from continuous volume to ternary states",
            "surface_theme": "warm_ivory",
            "camera_movement": "slow_zoom_in",
            "narration": "Every weight in a standard neural network is a continuous, high-precision volume.",
            "target_duration": 4.8,
            "comp_cls": PhysicalConceptQuantizationComposition,
        },
        {
            "id": "proto_comparison",
            "name": "Prototype B — Physical Comparison",
            "headline": "ENERGY WALL COLLAPSE",
            "subheadline": "seventy-one times less arithmetic energy on silicon",
            "surface_theme": "architectural_grey",
            "camera_movement": "crane_up",
            "narration": "Replacing floating-point multiplication with simple integer addition slashes arithmetic energy by seventy-one times.",
            "target_duration": 5.2,
            "comp_cls": PhysicalComparisonEnergyComposition,
        },
        {
            "id": "proto_evidence",
            "name": "Prototype C — Evidence & Reality",
            "headline": "PRIMARY RESEARCH PROVENANCE",
            "subheadline": "verified against Microsoft Research foundation paper",
            "surface_theme": "soft_white",
            "camera_movement": "pan_right",
            "narration": "Documented in Microsoft Research's foundation paper, seventy-billion parameter models now run locally on standard CPUs.",
            "target_duration": 4.8,
            "comp_cls": EvidenceRealityDocumentComposition,
        },
    ]

    # 2. Synthesize Speech via Kokoro am_liam (Batch Mode)
    print("\n[1/6] Synthesizing speech via Kokoro batch pipeline (am_liam)...")
    batch_items = []
    scene_audio_paths = []
    for sc in prototype_scenes:
        out_wav = audio_dir / f"{sc['id']}.wav"
        batch_items.append((sc["narration"].strip(), out_wav))
        scene_audio_paths.append(out_wav)

    runner = KokoroDirectRunner(workspace_root=WORKSPACE_ROOT)
    batch_results = runner.generate_batch(items=batch_items, voice_id="am_liam", speed=1.0)

    scene_durations = []
    for idx, (sc, (ok, meta)) in enumerate(zip(prototype_scenes, batch_results)):
        if not ok:
            raise RuntimeError(f"Kokoro batch synthesis failed for {sc['id']}: {meta}")
        dur = float(meta.get("duration", sc["target_duration"]))
        scene_durations.append(dur)
        sc["actual_duration"] = dur
        print(f"  -> {sc['name']}: {dur:.2f}s")

    total_duration = sum(scene_durations)
    print(f"  ✓ Total Prototype Narration Duration: {total_duration:.2f}s")

    # 3. Render the 3 Physical Explainer Stems
    print("\n[2/6] Rendering 1080x1920 Physical Explainer Stems...")
    stem_video_paths = []
    for idx, sc in enumerate(prototype_scenes):
        sc_id = sc["id"]
        exact_dur = sc["actual_duration"]

        contract = UniversalSceneContract(
            scene_id=f"phase7_{sc_id}",
            video_id="phase7_prototype",
            sequence_number=idx + 1,
            scene_type=SceneType.TECHNICAL_DIAGRAM,
            preferred_engine=RenderingEngine.NATIVE_MOTION,
            narrative_purpose=sc["headline"],
            audience_takeaway=f"Experience {sc['headline']} in physical editorial space",
            mechanism_description=sc["name"],
            target_duration_seconds=exact_dur,
            actual_duration_seconds=exact_dur,
            narration_duration_seconds=exact_dur,
            output_resolution=(1080, 1920),
            frame_rate=30.0,
            narration_text=sc["narration"],
            visual_concept=sc_id,
            evidence_items=[
                FactClaimEvidence(
                    claim_id=f"claim_{sc_id}",
                    claim_text=f"Phase 7 proof {sc_id}",
                    source_url="https://arxiv.org/abs/2402.17764",
                )
            ],
            engine_specific_config={
                "surface_theme": sc["surface_theme"],
                "camera_movement": sc["camera_movement"],
                "headline": sc["headline"],
                "subheadline": sc["subheadline"],
            }
        )

        comp = sc["comp_cls"](contract, width=1080, height=1920)
        out_stem_mp4 = stems_dir / f"{sc_id}.mp4"
        t0 = time.time()
        render_composition_to_mp4(comp, out_stem_mp4, fps=30.0)
        t_el = time.time() - t0
        stem_video_paths.append(out_stem_mp4)
        print(f"  -> Rendered {sc['name']}: {out_stem_mp4.stat().st_size / 1024 / 1024:.2f} MB in {t_el:.1f}s")

    # 4. Master Audio (Concatenate & Lo-Fi Bed Mix)
    print("\n[3/6] Engineering Master Soundtrack with lo-fi bed and sidechain ducking...")
    concat_speech_wav = audio_dir / "phase7_proto_speech.wav"
    concat_cmd = ["ffmpeg", "-y"]
    filter_inputs = []
    for i, p in enumerate(scene_audio_paths):
        concat_cmd.extend(["-i", str(p)])
        filter_inputs.append(f"[{i}:a]")
    filter_complex = f"{''.join(filter_inputs)}concat=n={len(scene_audio_paths)}:v=0:a=1[aout]"
    concat_cmd.extend(["-filter_complex", filter_complex, "-map", "[aout]", "-ar", "48000", str(concat_speech_wav)])
    subprocess.run(concat_cmd, capture_output=True, check=True)

    final_master_wav = audio_dir / "phase7_proto_master_audio.wav"
    sound_designer = ReferenceSoundDesigner()
    out_soundtrack, audio_meta = sound_designer.assemble_reference_soundtrack(
        narration_wav=concat_speech_wav,
        scene_durations=scene_durations,
        output_wav=final_master_wav,
    )
    print(f"  ✓ Master Audio generated: {final_master_wav.name} (Integrated: {audio_meta.get('integrated_lufs', -16.0)} LUFS)")

    # 5. Assemble Clean Master and Captioned Master
    print("\n[4/6] Assembling Clean Master and Captioned Master...")
    clean_prototype_mp4 = out_base / "phase7_visual_prototype_clean.mp4"
    captioned_prototype_mp4 = out_base / "phase7_visual_prototype.mp4"
    ass_subs_path = out_base / "phase7_prototype.ass"

    # Concatenate visual stems into clean video
    concat_list_file = out_base / "concat_list.txt"
    with open(concat_list_file, "w") as f:
        for s in stem_video_paths:
            f.write(f"file '{s.resolve().as_posix()}'\n")

    mux_clean_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list_file),
        "-i", str(final_master_wav),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(clean_prototype_mp4)
    ]
    subprocess.run(mux_clean_cmd, capture_output=True, check=True)
    print(f"  ✓ Clean Prototype MP4: {clean_prototype_mp4.name} ({clean_prototype_mp4.stat().st_size:,} bytes)")

    # Generate ASS Subtitles with Safe Bottom Margin 360 px
    with open(ass_subs_path, "w", encoding="utf-8") as f:
        f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n")
        f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: ExplainerLight,Arial,48,&H000F172A,&H000000FF,&H00FFFFFF,&H80FFFFFF,-1,0,0,0,100,100,0,0,1,3,1,2,60,60,360,1\n\n")
        f.write("[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

        curr_t = 0.0
        for sc in prototype_scenes:
            dur = sc["actual_duration"]
            start_str = f"{int(curr_t // 3600):01d}:{int((curr_t % 3600) // 60):02d}:{int(curr_t % 60):02d}.{int((curr_t * 100) % 100):02d}"
            end_t = curr_t + dur
            end_str = f"{int(end_t // 3600):01d}:{int((end_t % 3600) // 60):02d}:{int(end_t % 60):02d}.{int((end_t * 100) % 100):02d}"
            text = sc["narration"].replace("'", "\\'")
            f.write(f"Dialogue: 0,{start_str},{end_str},ExplainerLight,,0,0,360,,{text}\n")
            curr_t = end_t

    # Burn subtitles into final review master
    escaped_ass = str(ass_subs_path).replace("\\", "/").replace(":", "\\:")
    burn_cmd = [
        "ffmpeg", "-y",
        "-i", str(clean_prototype_mp4),
        "-vf", f"subtitles='{escaped_ass}'",
        "-c:v", "libx264", "-profile:v", "high", "-b:v", "4500k", "-maxrate", "6000k", "-bufsize", "8000k",
        "-c:a", "copy",
        str(captioned_prototype_mp4)
    ]
    subprocess.run(burn_cmd, capture_output=True, check=True)
    print(f"  ✓ Captioned Prototype MP4: {captioned_prototype_mp4.name} ({captioned_prototype_mp4.stat().st_size:,} bytes)")

    # 6. Contact Sheet & Comprehensive Visual Frame Extraction
    print("\n[5/6] Extracting Forensic Inspection Frames & 25-Frame Contact Sheet...")
    contact_sheet_path = out_base / "phase7_prototype_contact_sheet.png"
    generate_25frame_contact_sheet(
        video_path=captioned_prototype_mp4,
        output_path=contact_sheet_path,
        title="BitNet b1.58 Physical Explainer Prototype",
    )
    print(f"  ✓ Contact sheet saved: {contact_sheet_path.name}")

    # Copy contact sheet to Brain Artifacts directory
    brain_dir = Path("C:/Users/bavik/.gemini/antigravity/brain/174164e7-7384-4da6-a377-b063df7a125d")
    brain_sheet = brain_dir / "phase7_prototype_contact_sheet.png"
    if brain_dir.exists():
        import shutil
        shutil.copy2(contact_sheet_path, brain_sheet)
        print(f"  ✓ Copied contact sheet to Brain Artifacts directory: {brain_sheet.name}")

    # Extract 30 evenly distributed inspection frames for Step 2
    print("  -> Extracting 30 evenly distributed inspection frames...")
    frames_sub = inspection_dir / "extracted_30_frames"
    frames_sub.mkdir(parents=True, exist_ok=True)
    for i in range(30):
        t_sample = total_duration * (i + 0.5) / 30.0
        frame_out = frames_sub / f"frame_{i:02d}_{t_sample:.2f}s.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{t_sample:.3f}",
            "-i", str(captioned_prototype_mp4),
            "-vframes", "1",
            str(frame_out)
        ], capture_output=True, check=True)

    # Extract scene boundary and transition frames
    print("  -> Extracting scene keyframes (start, mid, end)...")
    curr_time = 0.0
    for idx, sc in enumerate(prototype_scenes):
        dur = sc["actual_duration"]
        for label, rel_t in [("start", 0.3), ("mid", dur * 0.5), ("end", dur - 0.3)]:
            abs_t = curr_time + rel_t
            kf_path = inspection_dir / f"{sc['id']}_{label}.png"
            subprocess.run([
                "ffmpeg", "-y", "-ss", f"{abs_t:.3f}",
                "-i", str(captioned_prototype_mp4),
                "-vframes", "1",
                str(kf_path)
            ], capture_output=True, check=True)
        curr_time += dur

    # 7. Quality Metrics Summary & Manifest
    print("\n[6/6] Writing Prototype Manifest...")
    clean_sha = compute_sha256(clean_prototype_mp4)
    captioned_sha = compute_sha256(captioned_prototype_mp4)
    audio_sha = compute_sha256(final_master_wav)
    contact_sha = compute_sha256(contact_sheet_path)

    manifest = {
        "prototype_title": "Phase 7.1 Visual Proof-of-Style Prototype",
        "topic": "BitNet b1.58: The 1-Bit LLM Revolution",
        "duration_seconds": total_duration,
        "resolution": "1080x1920",
        "fps": 30.0,
        "codec": "H.264 High Profile",
        "audio_loudness_lufs": audio_meta.get("integrated_lufs", -16.0),
        "audio_true_peak_dbtp": audio_meta.get("true_peak_dbtp", -1.0),
        "scenes": [
            {"id": sc["id"], "name": sc["name"], "duration": sc["actual_duration"]}
            for sc in prototype_scenes
        ],
        "outputs": {
            "prototype_clean_mp4": {
                "path": str(clean_prototype_mp4),
                "bytes": clean_prototype_mp4.stat().st_size,
                "sha256": clean_sha
            },
            "prototype_captioned_mp4": {
                "path": str(captioned_prototype_mp4),
                "bytes": captioned_prototype_mp4.stat().st_size,
                "sha256": captioned_sha
            },
            "contact_sheet": {
                "path": str(contact_sheet_path),
                "bytes": contact_sheet_path.stat().st_size,
                "sha256": contact_sha
            },
            "master_audio": {
                "path": str(final_master_wav),
                "bytes": final_master_wav.stat().st_size,
                "sha256": audio_sha
            },
            "subtitles_ass": {
                "path": str(ass_subs_path),
                "bytes": ass_subs_path.stat().st_size,
                "sha256": compute_sha256(ass_subs_path)
            }
        }
    }

    manifest_path = out_base / "phase7_prototype_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"  ✓ Prototype Manifest saved: {manifest_path.name}")

    return manifest


if __name__ == "__main__":
    t_start = time.time()
    manifest = run_prototype_production()
    print(f"\n[DONE] Prototype finished in {time.time() - t_start:.2f}s!")
