"""
Reference Visual Engine for SUPER.INTELLIGENCEEE - Phase 5.
Directly implements the visual language, kinetic typography, isometric 3D models,
and evidence cards inspired by the reference benchmark video 'This is what i want.mp4'.
"""

from .kinetic_typography import (
    ReferenceKineticTypography,
    KineticWord,
)

from .isometric_3d import (
    IsometricVoxelCube,
    IsometricBarChart,
    IsometricHardwareModels,
    IsometricLayerStack,
    iso_project,
)

from .evidence_cards import (
    GitHubRepoCard,
    DocumentationFigureViewer,
    SideBySideComparisonCard,
)

from .charts_and_telemetry import (
    LollipopChart,
    FlatlineTelemetryCard,
    DigitalStopwatchTimer,
    MoEExpertGrid,
)

from .reference_compositions import (
    ReferenceIsometricHookComposition,
    ReferenceRepoEvidenceComposition,
    ReferenceBarChartComparisonComposition,
    ReferenceLayerStreamingComposition,
    ReferenceMoEMechanismComposition,
    ReferenceDeterminismComparisonComposition,
    ReferenceLatencyTimerComposition,
    ReferenceLoopConclusionComposition,
)

__all__ = [
    "ReferenceKineticTypography",
    "KineticWord",
    "IsometricVoxelCube",
    "IsometricBarChart",
    "IsometricHardwareModels",
    "IsometricLayerStack",
    "iso_project",
    "GitHubRepoCard",
    "DocumentationFigureViewer",
    "SideBySideComparisonCard",
    "LollipopChart",
    "FlatlineTelemetryCard",
    "DigitalStopwatchTimer",
    "MoEExpertGrid",
    "ReferenceIsometricHookComposition",
    "ReferenceRepoEvidenceComposition",
    "ReferenceBarChartComparisonComposition",
    "ReferenceLayerStreamingComposition",
    "ReferenceMoEMechanismComposition",
    "ReferenceDeterminismComparisonComposition",
    "ReferenceLatencyTimerComposition",
    "ReferenceLoopConclusionComposition",
]
