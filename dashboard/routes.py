"""
SUPER.INTELLIGENCEEE — FastAPI Dashboard & API Routes
Provides local web interface at http://127.0.0.1:5000 with 6 core production modules.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.config import get_config
from core.database import Database
from core.job_manager import JobManager
from core.pipeline import SuperIntelligencePipeline
from publishing.approval import ApprovalManager
from publishing.queue import PublishingQueue
from publishing.youtube_integration import YouTubeIntegration
from publishing.instagram_integration import InstagramIntegration
from research.agent_reach_connector import AgentReachConnector
from intelligence.instagram_intel import (
    score_instagram_hook,
    rank_instagram_hooks,
    get_instagram_hook_formulas,
    analyze_spoken_beats,
    lint_instagram_caption,
    detect_ai_slop,
    humanize_text,
)
from intelligence.youtube_intel import (
    check_youtube_title_thumbnail,
    score_youtube_hook,
    analyze_retention_csv,
    generate_deadair_edl,
    generate_youtube_chapters,
    build_youtube_seo_package,
)

router = APIRouter()
config = get_config()
db = Database()
pipeline = SuperIntelligencePipeline(db=db, config=config)
approval_mgr = ApprovalManager(db=db, config=config)
queue_mgr = PublishingQueue(db=db, config=config)
job_mgr = JobManager(max_workers=1)
reach_connector = AgentReachConnector(db=db, config=config)
yt_integration = YouTubeIntegration(db=db, config=config)
ig_integration = InstagramIntegration()

templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@router.get("/", response_class=HTMLResponse)
async def view_overview(request: Request):
    """View 1: System Overview and Weekly Production Statistics."""
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM topics")
        total_topics = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM scripts")
        total_scripts = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM production_jobs WHERE status = 'APPROVED'")
        approved_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM production_jobs WHERE status = 'NEEDS_REVIEW'")
        pending_review_count = cursor.fetchone()["count"]

        cursor.execute(
            "SELECT * FROM production_jobs ORDER BY id DESC LIMIT 5"
        )
        recent_jobs = [dict(r) for r in cursor.fetchall()]

    return templates.TemplateResponse(
        request=request,
        name="overview.html",
        context={
            "request": request,
            "total_topics": total_topics,
            "total_scripts": total_scripts,
            "approved_count": approved_count,
            "pending_review_count": pending_review_count,
            "weekly_target": 5,
            "recent_jobs": recent_jobs,
        },
    )


@router.get("/research", response_class=HTMLResponse)
async def view_research(request: Request):
    """View 2: Research Engine & Topic Discovery."""
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM topics ORDER BY score DESC LIMIT 30"
        )
        topics = [dict(r) for r in cursor.fetchall()]

        cursor.execute("SELECT * FROM sources ORDER BY id ASC")
        sources = [dict(r) for r in cursor.fetchall()]

    return templates.TemplateResponse(
        request=request,
        name="research.html",
        context={
            "request": request,
            "topics": topics,
            "sources": sources,
        },
    )


@router.post("/api/research/discover")
async def trigger_discovery():
    """Triggers RSS and public web research discovery."""
    scored = pipeline.run_topic_research()
    return {"status": "SUCCESS", "message": f"Discovered and scored {len(scored)} topics."}


@router.get("/scripts", response_class=HTMLResponse)
async def view_scripts(request: Request):
    """View 3: Script Studio & Fact Checking."""
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT s.*, t.title as topic_title, t.category 
            FROM scripts s
            LEFT JOIN topics t ON s.topic_id = t.id
            ORDER BY s.id DESC LIMIT 20
            """
        )
        scripts = [dict(r) for r in cursor.fetchall()]

    return templates.TemplateResponse(
        request=request,
        name="scripts.html",
        context={
            "request": request,
            "scripts": scripts,
        },
    )


