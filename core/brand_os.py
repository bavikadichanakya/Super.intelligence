"""
SUPER.INTELLIGENCEEE — Brand OS Manager
Maintains persistent brand context, audience personas, visual guidelines,
prohibited claims, and time-stamped signals across sessions.
"""

from __future__ import annotations

import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config

logger = logging.getLogger("super_intelligence.brand_os")


class BrandOS:
    """Provides structured, persistent access to brand intelligence and market signals."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BrandOS, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, root_dir: Optional[Path | str] = None):
        if self._initialized:
            return
        base_dir = Path(root_dir) if root_dir else get_config().resolve_path("brand-os")
        self.root_dir = Path(base_dir).resolve()
        self.brand_brain_dir = self.root_dir / "brand-brain"
        self.signals_dir = self.root_dir / "signals"
        self.content_dir = self.root_dir / "content"
        self.creative_dir = self.root_dir / "creative"
        self.social_dir = self.root_dir / "social"
        self.reporting_dir = self.root_dir / "reporting"

        for d in [self.brand_brain_dir, self.signals_dir, self.content_dir, self.creative_dir, self.social_dir, self.reporting_dir]:
            d.mkdir(parents=True, exist_ok=True)

        self._initialized = True

    def get_brand_profile(self) -> str:
        f = self.brand_brain_dir / "brand-profile.md"
        return f.read_text(encoding="utf-8") if f.exists() else "SUPER.INTELLIGENCEEE Deep Tech Media"

    def get_prohibited_claims(self) -> List[str]:
        f = self.brand_brain_dir / "prohibited-claims.md"
        if not f.exists():
            return []
        lines = f.read_text(encoding="utf-8").splitlines()
        claims = []
        for line in lines:
            if line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "-", "*")):
                claims.append(line.strip().lstrip("0123456789.-* "))
        return claims

    def get_visual_guidelines(self) -> str:
        f = self.creative_dir / "visual-guidelines.md"
        return f.read_text(encoding="utf-8") if f.exists() else ""

    def get_platform_guidelines(self) -> str:
        f = self.social_dir / "platform-guidelines.md"
        return f.read_text(encoding="utf-8") if f.exists() else ""

    def add_signal(
        self,
        category: str,
        title: str,
        source_url: str,
        content: str,
        ttl_hours: int = 72,
    ) -> Dict[str, Any]:
        """
        Stores a timestamped market or research signal with provenance.
        Expired signals are excluded from active opportunity planning.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        expires = now + datetime.timedelta(hours=ttl_hours)
        sig_id = f"sig_{int(now.timestamp())}_{abs(hash(title)) % 10000}"

        signal_data = {
            "signal_id": sig_id,
            "category": category,
            "title": title,
            "source_url": source_url,
            "content": content,
            "created_at": now.isoformat(),
            "expires_at": expires.isoformat(),
            "status": "ACTIVE",
        }

        cat_dir = self.signals_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        sig_file = cat_dir / f"{sig_id}.json"
        sig_file.write_text(json.dumps(signal_data, indent=2), encoding="utf-8")
        logger.info(f"Recorded Brand OS signal: {sig_id} ('{title[:40]}')")
        return signal_data

    def get_active_signals(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns all non-expired signals with valid provenance."""
        now = datetime.datetime.now(datetime.timezone.utc)
        active = []

        search_dirs = [self.signals_dir / category] if category else [d for d in self.signals_dir.iterdir() if d.is_dir()]
        for cdir in search_dirs:
            if not cdir.exists():
                continue
            for s_file in cdir.glob("*.json"):
                try:
                    data = json.loads(s_file.read_text(encoding="utf-8"))
                    exp = datetime.datetime.fromisoformat(data["expires_at"])
                    if exp > now:
                        active.append(data)
                    else:
                        data["status"] = "EXPIRED"
                except Exception:
                    continue

        return sorted(active, key=lambda x: x.get("created_at", ""), reverse=True)


def get_brand_os() -> BrandOS:
    return BrandOS()

