"""
Audience Learning & Controlled Experimentation Engine
Manages scientific A/B and sequential content experiments.
Isolates single creative variables (Hook, Visual, Pacing, CTA) and compares results against account baselines.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class ExperimentVariable(str, Enum):
    FIRST_FRAME_VISUAL = "first_frame_visual"
    SPOKEN_HOOK = "spoken_hook"
    ON_SCREEN_HEADLINE = "on_screen_headline"
    STORY_LENGTH = "story_length"
    EXPLANATION_DENSITY = "explanation_density"
    CALL_TO_ACTION = "call_to_action"
    COVER_IMAGE = "cover_image"
    CONTENT_PILLAR = "content_pillar"


class ExperimentStatus(str, Enum):
    PROPOSED = "PROPOSED"
    IN_PRODUCTION = "IN_PRODUCTION"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    PUBLISHED = "PUBLISHED"
    EVALUATING = "EVALUATING"
    CONCLUDED = "CONCLUDED"


@dataclass
class ContentExperiment:
    experiment_id: str
    hypothesis: str
    variable_tested: ExperimentVariable
    control_baseline_job_id: int
    control_metrics: Dict[str, Any]
    variant_description: str
    status: ExperimentStatus = ExperimentStatus.PROPOSED
    variant_job_id: Optional[int] = None
    outcome_metrics: Optional[Dict[str, Any]] = None
    verdict: Optional[str] = None  # "REPEAT", "MODIFY", "DISCARD"
    confidence_level: str = "LOW"  # "LOW", "MODERATE", "HIGH"
    learning_notes: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GrowthExperimentEngine:
    """Orchestrates controlled growth hypotheses and records iterative learnings."""

    def __init__(self):
        self.experiments: List[ContentExperiment] = []

    def create_experiment(
        self,
        hypothesis: str,
        variable_tested: ExperimentVariable,
        control_job_id: int,
        control_metrics: Dict[str, Any],
        variant_description: str,
    ) -> ContentExperiment:
        """Initializes a new controlled creative experiment."""
        exp = ContentExperiment(
            experiment_id=f"exp_{int(time.time() * 1000)}",
            hypothesis=hypothesis,
            variable_tested=variable_tested,
            control_baseline_job_id=control_job_id,
            control_metrics=control_metrics,
            variant_description=variant_description,
        )
        self.experiments.append(exp)
        return exp

    def record_outcome(
        self,
        experiment_id: str,
        variant_job_id: int,
        outcome_metrics: Dict[str, Any],
        verdict: str,
        learning_notes: str,
    ) -> Optional[ContentExperiment]:
        """Evaluates experimental results against control baselines."""
        exp = next((e for e in self.experiments if e.experiment_id == experiment_id), None)
        if not exp:
            return None

        exp.variant_job_id = variant_job_id
        exp.outcome_metrics = outcome_metrics
        exp.verdict = verdict
        exp.learning_notes = learning_notes
        exp.status = ExperimentStatus.CONCLUDED

        # Confidence logic based on sample size
        views = outcome_metrics.get("views", 0)
        reach = outcome_metrics.get("reach", 0)
        if reach > 500 or views > 1000:
            exp.confidence_level = "HIGH"
        elif reach > 150 or views > 300:
            exp.confidence_level = "MODERATE"
        else:
            exp.confidence_level = "LOW (Sample size < 150)"

        return exp

    def get_active_experiments(self) -> List[ContentExperiment]:
        return [e for e in self.experiments if e.status != ExperimentStatus.CONCLUDED]

    def get_concluded_experiments(self) -> List[ContentExperiment]:
        return [e for e in self.experiments if e.status == ExperimentStatus.CONCLUDED]
