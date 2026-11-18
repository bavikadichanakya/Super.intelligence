"""
SUPER.INTELLIGENCEEE V2 — HyperFrames Multi-Archetype Template Builder
Constructs deterministic 1080x1920 vertical HTML compositions for HyperFrames rendering.
Supports Stock Video, Sketch whiteboard typography, SVG Motion Diagrams, and GSAP timeline animations.
"""

from __future__ import annotations

import html
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config
from core.schemas import VisualArchetype

logger = logging.getLogger("super_intelligence.template_builder")


class HyperFramesTemplateBuilder:
    """Builds 1080x1920 HyperFrames compositions conforming to the multi-archetype render contract."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.renderer_dir = self.config.resolve_path("renderer")
        self.compositions_dir = self.renderer_dir / "compositions"
        self.assets_dir = self.renderer_dir / "assets"
        self.compositions_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def build_reel_composition(
        self,
        storyboard: Dict[str, Any],
        scene_visuals: List[Path],
        reel_slug: str,
        audio_rel_path: Optional[str] = None,
    ) -> Path:
        """
        Creates a self-contained 1080x1920 vertical HyperFrames HTML composition
        with multi-archetype visual styling and deterministic GSAP timeline.
        """
        scenes = storyboard.get("scenes", [])
        total_duration = sum(float(s.get("duration", s.get("duration_seconds", 5.0))) for s in scenes)
        if total_duration <= 0:
            total_duration = 35.0

        scene_elements = []
        current_time = 0.0

        for i, sc in enumerate(scenes):
            duration = float(sc.get("duration", sc.get("duration_seconds", 5.0)))
            scene_idx = i + 1
            headline = html.escape(sc.get("on_screen_text", sc.get("headline", f"Scene {scene_idx}")))
            badge = html.escape(sc.get("badge", f"PULSE 0{scene_idx} / 0{len(scenes)}"))
            archetype_str = sc.get("visual_archetype", sc.get("visual_type", "editorial_hud"))
            archetype = VisualArchetype.from_str(archetype_str)

            visual_path = scene_visuals[i] if i < len(scene_visuals) else None
            asset_rel = f"assets/{visual_path.name}" if visual_path else ""
            is_video = visual_path and visual_path.suffix.lower() == ".mp4"

            # Media element: video or image
            if is_video:
                media_tag = f'<video class="scene-bg" src="{asset_rel}" autoplay muted loop playsinline></video>'
            else:
                media_tag = f'<img class="scene-bg" src="{asset_rel}" alt="Scene Visual" />'

            # Archetype-specific container class and badges
            badge_icon = "⚡"
            if archetype == VisualArchetype.SKETCH_TITLE:
                badge_icon = "✍️"
            elif archetype == VisualArchetype.SKETCH_STAT:
                badge_icon = "📊"
            elif archetype == VisualArchetype.SKETCH_LIST:
                badge_icon = "📝"
            elif archetype == VisualArchetype.SKETCH_QUOTE:
                badge_icon = "💬"
            elif archetype == VisualArchetype.MOTION_DIAGRAM:
                badge_icon = "📐"
            elif archetype == VisualArchetype.PRODUCT_DEMO:
                badge_icon = "💻"
            elif archetype == VisualArchetype.STOCK_BROLL:
                badge_icon = "🎥"

            scene_html = f"""
      <!-- SCENE {scene_idx} ({archetype.value}) -->
      <div id="scene-{scene_idx}" class="clip scene-container archetype-{archetype.value}" 
           data-start="{current_time:.2f}" 
           data-duration="{duration:.2f}" 
           data-track-index="0"
           data-archetype="{archetype.value}">
        {media_tag}
        <div class="scene-overlay">
          <div class="tech-hud">
            <span class="hud-pill">{badge_icon} {badge}</span>
          </div>
          <div class="headline-wrapper">
            <h2 class="scene-headline">{headline}</h2>
          </div>
        </div>
      </div>
