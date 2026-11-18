import json
import subprocess
from pathlib import Path

ffmpeg_pkg = Path("external/motion-canvas/node_modules/@motion-canvas/ffmpeg/package.json")
if ffmpeg_pkg.exists():
    with open(ffmpeg_pkg, "r", encoding="utf-8") as f:
        data = json.load(f)
        print("FFMPEG PKG:", data.get("name"), data.get("version"), data.get("bin"), data.get("main"))

core_pkg = Path("external/motion-canvas/node_modules/@motion-canvas/core/package.json")
if core_pkg.exists():
    with open(core_pkg, "r", encoding="utf-8") as f:
        data = json.load(f)
        print("CORE PKG:", data.get("name"), data.get("version"), data.get("bin"), data.get("main"))

vite_pkg = Path("external/motion-canvas/node_modules/@motion-canvas/vite-plugin/package.json")
if vite_pkg.exists():
    with open(vite_pkg, "r", encoding="utf-8") as f:
        data = json.load(f)
        print("VITE PKG:", data.get("name"), data.get("version"), data.get("bin"), data.get("main"))

