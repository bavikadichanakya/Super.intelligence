"""
SUPER.INTELLIGENCEEE — Agent Reach Research Connector
Wraps the official Agent Reach CLI (v1.6+) for isolated multi-channel research.
Integrates YouTube transcripts, GitHub repositories, Reddit discussions, and public web sources
into the source-grounded research and fact-checking workflow.
Strictly zero-budget, read-only, cookie-safe, and rate-limit compliant.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config
from core.database import Database

logger = logging.getLogger("super_intelligence.agent_reach")

ALLOWED_CHANNELS = {"youtube", "github", "reddit", "web", "v2ex"}
BLOCKED_CHANNELS = {"instagram", "facebook", "twitter", "xueqiu", "boss"}


class AgentReachConnector:
    """Safe, isolated subprocess bridge for Agent Reach multi-channel intelligence."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()
        self.bin_path = self._resolve_executable()

    def _resolve_executable(self) -> Optional[Path]:
        """Locates the agent-reach binary on Windows systems."""
        # Check current PATH
        found = shutil.which("agent-reach")
        if found:
            return Path(found)

        # Common user-local locations
        home = Path.home()
        candidates = [
            home / ".local" / "bin" / "agent-reach.exe",
            home / ".local" / "bin" / "agent-reach",
            home / ".cargo" / "bin" / "agent-reach.exe",
            Path(os.environ.get("APPDATA", "")) / "Python" / "Scripts" / "agent-reach.exe",
        ]
        for c in candidates:
            if c.exists():
                return c

        return None

    def is_available(self) -> bool:
        return self.bin_path is not None and self.bin_path.exists()

    def _run_reach(self, args: List[str], timeout: int = 45) -> Dict[str, Any]:
        """Runs agent-reach command with strict channel safety and JSON parsing."""
        if not self.is_available():
            return {
                "ok": False,
                "error": {
                    "code": "NOT_INSTALLED",
                    "hint": "Install via 'uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip'",
                },
            }

        channel = args[0] if args else ""
        if channel in BLOCKED_CHANNELS:
            logger.warning(f"Blocked request to channel '{channel}' per safety policy.")
            return {
                "ok": False,
                "error": {
                    "code": "POLICY_BLOCKED",
                    "hint": f"Channel '{channel}' is disabled to prevent cookie leakage and account policy violations.",
                },
            }

        if channel and channel not in ALLOWED_CHANNELS and channel not in ("version", "channels"):
            return {
                "ok": False,
                "error": {
                    "code": "CHANNEL_NOT_ALLOWED",
                    "hint": f"Channel '{channel}' is not in approved list: {sorted(ALLOWED_CHANNELS)}",
                },
            }

        cmd = [str(self.bin_path)] + args
        try:
            # Ensure local bin is in PATH
            env = dict(os.environ)
            local_bin = str(Path.home() / ".local" / "bin")
            if local_bin not in env.get("PATH", ""):
                env["PATH"] = f"{local_bin};{env.get('PATH', '')}"

            res = subprocess.run(
                cmd,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                env=env,
                check=False,
            )

            stdout = (res.stdout or "").strip()
            if not stdout:
                return {
                    "ok": False,
                    "error": {
                        "code": "EMPTY_OUTPUT",
                        "hint": (res.stderr or "").strip() or "No output from agent-reach",
                    },
                }

            # Parse JSON schema output
            try:
                data = json.loads(stdout)
                return data
            except json.JSONDecodeError:
                return {
                    "ok": False,
                    "raw_output": stdout,
                    "error": {"code": "JSON_PARSE_ERROR", "hint": res.stderr[:300]},
                }

        except subprocess.TimeoutExpired:
            return {"ok": False, "error": {"code": "TIMEOUT", "hint": f"Command timed out after {timeout}s"}}
        except Exception as e:
            logger.exception(f"Agent-Reach invocation failed: {e}")
            return {"ok": False, "error": {"code": "SUBPROCESS_ERROR", "hint": str(e)}}

    # -----------------------------------------------------------------------
    # Public Research Methods
    # -----------------------------------------------------------------------
    def get_youtube_metadata(self, target: str) -> Dict[str, Any]:
        """Retrieves YouTube video metadata (title, author, duration, view_count, description)."""
        data = self._run_reach(["youtube", "read", target])
        if data.get("ok") and data.get("items"):
            item = data["items"][0]
            raw = item.get("raw", {})
            return {
                "ok": True,
                "title": item.get("title"),
                "url": item.get("url"),
                "author": item.get("author"),
                "duration_seconds": raw.get("duration"),
                "view_count": raw.get("view_count"),
                "like_count": raw.get("like_count"),
                "tags": raw.get("tags", []),
                "description": item.get("text", ""),
            }
        return {"ok": False, "error": data.get("error", {"code": "NO_ITEM"})}

    def get_youtube_transcript(self, target: str, lang: str = "en") -> Dict[str, Any]:
        """Retrieves complete auto or manual subtitle text for a YouTube video."""
        data = self._run_reach(["youtube", "subtitle", target, "--lang", lang])
        if data.get("ok") and data.get("items"):
            item = data["items"][0]
            return {
                "ok": True,
                "title": item.get("title"),
                "url": item.get("url"),
                "language": lang,
                "transcript": item.get("text", ""),
            }
        return {"ok": False, "error": data.get("error", {"code": "NO_TRANSCRIPT"})}

    def search_github(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Searches GitHub repositories for emerging technology codebases and models."""
        data = self._run_reach(["github", "search", query, "--limit", str(limit)])
        results = []
        if data.get("ok") and data.get("items"):
            for item in data["items"]:
                raw = item.get("raw", {})
                results.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "author": item.get("author"),
                    "stars": raw.get("stargazers_count", 0),
                    "description": item.get("text", ""),
                    "language": raw.get("language"),
                    "topics": raw.get("topics", []),
                    "source": "GitHub",
                })
        return results

    def search_reddit_public(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Searches public Reddit discussions without requiring personal user cookies."""
        data = self._run_reach(["reddit", "search", query, "--limit", str(limit)])
        results = []
        if data.get("ok") and data.get("items"):
            for item in data["items"]:
                results.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "author": item.get("author"),
                    "content": item.get("text", ""),
                    "source": "Reddit",
                })
        return results

    def read_web_page(self, url: str) -> Dict[str, Any]:
        """Reads a public web page as clean markdown text."""
        data = self._run_reach(["web", "read", url])
        if data.get("ok") and data.get("items"):
            item = data["items"][0]
            return {
                "ok": True,
                "title": item.get("title") or url,
                "url": item.get("url") or url,
                "content": item.get("text", ""),
            }
        return {"ok": False, "error": data.get("error", {"code": "WEB_READ_FAILED"})}

    # -----------------------------------------------------------------------
    # Ingestion into Source-Grounded Production Database
    # -----------------------------------------------------------------------
    def ingest_research_to_topics(
        self,
        research_items: List[Dict[str, Any]],
        category: str = "Technology Experiments",
    ) -> List[int]:
        """
        Stores retrieved items directly into the SQLite `topics` table.
        Ensures strict source attribution and fact-checking entry.
        """
        inserted_ids = []
        for item in research_items:
            title = item.get("title", "").strip()
            url = item.get("url", "").strip()
            summary = item.get("description") or item.get("content") or item.get("text") or ""
            publisher = item.get("source") or item.get("author") or "Agent Reach"

            if not title or not url:
                continue

            topic_data = {
                "title": title[:200],
                "url": url,
                "publisher": publisher,
                "summary": summary[:1000],
                "category": category,
                "status": "DISCOVERED",
                "score": 85.0,
                "relevance_score": 80.0,
                "freshness_score": 90.0,
                "originality_score": 85.0,
                "notes": f"Ingested via Agent Reach ({publisher})",
            }
            t_id = self.db.insert_topic(topic_data)
            if t_id:
                inserted_ids.append(t_id)

        logger.info(f"Ingested {len(inserted_ids)} topics into database from Agent Reach.")
        return inserted_ids
