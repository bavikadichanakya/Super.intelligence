"""
SUPER.INTELLIGENCEEE — YouTube Intelligence & Packaging Module
Adapted from youtube-agent-skill (Jake Schincariol, MIT License).
Includes title/thumbnail pairing, hook scoring, retention CSV analysis,
transcript dead-air editing EDL, chapter generation, and SEO packaging.
Strictly local-first, Windows-safe, and zero paid API dependencies.
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parent / "data"
YT_HOOKS_FILE = DATA_DIR / "youtube_hooks.json"

DESKTOP_CUT = 60
MOBILE_CUT = 40
HARD_LIMIT = 100

VAGUE_WORDS = {
    "amazing", "incredible", "insane", "crazy", "huge", "massive", "ultimate",
    "best", "powerful", "secret", "revolutionary", "mindblowing", "epic",
    "perfect", "complete", "everything", "gamechanger", "unbelievable",
}
STOP_WORDS = {
    "the", "a", "an", "of", "for", "to", "in", "on", "and", "or", "is", "are",
    "with", "your", "you", "my", "i", "this", "that", "it", "how", "what", "why",
}
FILLER_ONLY = re.compile(
    r"^[\s,.-]*((um+|uh+|er+|ah+|so|okay|ok|right|yeah|like|anyway|basically|"
    r"actually|you know|i mean|let me see|hold on)[\s,.-]*)+$",
    re.I,
)


def _words(text: str) -> List[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def _clamp(n: float) -> float:
    return max(0.0, min(100.0, float(n)))


# ---------------------------------------------------------------------------
# 1. Title & Thumbnail Pairing Linter
# ---------------------------------------------------------------------------
def check_youtube_title_thumbnail(title: str, thumb_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Lints a YouTube title and thumbnail pairing.
    - Title desktop search cut: ~60 chars
    - Mobile home feed cut: ~40 chars
    - Hard limit: 100 chars
    - Vague buzzword detection
    - Thumbnail repetition penalty (thumbnail must complement title, not repeat it)
    - Shouting all-caps penalty (> 2 words)
    """
    t = title.strip()
    n = len(t)
    issues, good = [], []

    # 1. Length checks
    if n > HARD_LIMIT:
        issues.append(("length", f"{n} chars - YouTube hard limit is {HARD_LIMIT}"))
    elif n > DESKTOP_CUT:
        issues.append(("length", f"{n} chars - desktop search cuts near {DESKTOP_CUT}"))
    else:
        good.append(f"{n} chars, well within {DESKTOP_CUT}-char desktop cut")

    if n > MOBILE_CUT:
        head = t[:MOBILE_CUT].rsplit(" ", 1)[0]
        issues.append(("mobile", f"mobile feed cuts to '{head}...' - ensure subject is preserved"))
    else:
        good.append("fits completely on mobile feed without truncation")

    # 2. Shouting all-caps
    caps = [w for w in t.split() if len(w) > 2 and w.isupper()]
    if len(caps) > 2:
        issues.append(("shouting", f"{len(caps)} all-caps words - maximum 2 for emphasis"))
    elif caps:
        good.append(f"{len(caps)} capitalized word for deliberate emphasis")

    # 3. Vague words
    vague_found = [w for w in _words(t) if w in VAGUE_WORDS]
    if vague_found:
        issues.append(("vague", f"vague buzzwords: {', '.join(sorted(set(vague_found)))} (swap for numbers or concrete names)"))
    else:
        good.append("no vague clickbait buzzwords")

    # 4. Numbers / Concrete figures
    nums = re.findall(r"\d[\d,.]*%?", t)
    if nums:
        good.append(f"carries concrete figure ({', '.join(nums[:3])})")
    else:
        issues.append(("no-number", "lacks numbers, metrics, or proper names"))

    # 5. Open question
    if t.endswith("?"):
        good.append("open question creates curiosity gap")

    # 6. Front-loaded subject
    front = [w for w in _words(t)[:3] if w not in STOP_WORDS]
    if not front:
        issues.append(("front-load", "first three words are filler; move core subject forward"))

    # 7. Thumbnail pairing
    if thumb_text:
        tw = set(_words(t)) - STOP_WORDS
        hw = set(_words(thumb_text)) - STOP_WORDS
        shared = tw & hw
        if shared:
            issues.append(("duplicate", f"thumbnail text repeats title words: {', '.join(sorted(shared))}"))
        else:
            good.append("thumbnail text complements title without repeating words")

        if len(_words(thumb_text)) > 4:
            issues.append(("thumb-length", f"{len(_words(thumb_text))} words on thumbnail (maximum 3-4 at mobile feed size)"))
        else:
            good.append(f"{len(_words(thumb_text))} words on thumbnail (optimal mobile visibility)")

    score = round(_clamp(100 - 14 * len(issues) + 4 * len(good)), 1)

    return {
        "title": t,
        "thumb_text": thumb_text,
        "char_count": n,
        "score": score,
        "is_optimal": score >= 75.0,
        "issues": [{"category": k, "message": m} for k, m in issues],
        "strengths": good,
    }


