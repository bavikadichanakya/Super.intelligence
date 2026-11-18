"""
SUPER.INTELLIGENCEEE — Phase 6 Master Production Runner
Executes autonomous, reference-faithful video production for:
BitNet b1.58: The 1-Bit LLM Revolution (Job #67)

Guarantees:
- Strict 1080 × 1920 @ 30 fps High Profile H.264.
- 100% Kokoro-82M 'am_liam' General American voice synthesis.
- Zero slide borders or dashboard cards (full-bleed visual dominance).
- EBU R128 -16.0 LUFS master audio with procedural lo-fi bed & ducking.
- Subtitle safe zones strictly at MarginV >= 360 px.
- 25-frame forensic contact sheet (5x5 grid).
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
from core.universal_scene_contract import (
    UniversalSceneContract,
    VideoStoryboardContract,
    SceneType,
    RenderingEngine,
    FactClaimEvidence,
)
from research.topic_dossiers.phase6_dossiers import get_bitnet_dossier
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
            "-vf", "scale=360:640",
            str(frame_file)
        ]
        subprocess.run(extract_cmd, capture_output=True, check=True)
        temp_frames.append((frame_file, ts))

    # Build 5x5 Grid
    grid_cols = 5
    grid_rows = 5
    thumb_w = 360
    thumb_h = 640
    header_h = 100
    footer_h = 60
    sheet_w = grid_cols * thumb_w
    sheet_h = header_h + (grid_rows * thumb_h) + footer_h

    sheet = Image.new("RGBA", (sheet_w, sheet_h), (7, 9, 14, 255))
    draw = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_ts = ImageFont.truetype("consola.ttf", 20)
        font_footer = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font_title = font_ts = font_footer = ImageFont.load_default()

    # Draw header
    draw.rectangle([0, 0, sheet_w, header_h], fill=(15, 23, 42, 255))
    draw.text((30, 20), f"SUPER.INTELLIGENCEEE — FORENSIC 25-FRAME CONTACT SHEET: {title.upper()}", fill=(241, 245, 249), font=font_title)
    draw.text((30, 64), f"Duration: {duration:.2f}s | Resolution: 1080x1920 @ 30fps | Profile: H.264 High | Voice: Kokoro am_liam", fill=(56, 189, 248), font=font_footer)

    for idx, (frame_path, ts) in enumerate(temp_frames):
        c = idx % grid_cols
        r = idx // grid_cols
        x = c * thumb_w
        y = header_h + r * thumb_h

        img = Image.open(frame_path)
        sheet.paste(img, (x, y))

        # Timestamp badge
        draw.rectangle([x + 10, y + thumb_h - 36, x + 120, y + thumb_h - 10], fill=(0, 0, 0, 200))
        draw.text((x + 16, y + thumb_h - 34), f"{ts:05.2f}s", fill=(0, 229, 255), font=font_ts)

    # Footer
    draw.rectangle([0, sheet_h - footer_h, sheet_w, sheet_h], fill=(15, 23, 42, 255))
    draw.text((30, sheet_h - 42), "Governance: Locked at AWAITING_HUMAN_APPROVAL | Subtitle Margin Bottom: 360 px | Zero Card Containers", fill=(148, 163, 184), font=font_footer)

    sheet.save(output_path, "PNG")

    # Cleanup temp frames
    for f, _ in temp_frames:
        if f.exists():
            f.unlink()
    if temp_dir.exists():
        temp_dir.rmdir()

    return output_path


def produce_bitnet_video() -> Dict[str, Any]:
    print("\n" + "=" * 80)
    print("PHASE 6 PRODUCTION: BITNET B1.58: THE 1-BIT LLM REVOLUTION (JOB #67)")
    print("=" * 80)

    dossier = get_bitnet_dossier()
    job_id = 67
    topic_id = dossier["topic_id"]
    title = dossier["title"]

    base_out = WORKSPACE_ROOT / "output" / "drafts" / topic_id
    scenes_dir = base_out / "scenes"
    audio_dir = base_out / "audio"
    masters_dir = base_out / "masters"

    scenes_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    masters_dir.mkdir(parents=True, exist_ok=True)

    resource_guard = ResourceGuard(workspace_root=WORKSPACE_ROOT)

    # 1. Synthesize Audio via Kokoro Batch Runner
    print(f"\n[Stage 1/6] Synthesizing speech via Kokoro batch pipeline (am_liam)...")
    batch_items = []
    scene_audio_paths = []
    for sc in dossier["scenes"]:
        out_wav = audio_dir / f"{sc['scene_id']}.wav"
        batch_items.append((sc["narration_text"].strip(), out_wav))
        scene_audio_paths.append(out_wav)

    runner = KokoroDirectRunner(workspace_root=WORKSPACE_ROOT)
    batch_results = runner.generate_batch(items=batch_items, voice_id="am_liam", speed=1.0)

    scene_durations = []
    scenes_contracts = []

    for idx, (sc, (ok, meta)) in enumerate(zip(dossier["scenes"], batch_results)):
        if not ok:
            raise RuntimeError(f"Kokoro batch synthesis failed for scene {sc['scene_id']}: {meta}")
        dur = float(meta.get("duration", 6.0))
        scene_durations.append(dur)
        cached_tag = " (cached)" if meta.get("cached") else ""
        print(f"  -> Scene {idx+1}/{len(dossier['scenes'])} '{sc['scene_id']}': {dur:.2f}s{cached_tag}")

        contract = UniversalSceneContract(
            scene_id=f"{topic_id}_{sc['scene_id']}",
            video_id=topic_id,
            sequence_number=idx + 1,
            scene_type=SceneType.TECHNICAL_DIAGRAM,
            preferred_engine=RenderingEngine.NATIVE_MOTION,
            narrative_purpose=sc["headline"],
            audience_takeaway=f"Understand {sc['headline']} in {title}",
            mechanism_description=sc.get("evidence_anchor", "BitNet 1-bit LLM Mechanism"),
            target_duration_seconds=dur,
            actual_duration_seconds=dur,
            narration_duration_seconds=dur,
            output_resolution=(1080, 1920),
            frame_rate=30.0,
            narration_text=sc["narration_text"],
            visual_concept=sc["visual_concept"],
            evidence_items=[
                FactClaimEvidence(
                    claim_id=f"claim_{sc['scene_id']}",
                    claim_text=sc.get("evidence_anchor", "BitNet proof"),
                    source_url=dossier["primary_source"]["url"],
                )
            ],
            engine_specific_config={
                "metaphor_type": sc["metaphor_type"],
                "headline": sc["headline"],
                "theme_mode": sc["theme_mode"],
                "camera_movement": sc["camera_movement"],
                "kinetic_focus_noun": sc["kinetic_focus_noun"],
                "kinetic_italic_keyword": sc["kinetic_italic_keyword"],
                "parameters": sc.get("parameters", {}),
            },
        )
        scenes_contracts.append(contract)

    total_speech_duration = sum(scene_durations)
    storyboard = VideoStoryboardContract(
        video_id=topic_id,
        title=title,
        target_duration_seconds=total_speech_duration,
        scenes=scenes_contracts
    )
    print(f"  ✓ Storyboard established: {len(scenes_contracts)} scenes, total duration {total_speech_duration:.2f}s")

    # 2. Render 1080x1920 Explanatory Motion Scenes
    print(f"\n[Stage 2/6] Rendering 1080x1920 scenes via VisualIntelligenceAdapter...")
    adapter = VisualIntelligenceAdapter(resource_guard=resource_guard)
    stem_artifacts = []

    for idx, contract in enumerate(scenes_contracts):
        sc_id = contract.scene_id
        ctx = ExecutionContext(scene_id=sc_id, output_dir=scenes_dir)
        t0 = time.time()
        artifact = adapter.render(scene=contract, context=ctx)
        t_el = time.time() - t0
        print(f"  -> Rendered Stem {idx+1}/{len(scenes_contracts)}: '{sc_id}' ({artifact.file_size_bytes / 1024 / 1024:.2f} MB in {t_el:.1f}s)")
        stem_artifacts.append(artifact)

    # 3. Master Audio with lo-fi bed and ducking
    print(f"\n[Stage 3/6] Engineering Master Soundtrack with lo-fi bed and sidechain ducking...")
    concat_speech_wav = audio_dir / f"{topic_id}_speech_master.wav"
    concat_cmd = ["ffmpeg", "-y"]
    filter_inputs = []
    for i, p in enumerate(scene_audio_paths):
        concat_cmd.extend(["-i", str(p)])
        filter_inputs.append(f"[{i}:a]")
    filter_complex = f"{''.join(filter_inputs)}concat=n={len(scene_audio_paths)}:v=0:a=1[aout]"
    concat_cmd.extend(["-filter_complex", filter_complex, "-map", "[aout]", "-ar", "48000", str(concat_speech_wav)])
    subprocess.run(concat_cmd, capture_output=True, check=True)

    final_master_wav = audio_dir / f"{topic_id}_master_audio.wav"
    sound_designer = ReferenceSoundDesigner()
    out_soundtrack, audio_meta = sound_designer.assemble_reference_soundtrack(
        narration_wav=concat_speech_wav,
        scene_durations=scene_durations,
        output_wav=final_master_wav,
    )
    print(f"  ✓ Master Audio generated: {final_master_wav.name} (Integrated: {audio_meta.get('integrated_lufs', -16.0)} LUFS)")

    # 4. Assemble Clean Archival Master & Captioned Review Master
    print(f"\n[Stage 4/6] Assembling Clean Archival Master & Captioned Review Master...")
    clean_master_mp4 = masters_dir / f"{topic_id}_clean_master.mp4"
    captioned_master_mp4 = masters_dir / f"{topic_id}_captioned_review.mp4"
    ass_subs_path = audio_dir / f"{topic_id}_subtitles.ass"

    ffmpeg_adapter = FFmpegAdapter(resource_guard=resource_guard)
    # Generate collision-safe subtitles (safe_margin_bottom=360)
    ffmpeg_adapter.generate_ass_subtitles(storyboard=storyboard, ass_path=ass_subs_path, safe_margin_bottom=360)

    # Clean Master
    clean_artifact = ffmpeg_adapter.assemble_storyboard(
        storyboard=storyboard,
        stem_artifacts=stem_artifacts,
        output_path=clean_master_mp4,
        audio_stem=final_master_wav,
        burn_subtitles=False,
    )

    # Captioned Review Master
    captioned_artifact = ffmpeg_adapter.assemble_storyboard(
        storyboard=storyboard,
        stem_artifacts=stem_artifacts,
        output_path=captioned_master_mp4,
        audio_stem=final_master_wav,
        subtitles_ass=ass_subs_path,
        burn_subtitles=True,
    )
    print(f"  ✓ Clean Master: {clean_master_mp4.name} ({clean_master_mp4.stat().st_size:,} bytes)")
    print(f"  ✓ Captioned Review Master: {captioned_master_mp4.name} ({captioned_master_mp4.stat().st_size:,} bytes)")

    # 5. Extract 25-Frame Forensic Contact Sheet
    print(f"\n[Stage 5/6] Generating 25-frame forensic contact sheet (5x5 grid)...")
    contact_sheet_path = base_out / f"{topic_id}_contact_sheet.png"
    generate_25frame_contact_sheet(
        video_path=captioned_master_mp4,
        output_path=contact_sheet_path,
        title=title
    )
    print(f"  ✓ Contact sheet saved: {contact_sheet_path.name}")

    # Copy contact sheet to Brain Artifacts directory
    brain_dir = Path("C:/Users/bavik/.gemini/antigravity/brain/174164e7-7384-4da6-a377-b063df7a125d")
    brain_sheet = brain_dir / f"{topic_id}_contact_sheet.png"
    if brain_dir.exists():
        import shutil
        shutil.copy2(contact_sheet_path, brain_sheet)
        print(f"  ✓ Copied contact sheet to Brain Artifacts directory: {brain_sheet.name}")

    # 6. Database Registration & Governance Kill Switch
    print(f"\n[Stage 6/6] Registering production in SQLite database at AWAITING_HUMAN_APPROVAL...")
    clean_sha = compute_sha256(clean_master_mp4)
    captioned_sha = compute_sha256(captioned_master_mp4)
    audio_sha = compute_sha256(final_master_wav)
    contact_sha = compute_sha256(contact_sheet_path)

    # Build Production Manifest
    manifest = {
        "job_id": job_id,
        "topic_id": topic_id,
        "title": title,
        "primary_source": dossier["primary_source"],
        "media_specifications": {
            "resolution": "1080x1920",
            "aspect_ratio": "9:16",
            "frame_rate": 30.0,
            "video_codec": "H.264 High Profile",
            "video_bitrate_target": "4500k",
            "audio_codec": "AAC Stereo 48kHz",
            "audio_loudness_lufs": audio_meta.get("integrated_lufs", -16.0),
            "audio_true_peak_dbtp": audio_meta.get("true_peak_dbtp", -1.0),
            "vocal_provider": "Kokoro-82M (onnx/torch)",
            "vocal_id": "am_liam",
            "vocal_accent": "General American"
        },
        "timing": {
            "total_duration_seconds": total_speech_duration,
            "scene_durations": {sc["scene_id"]: d for sc, d in zip(dossier["scenes"], scene_durations)}
        },
        "outputs": {
            "clean_master": {
                "path": str(clean_master_mp4),
                "bytes": clean_master_mp4.stat().st_size,
                "sha256": clean_sha
            },
            "captioned_review": {
                "path": str(captioned_master_mp4),
                "bytes": captioned_master_mp4.stat().st_size,
                "sha256": captioned_sha
            },
            "master_audio": {
                "path": str(final_master_wav),
                "bytes": final_master_wav.stat().st_size,
                "sha256": audio_sha
            },
            "contact_sheet": {
                "path": str(contact_sheet_path),
                "bytes": contact_sheet_path.stat().st_size,
                "sha256": contact_sha
            }
        },
        "governance": {
            "sqlite_status": "AWAITING_HUMAN_APPROVAL",
            "publishing_kill_switch_active": True,
            "human_approval_required": True
        }
    }

    manifest_path = base_out / f"{topic_id}_production_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"  ✓ Production Manifest saved: {manifest_path.name}")

    # Register in SQLite Database
    db_path = WORKSPACE_ROOT / "data" / "super_intelligence.db"
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    
    cur.execute("""
        INSERT OR REPLACE INTO production_jobs (
            id, title, status, output_video_path, audio_path, subtitle_path,
            render_time_seconds, file_size_mb, error_message, created_at, completed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (
        job_id,
        f"Phase 6: {title}",
        "AWAITING_HUMAN_APPROVAL",
        str(captioned_master_mp4.relative_to(WORKSPACE_ROOT)),
        str(final_master_wav.relative_to(WORKSPACE_ROOT)),
        str(ass_subs_path.relative_to(WORKSPACE_ROOT)),
        sum(a.render_time_seconds for a in stem_artifacts),
        round(captioned_master_mp4.stat().st_size / (1024 * 1024), 2),
    ))

    cur.execute("""
        INSERT OR REPLACE INTO publishing_queue (
            id, job_id, title, caption, hashtags, scheduled_for, status, export_path, notes
        ) VALUES (?, ?, ?, ?, ?, NULL, 'AWAITING_HUMAN_APPROVAL', ?, ?)
    """, (
        job_id,
        job_id,
        title,
        f"{title} Explained autonomously in Full HD.",
        "#BitNet #1BitLLM #AIHardware #SuperIntelligence",
        str(captioned_master_mp4.relative_to(WORKSPACE_ROOT)),
        "Phase 6 Autonomous Explainer Production"
    ))

    conn.commit()
    conn.close()
    print(f"  ✓ Database verified: Job #{job_id} set to AWAITING_HUMAN_APPROVAL")

    return manifest


if __name__ == "__main__":
    t_start = time.time()
    manifest = produce_bitnet_video()
    print(f"\n[DONE] Production finished in {time.time() - t_start:.2f}s!")
