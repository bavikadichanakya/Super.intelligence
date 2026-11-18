"""
SUPER.INTELLIGENCEEE — Phase 3.5 Cinematic Adaptive Soundtrack Generator
Synthesizes a continuous, narrative-aligned multi-act musical score:
- Act 1: Atmospheric Introduction (Curiosity & Anticipation)
- Act 2: Technical Tension (Complexity & Memory Wall)
- Act 3: Architectural Breakthrough (Harmonic Lift & Shimmer)
- Act 4: Demonstration Workbench (Restrained Rhythmic Bed, Notched for Speech)
- Act 5: Comparative Momentum (Driving Rhythm & Performance Results)
- Act 6: Synthesis & Resolution (Resolving Cadence & Deliberate Ending Tail)
Uses NumPy for fast, pure-math synthesis with zero external dependencies.
"""

from __future__ import annotations

import logging
import math
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

logger = logging.getLogger("super_intelligence.adaptive_soundtrack")


class AdaptiveSoundtrackGenerator:
    """Generates continuous, 6-act narrative electronic scores for technology documentaries."""

    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    def synthesize_score(
        self,
        scene_durations: List[float],
        output_path: Path | str,
        base_volume: float = 0.18,
    ) -> Path:
        """
        Synthesizes a 48 kHz stereo WAV score matching the cumulative timing of the documentary.
        """
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        total_duration = sum(scene_durations)
        if total_duration <= 0.0:
            total_duration = 60.0

        n_samples = int(total_duration * self.sample_rate)
        t = np.linspace(0, total_duration, n_samples, endpoint=False, dtype=np.float32)

        # Output stereo channels
        left_channel = np.zeros(n_samples, dtype=np.float32)
        right_channel = np.zeros(n_samples, dtype=np.float32)

        # Calculate scene time boundaries
        cum_times = [0.0]
        for d in scene_durations:
            cum_times.append(cum_times[-1] + d)

        # ─── 1. Persistent Cinematic Sub-Bass Drone (D1 / 73.4 Hz + 55 Hz sub) ───
        sub_freq1 = 55.0
        sub_freq2 = 73.416  # D2
        sub_osc = (
            0.5 * np.sin(2 * np.pi * sub_freq1 * t)
            + 0.5 * np.sin(2 * np.pi * sub_freq2 * t)
        )
        # Slow 0.15 Hz stereo pulse
        sub_lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.15 * t)
        sub_bed = sub_osc * sub_lfo * 0.22

        left_channel += sub_bed
        right_channel += sub_bed

        # ─── 2. Act-by-Act Polyphonic Chord Progressions & Harmonic Evolution ───
        for idx, (t_start, t_end) in enumerate(zip(cum_times[:-1], cum_times[1:])):
            mask = (t >= t_start) & (t < t_end)
            if not np.any(mask):
                continue
            t_act = t[mask] - t_start
            act_dur = t_end - t_start

            # Crossfade envelopes (smooth 0.5s transition between acts)
            env = np.ones_like(t_act)
            fade_len = min(int(0.5 * self.sample_rate), len(t_act) // 3)
            if fade_len > 0:
                env[:fade_len] = np.linspace(0, 1, fade_len)
                env[-fade_len:] = np.linspace(1, 0, fade_len)

            if idx == 0:
                # ── ACT 1: ATMOSPHERIC INTRODUCTION (D minor / curiosity) ──
                # Notes: D3 (146.83), F3 (174.61), A3 (220.00), C4 (261.63)
                freqs = [146.83, 174.61, 220.00, 261.63]
                pad = np.zeros_like(t_act)
                for f_idx, f in enumerate(freqs):
                    # Slight detuning for rich chorus
                    pad += 0.25 * np.sin(2 * np.pi * (f - 0.3) * t_act)
                    pad += 0.25 * np.sin(2 * np.pi * (f + 0.3) * t_act)
                # Shimmer modulation
                shimmer = 0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t_act)
                act_signal = pad * shimmer * env * 0.26

                left_channel[mask] += act_signal * 0.95
                right_channel[mask] += act_signal * 1.05

            elif idx == 1:
                # ── ACT 2: TECHNICAL TENSION (G minor / complexity & memory wall) ──
                # Notes: G2 (98.00), G3 (196.00), Bb3 (233.08), D4 (293.66)
                freqs = [98.00, 196.00, 233.08, 293.66]
                pad = np.zeros_like(t_act)
                for f in freqs:
                    pad += 0.3 * np.sin(2 * np.pi * f * t_act)
                # 120 BPM (2.0 Hz) rhythmic pulse
                rhythm_pulse = 0.7 + 0.3 * np.abs(np.sin(2 * np.pi * 2.0 * t_act))
                act_signal = pad * rhythm_pulse * env * 0.28

                left_channel[mask] += act_signal * 1.05
                right_channel[mask] += act_signal * 0.95

            elif idx == 2:
                # ── ACT 3: THE BREAKTHROUGH (Harmonic Lift to F Major / Shimmer) ──
                # Notes: F3 (174.61), A3 (220.00), C4 (261.63), E4 (329.63) + High Sparkle
                freqs = [174.61, 220.00, 261.63, 329.63, 659.25]
                pad = np.zeros_like(t_act)
                for f in freqs:
                    pad += 0.22 * np.sin(2 * np.pi * f * t_act)
                # Resonant upward filter sweep
                sweep_factor = np.linspace(0.8, 1.25, len(t_act))
                act_signal = pad * sweep_factor * env * 0.30

                left_channel[mask] += act_signal
                right_channel[mask] += act_signal

            elif idx == 3:
                # ── ACT 4: DEMONSTRATION WORKBENCH (Minimal Rhythmic Ticking, Speech Notch) ──
                # Notes: D3 (146.83), A3 (220.00) + Clean clock pulse
                f_clock = 4.0  # 16th notes at 120 BPM
                clock_pulse = 0.15 * np.exp(-((t_act % 0.25) / 0.04) ** 2)
                pad = 0.2 * np.sin(2 * np.pi * 146.83 * t_act) + 0.15 * np.sin(2 * np.pi * 220.00 * t_act)
                act_signal = (pad + clock_pulse) * env * 0.24

                # Pan slight left/right alternation
                pan_lfo = np.sin(2 * np.pi * 1.0 * t_act)
                left_channel[mask] += act_signal * (0.8 + 0.2 * pan_lfo)
                right_channel[mask] += act_signal * (0.8 - 0.2 * pan_lfo)

            elif idx == 4:
                # ── ACT 5: COMPARATIVE RESULTS & ACCELERATION (Driving Momentum) ──
                # Driving octave bass + Bright synth lead (Bb3 -> C4 -> D4)
                bass = 0.35 * np.sin(2 * np.pi * 73.416 * t_act) + 0.25 * np.sin(2 * np.pi * 146.83 * t_act)
                lead = 0.2 * np.sin(2 * np.pi * 293.66 * t_act) + 0.15 * np.sin(2 * np.pi * 440.00 * t_act)
                momentum = 0.75 + 0.25 * np.abs(np.sin(2 * np.pi * 4.0 * t_act))
                act_signal = (bass + lead) * momentum * env * 0.32

                left_channel[mask] += act_signal * 1.02
                right_channel[mask] += act_signal * 0.98

            else:
                # ── ACT 6: SYNTHESIS & RESOLUTION (Grand Cadence & Deliberate Ending Tail) ──
                # Notes: D Major resolution (D3 146.83, F#3 185.00, A3 220.00, D4 293.66)
                freqs = [146.83, 185.00, 220.00, 293.66]
                pad = np.zeros_like(t_act)
                for f in freqs:
                    pad += 0.25 * np.sin(2 * np.pi * f * t_act)

                # Long graceful fade-out starting at 65% of the scene duration to guarantee a clean tail
                act_tail_fade = np.ones_like(t_act)
                fade_start_idx = int(0.65 * len(t_act))
                act_tail_fade[fade_start_idx:] = np.linspace(1.0, 0.0, len(t_act) - fade_start_idx) ** 1.5

                act_signal = pad * act_tail_fade * 0.28
                left_channel[mask] += act_signal
                right_channel[mask] += act_signal

        # ─── 3. Final Master Scaling & Soft Limiting ───
        master_l = left_channel * base_volume
        master_r = right_channel * base_volume

        # Soft hyperbolic tangent saturation to guarantee zero harsh digital clipping
        master_l = np.tanh(master_l)
        master_r = np.tanh(master_r)

        # Convert to 16-bit signed PCM
        pcm_l = (master_l * 32767).astype(np.int16)
        pcm_r = (master_r * 32767).astype(np.int16)

        # Interleave stereo channels
        stereo_pcm = np.empty((n_samples, 2), dtype=np.int16)
        stereo_pcm[:, 0] = pcm_l
        stereo_pcm[:, 1] = pcm_r

        with wave.open(str(out_p), "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(stereo_pcm.tobytes())

        logger.info(f"Synthesized continuous 6-act adaptive soundtrack ({total_duration:.2f}s) -> {out_p.name}")
        return out_p

