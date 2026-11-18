"""
SUPER.INTELLIGENCEEE — Phase 8 Flagship Documentary Production Script
Topic: Google Willow: The Breakthrough That Solved Quantum Error Correction
Reference Creative Authority: This is what i want.mp4

Produces:
1. Clean Master MP4 (1080x1920 @ 30fps High Profile)
2. Captioned Review Master MP4 (MarginV=360 Safe Zone)
3. 25-Frame Forensic Contact Sheet (Copied to Brain Artifacts)
4. 30 Evenly Distributed Frame Extractions
5. Production Manifest with SHA-256 Hashes
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
from rendering.physical_explainer_engine import (
    Scene1CryostatHookComposition,
    Scene2SurfaceCodeLatticeComposition,
    Scene3ErrorHealingPlaquetteComposition,
    Scene4BelowThresholdCurveComposition,
    Scene5SupercomputerComparisonComposition,
    Scene6LoopConclusionComposition,
)

OUTPUT_DIR = WORKSPACE_ROOT / "output" / "productions" / "phase8_willow_quantum"
REPORTS_DIR = WORKSPACE_ROOT / "reports" / "phase8_inspection"
BRAIN_ARTIFACTS_DIR = Path(r"C:\Users\bavik\.gemini\antigravity\brain\174164e7-7384-4da6-a377-b063df7a125d")


def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def render_composition_to_mp4(comp, output_mp4: Path, fps: float = 30.0) -> None:
    """Renders composition frames directly into FFmpeg stdin with deadlock-free 10MB pipe."""
    total_frames = int(comp.duration * fps)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{comp.width}x{comp.height}",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level", "4.2",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18",
        str(output_mp4),
    ]

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        bufsize=10**7,
    )

    try:
        for frame_idx in range(total_frames):
            t = frame_idx / fps
            frame = comp.render_frame(t)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise RuntimeError(f"Error rendering {output_mp4.name}: {e}")

    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed with code {proc.returncode} for {output_mp4.name}")


def create_lofi_pad_bed(duration: float, output_wav: Path) -> None:
    """Synthesizes subtle ambient harmonic pad bed via native FFmpeg aevalsrc."""
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    # Ambient multi-harmonic drone without quotes or spaces
    expr = (
        "0.06*sin(2*PI*155.56*t)+0.05*sin(2*PI*196.00*t)+"
        "0.04*sin(2*PI*233.08*t)+0.03*sin(2*PI*293.66*t)+0.02*sin(2*PI*349.23*t)"
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"aevalsrc={expr}:s=48000:d={duration:.2f}",
        "-af", f"lowpass=f=450,afade=t=in:ss=0:d=1.5,afade=t=out:st={max(0.0, duration - 2.0):.2f}:d=2.0",
        "-c:a", "pcm_s16le",
        str(output_wav),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def master_audio_soundtrack(speech_wav: Path, duration: float, master_wav: Path) -> None:
    """Master audio pipeline: speech + lo-fi bed + sidechain ducking + EBU R128 -16 LUFS."""
    music_wav = speech_wav.parent / "ambient_bed.wav"
    create_lofi_pad_bed(duration, music_wav)

    # Sidechain ducking: music ducks by -14dB when speech is active
    filter_complex = (
        "[1:a]volume=0.35[bg];"
        "[bg][0:a]sidechaincompress=threshold=0.04:ratio=4:attack=100:release=350[ducked_bg];"
        "[0:a]highpass=f=80,equalizer=f=3200:t=q:w=1.5:g=2.5[voice];"
        "[voice][ducked_bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        "[mixed]loudnorm=I=-16:TP=-1.0:LRA=6[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(speech_wav),
        "-i", str(music_wav),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:a", "pcm_s16le",
        "-ar", "48000",
        str(master_wav),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def create_ass_subtitles(scenes_meta: List[Dict[str, Any]], output_ass: Path) -> None:
    """Generates SubStation Alpha subtitles with MarginV=360 bottom platform safe zone."""
    output_ass.parent.mkdir(parents=True, exist_ok=True)
    header = """[Script Info]
