"""
Upload sanitized DeepSeek-R1 documentary to YouTube (Private default).
Replaces any HTML-like angle brackets with brackets to comply with YouTube Data API v3.
"""

import sys
import json
from pathlib import Path

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from core.database import Database
from publishing.youtube_integration import YouTubeIntegration

PROD_DIR = WORKSPACE_ROOT / "output" / "drafts" / "deepseek_r1_documentary"
VIDEO_PATH = PROD_DIR / "deepseek_r1_master.mp4"

TITLE = "How DeepSeek-R1 Shook Silicon Valley: The Open-Source AI Revolution"

RAW_CAPTION = (
    "Ever wondered how a single open-source GitHub repository shook Silicon Valley and challenged trillion-dollar AI monopolies overnight?\n\n"
    "In this technical breakdown, explore the radical systems engineering behind DeepSeek-R1 and DeepSeek-V3:\n"
    "1. Pure Reinforcement Learning via GRPO — eliminating millions in expensive human labeling.\n"
    "2. Emergent Self-Correction — spontaneous 'Aha moments' inside explicit [think] tokens.\n"
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
    print("UPLOADING DEEPSEEK-R1 DOCUMENTARY TO YOUTUBE (Strictly Private)")
    print("=" * 80)

    db = Database()
    yt = YouTubeIntegration(db=db)

    # Sanitize description completely
    clean_desc = f"{RAW_CAPTION}\n\n{HASHTAGS}".replace("<", "[").replace(">", "]")

    res = yt.upload_video(
        video_path=VIDEO_PATH,
        title=TITLE,
        description=clean_desc,
        tags=TAGS,
        category_id="28",
        privacy_status="private",
        production_job_id=69,
        explicit_approval=True,
        synthetic_content_declared=True,
    )

    print("\n" + "=" * 80)
    print("YOUTUBE UPLOAD RESULT:")
    print("=" * 80)
    print(f"  Success:        {res.get('ok')}")
    print(f"  Video ID:       {res.get('video_id')}")
    print(f"  Direct Link:    https://youtu.be/{res.get('video_id')}")
    print(f"  Privacy Status: {res.get('privacy_status')}")
    print(f"  Title:          {res.get('title')}")
    print("=" * 80)

    # Update publishing manifest
    pub_manifest = PROD_DIR / "publishing_manifest.json"
    data = {}
    if pub_manifest.exists():
        with open(pub_manifest, "r", encoding="utf-8") as f:
            data = json.load(f)
    data["youtube"] = res
    with open(pub_manifest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

if __name__ == "__main__":
    main()
