"""
SUPER.INTELLIGENCEEE V2 — Universal Scene Schema & Claim Evidence Models
Canonical data contract for the multi-archetype video production pipeline.
Provides bi-directional compatibility with legacy storyboard dictionaries.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union


class EvidenceStatus(str, Enum):
    """Claim verification status with rigorous credibility tracking."""
    VERIFIED = "VERIFIED"
    SOURCE_REPORTED = "SOURCE_REPORTED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    CONTRADICTED = "CONTRADICTED"
    RESEARCH_BLOCKED = "RESEARCH_BLOCKED"

    # Backward compatibility aliases
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    CONFLICTING_SOURCES = "CONFLICTING_SOURCES"

    @classmethod
    def from_str(cls, val: Union[str, "EvidenceStatus"]) -> "EvidenceStatus":
        if isinstance(val, cls):
            return val
        s = str(val).upper().strip()
        if s in ("PARTIALLY_SUPPORTED", "PARTIAL", "PARTIALLY_VERIFIED"):
            return cls.PARTIALLY_VERIFIED
        if s in ("CONFLICTING_SOURCES", "CONTRADICTED", "CONFLICT"):
            return cls.CONTRADICTED
        if s in ("UNSUPPORTED", "UNVERIFIED"):
            return cls.UNVERIFIED
        if s in ("BLOCKED", "RESEARCH_BLOCKED"):
            return cls.RESEARCH_BLOCKED
        if s in ("SOURCE_REPORTED", "REPORTED"):
            return cls.SOURCE_REPORTED
        if s in ("VERIFIED", "CONFIRMED"):
            return cls.VERIFIED
        return cls.UNVERIFIED


class VisualArchetype(str, Enum):
    """Canonical visual archetypes supported by the production engine."""
    STOCK_BROLL = "stock_broll"
    SKETCH_TITLE = "sketch_title"
    SKETCH_STAT = "sketch_stat"
    SKETCH_LIST = "sketch_list"
    SKETCH_QUOTE = "sketch_quote"
    MOTION_DIAGRAM = "motion_diagram"
    PRODUCT_DEMO = "product_demo"
    EDITORIAL_HUD = "editorial_hud"

    @classmethod
    def from_str(cls, val: Union[str, VisualArchetype]) -> VisualArchetype:
        if isinstance(val, VisualArchetype):
            return val
        s = str(val).lower().strip()
        # Aliases and legacy mappings
        if "broll" in s or "b_roll" in s or "stock" in s:
            return cls.STOCK_BROLL
        if "stat" in s or "metric" in s or "data" in s:
            return cls.SKETCH_STAT
        if "list" in s or "steps" in s or "impact" in s:
            return cls.SKETCH_LIST
        if "quote" in s or "citation" in s:
            return cls.SKETCH_QUOTE
        if "diagram" in s or "architecture" in s or "flow" in s:
            return cls.MOTION_DIAGRAM
        if "demo" in s or "mockup" in s or "screen" in s:
            return cls.PRODUCT_DEMO
        if "title" in s or "hook" in s or "opening" in s:
            return cls.SKETCH_TITLE
        return cls.EDITORIAL_HUD


@dataclass
class ClaimEvidence:
    """Represents a factual claim grounded in source evidence with multi-source verification."""
    claim_id: str
    claim_text: str
    source_url: str = ""
    source_title: str = ""
    supporting_passage: str = ""
    retrieval_timestamp: str = ""
    status: EvidenceStatus = EvidenceStatus.UNVERIFIED
    confidence_score: float = 0.0
    publisher: str = ""
    publication_date: str = ""
    claim_type: str = "quantitative"       # "quantitative" or "qualitative"
    corroborating_sources: List[str] = field(default_factory=list)
    verification_rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "claim_text": self.claim_text,
            "source_url": self.source_url,
            "source_title": self.source_title,
            "supporting_passage": self.supporting_passage,
            "retrieval_timestamp": self.retrieval_timestamp,
            "status": self.status.value,
            "confidence_score": self.confidence_score,
            "publisher": self.publisher,
            "publication_date": self.publication_date,
            "claim_type": self.claim_type,
            "corroborating_sources": list(self.corroborating_sources),
            "verification_rationale": self.verification_rationale,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ClaimEvidence:
        status_raw = data.get("status", EvidenceStatus.UNVERIFIED.value)
        status = EvidenceStatus.from_str(status_raw)
        return cls(
            claim_id=str(data.get("claim_id", "")),
            claim_text=str(data.get("claim_text", "")),
            source_url=str(data.get("source_url", "")),
            source_title=str(data.get("source_title", "")),
            supporting_passage=str(data.get("supporting_passage", "")),
            retrieval_timestamp=str(data.get("retrieval_timestamp", "")),
            status=status,
            confidence_score=float(data.get("confidence_score", 0.0)),
            publisher=str(data.get("publisher", "")),
            publication_date=str(data.get("publication_date", "")),
            claim_type=str(data.get("claim_type", "quantitative")),
            corroborating_sources=list(data.get("corroborating_sources") or []),
            verification_rationale=str(data.get("verification_rationale", "")),
        )


@dataclass
class SceneProps:
    """Properties configuring visual rendering for a specific archetype."""
    headline: str = ""
    lead_in: str = ""
    hero_word: str = ""
    theme: str = "dark"                   # "dark" or "light"
    motion_preset: str = "draw_reveal"    # "draw_reveal", "slide_up", "zoom_punch", "wobble"
    background_asset: Optional[str] = None
    overlay_opacity: float = 0.45
    evidence_ids: List[str] = field(default_factory=list)
    
    # Archetype-specific attributes
    # For sketch_list:
    list_items: List[Dict[str, Any]] = field(default_factory=list) # [{index, title, description, win}]
    # For sketch_stat:
    before: Optional[Dict[str, str]] = None                         # {"label": "Before", "value": "$240"}
    after: Optional[Dict[str, str]] = None                          # {"label": "After", "value": "$0"}
    stat_delta: Optional[str] = None                                # e.g. "10x", "-100%"
    # For sketch_quote:
    quote_text: str = ""
    quote_author: str = ""
    quote_role: str = ""
    # For motion_diagram:
    diagram_nodes: List[Dict[str, Any]] = field(default_factory=list) # [{id, label, type}]
    diagram_edges: List[Dict[str, Any]] = field(default_factory=list) # [{from, to, label}]
    # For product_demo:
    demo_url: str = ""
    demo_actions: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}


@dataclass
class CaptionConfig:
    """Safe area and visual styling parameters for on-screen subtitles."""
    enabled: bool = True
    layout: str = "safe_lower_third"      # "safe_lower_third", "middle_band", "hidden"
    safe_margin_bottom: int = 340         # Pixels from bottom edge (above Instagram UI)
    highlight_keywords: List[str] = field(default_factory=list)
    primary_color: str = "&H0000E5FF"     # ASS format yellow/cyan glow
    font_name: str = "Arial Black"
    font_size: int = 58

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UniversalScene:
    """
    Canonical Universal Scene Model.
    Provides strict typing, validation, and zero-defect backward compatibility
    with legacy dictionary storyboards.
    """
    scene_id: str
    scene_index: int
    duration_seconds: float
    narrative_role: str                   # HOOK, CONTEXT, DEVELOPMENT, EXPLANATION, IMPLICATIONS, LIMITATIONS, TAKEAWAY
    visual_archetype: VisualArchetype
    narration_text: str
    on_screen_text: str
    visual_props: SceneProps = field(default_factory=SceneProps)
    captions: CaptionConfig = field(default_factory=CaptionConfig)
    badge: Optional[str] = None
    instructions: Optional[str] = None
    transition: str = "fade"

    # Backward-compatible property accessors
    @property
    def narration(self) -> str:
        """Legacy alias for narration_text."""
        return self.narration_text

    @property
    def visual_type(self) -> str:
        """Legacy alias for visual_archetype string."""
        return self.visual_archetype.value

    @property
    def scene_number(self) -> int:
        """Legacy alias for scene_index."""
        return self.scene_index

    @property
    def duration(self) -> float:
        """Legacy alias for duration_seconds."""
        return self.duration_seconds

    def validate(self) -> Tuple[bool, List[str]]:
        """Validates scene attributes against production quality criteria."""
        errors = []
        if not self.scene_id:
            errors.append("scene_id must be non-empty.")
        if self.scene_index < 1:
            errors.append(f"scene_index must be >= 1 (got {self.scene_index}).")
        if self.duration_seconds <= 0:
            errors.append(f"duration_seconds must be positive (got {self.duration_seconds}).")
        if not self.narration_text.strip():
            errors.append(f"Scene #{self.scene_index} has empty narration_text.")
        if not self.on_screen_text.strip():
            errors.append(f"Scene #{self.scene_index} has empty on_screen_text.")
        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        """
        Exports canonical dictionary with both modern and legacy fields
        so existing modules and templates work without modification.
        """
        return {
            "scene_id": self.scene_id,
            "scene_index": self.scene_index,
            "scene_number": self.scene_index,        # legacy alias
            "duration_seconds": self.duration_seconds,
            "duration": self.duration_seconds,        # legacy alias
            "narrative_role": self.narrative_role,
            "name": self.narrative_role.replace("_", " ").title(), # legacy alias
            "visual_archetype": self.visual_archetype.value,
            "visual_type": self.visual_archetype.value, # legacy alias
            "scene_type": self.visual_archetype.value,  # graphics.py alias
            "narration_text": self.narration_text,
            "narration": self.narration_text,         # legacy alias
            "on_screen_text": self.on_screen_text,
            "badge": self.badge or f"SCENE {self.scene_index}",
            "instructions": self.instructions or "",
            "transition": self.transition,
            "visual_props": self.visual_props.to_dict(),
            "captions": self.captions.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UniversalScene:
        """Constructs a UniversalScene from either canonical or legacy dictionary."""
        s_idx = int(data.get("scene_index") or data.get("scene_number") or 1)
        s_id = str(data.get("scene_id") or f"scene_{s_idx:03d}")
        
        # Narration extraction with legacy fallbacks
        narration = str(data.get("narration_text") or data.get("narration") or "").strip()
        on_screen = str(data.get("on_screen_text") or data.get("headline") or f"Scene {s_idx}").strip()
        
        duration = float(data.get("duration_seconds") or data.get("duration") or 5.0)
        
        # Archetype resolution
        archetype_raw = (
            data.get("visual_archetype")
            or data.get("visual_type")
            or data.get("scene_type")
            or "editorial_hud"
        )
        archetype = VisualArchetype.from_str(archetype_raw)
        
        # Props extraction
        props_data = data.get("visual_props", {})
        if not isinstance(props_data, dict):
            props_data = {}
            
        headline = props_data.get("headline") or on_screen
        hero = props_data.get("hero_word") or ""
        if not hero:
            words = [w for w in re.findall(r"\b[A-Za-z0-9\$\%]+\b", headline) if len(w) > 3]
            hero = words[0] if words else headline.split()[-1] if headline.split() else "AI"
            
        scene_props = SceneProps(
            headline=headline,
            lead_in=props_data.get("lead_in", data.get("badge", "")),
            hero_word=hero,
            theme=props_data.get("theme", "dark"),
            motion_preset=props_data.get("motion_preset", "draw_reveal"),
            background_asset=props_data.get("background_asset"),
            overlay_opacity=float(props_data.get("overlay_opacity", 0.45)),
            evidence_ids=props_data.get("evidence_ids", []),
            list_items=props_data.get("list_items", []),
            before=props_data.get("before"),
            after=props_data.get("after"),
            stat_delta=props_data.get("stat_delta"),
            quote_text=props_data.get("quote_text", narration),
            quote_author=props_data.get("quote_author", "Verified Source"),
            quote_role=props_data.get("quote_role", "Research Documentation"),
            diagram_nodes=props_data.get("diagram_nodes", []),
            diagram_edges=props_data.get("diagram_edges", []),
            demo_url=props_data.get("demo_url", ""),
            demo_actions=props_data.get("demo_actions", []),
        )

        caps_data = data.get("captions", {})
        if not isinstance(caps_data, dict):
            caps_data = {}
        caption_config = CaptionConfig(
            enabled=caps_data.get("enabled", True),
            layout=caps_data.get("layout", "safe_lower_third"),
            safe_margin_bottom=int(caps_data.get("safe_margin_bottom", 340)),
            highlight_keywords=caps_data.get("highlight_keywords", [hero]),
        )

        role = str(data.get("narrative_role") or data.get("name") or f"SCENE_{s_idx}").upper().replace(" ", "_")

        return cls(
            scene_id=s_id,
            scene_index=s_idx,
            duration_seconds=duration,
            narrative_role=role,
            visual_archetype=archetype,
            narration_text=narration,
            on_screen_text=on_screen,
            visual_props=scene_props,
            captions=caption_config,
            badge=data.get("badge"),
            instructions=data.get("instructions"),
            transition=data.get("transition", "fade"),
        )

    def to_contract(self) -> Any:
        """Losslessly converts UniversalScene to UniversalSceneContract (v3.0.0)."""
        from core.universal_scene_contract import UniversalSceneContract
        return UniversalSceneContract.from_universal_scene(self)

    @classmethod
    def from_contract(cls, contract: Any) -> "UniversalScene":
        """Reconstructs UniversalScene from UniversalSceneContract."""
        return contract.to_universal_scene()


class EditorialWorkflowState(str, Enum):
    """Canonical workflow states for the technology media operating system."""
    DISCOVERED = "DISCOVERED"
    SCORING = "SCORING"
    RESEARCHING = "RESEARCHING"
    RESEARCH_VERIFIED = "RESEARCH_VERIFIED"
    RESEARCH_BLOCKED = "RESEARCH_BLOCKED"
    BRIEF_APPROVED = "BRIEF_APPROVED"
    SCRIPT_READY = "SCRIPT_READY"
    CREATIVE_PLAN_READY = "CREATIVE_PLAN_READY"
    ASSETS_READY = "ASSETS_READY"
    ASSET_REQUIRED = "ASSET_REQUIRED"
    LICENSING_REVIEW = "LICENSING_REVIEW"
    PRODUCING = "PRODUCING"
    QA_PENDING = "QA_PENDING"
    QA_FAILED = "QA_FAILED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    REVISION_REQUIRED = "REVISION_REQUIRED"
    HELD_BY_OWNER = "HELD_BY_OWNER"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    ANALYZED = "ANALYZED"
    REJECTED = "REJECTED"


@dataclass
class Source:
    """Represents a primary or supporting external reference source."""
    source_id: str
    url: str
    title: str = ""
    publisher: str = "Primary Source"
    publication_date: str = ""
    credibility_score: float = 1.0       # 0.0 to 1.0 scale
    raw_content: str = ""
    author: str = ""
    is_primary: bool = True
    retrieval_timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Source:
        return cls(
            source_id=str(data.get("source_id", "src_001")),
            url=str(data.get("url", "")),
            title=str(data.get("title", "")),
            publisher=str(data.get("publisher", "Primary Source")),
            publication_date=str(data.get("publication_date", "")),
            credibility_score=float(data.get("credibility_score", 1.0)),
            raw_content=str(data.get("raw_content", "")),
            author=str(data.get("author", "")),
            is_primary=bool(data.get("is_primary", True)),
            retrieval_timestamp=str(data.get("retrieval_timestamp", "")),
        )


@dataclass
class TopicScoreBreakdown:
    """Transparent 100-point opportunity scoring breakdown with fatigue tracking."""
    information_value: float = 0.0       # max 25 pts: technical substance & depth
    originality: float = 0.0             # max 20 pts: novel angle & low saturation
    evidence_quality: float = 0.0        # max 20 pts: primary source / paper / code
    audience_relevance: float = 0.0      # max 15 pts: builder & engineer utility
    visual_potential: float = 0.0        # max 10 pts: diagram / UI / demo opportunity
    timeliness: float = 0.0              # max 10 pts: recency & current momentum
    fatigue_penalty: float = 0.0         # 0 to -20 pts: recent topic repetition penalty
    decision: str = "REJECT"             # HIGH_PRIORITY (80-100), CONSIDER (65-79), RESEARCH_FURTHER (50-64), REJECT (<50)
    reasoning: str = ""

    @property
    def total_score(self) -> float:
        raw = (
            self.information_value
            + self.originality
            + self.evidence_quality
            + self.audience_relevance
            + self.visual_potential
            + self.timeliness
            - abs(self.fatigue_penalty)
        )
        return round(max(0.0, min(100.0, raw)), 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "information_value": self.information_value,
            "originality": self.originality,
            "evidence_quality": self.evidence_quality,
            "audience_relevance": self.audience_relevance,
            "visual_potential": self.visual_potential,
            "timeliness": self.timeliness,
            "fatigue_penalty": self.fatigue_penalty,
            "total_score": self.total_score,
            "decision": self.decision,
            "reasoning": self.reasoning,
        }


@dataclass
class ResearchDossier:
    """Structured research intelligence dossier for a selected topic."""
    topic_id: str
    topic_title: str
    topic_description: str
    original_angle: str
    primary_sources: List[Source] = field(default_factory=list)
    supporting_sources: List[Source] = field(default_factory=list)
    publication_dates: List[str] = field(default_factory=list)
    important_claims: List[ClaimEvidence] = field(default_factory=list)
    uncertainties: List[str] = field(default_factory=list)
    technical_explanation: str = ""
    limitations: List[str] = field(default_factory=list)
    potential_implications: List[str] = field(default_factory=list)
    visual_opportunities: List[str] = field(default_factory=list)
    suggested_creative_format: str = "tech_documentary" # tech_documentary, trend_shortform, animated_storytelling
    verification_status: str = "UNVERIFIED"             # VERIFIED, UNVERIFIED, RESEARCH_BLOCKED, CONTRADICTED
    score_breakdown: Optional[TopicScoreBreakdown] = None
    selection_rationale: str = ""
    retrieval_timestamp: str = ""
    dossier_provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "topic_title": self.topic_title,
            "topic_description": self.topic_description,
            "original_angle": self.original_angle,
            "primary_sources": [s.to_dict() for s in self.primary_sources],
            "supporting_sources": [s.to_dict() for s in self.supporting_sources],
            "publication_dates": self.publication_dates,
            "important_claims": [c.to_dict() for c in self.important_claims],
            "uncertainties": self.uncertainties,
            "technical_explanation": self.technical_explanation,
            "limitations": self.limitations,
            "potential_implications": self.potential_implications,
            "visual_opportunities": self.visual_opportunities,
            "suggested_creative_format": self.suggested_creative_format,
            "verification_status": self.verification_status,
            "score_breakdown": self.score_breakdown.to_dict() if self.score_breakdown else None,
            "selection_rationale": self.selection_rationale,
            "retrieval_timestamp": self.retrieval_timestamp,
            "dossier_provenance": dict(self.dossier_provenance),
        }


@dataclass
class ContentBrief:
    """Structured content brief linking research to story development."""
    brief_id: str
    topic_id: str
    target_audience: str = "Software engineers, AI researchers, and technical builders"
    learning_objective: str = ""
    central_question: str = ""
    original_editorial_angle: str = ""
    narrative_structure: str = "Hook -> Context -> Breakthrough -> Architecture -> Implications -> Limitations -> Verdict"
    evidence_requirements: List[str] = field(default_factory=list)
    suggested_duration_seconds: float = 58.0
    creative_engine: str = "tech_documentary" # tech_documentary, trend_shortform, animated_storytelling
    visual_treatment: str = "cinematic_diagrammatic"
    audio_treatment: str = "jarvis_british_rp"
    production_complexity: str = "standard"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

