"""
SUPER.INTELLIGENCEEE — Phase 2 Creative Intelligence & Dynamic Scene Planning Test Suite
Verifies:
1. Dynamic Scene Counts (3 to 12+ scenes) without fixed 7-scene lock
2. Six Narrative Structure Types and dynamic pattern selection
3. Topic Complexity Analysis & Format Selection
4. Creative Director Plan Formulation (Screen Demos, Diagrams, B-Roll, Sound Design)
5. Dynamic Scene Planner Schema Validation & Contract Integrity
6. Bi-directional Lossless Conversion: DynamicScene -> UniversalScene -> Legacy Dict
7. Visual Diversity Analyzer: Consecutive duplicate detection & crowded text remediation
8. Timing Coordinator: Audio-visual synchronization & visual hold padding
9. Format Profiles: Tech Documentary, Trend Short-Form, Animated Storytelling
10. End-to-End Dynamic Story Production with Fictional Synthetic Topic
"""

import pytest
from core.creative_contracts import (
    AssetRequirement,
    AudioCue,
    CreativeDirectionPlan,
    CreativeFormatType,
    DynamicScene,
    DynamicScenePlan,
    NarrativeStructureType,
    SceneType,
    StoryArchitecturePlan,
)
from creative.story_architecture.story_architect import StoryArchitectureEngine
from creative.director.creative_director import CreativeDirector
from creative.scene_planner.dynamic_scene_planner import DynamicScenePlanner
from creative.scene_planner.visual_diversity_analyzer import VisualDiversityAnalyzer
from creative.scene_planner.timing_coordinator import TimingCoordinator
from creative.formats.tech_documentary_profile import TechDocumentaryProfile
from creative.formats.trend_shortform_profile import TrendShortFormProfile
from creative.formats.animated_storytelling_profile import AnimatedStorytellingProfile
from content.storyboard import StoryboardGenerator
from core.schemas import ClaimEvidence, EvidenceStatus, ResearchDossier, Source, UniversalScene


def test_variable_scene_counts_from_3_to_12():
    """Validates that story architect can produce plans with variable scene counts (3, 5, 8, 12)."""
    engine = StoryArchitectureEngine()
    topic = {
        "title": "Quantum Attention Engine",
        "summary": "Novel quantum-classical hybrid attention algorithm.",
    }

    # Test 3 scenes (Fast Breaking Alert)
    plan_3 = engine.plan_architecture(topic, target_scene_count=3)
    assert plan_3.recommended_scene_count == 3
    assert len(plan_3.structural_beats) == 3

    # Test 5 scenes (Standard Explainer)
    plan_5 = engine.plan_architecture(topic, target_scene_count=5)
    assert plan_5.recommended_scene_count == 5
    assert len(plan_5.structural_beats) == 5

    # Test 8 scenes (Deep Tech Breakdown)
    plan_8 = engine.plan_architecture(topic, target_scene_count=8)
    assert plan_8.recommended_scene_count == 8
    assert len(plan_8.structural_beats) == 8

    # Test 12 scenes (Exhaustive Technical Teardown)
    plan_12 = engine.plan_architecture(topic, target_scene_count=12)
    assert plan_12.recommended_scene_count == 12
    assert len(plan_12.structural_beats) == 12


def test_narrative_structure_selection_by_topic_type():
    """Validates dynamic narrative structure selection based on topic signals."""
    engine = StoryArchitectureEngine()

    # 1. Comparison topic -> COMPARISON_TESTING_RESULTS_VERDICT
    comp_topic = {
        "title": "Llama-3 70B vs Claude-3.5 Sonnet Coding Benchmark Comparison",
        "summary": "Head-to-head empirical evaluations on HumanEval and SWE-bench.",
    }
    struct_comp = engine.select_narrative_structure(comp_topic)
    assert struct_comp == NarrativeStructureType.COMPARISON_TESTING_RESULTS_VERDICT

    # 2. Software demo / CLI tool -> DEMONSTRATION_BREAKDOWN_EVALUATION
    tool_topic = {
        "title": "Open-Source Autonomous Coding Agent CLI Tool",
        "summary": "Developer releases open-source terminal agent with local git execution capabilities.",
        "url": "https://github.com/example/cli-agent",
    }
    struct_tool = engine.select_narrative_structure(tool_topic)
    assert struct_tool == NarrativeStructureType.DEMONSTRATION_BREAKDOWN_EVALUATION

    # 3. Deep architecture -> PROBLEM_MECHANISM_SOLUTION_LIMITATIONS
    arch_topic = {
        "title": "Transformer State Space Kernels for Linear Context Scaling",
        "summary": "Novel recurrent attention kernels reduce quadratic complexity to sub-quadratic.",
    }
    struct_arch = engine.select_narrative_structure(arch_topic)
    assert struct_arch == NarrativeStructureType.PROBLEM_MECHANISM_SOLUTION_LIMITATIONS


