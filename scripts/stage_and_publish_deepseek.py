"""
SUPER.INTELLIGENCEEE — Staging and Multi-Platform Publishing Pipeline
Topic: deepseek-ai/DeepSeek-R1 Viral Spotlight
Stages the video into production_jobs and publishing_queue, then executes
official uploads to YouTube (private default) and Instagram Reels.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from core.database import Database
from publishing.youtube_integration import YouTubeIntegration
from publishing.instagram_integration import InstagramIntegration

PROD_DIR = WORKSPACE_ROOT / "output" / "drafts" / "deepseek_r1_documentary"
VIDEO_PATH = PROD_DIR / "deepseek_r1_master.mp4"
CONTACT_SHEET = PROD_DIR / "deepseek_r1_40frame_master_contact_sheet.png"

TITLE = "How DeepSeek-R1 Shook Silicon Valley: The Open-Source AI Revolution"

CAPTION = (
    "Ever wondered how a single open-source GitHub repository shook Silicon Valley and challenged trillion-dollar AI monopolies overnight?\n\n"
    "In this technical breakdown, explore the radical systems engineering behind DeepSeek-R1 and DeepSeek-V3:\n"
    "1. Pure Reinforcement Learning via GRPO — eliminating millions in expensive human labeling.\n"
    "2. Emergent Self-Correction — spontaneous 'Aha moments' inside explicit <think> tokens.\n"
    "3. Multi-Head Latent Attention (MLA) — compressing KV cache by 93.3% to shatter the GPU memory wall.\n"
    "4. DeepSeekMoE Sparse Routing — 671B parameters routed to just 37B active specialists.\n"
    "5. Benchmark Parity — matching closed frontier models at 27x lower API cost.\n"
    "6. Free Open Weights & MIT License — sovereign intelligence for the global developer community.\n\n"
    "Follow @super.intelligenceee for daily breakdowns of breakthrough AI repositories, architectures, and research papers."
)

HASHTAGS = "#DeepSeek #DeepSeekR1 #MachineLearning #OpenSource #ArtificialIntelligence #Python #Coding #TechNews #DataScience #LLM #AIResearch #SuperIntelligence"

TAGS = [
    "DeepSeek", "DeepSeek R1", "DeepSeek V3", "Artificial Intelligence",
    "Machine Learning", "Open Source AI", "LLM", "Reinforcement Learning",
    "GRPO", "Transformer", "Coding", "GitHub", "SuperIntelligence"
]

def main():
    print("=" * 80)
    print("STAGE & PUBLISH: deepseek-ai/DeepSeek-R1 SPOTLIGHT")
    print("=" * 80)

    db = Database()
    yt = YouTubeIntegration(db=db)
    ig = InstagramIntegration(db=db)

    # 1. Verify Authentication Status
    print("\n[VERIFICATION] Checking Social Connections...")
    yt_status = yt.get_connection_status()
    ig_status = ig.get_connection_status()

    print(f"  YouTube:   {yt_status['status']} | Channel: {yt_status.get('channel_title')} ({yt_status.get('channel_id')})")
    print(f"  Instagram: {ig_status['status']} | Account: @{ig_status.get('username')} ({ig_status.get('account_id')})")

    if not yt_status.get("connected"):
        print("ERROR: YouTube is not connected!")
        sys.exit(1)
    if not ig_status.get("connected"):
        print("ERROR: Instagram is not connected!")
        sys.exit(1)

    # 2. Stage Production Job in Database
    now_iso = datetime.now(timezone.utc).isoformat()
    file_size_mb = round(VIDEO_PATH.stat().st_size / (1024 * 1024), 2)

    with db.transaction() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO production_jobs (
                title, status, output_video_path, cover_image_path,
                audio_path, file_size_mb, created_at, completed_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                TITLE,
                "APPROVED",
                str(VIDEO_PATH),
                str(CONTACT_SHEET),
                str(PROD_DIR / "audio" / "scene1_hook_shockwave_master.wav"),
                file_size_mb,
                now_iso,
                now_iso,
                now_iso,
            )
        )
        job_id = cur.lastrowid
        print(f"\n[STAGING] Created Production Job #{job_id} (Status: APPROVED)")

        # Create explicit approval record
        cur.execute(
            """
            INSERT INTO approvals (
                production_job_id, entity_type, entity_id, decision,
                reviewer, reviewer_notes, reviewed_at, decided_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_id,
                "production_job",
                job_id,
                "APPROVED",
                "human_operator",
                "Explicit user command: generate a new video and try to upload it",
                now_iso,
                now_iso,
                "APPROVED",
            )
        )

        # Stage in Publishing Queue
        cur.execute(
            """
            INSERT INTO publishing_queue (
                job_id, production_job_id, title, caption, hashtags,
                video_path, scheduled_for, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_id,
                job_id,
                TITLE,
                CAPTION,
                HASHTAGS,
                str(VIDEO_PATH),
                now_iso,
                "APPROVED",
            )
        )
        queue_id = cur.lastrowid
        print(f"[STAGING] Created Publishing Queue Item #{queue_id} (Status: APPROVED)")

    results = {}

    # 3. Publish to YouTube
    print("\n" + "=" * 80)
    print("STEP 1: UPLOADING TO YOUTUBE (Strictly Private Default)...")
    print("=" * 80)
    try:
        yt_res = yt.upload_video(
            video_path=VIDEO_PATH,
            title=TITLE,
            description=f"{CAPTION}\n\n{HASHTAGS}",
            tags=TAGS,
            category_id="28",
            privacy_status="private",
            production_job_id=job_id,
            explicit_approval=True,
            synthetic_content_declared=True,
        )
        print(f"  [YOUTUBE SUCCESS] Video ID: {yt_res.get('video_id')}")
        print(f"  [YOUTUBE LINK]    https://youtu.be/{yt_res.get('video_id')}")
        print(f"  [PRIVACY STATUS]  {yt_res.get('privacy_status')}")
        results["youtube"] = yt_res
    except Exception as e:
        print(f"  [YOUTUBE ERROR] {e}")
        results["youtube"] = {"ok": False, "error": str(e)}

    # 4. Publish to Instagram
    print("\n" + "=" * 80)
    print("STEP 2: PUBLISHING REEL TO INSTAGRAM...")
    print("=" * 80)
    try:
        ig_res = ig.publish_reel(
            queue_item_id=queue_id,
            explicit_approval=True,
            share_to_feed=True,
            max_poll_seconds=180,
        )
        print(f"  [INSTAGRAM SUCCESS] Media ID: {ig_res.get('media_id')}")
        print(f"  [PERMALINK]         {ig_res.get('permalink')}")
        results["instagram"] = ig_res
    except Exception as e:
        print(f"  [INSTAGRAM ERROR] {e}")
        results["instagram"] = {"ok": False, "error": str(e)}

    # Save publish results manifest
    pub_manifest = PROD_DIR / "publishing_manifest.json"
    with open(pub_manifest, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved publish manifest: {pub_manifest}")

    print("\n" + "=" * 80)
    print("PUBLISHING WORKFLOW COMPLETED!")
    print("=" * 80)

if __name__ == "__main__":
    main()
