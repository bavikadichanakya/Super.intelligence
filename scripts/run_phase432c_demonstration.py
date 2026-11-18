"""
SUPER.INTELLIGENCEEE — Phase 4.3.2C End-to-End Autonomous Demonstration Runner
Executes the integrated production pipeline on genuine live topic #499 from arXiv:
"Metal Sandbox: Isolated Execution and Command Scheduling for GPU Coding Agents on Apple Silicon"
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
logger = logging.getLogger("phase432c_runner")


def main():
    logger.info("Initializing Phase 4.3.2C Autonomous Documentary Demonstration...")
    db = Database()
    pipeline = UnifiedDocumentaryPipeline(db=db)

    run_dir = Path("A:/SUPER.INTELLIGENCEEE/output/drafts/phase432c_production_run").resolve()
    masters_dir = run_dir / "masters"
    has_masters = (
        masters_dir.exists()
        and bool(list(masters_dir.glob("*_clean_master.mp4")))
        and bool(list(masters_dir.glob("*_captioned_review.mp4")))
    )
    if not has_masters and run_dir.exists():
        import shutil
        shutil.rmtree(run_dir, ignore_errors=True)
    run_dir.mkdir(parents=True, exist_ok=True)

    # Execute genuine live topic #499 (arXiv Metal Sandbox)
    start_time = time.time()
    manifest = pipeline.run_autonomous_production(
        topic_id=499,
        output_run_dir=run_dir,
    )
    total_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("PHASE 4.3.2C DEMONSTRATION RUN COMPLETE")
    print("=" * 80)
    print(f"Status:               {manifest['status']}")
    print(f"Production Job ID:    #{manifest['job_id']}")
    print(f"Approval ID:          #{manifest['approval_id']}")
    print(f"Topic:                {manifest['topic']['title']}")
    print(f"Publisher:            {manifest['topic']['publisher']}")
    print(f"Total Duration:       {manifest['duration_seconds']:.2f} seconds")
    print(f"Execution Wall Time:  {total_time:.2f} seconds")
    print(f"Captioned Master MP4: {manifest['captioned_master_path']}")
    print(f"Clean Master MP4:     {manifest['clean_master_path']}")
    print(f"Master Audio WAV:     {manifest['master_audio_path']}")
    print(f"Subtitles ASS:        {manifest['subtitles_ass_path']}")
    print(f"Contact Sheet PNG:    {manifest['qa_report'].get('contact_sheet')}")
    print(f"Total Stems:          {manifest['stem_count']}")
    for s in manifest["stems"]:
        print(f"  - [{s['engine'].upper()}] {Path(s['path']).name} ({s['duration']:.2f}s, SHA-256: {s['sha256'][:12]}...)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
