"""
SUPER.INTELLIGENCEEE — Phase 4.3.3.2 Native Motion Graphics Engine Package.
"""

from rendering.native_motion_engine.camera import CinematicCamera
from rendering.native_motion_engine.compositions import (
    BaseMotionComposition,
    CinematicEvidenceVerdictComposition,
    CloseUpMechanismComposition,
    EditorialVerdictComposition,
    ExplodedHardwareStackComposition,
    FullScreenArchitectureComposition,
    GenericMotionComposition,
    ProcessEntityTrackingComposition,
    SandboxIsolationComposition,
    SystemTopologyComposition,
)
from rendering.native_motion_engine.primitives import (
    counter_animation,
    fade_in,
    fade_out,
    get_progress,
    scale_in,
    slide_in,
)
from rendering.native_motion_engine.renderer import NativeMotionRenderer
from rendering.native_motion_engine.typography import SafeZone, TypographyEngine

__all__ = [
    "NativeMotionRenderer",
    "CinematicCamera",
    "BaseMotionComposition",
    "FullScreenArchitectureComposition",
    "CloseUpMechanismComposition",
    "ProcessEntityTrackingComposition",
    "ExplodedHardwareStackComposition",
    "CinematicEvidenceVerdictComposition",
    "SystemTopologyComposition",
    "SandboxIsolationComposition",
    "EditorialVerdictComposition",
    "GenericMotionComposition",
    "TypographyEngine",
    "SafeZone",
    "fade_in",
    "fade_out",
    "slide_in",
    "scale_in",
    "counter_animation",
    "get_progress",
]
