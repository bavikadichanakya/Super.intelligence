"""
Standardized 5.0-second Vertical (1080x1920) 30fps Manim Benchmark.
Proves mathematical and geometric scaling curves on CPU with Cairo & Pango.
Duration: Exactly 5.0s (150 frames).
"""
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.background_color = "#07090e"

class AttentionScalingBenchmark(Scene):
    def construct(self):
        # 1. Header (0.0s - 0.6s)
        header = Text("SCALING LAWS: ATTENTION", font_size=42, color="#00e5ff", weight=BOLD)
        header.to_edge(UP, buff=2.2)
        
        sub = Text("Quadratic O(N^2) vs Linear O(N)", font_size=28, color="#94a3b8")
        sub.next_to(header, DOWN, buff=0.4)

        # 2. Axes (0.6s - 1.5s)
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 100, 20],
            x_length=6.0,
            y_length=6.0,
            axis_config={"color": "#334155", "stroke_width": 2},
        )
        axes.next_to(sub, DOWN, buff=1.0)
        
        x_label = Text("Sequence Length (Tokens)", font_size=22, color="#64748b")
        x_label.next_to(axes, DOWN, buff=0.4)
        
        # 3. Curves (1.5s - 2.8s)
        # O(N^2) curve
        curve_quadratic = axes.plot(lambda x: (x / 10.0) ** 2, x_range=[0, 100], color="#ef4444", stroke_width=4)
        label_quad = Text("Standard: O(N^2)", font_size=24, color="#ef4444", weight=BOLD)
        label_quad.next_to(axes.c2p(75, 56), UP + LEFT, buff=0.2)

        # O(N) curve
        curve_linear = axes.plot(lambda x: x, x_range=[0, 100], color="#22c55e", stroke_width=4)
        label_lin = Text("Linear: O(N)", font_size=24, color="#22c55e", weight=BOLD)
        label_lin.next_to(axes.c2p(80, 80), DOWN + RIGHT, buff=0.2)

        # 4. Traveling Probe Points (2.8s - 4.2s)
        dot_quad = Dot(axes.c2p(0, 0), color="#fca5a5", radius=0.12)
        dot_lin = Dot(axes.c2p(0, 0), color="#86efac", radius=0.12)

        # 5. Conclusion Callout (4.2s - 5.0s)
        callout_box = RoundedRectangle(corner_radius=0.2, width=6.5, height=1.5, color="#3b82f6", fill_color="#0f172a", fill_opacity=0.9, stroke_width=2)
        callout_box.next_to(axes, DOWN, buff=1.2)
        callout_text = Text("8.4x COMPUTE REDUCTION AT 32K CONTEXT", font_size=24, color="#ffd43b", weight=BOLD)
        callout_text.move_to(callout_box.get_center())

        # EXECUTION TIMELINE (Sum = 5.00s)
        # 0.0s - 0.6s (run_time=0.6s)
        self.play(FadeIn(header, shift=UP * 0.3), FadeIn(sub), run_time=0.6)
        
        # 0.6s - 1.4s (run_time=0.8s)
        self.play(Create(axes), FadeIn(x_label), run_time=0.8)
        
        # 1.4s - 2.6s (run_time=1.2s)
        self.play(
            Create(curve_quadratic),
            FadeIn(label_quad),
            Create(curve_linear),
            FadeIn(label_lin),
            run_time=1.2
        )
        
        # 2.6s - 3.8s (run_time=1.2s)
        self.add(dot_quad, dot_lin)
        self.play(
            MoveAlongPath(dot_quad, curve_quadratic),
            MoveAlongPath(dot_lin, curve_linear),
            run_time=1.2
        )
        
        # 3.8s - 4.6s (run_time=0.8s)
        self.play(
            FadeIn(callout_box),
            FadeIn(callout_text),
            run_time=0.8
        )
        
        # 4.6s - 5.0s (run_time=0.4s)
        self.wait(0.4)

