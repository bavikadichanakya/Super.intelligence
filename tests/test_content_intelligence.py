"""
Test Suite for Content Intelligence Engine (Phase 12)
Validates audience intelligence, pillars, ideation, hook linter, story arcs,
platform packaging, diagnostics, experiments, and database telemetry.
"""

import pytest
from core.content_intelligence.audience_intelligence import AudienceIntelligence
from core.content_intelligence.content_pillars import ContentPillarsManager
from core.content_intelligence.ideation_engine import ContentIdeationEngine
from core.content_intelligence.hook_intelligence import HookIntelligenceEngine, HookArchetype
from core.content_intelligence.story_intelligence import StoryIntelligenceEngine
from core.content_intelligence.platform_packaging import PlatformPackagingEngine
from core.content_intelligence.performance_diagnostics import ContentPerformanceDiagnostics, FailureMode
from core.content_intelligence.experiment_engine import GrowthExperimentEngine, ExperimentVariable, ExperimentStatus
from core.database import Database


@pytest.fixture
def db():
    database = Database()
    return database


def test_audience_intelligence_editorial_alignment():
    ai = AudienceIntelligence()
    
    # Negative test: Generic news aggregation without mechanism
    bad_res = ai.evaluate_editorial_alignment(
        topic="Company announced today a new AI that might release soon",
        core_mechanism="They just posted a press release."
    )
    assert bad_res["aligned"] is False
    assert "Failed" in bad_res["reason"]
    
    # Positive test: Concrete engineering mechanism
    good_res = ai.evaluate_editorial_alignment(
        topic="DeepSeek R1 GRPO Reasoning",
        core_mechanism="Trained purely via reinforcement learning with rule-based reward verifiers without human demonstrations."
    )
    assert good_res["aligned"] is True
    assert "Passed" in good_res["reason"]
    assert "Every video must teach" in good_res["audience_promise"]


def test_content_pillars_classification():
    manager = ContentPillarsManager()
    pillars = manager.pillars
    assert len(pillars) == 4
    
    assert "open_frontier" in pillars
    assert "autonomous_systems" in pillars
    assert "hardware_physics" in pillars
    assert "systems_security" in pillars
    
    # Verify semantic taxonomy routing
    p_open = manager.route_topic_to_pillar("DeepSeek R1 Open Weights", ["llama", "qwen", "weights"])
    assert p_open.pillar_id == "open_frontier"
    
    p_agent = manager.route_topic_to_pillar("Browser Automation Swarm", ["agent", "mcp", "workflow"])
    assert p_agent.pillar_id == "autonomous_systems"
    
    p_hw = manager.route_topic_to_pillar("Blackwell Memory Bandwidth Wall", ["hbm", "gpu", "chip", "semiconductor"])
    assert p_hw.pillar_id == "hardware_physics"
    
    p_sec = manager.route_topic_to_pillar("Indirect Prompt Injection Jailbreak", ["security", "exploit", "cve"])
    assert p_sec.pillar_id == "systems_security"


def test_ideation_5_angle_generator():
    engine = ContentIdeationEngine()
    topic = "FlashAttention 3"
    breakthrough = "Eliminates memory roundtrips between GPU SRAM and HBM by tiling matrix multiplication."
    counter_status = "Naive attention required quadratic HBM reads and writes."
    takeaway = "FlashAttention is now standard in PyTorch 2.5."
    
    angles = engine.generate_angles_for_topic(
        topic=topic,
        technical_breakthrough=breakthrough,
        counter_status_quo=counter_status,
        practical_takeaway=takeaway,
    )
    assert len(angles) == 5
    
    angle_types = {a.angle_type for a in angles}
    assert "contrast" in angle_types
    assert "mechanical" in angle_types
    assert "financial_disruption" in angle_types
    assert "practical_laptop" in angle_types
    assert "uncomfortable_truth" in angle_types
    
    # Test backlog storage
    candidate = engine.add_to_backlog(
        topic_title=topic,
        content_pillar="hardware_physics",
        source_attribution="Tri Dao et al.",
        source_url="https://arxiv.org/abs/2407.08608",
        technical_breakthrough=breakthrough,
        counter_status_quo=counter_status,
        practical_takeaway=takeaway,
        priority_score=9.2,
        is_time_sensitive=False,
    )
    assert candidate.priority_score == 9.2
    assert len(engine.get_ranked_backlog()) == 1