# ---------------------------------------------------------------------------
# 2. YouTube Hook Scoring
# ---------------------------------------------------------------------------
def score_youtube_hook(hook: str) -> Dict[str, Any]:
    """Scores a YouTube opening hook for 0-5s retention."""
    t = hook.strip()
    words_list = _words(t)
    n = len(words_list)

    if n == 0:
        return {"hook": t, "score": 0.0, "feedback": ["Empty hook"]}

    feedback = []
    # YouTube hooks: optimal 6-14 words, spoken in < 4 seconds
    if n <= 14:
        length_score = 100.0
    elif n <= 20:
        length_score = 65.0
        feedback.append(f"Hook runs slightly long ({n} words); trim under 14 words")
    else:
        length_score = 25.0
        feedback.append(f"Hook is too verbose ({n} words); viewers decide in 3-5 seconds")

    # Check for question / tension
    has_question = t.endswith("?") or bool(re.search(r"\b(why|how|what happens)\b", t.lower()))
    has_concrete = bool(re.search(r"\d", t) or re.search(r"\b[A-Z][a-z]{2,}\b", t))
    has_stakes = bool(re.search(r"\b(failed|mistake|secret|danger|stop|truth|destroyed|replaces)\b", t.lower()))

    score = round(
        _clamp(
            length_score * 0.35
            + (100.0 if has_concrete else 30.0) * 0.25
            + (100.0 if has_stakes else 30.0) * 0.25
            + (100.0 if has_question else 50.0) * 0.15
        ),
        1,
    )

    return {
        "hook": t,
        "score": score,
        "word_count": n,
        "has_concrete": has_concrete,
        "has_stakes": has_stakes,
        "has_question": has_question,
        "feedback": feedback,
    }


