"""
Tests for Visuals and Video subsystems: Pillow editorial graphics, stock provider, template builder, validator.
"""

import pytest
from pathlib import Path
from PIL import Image
from visuals.graphics import EditorialGraphicsGenerator
from visuals.stock_provider import StockProvider
from video.template_builder import HyperFramesTemplateBuilder
from video.video_validator import VideoValidator

def test_editorial_graphics_generator(tmp_path):
    gen = EditorialGraphicsGenerator()
    
    # 1. Title card
    title_path = tmp_path / "test_title.png"
    gen.create_title_card("MILLION TOKEN CONTEXT SCALED", "AI BENCHMARKS", title_path)
    assert title_path.exists()
    with Image.open(title_path) as im:
        assert im.size == (1080, 1920)
        
    # 2. Stat card
    stat_path = tmp_path / "test_stat.png"
    gen.create_stat_card("INFERENCE SPEEDUP", "4.2X", "Linear memory scaling demonstrated.", stat_path)
    assert stat_path.exists()
    with Image.open(stat_path) as im:
        assert im.size == (1080, 1920)

def test_template_builder(tmp_path):
    builder = HyperFramesTemplateBuilder()
    dummy_storyboard = {
        "scenes": [
            {"scene_index": 1, "duration": 4.0, "on_screen_text": "HOOK HEADLINE"},
            {"scene_index": 2, "duration": 5.0, "on_screen_text": "DEVELOPMENT DETAILS"}
        ]
    }
    visual1 = tmp_path / "v1.png"
    visual2 = tmp_path / "v2.png"
    Image.new("RGB", (1080, 1920), (10, 12, 18)).save(visual1)
    Image.new("RGB", (1080, 1920), (10, 12, 18)).save(visual2)
    
    comp_path = builder.build_reel_composition(
        storyboard=dummy_storyboard,
        scene_visuals=[visual1, visual2],
        reel_slug="test_composition"
    )
    assert comp_path.exists()
    content = comp_path.read_text(encoding="utf-8")
    assert 'data-width="1080"' in content
    assert 'data-height="1920"' in content
    assert 'gsap.timeline' in content

