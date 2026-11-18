"""
SUPER.INTELLIGENCEEE — Phase 4.0 Intelligence Hardening Test Suite
Verifies:
1. Live source retrieval (arXiv search API fallback & RSS)
2. Publication date validation & ISO 8601 normalization
3. Qualitative architectural claim extraction
4. Quantitative benchmark claim extraction
5. Claim-evidence grounding & passage matching
6. Contradictory source detection & CONTRADICTED status assignment
7. Semantic topic deduplication & fatigue scoring
8. Freshness scoring based on publication date
9. Dossier provenance & explainable selection rationale
10. Source outage / rate limit handling & RESEARCH_BLOCKED failure state
"""

import datetime
from datetime import timezone
import pytest

from core.database import Database
from core.schemas import ClaimEvidence, EvidenceStatus, ResearchDossier, Source
from research.deduplicator import Deduplicator
from research.fact_checking import FactChecker
from research.public_web_collector import PublicWebCollector
from research.research_analyst import ResearchAnalyst
from research.rss_collector import RSSCollector
from research.source_extractor import SourceExtractor
from research.topic_scorer import TopicScorer


@pytest.fixture
def db(tmp_path):
    test_db_path = tmp_path / "test_phase40.db"
    return Database(db_path=str(test_db_path))


@pytest.fixture
def analyst(db):
    return ResearchAnalyst(db=db)


def test_01_live_source_retrieval(db):
    """1. Tests live source retrieval using arXiv Search API query fallback."""
    collector = RSSCollector(db=db)
    feed_cfg = {
        "name": "arXiv Computer Science AI",
        "url": "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=3",
        "publisher": "arXiv.org",
        "category": "Artificial Intelligence",
        "weight": 1.0,
    }
    articles = collector.fetch_feed(feed_cfg)
    assert len(articles) > 0, "Expected at least 1 live paper from arXiv API"
    sample = articles[0]
    assert sample["title"], "Article title must not be empty"
    assert sample["url"].startswith("http"), "Article URL must be HTTP/HTTPS"
    assert sample["publisher"] == "arXiv.org"
    assert sample["published_date"], "Article must have a publication date"
    assert sample["retrieval_timestamp"], "Article must have a retrieval timestamp"


def test_02_publication_date_validation_and_iso_normalization():
    """2. Tests publication date validation and normalization across varied formats."""
    # RFC 2822 format (standard RSS)
    rfc_date = "Sat, 07 Nov 2026 10:15:00 GMT"
    norm_rfc = SourceExtractor.normalize_date(rfc_date)
    assert norm_rfc.endswith("Z") or "+00:00" in norm_rfc
    assert "2026-11-07" in norm_rfc

    # ISO 8601 with offset
    iso_date = "2026-11-06T14:22:00+00:00"
    norm_iso = SourceExtractor.normalize_date(iso_date)
    assert "2026-11-06T14:22:00Z" == norm_iso

    # Simple date string YYYY-MM-DD
    simple_date = "2026-11-05"
    norm_simple = SourceExtractor.normalize_date(simple_date)
    assert norm_simple == "2026-11-05T00:00:00Z"

    # struct_time tuple
    tup = (2026, 11, 7, 12, 0, 0, 5, 311, 0)
    norm_tup = SourceExtractor.normalize_date(tup)
    assert "2026-11-07" in norm_tup


def test_03_qualitative_architectural_claim_extraction(analyst):
    """3. Tests extraction of qualitative architectural claims."""
    tech_text = (
        "The proposed system introduces a decoupled KV cache architecture. "
        "It replaces dense multi-head attention with state space linear layers to achieve constant memory footprint. "
        "Furthermore, the team released open source weights for the 7B foundation checkpoint."
    )
    url = "https://github.com/example-lab/state-space-kv"
    claims = analyst.extract_claims_from_text(tech_text, url, "Example Lab", "2026-11-07T00:00:00Z")

    assert len(claims) >= 2, "Expected multiple claims extracted"
    qual_claims = [c for c in claims if c.claim_type == "qualitative"]
    assert len(qual_claims) >= 1, "Expected at least 1 qualitative architectural claim"
    assert any("decoupled kv cache" in c.claim_text.lower() or "state space" in c.claim_text.lower() for c in qual_claims)
    assert qual_claims[0].status in (EvidenceStatus.VERIFIED, EvidenceStatus.SOURCE_REPORTED)


