"""
SUPER.INTELLIGENCEEE — Voicebox TTS Provider Adapter
Modular provider adapter connecting SUPER.INTELLIGENCEEE audio pipeline
to the local Voicebox REST API (https://voicebox.sh/).
Supports health checking, preset voice discovery, profile resolution,
synchronous streaming, asynchronous queued generation, cancellation,
and audio output validation.
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("super_intelligence.voicebox_provider")


# Authoritative Production Voice Lock Constants
VOICE_PROVIDER = "voicebox"
TTS_ENGINE = "kokoro"
VOICE_ID = "am_liam"
VOICE_LOCALE = "en-US"
VOICE_ACCENT = "general_american"


class VoiceboxProviderError(Exception):
    """Raised when Voicebox API requests or audio generation fails."""
    pass


class VoiceboxProvider:
    """
    Modular client adapter for Voicebox AI Voice Studio (FastAPI backend)
    with direct Kokoro-82M fallback bridge.
    Default endpoint: http://127.0.0.1:17493
    """

    DEFAULT_API_URL = "http://127.0.0.1:17493"
    DEFAULT_ENGINE = TTS_ENGINE
    DEFAULT_MALE_VOICE = VOICE_ID  # General American Male (Liam) — Locked
    DEFAULT_TIMEOUT_SEC = 120.0

    def __init__(
        self,
        api_url: Optional[str] = None,
        default_engine: Optional[str] = None,
        default_voice: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        config: Optional[Any] = None,
    ):
        self.config = config
        self.api_url = (
            api_url
            or os.environ.get("VOICEBOX_API_URL")
            or self._get_config_val("audio.voicebox.api_url", self.DEFAULT_API_URL)
        ).rstrip("/")

        self.default_engine = (
            default_engine
            or os.environ.get("VOICEBOX_ENGINE")
            or self._get_config_val("audio.voicebox.engine", self.DEFAULT_ENGINE)
        )

        self.default_voice = (
            default_voice
            or os.environ.get("VOICEBOX_VOICE_ID")
            or self._get_config_val("audio.voicebox.voice_id", self.DEFAULT_MALE_VOICE)
        )

        self.timeout_seconds = float(
            timeout_seconds
            or os.environ.get("VOICEBOX_TIMEOUT_SEC")
            or self._get_config_val("audio.voicebox.timeout_sec", self.DEFAULT_TIMEOUT_SEC)
        )

        self._cached_profiles: Dict[str, Dict[str, Any]] = {}

        # Direct in-process / subprocess Kokoro-82M runner
        from audio.providers.kokoro_direct import KokoroDirectRunner
        self.direct_runner = KokoroDirectRunner()

    def _get_config_val(self, key: str, default: Any) -> Any:
        if self.config and hasattr(self.config, "get"):
            try:
                val = self.config.get(key)
                if val is not None:
                    return val
            except Exception:
                pass
        return default

    def _http_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Tuple[int, bytes, Dict[str, str]]:
        """Executes a standard HTTP request to Voicebox API without external dependencies."""
        url = f"{self.api_url}{endpoint}"
        t = timeout or self.timeout_seconds
        headers = {
            "Accept": "application/json, audio/wav, */*",
            "User-Agent": "SUPER.INTELLIGENCEEE-VoiceboxProvider/1.0",
        }

        body_bytes = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            body_bytes = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=t) as resp:
                status_code = resp.status
                resp_headers = dict(resp.headers)
                body = resp.read()
                return status_code, body, resp_headers
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            logger.warning(f"Voicebox HTTP {e.code} on {method} {url}: {err_body}")
            return e.code, err_body.encode("utf-8"), dict(e.headers)
        except Exception as e:
            logger.warning(f"Voicebox connection error on {method} {url}: {e}")
            raise VoiceboxProviderError(f"Failed to connect to Voicebox at {url}: {e}") from e

    # ─── Health & Availability ──────────────────────────────────────────

    def check_health(self) -> Dict[str, Any]:
        """Queries /health endpoint."""
        try:
            status, body, _ = self._http_request("/health", method="GET", timeout=4.0)
            if status == 200:
                data = json.loads(body.decode("utf-8"))
                return {"healthy": data.get("status") == "healthy", "details": data}
            return {"healthy": False, "status_code": status, "error": body.decode("utf-8")}
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def is_available(self) -> bool:
        """Fast boolean check if Voicebox HTTP backend is online or direct Kokoro runner is available."""
        res = self.check_health()
        if res.get("healthy", False):
            return True
        return self.direct_runner.is_available()

    # ─── Profile & Preset Discovery ─────────────────────────────────────

    def list_profiles(self) -> List[Dict[str, Any]]:
        """Retrieves all registered voice profiles."""
        status, body, _ = self._http_request("/profiles", method="GET")
        if status == 200:
            profiles = json.loads(body.decode("utf-8"))
            if isinstance(profiles, list):
                for p in profiles:
                    if "id" in p:
                        self._cached_profiles[p["id"]] = p
                        self._cached_profiles[p.get("name", "")] = p
                return profiles
        return []

    def list_preset_voices(self, engine: str = "kokoro") -> List[Dict[str, Any]]:
        """Retrieves built-in preset voices for the given engine (e.g. kokoro)."""
        status, body, _ = self._http_request(f"/profiles/presets/{engine}", method="GET")
        if status == 200:
            res = json.loads(body.decode("utf-8"))
            return res.get("voices", [])
        return []

    def get_or_create_preset_profile(
        self,
        name: str = "Liam American Male",
        engine: str = "kokoro",
        preset_voice_id: str = "am_liam",
        language: str = "en",
        description: str = "Voice profile managed by SUPER.INTELLIGENCEEE",
    ) -> Dict[str, Any]:
        """Finds existing matching profile or creates a new preset profile."""
        existing = self.list_profiles()
        for p in existing:
            if p.get("name") == name or (
                p.get("preset_engine") == engine and p.get("preset_voice_id") == preset_voice_id
            ):
                return p

        # Create new profile
        payload = {
            "name": name,
            "description": description,
            "language": language,
            "voice_type": "preset",
            "preset_engine": engine,
            "preset_voice_id": preset_voice_id,
            "default_engine": engine,
        }
        status, body, _ = self._http_request("/profiles", method="POST", data=payload)
        if status in (200, 201):
            created = json.loads(body.decode("utf-8"))
            logger.info(f"Created Voicebox profile '{name}' (ID: {created.get('id')})")
            return created
        raise VoiceboxProviderError(f"Failed to create Voicebox profile '{name}': {body.decode('utf-8')}")

    # ─── Speech Synthesis ───────────────────────────────────────────────

    def generate_speech(
        self,
        text: str,
        output_wav_path: Path | str,
        profile_id: Optional[str] = None,
        voice_id: Optional[str] = None,
        engine: Optional[str] = None,
        language: str = "en",
        stream: bool = True,
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Synthesizes speech from text and saves to output_wav_path.
        Supports direct streaming (/generate/stream) or async job queue (/generate).
        Guarantees audio validation before returning.
        """
        out_p = Path(output_wav_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        start_t = time.time()

        if not text or not text.strip():
            return False, {"error": "Empty text provided for synthesis"}

        eng = engine or self.default_engine
        vid = voice_id or self.default_voice

        # Phase 3.5 Hard Validation: Reject legacy British voices in default production
        if vid in ("bm_george", "bm_daniel", "bm_lewis", "bm_fable") and not os.environ.get("ALLOW_LEGACY_BRITISH_ACCENT"):
            raise VoiceboxProviderError(
                f"Voice '{vid}' is rejected: British accent is strictly prohibited in Phase 3.5. "
                "Default narration must use General American English ('am_liam', 'am_adam')."
            )

        # 1. If HTTP backend is healthy, attempt HTTP synthesis
        http_healthy = self.check_health().get("healthy", False)
        if http_healthy:
            # Resolve Profile ID for HTTP backend
            resolved_profile_id = profile_id
            if not resolved_profile_id:
                try:
                    profile = self.get_or_create_preset_profile(
                        name=f"Kokoro {vid}",
                        engine=eng,
                        preset_voice_id=vid,
                        language=language,
                    )
                    resolved_profile_id = profile["id"]
                except Exception as e:
                    logger.warning(f"Voicebox HTTP profile creation failed ({e}); switching to direct Kokoro runner...")
                    http_healthy = False

            if http_healthy and stream:
                try:
                    success, meta = self._generate_via_stream(
                        text=text,
                        profile_id=resolved_profile_id,
                        engine=eng,
                        language=language,
                        output_path=out_p,
                    )
                    if success:
                        meta["execution_time_seconds"] = round(time.time() - start_t, 2)
                        meta["engine"] = f"voicebox_{eng}"
                        meta["voice"] = vid
                        meta["profile_id"] = resolved_profile_id
                        meta["fallback_used"] = False
                        return True, meta
                except Exception as e:
                    logger.warning(f"Voicebox HTTP streaming failed ({e}), attempting queue...")
                    try:
                        success, meta = self._generate_via_queue(
                            text=text,
                            profile_id=resolved_profile_id,
                            engine=eng,
                            language=language,
                            output_path=out_p,
                        )
                        if success:
                            meta["execution_time_seconds"] = round(time.time() - start_t, 2)
                            meta["engine"] = f"voicebox_{eng}"
                            meta["voice"] = vid
                            meta["profile_id"] = resolved_profile_id
                            meta["fallback_used"] = False
                            return True, meta
                    except Exception as e2:
                        logger.warning(f"Voicebox HTTP queue also failed ({e2}); switching to direct Kokoro runner...")

        # 2. Direct Local Kokoro-82M Runner (Guarantees exact Kokoro-82M model and am_liam voice)
        if self.direct_runner.is_available():
            logger.info(f"Synthesizing via direct Kokoro runner with locked voice '{vid}'...")
            ok_dir, meta_dir = self.direct_runner.generate(
                text=text,
                output_wav_path=out_p,
                voice_id=vid,
            )
            if ok_dir:
                return True, meta_dir
            
            # Controlled retry
            logger.warning(f"Direct Kokoro runner failed: {meta_dir.get('error')}. Retrying once...")
            time.sleep(1.0)
            ok_retry, meta_retry = self.direct_runner.generate(
                text=text,
                output_wav_path=out_p,
                voice_id=vid,
            )
            if ok_retry:
                return True, meta_retry
            raise VoiceboxProviderError(f"Kokoro direct synthesis failed after retry: {meta_retry.get('error')}")

        raise VoiceboxProviderError(f"No operational Voicebox or Kokoro provider available for locked voice '{vid}'.")

    def _generate_via_stream(
        self,
        text: str,
        profile_id: str,
        engine: str,
        language: str,
        output_path: Path,
    ) -> Tuple[bool, Dict[str, Any]]:
        """Streams audio bytes directly via POST /generate/stream."""
        payload = {
            "profile_id": profile_id,
            "text": text,
            "language": language,
            "engine": engine,
        }
        status, body, headers = self._http_request(
            "/generate/stream",
            method="POST",
            data=payload,
            timeout=self.timeout_seconds,
        )
        if status != 200 or len(body) < 100:
            raise VoiceboxProviderError(f"Voicebox stream returned status {status}: {body[:200]}")

        with open(output_path, "wb") as f:
            f.write(body)

        validation = self.validate_audio_file(output_path)
        if not validation["valid"]:
            raise VoiceboxProviderError(f"Generated stream audio invalid: {validation.get('error')}")

        return True, validation

    def _generate_via_queue(
        self,
        text: str,
        profile_id: str,
        engine: str,
        language: str,
        output_path: Path,
    ) -> Tuple[bool, Dict[str, Any]]:
        """Submits job via POST /generate, polls /history/{id}, and downloads /audio/{id}."""
        payload = {
            "profile_id": profile_id,
            "text": text,
            "language": language,
            "engine": engine,
        }
        status, body, _ = self._http_request("/generate", method="POST", data=payload)
        if status not in (200, 201):
            raise VoiceboxProviderError(f"Failed to submit generation job: {body.decode('utf-8')}")

        job = json.loads(body.decode("utf-8"))
        job_id = job["id"]

        # Poll for completion (up to timeout_seconds)
        poll_interval = 0.5
        max_attempts = int(self.timeout_seconds / poll_interval)
        for _ in range(max_attempts):
            time.sleep(poll_interval)
            h_status, h_body, _ = self._http_request(f"/history/{job_id}", method="GET")
            if h_status == 200:
                h_data = json.loads(h_body.decode("utf-8"))
                current_status = h_data.get("status")
                if current_status == "completed":
                    # Fetch final audio
                    a_status, a_body, _ = self._http_request(f"/audio/{job_id}", method="GET")
                    if a_status == 200:
                        with open(output_path, "wb") as f:
                            f.write(a_body)
                        val = self.validate_audio_file(output_path)
                        val["job_id"] = job_id
                        return True, val
                    raise VoiceboxProviderError(f"Failed to download audio for job {job_id}")
                elif current_status == "failed":
                    err_msg = h_data.get("error", "Unknown generation failure")
                    raise VoiceboxProviderError(f"Voicebox generation job {job_id} failed: {err_msg}")

        # Cancel on timeout
        self.cancel_generation(job_id)
        raise VoiceboxProviderError(f"Voicebox generation job {job_id} timed out after {self.timeout_seconds}s")

    def cancel_generation(self, generation_id: str) -> bool:
        """Cancels a running or queued generation job."""
        try:
            status, _, _ = self._http_request(f"/generate/{generation_id}/cancel", method="POST")
            return status == 200
        except Exception:
            return False

    # ─── Audio File Validation ──────────────────────────────────────────

    def validate_audio_file(self, file_path: Path | str) -> Dict[str, Any]:
        """Verifies that the generated WAV file is valid, non-empty, and readable."""
        p = Path(file_path)
        if not p.exists() or p.stat().st_size < 1024:
            return {"valid": False, "error": "File does not exist or size < 1KB"}

        try:
            with wave.open(str(p), "rb") as wf:
                channels = wf.getnchannels()
                sample_rate = wf.getframerate()
                frames = wf.getnframes()
                duration = frames / float(sample_rate) if sample_rate > 0 else 0.0

            if duration <= 0.2:
                return {"valid": False, "error": f"Audio duration too short ({duration:.2f}s)"}

            return {
                "valid": True,
                "duration": round(duration, 3),
                "sample_rate": sample_rate,
                "channels": channels,
                "file_size": p.stat().st_size,
            }
        except Exception as e:
            return {"valid": False, "error": f"Invalid WAV header: {e}"}

