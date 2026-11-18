"""
SUPER.INTELLIGENCEEE — Unit Tests for Text Layout Engine & Subtitle Validator
Validates multi-line wrapping, token protection, safe-area bounds, and collision checks.
"""

import unittest
from pathlib import Path
from rendering.text_layout_engine import TextLayoutEngine, TextAlignment, OverflowPolicy
from rendering.advanced_subtitle_engine import AdvancedSubtitleEngine
from rendering.automated_layout_validator import AutomatedLayoutValidator, LayoutElement


class TestTextLayoutEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = TextLayoutEngine()
        cls.sub_engine = AdvancedSubtitleEngine(cls.engine)
        cls.validator = AutomatedLayoutValidator()

    def test_short_text_single_line(self):
        box = self.engine.layout_text(
            text="Willow QPU",
            font_name_or_path="segoeuib.ttf",
            target_size=40,
            max_width=500
        )
        self.assertEqual(len(box.lines), 1)
        self.assertEqual(box.lines[0], "Willow QPU")
        self.assertLessEqual(box.total_width, 500)

    def test_long_text_wrapping(self):
        text = "Ever wondered why the world's most powerful quantum computers look like giant golden chandeliers hanging inside a frozen void?"
        box = self.engine.layout_text(
            text=text,
            font_name_or_path="segoeuib.ttf",
            target_size=38,
            max_width=900,
            max_lines=3
        )
        self.assertGreater(len(box.lines), 1)
        self.assertLessEqual(len(box.lines), 3)
        for line in box.lines:
            w, _ = self.engine.measure_text(line, box.font)
            self.assertLessEqual(w, 900)

    def test_scientific_terms_preservation(self):
        text = "Superconducting transmon qubits operate at ten millikelvin with dilution loop heat exchangers."
        box = self.engine.layout_text(
            text=text,
            font_name_or_path="segoeui.ttf",
            target_size=28,
            max_width=600
        )
        # Verify no word is broken in half
        joined = " ".join(box.lines)
        self.assertEqual(joined, text)

    def test_numbers_and_units_not_split(self):
        text = "Target temperature is 10 mK and pulse duration is 840 ns across distance 7."
        box = self.engine.layout_text(
            text=text,
            font_name_or_path="consolab.ttf",
            target_size=26,
            max_width=450
        )
        joined = " ".join(box.lines)
        self.assertIn("10 mK", joined)
        self.assertIn("840 ns", joined)

    def test_mathematical_expressions(self):
        text = "Empirical scaling Lambda = 0.79 +/- 0.02 verified with error e_L = 1.4 x 10^-3."
        box = self.engine.layout_text(
            text=text,
            font_name_or_path="consolab.ttf",
            target_size=24,
            max_width=500
        )
        self.assertLessEqual(box.total_width, 500)

    def test_narrow_container_reduce_font_size(self):
        text = "COMPUTATIONAL SUPREMACY BENCHMARK"
        box = self.engine.layout_text(
            text=text,
            font_name_or_path="segoeuib.ttf",
            target_size=40,
            max_width=300,
            max_lines=2,
            min_font_size=22,
            policy=OverflowPolicy.REDUCE_FONT_SIZE
        )
        self.assertLessEqual(box.total_width, 300)
        self.assertLessEqual(box.actual_font_size, 40)

    def test_subtitle_safe_area_validation(self):
        phrase = "Ever wondered why the world's most powerful quantum computers look like giant golden chandeliers hanging inside a frozen void?"
        box = self.sub_engine.compute_subtitle_layout(phrase, treatment=1, y_center=1680)
        valid, violations = self.sub_engine.validate_safe_area(box)
        self.assertTrue(valid, f"Subtitle violated safe area: {violations}")

    def test_layout_validator_collision_detection(self):
        self.validator.clear()
        elem1 = LayoutElement("title", "title", 100, 100, 300, 50, "TITLE", 40)
        elem2 = LayoutElement("subtitle", "subtitle", 250, 120, 200, 40, "SUBTITLE", 24)
        issues = self.validator.validate_scene_layout("test_scene", 0.0, [elem1, elem2])
        collision_issues = [i for i in issues if i.rule_violated == "TEXT_COLLISION"]
        self.assertGreater(len(collision_issues), 0)

    def test_layout_validator_frame_overflow(self):
        self.validator.clear()
        # Element positioned too close to right edge (x=1050, w=100 -> x+w=1150 > 1020)
        elem = LayoutElement("bad_tag", "annotation", 1000, 500, 120, 30, "OVERFLOW", 24)
        issues = self.validator.validate_scene_layout("test_scene", 0.0, [elem])
        overflow_issues = [i for i in issues if i.rule_violated == "RIGHT_FRAME_OVERFLOW"]
        self.assertGreater(len(overflow_issues), 0)


if __name__ == "__main__":
    unittest.main()
