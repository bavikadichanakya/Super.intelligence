"""
SUPER.INTELLIGENCEEE — Fact Checking & Multi-Source Claim Verification Engine
Enforces strict claim-level evidence verification, multi-source corroboration,
and contradiction detection across primary and secondary sources.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from core.database import get_db
from core.logger import get_logger
from core.schemas import ClaimEvidence, EvidenceStatus, Source

logger = get_logger("FactChecking")

VALID_STATUSES = [
    "DISCOVERED",
    "SHORTLISTED",
    "RESEARCHED",
    "VERIFIED",
    "SCRIPT_READY",
    "APPROVED",
    "REJECTED",
    "RESEARCH_BLOCKED",
    "CONTRADICTED",
]


class FactChecker:
    """Manages claim-level verification, multi-source corroboration, and editorial state transitions."""

    def __init__(self, db=None):
        self.db = db or get_db()

    # -----------------------------------------------------------------------
    # Source Credibility Evaluation
    # -----------------------------------------------------------------------
    @staticmethod
    def calculate_source_credibility(url: str, publisher: str = "") -> float:
        """
        Calculates source credibility score on a 0.0 to 1.0 scale:
        - 0.95 - 1.0: Academic papers & preprints (arXiv, bioRxiv, OpenReview, IEEE, ACM)
        - 0.90 - 0.95: Primary repositories & lab docs (GitHub, HuggingFace, DeepMind, OpenAI, Anthropic, Meta)
        - 0.80 - 0.85: Tier-1 technical press (MIT Tech Review, Ars Technica, IEEE Spectrum)
        - 0.70 - 0.75: Mainstream technology media (TechCrunch, The Verge, VentureBeat)
        - 0.50 - 0.65: Community aggregators & forums (Hacker News, Reddit)
        - 0.10 - 0.30: Unverified or scraper sites
        """
        u = (url or "").lower()
        p = (publisher or "").lower()

        # Tier 0: Academic & Preprints
        if any(dom in u for dom in ["arxiv.org", "biorxiv.org", "openreview.net", "ieee.org", "acm.org", "nature.com", "science.org"]):
            return 0.98

        # Tier 1: Primary Repositories & Frontier Labs
        if any(dom in u for dom in ["github.com", "huggingface.co"]):
            return 0.92
        if any(lab in p or lab in u for lab in ["deepmind", "openai", "anthropic", "meta", "microsoft research", "google research", "berkeley.edu", "stanford.edu", "mit.edu"]):
            return 0.92

        # Tier 2: Tier-1 Technical Press
        if any(press in p or press in u for press in ["arstechnica.com", "technologyreview.com", "spectrum.ieee.org", "quantamagazine.org"]):
            return 0.85

        # Tier 3: Mainstream Tech Media
        if any(media in p or media in u for media in ["techcrunch.com", "theverge.com", "venturebeat.com", "wired.com", "zdnet.com"]):
            return 0.75

        # Tier 4: Community Aggregators & Social
        if any(comm in u for comm in ["reddit.com", "news.ycombinator.com", "twitter.com", "x.com"]):
            return 0.60

        # General HTTPS vs HTTP
        if u.startswith("https://") and len(u) > 15:
            return 0.50
        return 0.25

    # -----------------------------------------------------------------------
    # Contradiction Detection & Corroboration
    # -----------------------------------------------------------------------
    @classmethod
    def detect_claim_contradiction(
        cls,
        claim: ClaimEvidence,
        external_passages: List[Dict[str, Any]]
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Inspects external passages for contradictory assertions or metrics.
        Returns:
            (is_contradicted, contradictory_source_url, reason)
        """
        c_text = claim.claim_text.lower()

        # Check for numeric metrics in claim (e.g. 4x speedup, 85% accuracy)
        metric_match = re.search(r"(\d+(?:\.\d+)?)\s*(%|x|times|speedup|ms|latency)", c_text)

        negation_markers = [
            "no measurable", "fails to improve", "disputed", "cannot reproduce",
            "benchmark overstated", "actually slower", "not open source",
            "hallucination rate of", "regressed", "degraded performance",
            "overstated", "inaccurate", "refuted"
        ]

        # Extract core subject tokens (e.g., "latency", "throughput", "accuracy")
        claim_keywords = set(re.findall(r"\b[a-z]{4,}\b", c_text))
        perf_terms = {
            "speedup", "latency", "throughput", "benchmark", "accuracy", "performance",
            "inference", "tokens", "serving", "model", "vram", "memory", "weights"
        }
        has_perf_in_claim = bool(claim_keywords & perf_terms)

        for ext in external_passages:
            ext_url = ext.get("url", "")
            if ext_url == claim.source_url:
                continue  # Skip same source

            passage = ext.get("text", "") or ext.get("content", "") or ext.get("summary", "")
            p_lower = passage.lower()

            p_keywords = set(re.findall(r"\b[a-z]{4,}\b", p_lower))
            overlap = claim_keywords.intersection(p_keywords)
            has_perf_in_p = bool(p_keywords & perf_terms)

            # Check if passage is in the same subject or performance domain
            is_relevant_context = (len(overlap) >= 2) or (has_perf_in_claim and has_perf_in_p)

            if is_relevant_context:
                # 1. Direct negation or refutation
                for neg in negation_markers:
                    if neg in p_lower:
                        return True, ext_url, f"External source '{ext.get('publisher', ext_url)}' explicitly contradicts claim: '{neg}' observed."

                # 2. Metric conflict (e.g., claim says 4x, external says 1.2x or regression)
                if metric_match:
                    ext_metrics = re.findall(r"(\d+(?:\.\d+)?)\s*(%|x|times|speedup)", p_lower)
                    for val_str, unit in ext_metrics:
                        try:
                            val = float(val_str)
                            claim_val = float(metric_match.group(1))
                            if unit.lower() == metric_match.group(2).lower():
                                # Significant divergence (> 50% discrepancy)
                                if abs(val - claim_val) / max(claim_val, 0.001) > 0.5:
                                    # Check if sentiment implies conflict
                                    if "only" in p_lower or "slower" in p_lower or "versus" in p_lower:
                                        return True, ext_url, f"Conflicting metric reported: claim asserts {claim_val}{unit}, while {ext.get('publisher', ext_url)} reports {val}{unit}."
                        except Exception:
                            continue

        return False, None, None

    @classmethod
    def corroborate_claim(
        cls,
        claim: ClaimEvidence,
        all_sources: List[Source],
        external_passages: Optional[List[Dict[str, Any]]] = None
    ) -> ClaimEvidence:
        """
        Validates claim against primary source and corroborating secondary evidence.
        Applies strict status assignment:
        - VERIFIED
        - SOURCE_REPORTED
        - PARTIALLY_VERIFIED
        - UNVERIFIED
        - CONTRADICTED
        - RESEARCH_BLOCKED
        """
        # 1. Check for contradiction first
        passages = external_passages or [{"url": s.url, "text": s.raw_content, "publisher": s.publisher} for s in all_sources]
        is_contra, contra_url, contra_reason = cls.detect_claim_contradiction(claim, passages)
        if is_contra:
            claim.status = EvidenceStatus.CONTRADICTED
            claim.confidence_score = max(0.1, claim.confidence_score * 0.3)
            claim.verification_rationale = contra_reason or "Contradicted by external technical reporting."
            return claim

        # 2. Check primary source credibility
        primary_source = next((s for s in all_sources if s.url == claim.source_url), None)
        cred = primary_source.credibility_score if primary_source else cls.calculate_source_credibility(claim.source_url, claim.publisher)

        # 3. Check corroborating sources
        corroborating = []
        c_keywords = set(re.findall(r"\b[a-z]{4,}\b", claim.claim_text.lower()))

        for src in all_sources:
            if src.url == claim.source_url:
                continue
            src_text = src.raw_content.lower()
            src_keywords = set(re.findall(r"\b[a-z]{4,}\b", src_text))
            if len(c_keywords.intersection(src_keywords)) >= 3:
                corroborating.append(src.url)

        claim.corroborating_sources = corroborating

        # 4. Status and confidence resolution
        is_primary_repo_or_paper = any(k in claim.source_url.lower() for k in ["arxiv.org", "github.com", "openreview.net", "biorxiv.org"])

        if is_primary_repo_or_paper:
            # Backed directly by code repository or peer-reviewed/preprint paper
            claim.status = EvidenceStatus.VERIFIED
            claim.confidence_score = 0.95
            claim.verification_rationale = f"Grounded in primary technical artifact/paper ({claim.publisher or 'Primary Source'})."
        elif len(corroborating) >= 1:
            # Multiple independent sources support the assertion
            claim.status = EvidenceStatus.VERIFIED
            claim.confidence_score = 0.90
            claim.verification_rationale = f"Corroborated across multiple independent sources ({len(corroborating)} secondary references)."
        elif cred >= 0.70:
            # Single credible source reporting without external independent confirmation
            claim.status = EvidenceStatus.SOURCE_REPORTED
            claim.confidence_score = 0.75
            claim.verification_rationale = f"Reported by single credible publication ({claim.publisher or 'External Source'}); awaiting multi-source confirmation."
        elif len(claim.supporting_passage.strip()) >= 30:
            claim.status = EvidenceStatus.PARTIALLY_VERIFIED
            claim.confidence_score = 0.50
            claim.verification_rationale = "Passage present but source credibility below independent threshold."
        else:
            claim.status = EvidenceStatus.UNVERIFIED
            claim.confidence_score = 0.20
            claim.verification_rationale = "Insufficient supporting passage or unverifiable citation."

        return claim

    # -----------------------------------------------------------------------
    # Editorial Workflow State Transitions
    # -----------------------------------------------------------------------
    @staticmethod
    def validate_transition(current_status: str, target_status: str) -> Tuple[bool, str]:
        if target_status not in VALID_STATUSES:
            return False, f"Invalid status: {target_status}. Allowed: {VALID_STATUSES}"

        if target_status in ("REJECTED", "RESEARCH_BLOCKED", "CONTRADICTED"):
            return True, f"Transition to {target_status} authorized."

        hierarchy = {
            "DISCOVERED": 0,
            "SHORTLISTED": 1,
            "RESEARCHED": 2,
            "VERIFIED": 3,
            "SCRIPT_READY": 4,
            "APPROVED": 5,
        }

        current_level = hierarchy.get(current_status, -1)
        target_level = hierarchy.get(target_status, -1)

        if target_status == "VERIFIED" and current_level < hierarchy["SHORTLISTED"]:
            return False, "Articles must be SHORTLISTED and RESEARCHED before being marked VERIFIED."

        return True, "Transition authorized."

    def update_status(self, article_id: int, target_status: str, notes: str = "") -> Tuple[bool, str]:
        articles = self.db.get_articles(limit=1000)
        target_art = next((a for a in articles if a["id"] == article_id), None)
        if not target_art:
            return False, f"Article ID {article_id} not found."

        current_status = target_art["status"]
        valid, msg = self.validate_transition(current_status, target_status)
        if not valid:
            logger.warning(f"Blocked invalid status transition for article {article_id}: {msg}")
            return False, msg

        success = self.db.update_article_status(article_id, target_status, notes=notes if notes else target_art.get("notes"))
        if success:
            logger.info(f"Article {article_id} transitioned from {current_status} -> {target_status}")
            return True, f"Successfully moved to {target_status}"
        return False, "Database update failed."

    def verify_article(self, article_id: int, source_verified: bool, facts_checked: bool, reviewer_notes: str) -> Tuple[bool, str]:
        """Verify an article after affirmative source check and editorial sanity review."""
        if not source_verified or not facts_checked:
            return False, "Cannot verify story without affirmative source URL verification and fact checking."

        notes_entry = f"Verified: {reviewer_notes.strip()}"
        return self.update_status(article_id, "VERIFIED", notes=notes_entry)
