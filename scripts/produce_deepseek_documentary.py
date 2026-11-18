"""
SUPER.INTELLIGENCEEE — DeepSeek-R1 Viral Open-Source Spotlight Documentary
Full 1080x1920 60s+ Master Production Pipeline:
- Unified Cleanroom Scientific Light Theme (#F8F9FA Pearl Background)
- WCAG AAA Compliant Architectural Typography
- Advanced Subtitle Engine (Transparent, zero-clipping, golden active-word accents)
- 7 Custom High-Fidelity Technical Scenes:
    1. The GitHub Shockwave (74k+ stars, model family chips, animated pulse)
    2. Pure RL via GRPO (SFT bottlenecks vs Compiler-verified GRPO rewards)
    3. The "Aha Moment" (Simulated IDE token stream, backtracking, <think> tags)
    4. Multi-Head Latent Attention (MLA) (Low-rank KV compression to 6.7%)
    5. DeepSeekMoE Sparse Routing Lattice (256 specialists + 1 shared expert, 37B active)
    6. Frontier Benchmark Showdown (AIME 2024, MATH-500, 27x lower cost)
    7. The Open Revolution & MIT License (Distillations, Sovereign AI, Super.intelligencee seal)
"""

from __future__ import annotations

import os
import sys
import time
import math
import wave
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_ROOT = Path("A:/SUPER.INTELLIGENCEEE").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from rendering.composition_engine_v2 import (
    CANVAS_WIDTH, CANVAS_HEIGHT, MARGIN_X, USABLE_WIDTH,
    GRID_LEFT, GRID_RIGHT, GRID_CENTER_X
)
from rendering.text_layout_engine import TextLayoutEngine
from rendering.advanced_subtitle_engine import AdvancedSubtitleEngine

PROD_DIR = WORKSPACE_ROOT / "output" / "drafts" / "deepseek_r1_documentary"
AUDIO_DIR = PROD_DIR / "audio"
SCENES_DIR = PROD_DIR / "scenes"
FRAMES_DIR = PROD_DIR / "frames"
KEYFRAMES_DIR = PROD_DIR / "keyframes"

PROD_DIR.mkdir(parents=True, exist_ok=True)
SCENES_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
KEYFRAMES_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# UNIFIED SCIENTIFIC LIGHT THEME PALETTE
# ==============================================================================
THEME_BG = (248, 249, 250, 255)          # Architectural Cleanroom Pearl (#F8F9FA)
THEME_CARD = (255, 255, 255, 255)        # Pure White Drafting Card (#FFFFFF)
THEME_BORDER = (226, 232, 240, 255)      # Subtle Architectural Border (#E2E8F0)
THEME_BORDER_DARK = (203, 213, 225, 255) # Prominent Grid Line (#CBD5E1)

# Typography Palette (WCAG AAA Compliant on Light Theme)
TYPE_PRIMARY = (15, 23, 42, 255)         # Deep Obsidian Slate (#0F172A)
TYPE_SECONDARY = (71, 85, 105, 255)      # Technical Slate (#475569)
TYPE_MUTED = (100, 116, 139, 255)        # Muted Metadata Slate (#64748B)

# Brand & Semantic Accents
ACCENT_BLUE = (29, 78, 216, 255)         # DeepSeek Research Blue (#1D4ED8)
ACCENT_CYAN = (14, 165, 233, 255)        # Latent Vector Cyan (#0EA5E9)
TECH_GREEN = (5, 150, 105, 255)          # Verified Below-Threshold / RL Healed (#059669)
SIGNAL_RED = (220, 38, 38, 255)          # SFT / Bottleneck Alert (#DC2626)
GOLD_ACCENT = (217, 119, 6, 255)         # Star / Milestone Gold (#D97706)
PURPLE_MOE = (124, 58, 237, 255)         # Mixture-of-Experts Purple (#7C3AED)

# Global Typography & Subtitle Engines
LAYOUT_ENGINE = TextLayoutEngine()
SUBTITLE_ENGINE = AdvancedSubtitleEngine(LAYOUT_ENGINE)

FONT_TITLE = LAYOUT_ENGINE.get_font("segoeuib.ttf", 44)
FONT_SUB = LAYOUT_ENGINE.get_font("segoeui.ttf", 26)
FONT_MONO = LAYOUT_ENGINE.get_font("consolab.ttf", 24)
FONT_BADGE = LAYOUT_ENGINE.get_font("segoeuib.ttf", 24)
FONT_NOTE = LAYOUT_ENGINE.get_font("segoeui.ttf", 20)
FONT_CODE = LAYOUT_ENGINE.get_font("consola.ttf", 22)
FONT_CODE_BOLD = LAYOUT_ENGINE.get_font("consolab.ttf", 22)

def draw_light_background(canvas: Image.Image):
    """Draws master cleanroom pearl background with subtle top-down ambient lighting."""
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], fill=THEME_BG)
    for y in range(400):
        alpha = int(35 * (1.0 - y / 400.0))
        draw.line([0, y, CANVAS_WIDTH, y], fill=(241, 245, 249, alpha))

def draw_header_bar(draw: ImageDraw.Draw, tag: str, title: str, subtitle: str, tag_color: Tuple[int, int, int, int]):
    """Renders consistent top header bar with protective safe-zone mask."""
    draw.rectangle([0, 0, CANVAS_WIDTH, 235], fill=THEME_BG)
    draw.text((GRID_LEFT, 90), tag, font=FONT_MONO, fill=tag_color)
    draw.text((GRID_LEFT, 124), title, font=FONT_TITLE, fill=TYPE_PRIMARY)
    draw.text((GRID_LEFT, 178), subtitle, font=FONT_SUB, fill=TYPE_SECONDARY)
    draw.line([GRID_LEFT, 218, GRID_RIGHT, 218], fill=THEME_BORDER_DARK, width=2)


