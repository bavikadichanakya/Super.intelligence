"""
SUPER.INTELLIGENCEEE — Voice Director Subsystem
Provides structured narration direction, pacing control, pause placement,
phonetic normalization, and engine-aware delivery tag filtering.
Strictly ensures unsupported tags are never sent to engines that read them literally.
"""

from __future__ import annotations

import dataclasses
import enum
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("super_intelligence.voice_director")


class NarrationTone(str, enum.Enum):
    """Supported editorial tones for technology documentary narration."""
    CURIOUS = "curious"                  # Inquiring, open, curiosity-gap framing
    CONVERSATIONAL = "conversational"    # Natural, warm, approachable cadence
    AUTHORITATIVE = "authoritative"      # Confident, resolute, deep conviction
    DRAMATIC = "dramatic"                # Tension-filled, high-contrast pauses, gravity
    ANALYTICAL = "analytical"            # Measured, precise, data-focused
    REFLECTIVE = "reflective"            # Thoughtful, deliberative, slow settlement
    ENERGETIC = "energetic"              # Fast, forward-driving, high momentum


@dataclasses.dataclass
class NarrationSegment:
    """A single sentence or clause directed for speech synthesis."""
    segment_index: int
    raw_text: str
    spoken_text: str
    tone: NarrationTone
    pace: float = 1.0
    pause_after_ms: int = 250
    emphasis_words: List[str] = dataclasses.field(default_factory=list)
    engine_instructions: Optional[str] = None


@dataclasses.dataclass
class DirectedScript:
    """The fully directed narration plan ready for speech rendering."""
    full_text: str
    tone: NarrationTone
    target_engine: str
    pace: float
    segments: List[NarrationSegment]
    phonetic_expansions_applied: int
    unsupported_tags_stripped: int
    engine_instruct: Optional[str] = None


