"""
SUPER.INTELLIGENCEEE — Phase 4.3.3 Production Demonstration Runner
Executes the integrated production pipeline with:
1. Kokoro-82M am_liam (General American male narration voice locked).
2. Light-First Cinematic Explainer Motion Graphics Engine (warm ivory #FAF7F2, obsidian typography #0F172A).
Target Topic: arXiv:2611.17294v1 (#499)
"Metal Sandbox: Isolated Execution and Command Scheduling for GPU Coding Agents on Apple Silicon"
Target directory: output/drafts/phase433_explainer_demo/
"""

import json
import logging
import sys
import time
from pathlib import Path

# Ensure project root in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.database import Database
from core.unified_pipeline import UnifiedDocumentaryPipeline

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("phase433_runner")


def main():
    logger.info("=" * 80)
    logger.info("INITIALIZING PHASE 4.3.3 CONTROLLED PRODUCTION DEMONSTRATION")
    logger.info("VOICE: Kokoro-82M [am_liam] | THEME: Light-First Cinematic Explainer")
    logger.info("=" * 80)

    db = Database()
    pipeline = UnifiedDocumentaryPipeline(db=db)

    run_dir = Path("A:/SUPER.INTELLIGENCEEE/output/drafts/phase433_explainer_demo").resolve()

    # Clean fresh directory for demonstration
    if run_dir.exists():
        import shutil
        shutil.rmtree(run_dir, ignore_errors=True)
    run_dir.mkdir(parents=True, exist_ok=True)

    # Execute production demonstration on arXiv topic #499
    start_time = time.time()
    manifest = pipeline.run_autonomous_production(
        topic_id=499,
        output_run_dir=run_dir,
        resume=False,
    )
    total_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("PHASE 4.3.3 PRODUCTION DEMONSTRATION COMPLETE")
    print("=" * 80)
    print(f"Status:               {manifest['status']}")
    print(f"Production Job ID:    #{manifest['job_id']}")
    print(f"Approval ID:          #{manifest['approval_id']}")
    print(f"Topic:                {manifest['topic']['title']}")
    print(f"Publisher:            {manifest['topic']['publisher']}")
    print(f"Voice Engine:         {manifest.get('voice_engine')}")
    print(f"Voice ID:             {manifest.get('voice_id')}")
    print(f"Voice Model:          {manifest.get('voice_model')}")
    print(f"Voice Accent:         {manifest.get('voice_accent')}")
    print(f"Total Duration:       {manifest['duration_seconds']:.2f} seconds")
    print(f"Execution Wall Time:  {total_time:.2f} seconds")
    print(f"Captioned Master MP4: {manifest['captioned_master_path']}")
    print(f"Clean Master MP4:     {manifest['clean_master_path']}")
    print(f"Master Audio WAV:     {manifest['master_audio_path']}")
    print(f"Subtitles ASS:        {manifest['subtitles_ass_path']}")
    print(f"Contact Sheet PNG:    {manifest['qa_report'].get('contact_sheet')}")
    print(f"Total Stems:          {manifest['stem_count']}")
    for s in manifest.get("stems", []):
        p = Path(s['path'])
        print(f"  - [{s['engine'].upper()}] {p.name} ({s['duration']:.2f}s, SHA-256: {s['sha256'][:12]}...)")
    
    # QA Summary
    qa_rep = manifest.get("qa_report", {})
    vis_qa = qa_rep.get("visual_qa", {})
    print("-" * 80)
    print(f"Overall QA Passed:    {qa_rep.get('passed')}")
    print(f"Technical QA Valid:   {qa_rep.get('technical_qa_captioned', {}).get('valid')}")
    print(f"Visual QA Pass:       {vis_qa.get('overall_qa_pass')}")
    print(f"Test Pattern Detected: {vis_qa.get('test_pattern_check', {}).get('test_patterns_detected', 0)} (Passed: {vis_qa.get('test_pattern_check', {}).get('passed')})")
    print(f"Black Frames:         {vis_qa.get('black_frame_check', {}).get('black_frames_detected', 0)}")
    print(f"Safe Zone Pass:       {vis_qa.get('safe_zone_check', {}).get('passed')}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
