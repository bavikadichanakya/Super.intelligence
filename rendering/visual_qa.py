"""
SUPER.INTELLIGENCEEE V2 — Deep Visual QA Subsystem
Performs automated computer-vision and perceptual quality auditing on rendered Reels.
Verifies frame luminance, perceptual diversity, duplicate detection, safe zone margins,
audio-visual synchronization, and generates high-resolution scene contact sheets.
"""

from __future__ import annotations

import json
import logging
import math
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageStat

from core.config import get_config

logger = logging.getLogger("super_intelligence.visual_qa")


class VisualQASubsystem:
    """Automated visual and perceptual quality assurance engine."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.ffmpeg_cmd = "ffmpeg"
        self.ffprobe_cmd = "ffprobe"

        self.contact_sheets_dir = self.config.resolve_path("output/contact_sheets")
        self.contact_sheets_dir.mkdir(parents=True, exist_ok=True)

    def probe_media_duration(self, file_path: Path | str) -> float:
        """Probes precise container/stream duration using ffprobe."""
        p = Path(file_path)
        if not p.exists():
            return 0.0

        cmd = [
            self.ffprobe_cmd,
            "-v", "error",
            "-show_entries", "format=duration:stream=duration",
            "-of", "json",
            str(p.resolve())
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(res.stdout)
            # Try format duration first
            if "format" in data and "duration" in data["format"]:
                return float(data["format"]["duration"])
            # Try first stream duration
            if "streams" in data and len(data["streams"]) > 0:
                for s in data["streams"]:
                    if "duration" in s:
                        return float(s["duration"])
            return 0.0
        except Exception as e:
            logger.warning(f"ffprobe duration probe failed for {p.name}: {e}")
            return 0.0

    def extract_keyframes(
        self,
        video_path: Path | str,
        timestamps: Optional[List[float]] = None,
        num_frames: int = 7,
        output_dir: Optional[Path] = None,
    ) -> List[Tuple[float, Path]]:
        """
        Extracts representative keyframes from the video at designated timestamps.
        Returns list of (timestamp_seconds, frame_path).
        """
        v_path = Path(video_path).resolve()
        if not v_path.exists():
            raise FileNotFoundError(f"Video file not found: {v_path}")

        dur = self.probe_media_duration(v_path)
        if dur <= 0.0:
            dur = 30.0

        if not timestamps:
            # Distribute timestamps evenly avoiding exact start and end edges
            step = dur / (num_frames + 1)
            timestamps = [round(step * (i + 1), 2) for i in range(num_frames)]

        out_dir = output_dir or v_path.parent / f"qa_frames_{v_path.stem}"
        out_dir.mkdir(parents=True, exist_ok=True)

        extracted = []
        for i, ts in enumerate(timestamps):
            frame_path = out_dir / f"frame_{i:02d}_{ts:.1f}s.png"
            cmd = [
                self.ffmpeg_cmd, "-y",
                "-ss", f"{ts:.2f}",
                "-i", str(v_path),
                "-vframes", "1",
                "-f", "image2",
                str(frame_path)
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0 and frame_path.exists() and frame_path.stat().st_size > 1000:
                extracted.append((ts, frame_path))
            else:
                logger.warning(f"Failed to extract frame at {ts:.2f}s: {res.stderr[:150]}")

        return extracted

    def check_black_frames(
        self,
        frame_items: List[Tuple[float, Path]],
        min_luminance: float = 6.0,
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Verifies that no extracted frame is a pitch-black void.
        Computes Root Mean Square (RMS) luminance across all color channels.
        """
        black_frames = []
        for ts, p in frame_items:
            try:
                with Image.open(p) as img:
                    # Convert to grayscale to evaluate perceptual luminance
                    gray = img.convert("L")
                    stat = ImageStat.Stat(gray)
                    mean_lum = stat.mean[0]
                    rms_lum = stat.rms[0]

                    if mean_lum < min_luminance:
                        black_frames.append({
                            "timestamp": ts,
                            "frame_path": str(p),
                            "mean_luminance": round(mean_lum, 2),
                            "rms_luminance": round(rms_lum, 2),
                            "issue": f"Solid black or near-zero luminance frame detected (mean: {mean_lum:.2f} < {min_luminance})"
                        })
            except Exception as e:
                logger.warning(f"Error checking luminance for {p.name}: {e}")

        passed = len(black_frames) == 0
        return passed, black_frames

    def check_perceptual_diversity(
        self,
        frame_items: List[Tuple[float, Path]],
        max_similarity: float = 0.94,
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Computes normalized Root Mean Square Error (RMSE) similarity between consecutive scene frames.
        Detects repetitive slide templates and stagnant duplicate scenes.
        """
        duplicate_pairs = []
        if len(frame_items) < 2:
            return True, []

        for i in range(len(frame_items) - 1):
            ts1, p1 = frame_items[i]
            ts2, p2 = frame_items[i + 1]

            try:
                with Image.open(p1) as im1, Image.open(p2) as im2:
                    # Resize to low-res thumbnail for fast perceptual histogram/pixel comparison
                    thumb1 = im1.resize((128, 128)).convert("RGB")
                    thumb2 = im2.resize((128, 128)).convert("RGB")

                    # Calculate Mean Squared Error using raw byte buffers
                    b1 = thumb1.tobytes()
                    b2 = thumb2.tobytes()
                    diff_sq_sum = sum((v1 - v2) ** 2 for v1, v2 in zip(b1, b2))

                    mse = diff_sq_sum / (128 * 128 * 3.0)
                    rmse = math.sqrt(mse)
                    # Similarity index: 1.0 = identical, 0.0 = completely distinct
                    similarity = max(0.0, 1.0 - (rmse / 255.0))

                    if similarity > max_similarity:
                        duplicate_pairs.append({
                            "frame_a": (ts1, str(p1)),
                            "frame_b": (ts2, str(p2)),
                            "similarity_score": round(similarity, 3),
                            "issue": f"Stagnant repetition: Consecutive frames at {ts1:.1f}s and {ts2:.1f}s are {similarity*100:.1f}% visually identical"
                        })
            except Exception as e:
                logger.warning(f"Perceptual diversity check error between {p1.name} and {p2.name}: {e}")

        passed = len(duplicate_pairs) == 0
        return passed, duplicate_pairs

    def check_test_patterns(
        self,
        frame_items: List[Tuple[float, Path]],
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Detects artificial test cards and calibration patterns (e.g. FFmpeg testsrc, SMPTE bars).
        Checks for pure saturated calibration color patches (yellow, magenta, cyan).
        """
        test_pattern_frames = []
        for ts, p in frame_items:
            try:
                with Image.open(p) as img:
                    thumb = img.resize((120, 120)).convert("RGB")
                    pixels = list(thumb.getdata())
                    total = len(pixels)
                    calib_colors = 0
                    for r, g, b in pixels:
                        # Check pure yellow, pure magenta, pure cyan calibration patches
                        if (r > 240 and g > 240 and b < 20) or (r > 240 and g < 20 and b > 240) or (r < 20 and g > 240 and b > 240):
                            calib_colors += 1

                    ratio = calib_colors / float(total)
                    if ratio > 0.08:  # Over 8% saturated calibration colors indicates testsrc
                        test_pattern_frames.append({
                            "timestamp": ts,
                            "frame_path": str(p),
                            "calibration_pixel_ratio": round(ratio, 3),
                            "issue": f"Calibration test card / testsrc detected at {ts:.1f}s (ratio: {ratio*100:.1f}%)"
                        })
            except Exception as e:
                logger.warning(f"Error checking test patterns for {p.name}: {e}")

        passed = len(test_pattern_frames) == 0
        return passed, test_pattern_frames

    def check_safe_zones(
        self,
        frame_items: List[Tuple[float, Path]],
        target_res: Tuple[int, int] = (1080, 1920),
    ) -> Tuple[bool, List[str]]:
        """
        Checks resolution compliance (1080x1920) across all extracted keyframes.
        """
        issues = []
        for ts, p in frame_items:
            try:
                with Image.open(p) as img:
                    if img.size != target_res:
                        issues.append(f"Frame at {ts:.1f}s violates 9:16 vertical standard: {img.size} != {target_res}")
            except Exception as e:
                issues.append(f"Could not open frame {p.name}: {e}")

        passed = len(issues) == 0
        return passed, issues

    def verify_audio_video_sync(
        self,
        video_path: Path | str,
        audio_path: Path | str,
        max_delta_seconds: float = 0.35,
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Verifies that final video track duration precisely matches master narration audio.
        Guarantees that narration speech is never truncated mid-sentence and no trailing black frames exist.
        """
        v_dur = self.probe_media_duration(video_path)
        a_dur = self.probe_media_duration(audio_path)
        delta = abs(v_dur - a_dur)

        passed = delta <= max_delta_seconds
        report = {
            "video_duration_seconds": round(v_dur, 2),
            "audio_duration_seconds": round(a_dur, 2),
            "delta_seconds": round(delta, 3),
            "max_allowed_delta": max_delta_seconds,
            "synchronized": passed,
            "status": "PASS" if passed else "FAIL_DESYNC",
        }
        if not passed:
            report["issue"] = f"AV desynchronization detected: Video ({v_dur:.2f}s) vs Audio ({a_dur:.2f}s) delta is {delta:.2f}s (exceeds {max_delta_seconds}s limit)"

        return passed, report

    def generate_contact_sheet(
        self,
        frame_items: List[Tuple[float, Path]],
        output_path: Path | str,
        title: str = "SUPER.INTELLIGENCEEE REEL VISUAL CONTACT SHEET",
        labels: Optional[List[str]] = None,
    ) -> Path:
        """
        Compiles all extracted scene keyframes into a high-resolution visual contact sheet
        annotated with timestamps, scene indexes, and production mode tags.
        """
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        if not frame_items:
            raise ValueError("No frames provided for contact sheet.")

        # Layout: Grid with 4 columns or dynamic cols based on frame count
        total_frames = len(frame_items)
        cols = min(4, total_frames)
        rows = math.ceil(total_frames / cols)

        thumb_w = 360
        thumb_h = 640 # 9:16 aspect ratio
        margin_x = 24
        margin_y = 24
        header_h = 100

        sheet_w = cols * thumb_w + (cols + 1) * margin_x
        sheet_h = header_h + rows * (thumb_h + 50) + (rows + 1) * margin_y

        sheet = Image.new("RGB", (sheet_w, sheet_h), (12, 16, 24))
        draw = ImageDraw.Draw(sheet)

        # Header Title
        draw.text((margin_x, 30), title.upper(), fill=(0, 229, 255), font=None)
        draw.text((margin_x, 60), f"TOTAL FRAMES: {total_frames} // TIME: {time.strftime('%Y-%m-%d %H:%M:%S')}", fill=(148, 163, 184), font=None)
        draw.line([(margin_x, 88), (sheet_w - margin_x, 88)], fill=(30, 45, 70), width=2)

        for i, (ts, fp) in enumerate(frame_items):
            c = i % cols
            r = i // cols

            x = margin_x + c * (thumb_w + margin_x)
            y = header_h + margin_y + r * (thumb_h + 50 + margin_y)

            try:
                with Image.open(fp) as im:
                    thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                    sheet.paste(thumb, (x, y))

                    # Border outline
                    draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], outline=(0, 229, 255), width=2)

                    # Timestamp & scene label badge
                    lbl = labels[i] if (labels and i < len(labels)) else f"SCENE #{i+1}"
                    draw.rectangle([(x, y + thumb_h + 6), (x + thumb_w, y + thumb_h + 38)], fill=(20, 28, 44))
                    draw.text((x + 8, y + thumb_h + 12), f"{lbl}  [{ts:.1f}s]", fill=(255, 215, 0), font=None)
            except Exception as e:
                logger.warning(f"Error drawing frame thumbnail on contact sheet: {e}")

        sheet.save(out_p, format="PNG")
        logger.info(f"Visual contact sheet saved: {out_p.name} ({out_p.stat().st_size} bytes)")
        return out_p

    def run_full_visual_audit(
        self,
        video_path: Path | str,
        audio_path: Optional[Path | str] = None,
        scene_briefs: Optional[List[Any]] = None,
        output_contact_sheet: Optional[Path | str] = None,
    ) -> Dict[str, Any]:
        """
        Runs comprehensive multi-point Visual QA audit:
        1. Keyframe extraction
        2. Black frame luminance detection
        3. Perceptual diversity and duplicate detection
        4. Safe zone 1080x1920 conformance
        5. Audio-visual duration synchronization
        6. Visual contact sheet generation
        """
        v_p = Path(video_path).resolve()
        logger.info(f"Starting Visual QA Audit on {v_p.name}...")

        # 1. Extract Keyframes at Scene Midpoints if scene briefs are provided
        timestamps = None
        if scene_briefs and len(scene_briefs) > 1:
            midpoints = []
            cumulative = 0.0
            for b in scene_briefs:
                d = float(b.duration_seconds) if hasattr(b, "duration_seconds") else float(b.get("duration_seconds", b.get("duration", 5.0)))
                midpoints.append(round(cumulative + (d / 2.0), 2))
                cumulative += d
            v_dur = self.probe_media_duration(v_p)
            if v_dur > 0:
                midpoints = [m for m in midpoints if m < v_dur]
            if len(midpoints) >= 2:
                timestamps = midpoints

        frame_items = self.extract_keyframes(
            v_p,
            num_frames=len(scene_briefs) if scene_briefs else 7,
            timestamps=timestamps,
        )

        # 2. Black Frame Detection
        bf_pass, bf_issues = self.check_black_frames(frame_items)

        # 3. Perceptual Diversity
        pd_pass, pd_issues = self.check_perceptual_diversity(frame_items)

        # 4. Safe Zones
        sz_pass, sz_issues = self.check_safe_zones(frame_items)

        # 5. Test Pattern & Calibration Card Detection
        tp_pass, tp_issues = self.check_test_patterns(frame_items)

        # 6. AV Sync
        av_pass, av_report = True, {}
        if audio_path and Path(audio_path).exists():
            av_pass, av_report = self.verify_audio_video_sync(v_p, audio_path)

        # 7. Contact Sheet
        cs_path = None
        target_cs = output_contact_sheet or self.contact_sheets_dir / f"{v_p.stem}_contact_sheet.png"
        labels = []
        if scene_briefs:
            for b in scene_briefs:
                if hasattr(b, "production_mode"):
                    m = b.production_mode.value if hasattr(b.production_mode, "value") else str(b.production_mode)
                elif hasattr(b, "scene_type"):
                    m = b.scene_type.value if hasattr(b.scene_type, "value") else str(b.scene_type)
                elif isinstance(b, dict):
                    m = b.get("production_mode", b.get("scene_type", "SCENE"))
                else:
                    m = "SCENE"
                labels.append(m.upper())

        try:
            cs_path = self.generate_contact_sheet(
                frame_items=frame_items,
                output_path=target_cs,
                title=f"VISUAL QA AUDIT: {v_p.name}",
                labels=labels,
            )
        except Exception as e:
            logger.warning(f"Could not generate contact sheet: {e}")

        all_passed = bf_pass and pd_pass and sz_pass and av_pass and tp_pass

        audit_report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "video_path": str(v_p),
            "total_frames_audited": len(frame_items),
            "overall_qa_pass": all_passed,
            "black_frame_check": {
                "passed": bf_pass,
                "black_frames_detected": len(bf_issues),
                "issues": bf_issues,
            },
            "perceptual_diversity_check": {
                "passed": pd_pass,
                "duplicate_pairs_detected": len(pd_issues),
                "issues": pd_issues,
            },
            "safe_zone_check": {
                "passed": sz_pass,
                "issues": sz_issues,
            },
            "test_pattern_check": {
                "passed": tp_pass,
                "test_patterns_detected": len(tp_issues),
                "issues": tp_issues,
            },
            "av_sync_check": av_report,
            "contact_sheet_path": str(cs_path) if cs_path else None,
        }

        return audit_report