# ---------------------------------------------------------------------------
# 3. Audience Retention CSV Analyzer
# ---------------------------------------------------------------------------
def analyze_retention_csv(
    csv_content_or_path: str | Path,
    duration_seconds: Optional[float] = None,
    transcript_srt: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Parses a YouTube Studio audience-retention CSV export and reports:
    - HOOK LEAK: percentage dropped in first 30 seconds
    - CLIFFS: sharp steep drops (where viewers leave)
    - SLIDE: average middle bleed rate
    - VERDICT: healthy, leaking, or severe
    """
    # Load rows
    rows = []
    if isinstance(csv_content_or_path, Path) or (isinstance(csv_content_or_path, str) and os.path.exists(csv_content_or_path)):
        with open(csv_content_or_path, newline="", encoding="utf-8-sig", errors="replace") as fh:
            reader = csv.reader(fh)
            for r in reader:
                nums = []
                for c in r:
                    clean_c = c.strip().replace("%", "").replace(",", "")
                    try:
                        nums.append(float(clean_c))
                    except ValueError:
                        pass
                if len(nums) >= 2:
                    rows.append((nums[0], nums[1]))
    else:
        # String stream
        reader = csv.reader(io.StringIO(str(csv_content_or_path)))
        for r in reader:
            nums = []
            for c in r:
                clean_c = c.strip().replace("%", "").replace(",", "")
                try:
                    nums.append(float(clean_c))
                except ValueError:
                    pass
            if len(nums) >= 2:
                rows.append((nums[0], nums[1]))

    if len(rows) < 8:
        return {
            "ok": False,
            "error": "Could not read at least 8 retention data points from CSV.",
            "points": len(rows),
        }

    xs = [r[0] for r in rows]
    ys = [r[1] for r in rows]
    pct_axis = max(xs) <= 100.5
    dur = duration_seconds

    def at_seconds(x):
        return (x / 100.0 * dur) if (pct_axis and dur) else x

    start = ys[0] if ys[0] else 100.0
    cutoff = 30.0 if not pct_axis else (30.0 / dur * 100 if dur else 10.0)
    hook_end = min((y for x, y in rows if x <= cutoff), default=start)
    hook_leak = round(start - hook_end, 2)

    drops = []
    for i in range(1, len(rows)):
        d = ys[i - 1] - ys[i]
        span = xs[i] - xs[i - 1] or 1.0
        drops.append((d / span, xs[i - 1], xs[i], d))

    drops.sort(reverse=True)
    cliffs = [
        {
            "from_point": round(a1, 2),
            "to_point": round(b1, 2),
            "percentage_lost": round(d, 2),
            "at_seconds": round(at_seconds(a1), 1) if (not pct_axis or dur) else None,
        }
        for _, a1, b1, d in drops[:5]
        if d > 0.8
    ]

    mid = [d for d, x0, _, _ in [(r[0], r[1], r[2], r[3]) for r in drops] if x0 > cutoff]
    slide = round(sum(mid) / len(mid), 3) if mid else 0.0

    verdict = "healthy" if hook_leak < 25.0 else ("leaking" if hook_leak < 40.0 else "severe")

    return {
        "ok": True,
        "points_count": len(rows),
        "start_retention": start,
        "end_retention": ys[-1],
        "hook_leak_percent": hook_leak,
        "verdict": verdict,
        "cliffs": cliffs,
        "slide_per_unit": slide,
        "advice": (
            "Hook is healthy; focus on middle pacing" if verdict == "healthy"
            else "Fix the first 30 seconds before editing the rest of the video"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Transcript Dead-Air & Edit Decision List (EDL)
# ---------------------------------------------------------------------------
def _parse_ts(s: str) -> float:
    s = s.strip().replace(",", ".")
    p = s.split(":")
    if len(p) == 3:
        return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2])
    elif len(p) == 2:
        return int(p[0]) * 60 + float(p[1])
    return float(s)


def _load_transcript_cues(raw: str) -> List[Tuple[float, float, str]]:
    cues = []
    # Check if JSON
    if raw.strip().startswith("{") or raw.strip().startswith("["):
        try:
            d = json.loads(raw)
            segs = d.get("segments", d if isinstance(d, list) else [])
            return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
        except Exception:
            pass

    cur = None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [_parse_ts(m.group(1)), _parse_ts(m.group(2)), []]
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2].append(line.strip())

    return [(a, b, " ".join(t)) for a, b, t in cues if t]


def generate_deadair_edl(transcript_content: str, floor_seconds: float = 0.45) -> Dict[str, Any]:
    """
    Scans a transcript (SRT, VTT, or JSON) for:
    - DEAD: gaps between spoken cues longer than floor
    - FILLER: cues that are purely filler words
    - REPEAT: restarted sentence takes
    Produces an Edit Decision List (EDL) with seconds saved.
    """
    cues = _load_transcript_cues(transcript_content)
    if not cues:
        return {"ok": False, "error": "No cues found in transcript", "cuts": []}

    dur = cues[-1][1]
    cuts = []

    for i, (s, e, t) in enumerate(cues):
        # 1. Filler cues
        if FILLER_ONLY.match(t):
            cuts.append({"kind": "FILLER", "start": s, "end": e, "reason": t.strip()[:48]})

        # 2. Dead air gaps
        if i > 0:
            gap = s - cues[i - 1][1]
            if gap > floor_seconds:
                keep = floor_seconds / 2.0
                cuts.append({
                    "kind": "DEAD",
                    "start": round(cues[i - 1][1] + keep, 3),
                    "end": round(s - keep, 3),
                    "reason": f"{gap:.2f}s pause",
                })

        # 3. Sentence restarts
        if t.strip() and not FILLER_ONLY.match(t):
            j = i - 1
            while j >= 0 and (FILLER_ONLY.match(cues[j][2]) or not cues[j][2].strip()):
                j -= 1
            if j >= 0:
                a1 = _words(cues[j][2])[:5]
                b1 = _words(t)[:5]
                if len(a1) >= 3 and a1 == b1:
                    cuts.append({
                        "kind": "REPEAT",
                        "start": cues[j][0],
                        "end": cues[j][1],
                        "reason": f"restart of '{' '.join(a1)}'",
                    })

    valid_cuts = [c for c in cuts if c["end"] > c["start"]]
    valid_cuts.sort(key=lambda c: c["start"])
    removed_sec = sum(c["end"] - c["start"] for c in valid_cuts)
    final_dur = max(0.0, dur - removed_sec)

    return {
        "ok": True,
        "original_duration_seconds": round(dur, 2),
        "cut_count": len(valid_cuts),
        "removed_seconds": round(removed_sec, 2),
        "projected_duration_seconds": round(final_dur, 2),
        "percent_shorter": round((removed_sec / dur * 100) if dur else 0.0, 1),
        "cuts": valid_cuts,
    }


# ---------------------------------------------------------------------------
# 5. YouTube Chapter Generator
# ---------------------------------------------------------------------------
def _mmss(t: float) -> str:
    t_int = int(t)
    h, m, s = t_int // 3600, (t_int % 3600) // 60, t_int % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def generate_youtube_chapters(
    transcript_or_scenes: str | List[Dict[str, Any]],
    target_chapters: int = 7,
    min_chapter_seconds: float = 10.0,
) -> Dict[str, Any]:
    """
    Generates YouTube chapters enforcing YouTube's official rules:
    - Must start at 00:00
    - At least 3 chapters
    - Each chapter must be >= 10 seconds
    """
    chapters = []

    # Case A: If given list of scene dictionaries
    if isinstance(transcript_or_scenes, list):
        current_time = 0.0
        for i, sc in enumerate(transcript_or_scenes):
            dur = float(sc.get("duration", 10.0))
            label = sc.get("name") or sc.get("headline") or f"Section {i+1}"
            chapters.append({
                "start_seconds": round(current_time, 2),
                "timestamp": _mmss(current_time),
                "title": label,
                "duration_seconds": round(dur, 2),
            })
            current_time += dur
    else:
        # Case B: If given transcript string
        cues = _load_transcript_cues(transcript_or_scenes)
        if len(cues) < 3:
            return {"ok": False, "error": "Insufficient cues for chaptering", "chapters": []}

        dur = cues[-1][1]
        picked = [0.0]
        # Evenly space candidate split points if few gaps
        step = max(min_chapter_seconds, dur / target_chapters)
        pos = step
        while pos < dur - min_chapter_seconds:
            picked.append(pos)
            pos += step

        for i, t in enumerate(picked):
            end_t = picked[i + 1] if i + 1 < len(picked) else dur
            # Find relevant text
            sub_text = " ".join(c[2] for c in cues if c[0] >= t and c[1] <= end_t)
            kw = [w for w in _words(sub_text) if w not in STOP_WORDS]
            draft_title = " ".join(w.capitalize() for w in kw[:3]) or f"Part {i+1}"
            chapters.append({
                "start_seconds": round(t, 2),
                "timestamp": _mmss(t),
                "title": draft_title,
                "duration_seconds": round(end_t - t, 2),
            })

    # Validate official YouTube chapter rules
    valid = (
        len(chapters) >= 3
        and chapters[0]["start_seconds"] == 0.0
        and all(c["duration_seconds"] >= min_chapter_seconds for c in chapters)
    )

    formatted_block = "\n".join([f"{c['timestamp']} {c['title']}" for c in chapters])

    return {
        "ok": True,
        "valid_for_youtube": valid,
        "chapter_count": len(chapters),
        "chapters": chapters,
        "formatted_block": formatted_block,
        "notes": "Ready to paste into YouTube video description." if valid else "Warning: Chapters require 3+ entries, 00:00 start, and 10s minimum each.",
    }


# ---------------------------------------------------------------------------
# 6. SEO Metadata Package Builder
# ---------------------------------------------------------------------------
def build_youtube_seo_package(
    title: str,
    summary: str,
    chapters: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    channel_name: str = "SUPER.INTELLIGENCEEE",
) -> Dict[str, Any]:
    """Builds a complete, optimized YouTube video metadata package."""
    clean_tags = list(dict.fromkeys([t.replace("#", "").strip() for t in (tags or []) if t.strip()]))
    if not clean_tags:
        clean_tags = ["AI", "Artificial Intelligence", "Technology", "Innovation", "Machine Learning"]

    tag_str = ", ".join(clean_tags[:15])

    chapter_block = chapters.get("formatted_block", "") if chapters else ""
    timestamps_text = f"TIMESTAMPS:\n{chapter_block}\n\n" if chapter_block else ""

    description = (
        f"{title}\n\n"
        f"{summary}\n\n"
        f"{timestamps_text}"
        f"Subscribe to {channel_name} for daily next-generation artificial intelligence and deep-tech briefings.\n\n"
        f"TAGS: {tag_str}"
    )

    return {
        "title": title[:100],
        "description": description,
        "tags": clean_tags[:20],
        "category_id": "28",  # Science & Technology
        "privacy_status": "private",  # Safe human-review default
    }
