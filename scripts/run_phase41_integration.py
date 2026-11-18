"""
SUPER.INTELLIGENCEEE — Phase 4.1 Master Pipeline Runner Script
Executes the unified production pipeline on the approved Phase 4.1 topic:
'Unpacking the Compute Efficiency of Strong-to-Weak OPD against GRPO' (arXiv:2611.08453)
Enforces:
- Hardened research dossier with mandatory qualifications.
- Dynamic story architecture & qualified script formulation.
- Dynamic scene planning & visual diversity checks.
- Voicebox Kokoro speech synthesis (am_liam) with millisecond-exact timing sync.
- TechDocProducer rendering to isolated output/drafts/phase41_prototype/.
- Automated visual QA and stream integrity audits.
- Strict human approval gating (NEEDS_REVIEW) and zero auto-publishing.
"""

import json
import logging
import sys
from pathlib import Path

# Add repository root to python search path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Set up logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("run_phase41_integration")

from core.unified_pipeline import UnifiedProductionPipeline

def main():
    topic = {
        "title": "Unpacking the Compute Efficiency of Strong-to-Weak OPD against GRPO",
        "url": "https://arxiv.org/abs/2611.08453",
        "summary": (
            "Empirical investigation of on-policy distillation (OPD) compute scaling versus Group Relative Policy Optimization (GRPO). "
            "A critical trade-off is revealed: 50x FLOP efficiency occurs strictly when distilling from the student's own GRPO checkpoint, "
            "whereas using an external teacher generally loses to GRPO in accuracy per training FLOP under matched settings."
        ),
        "category": "Artificial Intelligence Research",
        "source": "arXiv.org",
    }

    logger.info("Initializing Phase 4.1 Unified Production Pipeline...")
    pipeline = UnifiedProductionPipeline()

    logger.info("Starting execution of Phase 4.1 integration run...")
    result = pipeline.execute_integration_run(
        topic=topic,
        reel_slug="phase41_opd_vs_grpo_prototype",
    )

    print("\n" + "=" * 80)
    print("PHASE 4.1 INTEGRATION RUN COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print(f"Topic:                 {result['topic_title']}")
    print(f"Primary Source:        {result['primary_source']}")
    print(f"Reel Slug:             {result['reel_slug']}")
    print(f"Final Video:           {result['video_path']}")
    print(f"Contact Sheet:         {result['contact_sheet_path']}")
    print(f"Master Audio:          {result['master_audio_path']}")
    print(f"Total Duration:        {result['duration_seconds']:.2f}s")
    print(f"Voice Profile:         {result['voice_profile']}")
    print(f"Approval Status:       {result['approval_status']}")
    print(f"Published:             {result['published']}")
    print(f"Verified Claims:       {result['verified_claims_count']}")
    print("=" * 80)
    print("Connectivity Map:")
    for component, connected in result["connectivity_map"].items():
        print(f"  - {component}: {'CONNECTED' if connected else 'DISCONNECTED'}")
    print("=" * 80)
    print("Mandatory Qualifications Enforced:")
    for q in result["mandatory_qualifications"]:
        print(f"  * {q}")
    print("=" * 80 + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