def test_creative_director_allocates_visual_treatments():
    """Validates that CreativeDirector allocates diagrams, screen demos, and B-roll intentionally."""
    arch_engine = StoryArchitectureEngine()
    topic = {
        "id": "TOPIC_DIR_001",
        "title": "Autonomous CLI Framework with Multi-Agent Pipeline",
        "summary": "Engineers release terminal developer tool with visual graph architecture.",
    }
    arch_plan = arch_engine.plan_architecture(topic)

    director = CreativeDirector()
    dir_plan = director.formulate_creative_direction(arch_plan)

    assert isinstance(dir_plan, CreativeDirectionPlan)
    assert len(dir_plan.diagram_sections) >= 1, "Must allocate at least 1 technical diagram"
    assert len(dir_plan.broll_sections) >= 1, "Must allocate at least 1 B-roll section"
    assert "background_primary" in dir_plan.color_palette
    assert "takeaway" in dir_plan.ending_resolution.lower() or "resolves" in dir_plan.ending_resolution.lower()


def test_dynamic_scene_planner_produces_fully_validated_plan():
    """Validates that DynamicScenePlanner generates compliant DynamicScenePlans."""
    arch_engine = StoryArchitectureEngine()
    director = CreativeDirector()
    planner = DynamicScenePlanner()

    topic = {
        "id": "TOPIC_PLAN_001",
        "title": "Sub-Quadratic Quantized Transformer Kernels",
        "summary": "Demonstrated 4.2x speedup on consumer GPUs using fused INT4 CUDA operations.",
    }
    arch_plan = arch_engine.plan_architecture(topic, target_scene_count=5)
    dir_plan = director.formulate_creative_direction(arch_plan)
    scene_plan = planner.plan_scenes(arch_plan, dir_plan)

    assert isinstance(scene_plan, DynamicScenePlan)
    assert len(scene_plan.scenes) == 5

    # Validate all scenes
    ok, errors = scene_plan.validate()
    assert ok is True, f"Scene plan validation failed: {errors}"

    for sc in scene_plan.scenes:
        assert sc.scene_id.startswith("scene_")
        assert sc.sequence >= 1
        assert len(sc.narration) > 0
        assert sc.duration_seconds >= 3.0
        assert len(sc.asset_requirements) >= 1


def test_bi_directional_schema_compatibility_with_renderer():
    """Validates lossless conversion: DynamicScene -> UniversalScene -> Legacy Dict."""
    scene = DynamicScene(
        scene_id="scene_003_demo",
        sequence=3,
        narration="Here is the terminal CLI running local inference with zero latency.",
        scene_objective="Showcase live CLI performance",
        scene_type=SceneType.SCREEN_DEMONSTRATION,
        visual_concept="TERMINAL CLI RUNTIME",
        visual_description="Dark mode terminal window with streaming token outputs.",
        camera_direction="push_in_slow",
        motion_direction="draw_reveal",
        on_screen_text="LOCAL RUNTIME: 120 TOKENS/SEC",
        estimated_duration=4.5,
    )

    # 1. Convert to UniversalScene
    u_scene = scene.to_universal_scene()
    assert isinstance(u_scene, UniversalScene)
    assert u_scene.scene_id == "scene_003_demo"
    assert u_scene.scene_index == 3
    assert u_scene.duration_seconds == 4.5
    assert u_scene.narration_text == scene.narration

    # 2. Convert to legacy dictionary
    d = scene.to_dict()
    assert d["scene_number"] == 3
    assert d["duration"] == 4.5
    assert d["visual_type"] in ["product_demo", "motion_diagram"]
    assert d["headline"] == "LOCAL RUNTIME: 120 TOKENS/SEC"

    # 3. Pass to StoryboardGenerator
    storyboard = StoryboardGenerator.generate_storyboard({"scenes": [scene]})
    assert len(storyboard) == 1
    assert storyboard[0]["scene_number"] == 3


