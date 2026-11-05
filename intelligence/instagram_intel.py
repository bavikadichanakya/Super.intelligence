"""
SUPER.INTELLIGENCEEE — Instagram Intelligence & Content Optimization Module
Adapted from instagram-agent-skill (Jake Schincariol, MIT License).
Optimized for Windows 11, local-first execution, and zero paid API dependencies.
"""

from __future__ import annotations

import json
import os
import re
import statistics
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parent / "data"
HOOKS_FILE = DATA_DIR / "instagram_hooks.json"
SLOP_FILE = DATA_DIR / "slop.json"

WORD_RE = re.compile(r"[A-Za-z0-9$%'’-]+")
NUMBER_RE = re.compile(
    r"\$\s?\d[\d,]*(?:\.\d+)?"
    r"|\b\d[\d,]*(?:\.\d+)?\s?"
    r"(?:%|k\b|x\b|hrs?\b|hours?\b|mins?\b|minutes?\b|days?\b|weeks?\b|months?\b|years?\b)?",
    re.IGNORECASE,
)
PROPER_RE = re.compile(r"(?<!^)\b[A-Z][a-z]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)(#[A-Za-z0-9_]+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(
    r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app)/\S*",
    re.IGNORECASE,
)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
CONTRACTIONS_RE = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS_RE = re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE)

SPOKEN_NUMBERS = {
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
    "billion", "dozen", "half", "twice", "triple",
}
MONEY_WORDS = {
    "dollars", "dollar", "bucks", "grand", "percent", "cents",
    "millionaire", "billionaire", "revenue", "profit", "salary", "rent",
}
STAKES = {
    "stop", "never", "wrong", "mistake", "mistakes", "lost", "lose", "losing",
    "cost", "costs", "broke", "broken", "failed", "failure", "fail", "nobody",
    "no", "not", "don't", "dont", "doesn't", "didn't", "can't", "won't",
    "quit", "quitting", "fired", "deleted", "delete", "killed", "kills", "kill",
    "replaced", "replaces", "cut", "beat", "free", "paid", "charged", "hired",
    "saved", "first", "banned", "illegal", "worst", "hate", "hated", "wasted",
    "waste", "scam", "lie", "lied", "lying", "truth", "secret", "hidden",
    "stole", "stolen", "before", "until", "instead", "but", "except", "unless",
    "problem", "risk", "danger", "warning", "regret", "wish", "should",
    "shouldn't", "still", "already", "only", "without", "versus", "vs", "actually",
}
WEAK_OPENERS = [
    "so", "ok", "okay", "hey", "hi", "hello", "guys", "yo", "alright",
    "welcome", "today", "basically", "honestly", "look", "listen", "um",
    "just", "let", "lets", "let's", "i wanted", "i want", "one of",
    "have you", "did you", "do you", "are you", "in this", "in today",
    "the thing", "a lot", "there is", "there are", "this is", "it is",
    "as a", "when it", "if you've", "you know",
]
DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:stop scrolling|don'?t scroll)"),
     "Opens with 'stop scrolling'. Asking for attention proves you have not earned it."),
    (re.compile(r"(?i)^\s*(?:hey guys|hi guys|hello everyone|welcome back)"),
     "Opens with a generic greeting. A viewer decides in 1.5 seconds; do not waste it."),
    (re.compile(r"(?i)^\s*(?:in this video|today i'?m going to)"),
     "Announces the video rather than starting it."),
    (re.compile(r"(?i)#\w+"), "Spoken hook contains a hashtag. Hashtags belong in the caption."),
]
ASKS = [
    (re.compile(r"(?i)\bcomment (?:the word |\")?[A-Z0-9]{2,}\b"), "comment a keyword"),
    (re.compile(r"(?i)\b(?:dm|message) me\b"), "DM me"),
    (re.compile(r"(?i)\bsave (?:this|it)\b"), "save this"),
    (re.compile(r"(?i)\bshare (?:this|it)\b"), "share this"),
    (re.compile(r"(?i)\bfollow (?:me|for)\b"), "follow"),
    (re.compile(r"(?i)\blink in (?:my )?bio\b"), "link in bio"),
    (re.compile(r"(?i)\b(?:swipe|tap) (?:through|left|right|for|to)\b"), "swipe or tap"),
    (re.compile(r"(?i)\btell me\b|\bwhat would you\b|\bwhich one\b"), "answer a question"),
]
FILLER_TAGS = {
    "#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
    "#trending", "#instagood", "#love", "#follow", "#like4like", "#reels",
    "#reelsinstagram", "#viralreels", "#instadaily",
}


def _words(text: str) -> List[str]:
    return WORD_RE.findall(re.sub(r"(?<=\d),(?=\d)", "", text))