def test_04_quantitative_benchmark_claim_extraction(analyst):
    """4. Tests extraction of quantitative benchmark claims with metrics."""
    bench_text = (
        "In our empirical evaluation, the engine achieved a 3.8x throughput improvement over vLLM. "
        "Time-to-first-token latency was reduced by 45% while decreasing VRAM consumption by 12GB on A100 GPUs."
    )
    url = "https://arxiv.org/abs/2611.99999"
    claims = analyst.extract_claims_from_text(bench_text, url, "arXiv", "2026-11-07T00:00:00Z")

    quant_claims = [c for c in claims if c.claim_type == "quantitative"]
    assert len(quant_claims) >= 1, "Expected at least 1 quantitative claim"
    assert any("3.8x" in c.claim_text or "45%" in c.claim_text for c in quant_claims)
    assert quant_claims[0].status == EvidenceStatus.VERIFIED  # Grounded in arXiv primary paper


def test_05_claim_evidence_grounding_and_passage_matching(analyst):
    """5. Tests that claims are grounded with exact passages and retrieval timestamps."""
    article_text = (
        "Researchers demonstrated speculative decoding with a 0.5B draft model. "
        "The pipeline produced 142 tokens/sec without degradation in task accuracy."
    )
    url = "https://github.com/lab/spec-decode"
    claims = analyst.extract_claims_from_text(article_text, url, "GitHub", "2026-11-07T00:00:00Z")

    for c in claims:
        assert c.source_url == url
        assert len(c.supporting_passage) > 20
        assert c.supporting_passage in article_text
        assert c.retrieval_timestamp, "Retrieval timestamp must be present"
        assert c.confidence_score > 0.0


def test_06_contradictory_source_detection_and_status(analyst):
    """6. Tests detection of conflicting claims across sources and assignment of CONTRADICTED status."""
    primary_claim = ClaimEvidence(
        claim_id="claim_001",
        claim_text="The model achieves a 4.0x speedup across all sequence lengths with zero accuracy loss.",
        source_url="https://arxiv.org/abs/2611.11111",
        source_title="arXiv Primary Paper",
        supporting_passage="The model achieves a 4.0x speedup across all sequence lengths.",
        publisher="arXiv",
        status=EvidenceStatus.VERIFIED,
        confidence_score=0.95,
    )

    contradictory_passages = [
        {
            "url": "https://tech-audit.org/reproducibility-report",
            "publisher": "Tech Audit",
            "text": "Independent replication disputed: benchmark overstated and fails to improve latency under real-world serving.",
        }
    ]

    is_contra, contra_url, reason = FactChecker.detect_claim_contradiction(primary_claim, contradictory_passages)
    assert is_contra, "Contradiction should have been detected"
    assert "Tech Audit" in reason or "contradicts" in reason

    # Check corroboration integration
    sources = [
        Source(
            source_id="src_01",
            url=primary_claim.source_url,
            title="arXiv Paper",
            publisher="arXiv",
            credibility_score=0.98,
            raw_content=primary_claim.supporting_passage,
        ),
        Source(
            source_id="src_02",
            url=contradictory_passages[0]["url"],
            title="Audit Report",
            publisher="Tech Audit",
            credibility_score=0.85,
            raw_content=contradictory_passages[0]["text"],
        )
    ]
    corroborated = FactChecker.corroborate_claim(primary_claim, sources)
    assert corroborated.status == EvidenceStatus.CONTRADICTED
    assert corroborated.confidence_score <= 0.35
    assert "contradict" in corroborated.verification_rationale.lower()