# ==============================================================================
# SCENE 1: THE GITHUB SHOCKWAVE
# ==============================================================================
class Scene1HookShockwave:
    def __init__(self, duration: float):
        self.duration = duration
        self.subtitles = [
            ("Ever wondered how a single open-source GitHub repository", "open-source", 0.20, 4.10),
            ("shook Silicon Valley and challenged trillion-dollar AI monopolies overnight?", "monopolies", 4.30, 8.40),
        ]

    def render_frame(self, t: float, render_subs: bool = True, subs_only: bool = False) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0) if subs_only else THEME_BG)
        draw = ImageDraw.Draw(canvas, "RGBA")

        if not subs_only:
            draw_light_background(canvas)
            draw_header_bar(draw, "OPEN RESEARCH ARCHIVE // 01", "THE OPEN-SOURCE SHOCKWAVE", "A single GitHub repository challenges trillion-dollar frontier monopolies", ACCENT_BLUE)

            # Central GitHub Repository Card
            cx0, cy0, cw, ch = GRID_LEFT, 270, USABLE_WIDTH, 820
            draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=20, fill=THEME_CARD, outline=THEME_BORDER, width=2)

            # Repo Topbar
            draw.rectangle([cx0, cy0, cx0 + cw, cy0 + 80], fill=(241, 245, 249, 255))
            draw.line([cx0, cy0 + 80, cx0 + cw, cy0 + 80], fill=THEME_BORDER, width=1)
            draw.text((cx0 + 30, cy0 + 26), "github.com / deepseek-ai / DeepSeek-R1", font=FONT_MONO, fill=TYPE_PRIMARY)

            # Public Badge
            draw.rounded_rectangle([cx0 + cw - 150, cy0 + 22, cx0 + cw - 30, cy0 + 58], radius=18, fill=(236, 253, 245, 255), outline=TECH_GREEN, width=1)
            draw.text((cx0 + cw - 132, cy0 + 28), "Public Repo", font=FONT_NOTE, fill=TECH_GREEN)

            # Repo Title & Icon
            draw.text((cx0 + 36, cy0 + 115), "deepseek-ai / DeepSeek-R1", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 38), fill=ACCENT_BLUE)
            draw.text((cx0 + 36, cy0 + 175), "Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", font=FONT_SUB, fill=TYPE_SECONDARY)

            # Live Shockwave Animated Pulse Ring around repo metrics
            pulse_r = int(50 + (t * 80) % 180)
            pulse_alpha = max(0, int(160 * (1.0 - ((t * 80) % 180) / 180.0)))
            draw.ellipse([540 - pulse_r, cy0 + 340 - pulse_r, 540 + pulse_r, cy0 + 340 + pulse_r], outline=(29, 78, 216, pulse_alpha), width=3)

            # Metrics Row (Stars, Forks, License)
            m_cards = [
                ("⭐ 74,800+", "GitHub Stars", GOLD_ACCENT),
                ("🍴 8,450", "Active Forks", ACCENT_BLUE),
                ("📜 MIT", "Open License", TECH_GREEN),
            ]
            mc_w = (cw - 80) // 3
            for i, (val, lbl, col) in enumerate(m_cards):
                mx = cx0 + 30 + i * (mc_w + 10)
                my = cy0 + 240
                draw.rounded_rectangle([mx, my, mx + mc_w, my + 110], radius=14, fill=(248, 250, 252, 255), outline=THEME_BORDER, width=1)
                draw.text((mx + 20, my + 18), val, font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 32), fill=col)
                draw.text((mx + 20, my + 64), lbl, font=FONT_NOTE, fill=TYPE_MUTED)

            # Model Family Chips
            draw.text((cx0 + 36, cy0 + 380), "OFFICIAL MODEL WEIGHTS RELEASED", font=FONT_MONO, fill=TYPE_PRIMARY)
            chips = [
                ("DeepSeek-R1 (671B MoE)", TECH_GREEN),
                ("DeepSeek-R1-Zero (Pure RL)", ACCENT_BLUE),
                ("Distill-Qwen (1.5B – 32B)", PURPLE_MOE),
                ("Distill-Llama (8B, 70B)", GOLD_ACCENT),
            ]
            ch_y = cy0 + 420
            for i, (name, col) in enumerate(chips):
                ry = ch_y + i * 58
                draw.rounded_rectangle([cx0 + 36, ry, cx0 + cw - 36, ry + 46], radius=10, fill=(241, 245, 249, 255), outline=THEME_BORDER, width=1)
                draw.rectangle([cx0 + 36, ry, cx0 + 44, ry + 46], fill=col)
                draw.text((cx0 + 60, ry + 10), name, font=FONT_BADGE, fill=TYPE_PRIMARY)
                draw.text((cx0 + cw - 170, ry + 12), "FREE WEIGHTS", font=FONT_NOTE, fill=col)

            # Lower Impact Stat Card
            ix0, iy0, iw, ih = GRID_LEFT, cy0 + ch + 30, USABLE_WIDTH, 260
            draw.rounded_rectangle([ix0, iy0, ix0 + iw, iy0 + ih], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((ix0 + 36, iy0 + 26), "IMPACT METRICS ON GLOBAL AI INDUSTRY", font=FONT_MONO, fill=TYPE_PRIMARY)
            
            # Stat 1: Cost Disruption
            draw.text((ix0 + 36, iy0 + 75), "27x", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 52), fill=TECH_GREEN)
            draw.text((ix0 + 170, iy0 + 82), "Lower API Inference Cost", font=FONT_BADGE, fill=TYPE_PRIMARY)
            draw.text((ix0 + 170, iy0 + 114), "$0.55/1M vs $15.00/1M tokens (o1)", font=FONT_NOTE, fill=TYPE_SECONDARY)

            # Stat 2: Sovereign AI
            draw.text((ix0 + 36, iy0 + 160), "100%", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 52), fill=ACCENT_BLUE)
            draw.text((ix0 + 195, iy0 + 167), "Verifiable Weights & Local Deployment", font=FONT_BADGE, fill=TYPE_PRIMARY)
            draw.text((ix0 + 195, iy0 + 199), "Zero vendor lock-in // Instant local inference", font=FONT_NOTE, fill=TYPE_SECONDARY)

        if render_subs:
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    SUBTITLE_ENGINE.render_subtitle(canvas, text, active_word=word, treatment=1, y_center=1680)
                    break

        return canvas