def _clamp(n: float) -> float:
    return max(0.0, min(100.0, float(n)))


# ---------------------------------------------------------------------------
# 1. Hook Scoring & Ranking
# ---------------------------------------------------------------------------
def score_instagram_hook(hook: str) -> Dict[str, Any]:
    """
    Evaluates an Instagram spoken hook across 5 core dimensions:
    Brevity, Concreteness, Stakes, Frontloading, Audience + Dealbreakers.
    """
    raw = hook.strip()
    w = _words(raw)
    n_words = len(w)
    lower = raw.lower()

    if n_words == 0:
        return {"score": 0.0, "hook": raw, "dealbreakers": ["Empty hook"], "subscores": {}}

    # Dealbreakers
    dealbreakers = []
    for pat, msg in DEALBREAKERS:
        if pat.search(raw):
            dealbreakers.append(msg)

    # 1. Brevity (Target: < 3.0s speaking time at 165 wpm ≈ <= 8 words)
    est_sec = n_words / 2.75
    if n_words <= 8:
        brevity = 100.0
    elif n_words <= 12:
        brevity = _clamp(100.0 - (n_words - 8) * 12.5)
    elif n_words <= 16:
        brevity = _clamp(50.0 - (n_words - 12) * 10.0)
    else:
        brevity = 10.0

    # 2. Concreteness (Numbers, money, specific proper nouns)
    has_num = bool(NUMBER_RE.search(raw) or (set(w_l.lower() for w_l in w) & SPOKEN_NUMBERS))
    has_money = bool("$" in raw or (set(w_l.lower() for w_l in w) & MONEY_WORDS))
    has_proper = bool(PROPER_RE.search(raw))
    concreteness = 100.0 if (has_money or (has_num and has_proper)) else (75.0 if (has_num or has_proper) else 25.0)

    # 3. Stakes (Words that put something on the line)
    stakes_hits = [word for word in w if word.lower() in STAKES]
    stakes_score = 100.0 if len(stakes_hits) >= 2 else (75.0 if stakes_hits else 20.0)

    # 4. Frontloaded (Does it start immediately or have weak preamble?)
    first_three = " ".join([w_l.lower() for w_l in w[:3]])
    has_weak_opener = any(first_three.startswith(opener) for opener in WEAK_OPENERS)
    frontloaded = 20.0 if has_weak_opener else 90.0

    # 5. Audience (Directed at the viewer: you, your, engineers, designers, etc.)
    has_you = bool(re.search(r"\b(you|your|you're|you've)\b", lower))
    has_audience = has_you or bool(re.search(r"\b(engineers?|developers?|creators?|founders?)\b", lower))
    audience_score = 100.0 if has_audience else 40.0

    # Composite Score
    weights = {"brevity": 0.25, "concreteness": 0.25, "stakes": 0.20, "frontloaded": 0.15, "audience": 0.15}
    raw_score = (
        brevity * weights["brevity"]
        + concreteness * weights["concreteness"]
        + stakes_score * weights["stakes"]
        + frontloaded * weights["frontloaded"]
        + audience_score * weights["audience"]
    )
    if dealbreakers:
        raw_score = min(raw_score, 30.0)

    score = round(_clamp(raw_score), 1)

    return {
        "hook": raw,
        "score": score,
        "estimated_duration_seconds": round(est_sec, 2),
        "word_count": n_words,
        "dealbreakers": dealbreakers,
        "subscores": {
            "brevity": round(brevity, 1),
            "concreteness": round(concreteness, 1),
            "stakes": round(stakes_score, 1),
            "frontloaded": round(frontloaded, 1),
            "audience": round(audience_score, 1),
        },
        "recommendations": [
            d for d in dealbreakers
        ] + ([f"Shorten hook ({n_words} words; aim for <= 9 words)"] if n_words > 9 else [])
          + (["Add a concrete number or dollar figure"] if not (has_num or has_money) else [])
          + (["Inject a stakes/contrast word (e.g., 'stop', 'failed', 'secret', 'replaces')"] if not stakes_hits else []),
    }


def rank_instagram_hooks(hooks: List[str]) -> List[Dict[str, Any]]:
    scored = [score_instagram_hook(h) for h in hooks if h.strip()]
    return sorted(scored, key=lambda x: x["score"], reverse=True)


