import time
import psutil
import os
import subprocess
from manim import *

class ExplainerMathematicalVector(Scene):
    def construct(self):
        # Configure vertical 1080x1920 framing
        self.camera.frame_width = 9.0
        self.camera.frame_height = 16.0
        
        title = Text("LATENT VECTOR TRAJECTORY", font_size=42, color=WHITE).to_edge(UP, buff=1.5)
        self.play(Write(title), run_time=1.0)
        
        # Draw coordinate plane and spiral curve
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": BLUE_C}
        ).shift(DOWN * 0.5)
        
        curve = ParametricFunction(
            lambda t: np.array([
                1.5 * np.cos(t) * np.exp(-0.1 * t),
                1.5 * np.sin(t) * np.exp(-0.1 * t),
                0
            ]),
            t_range=[0, 4 * PI],
            color=YELLOW_D
        ).shift(DOWN * 0.5)
        
        dot = Dot(color=RED_C).move_to(curve.get_start())
        
        self.play(Create(axes), run_time=1.0)
        self.play(Create(curve), MoveAlongPath(dot, curve), run_time=2.0)
        self.wait(0.5)

if __name__ == "__main__":
    t0 = time.time()
    proc = psutil.Process()
    mem_before = proc.memory_info().rss / (1024 * 1024)
    print(f"Memory before render: {mem_before:.2f} MB")
    
    # Render with manim CLI
    output_dir = os.path.abspath("output/tests/manim_eval")
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        os.path.abspath(".venv/Scripts/python.exe"),
        "-m", "manim",
        "-qh",  # 1080p high quality
        "--fps", "30",
        "--media_dir", output_dir,
        __file__,
        "ExplainerMathematicalVector"
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    mem_after = proc.memory_info().rss / (1024 * 1024)
    
    print(f"Manim render completed in {dt:.2f} seconds. Exit code: {res.returncode}")
    print(f"Memory after: {mem_after:.2f} MB")
    if res.returncode != 0:
        print("STDERR:", res.stderr[-500:])
    else:
        print("Success! Output generated in media_dir.")

