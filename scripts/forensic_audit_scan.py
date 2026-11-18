"""
Forensic Codebase Scanner for Phase 4.3.2A Architecture Audit.
Scans all key directories, catalogs modules, entry points, dependencies, and state.
"""
import ast
import os
import sys
from pathlib import Path

ROOT = Path("A:/SUPER.INTELLIGENCEEE")

TARGET_DIRS = [
    "core",
    "research",
    "intelligence",
    "creative",
    "rendering",
    "video",
    "audio",
    "captions",
    "visuals",
    "publishing",
    "tests",
    "external",
    "config",
    "scripts"
]

def analyze_python_file(path: Path):
    try:
        content = path.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
        size_bytes = len(content.encode("utf-8"))
        
        tree = ast.parse(content, filename=str(path))
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                    
        has_main = '__name__ == "__main__"' in content or "__name__ == '__main__'" in content
        
        return {
            "path": str(path.relative_to(ROOT)),
            "lines": line_count,
            "bytes": size_bytes,
            "classes": classes,
            "functions": functions,
            "imports": sorted(list(set(imports))),
            "is_entry_point": has_main,
            "parse_error": None
        }
    except Exception as e:
        return {
            "path": str(path.relative_to(ROOT)),
            "lines": 0,
            "bytes": path.stat().st_size if path.exists() else 0,
            "classes": [],
            "functions": [],
            "imports": [],
            "is_entry_point": False,
            "parse_error": str(e)
        }

def run_scan():
    results = {}
    skip_dirs = {"venv", ".venv", "node_modules", "__pycache__", ".git", "dist", ".hyperframes"}
    
    for d in TARGET_DIRS:
        dp = ROOT / d
        if not dp.exists():
            results[d] = {"exists": False, "files": []}
            continue
        
        files = []
        for p in dp.rglob("*"):
            # Skip if any parent in skip_dirs
            if any(part in skip_dirs for part in p.parts):
                continue
            if p.is_file():
                if p.suffix == ".py":
                    files.append(analyze_python_file(p))
                else:
                    files.append({
                        "path": str(p.relative_to(ROOT)),
                        "lines": None,
                        "bytes": p.stat().st_size,
                        "classes": [],
                        "functions": [],
                        "imports": [],
                        "is_entry_point": False,
                        "parse_error": None
                    })
        results[d] = {"exists": True, "files": files}
    
    # Save audit raw scan
    out_file = ROOT / "reports" / "forensic_scan_raw.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    import json
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"Scan complete. Found {sum(len(v['files']) for v in results.values())} files across {len(TARGET_DIRS)} directories.")
    for d, data in results.items():
        if data["exists"]:
            py_count = sum(1 for f in data["files"] if f["path"].endswith(".py"))
            other_count = len(data["files"]) - py_count
            print(f" - {d}: {py_count} Python files, {other_count} other files")
        else:
            print(f" - {d}: DOES NOT EXIST")

if __name__ == "__main__":
    run_scan()
