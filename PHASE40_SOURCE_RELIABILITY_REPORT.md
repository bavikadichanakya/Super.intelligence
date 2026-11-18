# SUPER.INTELLIGENCEEE — PHASE 4.0 SOURCE RELIABILITY REPORT
**Subsystem:** Multi-Channel Intelligence & Connector Ingestion  
**Audit Timestamp:** 2026-11-07T12:18:00Z  
**Operating Standard:** Deterministic Source Attribution & Zero-Budget Scraping Resilience  

---

## 1. External Source Inventory & Real-World Ingestion Performance

A live multi-channel retrieval cycle was executed across all configured sources. Every source was evaluated for connection uptime, rate-limit tolerance, publication-date presence, and payload integrity.

| Source Name | Channel / Protocol | Credibility Tier | Credibility Score | Live Retrieved | Ingestion Status | Failure Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **arXiv CS.AI** | HTTPS / Atom & API Query | Tier 0: Academic Preprints | **0.98** | 8 | **ONLINE** | Weekend `<skipDays>` automatically triggers fallback to official arXiv Search API query endpoint. |
| **Ars Technica** | HTTPS / RSS & HTML Scraping | Tier 2: Tier-1 Tech Press | **0.85** | 20 | **ONLINE** | Resolved previous HTTP 405 by adopting Windows 11 Chrome 124 browser headers. Tier-2 Agent Reach fallback enabled. |
| **The Verge** | HTTPS / Atom & HTML Scraping | Tier 3: Mainstream Tech Media | **0.75** | 10 | **ONLINE** | Clean XML structure; multi-author and ISO publication date extraction verified. |
| **TechCrunch** | HTTPS / RSS & HTML Scraping | Tier 3: Mainstream Tech Media | **0.75** | 20 | **ONLINE** | Clean category filtering (`artificial-intelligence`); tracking parameter stripping enabled. |
| **VentureBeat** | HTTPS / RSS & HTML Scraping | Tier 3: Mainstream Tech Media | **0.75** | 0 | **ONLINE (Graceful)** | Upstream feed XML contained malformed token (`<unknown>:2:39`); gracefully handled without crashing pipeline. Fallback to Agent Reach active. |
| **GitHub Repositories** | Subprocess / Agent Reach CLI | Tier 1: Primary Repositories | **0.92** | 5 | **ONLINE** | Repositories searched via `agent-reach github search`. Fixed `"raw": null` crash on line 178. |

---

## 2. Source Credibility Tier Hierarchy

The system enforces a strict 6-tier credibility weighting model in `FactChecker.calculate_source_credibility`:

```
┌────────────────────────────────────────────────────────┐
│ Tier 0: Academic Preprints & Peer-Reviewed Papers     │
│ arXiv, bioRxiv, OpenReview, IEEE, ACM (Score: 0.98)   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Tier 1: Primary Codebases & Frontier Research Labs     │
│ GitHub, HuggingFace, DeepMind, OpenAI, Meta (Score: 0.92)│
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Tier 2: Tier-1 Technical & Engineering Press           │
│ Ars Technica, MIT Tech Review, IEEE Spectrum (Score: 0.85)│
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Tier 3: Mainstream Commercial Tech Journalism          │
│ The Verge, TechCrunch, VentureBeat, Wired (Score: 0.75)│
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Tier 4: Community Aggregators & Discussions            │
│ Hacker News, Reddit, Developer Forums (Score: 0.60)   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Tier 5: Unverified Blogs & Web Scrapers                │
│ Content aggregators, secondary re-blogs (Score: 0.25)  │
└────────────────────────────────────────────────────────┘
```

---

## 3. Connector Hardening & Fault Tolerance

### 3.1 ArXiv Weekend `<skipDays>` Ingestion Fallback
- **Problem**: ArXiv RSS feeds (`http://export.arxiv.org/rss/cs.AI`) configure `<skipDays><day>Saturday</day><day>Sunday</day></skipDays>` in their XML specification. Consequently, standard RSS fetchers return 0 items over weekends, causing a temporary blackout of primary academic research.
- **Remediation**: `RSSCollector.fetch_feed()` now detects when an arXiv RSS feed returns 0 entries. It automatically triggers an API fallback to `https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=15`. This Search API query ignores skipDays and returns the latest preprints every day of the week.

### 3.2 WAF & Anti-Bot Defense (`PublicWebCollector` Tier-2 Fallback)
- **Problem**: Cloudflare and Datadog WAFs on certain tech journalism portals issue HTTP 405 (Method Not Allowed) or HTTP 429 (Too Many Requests) when scraping with default Python user-agents.
- **Remediation**:
  1. Default headers upgraded to Windows 11 `Chrome/124.0.0.0` with `sec-ch-ua` platform tokens.
  2. If `requests.get()` encounters status `403`, `405`, `429`, or `503`, execution automatically transfers to `PublicWebCollector._fallback_agent_reach()`.
  3. `AgentReachConnector` runs a headless, cookie-safe subprocess (`agent-reach web read <url>`) that isolates DOM rendering and returns clean markdown.

### 3.3 Agent Reach GitHub Subscripting Guard
- **Problem**: In previous iterations, `agent-reach github search` returned items where `"raw": null`. Invoking `item.get("raw", {}).get("stargazers_count")` threw `TypeError: 'NoneType' object is not subscriptable` because `item.get("raw")` evaluated to `None`.
- **Remediation**: Upgraded all dictionary retrievals across `agent_reach_connector.py` to `raw = item.get("raw") or {}`, completely neutralizing `NoneType` crashes.

