"""
Test vertical 1080x1920 render with Manim Community v0.22.1 (using Pango & Cairo vector rendering)
"""
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.background_color = "#07090e"

class VerticalFormulaTest(Scene):
    def construct(self):
        # 1. Title with cyan tech styling
        title = Text("COMPUTATIONAL COMPLEXITY", font_size=44, color="#00e5ff", weight=BOLD)
        title.to_edge(UP, buff=2.5)

        # 2. Vector Ring / Target
        ring = Circle(radius=1.8, color="#00e5ff", stroke_width=4)
        ring.next_to(title, DOWN, buff=1.0)
        
        # 3. Mathematical text using Pango (Zero LaTeX dependency required)
        formula = Text("O(N log N)", font_size=72, color="#ffd43b", weight=BOLD)
        formula.move_to(ring.get_center())

        # 4. Metric tag
        sub = Text("Sub-Quadratic Scaling Proof", font_size=32, color="#94a3b8")
        sub.next_to(ring, DOWN, buff=1.0)

        # 5. Coordinate curve
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 100, 20],
            x_length=6,
            y_length=4,
            axis_config={"color": "#334155", "stroke_width": 2},
        )
        axes.next_to(sub, DOWN, buff=1.0)
        curve = axes.plot(lambda x: x * 2.3 * (1 + 0.5 * x), color="#8b5cf6", stroke_width=4)

        # Animation sequence
        self.play(FadeIn(title, shift=UP * 0.5), run_time=0.4)
        self.play(Create(ring), Write(formula), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.3)
        self.play(Create(axes), Create(curve), run_time=0.7)
        self.wait(0.5)
