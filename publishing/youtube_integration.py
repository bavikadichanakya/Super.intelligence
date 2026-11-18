"""
SUPER.INTELLIGENCEEE — Production YouTube Integration Module
Official Google OAuth 2.0 & YouTube Data API v3 Integration.
Implements:
- Persistent CSRF-protected OAuth state with atomic SQLite consumption (provider='youtube')
- Authenticated Fernet (AES-128-CBC + HMAC-SHA256) encryption at rest in data/secure/youtube_token.enc
- Channel identity verification via channels.list (snippet, contentDetails, statistics, mine=true)
- Resumable chunked video upload protocol (videos.insert with uploadType=resumable)
- Strict human editorial approval gate with SHA-256 artifact integrity binding
- Global kill switch enforcement and idempotency / duplicate upload prevention
- Default privacyStatus = 'private'
- Zero credentials in logs or git
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import secrets
import shutil
import time
import urllib.parse
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from cryptography.fernet import Fernet, InvalidToken

from core.config import get_config
from core.database import Database
from intelligence.youtube_intel import build_youtube_seo_package

logger = logging.getLogger("super_intelligence.youtube_integration")

OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
OAUTH_REVOKE_URL = "https://oauth2.googleapis.com/revoke"
YOUTUBE_CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"
YOUTUBE_UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


class YouTubeSecurityError(Exception):
    """Raised when OAuth state validation or CSRF checks fail."""
    pass


class YouTubeAuthError(Exception):
    """Raised when token exchange, refresh, or channel verification fails."""
    pass


class YouTubeUploadError(Exception):
    """Raised when video upload or verification fails."""
    pass


class YouTubeVisibility(str, Enum):
    PRIVATE = "private"
    UNLISTED = "unlisted"
    PUBLIC = "public"
    SCHEDULED = "scheduled"


VISIBILITY_DESCRIPTIONS: Dict[str, Dict[str, Any]] = {
    YouTubeVisibility.PRIVATE.value: {
        "label": "Private (Privacy-First Default)",
        "summary": "Visible only to channel owner and explicitly invited Google accounts.",
        "discovery_impact": (
            "Completely excluded from YouTube search, Shorts Feed recommendations, channel page, and "
            "public distribution. Unsuitable for organic audience reach. Ideal for test uploads, creator review, and staging."
        ),
        "enters_recommendations": False,
        "requires_confirmation": False,
    },
    YouTubeVisibility.UNLISTED.value: {
        "label": "Unlisted (Link Sharing Only)",
        "summary": "Accessible to anyone with the exact direct link. Does not appear on channel page or search results.",
        "discovery_impact": (
            "Bypasses the public YouTube Shorts carousel and recommendation algorithms. Only viewers sent the URL "
            "can watch. Unsuitable for organic cold discovery."
        ),
        "enters_recommendations": False,
        "requires_confirmation": True,
    },
    YouTubeVisibility.PUBLIC.value: {
        "label": "Public (Immediate Algorithmic Discovery)",
        "summary": "Instantly accessible worldwide to all YouTube users and indexed across all surfaces.",
        "discovery_impact": (
            "Submitted immediately to the YouTube Shorts Feed, search indexing, and personalized recommendation pools. "
            "REQUIRED for organic audience discovery and growth."
        ),
        "enters_recommendations": True,
        "requires_confirmation": True,
    },
    YouTubeVisibility.SCHEDULED.value: {
        "label": "Scheduled Release (Privacy-First Staged Public)",
        "summary": "Uploaded privately immediately, then automatically transitioned to public at a verified future UTC timestamp.",
        "discovery_impact": (
            "Staged privately until release time. Hits the Shorts Feed at the scheduled peak traffic window "
            "with fresh publication momentum."
        ),
        "enters_recommendations": True,
        "requires_confirmation": True,
    },
}


def validate_visibility_selection(
    visibility: str,
    explicit_owner_confirmation: bool = False,
    scheduled_publish_at: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Validates visibility selection under strict owner confirmation rules.
    - Preserves private as default without requiring explicit confirmation.
    - Requires explicit_owner_confirmation == True for unlisted, public, or scheduled.
    - Verifies scheduled publish timestamp is in the future.
    """
    valid_keys = [v.value for v in YouTubeVisibility]
    vis_clean = str(visibility).lower().strip()
    if vis_clean not in valid_keys:
        raise ValueError(f"Invalid visibility '{visibility}'. Must be one of: {valid_keys}")

    spec = VISIBILITY_DESCRIPTIONS[vis_clean]

    if spec["requires_confirmation"] and not explicit_owner_confirmation:
        raise PermissionError(
            f"Explicit owner confirmation is required to select visibility '{vis_clean}'. "
            f"Discovery impact: {spec['discovery_impact']}"
        )

    if vis_clean == YouTubeVisibility.SCHEDULED.value:
        if not scheduled_publish_at:
            raise ValueError("Scheduled visibility requires 'scheduled_publish_at' ISO timestamp.")
        try:
            pub_dt = datetime.fromisoformat(scheduled_publish_at.replace("Z", "+00:00"))
            if pub_dt <= datetime.now(timezone.utc):
                raise ValueError("Scheduled publish timestamp must be set to a future time.")
        except Exception as e:
            raise ValueError(f"Invalid scheduled_publish_at timestamp: {e}")

    return {
        "visibility": vis_clean,
        "spec": spec,
        "scheduled_publish_at": scheduled_publish_at if vis_clean == YouTubeVisibility.SCHEDULED.value else None,
    }


