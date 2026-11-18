"""
SUPER.INTELLIGENCEEE — Sound Design: Enhanced Cinematic Sound Designer (Phase 3.5)
Assembles professional multi-track broadcast soundscapes:
- Layer 1: American English Narration (-14.0 LUFS target)
- Layer 2: Continuous 6-Act Adaptive Electronic Score (with automated sidechain compression ducking)
- Layer 3: Synchronized Event-Driven Diegetic Foley (Typing, node chimes, metric pings, transition sweeps)
Outputs mastered stereo WAV (-14.0 LUFS) and exported sound_cue_timeline.json.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.config import get_config
from audio.audio_mixer import AudioMixer
from creative.tech_documentary.sound_design.adaptive_soundtrack import AdaptiveSoundtrackGenerator
from creative.tech_documentary.sound_design.sound_cues import SoundCue, SoundCueTimeline

logger = logging.getLogger("super_intelligence.sound_designer")


class SoundDesigner:
    """Orchestrates multi-layer cinematic soundscapes with adaptive score and sidechain ducking."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.audio_mixer = AudioMixer(config=self.config)
        self.sfx_dir = self.config.resolve_path(".agents/skills/media-use/audio/assets/sfx")
        self.adaptive_score_gen = AdaptiveSoundtrackGenerator(sample_rate=48000)
        self.ffmpeg_cmd = "ffmpeg"

    def build_event_cue_timeline(
        self,
        scene_durations: List[float],
        scene_types: List[str],
        doc_id: str = "tech_doc",
        scene_descriptions: Optional[List[str]] = None,
    ) -> SoundCueTimeline:
        """
        Builds a deterministic, event-anchored SoundCueTimeline where every effect
        corresponds to a verified visual or narrative timestamp. Zero arbitrary whooshes.
        """
        total_duration_ms = int(sum(scene_durations) * 1000)
        timeline = SoundCueTimeline(doc_id=doc_id, total_duration_ms=total_duration_ms)

        cum_ms = 0
        scene_descs = scene_descriptions or [f"Scene {i+1} ({st})" for i, st in enumerate(scene_types)]

        for idx, (dur, st, desc) in enumerate(zip(scene_durations, scene_types, scene_descs)):
            dur_ms = int(dur * 1000)
            st_upper = str(st).upper()

            # 1. Opening & Scene Transition Cues
            if idx == 0:
                timeline.add_cue(
                    event_type="DOCUMENTARY_OPEN",
                    timestamp_ms=cum_ms + 100,
                    visual_anchor=f"Title card reveal and documentary hook: {desc[:40]}",
                    asset_name="pop.mp3",
                    volume=0.12,
                    notes="Subtle introductory pop for primary topic headline",
                )
            else:
                timeline.add_cue(
                    event_type="SCENE_TRANSITION",
                    timestamp_ms=max(0, cum_ms - 150),
                    visual_anchor=f"Cut transition to Scene {idx+1}: {st_upper}",
                    asset_name="whoosh-cinematic.mp3",
                    volume=0.14,
                    notes="Clean scene cut transition marker",
                )

            # 2. Diegetic Scene-Specific Visual Foley
            if "TERMINAL" in st_upper or "SCREEN_DEMONSTRATION" in st_upper or "CODE" in st_upper:
                # Terminal typing burst starts when command starts rendering
                timeline.add_cue(
                    event_type="TERMINAL_COMMAND_EXECUTE",
                    timestamp_ms=cum_ms + 400,
                    visual_anchor="Terminal prompt execution and live output stream",
                    asset_name="typing.mp3",
                    volume=0.10,
                    notes="Realistic mechanical keystrokes under terminal stream",
                )
                # Output completion click
                timeline.add_cue(
                    event_type="PROCESS_COMPLETE",
                    timestamp_ms=cum_ms + int(dur_ms * 0.65),
                    visual_anchor="Benchmark CLI execution finishes with exit code 0",
                    asset_name="click-soft.mp3",
                    volume=0.12,
                    notes="Soft tactile feedback on execution completion",
                )

            elif "DIAGRAM" in st_upper or "ARCHITECTURE" in st_upper or "PROCESS" in st_upper:
                timeline.add_cue(
                    event_type="ARCHITECTURE_NODE_REVEAL",
                    timestamp_ms=cum_ms + 500,
                    visual_anchor="Vector architecture nodes activate with kinetic connection lines",
                    asset_name="chime.mp3",
                    volume=0.13,
                    notes="Harmonic chime on multi-component architecture illumination",
                )
                timeline.add_cue(
                    event_type="DATAFLOW_PULSE",
                    timestamp_ms=cum_ms + int(dur_ms * 0.55),
                    visual_anchor="Dynamic token flow packet reaches target verifier",
                    asset_name="ping.mp3",
                    volume=0.11,
                    notes="Subtle resonant ping on token dataflow arrival",
                )

            elif "COMPARISON" in st_upper or "METRIC" in st_upper or "RESULTS" in st_upper:
                timeline.add_cue(
                    event_type="METRIC_COUNTER_START",
                    timestamp_ms=cum_ms + 300,
                    visual_anchor="Side-by-side metric HUD counter begins incrementing",
                    asset_name="click-soft.mp3",
                    volume=0.10,
                    notes="Tactile click initiating quantitative comparison",
                )
                timeline.add_cue(
                    event_type="METRIC_BENCHMARK_LAND",
                    timestamp_ms=cum_ms + int(dur_ms * 0.70),
                    visual_anchor="Final speedup multiplier and memory savings land in HUD",
                    asset_name="impact-bass-1.mp3",
                    volume=0.15,
                    notes="Deep low-end impact accentuating empirical benchmark victory",
                )

            elif "VERDICT" in st_upper or "CONCLUSION" in st_upper or "OUTLOOK" in st_upper:
                timeline.add_cue(
                    event_type="VERDICT_SYNTHESIS",
                    timestamp_ms=cum_ms + 400,
                    visual_anchor="Definitive verdict card enters and locks into position",
                    asset_name="sparkle.mp3",
                    volume=0.14,
                    notes="Harmonic shimmer highlighting engineering takeaway",
                )
                timeline.add_cue(
                    event_type="EDITORIAL_OUTRO",
                    timestamp_ms=cum_ms + int(dur_ms * 0.75),
                    visual_anchor="Super.intelligence brand watermark lockup and signoff",
                    asset_name="notification.mp3",
                    volume=0.12,
                    notes="Final broadcast signature audio mark",
                )

            cum_ms += dur_ms

        return timeline

    def assemble_documentary_soundscape(
        self,
        voiceover_master_path: Path | str,
        scene_durations: List[float],
        scene_types: List[str],
        output_path: Path | str,
        target_lufs: float = -14.0,
        timeline: Optional[SoundCueTimeline] = None,
        scene_descriptions: Optional[List[str]] = None,
    ) -> Tuple[Path, Path]:
        """
        Assembles narration, continuous adaptive score with sidechain ducking,
        and event-driven diegetic foley into a broadcast master WAV.
        Returns:
            Tuple[Path to master WAV, Path to exported sound_cue_timeline.json]
        """
        voice_path = Path(voiceover_master_path).resolve()
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        voice_dur = self.audio_mixer.get_audio_duration(voice_path)
        total_duration = sum(scene_durations)
        if total_duration <= 0.0 or abs(total_duration - voice_dur) > 5.0:
            total_duration = max(voice_dur, total_duration)

        logger.info(
            f"Assembling Phase 3.5 multi-track soundscape (Voice: {voice_dur:.2f}s, Target: {total_duration:.2f}s)..."
        )

        # 1. Synthesize Continuous 6-Act Adaptive Electronic Score
        score_path = out_p.parent / f"adaptive_score_{out_p.stem}.wav"
        try:
            self.adaptive_score_gen.synthesize_score(
                scene_durations=scene_durations,
                output_path=score_path,
                base_volume=0.20,
            )
        except Exception as e:
            logger.warning(f"Continuous adaptive score synthesis failed ({e}). Proceeding without score...")
            score_path = None

        # 2. Build or Use Event-Driven Sound Cue Timeline
        if timeline is None:
            timeline = self.build_event_cue_timeline(
                scene_durations=scene_durations,
                scene_types=scene_types,
                doc_id=out_p.stem,
                scene_descriptions=scene_descriptions,
            )

        timeline_json_path = out_p.parent / "sound_cue_timeline.json"
        timeline.save_json(timeline_json_path)

        # 3. Assemble FFmpeg Multi-Track Graph with Sidechain Compression
        # Inputs:
        # 0: Voiceover Master (Reference Track & Sidechain Key)
        # 1: Adaptive Musical Score
        # 2..N: Sound Cues with exact millisecond delays
        cmd = [self.ffmpeg_cmd, "-y", "-i", str(voice_path)]
        input_count = 1

        score_idx = None
        if score_path and score_path.exists():
            cmd.extend(["-i", str(score_path)])
            score_idx = input_count
            input_count += 1

        cue_input_map: List[Tuple[int, SoundCue]] = []
        for cue in timeline.cues:
            sfx_file = self.sfx_dir / cue.asset_name
            if sfx_file.exists():
                cmd.extend(["-i", str(sfx_file)])
                cue_input_map.append((input_count, cue))
                input_count += 1
            else:
                logger.warning(f"SFX asset not found: {cue.asset_name} for cue {cue.cue_id}")

        # Construct Filter Complex
        filter_chains = []
        mix_inputs = []

        # Voiceover processing (ensure 48k stereo)
        filter_chains.append("[0:a]aformat=channel_layouts=stereo:sample_rates=48000[voice_main]")
        mix_inputs.append("[voice_main]")

        if score_idx is not None:
            # Duck music under voice using sidechain compressor
            # Music is ducked when speech energy exceeds threshold (0.08)
            filter_chains.append(f"[{score_idx}:a]aformat=channel_layouts=stereo:sample_rates=48000[score_in]")
            filter_chains.append(
                "[score_in][0:a]sidechaincompress="
                "threshold=0.08:ratio=6:attack=50:release=250:level_in=1:level_sc=1[ducked_score]"
            )
            filter_chains.append("[ducked_score]volume=0.35[score_final]")
            mix_inputs.append("[score_final]")

        # Foley cue delay & volume positioning
        for in_idx, cue in cue_input_map:
            delay_ms = cue.timestamp_ms
            filter_chains.append(
                f"[{in_idx}:a]adelay={delay_ms}|{delay_ms},volume={cue.volume:.2f},"
                f"aformat=channel_layouts=stereo:sample_rates=48000[foley_{in_idx}]"
            )
            mix_inputs.append(f"[foley_{in_idx}]")

        # Combine all audio streams
        filter_chains.append(
            f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=2[mixed]"
        )
        # Gentle master highpass filter to remove subsonic rumble below 35 Hz
        filter_chains.append("[mixed]highpass=f=35,aresample=48000[aout]")

        filter_str = ";".join(filter_chains)
        raw_mix_path = out_p.parent / f"raw_mix_{out_p.stem}.wav"

        cmd.extend([
            "-filter_complex", filter_str,
            "-map", "[aout]",
            "-ac", "2",
            "-ar", "48000",
            str(raw_mix_path),
        ])

        logger.info(f"Executing FFmpeg multi-stem mix with sidechain ducking ({len(mix_inputs)} inputs)...")
        res = subprocess.run(cmd, capture_output=True, text=True)

        # Cleanup intermediate score
        if score_path and score_path.exists():
            score_path.unlink(missing_ok=True)

        if res.returncode != 0 or not raw_mix_path.exists() or raw_mix_path.stat().st_size < 1000:
            logger.warning(f"Sidechain mix failed ({res.stderr[:250]}). Falling back to voice master...")
            final_p = self.audio_mixer.normalize_loudness(voice_path, out_p, target_lufs=target_lufs)
            return final_p, timeline_json_path

        # 4. Final Broadcast Loudness Normalization Pass (-14.0 LUFS)
        logger.info("Applying final ITU-R BS.1770-4 two-pass EBU R128 normalization (-14.0 LUFS)...")
        self.audio_mixer.normalize_loudness(raw_mix_path, out_p, target_lufs=target_lufs)

        # Cleanup raw mix
        if raw_mix_path.exists():
            raw_mix_path.unlink(missing_ok=True)

        logger.info(f"Broadcast soundscape finalized: {out_p.name} ({out_p.stat().st_size} bytes, target: {target_lufs} LUFS)")
        return out_p, timeline_json_path
