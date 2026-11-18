# SUPER.INTELLIGENCEEE — PHASE 3.6
# EXTERNAL SOURCE & CONNECTOR INVENTORY

**Author:** Systems Integration Engineer & Software Auditor  
**Date:** 2026-11-07  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Security Notice:** All API keys and environment secrets have been audited; no credentials or private tokens are exposed.

---

## 1. Complete Source Inventory Matrix

| Source / Connector | Category | Protocol / Method | Auth Required | Rate Limits | Observed Latency | Current Status | Primary Error Modes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TechCrunch AI Feed** | Technology News | HTTPS / RSS 2.0 | None (Public) | Standard CDN limits | 0.22 seconds | **OPERATIONAL** | None observed; returns 20 fresh items. |
| **The Verge AI Feed** | Emerging Tech | HTTPS / Atom XML | None (Public) | Cloudflare edge | 0.07 seconds | **OPERATIONAL** | HTML boilerplate in `<summary>` requires stripping. |
| **MIT Tech Review Feed** | Research / In-Depth | HTTPS / RSS 2.0 | None (Public) | Standard CDN limits | 0.33 seconds | **OPERATIONAL** | High-quality summaries; paywalled full articles. |
| **Ars Technica AI Feed** | Deep Systems & Policy | HTTPS / RSS 2.0 | None (Public) | Standard CDN limits | 1.59 seconds | **OPERATIONAL** | RSS feed works; direct page scraping triggers 405. |
| **VentureBeat AI Feed** | Enterprise AI & Agents | HTTPS / RSS 2.0 | None (Public) | Strict rate limiting | 0.49 seconds | **DEGRADED** | Direct page scraping returns HTTP 429 Too Many Requests. |
| **ArXiv CS.AI Feed** | Peer-Reviewed Papers | HTTPS / RSS 2.0 | None (Public) | Standard arXiv limits | 0.09 seconds | **OPERATIONAL (Weekday Only)** | Returns 0 items on weekends due to `<skipDays>` publication policy. |
| **Agent Reach CLI** (`agent-reach`) | Multi-Channel Hub | Local Subprocess (JSON) | None (Cookie-safe) | Platform-specific | 1.2 – 3.8 seconds | **OPERATIONAL** | Crashes with `TypeError` if `raw` metadata field is `None`. |
| **Agent Reach: GitHub** | Open Source Repos | Subprocess / REST | Optional GitHub Token | 60 req/hr unauth | 1.8 seconds | **OPERATIONAL** | Unauthenticated rate limit ceiling. |
| **Agent Reach: Web Reader** | Full Page Markdown | Subprocess / Headless | None | Target domain limits | 2.5 seconds | **OPERATIONAL** | Successfully bypasses 405/403 blocks (tested on Ars Technica). |
| **Agent Reach: YouTube** | Subtitles / Transcripts | Subprocess / yt-dlp | None | IP rate limits | 3.5 seconds | **OPERATIONAL** | Videos without auto/manual captions fail. |
| **PublicWebCollector** | Web Page HTML Parser | Python `requests` + `bs4` | None | None | 0.8 – 2.0 seconds | **FRAGILE** | Blocked by modern WAFs (Cloudflare/Akamai) on 40% of domains. |
| **Pexels Stock Provider** | B-Roll Video Retrieval | HTTPS / REST | `PEXELS_API_KEY` | 200 req/hr | N/A | **MOCK FALLBACK** | API key not provided; falls back to procedural color generator. |
| **Pixabay Stock Provider**| B-Roll Video Retrieval | HTTPS / REST | `PIXABAY_API_KEY`| 5000 req/hr | N/A | **MOCK FALLBACK** | API key not provided; falls back to procedural color generator. |
| **Voicebox Local Daemon** | American TTS Engine | HTTP REST (`127.0.0.1:17493`)| None (Localhost) | Sequential CPU load | 2.0 – 8.0s / stem | **OPERATIONAL** | CPU timeout if request window $< 60\text{s}$ under system load. |
| **SQLite Production Cache**| Local Intelligence Store | SQLite 3 (`WAL` mode) | None (Local file) | Single-writer lock | $< 0.01\text{s}$ | **OPERATIONAL** | Database contains 470 legacy/test records. |

---

## 2. Technical Profile of Core Connectors

### 2.1 RSSCollector (`research/rss_collector.py`)
- **Underlying Engine:** `feedparser` v6.0.11 + standard Python `socket` with 12.0s timeout.
- **Header Fingerprint:** Default feedparser User-Agent.
- **Strengths:** Robust XML, RSS, and Atom parsing; automatic redirect resolution; gzip decompression support.
- **Weaknesses:** Lacks intelligent retry with exponential backoff; does not distinguish between temporary weekend empty feeds (arXiv) and network failures.

### 2.2 PublicWebCollector (`research/public_web_collector.py`)
- **Underlying Engine:** Python `requests` + `BeautifulSoup` (`lxml` parser).
- **Header Fingerprint:** `SUPER.INTELLIGENCEEE-Researcher/2.0 (Open Technology Media; +http://super.intelligenceee.local)`.
- **Failure Vulnerability:** Modern anti-bot headers immediately reject this non-browser user agent with HTTP 403 (Forbidden) or HTTP 405 (Method Not Allowed).
- **Remediation:** Replace with standard browser headers or route article body extraction through `AgentReachConnector.read_web_page()`.

### 2.3 AgentReachConnector (`research/agent_reach_connector.py`)
- **Binary Location:** `C:\Users\bavik\.local\bin\agent-reach.EXE` (Version 1.6.1, installed via `uv`).
- **Policy Boundaries:**
  - Allowed Channels: `youtube`, `github`, `reddit`, `web`, `v2ex`.
  - Permanently Blocked: `instagram`, `facebook`, `twitter`, `xueqiu`, `boss` (strictly enforces zero cookie leakage policy).
- **Observed Bug:**
  Line 178: `raw = item.get("raw", {})`. When `agent-reach` returns an item where `"raw": null`, Python sets `raw = None`. Line 183: `raw.get("stargazers_count")` raises `AttributeError: 'NoneType' object has no attribute 'get'`.
  **Fix Required:** Change to `raw = item.get("raw") or {}`.

---

## 3. Storage & Caching Inventory

- **Active Database:** `A:\SUPER.INTELLIGENCEEE\data\super_intelligence.db`
- **Journalling Mode:** `WAL` (Write-Ahead Logging), `PRAGMA synchronous = NORMAL`.
- **Table Allocation:**
  - `articles`: 470 rows (historical RSS ingest records).
  - `topics`: 472 rows (scored candidate records).
  - `production_jobs`: 43 rows (rendered reel metadata).
  - `publishing_queue`: 20 rows (all in `PENDING_REVIEW` or `DRAFT` status; 0 published).
  - `activity_logs`: 11 rows (orchestrator audit trail).
- **Cache Invalidation:** The current system never expires or prunes `topics` older than 30 days. Old topics remain in SQLite indefinitely, slowing down sorting and causing potential stale topic resurfacing.

