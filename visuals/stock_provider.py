"""
SUPER.INTELLIGENCEEE V2 — Stock Visual Provider Module
Zero-budget visual provider: delegates to the VisualRouter to resolve, synthesize,
and cache multi-archetype assets with full provenance tracking.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from core.config import get_config
from core.database import Database
from core.schemas import UniversalScene
from visuals.visual_router import VisualRouter

logger = logging.getLogger("super_intelligence.stock_provider")


class StockProvider:
    """Provides high-quality, legally verified visuals for storyboard scenes at zero cost."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()
        self.router = VisualRouter(self.db, self.config)
        self.renders_assets_dir = self.config.resolve_path("renderer/assets")
        self.renders_assets_dir.mkdir(parents=True, exist_ok=True)

    def prepare_scene_visual(
        self,
        scene: Union[Dict[str, Any], UniversalScene],
        scene_index: int,
        total_scenes: int,
        reel_slug: str,
        brief: Optional[Any] = None,
        manifest: Optional[Any] = None,
    ) -> Path:
        """
        Ensures a valid visual asset exists for the scene by dispatching to the multi-archetype VisualRouter
        or the ProductionModeDispatcher.
        """
        return self.router.prepare_scene_visual(
            scene=scene,
            scene_index=scene_index,
            total_scenes=total_scenes,
            reel_slug=reel_slug,
            brief=brief,
            manifest=manifest,
        )
