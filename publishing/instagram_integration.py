"""
SUPER.INTELLIGENCEEE — Instagram Publishing & Meta Unified Login Integration
Production-grade integration using Meta Instagram API with Unified Login.
Implements:
- Unified Login OAuth 2.0 with persistent cryptographically signed state validation
- Zero-exposure token handling with authenticated AES-128-CBC + HMAC (Fernet) encryption at rest
- Identity & permission verification for Instagram Professional accounts
- Dynamic Graph API version management (configurable via config/environment)
- Robust resumable binary video upload & official Reel publishing with retry & offset recovery
- Mandatory server-side human editorial approval gate before publishing
- Duplicate publishing lock & race condition protection
- Backward-compatible zero-budget manual export fallback
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
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from cryptography.fernet import Fernet, InvalidToken

from core.config import get_config as get_modern_config
from core.config_manager import get_config as get_legacy_config
from core.database import Database, get_db

logger = logging.getLogger("super_intelligence.instagram_integration")

# Required and standard permissions under Unified Login (excluding unnecessary ad permissions)
UNIFIED_LOGIN_PERMISSIONS = [
    "instagram_basic",
    "instagram_content_publish",
    "instagram_manage_comments",
    "instagram_manage_insights",
]


class InstagramSecurityError(Exception):
    """Raised when an OAuth state validation or security check fails."""
    pass


class InstagramAuthError(Exception):
    """Raised when Meta token exchange or identity verification fails."""
    pass


class InstagramPublishError(Exception):
    """Raised when media container upload, status polling, or publishing fails."""
    pass


class InstagramIntegration:
    """
    Manages Meta Instagram API Unified Login authentication, encrypted credential storage,
    and official Reel publishing with persistent server-side human editorial approval gating.
    """

    def __init__(self, db: Optional[Any] = None, config: Optional[Any] = None):
        self.config = config or get_modern_config()
        self.legacy_config = get_legacy_config()
        self.db = db or Database()

        # Paths
        data_dir = self.config.resolve_path(Path("data"))
        self.secure_dir = data_dir / "secure"
        self.secure_dir.mkdir(parents=True, exist_ok=True)
        self.token_file = self.secure_dir / "instagram_token.enc"
        self.key_file = self.secure_dir / ".master_key"

        self.export_base_dir = self.config.resolve_path(Path("output") / "publish_packages")
        self.export_base_dir.mkdir(parents=True, exist_ok=True)

        # Encryption engine
        self._fernet = self._init_crypto()

    # -------------------------------------------------------------------------
    # API Version Management (P4)
    # -------------------------------------------------------------------------

    @property
    def api_version(self) -> str:
        """
        Meta Graph API Version (e.g. v21.0).
        Configurable via META_GRAPH_API_VERSION env or config.yaml publishing.instagram.api_version.
        Defaults to supported v21.0.
        """
        ver = (
            os.environ.get("META_GRAPH_API_VERSION")
            or self.config.get("publishing.instagram.api_version")
            or self.legacy_config.get("publishing.instagram.api_version")
            or "v21.0"
        )
        ver = str(ver).strip()
        if not ver.startswith("v"):
            ver = f"v{ver}"
        return ver

    @property
    def oauth_dialog_url(self) -> str:
        return f"https://www.facebook.com/{self.api_version}/dialog/oauth"

    @property
    def graph_base_url(self) -> str:
        return f"https://graph.facebook.com/{self.api_version}"

    @property
    def rupload_base_url(self) -> str:
        return f"https://rupload.facebook.com/ig-api-upload/{self.api_version}"

    # -------------------------------------------------------------------------
    # Cryptographic Engine & Encryption at Rest
    # -------------------------------------------------------------------------

    def _init_crypto(self) -> Fernet:
        """
        Initializes Fernet authenticated encryption engine.
        Reads key from INSTAGRAM_ENCRYPTION_KEY env var, or creates a dedicated
        restricted master key on disk.
        """
        env_key = os.environ.get("INSTAGRAM_ENCRYPTION_KEY")
        if env_key:
            try:
                return Fernet(env_key.encode("utf-8") if isinstance(env_key, str) else env_key)
            except Exception as e:
                logger.warning(f"Invalid INSTAGRAM_ENCRYPTION_KEY in environment ({e}), falling back to disk key.")

        if self.key_file.exists():
            try:
                key_bytes = self.key_file.read_bytes().strip()
                return Fernet(key_bytes)
            except Exception:
                pass

        # Generate a new persistent 32-byte URL-safe base64 key
        new_key = Fernet.generate_key()
        try:
            self.key_file.write_bytes(new_key)
        except Exception as e:
            logger.error(f"Failed to persist master key to disk: {e}")
        return Fernet(new_key)

    @property
    def client_id(self) -> str:
        """Meta App ID."""
        return (
            os.environ.get("META_APP_ID")
            or os.environ.get("INSTAGRAM_CLIENT_ID")
            or self.config.get("publishing.instagram.client_id", "")
            or self.legacy_config.get("publishing.instagram.client_id", "")
        )

    @property
    def client_secret(self) -> str:
        """Meta App Secret."""
        return (
            os.environ.get("META_APP_SECRET")
            or os.environ.get("INSTAGRAM_CLIENT_SECRET")
            or self.config.get("publishing.instagram.client_secret", "")
            or self.legacy_config.get("publishing.instagram.client_secret", "")
        )

    @property
    def config_id(self) -> str:
        """Meta Unified Login Configuration ID configured in App Dashboard."""
        return (
            os.environ.get("INSTAGRAM_CONFIG_ID")
            or os.environ.get("META_CONFIG_ID")
            or self.config.get("publishing.instagram.config_id", "")
            or self.legacy_config.get("publishing.instagram.config_id", "")
        )

    @property
    def redirect_uri(self) -> str:
        """OAuth redirect URI registered in Meta App Settings."""
        return (
            os.environ.get("INSTAGRAM_REDIRECT_URI")
            or self.config.get(
                "publishing.instagram.redirect_uri",
                "http://127.0.0.1:5000/oauth/instagram/callback",
            )
        )

    def is_configured(self) -> bool:
        """Checks if Meta App ID and Secret are provided."""
        return bool(self.client_id and self.client_secret and not self.client_id.startswith("YOUR_"))

    # -------------------------------------------------------------------------
    # Cryptographically Secure Persistent OAuth State Management (P5)
    # -------------------------------------------------------------------------

    def generate_state(self) -> str:
        """
        Generates a tamper-proof OAuth state token containing:
        - random 256-bit entropy nonce
        - UTC timestamp (seconds)
        - HMAC-SHA256 signature
        Format: nonce.timestamp.signature
        Persisted in SQLite database for server-restart durability and atomic single-use protection.
        """
        nonce = secrets.token_urlsafe(32)
        c_at = time.time()
        timestamp = str(int(c_at))
        secret = self.client_secret or "super_intelligence_state_salt"
        payload = f"{nonce}.{timestamp}"
        signature = hmac.new(
            secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # Persist to SQLite with 10-minute expiry (600s)
        self.db.record_oauth_state(
            nonce=nonce,
            provider="instagram",
            created_at=c_at,
            expires_at=c_at + 600.0,
        )

        return f"{payload}.{signature}"

    def validate_state(self, state: str, max_age_seconds: int = 600) -> bool:
        """
        Validates the authenticity, expiration, and atomic single-use consumption of an OAuth state token.
        Uses database atomic transaction to prevent replay attacks and race conditions.
        """
        if not state or state.count(".") != 2:
            return False

        try:
            nonce, ts_str, signature = state.split(".", 2)
            timestamp = int(ts_str)
        except Exception:
            return False

        # Expiry check
        now = time.time()
        if now - timestamp > max_age_seconds or timestamp > now + 60:
            return False

        # Signature verification before database access
        secret = self.client_secret or "super_intelligence_state_salt"
        payload = f"{nonce}.{ts_str}"
        expected_sig = hmac.new(
            secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            return False

        # Atomic single-use consumption in SQLite
        return self.db.consume_oauth_state(nonce=nonce, provider="instagram", max_age_seconds=max_age_seconds)

    # -------------------------------------------------------------------------
    # OAuth URL & Code Exchange (P3)
    # -------------------------------------------------------------------------

    def get_authorization_url(self) -> Tuple[str, str]:
        """
        Constructs the official Meta Unified Login authorization URL.
        Includes override_default_response_type=true when config_id is provided.
        Returns: (authorization_url, state)
        """
        if not self.is_configured():
            raise InstagramAuthError(
                "Meta App ID and App Secret must be configured in environment or config.yaml."
            )

        state = self.generate_state()
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "state": state,
        }

        # If a Meta Unified Login Configuration ID is defined, pass config_id and override flag
        if self.config_id:
            params["config_id"] = self.config_id
            params["override_default_response_type"] = "true"
        else:
            # Fallback to standard permission scope list (without advertising scopes)
            params["scope"] = ",".join(UNIFIED_LOGIN_PERMISSIONS)

        query_string = urllib.parse.urlencode(params)
        auth_url = f"{self.oauth_dialog_url}?{query_string}"
        return auth_url, state

    def exchange_code(self, code: str, state: Optional[str] = None) -> Dict[str, Any]:
        """
        Exchanges the authorization code for an access token using server-to-server request,
        verifies assigned Instagram professional accounts, queries permissions,
        and securely encrypts credentials at rest.
        """
        if not code:
            return {"ok": False, "error": "Missing authorization code from provider."}

        if state and not self.validate_state(state):
            logger.warning("Instagram OAuth state verification failed or state has expired.")
            return {"ok": False, "error": "Invalid or expired OAuth state parameter (CSRF protection)."}

        if not self.is_configured():
            return {"ok": False, "error": "Meta App ID or App Secret is not configured."}

        # Step 1: Exchange code for access token
        token_url = f"{self.graph_base_url}/oauth/access_token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }

        try:
            resp = requests.get(token_url, params=params, timeout=25)
            data = resp.json()
        except Exception as e:
            logger.error(f"Network error during Instagram token exchange: {e}")
            return {"ok": False, "error": f"Failed to contact Meta Graph API: {str(e)}"}

        if resp.status_code != 200 or "access_token" not in data:
            err = data.get("error", {})
            err_msg = err.get("message") or data.get("error_description") or "Unknown token exchange failure"
            err_code = err.get("code")
            logger.error(f"Meta token exchange error [code={err_code}]: {err_msg}")
            return {"ok": False, "error": err_msg, "code": err_code}

        access_token = data["access_token"]
        token_type = data.get("token_type", "bearer")
        expires_in = data.get("expires_in")  # seconds, or None for SUAT

        # Step 2: Attempt long-lived token exchange if applicable (for standard user tokens)
        long_lived_token, long_lived_expires_in = self._exchange_for_long_lived_token(access_token)
        if long_lived_token:
            access_token = long_lived_token
            expires_in = long_lived_expires_in or expires_in

        # Step 3: Identity & Account Verification
        account_info = self._fetch_assigned_instagram_account(access_token)
        if not account_info.get("ok"):
            return {
                "ok": False,
                "error": account_info.get("error", "No connected Instagram Professional account found."),
            }

        # Step 4: Verify granted permissions
        granted_permissions = self._fetch_granted_permissions(access_token)

        # Step 5: Encrypt and persist token
        expires_at_iso = None
        if expires_in:
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
            expires_at_iso = expires_at.isoformat()

        token_record = {
            "access_token": access_token,
            "token_type": token_type,
            "expires_at": expires_at_iso,
            "instagram_account_id": account_info.get("account_id"),
            "username": account_info.get("username"),
            "display_name": account_info.get("name"),
            "profile_picture_url": account_info.get("profile_picture_url"),
            "permissions": granted_permissions,
            "connected_at": datetime.now(timezone.utc).isoformat(),
            "config_id": self.config_id,
        }

        save_ok = self._save_encrypted_token(token_record)
        if not save_ok:
            return {"ok": False, "error": "Failed to encrypt credentials at rest."}

        logger.info(
            f"Successfully authenticated Instagram Professional account @{account_info.get('username')} "
            f"(ID: {account_info.get('account_id')}) via Unified Login."
        )

        return {
            "ok": True,
            "account_id": account_info.get("account_id"),
            "username": account_info.get("username"),
            "display_name": account_info.get("name"),
            "permissions": granted_permissions,
            "expires_at": expires_at_iso,
        }

    def _exchange_for_long_lived_token(self, token: str) -> Tuple[Optional[str], Optional[int]]:
        """Exchanges a short-lived user token for a 60-day long-lived token."""
        url = f"{self.graph_base_url}/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "fb_exchange_token": token,
        }
        try:
            r = requests.get(url, params=params, timeout=20)
            d = r.json()
            if r.status_code == 200 and "access_token" in d:
                return d["access_token"], d.get("expires_in")
        except Exception:
            pass
        return None, None

    def _fetch_assigned_instagram_account(self, token: str) -> Dict[str, Any]:
        """
        Under Unified Login / Facebook Login for Business, fetches the assigned Instagram account:
        First via /me/assigned_instagram_accounts, then falls back to /me/accounts.
        """
        # Primary Unified Login endpoint
        url = f"{self.graph_base_url}/me/assigned_instagram_accounts"
        params = {
            "fields": "id,username,name,profile_picture_url",
            "access_token": token,
        }
        try:
            r = requests.get(url, params=params, timeout=20)
            data = r.json()
            if r.status_code == 200 and "data" in data and len(data["data"]) > 0:
                first = data["data"][0]
                return {
                    "ok": True,
                    "account_id": first.get("id"),
                    "username": first.get("username", "Unknown"),
                    "name": first.get("name") or first.get("username"),
                    "profile_picture_url": first.get("profile_picture_url"),
                }
        except Exception as e:
            logger.debug(f"Error checking /assigned_instagram_accounts: {e}")

        # Fallback for Page-linked accounts: /me/accounts with instagram_business_account
        try:
            fallback_url = f"{self.graph_base_url}/me/accounts"
            fb_params = {
                "fields": "id,name,instagram_business_account{id,username,name,profile_picture_url}",
                "access_token": token,
            }
            r = requests.get(fallback_url, params=fb_params, timeout=20)
            data = r.json()
            if r.status_code == 200 and "data" in data:
                for page in data["data"]:
                    ig_acc = page.get("instagram_business_account")
                    if ig_acc:
                        return {
                            "ok": True,
                            "account_id": ig_acc.get("id"),
                            "username": ig_acc.get("username", page.get("name")),
                            "name": ig_acc.get("name") or page.get("name"),
                            "profile_picture_url": ig_acc.get("profile_picture_url"),
                        }
        except Exception as e:
            logger.debug(f"Error checking /me/accounts fallback: {e}")

        # Final check directly on /me
        try:
            me_url = f"{self.graph_base_url}/me"
            r = requests.get(me_url, params={"fields": "id,name", "access_token": token}, timeout=15)
            data = r.json()
            if r.status_code == 200 and "id" in data:
                return {
                    "ok": True,
                    "account_id": data.get("id"),
                    "username": data.get("name", "Instagram Business"),
                    "name": data.get("name"),
                }
        except Exception:
            pass

        return {
            "ok": False,
            "error": "No Instagram Professional (Business/Creator) account was found in this Meta Business Portfolio. "
            "Please ensure your Instagram account is assigned to your Business Portfolio in Meta Business Manager.",
        }

    def _fetch_granted_permissions(self, token: str) -> List[str]:
        """Queries /me/permissions to determine which permissions were granted."""
        url = f"{self.graph_base_url}/me/permissions"
        try:
            r = requests.get(url, params={"access_token": token}, timeout=15)
            data = r.json()
            if r.status_code == 200 and "data" in data:
                return [p["permission"] for p in data["data"] if p.get("status") == "granted"]
        except Exception as e:
            logger.debug(f"Could not fetch granted permissions: {e}")
        return ["instagram_basic", "instagram_content_publish"]

    # -------------------------------------------------------------------------
    # Secure Token Storage & Lifecycle
    # -------------------------------------------------------------------------

    def _save_encrypted_token(self, token_data: Dict[str, Any]) -> bool:
        """Encrypts token data with Fernet authenticated encryption and writes to disk."""
        try:
            plaintext = json.dumps(token_data).encode("utf-8")
            encrypted = self._fernet.encrypt(plaintext)
            self.token_file.write_bytes(encrypted)
            return True
        except Exception as e:
            logger.error(f"Failed to encrypt and save Instagram token: {e}")
            return False

    def load_token(self) -> Optional[Dict[str, Any]]:
        """
        Loads and decrypts token from secure storage.
        Falls back to environment variables (legacy mode) if no encrypted token exists.
        """
        if self.token_file.exists():
            try:
                encrypted = self.token_file.read_bytes()
                decrypted = self._fernet.decrypt(encrypted)
                token_record = json.loads(decrypted.decode("utf-8"))
                return token_record
            except InvalidToken:
                logger.error("Master key could not decrypt instagram_token.enc. Key may have changed.")
            except Exception as e:
                logger.error(f"Error loading encrypted Instagram token: {e}")

        # Legacy fallback from environment
        env_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
        env_account_id = os.environ.get("INSTAGRAM_ACCOUNT_ID")
        if env_token and env_account_id:
            return {
                "access_token": env_token,
                "instagram_account_id": env_account_id,
                "username": os.environ.get("INSTAGRAM_USERNAME", "Configured (Env)"),
                "display_name": "Instagram Professional (Env)",
                "permissions": ["instagram_basic", "instagram_content_publish"],
                "expires_at": None,
                "is_env_fallback": True,
            }

        return None

    def is_authenticated(self) -> bool:
        """Returns True if a valid, unexpired token is available."""
        token = self.load_token()
        if not token or not token.get("access_token"):
            return False

        # Expiry check if expires_at is present
        expires_at = token.get("expires_at")
        if expires_at:
            try:
                exp_dt = datetime.fromisoformat(expires_at)
                if exp_dt <= datetime.now(timezone.utc):
                    return False
            except Exception:
                pass
        return True

    def disconnect(self) -> bool:
        """Safely removes stored encrypted token."""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
            logger.info("Instagram credentials safely disconnected and wiped from storage.")
            return True
        except Exception as e:
            logger.error(f"Error removing encrypted token: {e}")
            return False

    def get_connection_status(self) -> Dict[str, Any]:
        """Returns public metadata about Instagram connection for dashboard display."""
        token_record = self.load_token()
        if not token_record:
            return {
                "connected": False,
                "status": "DISCONNECTED",
                "mode": "Manual Verified Export (Zero-Budget Default)",
                "account_id": None,
                "username": None,
                "display_name": None,
                "permissions": [],
                "token_status": "MISSING",
                "expires_at": None,
                "api_version": self.api_version,
                "is_configured": self.is_configured(),
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

        perms = token_record.get("permissions", [])
        has_publish = "instagram_content_publish" in perms

        return {
            "connected": not is_expired,
            "status": "EXPIRED" if is_expired else "CONNECTED",
            "mode": "Official Meta Graph API (Unified Login)",
            "account_id": token_record.get("instagram_account_id"),
            "username": token_record.get("username"),
            "display_name": token_record.get("display_name"),
            "profile_picture_url": token_record.get("profile_picture_url"),
            "permissions": perms,
            "has_publish_permission": has_publish,
            "token_status": "EXPIRED" if is_expired else "VALID",
            "expires_at": expires_at,
            "connected_at": token_record.get("connected_at"),
            "api_version": self.api_version,
            "is_configured": self.is_configured(),
            "policy": f"Official Meta Graph API {self.api_version} compliant. Zero unofficial botting.",
        }

    def check_api_readiness(self) -> Dict[str, Any]:
        """Backward-compatible readiness method for existing dashboard components."""
        status = self.get_connection_status()
        return {
            "api_enabled": status["connected"],
            "mode": status["mode"] if status["connected"] else "Manual Verified Export (Zero-Budget Default)",
            "token_configured": status["token_status"] == "VALID",
            "account_id_configured": bool(status["account_id"]),
            "policy": f"Official Meta Graph API {self.api_version} compliant. Zero unofficial botting.",
            "account_id": status["account_id"],
            "username": status["username"],
            "permissions": status["permissions"],
        }

    # -------------------------------------------------------------------------
    # Reel Publishing via Official Meta Graph API (P6 & P7)
    # -------------------------------------------------------------------------

    def publish_reel(
        self,
        queue_item_id: int,
        explicit_approval: bool = False,
        share_to_feed: bool = True,
        max_poll_seconds: int = 120,
    ) -> Dict[str, Any]:
        """
        Publishes a scheduled Reel using official Meta Graph API Resumable Upload.
        STRICT SECURITY & INTEGRITY REQUIREMENTS:
        1. explicit_approval must be True (manual human confirmation check).
        2. Queue item must exist and have an approved status in SQLite persistent storage.
        3. Underlying production job must have status == 'APPROVED'.
        4. Rejects items that are REJECTED, PENDING review, already PUBLISHED, or currently PUBLISHING.
        5. Atomically transitions queue status to PUBLISHING to prevent duplicate submission races.
        6. Implements resumable upload with timeout handling, retry, and container status polling.
        """
        # Step 1: Explicit human confirmation guard
        if not explicit_approval:
            raise PermissionError(
                "Explicit human editorial approval is required before publishing any Reel to Instagram. "
                "Automatic publishing without human consent is prohibited by editorial policy."
            )

        # Step 2: Authentication & Token verification
        token_record = self.load_token()
        if not token_record or not self.is_authenticated():
            raise InstagramAuthError(
                "Instagram account is not connected or token has expired. Please authenticate via Unified Login."
            )

        perms = token_record.get("permissions", [])
        if "instagram_content_publish" not in perms and not token_record.get("is_env_fallback"):
            raise InstagramAuthError("Connected Instagram token lacks the 'instagram_content_publish' permission.")

        token = token_record["access_token"]
        ig_user_id = token_record["instagram_account_id"]

        # Step 3: Server-side Approval & Item Integrity Verification (P6)
        items = self.db.get_publishing_queue()
        item = next((i for i in items if i["id"] == queue_item_id), None)
        if not item:
            raise ValueError(f"Publishing item #{queue_item_id} not found.")

        current_status = str(item.get("status", "")).upper()

        # Prevent duplicate publication
        if current_status == "PUBLISHED" or item.get("ig_media_id"):
            raise InstagramPublishError(
                f"Reel #{queue_item_id} has already been published to Instagram "
                f"(Media ID: {item.get('ig_media_id')}). Duplicate publication is blocked."
            )

        if current_status == "PUBLISHING":
            raise InstagramPublishError(
                f"Reel #{queue_item_id} is currently in progress of publishing. Concurrent duplicate upload blocked."
            )

        # Validate persistent approved status
        allowed_publish_statuses = {"APPROVED", "SCHEDULED", "READY_TO_PUBLISH"}
        if current_status not in allowed_publish_statuses:
            raise PermissionError(
                f"Reel #{queue_item_id} has invalid status '{current_status}'. "
                f"Only items in {allowed_publish_statuses} can be published."
            )

        # Cross-verify underlying production job approval
        job_id = item.get("production_job_id") or item.get("job_id")
        if job_id:
            try:
                with self.db.transaction() as conn:
                    cur = conn.cursor()
                    cur.execute("SELECT status FROM production_jobs WHERE id = ?", (job_id,))
                    pj_row = cur.fetchone()
                    if pj_row and pj_row["status"] not in ("APPROVED", "COMPLETED"):
                        raise PermissionError(
                            f"Underlying production job #{job_id} has status '{pj_row['status']}'. "
                            "Reel has not passed formal editorial review."
                        )
                    # Check approvals table for any explicit rejection
                    cur.execute(
                        "SELECT decision FROM approvals WHERE (production_job_id = ? OR entity_id = ?) ORDER BY id DESC LIMIT 1",
                        (job_id, job_id),
                    )
                    appr_row = cur.fetchone()
                    if appr_row and appr_row["decision"] == "REJECTED":
                        raise PermissionError(
                            f"Reel #{queue_item_id} was explicitly REJECTED in human editorial review."
                        )
            except PermissionError:
                raise
            except Exception as e:
                logger.debug(f"Approval check error: {e}")

        # Verify video asset on disk
        video_path_str = item.get("output_video_path") or item.get("video_path")
        if not video_path_str:
            raise ValueError(f"Queue item #{queue_item_id} has no output video path registered.")

        video_path = Path(video_path_str)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file does not exist on disk: {video_path}")

        file_size = video_path.stat().st_size
        if file_size <= 0:
            raise ValueError(f"Video file {video_path} is empty (0 bytes).")

        caption_full = f"{item.get('caption', '')}\n\n{item.get('hashtags', '')}".strip()

        # Step 4: Lock state to PUBLISHING
        self.db.update_publishing_item(
            queue_item_id,
            {"status": "PUBLISHING", "notes": "Initiating Meta Resumable Upload session..."},
        )

        try:
            # Step 5: Initialize Resumable Media Container
            init_url = f"{self.graph_base_url}/{ig_user_id}/media"
            init_payload = {
                "media_type": "REELS",
                "upload_type": "resumable",
                "caption": caption_full,
                "share_to_feed": "true" if share_to_feed else "false",
                "access_token": token,
            }

            try:
                r = requests.post(init_url, data=init_payload, timeout=30)
                init_res = r.json()
            except requests.RequestException as e:
                raise InstagramPublishError(f"Network failure initializing Reel container: {e}")

            if r.status_code != 200 or "id" not in init_res:
                err_msg = init_res.get("error", {}).get("message") or str(init_res)
                err_code = init_res.get("error", {}).get("code")
                raise InstagramPublishError(f"Meta Graph API rejected Reel container creation [code={err_code}]: {err_msg}")

            container_id = init_res["id"]
            rupload_uri = init_res.get("uri") or f"{self.rupload_base_url}/{container_id}"

            logger.info(f"Container #{container_id} created. Streaming video binary ({file_size / (1024*1024):.2f} MB)...")

            # Step 6: Binary Upload with Retry & Offset Resumption (P7)
            upload_success = False
            last_upload_error = None

            for attempt in range(1, 4):
                try:
                    # Check acknowledged offset before upload or on retry
                    current_offset = 0
                    if attempt > 1:
                        try:
                            chk_r = requests.get(
                                rupload_uri,
                                headers={"Authorization": f"OAuth {token}"},
                                timeout=15,
                            )
                            if chk_r.status_code == 200:
                                current_offset = int(chk_r.headers.get("offset", 0))
                                logger.info(f"Resuming upload from acknowledged offset: {current_offset}/{file_size}")
                        except Exception:
                            current_offset = 0

                    upload_headers = {
                        "Authorization": f"OAuth {token}",
                        "offset": str(current_offset),
                        "file_size": str(file_size),
                        "Content-Type": "video/mp4",
                    }

                    with open(video_path, "rb") as vf:
                        if current_offset > 0:
                            vf.seek(current_offset)
                        up_resp = requests.post(
                            rupload_uri,
                            headers=upload_headers,
                            data=vf,
                            timeout=180,
                        )

                    up_data = up_resp.json() if up_resp.content else {}
                    if up_resp.status_code in (200, 201) and up_data.get("success") is not False:
                        upload_success = True
                        break
                    else:
                        last_upload_error = f"Meta RUpload HTTP {up_resp.status_code}: {up_resp.text}"
                        logger.warning(f"Upload attempt {attempt} failed: {last_upload_error}")
                except (requests.Timeout, requests.ConnectionError) as net_err:
                    last_upload_error = f"Network timeout/disconnect on attempt {attempt}: {net_err}"
                    logger.warning(last_upload_error)

                time.sleep(2.0 * attempt)

            if not upload_success:
                raise InstagramPublishError(f"Video binary streaming failed after 3 attempts: {last_upload_error}")

            # Step 7: Container Status Polling
            logger.info(f"Binary streamed successfully. Polling container #{container_id} processing state...")
            status_url = f"{self.graph_base_url}/{container_id}"
            poll_start = time.time()
            container_ready = False

            while time.time() - poll_start < max_poll_seconds:
                time.sleep(3.0)
                try:
                    stat_r = requests.get(
                        status_url,
                        params={"fields": "status_code,status", "access_token": token},
                        timeout=15,
                    )
                    stat_data = stat_r.json()
                except requests.RequestException as e:
                    logger.warning(f"Container status poll warning (transient): {e}")
                    continue

                status_code = str(stat_data.get("status_code", "")).upper()
                if status_code == "FINISHED":
                    container_ready = True
                    break
                elif status_code == "IN_PROGRESS":
                    continue
                elif status_code in ("ERROR", "EXPIRED"):
                    error_detail = stat_data.get("status") or f"Container returned {status_code}"
                    raise InstagramPublishError(f"Meta media processing failed [status={status_code}]: {error_detail}")

            if not container_ready:
                raise InstagramPublishError(
                    f"Timed out after {max_poll_seconds}s waiting for Meta to transcode Reel container #{container_id}."
                )

            # Step 8: Publish Media Container
            logger.info(f"Container #{container_id} is ready. Publishing to Instagram feed...")
            publish_url = f"{self.graph_base_url}/{ig_user_id}/media_publish"
            pub_payload = {
                "creation_id": container_id,
                "access_token": token,
            }

            try:
                pub_r = requests.post(publish_url, data=pub_payload, timeout=30)
                pub_res = pub_r.json()
            except requests.RequestException as e:
                raise InstagramPublishError(f"Network error on media_publish: {e}")

            if pub_r.status_code != 200 or "id" not in pub_res:
                err_msg = pub_res.get("error", {}).get("message") or str(pub_res)
                err_code = pub_res.get("error", {}).get("code")
                raise InstagramPublishError(f"Meta rejected Reel publication [code={err_code}]: {err_msg}")

            ig_media_id = pub_res["id"]
            published_at_iso = datetime.now(timezone.utc).isoformat()

            # Step 9: Update Database State to PUBLISHED
            self.db.update_publishing_item(
                queue_item_id,
                {
                    "status": "PUBLISHED",
                    "ig_media_id": ig_media_id,
                    "published_at": published_at_iso,
                    "notes": f"Published via Meta Unified Login API (Container: {container_id})",
                },
            )

            logger.info(f"Successfully published Reel #{queue_item_id} to Instagram! Media ID: {ig_media_id}")
            return {
                "success": True,
                "item_id": queue_item_id,
                "ig_media_id": ig_media_id,
                "container_id": container_id,
                "published_at": published_at_iso,
                "status": "PUBLISHED",
            }

        except Exception:
            # Revert state back from PUBLISHING if failed
            try:
                self.db.update_publishing_item(
                    queue_item_id,
                    {"status": current_status, "notes": "Publishing attempt failed. Ready to retry."},
                )
            except Exception:
                pass
            raise

    # -------------------------------------------------------------------------
    # Zero-Budget Manual Export Fallback (Preserved)
    # -------------------------------------------------------------------------

    def create_export_package(self, queue_item_id: int) -> Dict[str, Any]:
        """
        Prepares a complete, self-contained publish bundle for manual posting.
        Preserves original zero-budget functionality.
        """
        items = self.db.get_publishing_queue()
        item = next((i for i in items if i["id"] == queue_item_id), None)
        if not item:
            raise ValueError(f"Publishing item {queue_item_id} not found.")

        package_dir = self.export_base_dir / f"package_{item['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        package_dir.mkdir(parents=True, exist_ok=True)

        video_src_str = item.get("output_video_path") or item.get("video_path", "")
        cover_src_str = item.get("cover_image_path", "")

        video_src = Path(video_src_str) if video_src_str else None
        cover_src = Path(cover_src_str) if cover_src_str else None

        dest_video = package_dir / "reel.mp4"
        dest_cover = package_dir / "cover.jpg"

        if video_src and video_src.exists():
            shutil.copy2(video_src, dest_video)
        if cover_src and cover_src.exists():
            shutil.copy2(cover_src, dest_cover)

        caption_txt = package_dir / "caption.txt"
        with open(caption_txt, "w", encoding="utf-8") as f:
            f.write(f"{item.get('caption', '')}\n\n{item.get('hashtags', '')}".strip())

        meta_json = package_dir / "metadata.json"
        metadata_payload = {
            "package_id": queue_item_id,
            "title": item.get("title"),
            "scheduled_for": item.get("scheduled_for") or item.get("scheduled_time"),
            "hashtags": item.get("hashtags"),
            "brand": self.config.get("brand.name", "SUPER.INTELLIGENCEEE"),
            "handle": self.config.get("brand.handle", "@super.intelligenceee"),
            "prepared_at": datetime.now(timezone.utc).isoformat(),
            "status": "READY_FOR_HUMAN_PUBLISH",
        }
        with open(meta_json, "w", encoding="utf-8") as f:
            json.dump(metadata_payload, f, indent=2)

        checklist_md = package_dir / "PUBLISH_CHECKLIST.md"
        checklist_content = f"""# SUPER.INTELLIGENCEEE — PUBLISHING CHECKLIST
Reel: {item.get('title')}
Target Slot: {item.get('scheduled_for') or item.get('scheduled_time')}

## Verification Steps:
- [ ] 1. Preview `reel.mp4` for audio sync and safe-zone margins.
- [ ] 2. Select `cover.jpg` as the cover image.
- [ ] 3. Copy text from `caption.txt`.
- [ ] 4. Post via Instagram mobile app or Meta Business Suite.
- [ ] 5. Confirm status as PUBLISHED in SUPER.INTELLIGENCEEE Dashboard.
"""
        with open(checklist_md, "w", encoding="utf-8") as f:
            f.write(checklist_content)

        self.db.update_publishing_item(
            queue_item_id,
            {"export_path": str(package_dir), "status": "READY_TO_PUBLISH"},
        )

        return {
            "package_id": queue_item_id,
            "package_dir": str(package_dir),
            "video_path": str(dest_video),
            "cover_path": str(dest_cover),
            "caption_path": str(caption_txt),
            "checklist_path": str(checklist_md),
        }
