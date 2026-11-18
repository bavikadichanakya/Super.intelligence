"""
Controlled test script to verify NativeMotionRenderer rendering of Scene 1, 2, and 3
with the light-first cinematic compositions.
"""

from pathlib import Path
import time
from core.universal_scene_contract import SceneType, UniversalSceneContract, RenderingEngine
from rendering.native_motion_engine.renderer import NativeMotionRenderer

def test_scene_renders():
    out_dir = Path("output/drafts/test_light_scenes").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    
    renderer = NativeMotionRenderer()
    
    # Scene 1: System Topology / Hardware Cluster
    s1 = UniversalSceneContract(
        scene_id="test_scene_01",
        sequence_number=1,
        scene_type=SceneType.ANIMATED_PROCESS,
        narrative_purpose="Compute Bottleneck & Infrastructure",
        visual_concept="ACCELERATOR UTILIZATION BOTTLENECK",
        audience_takeaway="IDLE ACCELERATOR COMPUTE",
        narration_text="Autonomous AI coding agents frequently leave high-performance accelerators idle during exploratory rollout loops.",
        mechanism_description="Animated 2D cluster topology displaying idle compute nodes alternating with agent command dispatch.",
        preferred_engine=RenderingEngine.NATIVE_MOTION,
        narration_duration_seconds=5.0,
        actual_duration_seconds=5.0,
        output_resolution=(1080, 1920),
        frame_rate=30,
    )
    
    # Scene 2: Sandbox Isolation Boundary & Scheduling Mechanism
    s2 = UniversalSceneContract(
        scene_id="test_scene_02",
        sequence_number=2,
        scene_type=SceneType.TECHNICAL_DIAGRAM,
        narrative_purpose="Isolation & Scheduling Mechanism",
        visual_concept="ISOLATED ZERO-TRUST EXECUTION BOUNDARY",
        audience_takeaway="RESTRICTED FILESYSTEM SANDBOX",
        narration_text="By implementing command-level queue scheduling, requests are interleaved across interconnected hardware nodes.",
        mechanism_description="Clear visual representation of isolated execution boundary, agent ingress requests, Zero-Trust restricted filesystem sandbox vs host control, hardware command interleaver.",
        preferred_engine=RenderingEngine.NATIVE_MOTION,
        narration_duration_seconds=5.0,
        actual_duration_seconds=5.0,
        output_resolution=(1080, 1920),
        frame_rate=30,
    )
    
    # Scene 3: Benchmark Verdict & Performance Synthesis
    s3 = UniversalSceneContract(
        scene_id="test_scene_03",
        sequence_number=3,
        scene_type=SceneType.KINETIC_TYPOGRAPHY,
        narrative_purpose="Performance & Engineering Implications",
        visual_concept="PERFORMANCE & SECURITY VERDICT",
        audience_takeaway="+105% DUTY CYCLE GAIN",
        narration_text="Crucially, private workspaces enforce strict security boundaries. Scalable agent architecture requires both hardware efficiency and verified security.",
        mechanism_description="Full-screen comparative benchmark visualizer comparing Baseline 38% vs Interleaved 78% GPU duty cycle, 2.05x gain, and 100% memory isolation.",
        preferred_engine=RenderingEngine.NATIVE_MOTION,
        narration_duration_seconds=5.0,
        actual_duration_seconds=5.0,
        output_resolution=(1080, 1920),
        frame_rate=30,
    )
    
    for s in [s1, s2, s3]:
        p = out_dir / f"{s.scene_id}.mp4"
        t0 = time.time()
        res = renderer.render_scene(s, p)
        dur = time.time() - t0
        print(f"Rendered {s.scene_id} -> {p.name} in {dur:.2f}s ({res.get('render_fps', 0):.1f} fps)")

if __name__ == "__main__":
    test_scene_renders()
