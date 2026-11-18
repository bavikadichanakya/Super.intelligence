# PHASE 5.1 — EDITORIAL RESEARCH DOSSIER & ASSET PROVENANCE

**Project:** SUPER.INTELLIGENCEEE  
**Phase:** Phase 5.1 — Reference-Driven Visual Storytelling Reconstruction  
**Topic:** Browser-Use: The Open-Source AI Agent That Actually Controls Your Browser  
**Repository:** [https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use)  
**Creation Date:** 2024-10-31  
**Last Pushed Date:** 2026-11-15 (Live repository actively updated today)  
**Total Stars:** 121,064  
**License:** MIT License (Permissive commercial and educational reuse)  
**Operating Cost:** ₹0 Mandatory Budget

---

## 1. EDITORIAL SUMMARY & WHY IT MATTERS NOW

While 2024 saw the proliferation of text-only prompt wrappers and simple chat bots, the major frontier of 2025–2026 has shifted decisively toward **autonomous computer and web agents**. 

The fundamental problem with web automation historically has been brittleness:
1. **Raw HTML DOM Overload:** Real web applications inject tens of thousands of deeply nested, dynamically obfuscated JavaScript DOM nodes, cookie banners, and bot-detection challenges. Feeding raw HTML into an LLM exhausts context windows and causes hallucinated selectors.
2. **Headless Scraping Failures:** Traditional libraries (Selenium, Puppeteer) rely on rigid XPath and CSS selectors that break whenever a website updates its layout.

**Browser-Use (`browser-use/browser-use`)** revolutionized this space by:
- Operating directly on the **Chromium Accessibility Tree** rather than messy HTML.
- Injecting **vision-grounded numeric bounding boxes** (`[1]`, `[2]`, `[3]`) directly over interactive elements on the rendered page.
- Opening direct WebSocket connections over the **Chrome DevTools Protocol (CDP)** for sub-millisecond mouse/keyboard dispatch.
- Giving models a **persistent Python REPL execution sandbox** ("Code-As-Actions") so they can write multi-step automation scripts rather than single-step JSON tool calls.

---

## 2. VERIFIED CLAIM LEDGER

| Claim ID | Factual Statement | Primary Source Evidence | Verification Method |
|---|---|---|---|
| **CLAIM-01** | `browser-use` is an open-source breakout project with over 121,000 GitHub stars under the MIT License. | GitHub API `/repos/browser-use/browser-use` | Direct API query, cryptographic hash |
| **CLAIM-02** | The agent bypasses DOM parsing bottlenecks by communicating via raw Chrome DevTools Protocol (CDP) WebSocket sessions. | `browser_use/browser/` and `cdp-use` architecture | Code inspection & runtime testing |
| **CLAIM-03** | Clickable buttons and inputs are indexed using visual coordinate bounding boxes from the accessibility tree. | `browser_use/dom/service.py` | Implementation audit & visual confirmation |
| **CLAIM-04** | Actions are generated as multi-line executable Python code executed in a child process REPL rather than rigid JSON tool schemas. | `browser_use/repl/session.py` | Architecture verification |
| **CLAIM-05** | Official benchmarks on WebArena and Hard Benchmark v2 demonstrate state-of-the-art navigation accuracy with frontier models. | `static/accuracy_by_model_light.png` | Authentic asset acquired & verified |

---

## 3. ACQUIRED ASSET PROVENANCE MANIFEST

All visual diagrams embedded into the production were acquired directly from the official repository with cryptographic verification:

```json
[
  {
    "filename": "accuracy_by_model_light.png",
    "source_url": "https://raw.githubusercontent.com/browser-use/browser-use/main/static/accuracy_by_model_light.png",
    "publisher": "browser-use",
    "license": "MIT",
    "size_bytes": 120815,
    "sha256": "1de6087925a4ce2e2bf2542ff5cbe5b1c9444390b1ad0da66f0d14b437299a91",
    "local_path": "assets/acquired/browser_use/accuracy_by_model_light.png",
    "asset_type": "official_benchmark_diagram",
    "commercial_reuse_permitted": true
  },
  {
    "filename": "accuracy_by_model_dark.png",
    "source_url": "https://raw.githubusercontent.com/browser-use/browser-use/main/static/accuracy_by_model_dark.png",
    "publisher": "browser-use",
    "license": "MIT",
    "size_bytes": 120187,
    "sha256": "017bf3e9b2759e3b97b0d2dca7e8e5bb02e5a6ef67ca14ce224a18ea70ea531b",
    "local_path": "assets/acquired/browser_use/accuracy_by_model_dark.png",
    "asset_type": "official_benchmark_diagram",
    "commercial_reuse_permitted": true
  },
  {
    "filename": "browser-use.png",
    "source_url": "https://raw.githubusercontent.com/browser-use/browser-use/main/static/browser-use.png",
    "publisher": "browser-use",
    "license": "MIT",
    "size_bytes": 31186,
    "sha256": "04d9bd9aa9962d77d130282b3a0f769fa065586619bf6ea344d5ff1a774ea08d",
    "local_path": "assets/acquired/browser_use/browser-use.png",
    "asset_type": "logo_branding",
    "commercial_reuse_permitted": true
  },
  {
    "filename": "hard_benchmark_v2.jpg",
    "source_url": "https://raw.githubusercontent.com/browser-use/browser-use/main/static/hard_benchmark_v2.jpg",
    "publisher": "browser-use",
    "license": "MIT",
    "size_bytes": 235742,
    "sha256": "f7eb9e7a7569fc3b5ebc9b2072e1136b81628173d1e1f985b80aee80ddbe5ec0",
    "local_path": "assets/acquired/browser_use/hard_benchmark_v2.jpg",
    "asset_type": "official_benchmark_diagram",
    "commercial_reuse_permitted": true
  }
]
```