@router.get("/production", response_class=HTMLResponse)
async def view_production(request: Request):
    """View 4: Video Production & Rendering Queue."""
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.*, t.title as topic_title
            FROM production_jobs p
            LEFT JOIN topics t ON p.topic_id = t.id
            ORDER BY p.id DESC LIMIT 20
            """
        )
        jobs = [dict(r) for r in cursor.fetchall()]

    return templates.TemplateResponse(
        request=request,
        name="production.html",
        context={
            "request": request,
            "jobs": jobs,
        },
    )


@router.post("/api/production/produce")
async def trigger_production(topic_id: Optional[int] = Form(None)):
    """Triggers end-to-end video production for a topic."""
    result = pipeline.produce_reel(topic_id=topic_id)
    return {"status": "SUCCESS", "result": result}


@router.get("/review", response_class=HTMLResponse)
async def view_review(request: Request):
    """View 5: Human-in-the-Loop Video Review Station."""
    with db.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.*, t.title as topic_title, t.category
            FROM production_jobs p
            LEFT JOIN topics t ON p.topic_id = t.id
            WHERE p.status = 'NEEDS_REVIEW' OR p.status = 'APPROVED'
            ORDER BY p.id DESC
            """
        )
        reels_for_review = [dict(r) for r in cursor.fetchall()]

    # Convert paths to media URLs
    for r in reels_for_review:
        if r.get("output_video_path"):
            p = Path(r["output_video_path"])
            # Format relative URL for frontend media mounting
            r["media_url"] = f"/media/{p.parent.name}/{p.name}"
        else:
            r["media_url"] = ""

    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "request": request,
            "reels": reels_for_review,
        },
    )


@router.post("/api/review/{production_id}/approve")
async def approve_video(production_id: int):
    """Approves video and enqueues into weekly publishing queue."""
    res = approval_mgr.approve_reel(production_id)
    return {"status": "APPROVED", "result": res}


@router.post("/api/review/{production_id}/reject")
async def reject_video(production_id: int, reason: str = Form("Failed editorial guidelines.")):
    """Rejects video."""
    res = approval_mgr.reject_reel(production_id, reason=reason)
    return {"status": "REJECTED", "result": res}


@router.get("/queue", response_class=HTMLResponse)
async def view_queue(request: Request):
    """View 6: Weekly Instagram Publishing Queue (5 Reels/week)."""
    items = queue_mgr.list_queue()
    for item in items:
        if item.get("video_path"):
            p = Path(item["video_path"])
            item["media_url"] = f"/media/{p.parent.name}/{p.name}"

    return templates.TemplateResponse(
        request=request,
        name="queue.html",
        context={
            "request": request,
            "items": items,
        },
    )


@router.get("/api/health")
async def get_health():
    """Returns technical diagnostics and environment health status."""
    return {
        "status": "ONLINE",
        "system": "SUPER.INTELLIGENCEEE V2",
        "python": "3.11.15",
        "piper_tts": "OPERATIONAL",
        "hyperframes": "OPERATIONAL",
        "ffmpeg": "OPERATIONAL",
        "weekly_target": 5,
        "database": "ACTIVE",
        "agent_reach": "AVAILABLE" if reach_connector.is_available() else "UNAVAILABLE",
        "youtube_api": "AUTHENTICATED" if yt_integration.is_authenticated() else "CONFIGURED" if yt_integration.is_configured() else "NOT_CONFIGURED",
    }


# ===========================================================================
# Omnichannel Intelligence Lab Endpoints
# ===========================================================================
@router.get("/intelligence", response_class=HTMLResponse)
async def view_intelligence(request: Request):
    """View 7: Omnichannel Content Intelligence Lab."""
    return templates.TemplateResponse(
        request=request,
        name="intelligence.html",
        context={
            "request": request,
            "agent_reach_available": reach_connector.is_available(),
            "yt_authenticated": yt_integration.is_authenticated(),
        },
    )


@router.post("/api/intelligence/hook/score")
async def api_score_hook(payload: Dict[str, Any]):
    hook = payload.get("hook", "")
    platform = payload.get("platform", "instagram")
    if platform == "youtube":
        return score_youtube_hook(hook)
    return score_instagram_hook(hook)


@router.get("/api/intelligence/hook/formulas")
async def api_get_hook_formulas():
    return {"instagram": get_instagram_hook_formulas()}


@router.post("/api/intelligence/script/beats")
async def api_analyze_beats(payload: Dict[str, Any]):
    script_text = payload.get("script_text", "")
    wpm = int(payload.get("wpm", 165))
    target = float(payload.get("target_seconds", 38.0))
    return analyze_spoken_beats(script_text, wpm=wpm, target_seconds=target)


@router.post("/api/intelligence/caption/lint")
async def api_lint_caption(payload: Dict[str, Any]):
    caption_text = payload.get("caption_text", "")
    keywords = payload.get("keywords")
    return lint_instagram_caption(caption_text, keywords=keywords)


@router.post("/api/intelligence/text/slop")
async def api_detect_slop(payload: Dict[str, Any]):
    text = payload.get("text", "")
    return detect_ai_slop(text)


@router.post("/api/intelligence/text/humanize")
async def api_humanize_text(payload: Dict[str, Any]):
    text = payload.get("text", "")
    humanized, applied = humanize_text(text)
    return {"original": text, "humanized_text": humanized, "replacements_applied": applied}


