"""
Find all references to existing scene models across the codebase.
"""
import ast
from pathlib import Path

ROOT = Path("A:/SUPER.INTELLIGENCEEE")
TARGET_SYMBOLS = {
    "UniversalScene",
    "DynamicScene",
    "StoryArchitecturePlan",
    "VisualArchetype",
    "SceneType",
    "SceneProps",
    "CaptionConfig",
    "ClaimEvidence",
    "EvidenceStatus",
    "AssetRequirement",
    "AudioCue"
}

results = {sym: [] for sym in TARGET_SYMBOLS}
skip_dirs = {"venv", ".venv", "node_modules", "__pycache__", ".git", "dist", ".hyperframes"}

for p in ROOT.rglob("*.py"):
    if any(part in skip_dirs for part in p.parts):
        continue
    try:
        content = p.read_text(encoding="utf-8")
        for sym in TARGET_SYMBOLS:
            if sym in content:
                rel = str(p.relative_to(ROOT))
                results[sym].append(rel)
    except Exception:
        pass

for sym, files in results.items():
    print(f"\nSymbol: {sym} (Found in {len(files)} files)")
    for f in sorted(set(files))[:10]:
        print(f"  - {f}")
    if len(files) > 10:
        print(f"  ... (+{len(files)-10} more)")

