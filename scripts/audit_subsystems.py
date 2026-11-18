"""
Detailed module inspection and classification script for Phase 4.3.2A Forensic Audit.
"""
import json
from pathlib import Path

raw_file = Path("reports/forensic_scan_raw.json")
with open(raw_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 80)
print("SUPER.INTELLIGENCEEE — SUBSYSTEM FORENSIC BREAKDOWN")
print("=" * 80)

for d, info in data.items():
    if not info["exists"]:
        continue
    py_files = [f for f in info["files"] if f["path"].endswith(".py")]
    print(f"\n### DIRECTORY: {d} ({len(py_files)} Python files)")
    for f in sorted(py_files, key=lambda x: x["path"]):
        p = f["path"]
        lines = f["lines"]
        classes = ", ".join(f["classes"][:5])
        if len(f["classes"]) > 5:
            classes += f" (+{len(f['classes'])-5} more)"
        is_entry = " [ENTRY POINT]" if f["is_entry_point"] else ""
        print(f"  - `{p}` ({lines} lines){is_entry}")
        if classes:
            print(f"      Classes: {classes}")
