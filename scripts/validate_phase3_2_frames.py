"""
SUPER.INTELLIGENCEEE — Phase 3.2 Spacing & Typography Midpoint Frame Validator
Samples each scene midpoint from the final rendered MP4 and runs SpacingTypographyValidator.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rendering.typography_validator import SpacingTypographyValidator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("validate_phase3_2_frames")

VIDEO_PATH = Path("output/drafts/doc_phase3_2_20261107_120433_state_space_attention_scaling_tech_doc_final.mp4")
OUTPUT_DIR = Path("output/qa_frames")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    {"index": 1, "name": "Kinetic Typography", "timestamp": 11.4},
    {"index": 2, "name": "Cinematic Silicon Die", "timestamp": 32.8},
    {"index": 3, "name": "Vector Diagram Attention Flow", "timestamp": 51.5},
    {"index": 4, "name": "Triton Terminal Execution", "timestamp": 69.1},
    {"index": 5, "name": "Comparative Data Visualization", "timestamp": 87.6},
    {"index": 6, "name": "Architectural Verdict", "timestamp": 103.8},
]

def main():
    validator = SpacingTypographyValidator()
    results = []

    for sc in SCENES:
        frame_path = OUTPUT_DIR / f"phase3_2_scene_{sc['index']:02d}_{sc['name'].lower().replace(' ', '_')}.png"
        
        # Extract frame via ffmpeg
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{sc['timestamp']:.3f}",
            "-i", str(VIDEO_PATH),
            "-frames:v", "1",
            "-q:v", "2",
            str(frame_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            logger.error(f"FFmpeg failed to extract frame at {sc['timestamp']}: {res.stderr.decode('utf-8', errors='ignore')}")
            continue

        report = validator.validate_frame(frame_path)
        report["scene_name"] = sc["name"]
        report["timestamp"] = sc["timestamp"]
        results.append(report)

        logger.info(
            f"Scene #{sc['index']} [{sc['name']}]: "
            f"Pass={report['passed']} | "
            f"Luminance={report['mean_bg_luminance']} (Threshold: >=0.65) | "
            f"Contrast={report['contrast_ratio']}:1 (Threshold: >=4.5:1) | "
            f"Density={report['active_content_density']*100:.1f}% | "
            f"SafeZones=(Top:{report['top_safe_zone_pass']}, Bottom:{report['bottom_safe_zone_pass']}) | "
            f"Issues={report['issues']}"
        )

    json_path = Path("output/drafts/phase3_2_spacing_typography_audit.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Audit complete for {len(results)} scenes. Report saved: {json_path}")

if __name__ == "__main__":
    main()
