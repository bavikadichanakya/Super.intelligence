"""
SUPER.INTELLIGENCEEE — Phase 3.5 Production Runner
Produces the complete Phase 3.5 Technology Documentary:
- Topic: Speculative Decoding: Breaking the Autoregressive Memory Wall
- Narration: General American English Male (am_liam via Voicebox Kokoro)
- Sound Design: Continuous 6-Act Adaptive Electronic Score + Automated Sidechain Ducking + Event-Driven SFX
- Visual Design: Light-First Swiss Editorial (Ivory canvas, zero dark cards, staggered typography reveals)
- Dynamic Motion: Zero static holds (< 1.0s) verified by MotionAuditor
- Quality Standards: EBU R128 (-14.0 LUFS), 1080x1920 30 FPS, Visual QA Contact Sheet
"""

import datetime
import json
import logging
import sys
import time
from pathlib import Path

# Add project root
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from core.config import get_config
from core.creative_contracts import SceneType
from audio.providers.voicebox_provider import VoiceboxProvider
from creative.tech_documentary.documentary_renderer.tech_doc_producer import TechDocProducer
from rendering.motion_audit import MotionAuditor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("super_intelligence.produce_phase3_5")


def main():
    logger.info("================================================================================")
    logger.info("   SUPER.INTELLIGENCEEE — PHASE 3.5 PRODUCTION ENGINE")
    logger.info("   Topic: Speculative Decoding: Breaking the Autoregressive Memory Wall")
    logger.info("   Voice: General American English Male (am_liam)")
    logger.info("================================================================================")

    config = get_config()
    output_dir = config.resolve_path("output/drafts")
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = output_dir / "phase3_5_audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    # 1. Define the 6-Scene Documentary Blueprint (Aligned to Section 5: Opening -> Silicon -> Tree -> Terminal -> Benchmarks -> Conclusion)
    scenes_data = [
        {
            "scene_index": 1,
            "scene_type": SceneType.KINETIC_TYPOGRAPHY,
            "narrative_role": "HOOK",
            "narration": (
                "Every time an LLM generates a single token, it hits a brutal physical ceiling: "
                "the memory bandwidth wall. Loading seventy billion parameters from GPU memory "
                "starves the compute cores, leaving modern hardware idle."
            ),
            "on_screen_text": "SPECULATIVE DECODING ACCELERATION",
            "visual_description": "Draft verifier models break autoregressive memory latency without quality loss.",
            "stat_number": "3.2x",
            "highlight_keyword": "SPECULATIVE",
            "sub_header": "Draft verifier models break autoregressive memory latency without quality loss.",
            "citation": "SOURCE: LEVIATHAN ET AL. // FAST INFERENCE VIA SPECULATIVE DECODING",
            "category": "SYSTEMS ARCHITECTURE",
        },
        {
            "scene_index": 2,
            "scene_type": SceneType.CINEMATIC_BROLL,
            "narrative_role": "HARDWARE_EXPLANATION",
            "narration": (
                "On high-end silicon like the A100, loading seventy billion parameters requires transferring "
                "one hundred forty gigabytes per token. High bandwidth memory bus saturation leaves over eighty-eight percent "
                "of tensor cores idling."
            ),
            "on_screen_text": "HARDWARE MEMORY WALL",
            "visual_description": "GPU Arithmetic Intensity Roofline Shift // Zero DRAM Spill",
            "sub_header": "NVIDIA A100 SXM4 // High-Bandwidth Memory Saturation at Batch Size 1",
            "telemetry": "HBM2e BUS SATURATION: 98.4% // DRAM ALLOCATION STALL",
        },
        {
            "scene_index": 3,
            "scene_type": SceneType.TECHNICAL_DIAGRAM,
            "narrative_role": "VERIFICATION_TREE",
            "narration": (
                "Speculative decoding shatters this bottleneck. A tiny draft model rapidly emits four candidate tokens. "
                "Then, the primary model verifies all four in one parallel pass, mathematically preserving the exact target distribution."
            ),
            "on_screen_text": "SPECULATIVE VERIFICATION TREE",
            "visual_description": "Draft Model Emits K=4 Tokens; Target Model Verifies in 1 Parallel Pass",
            "sub_header": "Draft Model Emits K=4 Tokens; Target Model Verifies in 1 Parallel Pass",
            "telemetry": "REJECTION SAMPLING: min(1, p/q) // EXACT PROBABILITY MATCH // P=1.0",
        },
        {
            "scene_index": 4,
            "scene_type": SceneType.SCREEN_DEMONSTRATION,
            "narrative_role": "TERMINAL_DEMO",
            "narration": (
                "In live production benchmarks with vLLM, draft acceptance rates consistently exceed seventy-eight percent. "
                "Per-token verification latency drops by half without sacrificing a single point of precision."
            ),
            "on_screen_text": "LIVE INFERENCE VERIFICATION",
            "visual_description": "vLLM Speculative Engine on NVIDIA A100-SXM4-80GB",
            "sub_header": "vLLM Speculative Engine on NVIDIA A100-SXM4-80GB",
            "command": "vllm serve Llama-3-70b --speculative-model Llama-3-8b --spec-tokens 4",
            "telemetry": "CUDA 12.4 | A100-80GB | ACCEPTANCE RATE 78.4% | FP16 PARITY",
        },
        {
            "scene_index": 5,
            "scene_type": SceneType.DATA_VISUALIZATION,
            "narrative_role": "BENCHMARK_COMPARISON",
            "narration": (
                "The numbers speak for themselves. Generation speed leaps from thirty tokens per second to over ninety-eight "
                "tokens per second—a three-point-two-times wall-clock acceleration with zero perplexity degradation."
            ),
            "on_screen_text": "EMPIRICAL INFERENCE BENCHMARKS",
            "visual_description": "Llama-3-70B Target + 1B Draft: Standard vs Speculative Decoding",
            "sub_header": "Llama-3-70B Target + 1B Draft: Standard vs Speculative Decoding",
            "telemetry": "BENCHMARK SUITE: NVIDIA A100 80GB // 100% REASONING PARITY",
        },
        {
            "scene_index": 6,
            "scene_type": SceneType.NARRATIVE_SCENE,
            "narrative_role": "CONCLUSION_VERDICT",
            "narration": (
                "The verdict is conclusive: standard autoregressive decoding is obsolete. Speculative draft verification "
                "is now the mandatory baseline architecture for production AI."
            ),
            "on_screen_text": "THE SPECULATIVE INFERENCE VERDICT",
            "visual_description": "Architectural Synthesis on Draft-Verifier Decoding",
            "sub_header": "Architectural Synthesis on Draft-Verifier Decoding",
            "telemetry": "SYSTEMS SUMMARY: EXACT TARGET DISTRIBUTION // 3.2X SPEEDUP",
        },
    ]

    # 2. Synthesize American Narration using Voicebox Kokoro (am_liam)
    logger.info("--- Step 1: Synthesizing General American Male Narration (am_liam) ---")
    voice_provider = VoiceboxProvider(api_url="http://127.0.0.1:17493")
    assert voice_provider.is_available(), "Voicebox daemon is not available on http://127.0.0.1:17493!"

    scene_audio_files: List[Path] = []
    for idx, sc in enumerate(scenes_data):
        sc_num = idx + 1
        wav_out = audio_dir / f"scene_{sc_num:02d}_{sc['narrative_role'].lower()}_am_liam.wav"
        if wav_out.exists() and voice_provider.validate_audio_file(wav_out).get("valid", False):
            dur_val = voice_provider.validate_audio_file(wav_out).get("duration", 0.0)
            logger.info(f"Using existing validated Scene {sc_num} audio: {wav_out.name} ({dur_val:.2f}s)")
            scene_audio_files.append(wav_out)
            continue

        logger.info(f"Synthesizing Scene {sc_num} narration via Voicebox (am_liam)...")
        success, voice_meta = voice_provider.generate_speech(
            text=sc["narration"],
            output_wav_path=wav_out,
            voice_id="am_liam",
        )
        assert success, f"Voice synthesis failed for Scene {sc_num}: {voice_meta.get('error')}"
        duration_s = voice_meta.get("duration", 0.0)
        logger.info(f"Scene {sc_num} audio ready: {wav_out.name} ({duration_s:.2f}s)")
        scene_audio_files.append(wav_out)

    total_voice_dur = sum(voice_provider.validate_audio_file(p).get("duration", 0.0) for p in scene_audio_files)
    logger.info(f"Total raw American voice duration: {total_voice_dur:.2f}s")
    assert 55.0 <= total_voice_dur <= 75.0, f"Total voice duration {total_voice_dur:.2f}s outside target window!"

    # 3. Produce Tech Documentary with Producer
    logger.info("--- Step 2: Executing TechDocProducer Full Pipeline ---")
    producer = TechDocProducer(config=config)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    reel_slug = f"doc_phase3_5_1_{timestamp}_speculative_decoding"

    topic = {
        "title": "Speculative Decoding: Breaking the Autoregressive Memory Wall",
        "category": "Systems Architecture",
    }

    result = producer.produce_documentary(
        scene_plan=scenes_data,
        topic=topic,
        scene_audio_files=scene_audio_files,
        reel_slug=reel_slug,
        burn_subtitles=True,
        transition_type="wipeleft",
    )

    logger.info(f"Produced video: {result.final_video_path}")
    logger.info(f"Final video duration: {result.duration_seconds:.2f}s")
    logger.info(f"Contact sheet: {result.contact_sheet_path}")

    # 4. Programmatic Motion Audit Verification
    logger.info("--- Step 3: Running Programmatic Motion Audit (Detecting Static Holds) ---")
    auditor = MotionAuditor()
    motion_res = auditor.audit_video(
        video_path=result.final_video_path,
        sample_interval=0.5,
        static_threshold_pct=0.035,
    )

    motion_json_path = output_dir / f"{reel_slug}_motion_audit.json"
    motion_res.save_json(motion_json_path)

    logger.info(f"Motion Audit Result: Mean Delta={motion_res.mean_delta_pct:.2f}%, Max Consecutive Static={motion_res.static_hold_max_consecutive_seconds:.1f}s, Pass={motion_res.motion_pass}")
    assert motion_res.motion_pass, f"Motion audit failed! Max frozen hold: {motion_res.static_hold_max_consecutive_seconds:.1f}s"

    # 5. Save Production Manifest
    manifest = {
        "doc_id": reel_slug,
        "topic": topic["title"],
        "category": topic["category"],
        "timestamp": timestamp,
        "voice": {
            "model": "Kokoro-82M",
            "voice_id": "am_liam",
            "accent": "General American English (Male)",
            "sample_rate": 24000,
            "master_sample_rate": 48000,
            "loudness_target_lufs": -14.0,
        },
        "audio_architecture": {
            "adaptive_soundtrack": "6-Act Continuous Score (pure-math NumPy electronic synthesis)",
            "sidechain_compression": "threshold=0.08:ratio=6:attack=50:release=250",
            "sound_cue_timeline": str(result.sound_cue_timeline_path),
        },
        "video": {
            "resolution": "1080x1920",
            "fps": 30,
            "duration_seconds": result.duration_seconds,
            "scene_count": result.scene_count,
            "final_video_path": str(result.final_video_path),
            "raw_video_path": str(result.raw_video_path),
            "contact_sheet_path": str(result.contact_sheet_path),
            "visual_qa_report": result.visual_qa_report,
            "motion_audit": motion_res.to_dict(),
        },
        "governance": {
            "approval_required": True,
            "auto_publish": False,
            "status": "READY_FOR_REVIEW",
        },
    }

    manifest_path = output_dir / f"{reel_slug}_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    logger.info(f"Production manifest saved: {manifest_path.name}")

    logger.info("================================================================================")
    logger.info("   PHASE 3.5 PRODUCTION COMPLETED SUCCESSFULLY!")
    logger.info(f"   Video: {result.final_video_path.name}")
    logger.info(f"   Duration: {result.duration_seconds:.2f}s")
    logger.info(f"   Audio Master: {result.master_audio_path.name}")
    logger.info(f"   Status: READY_FOR_REVIEW (Manual approval gate active)")
    logger.info("================================================================================")


if __name__ == "__main__":
    main()
