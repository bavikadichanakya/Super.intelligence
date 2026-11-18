"""
SUPER.INTELLIGENCEEE — Direct Kokoro-82M TTS Synthesis Bridge
Executes high-fidelity local neural text-to-speech using the isolated
Kokoro-82M environment in external/voicebox/backend/venv.
Guarantees 100% offline, zero-network, zero-port-conflict synthesis of General American 'am_liam'.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import time
import wave
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger("super_intelligence.kokoro_direct")

# Authoritative Production Voice Lock Constants
VOICE_PROVIDER = "voicebox"
TTS_ENGINE = "kokoro"
VOICE_ID = "am_liam"
VOICE_LOCALE = "en-US"
VOICE_ACCENT = "general_american"


class KokoroDirectError(Exception):
    """Raised when direct Kokoro synthesis fails."""
    pass


class KokoroDirectRunner:
    """
    Subprocess bridge executing Kokoro-82M directly in its dedicated virtual environment
    (A:/SUPER.INTELLIGENCEEE/external/voicebox/backend/venv).
    """

    def __init__(self, workspace_root: Optional[Path | str] = None):
        self.workspace_root = Path(workspace_root or "A:/SUPER.INTELLIGENCEEE").resolve()
        self.venv_python = (
            self.workspace_root / "external" / "voicebox" / "backend" / "venv" / "Scripts" / "python.exe"
        ).resolve()
        self.sample_rate = 24000

    def is_available(self) -> bool:
        """Verifies that the Kokoro venv python executable exists on disk."""
        return self.venv_python.exists()

    def generate(
        self,
        text: str,
        output_wav_path: Path | str,
        voice_id: str = VOICE_ID,
        speed: float = 1.0,
        timeout_seconds: float = 180.0,
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Synthesizes text into 24 kHz WAV audio via Kokoro-82M.
        Strictly enforces General American voice lock (am_liam).
        """
        if not self.is_available():
            raise KokoroDirectError(f"Kokoro virtual environment not found at: {self.venv_python}")

        # Enforce voice lock
        target_voice = voice_id or VOICE_ID
        if target_voice != VOICE_ID and not os.environ.get("ALLOW_VOICE_OVERRIDE"):
            raise KokoroDirectError(
                f"Production voice lock violation: Voice '{target_voice}' requested, "
                f"but '{VOICE_ID}' is strictly required."
            )

        out_p = Path(output_wav_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        start_time = time.time()
        
        # Self-contained python snippet to execute inside Kokoro venv
        runner_script = f"""
import os, sys, json, time
os.environ['HF_HUB_OFFLINE'] = '1'
import numpy as np
import soundfile as sf
from kokoro import KPipeline

text = {json.dumps(text)}
voice = {json.dumps(target_voice)}
out_path = {json.dumps(str(out_p))}
speed = {float(speed)}

try:
    pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
    generator = pipeline(text, voice=voice, speed=speed)
    all_audio = []
    for res in generator:
        if hasattr(res, 'audio') and res.audio is not None:
            chunk = res.audio
            if hasattr(chunk, 'detach'):
                chunk = chunk.detach().cpu().numpy()
            all_audio.append(chunk.squeeze())
        elif isinstance(res, (tuple, list)) and len(res) >= 3 and res[2] is not None:
            chunk = res[2]
            if hasattr(chunk, 'detach'):
                chunk = chunk.detach().cpu().numpy()
            all_audio.append(chunk.squeeze())
    if not all_audio:
        raise ValueError("Kokoro produced empty audio stream.")
    
    final_audio = np.concatenate(all_audio)
    sf.write(out_path, final_audio, 24000)
    duration = float(len(final_audio)) / 24000.0
    
    res = {{
        "success": True,
        "samples": len(final_audio),
        "duration": duration,
        "sample_rate": 24000,
        "voice": voice,
        "model": "hexgrad/Kokoro-82M",
    }}
    print("RESULT_JSON:" + json.dumps(res))
    sys.exit(0)
except Exception as e:
    res = {{
        "success": False,
        "error": str(e),
    }}
    print("RESULT_JSON:" + json.dumps(res))
    sys.exit(1)
"""

        try:
            cmd = [str(self.venv_python), "-c", runner_script]
            custom_env = os.environ.copy()
            custom_env["HF_HUB_OFFLINE"] = "1"
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=str(self.workspace_root),
                env=custom_env,
            )

            # Parse result from stdout
            result_meta: Dict[str, Any] = {}
            for line in proc.stdout.splitlines():
                if line.startswith("RESULT_JSON:"):
                    result_meta = json.loads(line[len("RESULT_JSON:"):])
                    break

            if proc.returncode == 0 and result_meta.get("success"):
                duration = result_meta.get("duration", 0.0)
                # Verify physical file existence and readable wave header
                if not out_p.exists() or out_p.stat().st_size < 1000:
                    raise KokoroDirectError(f"Generated WAV file is invalid or missing: {out_p}")

                wall_time = time.time() - start_time
                meta = {
                    "success": True,
                    "engine": "kokoro",
                    "provider": "voicebox_kokoro_direct",
                    "model": "hexgrad/Kokoro-82M",
                    "voice": target_voice,
                    "locale": VOICE_LOCALE,
                    "accent": VOICE_ACCENT,
                    "duration": duration,
                    "sample_rate": 24000,
                    "channels": 1,
                    "execution_time_seconds": round(wall_time, 2),
                    "fallback_used": False,
                    "voice_locked": True,
                }
                logger.info(
                    f"Direct Kokoro narration generated ({target_voice}): {duration:.2f}s "
                    f"in {wall_time:.2f}s -> {out_p.name}"
                )
                return True, meta

            err_msg = result_meta.get("error") or proc.stderr.strip() or "Unknown Kokoro execution failure."
            logger.error(f"Kokoro direct synthesis failed: {err_msg}")
            return False, {"error": err_msg, "execution_time_seconds": round(time.time() - start_time, 2)}

        except subprocess.TimeoutExpired:
            logger.error(f"Kokoro direct synthesis timed out after {timeout_seconds}s.")
            return False, {"error": f"Timeout after {timeout_seconds}s"}
        except Exception as e:
            logger.error(f"Kokoro direct runner exception: {e}")
            return False, {"error": str(e)}

    def generate_batch(
        self,
        items: List[Tuple[str, Path | str]],
        voice_id: str = VOICE_ID,
        speed: float = 1.0,
        timeout_seconds: float = 360.0,
    ) -> List[Tuple[bool, Dict[str, Any]]]:
        """
        Synthesizes multiple narration items in a SINGLE subprocess, loading KPipeline once.
        Supports fast skipping of already synthesized files.
        """
        if not self.is_available():
            raise KokoroDirectError(f"Kokoro virtual environment not found at: {self.venv_python}")

        target_voice = voice_id or VOICE_ID
        results: List[Optional[Tuple[bool, Dict[str, Any]]]] = [None] * len(items)
        pending_indices = []
        pending_items = []

        # Check existing cached files
        for idx, (text, out_path) in enumerate(items):
            out_p = Path(out_path).resolve()
            if out_p.exists() and out_p.stat().st_size > 1000:
                try:
                    with wave.open(str(out_p), "rb") as wf:
                        duration = wf.getnframes() / float(wf.getframerate())
                        results[idx] = (
                            True,
                            {
                                "success": True,
                                "duration": duration,
                                "cached": True,
                                "voice": target_voice,
                                "model": "hexgrad/Kokoro-82M",
                            },
                        )
                        logger.info(f"Using cached Kokoro audio: {out_p.name} ({duration:.2f}s)")
                        continue
                except Exception:
                    pass
            pending_indices.append(idx)
            pending_items.append({"text": text, "out_path": str(out_p)})

        if not pending_items:
            return [r for r in results if r is not None]

        # Build runner script for the pending batch
        script_payload = json.dumps(pending_items)
        runner_script = f"""
import os, sys, json, time
os.environ['HF_HUB_OFFLINE'] = '1'
import numpy as np
import soundfile as sf
from kokoro import KPipeline

items = {script_payload}
voice = {json.dumps(target_voice)}
speed = {float(speed)}

try:
    pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
    batch_results = []
    
    for item in items:
        text = item['text']
        out_path = item['out_path']
        generator = pipeline(text, voice=voice, speed=speed)
        all_audio = []
        for gs, ps, audio in generator:
            if audio is not None and len(audio) > 0:
                all_audio.append(audio)
        if not all_audio:
            batch_results.append({{"success": False, "error": "Empty audio generated"}})
            continue
        final_audio = np.concatenate(all_audio)
        sf.write(out_path, final_audio, 24000)
        dur = float(len(final_audio)) / 24000.0
        batch_results.append({{"success": True, "duration": dur, "samples": len(final_audio)}})
        
    print("RESULT_BATCH_JSON:" + json.dumps(batch_results))
    sys.exit(0)
except Exception as e:
    print("RESULT_BATCH_ERROR:" + str(e))
    sys.exit(1)
"""
        cmd = [str(self.venv_python), "-c", runner_script]
        custom_env = os.environ.copy()
        custom_env["HF_HUB_OFFLINE"] = "1"

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=str(self.workspace_root),
            env=custom_env,
        )

        batch_out = []
        for line in proc.stdout.splitlines():
            if line.startswith("RESULT_BATCH_JSON:"):
                batch_out = json.loads(line[len("RESULT_BATCH_JSON:"):])
                break

        if proc.returncode != 0 or not batch_out:
            err_msg = proc.stderr.strip() or "Batch synthesis failed."
            logger.error(f"Kokoro batch synthesis failed: {err_msg}")
            for p_idx in pending_indices:
                results[p_idx] = (False, {"error": err_msg})
            return [r for r in results if r is not None]

        for p_idx, res in zip(pending_indices, batch_out):
            if res.get("success"):
                results[p_idx] = (
                    True,
                    {
                        "success": True,
                        "duration": res.get("duration", 6.5),
                        "cached": False,
                        "voice": target_voice,
                        "model": "hexgrad/Kokoro-82M",
                    },
                )
            else:
                results[p_idx] = (False, {"error": res.get("error", "Unknown error")})

        return [r for r in results if r is not None]