"""
            scene_elements.append(scene_html)
            current_time += duration

        audio_markup = ""
        if audio_rel_path:
            audio_markup = f'<audio id="narration" src="{audio_rel_path}" data-start="0" data-duration="{total_duration:.2f}"></audio>'

        composition_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --ground: #07090e;
        --ink: #f8fafc;
        --cyan: #00e5ff;
        --purple: #8b5cf6;
        --gold: #ffd43b;
        --win-marker: #ffd43b;
        --strike: #e5484d;
        --font-main: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        --font-sketch: "Caveat", cursive, sans-serif;
        --font-mono: "JetBrains Mono", monospace;
      }}
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: var(--ground);
        font-family: var(--font-main);
      }}
      #root {{
        width: 1080px;
        height: 1920px;
        position: relative;
        background: radial-gradient(circle at 50% 30%, #151a2e 0%, #07090e 100%);
        overflow: hidden;
      }}
      .scene-container {{
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .scene-bg {{
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        object-fit: cover;
      }}
      .scene-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 240px 80px 340px 80px;
        pointer-events: none;
      }}
      .tech-hud {{
        display: flex;
        justify-content: center;
      }}
      .hud-pill {{
        background: rgba(14, 20, 36, 0.88);
        color: var(--cyan);
        border: 2px solid var(--cyan);
        padding: 12px 32px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 24px;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.25);
        backdrop-filter: blur(8px);
      }}
      .archetype-sketch_title .hud-pill,
      .archetype-sketch_stat .hud-pill,
      .archetype-sketch_list .hud-pill,
      .archetype-sketch_quote .hud-pill {{
        color: var(--gold);
        border-color: var(--gold);
        box-shadow: 0 0 20px rgba(255, 212, 59, 0.25);
      }}
      .headline-wrapper {{
        width: 100%;
        display: flex;
        justify-content: center;
      }}
      .scene-headline {{
        color: var(--ink);
        font-size: 54px;
        font-weight: 800;
        text-align: center;
        line-height: 1.25;
        letter-spacing: -0.5px;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.9);
      }}
      .archetype-sketch_title .scene-headline,
      .archetype-sketch_stat .scene-headline,
      .archetype-sketch_quote .scene-headline {{
        font-family: var(--font-sketch);
        font-size: 64px;
        line-height: 1.15;
      }}
      .scanlines {{
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
        background-size: 100% 4px;
        pointer-events: none;
        z-index: 10;
        opacity: 0.35;
      }}
    </style>
  </head>
  <body>
    <div id="root"
         data-composition-id="main"
         data-start="0"
         data-duration="{total_duration:.2f}"
         data-width="1080"
         data-height="1920"
         data-fps="30">
      
      {''.join(scene_elements)}
      
      <div class="scanlines"></div>
      {audio_markup}
    </div>

    <script>
      // HyperFrames Paused Timeline Contract
      const tl = gsap.timeline({{ paused: true }});
      
      const sceneCount = {len(scenes)};
      let curStart = 0;
      
      for (let s = 1; s <= sceneCount; s++) {{
        const scEl = document.querySelector("#scene-" + s);
        if (!scEl) continue;
        const sDur = parseFloat(scEl.getAttribute("data-duration") || "5.0");
        const bg = scEl.querySelector(".scene-bg");
        const title = scEl.querySelector(".scene-headline");
        const pill = scEl.querySelector(".hud-pill");
        
        // Background push
        if (bg) {{
          tl.fromTo(bg, 
            {{ scale: 1.0, transformOrigin: "50% 50%" }}, 
            {{ scale: 1.04, duration: sDur, ease: "none" }}, 
            curStart
          );
        }}
        
        // HUD pill pulse
        if (pill) {{
          tl.fromTo(pill,
            {{ opacity: 0, scale: 0.9 }},
            {{ opacity: 1, scale: 1.0, duration: 0.4, ease: "back.out(1.5)" }},
            curStart + 0.1
          );
        }}

        // Headline entrance
        if (title) {{
          tl.fromTo(title, 
            {{ opacity: 0, y: 25 }}, 
            {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }}, 
            curStart + 0.2
          );
        }}
        
        curStart += sDur;
      }}
      
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
        # Save to composition file
        comp_file = self.compositions_dir / f"{reel_slug}.html"
        with open(comp_file, "w", encoding="utf-8") as f:
            f.write(composition_html)

        # Also write to index.html so HyperFrames root always has active composition
        index_file = self.renderer_dir / "index.html"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(composition_html)

        logger.info(f"Built HyperFrames composition ({comp_file.name}, duration: {total_duration:.1f}s)")
        return comp_file
