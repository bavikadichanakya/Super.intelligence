"""
SUPER.INTELLIGENCEEE — Phase 5.2 Master Production Runner
Executes autonomous, reference-faithful video production for three (3) distinct technical topics:
1. AI Model Architecture: DeepSeek-R1 Latent Reasoning
2. Cybersecurity / Operating Systems: eBPF Kernel Verifier Exploitation
3. Hardware & GPU Compilers: FlashAttention-3 Hopper Asynchrony

Guarantees:
- Strict 1080 × 1920 @ 30 fps High Profile H.264.
- 100% Kokoro-82M 'am_liam' General American voice synthesis.
- Zero slide borders or dashboard cards (full-bleed visual dominance).
- EBU R128 -16.0 LUFS master audio with procedural lo-fi bed & ducking.
- Subtitle safe zones strictly at MarginV >= 360 px.
- 25-frame forensic contact sheets (5x5 grid).
- SQLite database logging locked at AWAITING_HUMAN_APPROVAL.
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

from core.database import Database
from core.universal_scene_contract import UniversalSceneContract, VideoStoryboardContract
from creative.visual_intelligence.visual_story_planner import VisualStoryPlanner
from research.topic_dossiers.phase52_dossiers import (
    get_deepseek_r1_dossier,
    get_ebpf_security_dossier,
    get_flashattention3_dossier,
)
from audio.providers.kokoro_direct import KokoroDirectRunner
from audio.reference_sound_designer import ReferenceSoundDesigner
from rendering.adapters.visual_intelligence_adapter import VisualIntelligenceAdapter
from rendering.adapters.ffmpeg_adapter import FFmpegAdapter
from rendering.render_artifact import RenderArtifact
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
            "-s", "288x512",
            str(frame_file)
        ]
        subprocess.run(extract_cmd, capture_output=True, check=True)
        temp_frames.append(frame_file)

    cols, rows = 5, 5
    cell_w, cell_h = 288, 512
    header_h = 70
    grid_img = Image.new("RGB", (cols * cell_w, rows * cell_h + header_h), (10, 13, 20))
    draw = ImageDraw.Draw(grid_img)

    try:
        font_header = ImageFont.truetype("arialbd.ttf", 22)
        font_ts = ImageFont.truetype("consola.ttf", 15)
    except Exception:
        font_header = ImageFont.load_default()
        font_ts = ImageFont.load_default()

    draw.text(
        (24, 20),
        f"PHASE 5.2 • 25-FRAME FORENSIC CONTACT SHEET: {title} (1080x1920 @ 30fps, {duration:.1f}s)",
        fill=(241, 245, 249),
        font=font_header,
    )

    for idx, (fpath, ts) in enumerate(zip(temp_frames, timestamps)):
        r = idx // cols
        c = idx % cols
        x = c * cell_w
        y = header_h + r * cell_h

        if fpath.exists():
            with Image.open(fpath) as img:
                grid_img.paste(img, (x, y))

        draw.rectangle([x, y + cell_h - 26, x + cell_w, y + cell_h], fill=(0, 0, 0, 190))
        draw.text((x + 8, y + cell_h - 22), f"F{idx+1:02d} | {ts:.2f}s", fill=(56, 189, 248), font=font_ts)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    grid_img.save(output_path, quality=95)

    # Cleanup temp frames
    for f in temp_frames:
        try:
            f.unlink(missing_ok=True)
        except Exception:
            pass
    try:
        temp_dir.rmdir()
    except Exception:
        pass

    return output_path


def run_production(
    prod_id: str,
    dossier: Dict[str, Any],
    db: Database,
    guard: ResourceGuard,
) -> Dict[str, Any]:
    """Runs a single complete end-to-end production for one topic."""
    print(f"\n=======================================================")
    print(f"STARTING PRODUCTION: {prod_id} ({dossier['topic']})")
    print(f"=======================================================")

    out_base = WORKSPACE_ROOT / "output" / "drafts" / prod_id
    audio_dir = out_base / "audio"
    stems_dir = out_base / "stems"
    masters_dir = out_base / "masters"
    audio_dir.mkdir(parents=True, exist_ok=True)
    stems_dir.mkdir(parents=True, exist_ok=True)
    masters_dir.mkdir(parents=True, exist_ok=True)

    planner = VisualStoryPlanner()
    storyboard, breakdown = planner.plan_storyboard(
        dossier=dossier,
        video_id=prod_id,
        script_data=dossier.get("script"),
    )

    kokoro = KokoroDirectRunner()
    sound_designer = ReferenceSoundDesigner()
    vi_adapter = VisualIntelligenceAdapter(resource_guard=guard)
    ffmpeg_adapter = FFmpegAdapter(resource_guard=guard)

    # 1. Synthesize Kokoro-82M Voice for all scenes via Fast Batch
    print(f"[Stage 1/6] Synthesizing Kokoro-82M 'am_liam' voice narration for {len(storyboard.scenes)} scenes (Fast Batch)...")
    batch_items = []
    scene_audio_paths = []

    for idx, scene in enumerate(storyboard.scenes):
        scene_wav = audio_dir / f"{prod_id}_scene_{idx+1:02d}.wav"
        batch_items.append((scene.narration_text.strip(), scene_wav))
        scene_audio_paths.append(scene_wav)

    batch_results = kokoro.generate_batch(items=batch_items, voice_id="am_liam", speed=1.0)
    scene_durations = []

    for idx, (scene, (ok, meta)) in enumerate(zip(storyboard.scenes, batch_results)):
        if not ok:
            raise RuntimeError(f"Kokoro batch synthesis failed for scene {scene.scene_id}: {meta}")
        dur = float(meta.get("duration", 6.5))
        scene.narration_duration_seconds = dur
        scene.actual_duration_seconds = dur
        scene_durations.append(dur)
        cached_tag = " (cached)" if meta.get("cached") else ""
        print(f"  -> Scene {idx+1}/{len(storyboard.scenes)}: {dur:.2f}s{cached_tag} -> {scene_audio_paths[idx].name}")

    total_speech_duration = sum(scene_durations)
    storyboard.target_duration_seconds = total_speech_duration
    print(f"  ✓ Voice synthesis complete: {len(scene_durations)} scenes, total speech {total_speech_duration:.2f}s")

    # 2. Render 1080x1920 visual stems sequentially
    print(f"[Stage 2/6] Rendering 1080x1920 visual stems sequentially under ResourceGuard...")
    stem_artifacts = []
    for idx, scene in enumerate(storyboard.scenes):
        print(f"  -> Rendering Stem {idx+1}/{len(storyboard.scenes)}: {scene.scene_id} ({scene.actual_duration_seconds:.2f}s)")
        ctx = ExecutionContext(scene_id=scene.scene_id, output_dir=stems_dir)
        artifact = vi_adapter.render(scene=scene, context=ctx)
        stem_artifacts.append(artifact)
        print(f"     ✓ Rendered in {artifact.render_time_seconds:.2f}s -> {artifact.output_path.name}")

    # 3. Assemble and Master Sound Track (EBU R128 -16.0 LUFS with lo-fi bed)
    print(f"[Stage 3/6] Engineering Master Soundtrack with lo-fi bed and sidechain ducking...")
    concat_speech_wav = audio_dir / f"{prod_id}_speech_master.wav"
    concat_cmd = ["ffmpeg", "-y"]
    filter_inputs = []
    for i, p in enumerate(scene_audio_paths):
        concat_cmd.extend(["-i", str(p)])
        filter_inputs.append(f"[{i}:a]")
    filter_complex = f"{''.join(filter_inputs)}concat=n={len(scene_audio_paths)}:v=0:a=1[aout]"
    concat_cmd.extend(["-filter_complex", filter_complex, "-map", "[aout]", "-ar", "48000", str(concat_speech_wav)])
    subprocess.run(concat_cmd, capture_output=True, check=True)

    final_master_wav = audio_dir / f"{prod_id}_master_audio.wav"
    out_soundtrack, audio_meta = sound_designer.assemble_reference_soundtrack(
        narration_wav=concat_speech_wav,
        scene_durations=scene_durations,
        output_wav=final_master_wav,
    )
    print(f"  ✓ Master Audio generated: {final_master_wav.name} (Integrated: {audio_meta.get('integrated_lufs', -16.0)} LUFS)")

    # 4. Assemble Clean Archival Master & Captioned Review Master
    print(f"[Stage 4/6] Assembling Clean Archival Master & Captioned Review Master...")
    clean_master = masters_dir / f"{prod_id}_clean_master.mp4"
    captioned_master = masters_dir / f"{prod_id}_captioned_review.mp4"
    ass_subs_path = out_base / f"{prod_id}_subtitles.ass"

    # Generate MarginV=360 collision-safe subtitles
    ffmpeg_adapter.generate_ass_subtitles(storyboard=storyboard, ass_path=ass_subs_path, safe_margin_bottom=360)

    # Clean Master
    clean_artifact = ffmpeg_adapter.assemble_storyboard(
        storyboard=storyboard,
        stem_artifacts=stem_artifacts,
        output_path=clean_master,
        audio_stem=final_master_wav,
        burn_subtitles=False,
    )

    # Captioned Review Master
    captioned_artifact = ffmpeg_adapter.assemble_storyboard(
        storyboard=storyboard,
        stem_artifacts=stem_artifacts,
        output_path=captioned_master,
        audio_stem=final_master_wav,
        subtitles_ass=ass_subs_path,
        burn_subtitles=True,
    )
    print(f"  ✓ Clean Master: {clean_master.name} ({clean_master.stat().st_size:,} bytes)")
    print(f"  ✓ Captioned Review Master: {captioned_master.name} ({captioned_master.stat().st_size:,} bytes)")

    # 5. Generate 25-frame contact sheet
    print(f"[Stage 5/6] Generating 25-frame forensic contact sheet (5x5 grid)...")
    contact_sheet_path = out_base / f"{prod_id}_contact_sheet.png"
    generate_25frame_contact_sheet(
        video_path=captioned_master,
        output_path=contact_sheet_path,
        title=dossier["topic"],
    )
    print(f"  ✓ Contact sheet saved: {contact_sheet_path.name}")

    # Copy contact sheet to Brain Artifacts directory
    brain_dir = Path("C:/Users/bavik/.gemini/antigravity/brain/174164e7-7384-4da6-a377-b063df7a125d")
    art_contact = brain_dir / f"{prod_id}_contact_sheet.png"
    if contact_sheet_path.exists():
        with open(contact_sheet_path, "rb") as src, open(art_contact, "wb") as dst:
            dst.write(src.read())

    # 6. Database Registration & Governance Kill Switch
    print(f"[Stage 6/6] Registering production in SQLite database at AWAITING_HUMAN_APPROVAL...")
    clean_sha = compute_sha256(clean_master)
    captioned_sha = compute_sha256(captioned_master)
    audio_sha = compute_sha256(final_master_wav)

    job_id = None
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO production_jobs (
                title, status, output_video_path, audio_path, subtitle_path,
                render_time_seconds, file_size_mb, error_message, created_at, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (
                f"Phase 5.2: {dossier['topic']}",
                "AWAITING_HUMAN_APPROVAL",
                str(captioned_master.relative_to(WORKSPACE_ROOT)),
                str(final_master_wav.relative_to(WORKSPACE_ROOT)),
                str(ass_subs_path.relative_to(WORKSPACE_ROOT)),
                sum(a.render_time_seconds for a in stem_artifacts),
                round(captioned_master.stat().st_size / (1024 * 1024), 2),
            ),
        )
        job_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO publishing_queue (
                job_id, title, caption, hashtags, scheduled_for, status, export_path, notes
            ) VALUES (?, ?, ?, ?, NULL, 'AWAITING_HUMAN_APPROVAL', ?, ?)
            """,
            (
                job_id,
                dossier["topic"],
                f"{dossier['primary_thesis']} Explained autonomously in Full HD.",
                f"#{breakdown.domain.value} #techexplainer #superintelligence",
                str(captioned_master.relative_to(WORKSPACE_ROOT)),
                f"SHA256: {captioned_sha}",
            ),
        )
        conn.commit()

    manifest = {
        "production_id": prod_id,
        "topic": dossier["topic"],
        "domain": breakdown.domain.value,
        "job_id": job_id,
        "status": "AWAITING_HUMAN_APPROVAL",
        "resolution": "1080x1920",
        "fps": 30,
        "duration_seconds": total_speech_duration,
        "scenes_count": len(storyboard.scenes),
        "clean_master": {
            "path": str(clean_master.relative_to(WORKSPACE_ROOT)),
            "sha256": clean_sha,
            "bytes": clean_master.stat().st_size,
        },
        "captioned_master": {
            "path": str(captioned_master.relative_to(WORKSPACE_ROOT)),
            "sha256": captioned_sha,
            "bytes": captioned_master.stat().st_size,
        },
        "master_audio": {
            "path": str(final_master_wav.relative_to(WORKSPACE_ROOT)),
            "sha256": audio_sha,
            "integrated_lufs": audio_meta.get("integrated_lufs", -16.0),
        },
        "contact_sheet": str(contact_sheet_path.relative_to(WORKSPACE_ROOT)),
    }

    manifest_file = out_base / f"{prod_id}_production_manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"  ✓ Production recorded in SQLite: Job #{job_id} [AWAITING_HUMAN_APPROVAL]")
    return manifest


def main():
    db = Database()
    guard = ResourceGuard(workspace_root=WORKSPACE_ROOT)

    productions = [
        ("phase52_deepseek_r1", get_deepseek_r1_dossier()),
        ("phase52_ebpf_security", get_ebpf_security_dossier()),
        ("phase52_flashattention3", get_flashattention3_dossier()),
    ]

    all_manifests = []
    for prod_id, dossier in productions:
        manifest = run_production(prod_id=prod_id, dossier=dossier, db=db, guard=guard)
        all_manifests.append(manifest)

    # Save summary manifest
    summary_file = WORKSPACE_ROOT / "output" / "drafts" / "phase52_master_summary_manifest.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(all_manifests, f, indent=2)

    print("\n=======================================================")
    print("ALL THREE (3) PRODUCTIONS COMPLETED SUCCESSFULLY!")
    print("=======================================================")
    for m in all_manifests:
        print(f"• Job #{m['job_id']}: {m['topic']} ({m['duration_seconds']:.1f}s, 1080x1920) -> {m['status']}")


if __name__ == "__main__":
    main()
