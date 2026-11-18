"""
SUPER.INTELLIGENCEEE — Phase 4.0 Live Topic Discovery & Research Verification Cycle
Executes a live harvest across multi-channel sources, runs publication date normalization,
URL & semantic deduplication, 100-point opportunity scoring with fatigue penalties,
and compiles evidence-grounded research dossiers with claim verification.
Records precise Part 8 metrics.
"""

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psutil

from core.database import Database
from core.schemas import EvidenceStatus
from research.deduplicator import Deduplicator
from research.fact_checking import FactChecker
from research.public_web_collector import PublicWebCollector
from research.research_analyst import ResearchAnalyst
from research.rss_collector import RSSCollector
from research.source_extractor import SourceExtractor
from research.topic_scorer import TopicScorer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Phase40Discovery")


def run_discovery_cycle():
    start_time = time.time()
    process = psutil.Process()
    ram_start_mb = process.memory_info().rss / (1024 * 1024)

    db = Database()
    collector = RSSCollector(db=db)
    analyst = ResearchAnalyst(db=db)

    # 1. Configured sources for live intelligence retrieval
    sources = [
        {
            "name": "arXiv CS.AI (Search API)",
            "url": "https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=8",
            "publisher": "arXiv.org",
            "category": "Artificial Intelligence Research",
            "weight": 1.0,
        },
        {
            "name": "Ars Technica AI",
            "url": "https://feeds.arstechnica.com/arstechnica/features",
            "publisher": "Ars Technica",
            "category": "Technology Analysis",
            "weight": 0.9,
        },
        {
            "name": "The Verge Tech",
            "url": "https://www.theverge.com/rss/index.xml",
            "publisher": "The Verge",
            "category": "Technology News",
            "weight": 0.8,
        },
        {
            "name": "TechCrunch AI",
            "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
            "publisher": "TechCrunch",
            "category": "Technology Industry",
            "weight": 0.8,
        },
        {
            "name": "VentureBeat AI",
            "url": "https://venturebeat.com/category/ai/feed/",
            "publisher": "VentureBeat",
            "category": "Enterprise AI",
            "weight": 0.8,
        },
    ]

    logger.info(f"Initiating live retrieval across {len(sources)} sources...")
    all_raw_candidates = []
    source_stats = {}

    for s_cfg in sources:
        name = s_cfg["name"]
        try:
            items = collector.fetch_feed(s_cfg)
            source_stats[name] = {"retrieved": len(items), "status": "ONLINE"}
            all_raw_candidates.extend(items)
        except Exception as e:
            logger.error(f"Failed to fetch {name}: {e}")
            source_stats[name] = {"retrieved": 0, "status": f"ERROR: {e}"}

    # Also search GitHub trending AI repos via Agent Reach
    try:
        from research.agent_reach_connector import AgentReachConnector
        arc = AgentReachConnector(db=db)
        if arc.is_available():
            gh_items = arc.search_github("llm inference", limit=5)
            source_stats["GitHub Repos (Agent Reach)"] = {"retrieved": len(gh_items), "status": "ONLINE"}
            for g in gh_items:
                all_raw_candidates.append({
                    "title": g.get("title", ""),
                    "url": g.get("url", ""),
                    "publisher": "GitHub",
                    "summary": g.get("description", ""),
                    "category": "Open Source Codebases",
                    "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "retrieval_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "status": "DISCOVERED",
                    "score": 0.0,
                    "weight": 1.0,
                })
        else:
            source_stats["GitHub Repos (Agent Reach)"] = {"retrieved": 0, "status": "UNAVAILABLE"}
    except Exception as e:
        logger.warning(f"GitHub retrieval failed: {e}")
        source_stats["GitHub Repos (Agent Reach)"] = {"retrieved": 0, "status": f"ERROR: {e}"}

    total_sources_retrieved = len(all_raw_candidates)
    logger.info(f"Raw articles harvested: {total_sources_retrieved}")

    # 2. Deduplication against historical database and intra-batch
    existing_articles = db.get_articles(limit=500)
    unique_candidates, dup_records = Deduplicator.filter_duplicates_with_report(
        all_raw_candidates, existing_articles, threshold=0.60
    )
    duplicates_removed_count = len(dup_records)
    genuine_candidates_count = len(unique_candidates)
    logger.info(f"Deduplication: {duplicates_removed_count} duplicates removed. {genuine_candidates_count} unique candidates identified.")

    # 3. 100-Point Scoring & Fatigue Penalties
    recent_productions = [
        "Speculative Decoding in Production: Accelerating LLM Serving",
        "State Space Models vs Attention: The Inference Scaling Frontier",
        "Whisper Transcription Pipeline: Sub-Second Audio Intelligence",
    ]

    scored_candidates = []
    for c in unique_candidates:
        breakdown = TopicScorer.score_100_points(
            c,
            existing_topics=existing_articles,
            recent_production_topics=recent_productions,
        )
        c_copy = dict(c)
        c_copy["score"] = breakdown.total_score
        c_copy["score_breakdown"] = breakdown.to_dict()
        scored_candidates.append(c_copy)

    # Sort descending by score
    scored_candidates.sort(key=lambda x: x["score"], reverse=True)

    # 4. In-Depth Research & Dossier Compilation on Top Candidates
    top_candidates = scored_candidates[:5]
    dossiers = []
    total_claims_extracted = 0
    total_claims_verified = 0
    total_claims_source_reported = 0
    total_claims_contradicted = 0
    total_claims_unverified = 0

    for top in top_candidates:
        dossier = analyst.build_dossier(
            top,
            supporting_topics=[c for c in scored_candidates if c != top],
            recent_production_topics=recent_productions,
        )
        dossiers.append(dossier)

        for claim in dossier.important_claims:
            total_claims_extracted += 1
            if claim.status == EvidenceStatus.VERIFIED:
                total_claims_verified += 1
            elif claim.status == EvidenceStatus.SOURCE_REPORTED:
                total_claims_source_reported += 1
            elif claim.status == EvidenceStatus.CONTRADICTED:
                total_claims_contradicted += 1
            elif claim.status in (EvidenceStatus.UNVERIFIED, EvidenceStatus.RESEARCH_BLOCKED):
                total_claims_unverified += 1

    ram_end_mb = process.memory_info().rss / (1024 * 1024)
    elapsed_sec = time.time() - start_time

    results = {
        "cycle_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "elapsed_seconds": round(elapsed_sec, 2),
        "ram_start_mb": round(ram_start_mb, 2),
        "ram_end_mb": round(ram_end_mb, 2),
        "ram_delta_mb": round(ram_end_mb - ram_start_mb, 2),
        "metrics": {
            "sources_retrieved_count": total_sources_retrieved,
            "genuine_candidates_discovered_count": genuine_candidates_count,
            "duplicates_removed_count": duplicates_removed_count,
            "claims_extracted_count": total_claims_extracted,
            "claims_independently_corroborated_count": total_claims_verified,
            "claims_source_reported_count": total_claims_source_reported,
            "claims_contradicted_count": total_claims_contradicted,
            "claims_unverified_count": total_claims_unverified,
        },
        "source_inventory": source_stats,
        "duplicates_sample": dup_records[:10],
        "top_ranked_candidates": [
            {
                "title": c["title"],
                "url": c["url"],
                "publisher": c["publisher"],
                "published_date": c["published_date"],
                "score": c["score"],
                "decision": c["score_breakdown"]["decision"],
                "fatigue_penalty": c["score_breakdown"]["fatigue_penalty"],
                "reasoning": c["score_breakdown"]["reasoning"],
            }
            for c in scored_candidates[:10]
        ],
        "dossiers_summary": [
            {
                "topic_id": d.topic_id,
                "title": d.topic_title,
                "verification_status": d.verification_status,
                "claims_count": len(d.important_claims),
                "selection_rationale": d.selection_rationale,
                "provenance": d.dossier_provenance,
                "claims": [c.to_dict() for c in d.important_claims],
            }
            for d in dossiers
        ],
    }

    out_file = Path("scratch/phase40_discovery_results.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Discovery cycle complete! Results written to {out_file}")
    logger.info(f"METRICS: Retrieved: {total_sources_retrieved}, Genuine: {genuine_candidates_count}, Dups: {duplicates_removed_count}")
    logger.info(f"CLAIMS: Extracted: {total_claims_extracted}, Verified/Corroborated: {total_claims_verified}, Source-Reported: {total_claims_source_reported}, Contradicted: {total_claims_contradicted}, Unverified: {total_claims_unverified}")
    logger.info(f"RAM: {ram_end_mb:.2f} MB (Delta: {ram_end_mb - ram_start_mb:+.2f} MB)")

    return results


if __name__ == "__main__":
    run_discovery_cycle()