@router.post("/api/intelligence/youtube/title")
async def api_check_yt_title(payload: Dict[str, Any]):
    title = payload.get("title", "")
    thumb_text = payload.get("thumb_text")
    return check_youtube_title_thumbnail(title, thumb_text=thumb_text)


@router.post("/api/intelligence/youtube/retention")
async def api_analyze_retention(payload: Dict[str, Any]):
    csv_content = payload.get("csv_content", "")
    duration = float(payload.get("duration_seconds", 120.0))
    return analyze_retention_csv(csv_content, duration_seconds=duration)


@router.post("/api/intelligence/youtube/chapters")
async def api_generate_chapters(payload: Dict[str, Any]):
    transcript = payload.get("transcript", "")
    return generate_youtube_chapters(transcript)


@router.post("/api/intelligence/youtube/deadair")
async def api_generate_deadair(payload: Dict[str, Any]):
    transcript = payload.get("transcript", "")
    floor = float(payload.get("floor_seconds", 0.45))
    return generate_deadair_edl(transcript, floor_seconds=floor)


# ===========================================================================
# Agent Reach Multi-Channel Research
# ===========================================================================
@router.post("/api/intelligence/research/reach")
async def api_query_reach(payload: Dict[str, Any]):
    channel = payload.get("channel", "github")
    query = payload.get("query", "")

    if channel == "github":
        res = reach_connector.search_github(query, limit=5)
        return {"ok": True, "result": res}
    elif channel == "youtube":
        meta = reach_connector.get_youtube_metadata(query)
        sub = reach_connector.get_youtube_transcript(query)
        if meta.get("ok"):
            meta["transcript"] = sub.get("transcript", "")
            return {"ok": True, "result": meta}
        return {"ok": False, "error": meta.get("error")}
    elif channel == "reddit":
        res = reach_connector.search_reddit_public(query, limit=5)
        return {"ok": True, "result": res}
    elif channel == "web":
        res = reach_connector.read_web_page(query)
        return {"ok": res.get("ok", False), "result": res}
    else:
        return {"ok": False, "error": {"hint": f"Channel '{channel}' is not permitted."}}


@router.post("/api/intelligence/research/ingest")
async def api_ingest_reach_results(payload: Dict[str, Any]):
    items = payload.get("items", [])
    category = payload.get("category", "Technology Experiments")
    inserted_ids = reach_connector.ingest_research_to_topics(items, category=category)
    return {"ok": True, "inserted_count": len(inserted_ids), "topic_ids": inserted_ids}


# ===========================================================================
# Publishing & Account Connection Endpoints
# ===========================================================================
@router.get("/oauth/youtube/connect")
async def oauth_youtube_connect():
    """Redirects operator to official Google OAuth 2.0 authorization screen."""
    if not yt_integration.is_configured():
        raise HTTPException(
            status_code=400,
            detail="YouTube OAuth Client ID and Secret not configured in .env or config.",
        )
    auth_url = yt_integration.get_auth_url()
    return RedirectResponse(url=auth_url)


@router.get("/oauth2callback")
async def oauth2_callback(code: Optional[str] = None, error: Optional[str] = None):
    """Handles OAuth 2.0 redirect code from Google."""
    if error:
        return HTMLResponse(f"<h3>Google OAuth Error: {error}</h3><a href='/intelligence'>Back to Dashboard</a>")
    if not code:
        return HTMLResponse("<h3>Missing authorization code</h3><a href='/intelligence'>Back to Dashboard</a>")

    res = yt_integration.exchange_code(code)
    if res.get("ok"):
        return RedirectResponse(url="/intelligence?connected=youtube")
    return HTMLResponse(f"<h3>Token exchange failed: {res.get('error')}</h3><a href='/intelligence'>Back</a>")


# ---------------------------------------------------------------------------
# Instagram Meta Unified Login OAuth & Publishing Endpoints
# ---------------------------------------------------------------------------
@router.get("/oauth/instagram/connect")
async def oauth_instagram_connect():
    """Redirects operator to official Meta Unified Login authorization screen."""
    if not ig_integration.is_configured():
        return HTMLResponse(
            "<h3>Meta Instagram API Configuration Incomplete</h3>"
            "<p>Please configure <code>META_APP_ID</code> and <code>META_APP_SECRET</code> in your <code>.env</code> file or <code>config.yaml</code>.</p>"
            "<p>Optionally configure <code>INSTAGRAM_CONFIG_ID</code> if you set up a Configuration ID in Meta App Dashboard.</p>"
            "<br><a href='/intelligence' style='color:#00e5ff;'>← Back to Dashboard</a>"
        )
    try:
        auth_url, _ = ig_integration.get_authorization_url()
        return RedirectResponse(url=auth_url)
    except Exception as e:
        return HTMLResponse(f"<h3>Failed to build Instagram authorization URL: {e}</h3><a href='/intelligence'>Back</a>")


