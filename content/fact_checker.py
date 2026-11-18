"""
SUPER.INTELLIGENCEEE V2 — Claim-Level Fact Verification Engine
Verifies script claims, validates quantitative assertions against source evidence,
prevents hallucinations, and manages editorial approval.
"""

from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Optional, Tuple

from core.database import get_db
from core.logger import get_logger
from core.schemas import ClaimEvidence, EvidenceStatus
from core.task_status import ScriptStatus

logger = get_logger("FactChecker")


class AuditResult(tuple):
    """Backwards-compatible tuple (ok, issues) that also carries claims list."""
    def __new__(cls, ok: bool, issues: List[str], claims: List[ClaimEvidence]):
        return super().__new__(cls, (ok, issues))

    def __init__(self, ok: bool, issues: List[str], claims: List[ClaimEvidence]):
        self.ok = ok
        self.issues = issues
        self.claims = claims


class FactChecker:
    """Verifies script claims, detects potential hallucinations, and manages editorial approval."""

    def __init__(self, db=None, config=None):
        self.db = db or get_db()
        self.config = config

    def extract_claims(self, script_data: Dict[str, Any]) -> List[ClaimEvidence]:
        """
        Parses script narrative text into discrete claim evidence records.
        Identifies quantitative claims, performance multipliers, percentages, and factual assertions.
        """
        claims: List[ClaimEvidence] = []
        source_url = script_data.get("source_url") or ""
        sources = script_data.get("sources", [])
        if not source_url and sources and isinstance(sources, list) and sources[0].get("url"):
            source_url = sources[0].get("url", "")

        publisher = script_data.get("publisher", "Primary Source")
        now_ts = datetime.datetime.now().isoformat()

        # Gather sections to inspect
        sections = [
            ("hook", script_data.get("hook", "")),
            ("development", script_data.get("development", "")),
            ("explanation", script_data.get("explanation", "")),
            ("implications", script_data.get("implications", "")),
            ("limitations", script_data.get("limitations", "")),
            ("takeaway", script_data.get("takeaway", "")),
        ]

        claim_idx = 1
        for sec_name, text in sections:
            if not text:
                continue
            # Split into sentences
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 15]
            for s in sentences:
                # Check if sentence contains verifiable factual assertions or metrics
                has_metric = bool(
                    re.search(r"\b\d+(\.\d+)?%|\b\d+(\.\d+)?x\b|\$[\d,]+|\b\d+(?:,\d+)*(?:\.\d+)?\s*(?:million|billion|tokens|ms|fps|gb|vram|ghz)\b", s, re.IGNORECASE)
                )
                has_assertion = any(kw in s.lower() for kw in [
                    "benchmark", "breakthrough", "linear", "reduces", "improves", "demonstrated", 
                    "unveiled", "outperforms", "scaling", "latency", "pruning", "inference"
                ])

                if has_metric or has_assertion:
                    claim = ClaimEvidence(
                        claim_id=f"claim_{claim_idx:03d}_{sec_name}",
                        claim_text=s,
                        source_url=source_url,
                        source_title=f"{publisher} Documentation",
                        supporting_passage="",
                        retrieval_timestamp=now_ts,
                        status=EvidenceStatus.UNVERIFIED,
                        confidence_score=0.0,
                    )
                    claims.append(claim)
                    claim_idx += 1

        return claims

    def audit_script_claims(
        self,
        script_data: Dict[str, Any],
        dossier: Optional[Any] = None,
    ) -> Tuple[bool, List[str], List[ClaimEvidence]]:
        """
        Verify that claims in script match source topic metadata and evidence.
        Flags unsupported statistics, missing provenance, and metric hallucinations.
        Supports deep evaluation against structured ResearchDossiers and raw source passages.
        """
        issues: List[str] = []
        sources = script_data.get("sources", [])
        source_url = script_data.get("source_url") or ""

        # Resolve dossier if attached to script_data
        active_dossier = dossier or script_data.get("dossier") or script_data.get("research_dossier")

        # 0. Check for research blocked status
        if active_dossier:
            d_status = getattr(active_dossier, "verification_status", None)
            if isinstance(active_dossier, dict):
                d_status = active_dossier.get("verification_status")
            if d_status == "RESEARCH_BLOCKED":
                issues.append("Research dossier marked RESEARCH_BLOCKED: cannot verify script without valid primary evidence.")

        # 0b. Anti-self-approval guard: Script writer cannot mark its own claims verified
        if script_data.get("self_verified") is True:
            issues.append("Script writer cannot mark its own claims as verified. Independent editorial QA required.")

        # 1. Provenance check
        has_valid_url = bool(source_url) or (isinstance(sources, list) and any(s.get("url") for s in sources))
        if active_dossier:
            p_sources = getattr(active_dossier, "primary_sources", [])
            if isinstance(active_dossier, dict):
                p_sources = active_dossier.get("primary_sources", [])
            if p_sources:
                has_valid_url = True

        if not has_valid_url:
            issues.append("Missing primary source URL reference.")

        # 2. Compile reference ground truth from topic context and raw source text
        ref_corpus_parts = [
            script_data.get("title", ""),
            script_data.get("summary", ""),
            script_data.get("context", ""),
            script_data.get("content_objective", ""),
        ]

        # Include raw text from ResearchDossier if available
        if active_dossier:
            p_sources = getattr(active_dossier, "primary_sources", [])
            if isinstance(active_dossier, dict):
                p_sources = active_dossier.get("primary_sources", [])
            for ps in p_sources:
                raw_txt = getattr(ps, "raw_content", "") if not isinstance(ps, dict) else ps.get("raw_content", "")
                if raw_txt:
                    ref_corpus_parts.append(raw_txt)

        # Include any text from sources
        if isinstance(sources, list):
            for s in sources:
                if isinstance(s, dict):
                    ref_corpus_parts.append(s.get("title", ""))
                    ref_corpus_parts.append(s.get("summary", ""))
                    ref_corpus_parts.append(s.get("snippet", ""))
                    ref_corpus_parts.append(s.get("raw_content", ""))

        ref_corpus = " ".join(ref_corpus_parts).lower()

        # 3. Extract claims and evaluate support
        claims = self.extract_claims(script_data)

        # Pattern to capture quantitative metrics
        metric_pattern = re.compile(
            r"\b(\d+(?:\.\d+)?%|\d+(?:\.\d+)?x|\$[\d,]+|\d+(?:,\d+)*(?:\.\d+)?\s*(?:million|billion|tokens|ms|fps|gb|vram))\b",
            re.IGNORECASE,
        )

        for claim in claims:
            c_text_lower = claim.claim_text.lower()
            metrics_in_claim = metric_pattern.findall(claim.claim_text)

            # Check if metrics are grounded in reference corpus
            metric_unsupported = False
            for m in metrics_in_claim:
                clean_m = m.lower().strip()
                if clean_m not in ref_corpus:
                    metric_unsupported = True
                    issues.append(
                        f"Ungrounded quantitative claim in {claim.claim_id}: '{m}' not supported by primary source evidence."
                    )

            if metric_unsupported:
                claim.status = EvidenceStatus.UNSUPPORTED
                claim.confidence_score = 0.1
            else:
                # Check semantic keywords support
                claim_words = [w for w in re.findall(r"\b[a-z]{4,}\b", c_text_lower) if w not in {"this", "that", "with", "from", "their", "more"}]
                if claim_words:
                    overlap = sum(1 for w in claim_words if w in ref_corpus)
                    overlap_ratio = overlap / len(claim_words)
                    if overlap_ratio >= 0.5:
                        claim.status = EvidenceStatus.VERIFIED
                        claim.confidence_score = min(1.0, round(0.5 + overlap_ratio * 0.5, 2))
                        claim.supporting_passage = "Corroborated by primary evidence and documentation."
                    elif overlap_ratio >= 0.25:
                        claim.status = EvidenceStatus.PARTIALLY_SUPPORTED
                        claim.confidence_score = round(overlap_ratio, 2)
                        claim.supporting_passage = "Partial keyword alignment with source context."
                    else:
                        claim.status = EvidenceStatus.UNVERIFIED
                        claim.confidence_score = 0.3
                else:
                    claim.status = EvidenceStatus.VERIFIED
                    claim.confidence_score = 0.8

        is_valid = len(issues) == 0
        return AuditResult(is_valid, issues, claims)

    def check_script(
        self,
        script_data: Dict[str, Any],
        script_id: Optional[int] = None,
        dossier: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Audits claims and returns full verification report with evidence grounding.
        Blocks automatic approval if ungrounded claims or missing source URLs are detected.
        """
        audit_res = self.audit_script_claims(script_data, dossier=dossier)
        ok = audit_res.ok
        issues = audit_res.issues
        claims = audit_res.claims

        evidence_summary = {
            "total_claims": len(claims),
            "verified": sum(1 for c in claims if c.status == EvidenceStatus.VERIFIED),
            "partially_supported": sum(1 for c in claims if c.status == EvidenceStatus.PARTIALLY_SUPPORTED),
            "unsupported": sum(1 for c in claims if c.status == EvidenceStatus.UNSUPPORTED),
        }

        if ok and script_id:
            try:
                self.approve_script(script_id, reviewer="Automated Fact Checker", notes="Source and metrics verified")
            except Exception as e:
                logger.warning(f"Could not record approval for script #{script_id}: {e}")
        elif not ok and script_id:
            try:
                self.reject_script(script_id, reason="; ".join(issues), reviewer="Automated Fact Checker")
            except Exception as e:
                logger.warning(f"Could not record rejection for script #{script_id}: {e}")

        return {
            "verified": ok,
            "issues": issues,
            "claims": [c.to_dict() for c in claims],
            "evidence_summary": evidence_summary,
        }

    def approve_script(self, script_id: int, reviewer: str = "Human Editor", notes: str = "Verified technical facts.") -> Tuple[bool, str]:
        script = self.db.get_script_by_id(script_id)
        if not script:
            return False, f"Script {script_id} not found."

        script["status"] = ScriptStatus.APPROVED.value
        self.db.update_script(script_id, script)
        self.db.record_approval("script", script_id, "APPROVED", feedback=notes, reviewer=reviewer)
        logger.info(f"Script #{script_id} APPROVED by {reviewer}")
        return True, "Script successfully approved for production."

    def reject_script(self, script_id: int, reason: str, reviewer: str = "Human Editor") -> Tuple[bool, str]:
        script = self.db.get_script_by_id(script_id)
        if not script:
            return False, f"Script {script_id} not found."

        script["status"] = ScriptStatus.REJECTED.value
        self.db.update_script(script_id, script)
        self.db.record_approval("script", script_id, "REJECTED", feedback=reason, reviewer=reviewer)
        logger.info(f"Script #{script_id} REJECTED by {reviewer}: {reason}")
        return True, "Script marked as rejected."
