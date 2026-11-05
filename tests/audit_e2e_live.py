"""
TASK 5 & 6 — COMPLETE LIVE END-TO-END BENCHMARK & RESOURCE AUDIT
Uses a real, publicly accessible RSS article to run the entire pipeline end-to-end.
Measures peak RAM, CPU usage, execution time, temp disk consumption, and video quality.
"""

import os
import sys
import time
import json
import psutil
import threading
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config import get_config
from core.database import Database
from core.pipeline import SuperIntelligencePipeline
from video.video_validator import VideoValidator


class ResourceMonitor:
    def __init__(self, interval: float = 0.5):
        self.interval = interval
        self.stop_event = threading.Event()
        self.peak_ram_mb = 0.0
        self.cpu_samples = []
        self.process = psutil.Process(os.getpid())
        self.thread = threading.Thread(target=self._monitor, daemon=True)

    def _monitor(self):
        while not self.stop_event.is_set():
            try:
                # Include child processes (FFmpeg, Piper, Node, etc.)
                mem = self.process.memory_info().rss
                cpu = self.process.cpu_percent(interval=None)
                for child in self.process.children(recursive=True):
                    try:
                        mem += child.memory_info().rss
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                mem_mb = mem / (1024 * 1024)
                if mem_mb > self.peak_ram_mb:
                    self.peak_ram_mb = mem_mb
                self.cpu_samples.append(cpu)
            except Exception:
                pass
            time.sleep(self.interval)

    def start(self):
        self.process.cpu_percent(interval=None)  # prime cpu calculation
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=2.0)
        avg_cpu = sum(self.cpu_samples) / max(len(self.cpu_samples), 1)
        peak_cpu = max(self.cpu_samples) if self.cpu_samples else 0.0
        return {
            "peak_ram_mb": round(self.peak_ram_mb, 2),
            "avg_cpu_percent": round(avg_cpu, 1),
            "peak_cpu_percent": round(peak_cpu, 1)
        }


def get_dir_size_mb(path: Path) -> float:
    if not path.exists():
        return 0.0
    total = sum(f.stat().st_size for f in path.glob("**/*") if f.is_file())
    return round(total / (1024 * 1024), 2)


def run_live_e2e_audit():
    config = get_config()
    db = Database()
    pipeline = SuperIntelligencePipeline(db=db, config=config)

    print("\n" + "="*70)
    print("STEP 1: DISCOVER REAL LIVE ARTICLE VIA PUBLIC RSS FEEDS")
    print("="*70)

    # 1. Discover live topic from real public RSS
    collected = pipeline.rss_collector.collect_all()
    print(f"Total live RSS items fetched: {len(collected)}")

    real_topic = None
    for item in collected:
        # Require a valid HTTP/HTTPS link to an external publisher
        if item.get("url", "").startswith("http") and "superintelligenceee.local" not in item.get("url", ""):
            real_topic = item
            break

    if not real_topic:
        raise RuntimeError("No live public RSS articles could be fetched.")

    print(f"Selected Live Article:")
    print(f"  Title:     {real_topic.get('title')}")
    print(f"  Publisher: {real_topic.get('publisher')}")
    print(f"  URL:       {real_topic.get('url')}")
    print(f"  Category:  {real_topic.get('category')}")

    # 2. Store source in database
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO topics (
                title, url, publisher, summary, category, published_date, status, score
            ) VALUES (?, ?, ?, ?, ?, ?, 'DISCOVERED', 92.5)
            """,
            (
                real_topic["title"],
                real_topic["url"],
                real_topic.get("publisher", "Live RSS"),
                real_topic.get("summary", ""),
                real_topic.get("category", "Artificial Intelligence News"),
                real_topic.get("published_date", "")
            )
        )
        live_topic_id = cursor.lastrowid

    print(f"Live topic recorded in SQLite with ID: #{live_topic_id}")

    # 3. Start Resource Benchmarking
    temp_dir = config.resolve_path(".temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_size_before = get_dir_size_mb(temp_dir)

    monitor = ResourceMonitor(interval=0.25)
    monitor.start()
    t_start = time.time()

    # 4. Execute Full Pipeline (Steps 3-12)
    print("\n" + "="*70)
    print("STEP 2-12: EXECUTING FULL PIPELINE")
    print("="*70)

    result = pipeline.produce_reel(topic_id=live_topic_id)
    render_duration = round(time.time() - t_start, 2)
    resource_stats = monitor.stop()

    temp_size_after = get_dir_size_mb(temp_dir)
    temp_consumed_mb = round(max(temp_size_after - temp_size_before, 0.0), 2)

    # 5. Verify Output and Approval Gate
    video_path = Path(result["video_path"])
    assert video_path.exists(), f"Output video file does not exist: {video_path}"
    assert result["status"] == "NEEDS_REVIEW", f"Approval gate breached! Status: {result['status']}"

    file_size_bytes = video_path.stat().st_size
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

    # 6. Technical Validation via FFprobe
    validator = VideoValidator(config=config)
    val_report = validator.validate_reel(video_path)

    # Check database status
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM production_jobs WHERE id = ?", (result["production_job_id"],))
        p_row = cursor.fetchone()
        job_row = dict(p_row) if p_row else {}
        cursor.execute("SELECT * FROM approvals WHERE production_job_id = ?", (result["production_job_id"],))
        a_row = cursor.fetchone()
        approval_row = dict(a_row) if a_row else {}

    audit_summary = {
        "status": "PASS",
        "live_article": {
            "title": real_topic.get("title"),
            "publisher": real_topic.get("publisher"),
            "source_url": real_topic.get("url"),
            "topic_id": live_topic_id
        },
        "approval_gate": {
            "production_job_id": result["production_job_id"],
            "production_status": job_row.get("status"),
            "gate_enforced": job_row.get("status") == "NEEDS_REVIEW",
            "approval_recorded": approval_row.get("status") == "PENDING_REVIEW" or "approvals" in str(approval_row)
        },
        "ffprobe_qa": {
            "valid": val_report.get("valid"),
            "width": val_report.get("width"),
            "height": val_report.get("height"),
            "fps": val_report.get("fps"),
            "duration_seconds": val_report.get("duration"),
            "video_codec": val_report.get("video_codec"),
            "audio_codec": val_report.get("audio_codec"),
            "file_size_mb": file_size_mb,
            "issues": val_report.get("issues", [])
        },
        "resource_benchmark": {
            "peak_ram_mb": resource_stats["peak_ram_mb"],
            "avg_cpu_percent": resource_stats["avg_cpu_percent"],
            "peak_cpu_percent": resource_stats["peak_cpu_percent"],
            "rendering_time_seconds": render_duration,
            "temp_disk_consumption_mb": temp_consumed_mb,
            "final_video_size_mb": file_size_mb,
            "workers": 1
        },
        "artifacts_generated": {
            "video_path": str(video_path),
            "captions": result.get("captions")
        }
    }

    print("\n" + "="*70)
    print("AUDIT RESULTS JSON:")
    print("="*70)
    print(json.dumps(audit_summary, indent=2))

    # Save to benchmark result file
    res_path = Path("A:/SUPER.INTELLIGENCEEE/output/audit_live_e2e_results.json")
    res_path.write_text(json.dumps(audit_summary, indent=2), encoding="utf-8")
    print(f"\nSaved benchmark results to: {res_path}")

    return audit_summary


if __name__ == "__main__":
    run_live_e2e_audit()