def test_07_semantic_topic_deduplication_and_fatigue_scoring(analyst):
    """7. Tests tracking parameter removal, semantic title deduplication, and fatigue penalty."""
    existing_articles = [
        {
            "title": "Speculative Decoding in Production: Accelerating LLM Serving",
            "url": "https://arstechnica.com/ai/speculative-decoding-production",
        }
    ]

    new_articles = [
        # 1. URL with tracking parameters
        {
            "title": "Speculative Decoding in Production",
            "url": "https://arstechnica.com/ai/speculative-decoding-production/?utm_source=twitter&utm_medium=feed&ref=newsletter",
        },
        # 2. Semantic title duplicate
        {
            "title": "Accelerating LLM Serving: Speculative Decoding in Production",
            "url": "https://theverge.com/ai/speculative-decoding-llm",
        },
        # 3. Genuinely distinct article
        {
            "title": "Neuromorphic Chip Architecture Slashes Robotics Power by 80%",
            "url": "https://spectrum.ieee.org/neuromorphic-robotics-efficiency",
        }
    ]

    uniques, dup_records = Deduplicator.filter_duplicates_with_report(new_articles, existing_articles, threshold=0.60)
    assert len(uniques) == 1
    assert "Neuromorphic" in uniques[0]["title"]
    assert len(dup_records) == 2

    # Verify fatigue penalty on recent topic
    topic_candidate = {
        "title": "Speculative Decoding for Faster LLM Inference",
        "summary": "Deploying draft models to accelerate token generation.",
        "url": "https://github.com/org/spec-decoding",
        "publisher": "GitHub",
    }
    recent_productions = ["Speculative Decoding in Production: Accelerating LLM Serving"]
    score_with_fatigue = TopicScorer.score_100_points(topic_candidate, recent_production_topics=recent_productions)
    assert score_with_fatigue.fatigue_penalty == 15.0
    assert "fatigue penalty applied" in score_with_fatigue.reasoning


def test_08_freshness_scoring_based_on_publication_date():
    """8. Tests timeliness / freshness score decay based on publication age."""
    now = datetime.datetime.now(timezone.utc)

    # Fresh within 12h
    fresh_date = (now - datetime.timedelta(hours=12)).isoformat()
    score_fresh = TopicScorer._calculate_timeliness_score(fresh_date)
    assert score_fresh == 10.0

    # 48h old (< 72h)
    mid_date = (now - datetime.timedelta(hours=48)).isoformat()
    score_mid = TopicScorer._calculate_timeliness_score(mid_date)
    assert score_mid == 8.5

    # 5 days old (< 7d)
    week_date = (now - datetime.timedelta(days=5)).isoformat()
    score_week = TopicScorer._calculate_timeliness_score(week_date)
    assert score_week == 7.0

    # 45 days old (> 30d)
    old_date = (now - datetime.timedelta(days=45)).isoformat()
    score_old = TopicScorer._calculate_timeliness_score(old_date)
    assert score_old == 2.0


def test_09_dossier_provenance_and_selection_rationale(analyst):
    """9. Tests dossier provenance tracking and explainable selection rationale."""
    topic = {
        "id": "top_phase40_01",
        "title": "Continuous Speculative Decoding with Bitwise Verification",
        "summary": "A novel draft model architecture replacing floating point verification with bitwise operations, reducing latency by 3.2x.",
        "url": "https://github.com/lab/bitwise-speculative-decoding",
        "publisher": "GitHub",
        "published_date": "2026-11-06T18:00:00Z",
    }

    dossier = analyst.build_dossier(topic)
    assert isinstance(dossier, ResearchDossier)
    assert dossier.verification_status in ("VERIFIED", "SOURCE_REPORTED")
    assert dossier.selection_rationale, "Selection rationale must be non-empty"
    assert "bitwise" in dossier.selection_rationale.lower() or "score" in dossier.selection_rationale.lower()

    # Check provenance dictionary
    prov = dossier.dossier_provenance
    assert prov["pipeline_version"] == "4.0.0"
    assert prov["generated_at"]
    assert prov["primary_source_count"] == 1
    assert prov["total_claims_extracted"] >= 1
    assert prov["source_credibility_avg"] >= 0.85


def test_10_source_outage_handling_and_research_blocked(analyst):
    """10. Tests graceful degradation and RESEARCH_BLOCKED state when source is unreachable or content is empty."""
    broken_topic = {
        "id": "top_blocked_01",
        "title": "Unreachable Paper with Dead Link",
        "summary": "Short",
        "url": "https://nonexistent-server-404.local/paper.pdf",
        "publisher": "Dead Link Publisher",
    }

    dossier = analyst.build_dossier(broken_topic)
    assert dossier.verification_status == "RESEARCH_BLOCKED"
    assert dossier.primary_sources[0].credibility_score == 0.20
    assert len(dossier.uncertainties) > 0
    assert "RESEARCH_BLOCKED" in dossier.verification_status
    assert "blocked" in dossier.selection_rationale.lower()

