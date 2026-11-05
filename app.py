"""
SUPER.INTELLIGENCEEE V2 — Master Application Entry Point
Zero-budget autonomous AI media engine on Windows 11.
FastAPI web server & command-line interface.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import get_config
from core.database import Database
from core.pipeline import SuperIntelligencePipeline
from dashboard.routes import router as dashboard_router

# Setup root logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/super_intelligence.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("super_intelligence.app")

# Ensure required runtime directories exist
config = get_config()
output_dir = config.resolve_path("output")
output_dir.mkdir(parents=True, exist_ok=True)
static_dir = Path(__file__).parent / "dashboard" / "static"
static_dir.mkdir(parents=True, exist_ok=True)

# Initialize FastAPI application
app = FastAPI(
    title="SUPER.INTELLIGENCEEE V2",
    description="Autonomous zero-budget AI content production engine for Instagram Reels.",
    version="2.0.0",
)

# Mount media directory for browser video streaming
app.mount("/media", StaticFiles(directory=str(output_dir)), name="media")
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include Dashboard & API Routes
app.include_router(dashboard_router)


def run_server(host: str = "127.0.0.1", port: int = 5000):
    """Starts the FastAPI web server."""
    logger.info(f"Starting SUPER.INTELLIGENCEEE Dashboard at http://{host}:{port}")
    uvicorn.run("app:app", host=host, port=port, log_level="info", reload=False)


def main():
    """CLI argument dispatcher."""
    parser = argparse.ArgumentParser(
        description="SUPER.INTELLIGENCEEE V2 — Autonomous Media Production Engine"
    )
    parser.add_argument("--web", action="store_true", help="Launch the local dashboard web server")
    parser.add_argument("--host", default="127.0.0.1", help="Host address for web server")
    parser.add_argument("--port", type=int, default=5000, help="Port number for web server")
    subparsers = parser.add_subparsers(dest="command")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Launch the local dashboard web server")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host address")
    serve_parser.add_argument("--port", type=int, default=5000, help="Port number")

    # Command: discover
    subparsers.add_parser("discover", help="Execute topic discovery and scoring")

    # Command: produce
    produce_parser = subparsers.add_parser("produce", help="Run full autonomous production for a Reel")
    produce_parser.add_argument("--topic-id", type=int, default=None, help="Specific topic ID to produce")

    # Command: status
    subparsers.add_parser("status", help="Print technical status and health metrics")

    args = parser.parse_args()

    # Default to serve if no command provided or if --web flag is supplied
    if not args.command or args.command == "serve" or getattr(args, "web", False):
        host = getattr(args, "host", "127.0.0.1")
        port = getattr(args, "port", 5000)
        run_server(host=host, port=port)

    elif args.command == "discover":
        db = Database()
        pipeline = SuperIntelligencePipeline(db=db, config=config)
        scored = pipeline.run_topic_research()
        print(f"\n[SUCCESS] Discovered and scored {len(scored)} topics.")

    elif args.command == "produce":
        db = Database()
        pipeline = SuperIntelligencePipeline(db=db, config=config)
        print(f"\n[LAUNCH] Starting end-to-end production (Topic ID: {args.topic_id or 'Auto-Top'})...")
        res = pipeline.produce_reel(topic_id=args.topic_id)
        print(f"\n[SUCCESS] Produced Reel #{res['production_job_id']}")
        print(f"Video: {res['video_path']}")
        print(f"Duration: {res['duration']}s | Format: {res['dimensions']} @ {res['fps']}fps")

    elif args.command == "status":
        db = Database()
        with db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as c FROM topics")
            topics_c = cursor.fetchone()["c"]
            cursor.execute("SELECT COUNT(*) as c FROM scripts")
            scripts_c = cursor.fetchone()["c"]
            cursor.execute("SELECT COUNT(*) as c FROM production_jobs WHERE status = 'APPROVED'")
            approved_c = cursor.fetchone()["c"]

        print("=" * 60)
        print("SUPER.INTELLIGENCEEE V2 — SYSTEM DIAGNOSTICS")
        print("=" * 60)
        print(f"Project Root:      A:\\SUPER.INTELLIGENCEEE")
        print(f"Runtime Python:    Python 3.11.15 (.venv)")
        print(f"TTS Engine:        Piper TTS (en_US-lessac-medium) + pyttsx3 fallback")
        print(f"Renderer:          HyperFrames v0.9.12 + FFmpeg fallback")
        print(f"Database:          data/super_intelligence.db (Active)")
        print(f"Discovered Topics: {topics_c}")
        print(f"Script Studio:     {scripts_c} scripts")
        print(f"Weekly Progress:   {approved_c} / 5 Approved Reels")
        print("=" * 60)


if __name__ == "__main__":
    main()