def get_instagram_hook_formulas() -> List[Dict[str, Any]]:
    if HOOKS_FILE.exists():
        try:
            return json.loads(HOOKS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


# ---------------------------------------------------------------------------
# 2. Spoken Beat Timing Calculator
# ---------------------------------------------------------------------------
def analyze_spoken_beats(
    script_text: str,
    wpm: int = 165,
    target_seconds: Optional[float] = 38.0,
) -> Dict[str, Any]:
    """
    Splits script into spoken beats, computes timecodes, and flags retention killers:
    - Beat 1 duration > 3.0s (hook too long)
    - Any single beat > 4.0s without visual transition
    - Abstract runs (3+ consecutive beats without concrete markers)
    """
    wps = wpm / 60.0
    lines = [l.strip() for l in script_text.splitlines() if l.strip()]
    beats = []

    for line in lines:
        n = len(_words(line))
        if n / wps <= 4.0 * 1.5:
            beats.append(line)
        else:
            # Paragraph split
            parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
            buf = ""
            for part in parts:
                candidate = (buf + " " + part).strip()
                if buf and len(_words(candidate)) / wps > 4.0:
                    beats.append(buf)
                    buf = part
                else:
                    buf = candidate
            if buf:
                beats.append(buf)

    rows = []
    clock = 0.0
    abstract_streak = 0
    flags = []

    for i, text in enumerate(beats):
        n = len(_words(text))
        dur = round(n / wps, 2)
        has_concrete = bool(NUMBER_RE.search(text) or PROPER_RE.search(text))

        if not has_concrete:
            abstract_streak += 1
        else:
            abstract_streak = 0

        beat_flag = None
        if i == 0 and dur > 3.0:
            beat_flag = f"HOOK SLOW ({dur}s > 3.0s window)"
            flags.append(f"Scene 1: Hook exceeds 3s window ({dur}s)")
        elif dur > 4.0:
            beat_flag = f"BEAT LONG ({dur}s > 4.0s)"
            flags.append(f"Scene {i+1}: Beat exceeds 4.0s ({dur}s) without visual cut")
        if abstract_streak >= 3:
            beat_flag = "ABSTRACT RUN (3+ abstract lines)"
            flags.append(f"Scene {i+1}: 3+ consecutive lines without numbers or names")

        rows.append({
            "beat_index": i + 1,
            "start_seconds": round(clock, 2),
            "duration_seconds": dur,
            "word_count": n,
            "text": text,
            "has_concrete": has_concrete,
            "flag": beat_flag,
        })
        clock += dur

    total_duration = round(clock, 2)
    target_delta = round(total_duration - target_seconds, 2) if target_seconds else 0.0

    return {
        "beats": rows,
        "beat_count": len(rows),
        "total_words": sum(r["word_count"] for r in rows),
        "total_duration_seconds": total_duration,
        "wpm": wpm,
        "target_seconds": target_seconds,
        "target_delta_seconds": target_delta,
        "flags": flags,
        "is_pacing_optimal": len(flags) == 0,
    }


# ---------------------------------------------------------------------------
# 3. Caption Linter & Feed Truncation Preview
# ---------------------------------------------------------------------------
def lint_instagram_caption(
    caption_text: str,
    keywords: Optional[List[str]] = None,
    cut: int = 125,
) -> Dict[str, Any]:
    """
    Lints Instagram caption against mobile feed display limits:
    - 125 char cut before '... more'
    - Hard limit 2200 characters
    - Official 5 hashtag cap
    - Unclickable URL check
    - CTA presence check
    """
    clean = caption_text.strip()
    total_chars = len(clean)
    lines = clean.split("\n")
    first_line = lines[0].strip() if lines else ""

    truncated = total_chars > cut
    feed_window = clean if not truncated else clean[:cut]

    tags = HASHTAG_RE.findall(clean)
    tag_count = len(tags)
    filler_tags_found = [t for t in tags if t.lower() in FILLER_TAGS]
    links_found = LINK_RE.findall(clean)
    asks_found = [name for pat, name in ASKS if pat.search(clean)]

    checks = []
    # 1. Length
    checks.append({
        "check": "LENGTH",
        "status": "PASS" if total_chars <= 2200 else "FAIL",
        "detail": f"{total_chars}/2200 characters",
    })
    # 2. First line truncation
    checks.append({
        "check": "FIRST_LINE_HOOK",
        "status": "PASS" if len(first_line) <= cut and not first_line.startswith("#") else "WARN",
        "detail": f"First line is {len(first_line)} chars (feed truncates at {cut})",
    })
    # 3. Hashtag cap (Official recommendation: <= 5)
    checks.append({
        "check": "HASHTAG_LIMIT",
        "status": "PASS" if tag_count <= 5 else "WARN",
        "detail": f"{tag_count}/5 hashtags (Instagram penalizes generic tag stuffing)",
    })
    # 4. Filler tags
    checks.append({
        "check": "FILLER_TAGS",
        "status": "PASS" if not filler_tags_found else "WARN",
        "detail": f"Found generic filler tags: {', '.join(filler_tags_found)}" if filler_tags_found else "None",
    })
    # 5. Non-clickable links
    checks.append({
        "check": "LINKS_IN_CAPTION",
        "status": "PASS" if not links_found else "WARN",
        "detail": "Links in captions are unclickable on Instagram; use 'link in bio' instead" if links_found else "None",
    })
    # 6. Call to Action (Ask)
    checks.append({
        "check": "CALL_TO_ACTION",
        "status": "PASS" if asks_found else "WARN",
        "detail": f"Identified asks: {', '.join(asks_found)}" if asks_found else "Missing clear call to action",
    })

    score = 100
    for c in checks:
        if c["status"] == "FAIL":
            score -= 30
        elif c["status"] == "WARN":
            score -= 10
    score = _clamp(score)

    return {
        "total_chars": total_chars,
        "feed_preview_box": feed_window + ("... more" if truncated else ""),
        "truncated_at_feed": truncated,
        "tag_count": tag_count,
        "hashtags": tags,
        "asks": asks_found,
        "checks": checks,
        "quality_score": score,
        "passed": all(c["status"] != "FAIL" for c in checks),
    }


# ---------------------------------------------------------------------------
# 4. AI Slop & Humanizer Detector
# ---------------------------------------------------------------------------
def _load_slop_lexicon() -> Dict[str, Any]:
    if SLOP_FILE.exists():
        try:
            return json.loads(SLOP_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"words": [], "phrases": []}


def detect_ai_slop(text: str) -> Dict[str, Any]:
    """
    Evaluates whether text exhibits robotic machine-generated signals:
    - Low sentence length variance (burstiness)
    - Low specificity / concrete noun density
    - High frequency of generic AI filler vocabulary ('delve', 'tapestry', 'fast-paced world')
    """
    lex = _load_slop_lexicon()
    s_list = [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]
    w_list = _words(text)
    n_words = len(w_list)

    if n_words < 10:
        return {"human_score": 50.0, "burstiness": 50.0, "specificity": 50.0, "slop_density": 0.0, "slop_hits": []}

    # 1. Burstiness (Sentence Length CV)
    lens = [len(s.split()) for s in s_list]
    mean_len = statistics.mean(lens) if lens else 1.0
    cv = (statistics.pstdev(lens) / mean_len) if len(lens) > 1 and mean_len > 0 else 0.4
    burstiness_score = _clamp((cv - 0.22) / (0.70 - 0.22) * 100)

    # 2. Specificity (Numbers, proper nouns per 100 words)
    concrete_hits = len(NUMBER_RE.findall(text)) + len(set(PROPER_RE.findall(text)))
    density_concrete = (concrete_hits * 100.0) / n_words
    specificity_score = _clamp((density_concrete - 0.5) / (6.0 - 0.5) * 100)

    # 3. Slop Lexicon Density
    slop_hits = []
    for item in lex.get("words", []) + lex.get("phrases", []):
        find_pat = r"\b" + re.escape(item["find"]) + r"\b"
        if re.search(find_pat, text, re.IGNORECASE):
            slop_hits.append(item)

    slop_density = (len(slop_hits) * 100.0) / n_words
    slop_score = _clamp(100.0 - (slop_density / 3.0) * 100.0)

    # 4. Contractions & Voice
    has_contractions = len(CONTRACTIONS_RE.findall(text))
    has_pronouns = len(PRONOUNS_RE.findall(text))
    voice_score = _clamp(((has_contractions + has_pronouns) * 100.0 / n_words) * 15.0)

    composite = (
        burstiness_score * 0.25
        + specificity_score * 0.25
        + slop_score * 0.35
        + voice_score * 0.15
    )

    return {
        "human_score": round(composite, 1),
        "is_human_sounding": composite >= 70.0 and len(slop_hits) == 0,
        "metrics": {
            "burstiness_score": round(burstiness_score, 1),
            "sentence_length_cv": round(cv, 2),
            "specificity_score": round(specificity_score, 1),
            "slop_score": round(slop_score, 1),
            "voice_score": round(voice_score, 1),
        },
        "slop_hits_count": len(slop_hits),
        "slop_hits": [h["find"] for h in slop_hits],
    }


def humanize_text(text: str) -> Tuple[str, List[Dict[str, str]]]:
    """
    Substitutes identified robotic AI buzzwords with conversational, punchy human alternatives.
    """
    lex = _load_slop_lexicon()
    result = text
    applied = []

    for item in lex.get("words", []) + lex.get("phrases", []):
        find = item["find"]
        replace = item.get("replace", "")
        if not replace:
            continue
        pattern = re.compile(r"\b" + re.escape(find) + r"\b", re.IGNORECASE)
        if pattern.search(result):
            result = pattern.sub(replace, result)
            applied.append({"find": find, "replacement": replace})

    return result, applied