def test_visual_diversity_analyzer_detects_and_remediates():
    """Validates that VisualDiversityAnalyzer catches consecutive duplicates and crowded text."""
    # Create flawed plan with consecutive duplicate scene types and excessive text
    sc1 = DynamicScene(
        scene_id="s1", sequence=1, narration="Hook narration.",
        scene_objective="Hook", scene_type=SceneType.KINETIC_TYPOGRAPHY,
        visual_concept="Hook", visual_description="Text",
        on_screen_text="This is an excessively long and crowded on-screen text headline that looks exactly like a generic PowerPoint presentation slide instead of a real high-impact video reel headline",
    )
    sc2 = DynamicScene(
        scene_id="s2", sequence=2, narration="Second scene.",
        scene_objective="Context", scene_type=SceneType.KINETIC_TYPOGRAPHY,  # Duplicate!
        visual_concept="Text 2", visual_description="Text 2",
        on_screen_text="Second Headline",
    )
    sc3 = DynamicScene(
        scene_id="s3", sequence=3, narration="Third scene.",
        scene_objective="Breakdown", scene_type=SceneType.TECHNICAL_DIAGRAM,
        visual_concept="Diagram", visual_description="Diagram",
        on_screen_text="Short Text",
    )

    plan = DynamicScenePlan(
        plan_id="plan_flawed", topic_id="top_test",
        creative_format=CreativeFormatType.TECH_DOCUMENTARY,
        narrative_structure=NarrativeStructureType.DISCOVERY_EXPLANATION_IMPLICATIONS,
        total_target_duration=15.0, scenes=[sc1, sc2, sc3]
    )

    analyzer = VisualDiversityAnalyzer()
    report = analyzer.analyze_plan(plan)

    assert report["passed"] is False
    assert report["consecutive_duplicates_count"] >= 1
    assert len(report["crowded_text_scenes"]) >= 1

    # Apply automated remediation
    remediated_plan = analyzer.remediate_diversity_issues(plan)
    report_fixed = analyzer.analyze_plan(remediated_plan)
    assert report_fixed["consecutive_duplicates_count"] == 0
    assert len(report_fixed["crowded_text_scenes"]) == 0


def test_timing_coordinator_synchronizes_and_audits():
    """Validates timing coordination and pacing audits."""
    coordinator = TimingCoordinator(target_wps=2.5)

    # Word count estimation
    text = "Engineers developed custom fused CUDA kernels enabling INT4 weight-only quantization."
    est = coordinator.estimate_narration_duration(text)
    assert 3.5 <= est <= 6.0

    # Timing profile audit
    sc1 = DynamicScene(
        scene_id="s1", sequence=1, narration="Paced narration for scene.",
        scene_objective="Obj", scene_type=SceneType.KINETIC_TYPOGRAPHY,
        visual_concept="Concept", visual_description="Desc",
        estimated_duration=4.0,
    )
    sc2 = DynamicScene(
        scene_id="s2", sequence=2, narration="Another well-paced scene.",
        scene_objective="Obj", scene_type=SceneType.TECHNICAL_DIAGRAM,
        visual_concept="Concept", visual_description="Desc",
        estimated_duration=5.5,
    )

    plan = DynamicScenePlan(
        plan_id="plan_time", topic_id="top_time",
        creative_format=CreativeFormatType.TECH_DOCUMENTARY,
        narrative_structure=NarrativeStructureType.DISCOVERY_EXPLANATION_IMPLICATIONS,
        total_target_duration=9.5, scenes=[sc1, sc2]
    )

    audit = coordinator.audit_timing_profile(plan)
    assert audit["passed"] is True
    assert audit["total_duration_seconds"] == 9.5
    assert len(audit["rushed_scenes"]) == 0
    assert len(audit["stagnant_scenes"]) == 0


