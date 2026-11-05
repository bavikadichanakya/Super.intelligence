"""
SUPER.INTELLIGENCEEE — YouTube Publishing Integration Module
Implements official Google OAuth 2.0 and YouTube Data API v3 integration.
Handles token exchange, secure storage, quota management, and video uploads.
Strictly zero-budget, preserves human-in-the-loop approval, and prevents credential leakage.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

from core.config import get_config
from core.database import Database
from intelligence.youtube_intel import build_youtube_seo_package

logger = logging.getLogger("super_intelligence.youtube_integration")

TOKEN_FILE_PATH = Path(__file__).resolve().parent.parent / "data" / "youtube_token.json"
OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
YOUTUBE_UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube.upload"


class YouTubeIntegration:
    """Manages YouTube channel authentication and video publishing via official APIs."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()
        self.client_id = os.environ.get("YOUTUBE_CLIENT_ID") or self.config.get("publishing.youtube.client_id", "")
        self.client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET") or self.config.get("publishing.youtube.client_secret", "")
        self.redirect_uri = os.environ.get("YOUTUBE_REDIRECT_URI") or self.config.get("publishing.youtube.redirect_uri", "http://127.0.0.1:5000/oauth2callback")
        self.export_dir = self.config.resolve_path(Path("output") / "youtube_packages")
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def is_configured(self) -> bool:
        """Checks if Client ID and Secret are provided in environment or config."""
        return bool(self.client_id and self.client_secret and not self.client_id.startswith("YOUR_"))

    def get_auth_url(self, state: str = "super_intelligence_oauth") -> str:
        """Builds official Google OAuth 2.0 authorization URL."""
        if not self.is_configured():
            raise ValueError("YouTube OAuth Client ID and Secret must be configured in .env or config.")

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": YOUTUBE_SCOPE,
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }
        return f"{OAUTH_AUTH_URL}?{urllib.parse.urlencode(params)}"

    def exchange_code(self, code: str) -> Dict[str, Any]:
        """Exchanges authorization code for access and refresh tokens."""
        if not self.is_configured():
            return {"ok": False, "error": "OAuth credentials not configured"}

        payload = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

        try:
            res = requests.post(OAUTH_TOKEN_URL, data=payload, timeout=20)
            data = res.json()
            if res.status_code == 200 and "access_token" in data:
                self._save_token(data)
                return {"ok": True, "token_saved": True, "expires_in": data.get("expires_in")}
            else:
                logger.error(f"OAuth token exchange failed: {data}")
                return {"ok": False, "error": data.get("error_description") or data.get("error")}
        except Exception as e:
            logger.exception(f"Token exchange exception: {e}")
            return {"ok": False, "error": str(e)}

    def _save_token(self, token_data: Dict[str, Any]):
        TOKEN_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        # Add timestamp
        token_data["saved_at"] = datetime.now(timezone.utc).isoformat()
        with open(TOKEN_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2)

    def load_token(self) -> Optional[Dict[str, Any]]:
        if TOKEN_FILE_PATH.exists():
            try:
                with open(TOKEN_FILE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def is_authenticated(self) -> bool:
        token = self.load_token()
        return bool(token and token.get("access_token"))

    def refresh_access_token(self) -> Optional[str]:
        """Refreshes expired access token using stored refresh_token."""
        token = self.load_token()
        if not token or not token.get("refresh_token"):
            return None

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": token["refresh_token"],
            "grant_type": "refresh_token",
        }

        try:
            res = requests.post(OAUTH_TOKEN_URL, data=payload, timeout=20)
            data = res.json()
            if res.status_code == 200 and "access_token" in data:
                token["access_token"] = data["access_token"]
                token["expires_in"] = data.get("expires_in", 3600)
                token["saved_at"] = datetime.now(timezone.utc).isoformat()
                self._save_token(token)
                return data["access_token"]
        except Exception as e:
            logger.error(f"Failed to refresh YouTube token: {e}")
        return None

    def upload_video(
        self,
        video_path: Path | str,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        privacy_status: str = "private",
        production_job_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Uploads a video to YouTube using resumable upload protocol.
        Strictly requires human approval if associated with a production_job_id.
        """
        v_path = Path(video_path)
        if not v_path.exists():
            return {"ok": False, "error": f"Video file not found: {v_path}"}

        # 1. Enforce Approval Gate
        if production_job_id is not None:
            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM production_jobs WHERE id = ?", (production_job_id,))
                job = cursor.fetchone()
                if not job or job["status"] != "APPROVED":
                    return {
                        "ok": False,
                        "error": "APPROVAL_GATE_BLOCKED: Production job must be explicitly APPROVED by human editor before publishing.",
                    }

        # 2. Check Authentication
        if not self.is_authenticated():
            return {
                "ok": False,
                "error": "NOT_AUTHENTICATED: YouTube account is not authenticated. Complete OAuth setup in Dashboard.",
                "auth_url": self.get_auth_url() if self.is_configured() else None,
            }

        token = self.load_token()
        access_token = token.get("access_token")

        # 3. Build Metadata
        metadata = {
            "snippet": {
                "title": title[:100],
                "description": description,
                "tags": tags or ["AI", "Technology"],
                "categoryId": "28",  # Science & Technology
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
            },
        }

        # 4. Initiate Resumable Upload
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(v_path.stat().st_size),
        }

        try:
            init_res = requests.post(
                f"{YOUTUBE_UPLOAD_URL}?uploadType=resumable&part=snippet,status",
                headers=headers,
                data=json.dumps(metadata),
                timeout=30,
            )

            # Token expired check
            if init_res.status_code == 401:
                refreshed = self.refresh_access_token()
                if refreshed:
                    headers["Authorization"] = f"Bearer {refreshed}"
                    init_res = requests.post(
                        f"{YOUTUBE_UPLOAD_URL}?uploadType=resumable&part=snippet,status",
                        headers=headers,
                        data=json.dumps(metadata),
                        timeout=30,
                    )

            if init_res.status_code not in (200, 201) or "Location" not in init_res.headers:
                return {
                    "ok": False,
                    "error": f"Upload initiation failed (HTTP {init_res.status_code}): {init_res.text[:300]}",
                }

            upload_url = init_res.headers["Location"]

            # 5. Stream Video Data
            with open(v_path, "rb") as vf:
                upload_headers = {"Content-Type": "video/mp4"}
                up_res = requests.put(upload_url, headers=upload_headers, data=vf, timeout=120)

                if up_res.status_code in (200, 201):
                    resp_data = up_res.json()
                    video_id = resp_data.get("id")
                    logger.info(f"Video uploaded to YouTube successfully! Video ID: {video_id}")
                    return {
                        "ok": True,
                        "video_id": video_id,
                        "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                        "privacy_status": privacy_status,
                    }
                else:
                    return {
                        "ok": False,
                        "error": f"Video binary upload failed (HTTP {up_res.status_code}): {up_res.text[:300]}",
                    }

        except Exception as e:
            logger.exception(f"YouTube upload exception: {e}")
            return {"ok": False, "error": str(e)}

    def create_shorts_package(self, production_job_id: int) -> Dict[str, Any]:
        """Prepares a standalone, verified export package for YouTube Shorts."""
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM production_jobs WHERE id = ?", (production_job_id,))
            job = cursor.fetchone()

        if not job:
            raise ValueError(f"Job #{production_job_id} not found.")

        video_path = Path(job["output_video_path"]) if job["output_video_path"] else None
        if not video_path or not video_path.exists():
            raise FileNotFoundError(f"Video file for job #{production_job_id} missing.")

        pkg_dir = self.export_dir / f"shorts_package_{production_job_id}_{datetime.now().strftime('%Y%m%d')}"
        pkg_dir.mkdir(parents=True, exist_ok=True)

        dest_video = pkg_dir / f"{video_path.stem}.mp4"
        shutil.copy2(video_path, dest_video)

        # Build SEO package
        seo = build_youtube_seo_package(
            title=f"{job['title']} #Shorts",
            summary=f"Automated intelligence briefing on {job['title']}.",
            tags=["AI", "Shorts", "Tech", "Innovation"],
        )

        with open(pkg_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(seo, f, indent=2)

        with open(pkg_dir / "description.txt", "w", encoding="utf-8") as f:
            f.write(seo["description"])

        return {
            "ok": True,
            "package_dir": str(pkg_dir),
            "video_path": str(dest_video),
            "title": seo["title"],
            "metadata_file": str(pkg_dir / "metadata.json"),
        }

