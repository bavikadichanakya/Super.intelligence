"""
SUPER.INTELLIGENCEEE V2 — Creative Engine Demonstration Reel Producer
Executes an end-to-end production run using the redesigned Creative Production Engine.
Produces a dynamic, cinematic Instagram Reel on frontier AI with:
- Decoupled SceneCreativeBriefs
- Multiple production modes (Motion Graphics, Split Screen, Data Viz, Architecture Diagram, Terminal, HUD, Stock)
- Ken Burns dynamic camera push-in and video motion preservation
- Exact per-scene audio synchronization (zero audio truncation, zero trailing black frames)
- Cryptographic AssetProvenanceManifest
- Deep Visual QA audit and annotated scene contact sheet
"""

import datetime
import json
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.database import Database
from core.pipeline import SuperIntelligencePipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("super_intelligence.demo_producer")


def main():
    print("=" * 80)
    print("SUPER.INTELLIGENCEEE V2 — CREATIVE ENGINE DEMONSTRATION RUN")
    print("=" * 80)

    db = Database()
    pipeline = SuperIntelligencePipeline(db=db)

    # 1. Prepare Frontier AI Benchmark Topic
    topic_data = {
        "title": "Sub-Quadratic Attention Scaled to 1M Tokens at the Edge",
        "url": "https://synthetic.superintelligenceee.local/sub-quadratic-attention-breakthrough",
        "publisher": "Frontier AI Benchmark Institute",
        "summary": "Researchers demonstrate a breakthrough sub-quadratic attention mechanism maintaining linear O(N) memory scaling across one million tokens. Empirical edge tests show 4.2x faster generation and 78% VRAM reduction on consumer hardware with zero accuracy loss.",
        "category": "New AI Models & Releases",
    }

    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO topics (title, url, publisher, summary, category, score, status, discovered_at)
            VALUES (?, ?, ?, ?, ?, 99.0, 'DISCOVERED', ?)
            """,
            (
                topic_data["title"],
                topic_data["url"],
                topic_data["publisher"],
                topic_data["summary"],
                topic_data["category"],
                datetime.datetime.now().isoformat(),
            ),
        )
        topic_id = cursor.lastrowid

    logger.info(f"Inserted Demonstration Topic #{topic_id}: '{topic_data['title']}'")

    # 2. Execute Full Production Pipeline
    logger.info("Executing SuperIntelligencePipeline.produce_reel...")
    start_time = datetime.datetime.now()
    result = pipeline.produce_reel(topic_id=topic_id)
    elapsed = (datetime.datetime.now() - start_time).total_seconds()

    print("\n" + "=" * 80)
    print("PRODUCTION PIPELINE EXECUTION COMPLETED")
    print(f"Elapsed Time: {elapsed:.1f}s")
    print(f"Production Job ID: #{result['production_job_id']}")
    print(f"Job Status: {result['status']}")
    print(f"Final Video: {result['video_path']}")
    print(f"Resolution: {result['dimensions']}")
    print(f"Duration: {result['duration']:.2f}s")
    print(f"Framerate: {result['fps']} fps")
    print("=" * 80)

    # 3. Print Creative Artifacts
    print("\n--- PRODUCED CREATIVE ARTIFACTS ---")
    print(f"1. Final MP4 Video:         {result['video_path']}")
    print(f"2. Storyboard JSON:         {result.get('storyboard_path')}")
    print(f"3. Creative Plan JSON:      {result.get('creative_plan_path')}")
    print(f"4. Provenance Manifest:     {result.get('manifest_path')}")
    print(f"5. Scene Contact Sheet:     {result.get('contact_sheet_path')}")

    # 4. Print Visual QA Telemetry
    vqa = result.get("visual_qa", {})
    print("\n--- DEEP VISUAL QA AUDIT REPORT ---")
    print(f"Overall Visual QA Pass:     {vqa.get('overall_qa_pass')}")
    print(f"Total Keyframes Audited:    {vqa.get('total_frames_audited')}")
    print(f"Black Frames Detected:      {vqa.get('black_frame_check', {}).get('black_frames_detected')} (Pass: {vqa.get('black_frame_check', {}).get('passed')})")
    print(f"Duplicate Frame Pairs:      {vqa.get('perceptual_diversity_check', {}).get('duplicate_pairs_detected')} (Pass: {vqa.get('perceptual_diversity_check', {}).get('passed')})")
    print(f"Safe Zone Resolution Pass:  {vqa.get('safe_zone_check', {}).get('passed')}")

    av_sync = vqa.get("av_sync_check", {})
    print(f"Audio/Video Sync Pass:      {av_sync.get('synchronized')} (Delta: {av_sync.get('delta_seconds')}s, Video: {av_sync.get('video_duration_seconds')}s, Audio: {av_sync.get('audio_duration_seconds')}s)")

    # 5. Print Audio QA Telemetry
    aqa = result.get("audio_qa", {})
    print("\n--- AUDIO QA AUDIT REPORT ---")
    print(f"QA Method:                  {aqa.get('qa_method')}")
    print(f"Passed:                     {aqa.get('passed')}")
    print(f"Score:                      {aqa.get('score')}")
    print(f"Issues:                     {aqa.get('issues')}")

    # 6. Print Fact Checking Telemetry
    fc = result.get("fact_check", {})
    print("\n--- FACT-CHECKING AUDIT REPORT ---")
    print(f"Verified:                   {fc.get('verified')}")
    print(f"Evidence Summary:           {fc.get('evidence_summary')}")
    print("=" * 80)


if __name__ == "__main__":
    main()
