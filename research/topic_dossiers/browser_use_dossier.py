"""
SUPER.INTELLIGENCEEE — Phase 5.1 Research Dossier: Browser-Use
Authentic, live-retrieved dossier for 'browser-use/browser-use'.
Primary Sources:
- Official GitHub Repository: https://github.com/browser-use/browser-use
- Repository Metadata: 121,064 Stars, MIT License, Python
- Official Documentation & Architecture: https://docs.browser-use.com
- Acquired Benchmark Artifacts: assets/acquired/browser_use/media_provenance_manifest.json
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class BrowserUseClaim:
    claim_id: str
    statement: str
    source_reference: str
    verified: bool = True


@dataclass
class BrowserUseDossier:
    topic_id: str = "browser_use_agent"
    title: str = "Browser-Use: The Open-Source AI Agent That Actually Controls Your Browser"
    category: str = "Autonomous Web Agents & LLM Tool Use"
    primary_source: str = "https://github.com/browser-use/browser-use"
    publication_date: str = "2024-10-31"
    last_pushed_date: str = "2026-11-15"
    stars_count: int = 121064
    license: str = "MIT License"
    language: str = "Python"
    summary: str = (
        "Browser-Use is an open-source Python library that connects LLMs to Chromium "
        "via the Chrome DevTools Protocol (CDP). Unlike brittle scrapers that parse raw HTML, "
        "it extracts an interactive accessibility tree, tags clickable elements with bounding boxes, "
        "and executes multi-step Python code in a persistent REPL."
    )
    claims: List[BrowserUseClaim] = field(default_factory=lambda: [
        BrowserUseClaim(
            claim_id="claim_01_stars",
            statement="Browser-Use has achieved over 121,000 GitHub stars as a breakout open-source AI project.",
            source_reference="GitHub API /repos/browser-use/browser-use"
        ),
        BrowserUseClaim(
            claim_id="claim_02_cdp",
            statement="The agent communicates directly with Chrome via raw Chrome DevTools Protocol (CDP) WebSocket sessions.",
            source_reference="browser_use/browser/ and cdp-use integration"
        ),
        BrowserUseClaim(
            claim_id="claim_03_bounding_boxes",
            statement="Interactive web elements are grounded using vision bounding boxes and DOM accessibility coordinate trees rather than raw HTML dumps.",
            source_reference="browser_use/dom/service.py"
        ),
        BrowserUseClaim(
            claim_id="claim_04_repl_actions",
            statement="Actions are executed as executable Python code blocks in a persistent child REPL worker rather than rigid single-step JSON tool calls.",
            source_reference="browser_use/repl/session.py"
        ),
        BrowserUseClaim(
            claim_id="claim_05_benchmarks",
            statement="Evaluated on WebArena and Hard Benchmark v2, achieving state-of-the-art navigation accuracy with frontier models.",
            source_reference="static/accuracy_by_model_light.png"
        ),
    ])
    acquired_assets: List[Dict[str, Any]] = field(default_factory=lambda: [
        {
            "filename": "accuracy_by_model_light.png",
            "path": "assets/acquired/browser_use/accuracy_by_model_light.png",
            "sha256": "1de6087925a4ce2e2bf2542ff5cbe5b1c9444390b1ad0da66f0d14b437299a91",
            "type": "official_benchmark_diagram"
        },
        {
            "filename": "browser-use.png",
            "path": "assets/acquired/browser_use/browser-use.png",
            "sha256": "04d9bd9aa9962d77d130282b3a0f769fa065586619bf6ea344d5ff1a774ea08d",
            "type": "logo_branding"
        }
    ])


def get_browser_use_dossier() -> BrowserUseDossier:
    return BrowserUseDossier()