def test_hook_intelligence_3_layer_standard_and_linter():
    hi = HookIntelligenceEngine()
    
    # Test Anti-Pattern Linter on rhetorical question
    rhetorical_hook = "Ever wondered how this crazy new AI works?"
    score1, warnings1 = hi.lint_spoken_hook(rhetorical_hook)
    assert score1 < 0.6
    assert any("Rhetorical question" in w for w in warnings1)
    
    # Test Anti-Pattern Linter on throat clearing
    throat_hook = "In this video today we are going to look at models."
    score2, warnings2 = hi.lint_spoken_hook(throat_hook)
    assert score2 < 0.7
    assert any("Throat-clearing" in w for w in warnings2)
    
    # Clean Hook
    clean_hook = "Silicon Valley spent billions on human data. This open repo beat them with pure math."
    clean_score, clean_warnings = hi.lint_spoken_hook(clean_hook)
    assert clean_score >= 0.95
    assert len(clean_warnings) == 0
    
    # Test 8-Archetype Batch Generation
    batch = hi.generate_hook_batch(
        topic="DeepSeek-R1",
        hero_metric="93% lower VRAM footprint",
        incumbent_entity="OpenAI o1",
        technical_mechanism="pure reinforcement learning and latent attention compression",
        practical_result="runs natively on consumer hardware at 40 tokens per second",
    )
    assert len(batch) == 8, "Must generate exactly 8 distinct archetyped hooks"
    
    for hook in batch:
        # Layer 1: Visual hook non-empty
        assert len(hook.first_frame_visual.strip()) > 10
        # Layer 2: Spoken line defined
        assert len(hook.spoken_opening_line.strip()) > 10
        # Layer 3: On-screen text defined
        assert len(hook.on_screen_headline.strip()) > 3
        # Curiosity gap and archetype present
        assert len(hook.curiosity_gap.strip()) > 5
        assert isinstance(hook.archetype, HookArchetype)


def test_story_intelligence_retention_arc():
    si = StoryIntelligenceEngine()
    arc = si.build_narrative_arc(
        topic="BitNet 1.58b 1-Bit LLMs",
        hook_spoken="Every GPU running AI is doing pointless floating-point math.",
        hook_visual="High-contrast kinetic matrix dropping FP16 floats into ternary states {-1, 0, 1}.",
        hook_text="1-BIT LLMS EXPLAINED",
        escalation_tension="Modern data centers are running out of electricity because FP16 multipliers consume massive watts.",
        technical_revelation="Ternary weights (-1, 0, 1) eliminate matrix multiplication entirely, turning compute into pure addition.",
        empirical_evidence="82% latency drop on ARM silicon with zero degradation in reasoning benchmarks.",
        practical_payoff="AI inference shifts from $40,000 servers to $50 microcontrollers.",
        share_persona="systems programmers and hardware engineers",
        cta_instruction="Link to the open BitNet C++ runtime in description.",
        total_duration=45.0,
    )
    
    assert len(arc.sections) == 6
    stage_names = [s.section_name for s in arc.sections]
    assert stage_names == [
        "hook",
        "escalation",
        "technical_revelation",
        "evidence",
        "payoff",
        "cta",
    ]
    assert arc.total_target_duration == 45.0
    assert (arc.sections[0].target_end_sec - arc.sections[0].target_start_sec) <= 4.5, "Hook section must stay within the first 4.5 seconds"


def test_platform_packaging_engine():
    engine = PlatformPackagingEngine()
    
    # YouTube Package
    yt = engine.package_for_youtube_shorts(
        topic="DeepSeek R1",
        hook_headline="How Pure RL Beat Closed AI",
        first_frame_action="Split-screen terminal showing loss curves and VRAM memory",
        breakthrough_summary="Trained with Group Relative Policy Optimization (GRPO) without human demonstrations.",
        niche_tags=["MachineLearning", "DeepSeek", "Coding"],
    )
    assert yt.platform == "youtube_shorts"
    assert len(yt.title_or_headline) <= 65
    assert "#Shorts" in yt.hashtags
    assert "#Shorts" in yt.caption_body
    
    # Instagram Package
    ig = engine.package_for_instagram_reels(
        topic="DeepSeek R1",
        core_insight="Pure RL eliminated human annotation bottlenecks.",
        first_frame_action="High-contrast benchmark leaderboard comparing R1 to o1",
        target_persona="AI engineer",
        breakthrough_bullets=[
            "GRPO replaces expensive PPO critic networks.",
            "Multi-head latent attention compresses KV cache by 90%.",
            "Zero supervised demonstration data needed for math reasoning."
        ],
        niche_tags=["deeplearning", "opensource", "coding", "tech"],
    )
    assert ig.platform == "instagram_reels"
    assert len(ig.hashtags) <= 5
    assert ig.caption_body.startswith(ig.caption_first_line)


