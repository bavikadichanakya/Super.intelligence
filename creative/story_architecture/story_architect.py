"""
SUPER.INTELLIGENCEEE — Story Architecture Engine
Analyzes content briefs, research dossiers, and technical topics to select or synthesize
the optimal narrative structure, scene count (3 to 12+), and structural beats.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Optional

from core.creative_contracts import (
    CreativeFormatType,
    NarrativeStructureType,
    StoryArchitecturePlan,
)
from core.schemas import ContentBrief, ResearchDossier

logger = logging.getLogger("super_intelligence.story_architect")


class StoryArchitectureEngine:
    """Selects and formulates dynamic narrative structures based on topic complexity."""

    def __init__(self, config=None):
        self.config = config

    def analyze_topic_complexity(
        self, topic: Dict[str, Any], dossier: Optional[ResearchDossier] = None
    ) -> Dict[str, Any]:
        """Evaluates topic complexity, density, and evidence metrics."""
        title = topic.get("title", "").lower()
        summary = topic.get("summary", "").lower()
        full_text = f"{title} {summary}"

        claims_count = len(dossier.important_claims) if dossier else 2
        uncertainties_count = len(dossier.uncertainties) if dossier else 1

        is_benchmark_comparison = any(kw in full_text for kw in ["vs", "benchmark", "comparison", "outperforms", "beats"])
        is_software_demo = any(kw in full_text for kw in ["github", "tool", "library", "sdk", "agent", "framework", "cli", "demo", "repo"])
        is_deep_architecture = any(kw in full_text for kw in ["architecture", "transformer", "attention", "quantization", "kernel", "state space", "moe", "pruning"])
        is_breaking_news = any(kw in full_text for kw in ["breaking", "launches", "unveiled", "announces", "released"])

        # Estimate complexity on 1 to 5 scale
        complexity_score = 3
        if is_deep_architecture:
            complexity_score += 1
        if claims_count > 3:
            complexity_score += 1
        if is_breaking_news and not is_deep_architecture:
            complexity_score = 2

        return {
            "complexity_score": min(5, complexity_score),
            "is_benchmark_comparison": is_benchmark_comparison,
            "is_software_demo": is_software_demo,
            "is_deep_architecture": is_deep_architecture,
            "is_breaking_news": is_breaking_news,
            "claims_count": claims_count,
            "uncertainties_count": uncertainties_count,
        }

    def select_narrative_structure(
        self,
        topic: Dict[str, Any],
        dossier: Optional[ResearchDossier] = None,
        brief: Optional[ContentBrief] = None,
    ) -> NarrativeStructureType:
        """Determines the appropriate narrative structure."""
        if brief and brief.narrative_structure:
            try:
                return NarrativeStructureType(brief.narrative_structure)
            except ValueError:
                pass

        metrics = self.analyze_topic_complexity(topic, dossier)

        if metrics["is_benchmark_comparison"]:
            return NarrativeStructureType.COMPARISON_TESTING_RESULTS_VERDICT
        elif metrics["is_software_demo"]:
            return NarrativeStructureType.DEMONSTRATION_BREAKDOWN_EVALUATION
        elif metrics["is_deep_architecture"]:
            return NarrativeStructureType.PROBLEM_MECHANISM_SOLUTION_LIMITATIONS
        elif metrics["is_breaking_news"]:
            return NarrativeStructureType.DISCOVERY_EXPLANATION_IMPLICATIONS
        else:
            return NarrativeStructureType.QUESTION_INVESTIGATION_EVIDENCE_CONCLUSION

    def plan_architecture(
        self,
        topic: Dict[str, Any],
        dossier: Optional[ResearchDossier] = None,
        brief: Optional[ContentBrief] = None,
        target_scene_count: Optional[int] = None,
    ) -> StoryArchitecturePlan:
        """
        Formulates the complete StoryArchitecturePlan with dynamic scene beats.
        Scene count is driven by the topic and narrative structure (3 to 12+).
        """
        topic_id = str(topic.get("id", "top_001"))
        title = topic.get("title", "AI Technical Milestone")
        structure = self.select_narrative_structure(topic, dossier, brief)

        # Determine creative format
        if brief and brief.creative_engine:
            try:
                format_type = CreativeFormatType(brief.creative_engine)
            except ValueError:
                format_type = CreativeFormatType.TECH_DOCUMENTARY
        elif dossier and dossier.suggested_creative_format:
            try:
                format_type = CreativeFormatType(dossier.suggested_creative_format)
            except ValueError:
                format_type = CreativeFormatType.TECH_DOCUMENTARY
        else:
            format_type = CreativeFormatType.TECH_DOCUMENTARY

        # Generate narrative beats based on selected structure
        beats = []
        if structure == NarrativeStructureType.DISCOVERY_EXPLANATION_IMPLICATIONS:
            # 3 to 4 beats: Breaking or fast development
            beats = [
                {"role": "HOOK_ALERT", "beat_name": "Breaking Discovery", "target_pct": 0.20, "objective": "State the development and why it matters immediately."},
                {"role": "TECHNICAL_EXPLANATION", "beat_name": "Core Mechanism", "target_pct": 0.40, "objective": "Explain what changed and how it functions."},
                {"role": "IMPLICATIONS", "beat_name": "Real-World Impact", "target_pct": 0.25, "objective": "Detail practical takeaways for builders."},
                {"role": "VERDICT", "beat_name": "Summary Verdict", "target_pct": 0.15, "objective": "Provide memorable closing context."},
            ]
        elif structure == NarrativeStructureType.PROBLEM_MECHANISM_SOLUTION_LIMITATIONS:
            # 5 to 6 beats: Deep architecture
            beats = [
                {"role": "HOOK", "beat_name": "The Core Challenge", "target_pct": 0.15, "objective": "Identify the existing engineering bottleneck or compute ceiling."},
                {"role": "PROBLEM_CONTEXT", "beat_name": "Why Prior Approaches Failed", "target_pct": 0.18, "objective": "Explain why legacy methods hit latency or VRAM barriers."},
                {"role": "MECHANISM", "beat_name": "Architectural Innovation", "target_pct": 0.25, "objective": "Unpack the technical solution, algorithm, or kernel design."},
                {"role": "SOLUTION_BENCHMARK", "beat_name": "Empirical Results", "target_pct": 0.18, "objective": "Show verified benchmark metrics and performance speedups."},
                {"role": "LIMITATIONS", "beat_name": "Reality Check & Caveats", "target_pct": 0.14, "objective": "Highlight edge cases, hardware constraints, and trade-offs."},
                {"role": "TAKEAWAY", "beat_name": "Builder Implication", "target_pct": 0.10, "objective": "Deliver concrete actionable insight."},
            ]
        elif structure == NarrativeStructureType.DEMONSTRATION_BREAKDOWN_EVALUATION:
            # 5 beats: Software & Tooling
            beats = [
                {"role": "HOOK_DEMO", "beat_name": "Live Demonstration Tease", "target_pct": 0.20, "objective": "Show the tool running in real time."},
                {"role": "SYSTEM_OVERVIEW", "beat_name": "What It Does", "target_pct": 0.20, "objective": "Clarify inputs, outputs, and interface."},
                {"role": "TECHNICAL_BREAKDOWN", "beat_name": "How It Was Built", "target_pct": 0.25, "objective": "Explain internal data pipelines or model routing."},
                {"role": "BENCHMARK_EVALUATION", "beat_name": "Stress Test & Performance", "target_pct": 0.20, "objective": "Audit speed, accuracy, and failure modes."},
                {"role": "RESOURCES", "beat_name": "How to Run Locally", "target_pct": 0.15, "objective": "Provide repo details, dependencies, and setup notes."},
            ]
        elif structure == NarrativeStructureType.COMPARISON_TESTING_RESULTS_VERDICT:
            # 5 to 6 beats: Model vs Model
            beats = [
                {"role": "HOOK_MATCHUP", "beat_name": "The Head-to-Head", "target_pct": 0.18, "objective": "Frame the comparison between two models or techniques."},
                {"role": "METHODOLOGY", "beat_name": "Testing Parameters", "target_pct": 0.20, "objective": "Define hardware, dataset, and evaluation metrics."},
                {"role": "ROUND_ONE_RESULTS", "beat_name": "Speed & Latency Test", "target_pct": 0.22, "objective": "Compare throughput and resource consumption."},
                {"role": "ROUND_TWO_RESULTS", "beat_name": "Reasoning & Accuracy Test", "target_pct": 0.22, "objective": "Evaluate output quality and hallucination rates."},
                {"role": "VERDICT", "beat_name": "Final Engineering Verdict", "target_pct": 0.18, "objective": "Declare which solution fits which production use case."},
            ]
        elif structure == NarrativeStructureType.HISTORICAL_BREAKTHROUGH_CURRENT_FUTURE:
            # 6 to 8 beats: Comprehensive Deep Tech Explainer
            beats = [
                {"role": "HOOK", "beat_name": "Frontier Milestone", "target_pct": 0.12, "objective": "Hook audience with latest major breakthrough."},
                {"role": "HISTORICAL_CONTEXT", "beat_name": "The Origin Point", "target_pct": 0.14, "objective": "Recall where the technology started and earlier limits."},
                {"role": "BREAKTHROUGH_MOMENT", "beat_name": "The Turning Point", "target_pct": 0.18, "objective": "Explain the key theoretical or empirical pivot."},
                {"role": "TECHNICAL_DETAILS", "beat_name": "Deep Dive Mechanics", "target_pct": 0.20, "objective": "Diagram the modern implementation."},
                {"role": "CURRENT_BENCHMARKS", "beat_name": "State of the Art Today", "target_pct": 0.16, "objective": "Present verified production numbers."},
                {"role": "FUTURE_TRAJECTORY", "beat_name": "Where This Goes Next", "target_pct": 0.20, "objective": "Analyze emerging implications for the next 12-24 months."},
            ]
        else:
            # Question -> Investigation -> Evidence -> Conclusion (4 beats)
            beats = [
                {"role": "CORE_QUESTION", "beat_name": "The Central Mystery", "target_pct": 0.22, "objective": "Pose the key technical question."},
                {"role": "INVESTIGATION", "beat_name": "Testing the Hypothesis", "target_pct": 0.28, "objective": "Investigate the underlying claims and code."},
                {"role": "EVIDENCE", "beat_name": "Empirical Proof", "target_pct": 0.30, "objective": "Examine the verified data and primary sources."},
                {"role": "CONCLUSION", "beat_name": "Final Answer", "target_pct": 0.20, "objective": "Deliver clear answer with evidence-backed conclusion."},
            ]

        # Override or adjust scene count if requested
        if target_scene_count and 3 <= target_scene_count <= 12 and target_scene_count != len(beats):
            # Scale or subdivide beats to match target
            if target_scene_count > len(beats):
                # Expand core technical beat into multiple detailed steps
                extra = target_scene_count - len(beats)
                for e in range(extra):
                    insert_idx = min(len(beats) - 1, 2 + e)
                    beats.insert(insert_idx, {
                        "role": f"DEEP_DIVE_PART_{e+1}",
                        "beat_name": f"Detailed Technical Phase {e+1}",
                        "target_pct": round(1.0 / target_scene_count, 2),
                        "objective": f"In-depth analysis of sub-component #{e+1}",
                    })
            elif target_scene_count < len(beats):
                # Consolidate beats
                beats = beats[:target_scene_count]

        # Normalize target percentages
        total_pct = sum(b["target_pct"] for b in beats)
        for b in beats:
            b["target_pct"] = round(b["target_pct"] / total_pct, 3)

        target_duration = float(brief.suggested_duration_seconds) if brief else 58.0

        plan = StoryArchitecturePlan(
            architecture_id=f"arch_{str(uuid.uuid4())[:8]}",
            topic_id=topic_id,
            topic_title=title,
            narrative_structure=structure,
            selected_creative_format=format_type,
            recommended_scene_count=len(beats),
            target_duration_seconds=target_duration,
            structural_beats=beats,
            rationale=f"Selected {structure.value} based on topic complexity metrics ({len(beats)} scenes).",
        )

        logger.info(f"Formulated StoryArchitecturePlan [{plan.architecture_id}]: {structure.value} with {len(beats)} scenes.")
        return plan