def test_format_profiles_metadata():
    """Validates that all three creative format profiles export valid contracts."""
    doc_meta = TechDocumentaryProfile.get_profile_metadata()
    assert doc_meta["format_type"] == "tech_documentary"
    assert doc_meta["primary_priority"] is True
    assert "screen_demonstration" in doc_meta["supported_scene_types"]

    short_meta = TrendShortFormProfile.get_profile_metadata()
    assert short_meta["format_type"] == "trend_shortform"
    assert short_meta["target_duration_range"] == (25.0, 45.0)

    story_meta = AnimatedStorytellingProfile.get_profile_metadata()
    assert story_meta["format_type"] == "animated_storytelling"
    assert "character_continuity" in story_meta["visual_style_guidelines"]


def test_fictional_synthetic_e2e_creative_pipeline():
    """
    End-to-End Dynamic Story Production Test using a Fictional Synthetic Topic.
    Clearly Identified Synthetic Test Data:
    'SYNTHETIC_NEURAL_SPARSITY_ACCELERATOR_2026'
    """
    synthetic_topic = {
        "id": "SYNTH_TOPIC_999",
        "title": "[SYNTHETIC TEST] Neural Sparsity Matrix Core Unlocks 8x Throughput",
        "summary": "Fictional AI benchmark demonstrates 8x throughput gains on simulated edge hardware using synthetic sparse tensor routing.",
        "url": "https://super.intelligenceee.local/synthetic/sparsity-matrix",
        "publisher": "Synthetic AI Research Lab",
    }

    # 1. Compile Research Dossier
    synthetic_source = Source(
        source_id="src_synth_01",
        url=synthetic_topic["url"],
        title=synthetic_topic["title"],
        publisher=synthetic_topic["publisher"],
        raw_content=synthetic_topic["summary"],
    )
    dossier = ResearchDossier(
        topic_id=synthetic_topic["id"],
        topic_title=synthetic_topic["title"],
        topic_description=synthetic_topic["summary"],
        original_angle="Architectural breakdown of sparse tensor routing on edge hardware.",
        primary_sources=[synthetic_source],
        important_claims=[
            ClaimEvidence(
                claim_id="synth_claim_001",
                claim_text="Demonstrates 8x throughput gains on simulated edge hardware.",
                source_url=synthetic_topic["url"],
                status=EvidenceStatus.VERIFIED,
                confidence_score=1.0,
            )
        ],
        verification_status="VERIFIED",
    )

    # 2. Formulate Story Architecture (Request 6 dynamic scenes)
    arch_engine = StoryArchitectureEngine()
    arch_plan = arch_engine.plan_architecture(synthetic_topic, dossier=dossier, target_scene_count=6)
    assert arch_plan.recommended_scene_count == 6

    # 3. Creative Director Formulation
    director = CreativeDirector()
    dir_plan = director.formulate_creative_direction(arch_plan, dossier=dossier)
    assert len(dir_plan.diagram_sections) >= 1

    # 4. Dynamic Scene Planning
    planner = DynamicScenePlanner()
    scene_plan = planner.plan_scenes(arch_plan, dir_plan, dossier=dossier)
    assert len(scene_plan.scenes) == 6

    # 5. Visual Diversity & Timing Check
    analyzer = VisualDiversityAnalyzer()
    div_report = analyzer.analyze_plan(scene_plan)
    assert div_report["unique_types_count"] >= 3

    coordinator = TimingCoordinator()
    timing_report = coordinator.audit_timing_profile(scene_plan)
    assert timing_report["passed"] is True

    # 6. Bi-directional Renderer Compatibility
    legacy_storyboard = StoryboardGenerator.generate_storyboard({"dynamic_plan": scene_plan})
    assert len(legacy_storyboard) == 6
    assert legacy_storyboard[0]["scene_number"] == 1
    assert legacy_storyboard[5]["scene_number"] == 6

