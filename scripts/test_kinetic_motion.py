"""
SUPER.INTELLIGENCEEE — Phase 3.5 Kinetic Typography & Motion Audit Test
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from creative.tech_documentary.kinetic_typography.kinetic_engine import KineticTypographyEngine
from rendering.motion_audit import MotionAuditor

def main():
    print("Testing Phase 3.5 Kinetic Engine & Motion Audit...")
    engine = KineticTypographyEngine()
    auditor = MotionAuditor()

    out_clip = Path("output/drafts/test_kinetic_motion.mp4")
    engine.render_kinetic_clip(
        output_path=out_clip,
        primary_text="SPECULATIVE DECODING ACCELERATION",
        highlight_keyword="SPECULATIVE",
        stat_number="3.2x",
        sub_text="Draft verifiers break autoregressive latency bottlenecks.",
        duration_seconds=4.0,
    )

    print(f"Clip rendered: {out_clip.exists()}, size: {out_clip.stat().st_size}")
    res = auditor.audit_video(out_clip, sample_interval=0.5, static_threshold_pct=0.35)
    print(f"Motion Audit Result: Mean Delta={res.mean_delta_pct}%, Max Static={res.static_hold_max_consecutive_seconds}s, Pass={res.motion_pass}")
    assert res.motion_pass, f"Motion audit failed! Max static = {res.static_hold_max_consecutive_seconds}s"
    print("KINETIC MOTION AUDIT PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

