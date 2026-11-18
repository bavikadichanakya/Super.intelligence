"""
Execution runner for HyperFrames 5-second Benchmark with ResourceGuard telemetry.
"""
import sys
import json
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rendering.resource_guard import ResourceGuard

def run_benchmark():
    guard = ResourceGuard()
    guard.configure_environment()
    
    output_dir = Path("output/benchmark")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    final_mp4 = (output_dir / "benchmark_hyperframes_5s.mp4").resolve()
    
    cmd = [
        "npx.cmd", "hyperframes", "render",
        "renderer",
        "-c", "compositions/benchmark_hyperframes_5s.html",
        "-o", str(final_mp4)
    ]
    
    print("[HYPERFRAMES BENCHMARK] Starting guarded execution...")
    result = guard.execute_isolated_render(cmd, cwd=Path("."), timeout_seconds=180.0)
    
    # Probe video if exists
    probe_data = {}
    if final_mp4.exists():
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,nb_frames,duration,bit_rate",
            "-of", "json",
            str(final_mp4)
        ]
        p_res = subprocess.run(probe_cmd, capture_output=True, text=True)
        if p_res.returncode == 0:
            probe_data = json.loads(p_res.stdout)
            
    summary = {
        "engine": "HyperFrames (HTML/CSS/SVG/GSAP)",
        "scene": "Timeline & Multi-Scene Synchronization",
        "exit_code": result["returncode"],
        "elapsed_seconds": round(result["duration_seconds"], 2),
        "peak_ram_mb": round(result["peak_ram_mb"], 2),
        "peak_cpu_percent": round(result.get("peak_cpu_percent", 0.0), 2),
        "output_file": str(final_mp4) if final_mp4.exists() else None,
        "file_size_bytes": final_mp4.stat().st_size if final_mp4.exists() else 0,
        "probe": probe_data,
        "log_file": str(result.get("log_path", ""))
    }
    
    out_json = output_dir / "benchmark_hyperframes_metrics.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print("[HYPERFRAMES BENCHMARK] Finished.")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    run_benchmark()