Title: Google Willow Quantum Error Correction Documentary
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,52,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,3,4,0,2,80,80,360,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    current_time = 0.0

    for s in scenes_meta:
        dur = s["duration"]
        text = s["narration"]
        start_t = current_time
        end_t = current_time + dur
        current_time = end_t

        # Format timestamps (H:MM:SS.CS)
        def fmt(t_sec):
            hrs = int(t_sec // 3600)
            mins = int((t_sec % 3600) // 60)
            secs = t_sec % 60
            return f"{hrs:d}:{mins:02d}:{secs:05.2f}"

        # Split long sentences into 2 sub-lines if necessary
        words = text.split()
        if len(words) > 12:
            mid = len(words) // 2
            formatted_text = " ".join(words[:mid]) + "\\N" + " ".join(words[mid:])
        else:
            formatted_text = text

        events.append(f"Dialogue: 0,{fmt(start_t)},{fmt(end_t)},Default,,0,0,360,,{formatted_text}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")


def generate_contact_sheet(video_path: Path, output_sheet: Path, rows: int = 5, cols: int = 5) -> None:
    """Extracts rows*cols evenly distributed frames and arranges them into a high-res contact sheet."""
    total_samples = rows * cols
    temp_dir = video_path.parent / "temp_sheet_frames"
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Probe duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    dur = float(subprocess.check_output(probe_cmd).strip())

    frame_files = []
    for idx in range(total_samples):
        t = (idx + 0.5) * (dur / total_samples)
        out_f = temp_dir / f"f_{idx:02d}.png"
        extract_cmd = [
            "ffmpeg", "-y",
            "-ss", f"{t:.3f}",
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(out_f)
        ]
        subprocess.run(extract_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        frame_files.append(out_f)

    # Assemble sheet (1080x1920 -> thumbnail 216x384)
    thumb_w, thumb_h = 216, 384
    sheet_w = cols * thumb_w + (cols + 1) * 12
    sheet_h = rows * thumb_h + (rows + 1) * 12 + 80  # Header bar

    sheet = Image.new("RGB", (sheet_w, sheet_h), (15, 23, 42))
    draw = ImageDraw.Draw(sheet)

    # Sheet Header
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 32)
        font_meta = ImageFont.truetype("consola.ttf", 20)
    except Exception:
        font_title = font_meta = ImageFont.load_default()

    draw.text((24, 24), "PHASE 8 FLAGSHIP FORENSIC CONTACT SHEET (25 TEMPORAL FRAMES)", fill=(255, 255, 255), font=font_title)
    draw.text((sheet_w - 440, 30), "GOOGLE WILLOW: QUANTUM ERROR CORRECTION", fill=(56, 189, 248), font=font_meta)

    for idx, f_path in enumerate(frame_files):
        r = idx // cols
        c = idx % cols
        x = 12 + c * (thumb_w + 12)
        y = 80 + 12 + r * (thumb_h + 12)

        im = Image.open(f_path).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))

        # Timecode badge
        t_sample = (idx + 0.5) * (dur / total_samples)
        draw.rectangle([x + 6, y + thumb_h - 28, x + 84, y + thumb_h - 6], fill=(0, 0, 0, 200))
        draw.text((x + 12, y + thumb_h - 26), f"{t_sample:4.1f}s", fill=(255, 255, 255), font=font_meta)

    sheet.save(output_sheet, format="PNG")

    # Cleanup temp
    for f in frame_files:
        f.unlink()
    temp_dir.rmdir()


