import os
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for

from core.config_manager import get_config
from core.database import get_db
from core.logger import get_logger, get_system_resources
from core.task_manager import TaskManager
from core.scheduler import Scheduler
from research.rss_collector import RSSCollector
from research.fact_checking import FactChecker
from intelligence.script_generator import ScriptGenerator
from rendering.video_renderer import VideoRenderer
from publishing.content_queue import ContentQueue
from publishing.caption_manager import CaptionManager
from publishing.instagram_integration import InstagramIntegration
from analytics.performance_tracker import PerformanceTracker
from analytics.weekly_report import WeeklyReport
from media.asset_manager import AssetManager

logger = get_logger("Dashboard")

def create_app() -> Flask:
    base_dir = Path(__file__).resolve().parent.parent
    template_dir = base_dir / "dashboard" / "templates"
    static_dir = base_dir / "dashboard" / "static"

    app = Flask(__name__, template_folder=str(template_dir), static_folder=str(static_dir))
    app.config["SECRET_KEY"] = "super-intelligence-secret-key-2026"

    config = get_config()
    db = get_db()
    task_manager = TaskManager()
    scheduler = Scheduler()
    fact_checker = FactChecker()
    script_generator = ScriptGenerator()
    video_renderer = VideoRenderer()
    content_queue = ContentQueue()
    ig_integration = InstagramIntegration()
    analytics_tracker = PerformanceTracker()
    weekly_reporter = WeeklyReport()
    asset_manager = AssetManager()

    # Serve rendered video and cover outputs
    @app.route("/output/<path:filename>")
    def serve_output(filename):
        output_dir = config.resolve_path("output")
        return send_from_directory(output_dir, filename)

    # -------------------------------------------------------------
    # Main Dashboard Single-Page View
    # -------------------------------------------------------------
    @app.route("/")
    def index():
        stats = db.get_dashboard_stats()
        schedule_info = scheduler.get_today_schedule()
        full_week = scheduler.get_full_week_schedule()
        articles = db.get_articles(limit=50)
        scripts = db.get_scripts(limit=50)
        jobs = db.get_production_jobs(limit=50)
        queue = db.get_publishing_queue()
        assets = asset_manager.list_assets()
        analytics_summary = analytics_tracker.get_summary()
        resources = get_system_resources()
        api_readiness = ig_integration.check_api_readiness()

        return render_template(
            "index.html",
            stats=stats,
            schedule_info=schedule_info,
            full_week=full_week,
            articles=articles,
            scripts=scripts,
            jobs=jobs,
            queue=queue,
            assets=assets,
            analytics=analytics_summary,
            resources=resources,
            api_readiness=api_readiness,
            brand_name=config.get("brand.name", "SUPER.INTELLIGENCEEE"),
            brand_handle=config.get("brand.handle", "@super.intelligenceee")
        )

    # -------------------------------------------------------------
    # API: System Telemetry & Tasks
    # -------------------------------------------------------------
    @app.route("/api/telemetry")
    def api_telemetry():
        return jsonify({
            "resources": get_system_resources(),
            "stats": db.get_dashboard_stats(),
            "active_tasks": task_manager.list_tasks()
        })

    @app.route("/api/tasks/<task_id>")
    def api_task_status(task_id):
        t = task_manager.get_task(task_id)
        if not t:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(t)

    # -------------------------------------------------------------
    # API: Research & Discovery
    # -------------------------------------------------------------
    @app.route("/api/research/discover", methods=["POST"])
    def api_discover_stories():
        def _task(task_obj):
            collector = RSSCollector()
            def p_cb(pct, msg):
                task_obj.set_progress(pct, msg)
            res = collector.collect_all(progress_callback=p_cb)
            return {"discovered_count": len(res)}

        tid = task_manager.submit_task("RSS Discovery Cycle", _task)
        return jsonify({"task_id": tid, "message": "Discovery started in background."})

    @app.route("/api/research/status", methods=["POST"])
    def api_update_article_status():
        data = request.json or {}
        article_id = int(data.get("article_id", 0))
        new_status = data.get("status", "")
        notes = data.get("notes", "")

        ok, msg = fact_checker.update_status(article_id, new_status, notes=notes)
        if ok:
            return jsonify({"success": True, "message": msg})
        return jsonify({"success": False, "error": msg}), 400

    @app.route("/api/research/add", methods=["POST"])
    def api_add_custom_article():
        data = request.json or {}
        title = data.get("title", "").strip()
        url = data.get("url", "").strip()
        publisher = data.get("publisher", "Manual Entry").strip()
        summary = data.get("summary", "").strip()
        category = data.get("category", "Artificial Intelligence News")

        if not title or not url:
            return jsonify({"error": "Title and URL are required"}), 400

        art_id = db.insert_article({
            "title": title,
            "url": url,
            "publisher": publisher,
            "summary": summary,
            "category": category,
            "status": "SHORTLISTED",
            "score": 1.5,
            "notes": "Added manually via dashboard"
        })
        return jsonify({"success": True, "article_id": art_id})

    # -------------------------------------------------------------
    # API: Script Intelligence
    # -------------------------------------------------------------
    @app.route("/api/scripts/generate", methods=["POST"])
    def api_generate_script():
        data = request.json or {}
        article_id = int(data.get("article_id", 0))
        articles = db.get_articles(limit=1000)
        art = next((a for a in articles if a["id"] == article_id), None)
        if not art:
            return jsonify({"error": "Article not found"}), 404

        script = script_generator.create_script_for_article(art)
        if script:
            return jsonify({"success": True, "script": script})
        return jsonify({"error": "Failed to generate script"}), 500

    @app.route("/api/scripts/<int:script_id>/update", methods=["POST"])
    def api_update_script(script_id):
        data = request.json or {}
        existing = db.get_script_by_id(script_id)
        if not existing:
            return jsonify({"error": "Script not found"}), 404

        # Update fields
        for k in ["title", "hook", "context", "development", "explanation", "implications", "limitations", "takeaway", "status"]:
            if k in data:
                existing[k] = data[k]

        # Recalculate word count
        all_text = " ".join([
            existing.get("hook", ""), existing.get("context", ""),
            existing.get("development", ""), existing.get("explanation", ""),
            existing.get("implications", ""), existing.get("limitations", ""),
            existing.get("takeaway", "")
        ])
        existing["word_count"] = len(all_text.split())
        existing["est_duration"] = round(existing["word_count"] / 2.6, 1)

        ok = db.update_script(script_id, existing)
        return jsonify({"success": ok, "script": existing})

    # -------------------------------------------------------------
    # API: Video Rendering & Production
    # -------------------------------------------------------------
    @app.route("/api/render/single", methods=["POST"])
    def api_render_single():
        if task_manager.is_render_running():
            return jsonify({"error": "Another video is currently rendering. Sequential rendering strictly enforced for 8 GB RAM."}), 429

        data = request.json or {}
        script_id = int(data.get("script_id", 0))
        script = db.get_script_by_id(script_id)
        if not script:
            return jsonify({"error": "Script not found"}), 404

        def _task(task_obj):
            def p_cb(pct, msg):
                task_obj.set_progress(pct, msg)
            return video_renderer.render_reel(script_or_id=script, progress_callback=p_cb)

        tid = task_manager.submit_task(f"Render Reel: {script.get('title')[:30]}", _task)
        return jsonify({"task_id": tid, "message": "Render task queued."})

    @app.route("/api/render/batch", methods=["POST"])
    def api_render_batch():
        if task_manager.is_render_running():
            return jsonify({"error": "A render task is already in progress."}), 429

        # Render all approved scripts up to 5 sequentially
        scripts = db.get_scripts(status="APPROVED", limit=5)
        if not scripts:
            # Fallback: look for draft scripts if none explicitly approved
            scripts = db.get_scripts(status="DRAFT", limit=5)

        if not scripts:
            return jsonify({"error": "No scripts ready to render. Generate or approve scripts first."}), 400

        def _batch_task(task_obj):
            total = len(scripts)
            results = []
            for idx, sc in enumerate(scripts):
                pct_start = int((idx / total) * 100)
                task_obj.set_progress(pct_start, f"Batch {idx+1}/{total}: Starting '{sc.get('title')[:25]}'")
                
                def sub_p_cb(sub_pct, sub_msg):
                    composite_pct = int(pct_start + (sub_pct / 100) * (100 / total))
                    task_obj.set_progress(composite_pct, f"Reel {idx+1}/{total}: {sub_msg}")

                res = video_renderer.render_reel(script_or_id=sc, progress_callback=sub_p_cb)
                results.append(res)
            return {"batch_completed": len(results), "reels": results}

        tid = task_manager.submit_task(f"Sequential Batch Render ({len(scripts)} Reels)", _batch_task)
        return jsonify({"task_id": tid, "message": f"Sequential batch render of {len(scripts)} Reels started."})

    # -------------------------------------------------------------
    # API: Publishing & Package Export
    # -------------------------------------------------------------
    @app.route("/api/publishing/assign-weekly", methods=["POST"])
    def api_assign_weekly_slots():
        scheduled = content_queue.assign_weekly_slots()
        return jsonify({"success": True, "scheduled_count": len(scheduled)})

    @app.route("/api/publishing/export-package", methods=["POST"])
    def api_export_publish_package():
        data = request.json or {}
        item_id = int(data.get("item_id", 0))
        try:
            pkg = ig_integration.create_export_package(item_id)
            return jsonify({"success": True, "package": pkg})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/api/publishing/status", methods=["POST"])
    def api_update_publishing_status():
        data = request.json or {}
        item_id = int(data.get("item_id", 0))
        new_status = data.get("status", "")
        notes = data.get("notes", "")
        ok = content_queue.update_status(item_id, new_status, notes=notes)
        return jsonify({"success": ok})

    # -------------------------------------------------------------
    # API: Meta Unified Login & Instagram Direct Publishing
    # -------------------------------------------------------------
    @app.route("/oauth/instagram/connect")
    def flask_oauth_instagram_connect():
        if not ig_integration.is_configured():
            return "<h3>Meta Instagram API not configured in .env or config</h3><a href='/'>Back</a>", 400
        try:
            auth_url, _ = ig_integration.get_authorization_url()
            return redirect(auth_url)
        except Exception as e:
            return f"<h3>OAuth Connect Error: {e}</h3><a href='/'>Back</a>", 500

    @app.route("/oauth/instagram/callback")
    def flask_oauth_instagram_callback():
        error = request.args.get("error")
        error_desc = request.args.get("error_description") or request.args.get("error_reason") or error
        if error:
            return f"<h3>Meta Authorization Failed: {error_desc}</h3><a href='/'>Return to Dashboard</a>", 400

        code = request.args.get("code")
        state = request.args.get("state")
        if not code:
            return "<h3>Missing authorization code from Meta</h3><a href='/'>Back</a>", 400

        res = ig_integration.exchange_code(code=code, state=state)
        if res.get("ok"):
            return redirect("/?connected=instagram")
        return f"<h3>Token Exchange Failed: {res.get('error')}</h3><a href='/'>Back</a>", 400

    @app.route("/api/instagram/status")
    def flask_api_instagram_status():
        return jsonify(ig_integration.get_connection_status())

    @app.route("/api/instagram/disconnect", methods=["POST"])
    def flask_api_instagram_disconnect():
        ok = ig_integration.disconnect()
        return jsonify({"ok": ok, "status": "DISCONNECTED"})

    @app.route("/api/instagram/publish/<int:queue_id>", methods=["POST"])
    def flask_api_instagram_publish(queue_id):
        data = request.json or {}
        explicit_approval = bool(data.get("explicit_approval", False))
        if not explicit_approval:
            return jsonify({"error": "Explicit human editorial approval required before publishing."}), 403

        try:
            res = ig_integration.publish_reel(queue_item_id=queue_id, explicit_approval=True)
            return jsonify({"success": True, "result": res})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # -------------------------------------------------------------
    # API: Analytics & Reports
    # -------------------------------------------------------------
    @app.route("/api/analytics/record", methods=["POST"])
    def api_record_analytics():
        data = request.json or {}
        entry_id = analytics_tracker.record_metrics(
            publishing_id=data.get("publishing_id"),
            reel_title=data.get("reel_title", "Untitled Reel"),
            views=int(data.get("views", 0)),
            reach=int(data.get("reach", 0)),
            likes=int(data.get("likes", 0)),
            comments=int(data.get("comments", 0)),
            shares=int(data.get("shares", 0)),
            saves=int(data.get("saves", 0)),
            watch_time_avg=float(data.get("watch_time_avg", 0.0)),
            followers_gained=int(data.get("followers_gained", 0))
        )
        return jsonify({"success": True, "entry_id": entry_id})

    @app.route("/api/reports/generate", methods=["POST"])
    def api_generate_report():
        rep = weekly_reporter.generate_report()
        return jsonify({"success": True, "report": rep})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False)

