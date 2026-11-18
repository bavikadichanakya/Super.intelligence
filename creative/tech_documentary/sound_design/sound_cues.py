"""
SUPER.INTELLIGENCEEE — Phase 3.5 Event-Driven Sound Cue System
Provides structured temporal audio cues mapped directly to visual & narrative anchors:
Every sound effect MUST link to an identifiable visual event or narrative inflection point.
Zero arbitrary or floating whooshes.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("super_intelligence.sound_cues")


@dataclass
class SoundCue:
    """Represents a discrete audio event anchored to an exact visual or narrative timestamp."""
    cue_id: str
    event_type: str  # e.g., "SCENE_TRANSITION", "TERMINAL_EXECUTE", "NODE_PULSE", "METRIC_LAND", "VERDICT_RESOLVE"
    timestamp_ms: int
    visual_anchor: str  # Human-auditable description of the visual event
    asset_name: str  # File name in sfx directory
    volume: float = 0.15
    duration_ms: Optional[int] = None
    notes: str = ""

    @property
    def timestamp_seconds(self) -> float:
        return self.timestamp_ms / 1000.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SoundCueTimeline:
    """Collection and orchestration timeline of sound cues across a documentary."""
    doc_id: str
    total_duration_ms: int
    cues: List[SoundCue] = field(default_factory=list)

    def add_cue(
        self,
        event_type: str,
        timestamp_ms: int,
        visual_anchor: str,
        asset_name: str,
        volume: float = 0.15,
        cue_id: Optional[str] = None,
        duration_ms: Optional[int] = None,
        notes: str = "",
    ) -> SoundCue:
        if cue_id is None:
            cue_id = f"cue_{len(self.cues) + 1:03d}_{event_type.lower()}"
        cue = SoundCue(
            cue_id=cue_id,
            event_type=event_type,
            timestamp_ms=int(timestamp_ms),
            visual_anchor=visual_anchor,
            asset_name=asset_name,
            volume=round(volume, 3),
            duration_ms=duration_ms,
            notes=notes,
        )
        self.cues.append(cue)
        self.sort()
        return cue

    def sort(self) -> None:
        self.cues.sort(key=lambda c: c.timestamp_ms)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "total_duration_ms": self.total_duration_ms,
            "total_duration_seconds": round(self.total_duration_ms / 1000.0, 3),
            "cue_count": len(self.cues),
            "cues": [c.to_dict() for c in self.cues],
        }

    def save_json(self, output_path: Path | str) -> Path:
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Saved SoundCueTimeline with {len(self.cues)} cues to {out_p.name}")
        return out_p

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SoundCueTimeline:
        timeline = cls(
            doc_id=data.get("doc_id", "unknown"),
            total_duration_ms=data.get("total_duration_ms", 0),
        )
        for c in data.get("cues", []):
            timeline.cues.append(SoundCue(**c))
        timeline.sort()
        return timeline