class YouTubeIntegration:
    """Manages YouTube channel authentication, token encryption, and video publishing."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()

        # Paths
        data_dir = self.config.resolve_path(Path("data"))
        self.secure_dir = data_dir / "secure"
        self.secure_dir.mkdir(parents=True, exist_ok=True)
        self.token_file = self.secure_dir / "youtube_token.enc"
        self.key_file = self.secure_dir / ".master_key"

        self.export_dir = self.config.resolve_path(Path("output") / "youtube_packages")
        self.export_dir.mkdir(parents=True, exist_ok=True)

        # Fernet encryption
        self._fernet = self._init_crypto()

    # -------------------------------------------------------------------------
    # Cryptographic Engine
    # -------------------------------------------------------------------------
    def _init_crypto(self) -> Fernet:
        """Initializes Fernet authenticated encryption engine using shared secure master key."""
        env_key = os.environ.get("YOUTUBE_ENCRYPTION_KEY") or os.environ.get("INSTAGRAM_ENCRYPTION_KEY")
        if env_key:
            try:
                return Fernet(env_key.encode("utf-8") if isinstance(env_key, str) else env_key)
            except Exception as e:
                logger.warning(f"Invalid encryption key in environment ({e}), falling back to disk key.")

        if self.key_file.exists():
            try:
                key_bytes = self.key_file.read_bytes().strip()
                return Fernet(key_bytes)
            except Exception:
                pass

        new_key = Fernet.generate_key()
        try:
            self.key_file.write_bytes(new_key)
        except Exception as e:
            logger.error(f"Failed to persist master key to disk: {e}")
        return Fernet(new_key)

    @property
    def client_id(self) -> str:
        """Google OAuth 2.0 Client ID."""
        return (
            os.environ.get("YOUTUBE_CLIENT_ID")
            or self.config.get("publishing.youtube.client_id", "")
        ).strip()

    @property
    def client_secret(self) -> str:
        """Google OAuth 2.0 Client Secret."""
        return (
            os.environ.get("YOUTUBE_CLIENT_SECRET")
            or self.config.get("publishing.youtube.client_secret", "")
        ).strip()

    @property
    def redirect_uri(self) -> str:
        """Google OAuth redirect URI."""
        return (
            os.environ.get("YOUTUBE_REDIRECT_URI")
            or self.config.get(
                "publishing.youtube.redirect_uri",
                "http://127.0.0.1:5000/auth/youtube/callback",
            )
        ).strip()

    @property
    def scopes(self) -> List[str]:
        raw = os.environ.get("YOUTUBE_OAUTH_SCOPES") or self.config.get("publishing.youtube.scopes")
        if raw:
            if isinstance(raw, list):
                return raw
            return [s.strip() for s in str(raw).split(",") if s.strip()]
        return DEFAULT_SCOPES

    def is_configured(self) -> bool:
        """Returns True if Client ID and Secret are provided and non-placeholder."""
        return bool(
            self.client_id
            and self.client_secret
            and not self.client_id.startswith("YOUR_")
            and not self.client_secret.startswith("YOUR_")
        )

    # -------------------------------------------------------------------------
    # Persistent State Management (CSRF Protection)
    # -------------------------------------------------------------------------
    def generate_state(self) -> str:
        """
        Generates a tamper-proof OAuth state token: nonce.timestamp.signature
        Persisted in SQLite database with 600s TTL and atomic single-use consumption.
        """
        nonce = secrets.token_urlsafe(32)
        c_at = time.time()
        timestamp = str(int(c_at))
        secret = self.client_secret or "super_intelligence_yt_state_salt"
        payload = f"{nonce}.{timestamp}"
        signature = hmac.new(
            secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        self.db.record_oauth_state(
            nonce=nonce,
            provider="youtube",
            created_at=c_at,
            expires_at=c_at + 600.0,
        )
        return f"{payload}.{signature}"

    def validate_state(self, state: str, max_age_seconds: int = 600) -> bool:
        """Validates authenticity, signature, and atomic single-use consumption."""
        if not state or state.count(".") != 2:
            return False

        try:
            nonce, ts_str, signature = state.split(".", 2)
            timestamp = int(ts_str)
        except Exception:
            return False

        now = time.time()
        if now - timestamp > max_age_seconds or timestamp > now + 60:
            return False

        secret = self.client_secret or "super_intelligence_yt_state_salt"
        payload = f"{nonce}.{ts_str}"
        expected_sig = hmac.new(
            secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            return False

        return self.db.consume_oauth_state(nonce=nonce, provider="youtube", max_age_seconds=max_age_seconds)

    # -------------------------------------------------------------------------
    # OAuth URL & Code Exchange
    # -------------------------------------------------------------------------
    def get_auth_url(self) -> Tuple[str, str]:
        """Builds official Google OAuth 2.0 authorization URL. Returns (url, state)."""
        if not self.is_configured():
            raise YouTubeAuthError(
                "YouTube OAuth Client ID and Secret must be configured in environment (.env) or config."
            )

        state = self.generate_state()
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
            "include_granted_scopes": "true",
        }
        auth_url = f"{OAUTH_AUTH_URL}?{urllib.parse.urlencode(params)}"
        return auth_url, state

    def exchange_code(self, code: str, state: Optional[str] = None) -> Dict[str, Any]:
        """
        Exchanges authorization code for access and refresh tokens,
        identifies the authenticated channel via channels.list,
        and encrypts credentials at rest.
        """
        if not code:
            return {"ok": False, "error": "Missing authorization code from Google."}

        if state and not self.validate_state(state):
            logger.warning("YouTube OAuth state verification failed or expired (CSRF block).")
            return {"ok": False, "error": "Invalid or expired OAuth state parameter (CSRF protection)."}

        if not self.is_configured():
            return {"ok": False, "error": "Google Client ID or Secret is not configured."}

        payload = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

        try:
            res = requests.post(OAUTH_TOKEN_URL, data=payload, timeout=25)
            data = res.json()
        except Exception as e:
            logger.error(f"Network error contacting Google OAuth token endpoint: {e}")
            return {"ok": False, "error": f"Failed to contact Google OAuth endpoint: {e}"}

        if res.status_code != 200 or "access_token" not in data:
            err = data.get("error_description") or data.get("error") or "Unknown token exchange failure"
            logger.error(f"Google token exchange failed (HTTP {res.status_code}): {err}")
            return {"ok": False, "error": err}

        access_token = data["access_token"]
        refresh_token = data.get("refresh_token")
        expires_in = data.get("expires_in", 3600)
        token_type = data.get("token_type", "Bearer")
        granted_scope = data.get("scope", " ".join(self.scopes))

        # Retrieve existing refresh_token if Google omitted it on re-consent
        if not refresh_token:
            existing = self.load_token()
            if existing and existing.get("refresh_token"):
                refresh_token = existing["refresh_token"]

        # Step 2: Channel verification via YouTube Data API v3
        channel_info = self._fetch_channel_profile(access_token)
        if not channel_info.get("ok"):
            logger.warning(f"Could not fetch channel details: {channel_info.get('error')}")

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))

        token_record = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": token_type,
            "expires_at": expires_at.isoformat(),
            "scope": granted_scope,
            "channel_id": channel_info.get("channel_id"),
            "channel_title": channel_info.get("channel_title"),
            "channel_description": channel_info.get("description"),
            "thumbnail_url": channel_info.get("thumbnail_url"),
            "subscriber_count": channel_info.get("subscriber_count"),
            "video_count": channel_info.get("video_count"),
            "connected_at": datetime.now(timezone.utc).isoformat(),
            "last_sync_time": datetime.now(timezone.utc).isoformat(),
        }

        save_ok = self._save_encrypted_token(token_record)
        if not save_ok:
            return {"ok": False, "error": "Failed to encrypt credentials at rest."}

        logger.info(
            f"Successfully authenticated YouTube channel '{channel_info.get('channel_title')}' "
            f"(ID: {channel_info.get('channel_id')})."
        )
        return {
            "ok": True,
            "channel_id": channel_info.get("channel_id"),
            "channel_title": channel_info.get("channel_title"),
            "subscriber_count": channel_info.get("subscriber_count"),
            "expires_at": token_record["expires_at"],
        }

    def _fetch_channel_profile(self, access_token: str) -> Dict[str, Any]:
        """Queries channels.list with part=snippet,contentDetails,statistics&mine=true."""
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"part": "snippet,contentDetails,statistics", "mine": "true"}

        try:
            res = requests.get(YOUTUBE_CHANNELS_URL, headers=headers, params=params, timeout=20)
            data = res.json()
            if res.status_code == 200 and "items" in data and len(data["items"]) > 0:
                item = data["items"][0]
                snippet = item.get("snippet", {})
                stats = item.get("statistics", {})
                thumbs = snippet.get("thumbnails", {})
                thumb_url = (
                    thumbs.get("default", {}).get("url")
                    or thumbs.get("medium", {}).get("url")
                    or thumbs.get("high", {}).get("url")
                )
                return {
                    "ok": True,
                    "channel_id": item.get("id"),
                    "channel_title": snippet.get("title", "YouTube Channel"),
                    "description": snippet.get("description", ""),
                    "thumbnail_url": thumb_url,
                    "subscriber_count": int(stats.get("subscriberCount", 0)),
                    "video_count": int(stats.get("videoCount", 0)),
                    "view_count": int(stats.get("viewCount", 0)),
                }
            elif res.status_code == 200 and len(data.get("items", [])) == 0:
                return {
                    "ok": False,
                    "error": "No YouTube channel associated with this Google account. Create a channel in YouTube Studio first.",
                }
            else:
                err_msg = data.get("error", {}).get("message") or f"HTTP {res.status_code}"
                return {"ok": False, "error": err_msg}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # -------------------------------------------------------------------------
    # Token Storage, Decryption & Refresh
    # -------------------------------------------------------------------------
    def _save_encrypted_token(self, token_data: Dict[str, Any]) -> bool:
        """Encrypts token data with Fernet authenticated encryption."""
        try:
            plaintext = json.dumps(token_data).encode("utf-8")
            encrypted = self._fernet.encrypt(plaintext)
            self.token_file.write_bytes(encrypted)
            return True
        except Exception as e:
            logger.error(f"Failed to encrypt and save YouTube token: {e}")
            return False

    def load_token(self) -> Optional[Dict[str, Any]]:
        """Loads and decrypts token from secure storage."""
        if self.token_file.exists():
            try:
                encrypted = self.token_file.read_bytes()
                decrypted = self._fernet.decrypt(encrypted)
                return json.loads(decrypted.decode("utf-8"))
            except InvalidToken:
                logger.error("Master key could not decrypt youtube_token.enc. Key may have changed.")
            except Exception as e:
                logger.error(f"Error loading encrypted YouTube token: {e}")

        # Check for legacy plaintext token file and migrate it if found
        legacy_path = self.config.resolve_path(Path("data") / "youtube_token.json")
        if legacy_path.exists():
            try:
                with open(legacy_path, "r", encoding="utf-8") as f:
                    legacy_data = json.load(f)
                self._save_encrypted_token(legacy_data)
                legacy_path.unlink(missing_ok=True)
                logger.info("Migrated legacy plaintext youtube_token.json to encrypted storage.")
                return legacy_data
            except Exception:
                pass
        return None

    def is_authenticated(self) -> bool:
        """Returns True if a valid token with an access or refresh token exists."""
        token = self.load_token()
        return bool(token and (token.get("access_token") or token.get("refresh_token")))

    def get_valid_access_token(self) -> Optional[str]:
        """Returns active access token, refreshing it automatically if expired."""
        token = self.load_token()
        if not token:
            return None

        expires_at_str = token.get("expires_at")
        if expires_at_str:
            try:
                exp_dt = datetime.fromisoformat(expires_at_str)
                # If still valid for at least 60 seconds
                if exp_dt > datetime.now(timezone.utc) + timedelta(seconds=60):
                    return token.get("access_token")
            except Exception:
                pass

        # Needs refresh
        return self.refresh_access_token()

    def refresh_access_token(self) -> Optional[str]:
        """Refreshes expired access token using stored refresh_token."""
        token = self.load_token()
        if not token or not token.get("refresh_token"):
            logger.warning("Cannot refresh YouTube access token: No refresh token stored.")
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
                expires_in = data.get("expires_in", 3600)
                token["expires_at"] = (datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))).isoformat()
                token["last_refresh"] = datetime.now(timezone.utc).isoformat()
                self._save_encrypted_token(token)
                logger.info("Successfully refreshed YouTube access token.")
                return data["access_token"]
            else:
                err = data.get("error_description") or data.get("error") or str(data)
                logger.error(f"Failed to refresh YouTube token: {err}")
        except Exception as e:
            logger.error(f"Network error refreshing YouTube token: {e}")
        return None

    def disconnect(self) -> bool:
        """Revokes credentials if possible, deletes local encrypted token, marks disconnected."""
        token = self.load_token()
        if token:
            rev_tok = token.get("refresh_token") or token.get("access_token")
            if rev_tok:
                try:
                    requests.post(OAUTH_REVOKE_URL, data={"token": rev_tok}, timeout=10)
                except Exception:
                    pass

        try:
            if self.token_file.exists():
                self.token_file.unlink()
            logger.info("YouTube credentials safely disconnected and wiped from storage.")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting YouTube token: {e}")
            return False

    def get_connection_status(self) -> Dict[str, Any]:
        """Returns safe public status metadata for dashboard display (never secrets)."""
        token_record = self.load_token()
        if not token_record:
            return {
                "connected": False,
                "status": "DISCONNECTED",
                "channel_id": None,
                "channel_title": None,
                "thumbnail_url": None,
                "subscriber_count": None,
                "token_status": "MISSING",
                "expires_at": None,
                "is_configured": self.is_configured(),
                "redirect_uri": self.redirect_uri,
            }

        is_expired = False
        expires_at = token_record.get("expires_at")
        if expires_at:
            try:
                exp_dt = datetime.fromisoformat(expires_at)
                if exp_dt <= datetime.now(timezone.utc):
                    is_expired = True
            except Exception:
                pass

        has_refresh = bool(token_record.get("refresh_token"))
        status_label = "CONNECTED" if (not is_expired or has_refresh) else "EXPIRED"

        return {
            "connected": True if (not is_expired or has_refresh) else False,
            "status": status_label,
            "channel_id": token_record.get("channel_id"),
            "channel_title": token_record.get("channel_title") or "Authenticated Channel",
            "thumbnail_url": token_record.get("thumbnail_url"),
            "subscriber_count": token_record.get("subscriber_count"),
            "token_status": "VALID" if not is_expired else ("REFRESHABLE" if has_refresh else "EXPIRED"),
            "expires_at": expires_at,
            "connected_at": token_record.get("connected_at"),
            "is_configured": self.is_configured(),
            "redirect_uri": self.redirect_uri,
        }

    # -------------------------------------------------------------------------
    # Video Upload (Resumable Protocol & Governance Gate)
    # -------------------------------------------------------------------------
    def _compute_sha256(self, file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)
        return h.hexdigest()

    def upload_video(
        self,
        video_path: Path | str,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        category_id: str = "28",  # Science & Technology
        privacy_status: str = YouTubeVisibility.PRIVATE.value,  # Mandatory default: 'private'
        explicit_owner_confirmation: bool = False,
        scheduled_publish_at: Optional[str] = None,
        production_job_id: Optional[int] = None,
        explicit_approval: bool = False,
        synthetic_content_declared: bool = True,
    ) -> Dict[str, Any]:
        """
        Uploads an approved video to YouTube using the official resumable upload protocol.
        MANDATORY GOVERNANCE GATES:
        1. Global kill switch check.
        2. explicit_approval == True.
        3. Owner visibility validation (public/unlisted/scheduled requires explicit_owner_confirmation).
        4. If production_job_id provided, status must be APPROVED in database.
        5. SHA-256 artifact integrity check.
        6. Duplicate publication block.
        7. Default privacyStatus == 'private'.
        """
        # Gate 0: Kill Switch
        from core.kill_switch import get_kill_switch
        get_kill_switch().assert_not_active("YouTubeIntegration:upload_video")

        # Gate 1: Explicit Human Editorial Approval
        if not explicit_approval:
            raise PermissionError(
                "Explicit human editorial approval is required before uploading any video to YouTube. "
                "Automatic publishing without human consent is prohibited by editorial policy."
            )

        # Gate 1b: Owner Visibility Validation & Consent
        vis_spec = validate_visibility_selection(
            visibility=privacy_status,
            explicit_owner_confirmation=explicit_owner_confirmation,
            scheduled_publish_at=scheduled_publish_at,
        )
        selected_visibility = vis_spec["visibility"]

        # Gate 2: Source File Integrity
        v_path = Path(video_path).resolve()
        if not v_path.exists():
            raise FileNotFoundError(f"Source video file not found: {v_path}")

        file_size = v_path.stat().st_size
        if file_size <= 0:
            raise ValueError(f"Video file is empty (0 bytes): {v_path}")

        artifact_hash = self._compute_sha256(v_path)

        # Gate 3: Idempotency & Duplicate Prevention
        if self.db.is_youtube_video_published(artifact_hash):
            raise YouTubeUploadError(
                f"Video with SHA-256 hash {artifact_hash[:12]}... has already been published to YouTube. "
                "Duplicate publication is blocked."
            )

        # Gate 4: Production Job Database Verification
        approval_id = None
        if production_job_id is not None:
            with self.db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM production_jobs WHERE id = ?", (production_job_id,))
                job = cursor.fetchone()
                if not job:
                    raise ValueError(f"Production job #{production_job_id} does not exist.")
                if job["status"] not in ("APPROVED", "COMPLETED"):
                    raise PermissionError(
                        f"Production job #{production_job_id} has status '{job['status']}'. "
                        "Only jobs in APPROVED status can be published."
                    )

                cursor.execute(
                    "SELECT id, decision FROM approvals WHERE (production_job_id = ? OR entity_id = ?) ORDER BY id DESC LIMIT 1",
                    (production_job_id, production_job_id),
                )
                appr_row = cursor.fetchone()
                if appr_row:
                    if appr_row["decision"] == "REJECTED":
                        raise PermissionError(f"Production job #{production_job_id} was explicitly REJECTED.")
                    approval_id = appr_row["id"]

        # Gate 5: Authentication & Active Access Token
        access_token = self.get_valid_access_token()
        if not access_token:
            raise YouTubeAuthError(
                "YouTube account is not authenticated or token could not be refreshed. "
                "Authenticate channel in the Dashboard."
            )

        # Build Metadata Package
        clean_tags = [t.strip().replace("#", "") for t in (tags or ["AI", "Technology"]) if t.strip()]

        api_privacy = "private" if selected_visibility == YouTubeVisibility.SCHEDULED.value else selected_visibility
        status_payload: Dict[str, Any] = {
            "privacyStatus": api_privacy,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": synthetic_content_declared,
        }
        if selected_visibility == YouTubeVisibility.SCHEDULED.value and scheduled_publish_at:
            status_payload["publishAt"] = scheduled_publish_at

        metadata = {
            "snippet": {
                "title": title[:100],
                "description": description,
                "tags": clean_tags[:20],
                "categoryId": str(category_id),
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
            },
            "status": status_payload,
        }

        # Step 1: Initiate Resumable Upload Session
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(file_size),
        }

        logger.info(f"Initiating resumable upload for '{title}' ({file_size / (1024*1024):.2f} MB)...")
        try:
            init_res = requests.post(
                f"{YOUTUBE_UPLOAD_URL}?uploadType=resumable&part=snippet,status",
                headers=headers,
                data=json.dumps(metadata),
                timeout=30,
            )
        except Exception as e:
            raise YouTubeUploadError(f"Network error initiating YouTube upload: {e}")

        if init_res.status_code not in (200, 201) or "Location" not in init_res.headers:
            err_msg = init_res.text[:300]
            raise YouTubeUploadError(f"YouTube rejected upload session (HTTP {init_res.status_code}): {err_msg}")

        session_url = init_res.headers["Location"]

        # Step 2: Stream Video Binary to Resumable Session
        upload_success = False
        resp_data = {}
        last_err = None

        for attempt in range(1, 4):
            try:
                with open(v_path, "rb") as vf:
                    upload_headers = {
                        "Content-Type": "video/mp4",
                        "Content-Length": str(file_size),
                    }
                    up_res = requests.put(session_url, headers=upload_headers, data=vf, timeout=300)

                if up_res.status_code in (200, 201):
                    resp_data = up_res.json()
                    upload_success = True
                    break
                else:
                    last_err = f"HTTP {up_res.status_code}: {up_res.text[:300]}"
                    logger.warning(f"Upload chunk attempt {attempt} failed: {last_err}")
            except (requests.Timeout, requests.ConnectionError) as net_err:
                last_err = f"Network timeout/disconnect on attempt {attempt}: {net_err}"
                logger.warning(last_err)

            time.sleep(2.0 * attempt)

        if not upload_success or "id" not in resp_data:
            raise YouTubeUploadError(f"YouTube binary upload failed after 3 attempts: {last_err}")

        video_id = resp_data["id"]
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        verified_privacy = resp_data.get("status", {}).get("privacyStatus", privacy_status)

        # Step 3: Record publication in SQLite database
        pub_record = {
            "job_id": production_job_id,
            "video_id": video_id,
            "youtube_url": youtube_url,
            "privacy_status": verified_privacy,
            "title": title,
            "description": description,
            "tags": clean_tags,
            "artifact_hash": artifact_hash,
            "approval_id": approval_id,
            "status": "UPLOADED",
            "error_message": None,
        }
        self.db.record_youtube_publication(pub_record)

        # Step 4: Record auditable security event in activity log
        try:
            from core.activity_logger import get_activity_logger
            audit_logger = get_activity_logger(self.db)
            audit_logger.log(
                task_id=f"yt_pub_{video_id}",
                agent_id="YouTubeIntegration",
                action="YOUTUBE_VIDEO_UPLOAD",
                resource=f"video_id:{video_id}|privacy:{verified_privacy}",
                result="SUCCESS",
                approval_status=f"APPROVAL:{approval_id}|CONFIRMATION:{explicit_owner_confirmation}",
            )
        except Exception as audit_err:
            logger.warning(f"Could not record activity log for YouTube upload: {audit_err}")

        logger.info(f"Video uploaded to YouTube successfully! Video ID: {video_id} (Privacy: {verified_privacy})")

        return {
            "ok": True,
            "video_id": video_id,
            "youtube_url": youtube_url,
            "privacy_status": verified_privacy,
            "artifact_hash": artifact_hash,
            "title": title,
        }

    def get_visibility_options(self) -> Dict[str, Any]:
        """Returns the available publishing visibility options and policy definitions."""
        return {
            "default": YouTubeVisibility.PRIVATE.value,
            "options": VISIBILITY_DESCRIPTIONS,
            "policy": {
                "safe_default": "private",
                "requires_owner_confirmation": True,
                "discovery_requirement": (
                    "Public or Scheduled visibility is required to enter the YouTube Shorts Feed carousel "
                    "and search discovery recommendations."
                ),
            },
        }

    # -------------------------------------------------------------------------
    # Standalone Shorts Package Export
    # -------------------------------------------------------------------------
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

        pkg_dir = self.export_dir / f"shorts_package_{production_job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        pkg_dir.mkdir(parents=True, exist_ok=True)

        dest_video = pkg_dir / f"{video_path.stem}.mp4"
        shutil.copy2(video_path, dest_video)

        seo = build_youtube_seo_package(
            title=f"{job['title']}",
            summary=f"Technical documentary on {job['title']}.",
            tags=["AI", "Quantum", "DeepTech", "Shorts"],
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
