"""
SUPER.INTELLIGENCEEE — Content Intelligence, Viral Pattern Analysis & Audience Growth Engine
Core module orchestrating editorial identity, content pillars, ideation, hook generation,
platform packaging, analytics diagnosis, and evidence-based audience learning.
"""

from .audience_intelligence import AudienceIntelligence, TargetAudience, EditorialIdentity
from .content_pillars import ContentPillarsManager, ContentPillar
from .ideation_engine import ContentIdeationEngine, IdeaCandidate, ContentAngle
from .hook_intelligence import HookIntelligenceEngine, HookArchetype, ThreeLayerHook
from .opening_quality_gate import OpeningQualityGate, OpeningConcept, OpeningConceptType
from .story_intelligence import StoryIntelligenceEngine, StorySection, NarrativeStructure
from .platform_packaging import PlatformPackagingEngine, PlatformPackage
from .performance_diagnostics import (
    ContentPerformanceDiagnostics,
    DiagnosticReport,
    AccountBaselineCalculator,
    OFFICIAL_METRIC_DEFINITIONS,
    CAUSATION_DISCLAIMER,
)
from .experiment_engine import GrowthExperimentEngine, ContentExperiment

__all__ = [
    "AudienceIntelligence",
    "TargetAudience",
    "EditorialIdentity",
    "ContentPillarsManager",
    "ContentPillar",
    "ContentIdeationEngine",
    "IdeaCandidate",
    "ContentAngle",
    "HookIntelligenceEngine",
    "HookArchetype",
    "ThreeLayerHook",
    "OpeningQualityGate",
    "OpeningConcept",
    "OpeningConceptType",
    "StoryIntelligenceEngine",
    "StorySection",
    "NarrativeStructure",
    "PlatformPackagingEngine",
    "PlatformPackage",
    "ContentPerformanceDiagnostics",
    "DiagnosticReport",
    "AccountBaselineCalculator",
    "OFFICIAL_METRIC_DEFINITIONS",
    "CAUSATION_DISCLAIMER",
    "GrowthExperimentEngine",
    "ContentExperiment",
]
