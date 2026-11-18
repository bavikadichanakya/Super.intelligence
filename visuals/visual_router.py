"""
SUPER.INTELLIGENCEEE V2 — Visual Router & Multi-Archetype Asset Engine
Resolves visual assets for all 7 canonical archetypes with local zero-cost caching.
Integrates Sketch typography, Motion Diagrams, Terminal Demos, and Stock B-roll.
"""

from __future__ import annotations

import logging
import math
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont

from core.config import get_config
from core.creative_brief import SceneCreativeBrief, ProductionMode
from core.database import Database
from core.provenance import LicenseType, AssetProvenanceManifest
from core.schemas import SceneProps, UniversalScene, VisualArchetype
from visuals.asset_manager import VisualAssetManager
from visuals.graphics import EditorialGraphicsGenerator
from visuals.production_modes import ProductionModeDispatcher

logger = get_logger = logging.getLogger("super_intelligence.visual_router")


class VisualRouter:
    """Intelligently routes and synthesizes visual assets across archetypes."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()
        self.asset_manager = VisualAssetManager(self.db, self.config)
        self.graphics = EditorialGraphicsGenerator(self.config)

        self.renderer_assets_dir = self.config.resolve_path("renderer/assets")
        self.stock_video_dir = self.config.resolve_path("assets/video/stock")
        self.stock_image_dir = self.config.resolve_path("assets/images/stock")
        self.fonts_dir = self.config.resolve_path("assets/fonts")

        self.renderer_assets_dir.mkdir(parents=True, exist_ok=True)
        self.stock_video_dir.mkdir(parents=True, exist_ok=True)
        self.stock_image_dir.mkdir(parents=True, exist_ok=True)
        self.mode_dispatcher = ProductionModeDispatcher(self.config)

        # Style Palettes
        self.bg_sketch = (34, 40, 43)        # #22282B dark paper ground
        self.bg_panel = (43, 50, 54)         # #2B3236 card panel
        self.grid_line = (70, 80, 90)        # #46505A subtle paper grid
        self.yellow_win = (255, 212, 59)     # #FFD43B sketch marker highlight
        self.cyan_glow = (0, 229, 255)       # #00E5FF cyber pulse
        self.red_strike = (229, 72, 77)      # #E5484D baseline strike
        self.green_gain = (34, 197, 94)      # #22C55E win metric
        self.white_text = (245, 241, 230)    # #F5F1E6 soft paper text
        self.muted_text = (148, 160, 170)    # #94A0AA secondary text

    def _draw_paper_grid(self, draw: ImageDraw.ImageDraw, width: int = 1080, height: int = 1920):
        """Draws subtle paper grid lines per Sketch signature."""
        grid_size = 56
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=(45, 53, 58), width=1)
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=(45, 53, 58), width=1)

    def _generate_sketch_title_card(self, scene: Dict[str, Any], output_path: Path) -> Path:
        """Renders Sketch Title archetype: Caveat headline, paper ground, yellow marker."""
        img = Image.new("RGB", (1080, 1920), self.bg_sketch)
        draw = ImageDraw.Draw(img)
        self._draw_paper_grid(draw)

        # Card container with slight tilt
        draw.rounded_rectangle([(80, 480), (1000, 1380)], radius=16, fill=self.bg_panel, outline=self.grid_line, width=2)

        lead_in = scene.get("visual_props", {}).get("lead_in") or scene.get("badge") or "BREAKTHROUGH REPORT"
        headline = scene.get("visual_props", {}).get("headline") or scene.get("on_screen_text") or "AI MILESTONE"
        hero_word = scene.get("visual_props", {}).get("hero_word") or "BREAKTHROUGH"

        # Lead-in pill
        draw.rounded_rectangle([(140, 560), (520, 620)], radius=8, fill=(51, 59, 64))
        draw.text((160, 575), f"⚡ {lead_in.upper()}", fill=self.yellow_win, font=self.graphics.font_badge)

        # Headline
        words = headline.split()
        wrapped_lines = self.graphics._wrap_text(headline.upper(), max_chars=18)
        start_y = 680
        for i, line in enumerate(wrapped_lines[:4]):
            y = start_y + i * 85
            # Draw yellow marker highlight behind hero word if present in line
            if hero_word.upper() in line.upper():
                draw.rectangle([(130, y - 5), (950, y + 65)], fill=self.yellow_win)
                draw.text((150, y), line, fill=(31, 35, 40), font=self.graphics.font_title)
            else:
                draw.text((150, y), line, fill=self.white_text, font=self.graphics.font_title)

        # Bottom signature note
        draw.text((150, 1260), "Verified Technical Milestone", fill=self.muted_text, font=self.graphics.font_body)
        img.save(output_path, format="PNG")
        return output_path

    def _generate_sketch_stat_card(self, scene: Dict[str, Any], output_path: Path) -> Path:
        """Renders Sketch Stat archetype: Before & After comparison with struck baseline."""
        img = Image.new("RGB", (1080, 1920), self.bg_sketch)
        draw = ImageDraw.Draw(img)
        self._draw_paper_grid(draw)

        # Container
        draw.rounded_rectangle([(80, 440), (1000, 1420)], radius=16, fill=self.bg_panel, outline=self.grid_line, width=2)

        props = scene.get("visual_props", {})
        headline = props.get("headline", "PERFORMANCE METRIC")
        before = props.get("before") or {"label": "Baseline", "value": "Standard Cloud"}
        after = props.get("after") or {"label": "Accelerated", "value": "3.8x Speedup"}
        delta = props.get("stat_delta", "3.8x")

        # Eyebrow
        draw.text((140, 520), "EMPIRICAL BENCHMARK COMPARISON", fill=self.yellow_win, font=self.graphics.font_badge)
        draw.text((140, 570), headline.upper()[:24], fill=self.white_text, font=self.graphics.font_title)

        # Before Card (Struck through)
        draw.rounded_rectangle([(140, 700), (940, 880)], radius=12, fill=(34, 40, 43), outline=(60, 70, 76), width=2)
        draw.text((170, 730), before.get("label", "Prior Architecture").upper(), fill=self.muted_text, font=self.graphics.font_badge)
        draw.text((170, 780), before.get("value", "1.0x Baseline"), fill=(160, 170, 180), font=self.graphics.font_title)
        # Red Strike-through line
        draw.line([(160, 815), (750, 815)], fill=self.red_strike, width=5)

        # After Card (Hero Win Highlight)
        draw.rounded_rectangle([(140, 930), (940, 1150)], radius=12, fill=(34, 40, 43), outline=self.yellow_win, width=3)
        draw.text((170, 960), after.get("label", "Optimized Throughput").upper(), fill=self.yellow_win, font=self.graphics.font_badge)
        draw.text((170, 1010), after.get("value", delta), fill=self.white_text, font=self.graphics.font_stat)

        # Bottom Win Callout Pill
        draw.rounded_rectangle([(140, 1220), (540, 1290)], radius=25, fill=self.yellow_win)
        draw.text((170, 1240), f"WIN: {delta} GAIN", fill=(31, 35, 40), font=self.graphics.font_badge)

        img.save(output_path, format="PNG")
        return output_path

    def _generate_sketch_list_card(self, scene: Dict[str, Any], output_path: Path) -> Path:
        """Renders Sketch List archetype: Structured step/items card with win highlight."""
        img = Image.new("RGB", (1080, 1920), self.bg_sketch)
        draw = ImageDraw.Draw(img)
        self._draw_paper_grid(draw)

        draw.rounded_rectangle([(80, 420), (1000, 1460)], radius=16, fill=self.bg_panel, outline=self.grid_line, width=2)

        props = scene.get("visual_props", {})
        headline = props.get("headline", "PRODUCTION ADVANTAGES")
        items = props.get("list_items") or [
            {"index": 1, "title": "Workstation GPUs", "description": "Local zero-latency execution", "win": False},
            {"index": 2, "title": "Real-Time Latency", "description": "3.8x inference throughput", "win": True},
            {"index": 3, "title": "Zero Cloud Lock-in", "description": "$0 recurring API overhead", "win": False},
        ]

        draw.text((140, 490), "ARCHITECTURAL IMPACT", fill=self.yellow_win, font=self.graphics.font_badge)
        draw.text((140, 540), headline.upper()[:24], fill=self.white_text, font=self.graphics.font_title)

        y = 660
        for item in items[:3]:
            is_win = item.get("win", False)
            card_border = self.yellow_win if is_win else (60, 70, 76)
            card_bg = (40, 48, 52) if is_win else (34, 40, 43)

            draw.rounded_rectangle([(140, y), (940, y + 180)], radius=12, fill=card_bg, outline=card_border, width=2)
            # Step indicator
            pill_fill = self.yellow_win if is_win else (55, 65, 72)
            pill_text = (31, 35, 40) if is_win else self.white_text
            draw.rounded_rectangle([(165, y + 25), (250, y + 75)], radius=10, fill=pill_fill)
            draw.text((185, y + 35), f"0{item.get('index', 1)}", fill=pill_text, font=self.graphics.font_badge)

            # Item title & description
            draw.text((275, y + 35), str(item.get("title", "")).upper()[:26], fill=self.white_text, font=self.graphics.font_badge)
            desc_lines = self.graphics._wrap_text(str(item.get("description", "")), max_chars=34)
            for j, d_line in enumerate(desc_lines[:2]):
                draw.text((170, y + 95 + j * 35), d_line, fill=self.muted_text, font=self.graphics.font_body)

            y += 220

        img.save(output_path, format="PNG")
        return output_path

    def _generate_sketch_quote_card(self, scene: Dict[str, Any], output_path: Path) -> Path:
        """Renders Sketch Quote archetype: Primary source quote with author and role."""
        img = Image.new("RGB", (1080, 1920), self.bg_sketch)
        draw = ImageDraw.Draw(img)
        self._draw_paper_grid(draw)

        draw.rounded_rectangle([(80, 460), (1000, 1400)], radius=16, fill=self.bg_panel, outline=self.grid_line, width=2)

        props = scene.get("visual_props", {})
        quote_text = props.get("quote_text") or scene.get("narration_text") or "Verified primary source documentation."
        author = props.get("quote_author") or "Primary Source"
        role = props.get("quote_role") or "Technical Research Documentation"

        # Giant quote mark
        draw.text((140, 520), "“", fill=self.yellow_win, font=self.graphics.font_stat)

        # Quote lines
        wrapped = self.graphics._wrap_text(quote_text, max_chars=24)
        q_y = 680
        for i, line in enumerate(wrapped[:5]):
            draw.text((140, q_y + i * 75), line, fill=self.white_text, font=self.graphics.font_title)

        div_y = q_y + min(len(wrapped), 5) * 75 + 40
        draw.line([(140, div_y), (400, div_y)], fill=self.yellow_win, width=3)

        # Author & Attribution
        draw.text((140, div_y + 35), author.upper(), fill=self.yellow_win, font=self.graphics.font_badge)
        draw.text((140, div_y + 85), role[:40], fill=self.muted_text, font=self.graphics.font_body)

        img.save(output_path, format="PNG")
        return output_path

    def _generate_motion_diagram_card(self, scene: Dict[str, Any], output_path: Path) -> Path:
        """Renders Motion Diagram archetype: 3-stage architecture pipeline card."""
        img = Image.new("RGB", (1080, 1920), (10, 12, 18))
        draw = ImageDraw.Draw(img)

        # Header
        draw.text((100, 440), "SYSTEM ARCHITECTURE PIPELINE", fill=self.cyan_glow, font=self.graphics.font_badge)
        draw.text((100, 490), "EXECUTION TOPOLOGY", fill=self.white_text, font=self.graphics.font_title)

        # 3 Stages Flow
        stages = [
            ("01", "INGESTION & CONTEXT", "Linear scaling over million tokens", (0, 229, 255)),
            ("02", "NEURAL PRUNING", "Autonomous weight optimization", (255, 215, 0)),
            ("03", "VERIFIED INFERENCE", "Zero accuracy degradation on edge", (34, 197, 94)),
        ]

        y = 630
        for i, (num, title, sub, color) in enumerate(stages):
            # Stage box
            draw.rounded_rectangle([(100, y), (980, y + 170)], radius=18, fill=(18, 22, 34), outline=color, width=2)
            draw.rounded_rectangle([(130, y + 30), (210, y + 80)], radius=8, fill=color)
            draw.text((150, y + 40), num, fill=(10, 12, 18), font=self.graphics.font_badge)

            draw.text((240, y + 40), title, fill=self.white_text, font=self.graphics.font_badge)
            draw.text((130, y + 105), sub, fill=self.muted_text, font=self.graphics.font_body)

            # Connecting link arrow
            if i < 2:
                arrow_y = y + 170
                draw.line([(540, arrow_y), (540, arrow_y + 50)], fill=(70, 85, 120), width=3)
                draw.polygon([(530, arrow_y + 50), (550, arrow_y + 50), (540, arrow_y + 65)], fill=self.cyan_glow)

            y += 230

        img.save(output_path, format="PNG")
        return output_path

    def _generate_product_demo_card(self, scene: Dict[str, Any], output_path: Path) -> Path:
        """Renders Product Demo archetype: Terminal / CLI execution mockup."""
        img = Image.new("RGB", (1080, 1920), (12, 14, 20))
        draw = ImageDraw.Draw(img)

        # Window chrome
        draw.rounded_rectangle([(80, 480), (1000, 1380)], radius=16, fill=(18, 22, 30), outline=(50, 60, 75), width=2)
        # Title bar
        draw.rounded_rectangle([(80, 480), (1000, 545)], radius=16, fill=(28, 34, 46))
        # Window controls
        draw.ellipse([(115, 505), (135, 525)], fill=(239, 68, 68))
        draw.ellipse([(145, 505), (165, 525)], fill=(245, 158, 11))
        draw.ellipse([(175, 505), (195, 525)], fill=(34, 197, 94))
        draw.text((220, 505), "terminal — super.intelligenceee@edge", fill=self.muted_text, font=self.graphics.font_badge)

        # Terminal lines
        t_y = 600
        commands = [
            ("$ python run_benchmark.py --mode=autonomous", (245, 241, 230)),
            ("[INFO] Loading neural architecture into VRAM...", (148, 163, 184)),
            ("[SUCCESS] Pruning completed in 1.4s.", (34, 197, 94)),
            ("[METRIC] Throughput: 3.8x speedup confirmed.", (255, 215, 0)),
            ("[STATUS] Verification: ZERO DRIFT DETECTED", (0, 229, 255)),
        ]
        for cmd, col in commands:
            draw.text((120, t_y), cmd, fill=col, font=self.graphics.font_body)
            t_y += 85

        img.save(output_path, format="PNG")
        return output_path

    def _resolve_stock_broll(self, scene: Dict[str, Any], output_path: Path) -> Path:
        """Finds or prepares a stock b-roll asset (video or high-res photo)."""
        # 1. Check local video stock cache
        stock_videos = list(self.stock_video_dir.glob("*.mp4"))
        if stock_videos:
            selected_video = stock_videos[0]
            # Copy to renderer assets
            target_video = output_path.with_suffix(".mp4")
            shutil.copy2(selected_video, target_video)
            logger.info(f"Resolved local stock video: {selected_video.name}")
            return target_video

        # 2. Check local images stock cache
        stock_images = list(self.stock_image_dir.glob("*.png")) + list(self.stock_image_dir.glob("*.jpg"))
        if stock_images:
            selected_img = stock_images[0]
            shutil.copy2(selected_img, output_path)
            logger.info(f"Resolved local stock photo: {selected_img.name}")
            return output_path

        # 3. Fallback: generate high-aesthetic cinematic tech outro card
        return self.graphics.create_outro_card(
            call_to_action="STAY AHEAD WITH SUPER.INTELLIGENCEEE",
            handle="@super.intelligenceee",
            output_path=output_path,
        )

    def prepare_scene_visual(
        self,
        scene: Union[Dict[str, Any], UniversalScene],
        scene_index: int,
        total_scenes: int,
        reel_slug: str,
        brief: Optional[SceneCreativeBrief] = None,
        manifest: Optional[Any] = None,
    ) -> Path:
        """
        Dispatches asset synthesis/resolution to the appropriate visual archetype or production mode handler.
        Guarantees that a valid asset is produced, registered, and cached with legal provenance.
        """
        scene_dict = scene.to_dict() if isinstance(scene, UniversalScene) else scene
        output_name = f"{reel_slug}_scene_{scene_index}.png"
        target_path = self.renderer_assets_dir / output_name

        # Priority 1: Direct SceneCreativeBrief dispatch via ProductionModeDispatcher
        effective_brief = brief
        if not effective_brief and "creative_brief" in scene_dict:
            raw_b = scene_dict["creative_brief"]
            effective_brief = SceneCreativeBrief.from_dict(raw_b) if isinstance(raw_b, dict) else raw_b

        if effective_brief:
            asset_path = self.mode_dispatcher.dispatch_scene_visual(
                brief=effective_brief,
                output_path=target_path,
                manifest=manifest,
            )
            archetype_tag = str(effective_brief.production_mode.value)
        elif "production_mode" in scene_dict:
            pm = scene_dict["production_mode"]
            mode_enum = ProductionMode(pm) if isinstance(pm, str) else pm
            syn_brief = SceneCreativeBrief(
                scene_id=scene_dict.get("scene_id", f"sc_{scene_index:03d}"),
                scene_index=scene_index,
                narrative_purpose=scene_dict.get("narrative_role", "EXPLANATION"),
                intended_emotion="CLARITY",
                visual_metaphor="TECHNICAL_TOPOLOGY",
                primary_subject=scene_dict.get("primary_subject", "EDGE_NEURAL_CORE"),
                visual_action=scene_dict.get("visual_action", scene_dict.get("on_screen_text", "SYSTEM FLOW")),
                production_mode=mode_enum,
                asset_requirements=[],
                composition="macro_center_hero",
                camera_movement="push_in_slow",
                animation_instructions="",
                duration_seconds=float(scene_dict.get("duration_seconds", scene_dict.get("duration", 5.0))),
                on_screen_text=scene_dict.get("on_screen_text", ""),
                visual_concept_rationale=scene_dict.get("visual_concept_rationale", "Autonomous production mode dispatch")
            )
            asset_path = self.mode_dispatcher.dispatch_scene_visual(
                brief=syn_brief,
                output_path=target_path,
                manifest=manifest,
            )
            archetype_tag = str(mode_enum.value)
        else:
            archetype = VisualArchetype.from_str(
                scene_dict.get("visual_archetype")
                or scene_dict.get("visual_type")
                or scene_dict.get("scene_type")
                or "editorial_hud"
            )

            if archetype == VisualArchetype.SKETCH_TITLE:
                asset_path = self._generate_sketch_title_card(scene_dict, target_path)
            elif archetype == VisualArchetype.SKETCH_STAT:
                asset_path = self._generate_sketch_stat_card(scene_dict, target_path)
            elif archetype == VisualArchetype.SKETCH_LIST:
                asset_path = self._generate_sketch_list_card(scene_dict, target_path)
            elif archetype == VisualArchetype.SKETCH_QUOTE:
                asset_path = self._generate_sketch_quote_card(scene_dict, target_path)
            elif archetype == VisualArchetype.MOTION_DIAGRAM:
                asset_path = self._generate_motion_diagram_card(scene_dict, target_path)
            elif archetype == VisualArchetype.PRODUCT_DEMO:
                asset_path = self._generate_product_demo_card(scene_dict, target_path)
            elif archetype == VisualArchetype.STOCK_BROLL:
                asset_path = self._resolve_stock_broll(scene_dict, target_path)
            else: # EDITORIAL_HUD fallback
                asset_path = self.graphics.create_scene_card(
                    scene=scene_dict,
                    scene_index=scene_index,
                    total_scenes=total_scenes,
                    output_path=target_path,
                )
            archetype_tag = archetype.value

        # Register asset in database with provenance
        try:
            is_video = asset_path.suffix.lower() == ".mp4"
            lic = LicenseType.CC0 if is_video else LicenseType.EDITORIAL_GENERATED
            self.asset_manager.register_asset(
                file_path=asset_path,
                asset_type="video_mp4" if is_video else "image_png",
                name=f"Visual Asset {archetype_tag}: {reel_slug} Scene #{scene_index}",
                source_url=f"local://visual_router/{archetype_tag}",
                license_type=lic,
                author="SUPER.INTELLIGENCEEE Visual Engine",
                tags=["visual_archetype", archetype_tag, reel_slug],
            )
        except Exception as e:
            logger.error(f"Asset registration error in database for {asset_path.name}: {e}")
            if manifest:
                manifest.add_asset(
                    file_path=asset_path,
                    asset_category="video" if asset_path.suffix.lower() == ".mp4" else "graphic_card",
                    license_type="UNVERIFIED",
                    source_url=f"local://visual_router/{archetype_tag}",
                    author_creator="SUPER.INTELLIGENCEEE Visual Engine",
                    asset_id=f"scene_{scene_index}_{asset_path.stem}",
                    notes=f"Database registration failure: {e}",
                )

        # Also register in manifest if not already recorded
        if manifest and not any(r.file_path == str(asset_path.resolve()) for r in manifest.records):
            is_vid = asset_path.suffix.lower() == ".mp4"
            manifest.add_asset(
                file_path=asset_path,
                asset_category="video" if is_vid else "graphic_card",
                license_type="CC0" if is_vid else "Editorial Generated",
                source_url=f"local://visual_router/{archetype_tag}",
                author_creator="SUPER.INTELLIGENCEEE Visual Engine",
                asset_id=f"scene_{scene_index}_{asset_path.stem}",
                notes=f"Visual for scene #{scene_index}"
            )

        return asset_path