@router.get("/oauth/instagram/callback")
async def oauth_instagram_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    error_reason: Optional[str] = None,
    error_description: Optional[str] = None,
):
    """
    Handles redirect callback from Meta Unified Login:
    - Validates HMAC signed state
    - Checks for user consent denial or provider errors
    - Exchanges authorization code for encrypted token
    - Verifies Instagram professional identity and permissions
    """
    if error:
        msg = error_description or error_reason or error
        return HTMLResponse(
            f"<div style='font-family:sans-serif; background:#080b14; color:#f8fafc; padding:2rem; min-height:100vh;'>"
            f"<h2 style='color:#ef4444;'>Meta Login Authorization Cancelled or Failed</h2>"
            f"<p><b>Provider Error:</b> {msg}</p>"
            f"<p style='color:#94a3b8;'>If you declined permissions, please reconnect and grant access to your Instagram Professional account.</p>"
            f"<br><a href='/intelligence' style='display:inline-block; background:#00e5ff; color:#000; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:bold;'>← Return to Dashboard</a>"
            f"</div>"
        )

    if not code:
        return HTMLResponse(
            "<div style='font-family:sans-serif; background:#080b14; color:#f8fafc; padding:2rem; min-height:100vh;'>"
            "<h2 style='color:#ef4444;'>Missing Authorization Code</h2>"
            "<p>Meta did not return an authorization code.</p>"
            "<br><a href='/intelligence' style='display:inline-block; background:#00e5ff; color:#000; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:bold;'>← Return to Dashboard</a>"
            "</div>"
        )

    res = ig_integration.exchange_code(code=code, state=state)
    if res.get("ok"):
        return RedirectResponse(url="/intelligence?connected=instagram")
    else:
        err_msg = res.get("error", "Unknown authorization exchange error.")
        return HTMLResponse(
            f"<div style='font-family:sans-serif; background:#080b14; color:#f8fafc; padding:2rem; min-height:100vh;'>"
            f"<h2 style='color:#ef4444;'>Instagram Connection Failed</h2>"
            f"<p><b>Error Details:</b> {err_msg}</p>"
            f"<p style='color:#94a3b8;'>Ensure your Meta App is configured with Unified Login and that an Instagram Professional account is assigned to your Business Portfolio.</p>"
            f"<br><a href='/intelligence' style='display:inline-block; background:#00e5ff; color:#000; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:bold;'>← Back to Dashboard</a>"
            f"</div>"
        )


@router.post("/api/instagram/disconnect")
async def api_instagram_disconnect():
    """Disconnects and securely wipes encrypted Instagram credentials."""
    ok = ig_integration.disconnect()
    return {"ok": ok, "status": "DISCONNECTED"}


@router.post("/api/instagram/publish/{queue_id}")
async def api_instagram_publish(
    queue_id: int,
    request: Request,
):
    """
    Publishes an approved Reel through the official Meta Graph API.
    MANDATORY: Explicit human editorial approval must be submitted.
    """
    data = {}
    try:
        data = await request.json()
    except Exception:
        pass

    explicit_approval = bool(data.get("explicit_approval", False))
    if not explicit_approval:
        raise HTTPException(
            status_code=403,
            detail="Explicit human editorial approval is required before publishing any Reel to Instagram.",
        )

    try:
        res = ig_integration.publish_reel(queue_item_id=queue_id, explicit_approval=True)
        return {"ok": True, "result": res}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        logger.exception(f"Error publishing Reel #{queue_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/publishing/status")
async def api_publishing_status():
    """Returns technical publishing and OAuth status for YouTube and Instagram."""
    ig_status = ig_integration.get_connection_status()
    return {
        "youtube": {
            "configured": yt_integration.is_configured(),
            "authenticated": yt_integration.is_authenticated(),
            "status": "AUTHENTICATED" if yt_integration.is_authenticated() else "CONFIGURED_NOT_AUTHENTICATED" if yt_integration.is_configured() else "NOT_CONFIGURED",
            "client_id": yt_integration.client_id[:16] + "..." if yt_integration.client_id else None,
            "redirect_uri": yt_integration.redirect_uri,
        },
        "instagram": ig_status,
    }