def test_performance_diagnostics_engine():
    diag = ContentPerformanceDiagnostics()
    
    # Test Case 1: Instagram Hook Cliff (Job #69 empirical: 70.5% skip rate)
    res_cliff = diag.diagnose_instagram_reel(
        media_id="17982638913132487",
        views=134,
        reach=121,
        skip_rate=70.5,
        avg_watch_time_sec=4.53,
        shares=0,
        saves=0,
        likes=2,
        total_duration_sec=74.0,
    )
    assert res_cliff.failure_mode == FailureMode.HOOK_CLIFF
    assert res_cliff.confidence >= 0.90
    assert "Hook Cliff" in res_cliff.headline_diagnosis
    assert "rhetorical question" in res_cliff.actionable_fix_next_video.lower()
    
    # Test Case 2: YouTube Shorts Distribution Blocked (Job #69 empirical: private status)
    res_blocked = diag.diagnose_youtube_short(
        video_id="p_2bfJK-nBQ",
        view_count=3,
        like_count=1,
        privacy_status="private",
        duration_sec=74.0,
    )
    assert res_blocked.failure_mode == FailureMode.DISTRIBUTION_BLOCKED
    assert "Distribution Blocked" in res_blocked.headline_diagnosis
    assert "private" in res_blocked.root_cause_explanation.lower()
    
    # Test Case 3: Instagram Low Shareability (High reach, zero DMs)
    res_shares = diag.diagnose_instagram_reel(
        media_id="17982638913139999",
        views=1500,
        reach=1200,
        skip_rate=35.0,
        avg_watch_time_sec=28.0,
        shares=0,
        saves=12,
        likes=85,
        total_duration_sec=45.0,
    )
    assert res_shares.failure_mode == FailureMode.LOW_SHAREABILITY
    assert "Zero DM Shares" in res_shares.headline_diagnosis


def test_growth_experiment_engine():
    engine = GrowthExperimentEngine()
    
    # Create experiment
    exp = engine.create_experiment(
        hypothesis="Replacing static title card with Frame 0 kinetic benchmark motion drops Instagram skip rate below 40%.",
        variable_tested=ExperimentVariable.FIRST_FRAME_VISUAL,
        control_job_id=69,
        control_metrics={"skip_rate": 70.5, "views": 134, "avg_watch_time": 4.53},
        variant_description="High-contrast animated GRPO reward curve in Frame 0 with spoken line starting at 0.15s.",
    )
    assert exp.status == ExperimentStatus.PROPOSED
    assert len(engine.get_active_experiments()) == 1
    
    # Record outcome
    concluded = engine.record_outcome(
        experiment_id=exp.experiment_id,
        variant_job_id=70,
        outcome_metrics={"skip_rate": 34.2, "views": 1250, "reach": 1100, "avg_watch_time": 28.5},
        verdict="REPEAT",
        learning_notes="Kinetic Frame 0 benchmark motion halved the skip rate from 70.5% to 34.2%. Standardize across all Pillar 1 videos.",
    )
    assert concluded is not None
    assert concluded.status == ExperimentStatus.CONCLUDED
    assert concluded.verdict == "REPEAT"
    assert len(engine.get_concluded_experiments()) == 1


def test_database_telemetry_persistence(db):
    # Create production job to satisfy foreign key constraint
    job_id = db.create_production_job(None, "Phase 12 Telemetry Verification Test")
    assert job_id > 0

    # Record performance snapshot in SQLite
    snap_data = {
        "production_job_id": job_id,
        "platform": "instagram",
        "platform_media_id": f"test_media_{job_id}",
        "title": "DeepSeek R1 GRPO Breakdown",
        "topic": "DeepSeek R1",
        "content_pillar": "open_frontier",
        "hook_archetype": "contrarian_shock",
        "hook_script": "Everything told about AI reasoning is wrong.",
        "video_length": 45.0,
        "views": 250,
        "reach": 240,
        "likes": 15,
        "shares": 5,
        "saves": 8,
        "skip_rate": 32.5,
        "avg_watch_time": 28.4,
        "retention_pct": 63.1,
    }
    snap_id = db.save_performance_snapshot(snap_data)
    assert snap_id > 0
    
    # Query snapshot
    snapshots = db.get_performance_snapshots(limit=5)
    assert len(snapshots) > 0
    matched = [s for s in snapshots if s["platform_media_id"] == f"test_media_{job_id}"]
    assert len(matched) == 1
    assert matched[0]["views"] == 250
    assert matched[0]["skip_rate"] == 32.5
    
    # Test experiment tracking in SQLite
    exp_data = {
        "experiment_id": "exp_test_persistence_001",
        "hypothesis": "Testing kinetic first-frame vs static slide",
        "variable_tested": "first_frame_visual",
        "control_job_id": 69,
        "control_metrics": {"skip_rate": 70.5},
        "variant_description": "Frame 0 animated benchmark graph",
        "status": "VALIDATED",
        "variant_job_id": 70,
        "outcome_metrics": {"skip_rate": 34.2},
        "verdict": "REPEAT",
        "learning_notes": "Kinetic first-frame reduced skip rate by more than half.",
    }
    exp_id = db.save_experiment(exp_data)
    assert exp_id > 0
    
    experiments = db.get_experiments(status="VALIDATED")
    exp_match = [e for e in experiments if e["experiment_id"] == "exp_test_persistence_001"]
    assert len(exp_match) == 1
    assert exp_match[0]["status"] == "VALIDATED"
    assert exp_match[0]["verdict"] == "REPEAT"
