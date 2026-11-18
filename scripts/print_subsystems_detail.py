import json
from pathlib import Path

raw_file = Path("reports/forensic_scan_raw.json")
with open(raw_file, "r", encoding="utf-8") as f:
    data = json.load(f)

for d in ["creative", "rendering", "video", "audio", "captions", "visuals", "publishing", "tests"]:
    if d not in data or not data[d]["exists"]:
        continue
    py_files = [f for f in data[d]["files"] if f["path"].endswith(".py")]
    print(f"\n### {d} ({len(py_files)} files)")
    for f in sorted(py_files, key=lambda x: x["path"]):
        print(f"  - `{f['path']}` ({f['lines']}L): {', '.join(f['classes'])}")