# ==============================================================================
# SCENE 2: PURE RL VIA GRPO
# ==============================================================================
class Scene2ReasoningGRPO:
    def __init__(self, duration: float):
        self.duration = duration
        self.subtitles = [
            ("Frontier reasoning models were assumed to require millions in human-labeled data,", "millions", 0.20, 5.20),
            ("until DeepSeek proved pure reinforcement learning induces self-reflection from scratch.", "reinforcement", 5.40, 10.50),
        ]

    def render_frame(self, t: float, render_subs: bool = True, subs_only: bool = False) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0) if subs_only else THEME_BG)
        draw = ImageDraw.Draw(canvas, "RGBA")

        if not subs_only:
            draw_light_background(canvas)
            draw_header_bar(draw, "TRAINING METHODOLOGY // 02", "PURE REINFORCEMENT LEARNING", "Group Relative Policy Optimization eliminates expensive human annotation", TECH_GREEN)

            card_w = USABLE_WIDTH
            # Card 1: Traditional Supervised Fine-Tuning (SFT)
            c1_y = 260
            draw.rounded_rectangle([GRID_LEFT, c1_y, GRID_LEFT + card_w, c1_y + 360], radius=18, fill=THEME_CARD, outline=(254, 202, 202, 255), width=2)
            draw.rectangle([GRID_LEFT, c1_y, GRID_LEFT + card_w, c1_y + 55], fill=(254, 242, 242, 255))
            draw.text((GRID_LEFT + 24, c1_y + 16), "TRADITIONAL REASONING PIPELINE (SFT + RLHF)", font=FONT_BADGE, fill=SIGNAL_RED)

            sft_points = [
                ("❌ Expensive Human Labeling", "Requires millions in hand-crafted chain-of-thought solutions"),
                ("❌ Human Cognitive Bias", "Models inherit human reasoning errors and shortcuts"),
                ("❌ Value Critic Memory Wall", "Requires separate value model eating 50% extra GPU VRAM"),
            ]
            for idx, (title, desc) in enumerate(sft_points):
                py = c1_y + 75 + idx * 85
                draw.text((GRID_LEFT + 24, py), title, font=FONT_BADGE, fill=TYPE_PRIMARY)
                draw.text((GRID_LEFT + 24, py + 30), desc, font=FONT_SUB, fill=TYPE_SECONDARY)

            # Card 2: DeepSeek-R1-Zero Pure RL via GRPO
            c2_y = 650
            draw.rounded_rectangle([GRID_LEFT, c2_y, GRID_LEFT + card_w, c2_y + 400], radius=18, fill=THEME_CARD, outline=(167, 243, 208, 255), width=2)
            draw.rectangle([GRID_LEFT, c2_y, GRID_LEFT + card_w, c2_y + 55], fill=(236, 253, 245, 255))
            draw.text((GRID_LEFT + 24, c2_y + 16), "DEEPSEEK-R1-ZERO: PURE REINFORCEMENT LEARNING", font=FONT_BADGE, fill=TECH_GREEN)

            grpo_points = [
                ("✓ Zero Supervised Cold Start", "Directly initialized from base model without human COT data"),
                ("✓ Rule-Based Verifiers", "Rewards driven by mathematical compilers and exact unit tests"),
                ("✓ Group Relative Optimization (GRPO)", "Samples group of outputs to estimate baseline; drops critic model"),
                ("✓ Spontaneous Emergent Reasoning", "Model spontaneously develops self-correction and backtracking"),
            ]
            for idx, (title, desc) in enumerate(grpo_points):
                py = c2_y + 75 + idx * 80
                draw.text((GRID_LEFT + 24, py), title, font=FONT_BADGE, fill=TYPE_PRIMARY)
                draw.text((GRID_LEFT + 24, py + 28), desc, font=FONT_SUB, fill=TYPE_SECONDARY)

            # Bottom Mathematical Foundation Card
            eq_y = 1080
            draw.rounded_rectangle([GRID_LEFT, eq_y, GRID_LEFT + card_w, eq_y + 320], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((GRID_LEFT + 24, eq_y + 24), "MATHEMATICAL FORMULATION: GRPO OBJECTIVE", font=FONT_MONO, fill=ACCENT_BLUE)
            
            # Equation Render
            eq_text = "J_GRPO(θ) = E [ 1/G ∑ min( r_i · A_i, clip(r_i, 1-ε, 1+ε) · A_i ) - β · D_KL ]"
            draw.text((GRID_LEFT + 24, eq_y + 75), eq_text, font=FONT_CODE_BOLD, fill=TYPE_PRIMARY)

            draw.line([GRID_LEFT + 24, eq_y + 130, GRID_RIGHT - 24, eq_y + 130], fill=THEME_BORDER, width=1)
            draw.text((GRID_LEFT + 24, eq_y + 155), "Where G candidate responses are sampled per question:", font=FONT_SUB, fill=TYPE_SECONDARY)
            draw.text((GRID_LEFT + 24, eq_y + 195), "• Advantage:  A_i = ( R_i - mean(R) ) / std(R)", font=FONT_CODE, fill=TECH_GREEN)
            draw.text((GRID_LEFT + 24, eq_y + 235), "• Verifier:   R_acc (compiler output) + R_format (boxed solution)", font=FONT_CODE, fill=ACCENT_BLUE)
            draw.text((GRID_LEFT + 24, eq_y + 275), "• Memory:     Zero value-network overhead saves 40GB+ per GPU node", font=FONT_CODE, fill=TYPE_MUTED)

        if render_subs:
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    SUBTITLE_ENGINE.render_subtitle(canvas, text, active_word=word, treatment=1, y_center=1680)
                    break

        return canvas


# ==============================================================================
# SCENE 3: THE "AHA MOMENT" & <THINK> TOKENS
# ==============================================================================
class Scene3AhaMoment:
    def __init__(self, duration: float):
        self.duration = duration
        self.subtitles = [
            ("Without any human guidance, the model spontaneously learned to pause, rethink,", "rethink", 0.20, 5.10),
            ("and verify its own deductions inside explicit thinking tokens before answering.", "thinking", 5.30, 10.10),
        ]

    def render_frame(self, t: float, render_subs: bool = True, subs_only: bool = False) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0) if subs_only else THEME_BG)
        draw = ImageDraw.Draw(canvas, "RGBA")

        if not subs_only:
            draw_light_background(canvas)
            draw_header_bar(draw, "EMERGENT BEHAVIOR // 03", "THE SPONTANEOUS 'AHA MOMENT'", "Model autonomously generates reflection tokens during pure reinforcement learning", GOLD_ACCENT)

            # IDE Terminal Window
            tx0, ty0, tw, th = GRID_LEFT, 260, USABLE_WIDTH, 920
            draw.rounded_rectangle([tx0, ty0, tx0 + tw, ty0 + th], radius=18, fill=(30, 41, 59, 255), outline=TYPE_PRIMARY, width=2)

            # Terminal Titlebar
            draw.rectangle([tx0, ty0, tx0 + tw, ty0 + 56], fill=(15, 23, 42, 255))
            # Mac dots
            draw.ellipse([tx0 + 20, ty0 + 20, tx0 + 36, ty0 + 36], fill=(239, 68, 68, 255))
            draw.ellipse([tx0 + 44, ty0 + 20, tx0 + 60, ty0 + 36], fill=(234, 179, 8, 255))
            draw.ellipse([tx0 + 68, ty0 + 20, tx0 + 84, ty0 + 36], fill=(34, 197, 94, 255))
            draw.text((tx0 + 110, ty0 + 16), "deepseek_r1_zero_step_4200_trace.log", font=FONT_MONO, fill=(148, 163, 184, 255))

            # Terminal Code Content
            lines = [
                ("<think>", (14, 165, 233, 255), True),
                ("Problem: Find integer x such that x^2 + 5x - 84 = 0 and x > 0.", (226, 232, 240, 255), False),
                ("Let me factor the quadratic equation:", (148, 163, 184, 255), False),
                ("Looking for two factors of -84 that add up to +5.", (148, 163, 184, 255), False),
                ("Trial 1: (+14, -6) -> sum = 8. (Incorrect)", (248, 113, 113, 255), False),
                ("Trial 2: (+21, -4) -> sum = 17. (Incorrect)", (248, 113, 113, 255), False),
                ("", (0, 0, 0, 0), False),
                ("Wait, wait, wait...", (251, 191, 36, 255), True),
                ("Let me re-evaluate my factor combinations systematically!", (251, 191, 36, 255), True),
                ("84 divided by 7 is 12.", (226, 232, 240, 255), False),
                ("Trial 3: (+12, -7) -> 12 * (-7) = -84, and 12 + (-7) = +5!", (74, 222, 128, 255), True),
                ("Ah! That matches the linear coefficient exactly.", (74, 222, 128, 255), False),
                ("Therefore: (x + 12)(x - 7) = 0.", (226, 232, 240, 255), False),
                ("Since condition specifies x > 0, we reject x = -12 and choose x = 7.", (226, 232, 240, 255), False),
                ("Double check: 7^2 + 5(7) = 49 + 35 = 84. Verified!", (74, 222, 128, 255), False),
                ("</think>", (14, 165, 233, 255), True),
                ("The positive solution is \\boxed{7}.", (255, 255, 255, 255), True),
            ]

            # Dynamic line typing effect based on time t
            max_lines = min(len(lines), int(3 + (t / self.duration) * (len(lines) - 2)))
            ly = ty0 + 80
            for idx in range(max_lines):
                text_str, col, is_bold = lines[idx]
                if text_str:
                    f = FONT_CODE_BOLD if is_bold else FONT_CODE
                    draw.text((tx0 + 28, ly), text_str, font=f, fill=col)
                ly += 45

            # Bottom Emergent Calling Card
            by = ty0 + th + 30
            draw.rounded_rectangle([GRID_LEFT, by, GRID_LEFT + USABLE_WIDTH, by + 260], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((GRID_LEFT + 24, by + 24), "OBSERVED BEHAVIORS INDUCED BY PURE RL", font=FONT_MONO, fill=PURPLE_MOE)

            behaviors = [
                ("1. Spontaneous Rethinking", "Generates phrases like 'Wait, wait, wait' to initiate backtracking"),
                ("2. Self-Verification", "Allocates test-time compute to recalculate intermediate proofs"),
                ("3. Variable Length Reflection", "Adapts thinking token count from 200 to 12,000+ per difficulty"),
            ]
            for idx, (bh_title, bh_desc) in enumerate(behaviors):
                py = by + 68 + idx * 60
                draw.text((GRID_LEFT + 24, py), bh_title, font=FONT_BADGE, fill=TYPE_PRIMARY)
                draw.text((GRID_LEFT + 340, py + 2), bh_desc, font=FONT_NOTE, fill=TYPE_SECONDARY)

        if render_subs:
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    SUBTITLE_ENGINE.render_subtitle(canvas, text, active_word=word, treatment=1, y_center=1680)
                    break

        return canvas


# ==============================================================================
# SCENE 4: MULTI-HEAD LATENT ATTENTION (MLA)
# ==============================================================================
class Scene4MLAArchitecture:
    def __init__(self, duration: float):
        self.duration = duration
        self.subtitles = [
            ("To solve the catastrophic GPU memory crisis of traditional transformers,", "memory", 0.20, 5.20),
            ("DeepSeek engineered Multi-Head Latent Attention, compressing the KV cache by ninety-three percent.", "ninety-three", 5.40, 10.90),
        ]

    def render_frame(self, t: float, render_subs: bool = True, subs_only: bool = False) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0) if subs_only else THEME_BG)
        draw = ImageDraw.Draw(canvas, "RGBA")

        if not subs_only:
            draw_light_background(canvas)
            draw_header_bar(draw, "SYSTEMS ARCHITECTURE // 04", "MULTI-HEAD LATENT ATTENTION", "Low-rank key-value projection shatters GPU memory bandwidth bottleneck", ACCENT_CYAN)

            # KV Cache Memory Comparison Card
            cx0, cy0, cw, ch = GRID_LEFT, 260, USABLE_WIDTH, 480
            draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((cx0 + 28, cy0 + 26), "KV CACHE MEMORY CONSUMPTION PER TOKEN", font=FONT_MONO, fill=TYPE_PRIMARY)

            # Bar 1: Multi-Head Attention (Standard Transformer)
            b1_y = cy0 + 80
            draw.text((cx0 + 28, b1_y), "Standard MHA (Llama / GPT-4)", font=FONT_BADGE, fill=SIGNAL_RED)
            draw.text((cx0 + cw - 180, b1_y), "100% (Bottleneck)", font=FONT_BADGE, fill=SIGNAL_RED)
            draw.rounded_rectangle([cx0 + 28, b1_y + 36, cx0 + cw - 28, b1_y + 80], radius=8, fill=(241, 245, 249, 255), outline=THEME_BORDER, width=1)
            draw.rounded_rectangle([cx0 + 28, b1_y + 36, cx0 + cw - 28, b1_y + 80], radius=8, fill=(254, 202, 202, 255), outline=SIGNAL_RED, width=1)
            draw.text((cx0 + 44, b1_y + 46), "Uncompressed Keys & Values Stored per Layer: O(2 · n_heads · d_head · L)", font=FONT_NOTE, fill=TYPE_PRIMARY)

            # Bar 2: Multi-Query Attention (MQA)
            b2_y = cy0 + 195
            draw.text((cx0 + 28, b2_y), "Multi-Query Attention (MQA)", font=FONT_BADGE, fill=GOLD_ACCENT)
            draw.text((cx0 + cw - 240, b2_y), "12.5% (Capacity Loss)", font=FONT_BADGE, fill=GOLD_ACCENT)
            draw.rounded_rectangle([cx0 + 28, b2_y + 36, cx0 + cw - 28, b2_y + 80], radius=8, fill=(241, 245, 249, 255), outline=THEME_BORDER, width=1)
            draw.rounded_rectangle([cx0 + 28, b2_y + 36, cx0 + int(cw * 0.28), b2_y + 80], radius=8, fill=(254, 240, 138, 255), outline=GOLD_ACCENT, width=1)
            draw.text((cx0 + 44, b2_y + 46), "Single Key/Value Head: degraded expressive representational capacity", font=FONT_NOTE, fill=TYPE_PRIMARY)

            # Bar 3: DeepSeek Multi-Head Latent Attention (MLA)
            b3_y = cy0 + 310
            draw.text((cx0 + 28, b3_y), "DeepSeek MLA (Low-Rank Latent Compression)", font=FONT_BADGE, fill=TECH_GREEN)
            draw.text((cx0 + cw - 180, b3_y), "6.7% (93.3% Saved)", font=FONT_BADGE, fill=TECH_GREEN)
            draw.rounded_rectangle([cx0 + 28, b3_y + 36, cx0 + cw - 28, b3_y + 80], radius=8, fill=(241, 245, 249, 255), outline=THEME_BORDER, width=1)
            # Animated compression bar filling
            fill_w = int((cw - 56) * (0.067 + 0.005 * math.sin(t * 3.0)))
            draw.rounded_rectangle([cx0 + 28, b3_y + 36, cx0 + 28 + fill_w, b3_y + 80], radius=8, fill=(167, 243, 208, 255), outline=TECH_GREEN, width=2)
            draw.text((cx0 + 44, b3_y + 46), "Latent Vector c_t^KV: Only 512 dimensions stored per token!", font=FONT_NOTE, fill=TECH_GREEN)

            # Latent Compression Gauge Callout
            draw.text((cx0 + 28, cy0 + 420), "RESULT: 93.3% VRAM REDUCTION — 5.7x HIGHER SERVING BATCH SIZE", font=FONT_MONO, fill=TECH_GREEN)

            # Architectural Down/Up-Projection Flow Diagram
            fx0, fy0, fw, fh = GRID_LEFT, cy0 + ch + 30, USABLE_WIDTH, 420
            draw.rounded_rectangle([fx0, fy0, fx0 + fw, fy0 + fh], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((fx0 + 28, fy0 + 26), "MATHEMATICAL COMPRESSION MECHANISM", font=FONT_MONO, fill=ACCENT_BLUE)

            flow_steps = [
                ("1. Hidden State h_t", "Model dimension d = 7,168", (241, 245, 249, 255), TYPE_PRIMARY),
                ("↓ Low-Rank Down-Projection", "Matrix W^DKV compresses h_t", (255, 255, 255, 255), ACCENT_BLUE),
                ("2. Compressed Latent Vector c_t^KV", "Dimension d_c = 512 (Only this is cached!)", (236, 253, 245, 255), TECH_GREEN),
                ("↓ Decompressed During Attention", "Up-projected by W^UK and W^UV on the fly", (255, 255, 255, 255), ACCENT_BLUE),
                ("3. Decoupled RoPE Key", "Rotary position embeddings kept separate for full precision", (248, 250, 252, 255), PURPLE_MOE),
            ]
            for idx, (st_title, st_desc, bg_col, txt_col) in enumerate(flow_steps):
                sy = fy0 + 70 + idx * 64
                draw.rounded_rectangle([fx0 + 28, sy, fx0 + fw - 28, sy + 52], radius=10, fill=bg_col, outline=THEME_BORDER, width=1)
                draw.text((fx0 + 44, sy + 14), st_title, font=FONT_BADGE, fill=txt_col)
                draw.text((fx0 + 420, sy + 16), st_desc, font=FONT_NOTE, fill=TYPE_SECONDARY)

            # Throughput Disruption Card
            sx0, sy0, sw, sh = GRID_LEFT, fy0 + fh + 30, USABLE_WIDTH, 240
            draw.rounded_rectangle([sx0, sy0, sx0 + sw, sy0 + sh], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((sx0 + 28, sy0 + 26), "REAL-WORLD INFERENCE THROUGHPUT ADVANTAGE", font=FONT_MONO, fill=TYPE_PRIMARY)

            draw.text((sx0 + 28, sy0 + 75), "5.7x", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 52), fill=ACCENT_BLUE)
            draw.text((sx0 + 170, sy0 + 82), "Higher Generation Throughput (Tokens/s)", font=FONT_BADGE, fill=TYPE_PRIMARY)
            draw.text((sx0 + 170, sy0 + 114), "Memory bandwidth bound shifted directly into compute efficiency", font=FONT_NOTE, fill=TYPE_SECONDARY)

            draw.text((sx0 + 28, sy0 + 155), "128k", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 52), fill=TECH_GREEN)
            draw.text((sx0 + 170, sy0 + 162), "Native Full Context Window Supported", font=FONT_BADGE, fill=TYPE_PRIMARY)
            draw.text((sx0 + 170, sy0 + 194), "Fits complete codebases and research papers comfortably in VRAM", font=FONT_NOTE, fill=TYPE_SECONDARY)

        if render_subs:
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    SUBTITLE_ENGINE.render_subtitle(canvas, text, active_word=word, treatment=1, y_center=1680)
                    break

        return canvas


