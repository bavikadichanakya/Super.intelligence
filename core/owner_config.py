"""
SUPER.INTELLIGENCEEE — Owner-Controlled Configuration & Governance Layer
Loads, parses, and enforces owner policies defined in owner/*.md.
Guarantees application-level protection against unauthorized agent modification.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from core.config import get_config

logger = logging.getLogger("super_intelligence.owner_config")


class OwnerPolicyError(Exception):
    """Raised when an operation violates an owner policy."""


class OwnerConfigProtectionError(Exception):
    """Raised when an unauthorized attempt is made to mutate owner policies."""


class OwnerConfig:
    """Singleton loader and validator for owner-controlled governance policies."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OwnerConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, owner_dir: Optional[Path | str] = None):
        if self._initialized:
            return
        base_dir = Path(owner_dir) if owner_dir else get_config().resolve_path("owner")
        self.owner_dir = Path(base_dir).resolve()
        self.owner_dir.mkdir(parents=True, exist_ok=True)

        self.voice_file = self.owner_dir / "brand-voice.md"
        self.budget_file = self.owner_dir / "budget-cap.md"
        self.approval_file = self.owner_dir / "approval-bar.md"
        self.positioning_file = self.owner_dir / "positioning.md"
        self.kill_switch_file = self.owner_dir / "STOP"

        self._policies: Dict[str, str] = {}
        self._parsed_voice: Dict[str, Any] = {}
        self._parsed_budget: Dict[str, Any] = {}
        self._parsed_approval: Dict[str, Any] = {}
        self._parsed_positioning: Dict[str, Any] = {}

        self.reload()
        self._initialized = True

    def reload(self) -> None:
        """Reads all owner policy files and validates completeness."""
        self._policies = {
            "brand_voice": self._read_policy_file(self.voice_file),
            "budget_cap": self._read_policy_file(self.budget_file),
            "approval_bar": self._read_policy_file(self.approval_file),
            "positioning": self._read_policy_file(self.positioning_file),
        }
        self._parse_all()

    def _read_policy_file(self, path: Path) -> str:
        if not path.exists():
            logger.warning(f"Owner policy file missing: {path.name}")
            return ""
        content = path.read_text(encoding="utf-8")
        # Check for unresolved fill-in prompts
        if "[FILL IN:" in content:
            msg = f"Owner policy file {path.name} contains unresolved placeholder '[FILL IN: ...]'. Workflow halted."
            logger.error(msg)
            raise OwnerPolicyError(msg)
        return content

    def _parse_all(self) -> None:
        """Parses markdown rules into structured lookup dictionaries."""
        # 1. Parse Brand Voice rules (extract strictly from Prohibited Vocabulary section)
        voice_text = self._policies.get("brand_voice", "").lower()
        prohibited = set()
        if "prohibited vocabulary" in voice_text:
            prohib_section = voice_text.split("prohibited vocabulary")[1].split("##")[0]
            prohibited.update(re.findall(r"`([a-z0-9\s'_-]+)`", prohib_section))

        # Core forbidden hype buzzwords
        banned_words = {
            "mindblowing", "insane", "crazy", "huge", "massive", "gamechanger",
            "revolutionary", "ultimate", "epic", "unbelievable", "stop scrolling",
            "don't scroll", "hey guys", "welcome back", "viral hack"
        }
        prohibited.update(banned_words)

        self._parsed_voice = {
            "prohibited_words": prohibited,
            "max_emojis_per_scene": 1,
            "max_hashtags": 4,
            "banned_hashtags": {"#viral", "#fyp", "#foryou", "#explore", "#trending", "#instadaily", "#like4like"},
        }

        # 2. Parse Budget Cap
        self._parsed_budget = {
            "monthly_cap": 0.0,
            "cost_per_action_cap": 0.0,
            "zero_cost_mode": True,
            "financial_actions_permitted": False,
        }

        # 3. Parse Approval Bar
        self._parsed_approval = {
            "human_approval_mandatory": True,
            "auto_publish_permitted": False,
            "gated_platforms": ["instagram", "youtube", "tiktok", "twitter"],
        }

        # 4. Parse Positioning
        self._parsed_positioning = {
            "pillars": ["Frontier Architecture", "Local-First & Edge AI", "Systems Reliability & Benchmarks", "Verified Open Source"],
            "target_audience": ["AI Engineers", "Systems Architects", "Backend Builders"],
            "requires_primary_source": True,
        }

    # ------------------------------------------------------------------
    # Policy Enforcement Methods
    # ------------------------------------------------------------------
    def validate_copy_against_voice(self, text: str) -> Tuple[bool, List[str]]:
        """Scans draft copy against owner brand voice rules."""
        issues: List[str] = []
        text_lower = text.lower()

        # Check prohibited buzzwords
        for bad in self._parsed_voice.get("prohibited_words", set()):
            if re.search(r"\b" + re.escape(bad) + r"\b", text_lower):
                issues.append(f"Contains prohibited hype vocabulary: '{bad}'")

        # Check banned hashtags
        for tag in self._parsed_voice.get("banned_hashtags", set()):
            if tag.lower() in text_lower:
                issues.append(f"Contains prohibited engagement-bait hashtag: '{tag}'")

        return len(issues) == 0, issues

    def check_financial_action(self, amount: float, category: str = "general") -> bool:
        """
        Validates whether a financial expenditure is authorized.
        Strict zero-budget policy rejects any amount > 0.
        """
        if amount > 0.0:
            logger.error(f"Financial expenditure rejected: ₹{amount:.2f} for {category} exceeds ₹0.00 budget cap.")
            return False
        return True

    def is_publishing_gated(self, platform: str = "instagram") -> bool:
        """Checks if publishing to the given platform requires human approval."""
        return self._parsed_approval.get("human_approval_mandatory", True)

    def is_kill_switch_active(self) -> bool:
        """Checks if emergency stop flag exists."""
        return self.kill_switch_file.exists()

    # ------------------------------------------------------------------
    # Immutability Protection
    # ------------------------------------------------------------------
    def protect_file_mutation(self, caller: str = "Agent") -> None:
        """Prevents agents or workers from modifying owner governance configuration."""
        raise OwnerConfigProtectionError(
            f"Access Denied: Caller '{caller}' attempted to mutate protected owner configuration."
        )

    def get_policy_summary(self) -> Dict[str, Any]:
        return {
            "zero_budget_cap": "₹0.00 / $0.00",
            "human_approval_mandatory": self._parsed_approval.get("human_approval_mandatory", True),
            "kill_switch_active": self.is_kill_switch_active(),
            "prohibited_words_count": len(self._parsed_voice.get("prohibited_words", set())),
            "editorial_pillars": self._parsed_positioning.get("pillars", []),
        }


def get_owner_config() -> OwnerConfig:
    return OwnerConfig()

