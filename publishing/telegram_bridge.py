"""
SUPER.INTELLIGENCEEE — Telegram Review & Alerting Bridge
Enables remote human-in-the-loop review, approval/rejection commands, and production alerts.
Zero-subscription cost utilizing the free Telegram Bot API.
"""

from __future__ import annotations

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

from core.config import get_config
from core.database import Database
from publishing.approval import ApprovalManager

logger = logging.getLogger("super_intelligence.telegram_bridge")


class TelegramBridge:
    """Telegram Bot bridge for review notifications, video dispatch, and remote approvals."""

    def __init__(
        self,
        bot_token: Optional[str] = None,
        chat_id: Optional[str] = None,
        db: Optional[Database] = None,
        config=None,
    ):
        self.config = config or get_config()
        self.db = db or Database()
        self.bot_token = (
            bot_token
            or os.environ.get("TELEGRAM_BOT_TOKEN")
            or self.config.get("publishing.telegram.bot_token", "")
        )
        self.chat_id = (
            chat_id
            or os.environ.get("TELEGRAM_CHAT_ID")
            or self.config.get("publishing.telegram.chat_id", "")
        )
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"
        self.approval_mgr = ApprovalManager(self.db, self.config)

    def is_configured(self) -> bool:
        """Returns True if valid token and chat_id are present."""
        return bool(self.bot_token and self.chat_id and not self.bot_token.startswith("YOUR_"))

    def send_notification(self, text: str, parse_mode: str = "Markdown") -> Dict[str, Any]:
        """Sends a text alert or notification to the configured Telegram chat."""
        if not self.is_configured():
            logger.warning("TelegramBridge is not configured (missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID).")
            return {
                "success": False,
                "status": "NOT_CONFIGURED",
                "message": "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be configured in environment or config.json."
            }

        url = f"{self.api_base}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }

        try:
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
            if res.status_code == 200 and data.get("ok"):
                return {"success": True, "status": "DELIVERED", "message_id": data["result"]["message_id"]}
            else:
                logger.error(f"Telegram sendMessage failed: {data}")
                return {"success": False, "status": "API_ERROR", "error": data.get("description", "Unknown error")}
        except Exception as e:
            logger.exception(f"Telegram notification exception: {e}")
            return {"success": False, "status": "NETWORK_ERROR", "error": str(e)}

    def send_reel_for_review(
        self,
        production_job_id: int,
        video_path: str | Path,
        title: str,
        caption_text: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Dispatches a draft video to the Telegram chat with technical specs
        and interactive inline approval buttons.
        """
        if not self.is_configured():
            logger.warning("TelegramBridge is not configured (missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID).")
            return {
                "success": False,
                "status": "NOT_CONFIGURED",
                "message": "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be configured in environment or config.json."
            }

        v_path = Path(video_path)
        if not v_path.exists():
            return {"success": False, "status": "FILE_NOT_FOUND", "message": f"Video file not found: {v_path}"}

        url = f"{self.api_base}/sendVideo"
        meta = metadata or {}
        duration = meta.get("duration", "N/A")
        fps = meta.get("fps", 30)
        size_mb = round(v_path.stat().st_size / (1024 * 1024), 2)

        caption_msg = (
            f"🎬 *SUPER.INTELLIGENCEEE — REVIEW REQUIRED*\n\n"
            f"📌 *Job #*: `{production_job_id}`\n"
            f"📰 *Title*: {title}\n"
            f"⏱ *Duration*: `{duration}s` | *FPS*: `{fps}` | *Size*: `{size_mb} MB`\n\n"
            f"📝 *Caption Draft*:\n_{caption_text[:300]}_{'...' if len(caption_text) > 300 else ''}\n\n"
            f"Select decision below to update database and schedule queue:"
        )

        inline_keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ Approve Reel", "callback_data": f"approve_{production_job_id}"},
                    {"text": "❌ Reject Reel", "callback_data": f"reject_{production_job_id}"},
                ]
            ]
        }

        try:
            with open(v_path, "rb") as video_file:
                files = {"video": (v_path.name, video_file, "video/mp4")}
                data = {
                    "chat_id": self.chat_id,
                    "caption": caption_msg,
                    "parse_mode": "Markdown",
                    "reply_markup": json.dumps(inline_keyboard),
                }
                res = requests.post(url, data=data, files=files, timeout=60)
                resp_json = res.json()

                if res.status_code == 200 and resp_json.get("ok"):
                    logger.info(f"Reel #{production_job_id} dispatched to Telegram for human review.")
                    return {
                        "success": True,
                        "status": "SUBMITTED_TO_TELEGRAM",
                        "message_id": resp_json["result"]["message_id"],
                    }
                else:
                    logger.error(f"Telegram sendVideo failed: {resp_json}")
                    return {"success": False, "status": "API_ERROR", "error": resp_json.get("description")}

        except Exception as e:
            logger.exception(f"Failed to send video to Telegram: {e}")
            return {"success": False, "status": "DISPATCH_FAILED", "error": str(e)}

    def handle_callback_action(self, callback_data: str, reviewer: str = "Telegram Editor") -> Dict[str, Any]:
        """
        Executes approval decision from Telegram inline button callback.
        Supports: 'approve_<job_id>' and 'reject_<job_id>'
        """
        if callback_data.startswith("approve_"):
            try:
                job_id = int(callback_data.split("_")[1])
                res = self.approval_mgr.approve_reel(
                    production_job_id=job_id,
                    reviewer_name=reviewer,
                    notes="Approved remotely via Telegram Review Bridge.",
                )
                self.send_notification(f"✅ *Reel #{job_id} APPROVED* by {reviewer}. Scheduled for Instagram.")
                return {"success": True, "action": "APPROVED", "result": res}
            except Exception as e:
                return {"success": False, "action": "APPROVE_ERROR", "error": str(e)}

        elif callback_data.startswith("reject_"):
            try:
                job_id = int(callback_data.split("_")[1])
                res = self.approval_mgr.reject_reel(
                    production_job_id=job_id,
                    reviewer_name=reviewer,
                    reason="Rejected remotely via Telegram Review Bridge.",
                )
                self.send_notification(f"❌ *Reel #{job_id} REJECTED* by {reviewer}. Moved to failed drafts.")
                return {"success": True, "action": "REJECTED", "result": res}
            except Exception as e:
                return {"success": False, "action": "REJECT_ERROR", "error": str(e)}

        return {"success": False, "action": "UNKNOWN_CALLBACK", "callback_data": callback_data}