# ==============================================================================
# SCENE 5: DEEPSEEK-MOE SPARSE ROUTING LATTICE
# ==============================================================================
class Scene5MOERouting:
    def __init__(self, duration: float):
        self.duration = duration
        self.subtitles = [
            ("Scaling to six hundred seventy-one billion total parameters,", "parameters", 0.20, 4.30),
            ("its Mixture-of-Experts engine routes each token to just thirty-seven billion active parameters", "thirty-seven", 4.50, 9.20),
            ("across two hundred fifty-six specialists.", "specialists", 9.40, 12.00),
        ]

    def render_frame(self, t: float, render_subs: bool = True, subs_only: bool = False) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0) if subs_only else THEME_BG)
        draw = ImageDraw.Draw(canvas, "RGBA")

        if not subs_only:
            draw_light_background(canvas)
            draw_header_bar(draw, "SPARSE COMPUTATION // 05", "DEEPSEEK-MOE ROUTING LATTICE", "671B parameters routed to 37B active specialists per token", PURPLE_MOE)

            # Massive Parameter Ratio Banner
            rx0, ry0, rw, rh = GRID_LEFT, 260, USABLE_WIDTH, 140
            draw.rounded_rectangle([rx0, ry0, rx0 + rw, ry0 + rh], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((rx0 + 36, ry0 + 20), "TOTAL PARAMETERS", font=FONT_NOTE, fill=TYPE_MUTED)
            draw.text((rx0 + 36, ry0 + 50), "671 Billion", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 46), fill=TYPE_PRIMARY)

            draw.line([rx0 + rw // 2, ry0 + 20, rx0 + rw // 2, ry0 + rh - 20], fill=THEME_BORDER, width=2)

            draw.text((rx0 + rw // 2 + 36, ry0 + 20), "ACTIVE PARAMETERS PER TOKEN", font=FONT_NOTE, fill=TECH_GREEN)
            draw.text((rx0 + rw // 2 + 36, ry0 + 50), "37 Billion (5.5%)", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 46), fill=TECH_GREEN)

            # 256 Expert Specialists Matrix (16 x 16 Grid)
            gx0, gy0, gw, gh = GRID_LEFT, 430, USABLE_WIDTH, 560
            draw.rounded_rectangle([gx0, gy0, gx0 + gw, gy0 + gh], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((gx0 + 28, gy0 + 24), "FINE-GRAINED SPECIALIST LATTICE: 256 ROUTED EXPERTS", font=FONT_MONO, fill=PURPLE_MOE)

            # Render 16x16 grid of small expert chips
            grid_cols = 16
            grid_rows = 16
            chip_size = 24
            pad_x = (gw - 56 - (grid_cols * chip_size)) // (grid_cols - 1)
            pad_y = 7
            start_x = gx0 + 28
            start_y = gy0 + 70

            # Dynamic simulated active experts based on time t
            active_set = set([
                (int(t * 13 + i * 37) % 256) for i in range(8)
            ])

            for idx in range(256):
                col = idx % grid_cols
                row = idx // grid_cols
                cx = start_x + col * (chip_size + pad_x)
                cy = start_y + row * (chip_size + pad_y)

                if idx in active_set:
                    # Pulsing active expert
                    draw.rounded_rectangle([cx - 2, cy - 2, cx + chip_size + 2, cy + chip_size + 2], radius=6, fill=PURPLE_MOE, outline=(233, 213, 255, 255), width=2)
                else:
                    draw.rounded_rectangle([cx, cy, cx + chip_size, cy + chip_size], radius=4, fill=(241, 245, 249, 255), outline=THEME_BORDER, width=1)

            # Shared Expert Special Banner
            sh_y = start_y + grid_rows * (chip_size + pad_y) + 16
            draw.rounded_rectangle([gx0 + 28, sh_y, gx0 + gw - 28, sh_y + 42], radius=8, fill=(236, 253, 245, 255), outline=TECH_GREEN, width=1)
            draw.text((gx0 + 44, sh_y + 10), "★ 1 Dedicated Shared Expert: Always active to capture shared common knowledge", font=FONT_NOTE, fill=TECH_GREEN)

            # Architectural Innovation Cards
            ix0, iy0, iw, ih = GRID_LEFT, 1020, USABLE_WIDTH, 440
            draw.rounded_rectangle([ix0, iy0, ix0 + iw, iy0 + ih], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((ix0 + 28, iy0 + 24), "DEEPSEEK-MOE STRUCTURAL INNOVATIONS", font=FONT_MONO, fill=ACCENT_BLUE)

            innovations = [
                ("Fine-Grained Segmentation", "Divides traditional massive experts into 256 smaller units, allowing combinations tailored to complex cross-domain tasks."),
                ("Auxiliary-Loss-Free Balancing", "Replaces degrading auxiliary balance loss with dynamic routing bias adjustments, preventing expert collapse without hurting accuracy."),
                ("Extreme Computational Sparsity", "Each token activates only 5.5% of total model weights, achieving 671B capabilities at 37B compute cost."),
                ("Ultra-Fast Training Convergence", "Achieves state-of-the-art loss faster than dense equivalents with identical FLOPS."),
            ]
            for idx, (in_title, in_desc) in enumerate(innovations):
                py = iy0 + 68 + idx * 88
                draw.text((ix0 + 28, py), f"• {in_title}", font=FONT_BADGE, fill=TYPE_PRIMARY)
                draw.text((ix0 + 28, py + 30), in_desc, font=FONT_SUB, fill=TYPE_SECONDARY)

        if render_subs:
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    SUBTITLE_ENGINE.render_subtitle(canvas, text, active_word=word, treatment=1, y_center=1680)
                    break

        return canvas


# ==============================================================================
# SCENE 6: FRONTIER BENCHMARK SHOWDOWN
# ==============================================================================
class Scene6BenchmarkShowdown:
    def __init__(self, duration: float):
        self.duration = duration
        self.subtitles = [
            ("In standardized mathematical and coding benchmarks,", "benchmarks", 0.20, 4.10),
            ("this open-source architecture matches closed frontier models at a fraction of the cost.", "fraction", 4.30, 8.80),
        ]

    def render_frame(self, t: float, render_subs: bool = True, subs_only: bool = False) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0) if subs_only else THEME_BG)
        draw = ImageDraw.Draw(canvas, "RGBA")

        if not subs_only:
            draw_light_background(canvas)
            draw_header_bar(draw, "EMPIRICAL BENCHMARKS // 06", "FRONTIER BENCHMARK SHOWDOWN", "DeepSeek-R1 performance parity against closed frontier systems", GOLD_ACCENT)

            # Benchmark Comparison Card
            cx0, cy0, cw, ch = GRID_LEFT, 260, USABLE_WIDTH, 750
            draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((cx0 + 28, cy0 + 24), "STANDARDIZED REASONING & CODING BENCHMARKS", font=FONT_MONO, fill=TYPE_PRIMARY)

            benchmarks = [
                ("AIME 2024 (Math Olympiad)", 79.8, 79.2, "79.8%", "79.2%"),
                ("MATH-500 (Competition Math)", 97.3, 96.4, "97.3%", "96.4%"),
                ("Codeforces Percentile", 96.3, 96.6, "Top 96.3%", "Top 96.6%"),
                ("MMLU (General Intelligence)", 90.8, 91.8, "90.8%", "91.8%"),
                ("SWE-bench Verified (Coding)", 49.2, 48.9, "49.2%", "48.9%"),
            ]

            by_start = cy0 + 75
            for idx, (b_name, score_r1, score_o1, str_r1, str_o1) in enumerate(benchmarks):
                by = by_start + idx * 130
                draw.text((cx0 + 28, by), b_name, font=FONT_BADGE, fill=TYPE_PRIMARY)

                # Bar 1: DeepSeek-R1 (Emerald Green)
                draw.text((cx0 + 28, by + 34), "DeepSeek-R1", font=FONT_NOTE, fill=TECH_GREEN)
                w_r1 = int((cw - 220) * (score_r1 / 100.0))
                draw.rounded_rectangle([cx0 + 150, by + 32, cx0 + 150 + w_r1, by + 56], radius=6, fill=TECH_GREEN)
                draw.text((cx0 + 160 + w_r1, by + 32), str_r1, font=FONT_BADGE, fill=TECH_GREEN)

                # Bar 2: OpenAI o1 (Dark Slate)
                draw.text((cx0 + 28, by + 68), "OpenAI o1", font=FONT_NOTE, fill=TYPE_SECONDARY)
                w_o1 = int((cw - 220) * (score_o1 / 100.0))
                draw.rounded_rectangle([cx0 + 150, by + 66, cx0 + 150 + w_o1, by + 90], radius=6, fill=(148, 163, 184, 255))
                draw.text((cx0 + 160 + w_o1, by + 66), str_o1, font=FONT_BADGE, fill=TYPE_SECONDARY)

                if idx < len(benchmarks) - 1:
                    draw.line([cx0 + 28, by + 115, cx0 + cw - 28, by + 115], fill=THEME_BORDER, width=1)

            # Massive Economic Disruption Card
            ex0, ey0, ew, eh = GRID_LEFT, 1040, USABLE_WIDTH, 420
            draw.rounded_rectangle([ex0, ey0, ex0 + ew, ey0 + eh], radius=18, fill=THEME_CARD, outline=(167, 243, 208, 255), width=2)
            draw.rectangle([ex0, ey0, ex0 + ew, ey0 + 55], fill=(236, 253, 245, 255))
            draw.text((ex0 + 28, ey0 + 16), "INFERENCE ECONOMICS: 27x COST DISRUPTION", font=FONT_BADGE, fill=TECH_GREEN)

            # Cost Comparison Columns
            col_w = (ew - 80) // 2
            # Left: OpenAI o1
            draw.rounded_rectangle([ex0 + 28, ey0 + 80, ex0 + 28 + col_w, ey0 + 380], radius=14, fill=(248, 250, 252, 255), outline=THEME_BORDER, width=1)
            draw.text((ex0 + 48, ey0 + 100), "OpenAI o1 API", font=FONT_BADGE, fill=TYPE_PRIMARY)
            draw.text((ex0 + 48, ey0 + 140), "$15.00", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 46), fill=SIGNAL_RED)
            draw.text((ex0 + 48, ey0 + 200), "per 1M input tokens", font=FONT_NOTE, fill=TYPE_SECONDARY)
            draw.text((ex0 + 48, ey0 + 240), "$60.00 per 1M output tokens", font=FONT_SUB, fill=TYPE_MUTED)
            draw.text((ex0 + 48, ey0 + 300), "• Closed weights // Proprietary", font=FONT_NOTE, fill=SIGNAL_RED)

            # Right: DeepSeek-R1
            rx = ex0 + 52 + col_w
            draw.rounded_rectangle([rx, ey0 + 80, rx + col_w, ey0 + 380], radius=14, fill=(240, 253, 244, 255), outline=TECH_GREEN, width=2)
            draw.text((rx + 20, ey0 + 100), "DeepSeek-R1 API", font=FONT_BADGE, fill=TECH_GREEN)
            draw.text((rx + 20, ey0 + 140), "$0.55", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 46), fill=TECH_GREEN)
            draw.text((rx + 20, ey0 + 200), "per 1M input tokens (27x cheaper)", font=FONT_NOTE, fill=TECH_GREEN)
            draw.text((rx + 20, ey0 + 240), "$2.19 per 1M output tokens", font=FONT_SUB, fill=TYPE_PRIMARY)
            draw.text((rx + 20, ey0 + 300), "• 100% Free Open Weights via Ollama", font=FONT_NOTE, fill=TECH_GREEN)

        if render_subs:
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    SUBTITLE_ENGINE.render_subtitle(canvas, text, active_word=word, treatment=1, y_center=1680)
                    break

        return canvas


# ==============================================================================
# SCENE 7: THE OPEN REVOLUTION & MIT LICENSE
# ==============================================================================
class Scene7OpenRevolution:
    def __init__(self, duration: float):
        self.duration = duration
        self.subtitles = [
            ("By open-sourcing complete model weights and technical architecture under MIT license,", "MIT license", 0.20, 5.80),
            ("DeepSeek proved that frontier intelligence belongs to the open developer ecosystem.", "developer", 6.00, 10.80),
        ]

    def render_frame(self, t: float, render_subs: bool = True, subs_only: bool = False) -> Image.Image:
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0) if subs_only else THEME_BG)
        draw = ImageDraw.Draw(canvas, "RGBA")

        if not subs_only:
            draw_light_background(canvas)
            draw_header_bar(draw, "THE OPEN FRONTIER // 07", "DEMOCRATIZING FRONTIER INTELLIGENCE", "Complete weights and technical architecture freely released under MIT License", ACCENT_BLUE)

            # Massive MIT License Golden Seal
            lx0, ly0, lw, lh = GRID_LEFT, 260, USABLE_WIDTH, 360
            draw.rounded_rectangle([lx0, ly0, lx0 + lw, ly0 + lh], radius=20, fill=THEME_CARD, outline=(252, 211, 77, 255), width=2)
            draw.rectangle([lx0, ly0, lx0 + lw, ly0 + 55], fill=(254, 252, 232, 255))
            draw.text((lx0 + 28, ly0 + 16), "OFFICIAL LICENSE SPECIFICATION: MIT LICENSE", font=FONT_BADGE, fill=GOLD_ACCENT)

            draw.text((lx0 + 36, ly0 + 80), "UNRESTRICTED FREEDOM TO BUILD", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 36), fill=TYPE_PRIMARY)
            license_terms = [
                ("✓ Free Commercial Deployment", "Deploy in private enterprises without licensing fees or royalties"),
                ("✓ Full Model Distillation Rights", "Freely distill into custom dense models for edge devices and robots"),
                ("✓ Unrestricted Research & Forking", "Inspect internal attention matrices and refine routing kernels"),
            ]
            for idx, (lt_title, lt_desc) in enumerate(license_terms):
                py = ly0 + 140 + idx * 65
                draw.text((lx0 + 36, py), lt_title, font=FONT_BADGE, fill=TECH_GREEN)
                draw.text((lx0 + 36, py + 26), lt_desc, font=FONT_NOTE, fill=TYPE_SECONDARY)

            # Distilled Models Matrix
            dx0, dy0, dw, dh = GRID_LEFT, 650, USABLE_WIDTH, 440
            draw.rounded_rectangle([dx0, dy0, dx0 + dw, dy0 + dh], radius=18, fill=THEME_CARD, outline=THEME_BORDER, width=2)
            draw.text((dx0 + 28, dy0 + 24), "OFFICIAL DISTILLED REASONING SUITE", font=FONT_MONO, fill=PURPLE_MOE)

            distillations = [
                ("DeepSeek-R1-Distill-Qwen-1.5B", "Runs smoothly on smartphones and Raspberry Pi boards"),
                ("DeepSeek-R1-Distill-Qwen-7B", "Beats original non-reasoning GPT-4 on math benchmarks"),
                ("DeepSeek-R1-Distill-Qwen-14B", "Runs on single RTX 3060/4060 laptop GPUs at 40+ tokens/s"),
                ("DeepSeek-R1-Distill-Qwen-32B", "Matches frontier reasoning; runs on 24GB VRAM workstation"),
                ("DeepSeek-R1-Distill-Llama-70B", "Outperforms closed proprietary models across Olympiad math"),
            ]
            for idx, (d_name, d_desc) in enumerate(distillations):
                py = dy0 + 68 + idx * 72
                draw.rounded_rectangle([dx0 + 28, py, dx0 + dw - 28, py + 58], radius=10, fill=(248, 250, 252, 255), outline=THEME_BORDER, width=1)
                draw.text((dx0 + 44, py + 10), d_name, font=FONT_BADGE, fill=TYPE_PRIMARY)
                draw.text((dx0 + 44, py + 34), d_desc, font=FONT_NOTE, fill=TYPE_SECONDARY)

            # Super.intelligencee Channel Closing Callout
            cx0, cy0, cw, ch = GRID_LEFT, 1120, USABLE_WIDTH, 340
            draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=20, fill=THEME_CARD, outline=ACCENT_BLUE, width=3)
            
            # Badge
            draw.rounded_rectangle([cx0 + 28, cy0 + 28, cx0 + 260, cy0 + 68], radius=8, fill=(239, 246, 255, 255), outline=ACCENT_BLUE, width=1)
            draw.text((cx0 + 40, cy0 + 36), "FLAGSHIP SPOTLIGHT", font=FONT_MONO, fill=ACCENT_BLUE)

            draw.text((cx0 + 28, cy0 + 90), "SUPER.INTELLIGENCEEE", font=LAYOUT_ENGINE.get_font("segoeuib.ttf", 46), fill=TYPE_PRIMARY)
            draw.text((cx0 + 28, cy0 + 155), "Daily breakdowns of breakthrough AI repositories, architectures, and papers.", font=FONT_SUB, fill=TYPE_SECONDARY)

            # Call to Action Buttons
            draw.rounded_rectangle([cx0 + 28, cy0 + 225, cx0 + 420, cy0 + 295], radius=14, fill=ACCENT_BLUE)
            draw.text((cx0 + 65, cy0 + 245), "FOLLOW @super.intelligenceee", font=FONT_BADGE, fill=(255, 255, 255, 255))

            draw.rounded_rectangle([cx0 + 450, cy0 + 225, cx0 + cw - 28, cy0 + 295], radius=14, fill=(236, 253, 245, 255), outline=TECH_GREEN, width=2)
            draw.text((cx0 + 485, cy0 + 245), "SUBSCRIBE ON YOUTUBE", font=FONT_BADGE, fill=TECH_GREEN)

        if render_subs:
            for text, word, t0, t1 in self.subtitles:
                if t0 <= t < t1:
                    SUBTITLE_ENGINE.render_subtitle(canvas, text, active_word=word, treatment=1, y_center=1680)
                    break

        return canvas


