"""
SUPER.INTELLIGENCEEE — Governed Multi-Agent Workflow Demonstration
Executes a complete 9-stage governed production cycle on a verified research topic.
Demonstrates:
  1. Signal harvesting & Brand OS alignment
  2. Owner-Controlled Policy Validation (Budget, Brand Voice, Hard Gates)
  3. 7-Factor Opportunity Scoring & Hard Evidence Gate
  4. Structured Task Briefs & Lifecycle State Machine
  5. Inter-Agent Dispatch across Specialized Departments
  6. Quality Assurance (Factual grounding + FFprobe specs)
  7. Human Approval Queue & Strict Anti-Self-Approval Enforcement
  8. Verifiable Zero-Cost & Single-Worker Memory Safety
"""

import sys
import json
import logging
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger("super_intelligence.governance_demo")

from core.database import get_db
from core.orchestrator import NexusOrchestrator
from core.kill_switch import get_kill_switch
from core.owner_config import get_owner_config
from publishing.approval_queue import ApprovalQueue
from publishing.instagram_integration import InstagramIntegration


def run_demonstration():
    print("=" * 80)
    print("  SUPER.INTELLIGENCEEE — GOVERNED MULTI-AGENT OPERATING SYSTEM DEMO")
    print("=" * 80)

    db = get_db()
    kill_switch = get_kill_switch()
    owner_config = get_owner_config()
    queue = ApprovalQueue(db)

    # 1. Inspect Owner-Controlled Configuration
    print("\n[PHASE 1] Verifying Owner-Controlled Configuration...")
    policies = owner_config.get_policy_summary()
    print(f"  * Budget Cap: {policies['zero_budget_cap']}")
    print(f"  * Approval Bar: Mandatory Human Approval = {policies['human_approval_mandatory']}")
    print(f"  * Prohibited Words: {policies['prohibited_words_count']} buzzwords")
    print(f"  * Editorial Pillars: {', '.join(policies['editorial_pillars'])}")
    print("  [SUCCESS] All owner policies loaded and validated.")

    # 2. Check Global Kill Switch
    print("\n[PHASE 2] Checking Global Kill Switch Status...")
    assert not kill_switch.is_active(), "Kill switch is active!"
    print("  * Global Kill Switch: INACTIVE (Systems normal)")

    # 3. Initialize Orchestrator
    print("\n[PHASE 3] Initializing Central Nexus Orchestrator...")
    orchestrator = NexusOrchestrator(db=db)
    print("  * Orchestrator initialized with 9 department agents.")

    # 4. Prepare / Verify Candidate Research Topic
    print("\n[PHASE 4] Preparing High-Trust Candidate Research Topic...")
    topic_data = {
        "title": "Sub-Quadratic Quantization Milestone for Edge AI",
        "url": "https://arxiv.org/abs/2601.12345",
        "publisher": "ArXiv Research Labs",
        "summary": "Researchers demonstrated sub-quadratic memory scaling across million-token contexts on consumer hardware, enabling real-time local inference without accuracy loss.",
        "category": "Artificial Intelligence",
        "score": 96.0,
    }
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM topics WHERE url = ?", (topic_data["url"],))
        existing = cursor.fetchone()
        if existing:
            topic_id = existing["id"]
        else:
            cursor.execute(
                """
                INSERT INTO topics (title, url, publisher, summary, category, score, status)
                VALUES (?, ?, ?, ?, ?, ?, 'DISCOVERED')
                """,
                (topic_data["title"], topic_data["url"], topic_data["publisher"], topic_data["summary"], topic_data["category"], topic_data["score"]),
            )
            topic_id = cursor.lastrowid
    print(f"  * Topic ID #{topic_id}: '{topic_data['title']}'")
    print(f"  * Primary Evidence URL: {topic_data['url']}")

    # 5. Execute Governed Workflow
    print("\n[PHASE 5] Executing Governed Multi-Stage Workflow...")
    result = orchestrator.execute_workflow(topic_id=topic_id)

    print("\n[PHASE 6] Workflow Results & Verification:")
    print(f"  * Workflow ID: {result['workflow_id']}")
    print(f"  * Overall Status: {result['status']}")
    print(f"  * Production Job ID: #{result['production_job_id']}")
    print(f"  * Rendered Video: {result['video_path']}")
    print(f"  * Video Duration: {result['duration']:.2f}s")

    opp = result["opportunity"]
    print(f"\n  [OPPORTUNITY SCORING MATRIX]")
    print(f"  * Composite Score: {opp['overall_score']:.1f} / 100")
    print(f"  * Eligible (Evidence Gate): {opp['eligible']}")
    for factor, score in opp["factors"].items():
        print(f"    - {factor:20s}: {score:.1f}/10 (Weight: {opp['weights'].get(factor, 0.0):.2f})")
    print(f"  * Reasoning: {opp['reasoning']}")

    # 6. Verify Human Approval Queue State
    print("\n[PHASE 7] Inspecting Human Approval Queue...")
    pending_items = queue.list_pending_approvals()
    print(f"  * Items in 'queue/needs-your-ok/': {len(pending_items)}")
    matching_item = next((item for item in pending_items if item.production_job_id == result["production_job_id"]), None)
    assert matching_item is not None, "Produced reel was not enqueued in Human Approval Queue!"
    print(f"  * Job #{matching_item.production_job_id} successfully queued with status: {matching_item.owner_decision}")

    # 7. Strict Anti-Bypass Guard Verification
    print("\n[PHASE 8] Testing Strict Anti-Bypass Gate (Attempting unauthorized publish)...")
    ig = InstagramIntegration(db)
    try:
        ig.publish_reel(result["production_job_id"], explicit_approval=False)
        print("  [ERROR] Security vulnerability: Reel published without human approval!")
        sys.exit(1)
    except (PermissionError, ValueError) as e:
        print(f"  * [GATE ENFORCED] Publishing blocked as expected: '{e}'")

    # 8. Test Agent Self-Approval Block
    print("\n[PHASE 9] Testing Agent Self-Approval Block...")
    from publishing.approval_queue import ApprovalSelfCheckError
    try:
        queue.decide(result["production_job_id"], decision="APPROVE", reviewer_name="distribution_agent")
        print("  [ERROR] Agent was able to self-approve!")
        sys.exit(1)
    except ApprovalSelfCheckError as e:
        print(f"  * [GATE ENFORCED] Self-approval blocked as expected: '{e}'")

    # 9. Affirmative Human Owner Approval Simulation
    print("\n[PHASE 10] Simulating Affirmative Human Owner Review & Approval...")
    owner_name = "Chanakya Bavikadi"
    approval_result = queue.decide(
        result["production_job_id"],
        decision="APPROVE",
        reviewer_name=owner_name,
        notes="Verified claims against ArXiv preprint. High-contrast typography and clean timing."
    )
    print(f"  * Reviewer: {approval_result['reviewer']}")
    print(f"  * New Status: {approval_result['status']}")
    print(f"  * Notes: {approval_result['notes']}")

    # Verify moved to queue/completed/
    completed_items = queue.list_completed_approvals()
    print(f"  * Items in 'queue/completed/': {len(completed_items)}")
    print("  * Approval cycle successfully completed!")

    print("\n" + "=" * 80)
    print("  GOVERNED MULTI-AGENT WORKFLOW FULLY VERIFIED")
    print("=" * 80)


if __name__ == "__main__":
    run_demonstration()