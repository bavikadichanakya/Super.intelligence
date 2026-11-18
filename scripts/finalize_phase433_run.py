"""
SUPER.INTELLIGENCEEE — Phase 4.3.3 Production Finalizer
Re-renders stems with sequence-number priority routing, re-assembles masters,
runs full Visual QA, and updates manifest and database records.
"""

import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.database import Database
from core.unified_pipeline import UnifiedDocumentaryPipeline, PipelineStage
from core.universal_scene_contract import VideoStoryboardContract
from rendering.render_artifact import RenderArtifact

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("phase433_finalizer")


def main():
    run_dir = Path("A:/SUPER.INTELLIGENCEEE/output/drafts/phase433_explainer_demo").resolve()
    db = Database()
    pipeline = UnifiedDocumentaryPipeline(db=db)

    # 1. Load existing storyboard
    sb_path = run_dir / "storyboard.json"
    with open(sb_path, "r", encoding="utf-8") as f:
        sb_raw = json.load(f)
    storyboard = VideoStoryboardContract.model_validate(sb_raw)

    # 2. Load existing research dossier
    dossier_path = run_dir / "research_dossier.json"
    dossier = pipeline.build_research_dossier(pipeline.select_or_discover_topic(topic_id=499))

    # 3. Load master audio
    master_audio = run_dir / "audio" / "master_narration_16lufs.wav"

    # 4. Re-render stems with corrected renderer routing
    logger.info("Re-rendering scene stems with sequence-number priority...")
    t0 = time.time()
    stem_artifacts = pipeline.render_scenes_with_dispatcher(storyboard, run_dir)
    render_time = time.time() - t0
    logger.info(f"All {len(stem_artifacts)} stems re-rendered in {render_time:.2f}s.")

    # 5. Assemble dual masters (Clean + Captioned)
    logger.info("Assembling clean and captioned masters...")
    clean_master, captioned_master, sub_file = pipeline.assemble_dual_masters(
        storyboard=storyboard,
        stem_artifacts=stem_artifacts,
        master_audio_path=master_audio,
        run_dir=run_dir,
    )

    # 6. Run full Quality Assurance
    logger.info("Running full Visual & Technical QA...")
    qa_report = pipeline.execute_quality_assurance(
        clean_master=clean_master,
        captioned_master=captioned_master,
        storyboard=storyboard,
        dossier=dossier,
        run_dir=run_dir,
    )

    # 7. Update approval submission
    approval_id = pipeline.register_approval_submission(
        job_id=56,
        storyboard=storyboard,
        captioned_master=captioned_master,
        dossier=dossier,
        qa_report=qa_report,
    )

    # 8. Load timing metadata from previous manifest if available
    prev_manifest_path = run_dir / "production_manifest.json"
    timing_meta = {}
    topic_data = {}
    if prev_manifest_path.exists():
        with open(prev_manifest_path, "r", encoding="utf-8") as f:
            pm = json.load(f)
            timing_meta = pm.get("timing_metadata", {})
            topic_data = pm.get("topic", {})

    manifest = {
        "status": "AWAITING_HUMAN_APPROVAL",
        "job_id": 56,
        "approval_id": approval_id,
        "topic": topic_data or {"id": 499, "title": storyboard.title, "publisher": "arXiv.org"},
        "voice_id": timing_meta.get("voice_used", "am_liam"),
        "voice_provider": "voicebox",
        "voice_engine": timing_meta.get("engine_used", "kokoro"),
        "voice_model": timing_meta.get("model", "hexgrad/Kokoro-82M"),
        "voice_locale": timing_meta.get("locale", "en-US"),
        "voice_accent": timing_meta.get("accent", "general_american"),
        "duration_seconds": captioned_master.duration_seconds,
        "clean_master_path": str(clean_master.output_path),
        "captioned_master_path": str(captioned_master.output_path),
        "subtitles_ass_path": str(sub_file),
        "master_audio_path": str(master_audio),
        "stem_count": len(stem_artifacts),
        "stems": [
            {
                "engine": a.engine_name,
                "path": str(a.output_path),
                "duration": a.duration_seconds,
                "sha256": a.sha256_hash,
                "size_bytes": a.file_size_bytes,
            }
            for a in stem_artifacts
        ],
        "timing_metadata": timing_meta,
        "qa_report": qa_report,
        "run_dir": str(run_dir),
    }

    with open(run_dir / "production_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 80)
    print("PHASE 4.3.3 FINAL MASTERING COMPLETE")
    print("=" * 80)
    print(f"Status:               {manifest['status']}")
    print(f"Production Job ID:    #{manifest['job_id']}")
    print(f"Approval ID:          #{manifest['approval_id']}")
    print(f"Voice ID:             {manifest.get('voice_id')}")
    print(f"Voice Engine:         {manifest.get('voice_engine')}")
    print(f"Voice Model:          {manifest.get('voice_model')}")
    print(f"Total Duration:       {manifest['duration_seconds']:.2f}s")
    print(f"Captioned Master:     {manifest['captioned_master_path']}")
    print(f"Clean Master:         {manifest['clean_master_path']}")
    print(f"Contact Sheet:        {manifest['qa_report'].get('contact_sheet')}")
    print("-" * 80)
    print(f"Overall QA Passed:    {qa_report.get('passed')}")
    print(f"Technical QA Valid:   {qa_report.get('technical_qa_captioned', {}).get('valid')}")
    vis_qa = qa_report.get("visual_qa", {})
    print(f"Visual QA Pass:       {vis_qa.get('overall_qa_pass')}")
    print(f"Diversity Pass:       {vis_qa.get('perceptual_diversity_check', {}).get('passed')}")
    print(f"Test Pattern Detected: {vis_qa.get('test_pattern_check', {}).get('test_patterns_detected', 0)}")
    print(f"Black Frames:         {vis_qa.get('black_frame_check', {}).get('black_frames_detected', 0)}")
    print(f"Safe Zone Pass:       {vis_qa.get('safe_zone_check', {}).get('passed')}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