# ==============================================================================
# PIPELINE EXECUTION ENGINE
# ==============================================================================
def render_single_stream(
    renderer: Any,
    audio_file: Path,
    out_mp4: Path,
    fps: int = 24,
    render_subs: bool = True,
    subs_only: bool = False,
    keyframe_path: Optional[Path] = None
):
    """Pipes PIL generated frames directly into ffmpeg stdin."""
    total_frames = int(renderer.duration * fps)
    cmd_ff = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(fps), "-i", "-",
        "-i", str(audio_file),
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(out_mp4)
    ]
    proc = subprocess.Popen(cmd_ff, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    t_start = time.time()
    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = renderer.render_frame(t, render_subs=render_subs, subs_only=subs_only)
        proc.stdin.write(frame.tobytes())
        if keyframe_path and f_idx == total_frames // 2:
            frame.save(keyframe_path)
            
    proc.stdin.close()
    proc.wait()
    dur = time.time() - t_start
    print(f"    Stream {out_mp4.name} finished in {dur:.1f}s ({total_frames/dur:.1f} fps): {out_mp4.stat().st_size} bytes")


def main():
    print("=" * 80)
    print("PRODUCING FLAGSHIP SPOTLIGHT: deepseek-ai/DeepSeek-R1 (> 60s)")
    print("=" * 80)

    # Read durations manifest
    manifest_path = AUDIO_DIR / "durations.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        durations = json.load(f)

    scenes = [
        (1, "scene1_hook_shockwave", Scene1HookShockwave(durations["scene1_hook_shockwave"]["scene_duration"])),
        (2, "scene2_reasoning_grpo", Scene2ReasoningGRPO(durations["scene2_reasoning_grpo"]["scene_duration"])),
        (3, "scene3_aha_moment", Scene3AhaMoment(durations["scene3_aha_moment"]["scene_duration"])),
        (4, "scene4_mla_architecture", Scene4MLAArchitecture(durations["scene4_mla_architecture"]["scene_duration"])),
        (5, "scene5_moe_routing", Scene5MOERouting(durations["scene5_moe_routing"]["scene_duration"])),
        (6, "scene6_benchmark_showdown", Scene6BenchmarkShowdown(durations["scene6_benchmark_showdown"]["scene_duration"])),
        (7, "scene7_open_revolution", Scene7OpenRevolution(durations["scene7_open_revolution"]["scene_duration"])),
    ]

    total_film_dur = sum(rend.duration for _, _, rend in scenes)
    print(f"Total Master Film Duration: {total_film_dur:.2f}s (> 60s)")

    # 1. RENDER CAPTIONED REVIEW MASTER SCENES
    print("\n--- PASS 1: CAPTIONED REVIEW MASTER SCENES ---")
    cap_scenes = []
    for idx, sid, rend in scenes:
        audio_file = AUDIO_DIR / f"{sid}_master.wav"
        c_mp4 = SCENES_DIR / f"{sid}_captioned.mp4"
        kf_path = KEYFRAMES_DIR / f"{sid}_keyframe.png"
        print(f"\n[SCENE {idx}] Rendering Captioned {sid} ({rend.duration:.2f}s)...")
        render_single_stream(rend, audio_file, c_mp4, render_subs=True, subs_only=False, keyframe_path=kf_path)
        cap_scenes.append(c_mp4)

    # 2. CONCATENATE MASTER FILM
    print("\n" + "=" * 80)
    print(f"CONCATENATING CAPTIONED REVIEW MASTER FILM (Total: {total_film_dur:.2f}s)...")
    print("=" * 80)

    txt_path = PROD_DIR / "concat_master.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for sc in cap_scenes:
            f.write(f"file '{sc.resolve().as_posix()}'\n")

    master_film = PROD_DIR / "deepseek_r1_master.mp4"
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(txt_path), "-c", "copy", str(master_film)]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  [CONCAT SUCCESS] master_film: {master_film.stat().st_size} bytes")

    # 3. EXTRACT 40-FRAME MASTER CONTACT SHEET
    print("\n[CONTACT SHEET] Extracting 40 frames from Captioned Review Master...")
    num_frames = 40
    cols, rows = 5, 8
    step_t = total_film_dur / num_frames

    extracted = []
    for i in range(num_frames):
        tf = i * step_t
        out_f = FRAMES_DIR / f"film_f{i:02d}.png"
        cmd_ext = ["ffmpeg", "-y", "-ss", f"{tf:.3f}", "-i", str(master_film), "-vframes", "1", "-q:v", "2", str(out_f)]
        subprocess.run(cmd_ext, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        extracted.append(out_f)

    tw, th = 320, 568
    pad = 12
    sw = cols * tw + (cols + 1) * pad
    sh = rows * th + (rows + 1) * pad + 60

    sheet = Image.new("RGB", (sw, sh), (248, 249, 250))
    sdraw = ImageDraw.Draw(sheet)
    sdraw.text((pad, 16), f"SUPER.INTELLIGENCEEE // DEEPSEEK-R1 SPOTLIGHT — 40-FRAME MASTER AUDIT ({total_film_dur:.1f}s)", font=FONT_TITLE, fill=TYPE_PRIMARY)

    for idx, ff in enumerate(extracted):
        r = idx // cols
        c = idx % cols
        x = pad + c * (tw + pad)
        y = 60 + pad + r * (th + pad)
        if ff.exists() and ff.stat().st_size > 0:
            im = Image.open(ff).resize((tw, th), Image.Resampling.LANCZOS)
            sheet.paste(im, (x, y))
        sdraw.rectangle([x, y, x + tw, y + th], outline=(203, 213, 225), width=2)
        sdraw.text((x + 8, y + 8), f"#{idx+1:02d} ({idx*step_t:.1f}s)", font=FONT_MONO, fill=TYPE_PRIMARY)

    master_sheet = PROD_DIR / "deepseek_r1_40frame_master_contact_sheet.png"
    sheet.save(master_sheet)
    print(f"  Saved master contact sheet: {master_sheet.name}")

    print("\n" + "=" * 80)
    print("ALL PRODUCTION DELIVERABLES COMPLETED SUCCESSFULLY!")
    print(f"Master Video: {master_film}")
    print(f"Contact Sheet: {master_sheet}")
    print("=" * 80)


if __name__ == "__main__":
    main()
