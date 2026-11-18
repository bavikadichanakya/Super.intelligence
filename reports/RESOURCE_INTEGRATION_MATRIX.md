# SUPER.INTELLIGENCEEE — Resource Integration Matrix

**Audit Date:** 2026-11-06  
**Classification Standard:**  
- **`LIVE_VERIFIED`:** Actively executed in local runtime with real outputs, cryptographic validation, or external network verification.
- **`MOCK_VERIFIED`:** Unit or integration tests pass using simulated fixtures, mock responses, or synthetic payloads. Real external execution unverified.
- **`PARTIALLY_IMPLEMENTED`:** Code structures exist and run in fallback mode, but full feature capabilities (e.g. neural models, live auth) are incomplete.
- **`NOT_IMPLEMENTED`:** Component referenced in documentation or design plans but lacking executable code.
- **`BLOCKED`:** Requires external credentials, paid API keys, or unavailable system dependencies.

---

## 1. Complete Resource & Subsystem Classification

| Subsystem / Resource | Classification | Executable Entry Point | Evidence / Artifact | Operational Notes & Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **Piper TTS Engine** | **`LIVE_VERIFIED`** | `audio/piper_engine.py:PiperEngine.synthesize` | `output/verification/sample_raw_30s.wav` | Local ONNX adult male British RP model (`jarvis-high.onnx`, SHA-256 `9791877D...`). 100% offline, zero-budget, 22,050 Hz. |
| **FFmpeg / FFprobe** | **`LIVE_VERIFIED`** | `video/ffmpeg_pipeline.py:FFmpegVideoPipeline.compose_final_reel` | `output/drafts/reel_*_final.mp4` | Windows 11 binaries on PATH. Libass subtitle burning, H.264/AAC muxing, -14.0 LUFS loudnorm. |
| **HyperFrames Runner** | **`LIVE_VERIFIED`** | `video/hyperframes_runner.py:HyperFramesRunner.render_composition` | `output/motion_clips/clip_*.mp4` | 1.25s per motion clip via optimized FFmpeg zoompan. Zero crashes under 8 GB RAM. |
| **Audio Mixer & Mastering** | **`LIVE_VERIFIED`** | `audio/audio_mixer.py:AudioMixer.normalize_loudness` | `output/drafts/reel_*_audio_master.wav` | Dual-pass loudnorm, EBU R128 and mobile online targets (-14 to -16 LUFS), True Peak $\le -0.8$ dBTP, SFX overlays. |
| **Visual QA Subsystem** | **`LIVE_VERIFIED`** | `rendering/visual_qa.py:VisualQASubsystem.run_full_visual_audit` | `output/contact_sheets/*_contact_sheet.png` | Extracts scene frames, validates color histograms, checks for black frames, generates contact sheet. |
| **SQLite Persistence** | **`LIVE_VERIFIED`** | `core/database.py:Database` | `data/super_intelligence.db` | WAL-journaled local database. Tables for topics, scripts, jobs, approvals, task briefs, and analytics. |
| **FastAPI Dashboard** | **`LIVE_VERIFIED`** | `dashboard/app.py:create_app` | `http://127.0.0.1:5000` | 7 core dashboard views (Overview, Research, Scripting, Storyboard, Production, Review, Queue). |
| **Agent-Reach Discovery** | **`PARTIALLY_IMPLEMENTED`** | `research/agent_reach_connector.py:AgentReachConnector` | `tests/test_integrated_skills.py` | Public GitHub search, Reddit scraping, and public web ingestion work. Authenticated social channels (X, Xiaohongshu) unconfigured. |
| **Whisper Audio QA** | **`PARTIALLY_IMPLEMENTED`** | `captions/whisper_qa.py:WhisperQA.verify_audio` | `audio_qa` dict in production reports | Heuristic acoustic analysis (energy, duration, zero-crossing) is live. Neural Faster-Whisper is an optional fallback. |
| **Remotion Motion Library** | **`PARTIALLY_IMPLEMENTED`** | `.agents/skills/remotion-to-hyperframes` | `tests/test_v2_visuals_video.py` | Standalone TS/JS configs and skill guides exist. Python video pipeline emulates Remotion layouts via Pillow/FFmpeg. |
| **Sketch Visual System** | **`PARTIALLY_IMPLEMENTED`** | `sketch-skill/` | `visuals/visual_router.py` | HTML/SVG templates present in `sketch-skill/`. Mapped into UniversalScene archetypes (`sketch_title`, `sketch_stat`, etc.). |
| **Instagram Graph API** | **`MOCK_VERIFIED`** | `publishing/instagram_integration.py:InstagramIntegration` | `tests/test_instagram_unified_login.py` (25/25 pass) | OAuth CSRF HMAC protection, token encryption (Fernet), resumable binary upload tested via mocks. `META_APP_ID` is empty in `.env`. |
| **YouTube Data API v3** | **`MOCK_VERIFIED`** | `publishing/youtube_integration.py:YouTubeIntegration` | `tests/test_integrated_skills.py` | Google OAuth scaffolding and SEO packaging tested. Live channel authentication is unauthenticated (`is_authenticated() == False`). |
| **Telegram Bridge** | **`MOCK_VERIFIED`** | `publishing/telegram_bridge.py:TelegramBridge` | `tests/test_telegram_bridge.py` (3/3 pass) | Bot notification dispatch and approval callback parsing verified via mocks. `TELEGRAM_BOT_TOKEN` is unconfigured. |
| **Live Social Performance Ingestion** | **`NOT_IMPLEMENTED`** | `analytics/performance_tracker.py` | Database `analytics` table | SQLite schema exists, but metrics are only recorded manually via dashboard form; no background API poller exists. |
| **Paid Third-Party AI APIs** | **`BLOCKED`** | External LLM endpoints (OpenAI, Anthropic) | N/A | Excluded by mandatory constraint: ₹0 / $0 operating budget. All processing must remain local-first. |

---

## 2. Dependency Risk Assessment

1. **Zero External Billing Risk:** No module requires a credit card or billed token to execute a complete production run. The entire pipeline from topic discovery to rendered MP4 runs locally.
2. **Platform Credential Gates:** Social publishing to Instagram and YouTube cannot perform live network uploads until the operator configures valid Meta Developer and Google Cloud OAuth credentials in `.env`.
3. **Local Tooling Health:** FFmpeg, FFprobe, and Python 3.11 are verified as operational on the Windows 11 host.