def main():
    print("=" * 80)
    print("PHASE 8 FLAGSHIP PRODUCTION: GOOGLE WILLOW QUANTUM ERROR CORRECTION")
    print("=" * 80)
    start_time = time.time()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "audio").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "stems").mkdir(parents=True, exist_ok=True)

    # 1. Topic & Narrative Definition
    scenes_definition = [
        {
            "id": "scene1_cryostat_hook",
            "name": "Scene 1 — The Fragility Paradox (Cryostat Hook)",
            "comp_cls": Scene1CryostatHookComposition,
            "narration": "For three decades, quantum computing faced an impossible barrier. Adding more qubits made them exponentially more fragile. Until now.",
            "headline": "THE FRAGILITY PARADOX",
            "subheadline": "Why scaling quantum computers previously seemed impossible.",
        },
        {
            "id": "scene2_surface_code",
            "name": "Scene 2 — The 2D Surface Code Lattice",
            "comp_cls": Scene2SurfaceCodeLatticeComposition,
            "narration": "This is Willow, Google's breakthrough 105-qubit quantum processor. Instead of physical shielding, it organizes superconducting transmon qubits into a two-dimensional mathematical surface code.",
            "headline": "THE SURFACE CODE",
            "subheadline": "105 Physical Superconducting Transmon Qubits in 2D Lattice",
        },
        {
            "id": "scene3_error_healing",
            "name": "Scene 3 — Real-Time Syndrome Healing",
            "comp_cls": Scene3ErrorHealingPlaquetteComposition,
            "narration": "Surrounding measurement qubits act as sentinels. When cosmic rays cause a bit-flip, stabilizer sentinels detect and heal the error in under one microsecond, without ever collapsing the quantum superposition.",
            "headline": "REAL-TIME SYNDROME HEALING",
            "subheadline": "Detecting and correcting errors without collapsing quantum states.",
        },
        {
            "id": "scene4_below_threshold",
            "name": "Scene 4 — Crossing the Threshold (Nature Paper)",
            "comp_cls": Scene4BelowThresholdCurveComposition,
            "narration": "For the first time in history, Google proved that scaling up code distance exponentially reduces logical error, officially crossing the fault-tolerant threshold.",
            "headline": "CROSSING THE THRESHOLD",
            "subheadline": "First experimental proof: larger distance = lower error.",
        },
        {
            "id": "scene5_supercomputer_comparison",
            "name": "Scene 5 — The 10-Septillion-Year Benchmark",
            "comp_cls": Scene5SupercomputerComparisonComposition,
            "narration": "On standard random circuit sampling, Willow solved a calculation in under five minutes that would take Frontier, the world's fastest supercomputer, ten septillion years. Longer than the age of the universe.",
            "headline": "BENCHMARK PERFORMANCE",
            "subheadline": "5 Minutes on Willow vs 10 Septillion Years on Frontier.",
        },
        {
            "id": "scene6_loop_conclusion",
            "name": "Scene 6 — The Fault-Tolerant Horizon & Loop",
            "comp_cls": Scene6LoopConclusionComposition,
            "narration": "The era of self-healing qubits has begun. And that is how we finally solved the quantum fragility paradox.",
            "headline": "THE FAULT-TOLERANT ERA",
            "subheadline": "Self-healing qubits unlock practical materials science, chemistry, and AI.",
        },
    ]

    # 2. Kokoro Speech Synthesis (am_liam)
    print("\n[1/6] Synthesizing Voiceover via Kokoro batch pipeline (am_liam)...")
    runner = KokoroDirectRunner(workspace_root=WORKSPACE_ROOT)
    batch_items = []
    for s in scenes_definition:
        s_wav = OUTPUT_DIR / "audio" / f"{s['id']}.wav"
        batch_items.append((s["narration"].strip(), s_wav))

    batch_results = runner.generate_batch(items=batch_items, voice_id="am_liam", speed=1.0)

    # Update scene durations from exact speech length + 0.5s natural pause
    total_audio_duration = 0.0
    for s, (ok, meta) in zip(scenes_definition, batch_results):
        if not ok:
            raise RuntimeError(f"Kokoro batch synthesis failed for {s['id']}: {meta}")
        exact_dur = round(float(meta.get("duration", 7.5)) + 0.5, 2)
        s["duration"] = exact_dur
        total_audio_duration += exact_dur
        print(f"  -> {s['name']}: {exact_dur:.2f}s")

    print(f"  ✓ Total Documentary Narration Duration: {total_audio_duration:.2f}s")

    # Concatenate all speech segments
    speech_concat_wav = OUTPUT_DIR / "audio" / "phase8_willow_speech_concat.wav"
    concat_list_file = OUTPUT_DIR / "audio" / "speech_concat_list.txt"
    with open(concat_list_file, "w") as f:
        for s in scenes_definition:
            s_wav = OUTPUT_DIR / "audio" / f"{s['id']}.wav"
            f.write(f"file '{s_wav.resolve()}'\n")

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_file), "-c", "copy", str(speech_concat_wav)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    # 3. Render 1080x1920 Physical Explainer Stems
    print("\n[2/6] Rendering 1080x1920 Bespoke Physical Explainer Stems...")
    stem_paths = []
    for idx, s in enumerate(scenes_definition):
        t0 = time.time()
        # Full Pydantic Universal Scene Contract
        mock_scene = UniversalSceneContract(
            scene_id=f"phase8_{s['id']}",
            video_id="phase8_willow_quantum",
            sequence_number=idx + 1,
            scene_type=SceneType.TECHNICAL_DIAGRAM,
            preferred_engine=RenderingEngine.NATIVE_MOTION,
            rendering_engine=RenderingEngine.NATIVE_MOTION,
            narrative_purpose=s["headline"],
            audience_takeaway=f"Understand {s['headline']} through physical mechanism",
            mechanism_description=s["name"],
            target_duration_seconds=s["duration"],
            actual_duration_seconds=s["duration"],
            narration_duration_seconds=s["duration"],
            output_resolution=(1080, 1920),
            frame_rate=30.0,
            narration_text=s["narration"],
            visual_concept=s["id"],
            evidence_items=[
                FactClaimEvidence(
                    claim_id=f"claim_{s['id']}",
                    claim_text=f"Google Willow validation: {s['name']}",
                    source_url="https://nature.com/articles/s41586-024-08449-0",
                )
            ],
            engine_specific_config={
                "headline": s["headline"],
                "subheadline": s["subheadline"],
            }
        )
        comp = s["comp_cls"](mock_scene, width=1080, height=1920)
        stem_mp4 = OUTPUT_DIR / "stems" / f"{s['id']}.mp4"
        if not stem_mp4.exists() or stem_mp4.stat().st_size < 10000:
            render_composition_to_mp4(comp, stem_mp4, fps=30.0)
            elapsed = time.time() - t0
            print(f"  -> Rendered {s['name']}: {stem_mp4.stat().st_size / 1e6:.2f} MB in {elapsed:.1f}s")
        else:
            print(f"  -> Using cached stem {s['name']}: {stem_mp4.stat().st_size / 1e6:.2f} MB")
        stem_paths.append(stem_mp4)

    # 4. Master Audio Engineering (Lo-Fi Bed + Sidechain Ducking)
    print("\n[3/6] Engineering Master Soundtrack with lo-fi pad bed and sidechain ducking...")
    master_audio_wav = OUTPUT_DIR / "audio" / "phase8_willow_master_audio.wav"
    master_audio_soundtrack(speech_concat_wav, total_audio_duration, master_audio_wav)
    print("  ✓ Master Audio generated: phase8_willow_master_audio.wav (EBU R128: -16.0 LUFS)")

    # 5. Clean Master & Subtitle Burning
    print("\n[4/6] Assembling Clean Master and Captioned Master...")
    concat_txt = OUTPUT_DIR / "video_concat_list.txt"
    with open(concat_txt, "w") as f:
        for p in stem_paths:
            f.write(f"file '{p.resolve()}'\n")

    clean_mp4 = OUTPUT_DIR / "willow_quantum_documentary_clean.mp4"
    cmd_clean = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-i", str(master_audio_wav),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(clean_mp4)
    ]
    subprocess.run(cmd_clean, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✓ Clean Master MP4: {clean_mp4.name} ({clean_mp4.stat().st_size:,} bytes)")

    # Generate ASS Subtitles (MarginV=360)
    subtitles_ass = OUTPUT_DIR / "willow_quantum_documentary.ass"
    create_ass_subtitles(scenes_definition, subtitles_ass)

    # Burn subtitles
    captioned_mp4 = OUTPUT_DIR / "willow_quantum_documentary.mp4"
    ass_escaped = str(subtitles_ass.resolve()).replace("\\", "/").replace(":", "\\:")
    cmd_caption = [
        "ffmpeg", "-y",
        "-i", str(clean_mp4),
        "-vf", f"subtitles='{ass_escaped}'",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level", "4.2",
        "-preset", "veryfast",
        "-crf", "18",
        "-c:a", "copy",
        str(captioned_mp4)
    ]
    subprocess.run(cmd_caption, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✓ Captioned Review Master MP4: {captioned_mp4.name} ({captioned_mp4.stat().st_size:,} bytes)")

    # 6. Forensic Inspections & Contact Sheet
    print("\n[5/6] Extracting Forensic Inspection Frames & 25-Frame Contact Sheet...")
    contact_sheet_png = OUTPUT_DIR / "willow_quantum_documentary_contact_sheet.png"
    generate_contact_sheet(captioned_mp4, contact_sheet_png, rows=5, cols=5)
    print(f"  ✓ Contact sheet saved: {contact_sheet_png.name}")

    # Copy to Brain Artifacts
    brain_contact_sheet = BRAIN_ARTIFACTS_DIR / "willow_quantum_documentary_contact_sheet.png"
    brain_contact_sheet.write_bytes(contact_sheet_png.read_bytes())
    print(f"  ✓ Copied contact sheet to Brain Artifacts directory: {brain_contact_sheet.name}")

    # Extract 30 evenly distributed frames
    print("  -> Extracting 30 evenly distributed inspection frames...")
    frames_30_dir = REPORTS_DIR / "extracted_30_frames"
    frames_30_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(30):
        t_sample = (idx + 0.5) * (total_audio_duration / 30.0)
        f_out = frames_30_dir / f"frame_{idx:02d}_{t_sample:.2f}s.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{t_sample:.3f}", "-i", str(captioned_mp4), "-vframes", "1", "-q:v", "2", str(f_out)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    # 7. Production Manifest
    print("\n[6/6] Writing Production Manifest...")
    manifest = {
        "production_title": "Phase 8 Flagship Documentary: Google Willow Quantum Error Correction",
        "topic": "Google Willow: The Breakthrough That Solved Quantum Error Correction",
        "primary_evidence": "Nature Vol 636 / Google Quantum AI (Dec 2024)",
        "duration_seconds": total_audio_duration,
        "resolution": "1080x1920",
        "fps": 30.0,
        "codec": "H.264 High Profile",
        "audio_loudness_lufs": -16.0,
        "audio_true_peak_dbtp": -1.0,
        "governance_status": "AWAITING_HUMAN_APPROVAL",
        "publishing_kill_switch": "ARMED",
        "scenes": [
            {"id": s["id"], "name": s["name"], "duration": s["duration"]}
            for s in scenes_definition
        ],
        "outputs": {
            "clean_master_mp4": {
                "path": str(clean_mp4),
                "bytes": clean_mp4.stat().st_size,
                "sha256": compute_sha256(clean_mp4),
            },
            "captioned_master_mp4": {
                "path": str(captioned_mp4),
                "bytes": captioned_mp4.stat().st_size,
                "sha256": compute_sha256(captioned_mp4),
            },
            "contact_sheet": {
                "path": str(contact_sheet_png),
                "bytes": contact_sheet_png.stat().st_size,
                "sha256": compute_sha256(contact_sheet_png),
            },
            "master_audio": {
                "path": str(master_audio_wav),
                "bytes": master_audio_wav.stat().st_size,
                "sha256": compute_sha256(master_audio_wav),
            },
            "subtitles_ass": {
                "path": str(subtitles_ass),
                "bytes": subtitles_ass.stat().st_size,
                "sha256": compute_sha256(subtitles_ass),
            },
        }
    }

    manifest_json = OUTPUT_DIR / "willow_quantum_documentary_manifest.json"
    with open(manifest_json, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  ✓ Production Manifest saved: {manifest_json.name}")

    total_time = time.time() - start_time
    print(f"\n[DONE] Phase 8 Flagship Documentary produced successfully in {total_time:.2f}s!")


if __name__ == "__main__":
    main()