class VoiceDirector:
    """
    Directs script styling, dramatic cadence, phonetic pronunciations,
    and engine compatibility guards.
    """

    # Engines that interpret paralinguistic [tags] natively
    ENGINES_WITH_TAG_SUPPORT: Set[str] = {"chatterbox_turbo", "chatterbox"}

    # Engines that support natural-language style instructions
    ENGINES_WITH_INSTRUCT_SUPPORT: Set[str] = {"qwen_custom_voice", "qwen", "qwen_voice_design"}

    # Baseline phonetic expansions for AI and machine learning engineering terminology
    DEFAULT_LEXICON: Dict[str, str] = {
        r"\bO\(N\^2\)\b": "O of N squared",
        r"\bO\(N\s*log\s*N\)\b": "O of N log N",
        r"\bO\(N\)\b": "O of N",
        r"\b1M\b": "one million",
        r"\b32K\b": "thirty-two thousand",
        r"\b128\s*KB\b": "one hundred and twenty-eight kilobytes",
        r"\b80\s*GB\b": "eighty gigabytes",
        r"\b24\s*GB\b": "twenty-four gigabytes",
        r"\b7\.7\s*GB\b": "seven point seven gigabytes",
        r"\bSRAM\b": "S-RAM",
        r"\bVRAM\b": "V-RAM",
        r"\bTriton\b": "Try-ton",
        r"\bCUDA\b": "Coo-da",
        r"\bHBM2e\b": "H-B-M two-e",
        r"\bFP8\b": "F-P eight",
        r"\bFP16\b": "F-P sixteen",
        r"\bJIT\b": "JIT",
        r"\bSSM\b": "S-S-M",
        r"\bSXM4\b": "S-X-M four",
        r"\btok/s\b": "tokens per second",
        r"\bms\b": "milliseconds",
    }

    # Tone delivery profiles
    TONE_CONFIGS: Dict[NarrationTone, Dict[str, Any]] = {
        NarrationTone.CURIOUS: {
            "pace": 0.96,
            "pause_ms": 320,
            "instruct": "speak with quiet curiosity, leaning into the mystery before resolving it",
            "tag": "[curious]",
        },
        NarrationTone.CONVERSATIONAL: {
            "pace": 1.02,
            "pause_ms": 220,
            "instruct": "speak naturally and warmly, as if explaining an exciting technical breakthrough to a peer",
            "tag": "[narration]",
        },
        NarrationTone.AUTHORITATIVE: {
            "pace": 0.94,
            "pause_ms": 350,
            "instruct": "speak with confident authority, measured cadence, and definitive technical conviction",
            "tag": "[narration]",
        },
        NarrationTone.DRAMATIC: {
            "pace": 0.90,
            "pause_ms": 450,
            "instruct": "speak with cinematic tension, dramatic pauses, and solemn weight",
            "tag": "[dramatic]",
        },
        NarrationTone.ANALYTICAL: {
            "pace": 0.95,
            "pause_ms": 280,
            "instruct": "speak with surgical precision and analytical clarity, articulating numbers distinctly",
            "tag": "[narration]",
        },
        NarrationTone.REFLECTIVE: {
            "pace": 0.88,
            "pause_ms": 400,
            "instruct": "speak thoughtfully and deliberatively, allowing ideas to settle",
            "tag": "[whispering]",
        },
        NarrationTone.ENERGETIC: {
            "pace": 1.08,
            "pause_ms": 180,
            "instruct": "speak with dynamic energy and forward momentum",
            "tag": "[happy]",
        },
    }

    def __init__(self, custom_lexicon: Optional[Dict[str, str]] = None):
        self.lexicon = dict(self.DEFAULT_LEXICON)
        if custom_lexicon:
            self.lexicon.update(custom_lexicon)

    def apply_phonetic_lexicon(self, text: str) -> Tuple[str, int]:
        """Expands technical acronyms and math notation into natural spoken forms."""
        count = 0
        expanded = text
        for pattern, replacement in self.lexicon.items():
            new_text, n = re.subn(pattern, replacement, expanded, flags=re.IGNORECASE)
            if n > 0:
                count += n
                expanded = new_text
        return expanded, count

    def sanitize_for_engine(self, text: str, engine: str) -> Tuple[str, int]:
        """
        Removes paralinguistic [tags] (e.g. [laugh], [sigh], [dramatic])
        if the target engine does not natively support them.
        Prevents Kokoro, Piper, and LuxTTS from reading tags literally.
        """
        engine_lower = (engine or "").lower().replace("voicebox_", "")
        if engine_lower in self.ENGINES_WITH_TAG_SUPPORT:
            # Engine natively parses tags; retain them
            return text, 0

        # Strip all bracketed emotion tags like [laugh], [dramatic], [sigh]
        tag_pattern = r"\[(laugh|cough|chuckle|gasp|sigh|groan|sniff|shush|clear throat|angry|crying|dramatic|fear|happy|narration|sarcastic|surprised|whispering|advertisement|curious)\]"
        cleaned, n = re.subn(tag_pattern, "", text, flags=re.IGNORECASE)
        # Collapse multiple spaces created by removed tags
        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
        return cleaned, n

    def inject_cadence_pauses(self, text: str, tone: NarrationTone) -> str:
        """
        Introduces rhythmic em-dashes (—) and ellipses (...) at major clause
        boundaries to create natural breathing space for neural vocoders.
        """
        # Ensure em-dashes have padding for TTS phonemizers
        paced = text.replace("—", " — ").replace("...", " ... ")
        paced = re.sub(r"\s+—\s+", " — ", paced)
        paced = re.sub(r"\s+\.\.\.\s+", " ... ", paced)
        return paced

    def split_into_speaking_segments(self, text: str) -> List[str]:
        """Splits narrative text into natural sentence or major clause units."""
        # Split on sentence boundaries (. ! ?) and major clause breaks (—)
        raw_sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
        segments = []
        for s in raw_sentences:
            s = s.strip()
            if not s:
                continue
            # If a sentence is very long (> 120 chars) and contains an em-dash, split across the dash
            if len(s) > 120 and " — " in s:
                clauses = s.split(" — ")
                for i, c in enumerate(clauses):
                    c = c.strip()
                    if c:
                        # Append the em-dash pause back to the clause if not final
                        if i < len(clauses) - 1:
                            segments.append(f"{c} —")
                        else:
                            segments.append(c)
            else:
                segments.append(s)
        return segments

    def direct_script(
        self,
        script_text: str,
        target_engine: str = "kokoro",
        tone: NarrationTone = NarrationTone.AUTHORITATIVE,
        custom_pace: Optional[float] = None,
        emphasis_words: Optional[List[str]] = None,
    ) -> DirectedScript:
        """
        Prepares a complete directed script for the target voice engine:
        1. Applies phonetic lexicon expansions.
        2. Injects rhythmic cadence pauses.
        3. Sanitizes unsupported paralinguistic tags.
        4. Configures engine-specific instruction parameters.
        5. Decomposes into structured NarrationSegments.
        """
        tone_cfg = self.TONE_CONFIGS.get(tone, self.TONE_CONFIGS[NarrationTone.AUTHORITATIVE])
        pace = custom_pace if custom_pace is not None else tone_cfg["pace"]

        # Step 1: Phonetics
        phonetic_text, exp_count = self.apply_phonetic_lexicon(script_text)

        # Step 2: Cadence
        cadence_text = self.inject_cadence_pauses(phonetic_text, tone)

        # Step 3: Engine Tag Sanitization
        sanitized_text, stripped_tags = self.sanitize_for_engine(cadence_text, target_engine)

        # Step 4: Engine-specific instruction metadata
        engine_instruct = None
        engine_lower = (target_engine or "").lower().replace("voicebox_", "")
        if engine_lower in self.ENGINES_WITH_INSTRUCT_SUPPORT:
            engine_instruct = tone_cfg.get("instruct")

        # Step 5: Segmentation
        raw_segments = self.split_into_speaking_segments(sanitized_text)
        segments: List[NarrationSegment] = []

        for idx, seg_text in enumerate(raw_segments, start=1):
            segments.append(
                NarrationSegment(
                    segment_index=idx,
                    raw_text=seg_text,
                    spoken_text=seg_text,
                    tone=tone,
                    pace=pace,
                    pause_after_ms=tone_cfg["pause_ms"],
                    emphasis_words=emphasis_words or [],
                    engine_instructions=engine_instruct,
                )
            )

        return DirectedScript(
            full_text=sanitized_text,
            tone=tone,
            target_engine=target_engine,
            pace=pace,
            segments=segments,
            phonetic_expansions_applied=exp_count,
            unsupported_tags_stripped=stripped_tags,
            engine_instruct=engine_instruct,
        )

