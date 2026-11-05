import sqlite3
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from core.config import get_config
from core.logger import get_logger

logger = get_logger("Database")

class Database:
    """SQLite Database Manager for SUPER.INTELLIGENCEEE content production engine."""
    
    _instance: Optional["Database"] = None

    def __new__(cls, db_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_db(db_path)
            return cls._instance
        elif db_path is not None and Path(db_path) != cls._instance.db_path:
            # Create a separate isolated instance for this specific database file (e.g. test fixtures)
            obj = super(Database, cls).__new__(cls)
            obj._init_db(db_path)
            return obj
        return cls._instance

    def _init_db(self, db_path: Optional[str] = None):
        config = get_config()
        data_dir = config.resolve_path(config.get("paths.data_dir", "data"))
        data_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = Path(db_path) if db_path else data_dir / "super_intelligence.db"
        self._create_schema()
        logger.info(f"Database initialized at: {self.db_path}")

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=20.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @contextmanager
    def transaction(self):
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _create_schema(self):
        with self.get_connection() as conn:
            conn.executescript("""
            -- Sources Table
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                url TEXT NOT NULL,
                reliability_score REAL DEFAULT 1.0,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Topics / Articles Table
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                publisher TEXT NOT NULL,
                summary TEXT,
                category TEXT,
                published_date TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'DISCOVERED',
                score REAL DEFAULT 0.0,
                relevance_score REAL DEFAULT 0.0,
                freshness_score REAL DEFAULT 0.0,
                originality_score REAL DEFAULT 0.0,
                source_id INTEGER,
                notes TEXT,
                FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE SET NULL
            );

            CREATE INDEX IF NOT EXISTS idx_topics_status ON topics(status);
            CREATE INDEX IF NOT EXISTS idx_topics_score ON topics(score DESC);
            CREATE INDEX IF NOT EXISTS idx_topics_url ON topics(url);

            -- Backward-compatible articles alias / view if needed
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                publisher TEXT NOT NULL,
                summary TEXT,
                category TEXT,
                published_date TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'DISCOVERED',
                score REAL DEFAULT 0.0,
                notes TEXT
            );

            -- Scripts Table
            CREATE TABLE IF NOT EXISTS scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER,
                article_id INTEGER,
                title TEXT NOT NULL,
                content_style TEXT NOT NULL,
                hook TEXT NOT NULL,
                context TEXT,
                development TEXT,
                explanation TEXT,
                implications TEXT,
                limitations TEXT,
                takeaway TEXT,
                script_json TEXT NOT NULL,
                word_count INTEGER DEFAULT 0,
                est_duration REAL DEFAULT 0.0,
                status TEXT DEFAULT 'DRAFT',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE SET NULL
            );

            CREATE INDEX IF NOT EXISTS idx_scripts_status ON scripts(status);

            -- Storyboards Table
            CREATE TABLE IF NOT EXISTS storyboards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_id INTEGER NOT NULL,
                scene_number INTEGER NOT NULL,
                name TEXT,
                narration TEXT,
                on_screen_text TEXT,
                visual_type TEXT,
                instructions TEXT,
                transition TEXT,
                duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (script_id) REFERENCES scripts(id) ON DELETE CASCADE
            );

            -- Media Assets Table
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL UNIQUE,
                asset_type TEXT NOT NULL,
                source_url TEXT,
                creator TEXT,
                license TEXT DEFAULT 'Editorial Generated',
                attribution TEXT,
                permissions TEXT,
                width INTEGER,
                height INTEGER,
                duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Backward-compatible media_assets alias table
            CREATE TABLE IF NOT EXISTS media_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL UNIQUE,
                asset_type TEXT NOT NULL,
                source_url TEXT,
                creator TEXT,
                license TEXT DEFAULT 'Editorial Generated',
                attribution TEXT,
                permissions TEXT,
                width INTEGER,
                height INTEGER,
                duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Narration Jobs Table
            CREATE TABLE IF NOT EXISTS narration_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_id INTEGER,
                engine TEXT NOT NULL,
                voice TEXT NOT NULL,
                output_audio_path TEXT,
                duration REAL,
                execution_time_seconds REAL,
                status TEXT DEFAULT 'PENDING',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (script_id) REFERENCES scripts(id) ON DELETE CASCADE
            );

            -- Caption Jobs Table
            CREATE TABLE IF NOT EXISTS caption_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_id INTEGER,
                srt_path TEXT,
                vtt_path TEXT,
                json_path TEXT,
                status TEXT DEFAULT 'PENDING',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (script_id) REFERENCES scripts(id) ON DELETE CASCADE
            );

            -- Render Jobs Table
            CREATE TABLE IF NOT EXISTS render_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_id INTEGER,
                renderer_type TEXT DEFAULT 'HyperFrames',
                output_path TEXT,
                resolution TEXT,
                fps INTEGER,
                execution_time_seconds REAL,
                status TEXT DEFAULT 'PENDING',
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (script_id) REFERENCES scripts(id) ON DELETE CASCADE
            );

            -- Master Production Jobs Table
            CREATE TABLE IF NOT EXISTS production_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_id INTEGER,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'PENDING',
                output_video_path TEXT,
                cover_image_path TEXT,
                audio_path TEXT,
                subtitle_path TEXT,
                render_time_seconds REAL,
                file_size_mb REAL,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (script_id) REFERENCES scripts(id) ON DELETE SET NULL
            );

            CREATE INDEX IF NOT EXISTS idx_jobs_status ON production_jobs(status);

            -- Approvals Table
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL, -- 'script', 'video'
                entity_id INTEGER NOT NULL,
                reviewer TEXT DEFAULT 'Human Editor',
                decision TEXT NOT NULL,    -- 'APPROVED', 'REJECTED'
                feedback TEXT,
                decided_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Publishing Queue Table
            CREATE TABLE IF NOT EXISTS publishing_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                title TEXT NOT NULL,
                caption TEXT NOT NULL,
                hashtags TEXT NOT NULL,
                scheduled_for TIMESTAMP,
                status TEXT DEFAULT 'QUEUED',
                ig_media_id TEXT,
                published_at TIMESTAMP,
                export_path TEXT,
                notes TEXT,
                FOREIGN KEY (job_id) REFERENCES production_jobs(id) ON DELETE SET NULL
            );

            CREATE INDEX IF NOT EXISTS idx_pub_status ON publishing_queue(status);

            -- Analytics Table
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                publishing_id INTEGER,
                reel_title TEXT NOT NULL,
                views INTEGER DEFAULT 0,
                reach INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                saves INTEGER DEFAULT 0,
                watch_time_avg REAL DEFAULT 0.0,
                followers_gained INTEGER DEFAULT 0,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (publishing_id) REFERENCES publishing_queue(id) ON DELETE SET NULL
            );

            -- Application Settings Table
            CREATE TABLE IF NOT EXISTS application_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- OAuth States Table (Persistent CSRF Protection with Atomic Single-Use)
            CREATE TABLE IF NOT EXISTS oauth_states (
                nonce TEXT PRIMARY KEY,
                provider TEXT NOT NULL DEFAULT 'instagram',
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                consumed INTEGER DEFAULT 0,
                consumed_at REAL
            );
            CREATE INDEX IF NOT EXISTS idx_oauth_states_expires ON oauth_states(expires_at);
            """)

            # Safe automated migrations for schema evolution
            migrations = [
                "ALTER TABLE scripts ADD COLUMN topic_id INTEGER",
                "ALTER TABLE scripts ADD COLUMN article_id INTEGER",
                "ALTER TABLE production_jobs ADD COLUMN topic_id INTEGER",
                "ALTER TABLE production_jobs ADD COLUMN updated_at TIMESTAMP",
                "ALTER TABLE production_jobs ADD COLUMN error_log TEXT",
                "ALTER TABLE approvals ADD COLUMN production_job_id INTEGER",
                "ALTER TABLE approvals ADD COLUMN status TEXT",
                "ALTER TABLE approvals ADD COLUMN reviewer_notes TEXT",
                "ALTER TABLE approvals ADD COLUMN submitted_at TIMESTAMP",
                "ALTER TABLE approvals ADD COLUMN reviewed_at TIMESTAMP",
                "ALTER TABLE publishing_queue ADD COLUMN production_job_id INTEGER",
                "ALTER TABLE publishing_queue ADD COLUMN scheduled_time TIMESTAMP",
                "ALTER TABLE publishing_queue ADD COLUMN video_path TEXT",
                "ALTER TABLE publishing_queue ADD COLUMN caption_text TEXT",
                "ALTER TABLE publishing_queue ADD COLUMN retry_count INTEGER DEFAULT 0",
                "ALTER TABLE assets ADD COLUMN name TEXT",
                "ALTER TABLE assets ADD COLUMN filename TEXT",
                "ALTER TABLE assets ADD COLUMN file_hash TEXT",
                "ALTER TABLE assets ADD COLUMN file_size_bytes INTEGER",
                "ALTER TABLE assets ADD COLUMN license_type TEXT",
                "ALTER TABLE assets ADD COLUMN author TEXT",
                "ALTER TABLE assets ADD COLUMN tags TEXT",
                "ALTER TABLE assets ADD COLUMN is_verified INTEGER DEFAULT 1",
            ]
            for mig in migrations:
                try:
                    conn.execute(mig)
                except Exception:
                    pass

    # -------------------------------------------------------------
    # Topic / Article Operations
    # -------------------------------------------------------------
    def insert_topic(self, topic: Dict[str, Any]) -> Optional[int]:
        now_iso = datetime.now(timezone.utc).isoformat()
        try:
            with self.get_connection() as conn:
                cur = conn.execute("""
                    INSERT OR IGNORE INTO topics (
                        title, url, publisher, summary, category, published_date,
                        status, score, relevance_score, freshness_score, originality_score, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    topic.get("title"),
                    topic.get("url"),
                    topic.get("publisher", "Unknown"),
                    topic.get("summary", ""),
                    topic.get("category", "Artificial Intelligence News"),
                    topic.get("published_date", now_iso),
                    topic.get("status", "DISCOVERED"),
                    topic.get("score", 0.0),
                    topic.get("relevance_score", 0.0),
                    topic.get("freshness_score", 0.0),
                    topic.get("originality_score", 0.0),
                    topic.get("notes", "")
                ))
                # Also mirror into articles table for backward compatibility
                conn.execute("""
                    INSERT OR IGNORE INTO articles (
                        title, url, publisher, summary, category, published_date, status, score, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    topic.get("title"), topic.get("url"), topic.get("publisher", "Unknown"),
                    topic.get("summary", ""), topic.get("category", "Artificial Intelligence News"),
                    topic.get("published_date", now_iso), topic.get("status", "DISCOVERED"),
                    topic.get("score", 0.0), topic.get("notes", "")
                ))
                last_id = cur.lastrowid
                if not last_id or last_id == 0:
                    lookup = conn.execute("SELECT id FROM topics WHERE url = ?", (topic.get("url"),)).fetchone()
                    if lookup:
                        last_id = lookup["id"]
                return last_id
        except Exception as e:
            logger.error(f"Error inserting topic: {e}")
            return None

    def insert_article(self, article: Dict[str, Any]) -> Optional[int]:
        return self.insert_topic(article)

    def get_topics(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            if status:
                cur = conn.execute(
                    "SELECT * FROM topics WHERE status = ? ORDER BY score DESC, discovered_at DESC LIMIT ?",
                    (status, limit)
                )
            else:
                cur = conn.execute(
                    "SELECT * FROM topics ORDER BY score DESC, discovered_at DESC LIMIT ?",
                    (limit,)
                )
            return [dict(row) for row in cur.fetchall()]

    def get_articles(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        return self.get_topics(status=status, limit=limit)

    def update_topic_status(self, topic_id: int, new_status: str, notes: Optional[str] = None) -> bool:
        with self.get_connection() as conn:
            if notes is not None:
                cur = conn.execute("UPDATE topics SET status = ?, notes = ? WHERE id = ?", (new_status, notes, topic_id))
                conn.execute("UPDATE articles SET status = ?, notes = ? WHERE id = ?", (new_status, notes, topic_id))
            else:
                cur = conn.execute("UPDATE topics SET status = ? WHERE id = ?", (new_status, topic_id))
                conn.execute("UPDATE articles SET status = ? WHERE id = ?", (new_status, topic_id))
            return cur.rowcount > 0

    def update_article_status(self, article_id: int, new_status: str, notes: Optional[str] = None) -> bool:
        return self.update_topic_status(article_id, new_status, notes)

    # -------------------------------------------------------------
    # Script Operations
    # -------------------------------------------------------------
    def insert_script(self, script_data: Dict[str, Any]) -> Optional[int]:
        try:
            with self.get_connection() as conn:
                cur = conn.execute("""
                    INSERT INTO scripts (
                        topic_id, article_id, title, content_style, hook, context, development,
                        explanation, implications, limitations, takeaway, script_json,
                        word_count, est_duration, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    script_data.get("topic_id", script_data.get("article_id")),
                    script_data.get("article_id", script_data.get("topic_id")),
                    script_data.get("title"),
                    script_data.get("content_style", "Breaking AI News"),
                    script_data.get("hook", ""),
                    script_data.get("context", ""),
                    script_data.get("development", ""),
                    script_data.get("explanation", ""),
                    script_data.get("implications", ""),
                    script_data.get("limitations", ""),
                    script_data.get("takeaway", ""),
                    json.dumps(script_data.get("script_json", {})),
                    script_data.get("word_count", 0),
                    script_data.get("est_duration", 35.0),
                    script_data.get("status", "DRAFT")
                ))
                return cur.lastrowid
        except Exception as e:
            logger.error(f"Error inserting script: {e}")
            return None

    def get_scripts(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            if status:
                cur = conn.execute("SELECT * FROM scripts WHERE status = ? ORDER BY created_at DESC LIMIT ?", (status, limit))
            else:
                cur = conn.execute("SELECT * FROM scripts ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = [dict(row) for row in cur.fetchall()]
            for r in rows:
                if r.get("script_json"):
                    try:
                        r["script_json"] = json.loads(r["script_json"])
                    except Exception:
                        pass
            return rows

    def get_script_by_id(self, script_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM scripts WHERE id = ?", (script_id,))
            row = cur.fetchone()
            if not row:
                return None
            res = dict(row)
            if res.get("script_json"):
                try:
                    res["script_json"] = json.loads(res["script_json"])
                except Exception:
                    pass
            return res

    def update_script(self, script_id: int, script_data: Dict[str, Any]) -> bool:
        with self.get_connection() as conn:
            cur = conn.execute("""
                UPDATE scripts SET
                    title = ?, content_style = ?, hook = ?, context = ?,
                    development = ?, explanation = ?, implications = ?,
                    limitations = ?, takeaway = ?, script_json = ?,
                    word_count = ?, est_duration = ?, status = ?
                WHERE id = ?
            """, (
                script_data.get("title"),
                script_data.get("content_style"),
                script_data.get("hook"),
                script_data.get("context"),
                script_data.get("development"),
                script_data.get("explanation"),
                script_data.get("implications"),
                script_data.get("limitations"),
                script_data.get("takeaway"),
                json.dumps(script_data.get("script_json", {})),
                script_data.get("word_count", 0),
                script_data.get("est_duration", 35.0),
                script_data.get("status", "DRAFT"),
                script_id
            ))
            return cur.rowcount > 0

    # -------------------------------------------------------------
    # Assets Operations
    # -------------------------------------------------------------
    def register_asset(self, asset: Dict[str, Any]) -> Optional[int]:
        with self.get_connection() as conn:
            cur = conn.execute("""
                INSERT OR REPLACE INTO assets (
                    filename, file_path, asset_type, source_url, creator,
                    license, attribution, permissions, width, height, duration
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                asset.get("filename"),
                asset.get("file_path"),
                asset.get("asset_type", "image"),
                asset.get("source_url", ""),
                asset.get("creator", "SUPER.INTELLIGENCEEE"),
                asset.get("license", "Editorial Generated"),
                asset.get("attribution", ""),
                asset.get("permissions", "Authorized"),
                asset.get("width", 1080),
                asset.get("height", 1920),
                asset.get("duration", 0.0)
            ))
            # Also insert into media_assets
            conn.execute("""
                INSERT OR REPLACE INTO media_assets (
                    filename, file_path, asset_type, source_url, creator,
                    license, attribution, permissions, width, height, duration
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                asset.get("filename"), asset.get("file_path"), asset.get("asset_type", "image"),
                asset.get("source_url", ""), asset.get("creator", "SUPER.INTELLIGENCEEE"),
                asset.get("license", "Editorial Generated"), asset.get("attribution", ""),
                asset.get("permissions", "Authorized"), asset.get("width", 1080),
                asset.get("height", 1920), asset.get("duration", 0.0)
            ))
            return cur.lastrowid

    def register_media_asset(self, asset: Dict[str, Any]) -> Optional[int]:
        return self.register_asset(asset)

    def get_assets(self, asset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            if asset_type:
                cur = conn.execute("SELECT * FROM assets WHERE asset_type = ? ORDER BY created_at DESC", (asset_type,))
            else:
                cur = conn.execute("SELECT * FROM assets ORDER BY created_at DESC")
            return [dict(r) for r in cur.fetchall()]

    def get_media_assets(self, asset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.get_assets(asset_type)

    # -------------------------------------------------------------
    # Production Jobs & Approvals
    # -------------------------------------------------------------
    def create_production_job(self, script_id: Optional[int], title: str) -> int:
        with self.get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO production_jobs (script_id, title, status)
                VALUES (?, ?, 'PENDING')
            """, (script_id, title))
            return cur.lastrowid

    def update_production_job(self, job_id: int, updates: Dict[str, Any]) -> bool:
        allowed = [
            "status", "output_video_path", "cover_image_path", "audio_path",
            "subtitle_path", "render_time_seconds", "file_size_mb",
            "error_message", "completed_at"
        ]
        fields = [f"{k} = ?" for k in updates.keys() if k in allowed]
        values = [updates[k] for k in updates.keys() if k in allowed]
        if not fields:
            return False
        values.append(job_id)
        query = f"UPDATE production_jobs SET {', '.join(fields)} WHERE id = ?"
        with self.get_connection() as conn:
            cur = conn.execute(query, tuple(values))
            return cur.rowcount > 0

    def get_production_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM production_jobs ORDER BY created_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cur.fetchall()]

    def record_approval(self, entity_type: str, entity_id: int, decision: str, feedback: str = "", reviewer: str = "Human Editor") -> int:
        with self.get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO approvals (entity_type, entity_id, reviewer, decision, feedback)
                VALUES (?, ?, ?, ?, ?)
            """, (entity_type, entity_id, reviewer, decision, feedback))
            return cur.lastrowid

    # -------------------------------------------------------------
    # Publishing Queue & Analytics
    # -------------------------------------------------------------
    def add_to_publishing_queue(self, item: Dict[str, Any]) -> int:
        with self.get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO publishing_queue (
                    job_id, title, caption, hashtags, scheduled_for, status, export_path, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get("job_id"),
                item.get("title"),
                item.get("caption", ""),
                item.get("hashtags", ""),
                item.get("scheduled_for"),
                item.get("status", "QUEUED"),
                item.get("export_path", ""),
                item.get("notes", "")
            ))
            return cur.lastrowid

    def get_publishing_queue(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            if status:
                cur = conn.execute("""
                    SELECT pq.*, pj.output_video_path, pj.cover_image_path 
                    FROM publishing_queue pq 
                    LEFT JOIN production_jobs pj ON pq.job_id = pj.id
                    WHERE pq.status = ? ORDER BY pq.scheduled_for ASC, pq.id ASC
                """, (status,))
            else:
                cur = conn.execute("""
                    SELECT pq.*, pj.output_video_path, pj.cover_image_path 
                    FROM publishing_queue pq 
                    LEFT JOIN production_jobs pj ON pq.job_id = pj.id
                    ORDER BY pq.scheduled_for ASC, pq.id ASC
                """)
            return [dict(r) for r in cur.fetchall()]

    def update_publishing_item(self, item_id: int, updates: Dict[str, Any]) -> bool:
        allowed = ["caption", "hashtags", "scheduled_for", "status", "ig_media_id", "published_at", "export_path", "notes"]
        fields = [f"{k} = ?" for k in updates.keys() if k in allowed]
        values = [updates[k] for k in updates.keys() if k in allowed]
        if not fields:
            return False
        values.append(item_id)
        query = f"UPDATE publishing_queue SET {', '.join(fields)} WHERE id = ?"
        with self.get_connection() as conn:
            cur = conn.execute(query, tuple(values))
            return cur.rowcount > 0

    def record_analytics(self, entry: Dict[str, Any]) -> int:
        with self.get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO analytics (
                    publishing_id, reel_title, views, reach, likes, comments,
                    shares, saves, watch_time_avg, followers_gained
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.get("publishing_id"),
                entry.get("reel_title"),
                entry.get("views", 0),
                entry.get("reach", 0),
                entry.get("likes", 0),
                entry.get("comments", 0),
                entry.get("shares", 0),
                entry.get("saves", 0),
                entry.get("watch_time_avg", 0.0),
                entry.get("followers_gained", 0)
            ))
            return cur.lastrowid

    def get_analytics(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM analytics ORDER BY recorded_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cur.fetchall()]

    def get_dashboard_stats(self) -> Dict[str, int]:
        with self.get_connection() as conn:
            def scalar(query, params=()):
                cur = conn.execute(query, params)
                row = cur.fetchone()
                return row[0] if row else 0

            return {
                "discovered_topics": scalar("SELECT COUNT(*) FROM topics"),
                "verified_topics": scalar("SELECT COUNT(*) FROM topics WHERE status = 'VERIFIED'"),
                "approved_topics": scalar("SELECT COUNT(*) FROM topics WHERE status = 'APPROVED'"),
                "scripts_draft": scalar("SELECT COUNT(*) FROM scripts WHERE status = 'DRAFT'"),
                "scripts_approved": scalar("SELECT COUNT(*) FROM scripts WHERE status = 'APPROVED'"),
                "rendered_videos": scalar("SELECT COUNT(*) FROM production_jobs WHERE status = 'COMPLETED'"),
                "queued_videos": scalar("SELECT COUNT(*) FROM publishing_queue WHERE status = 'QUEUED'"),
                "published_videos": scalar("SELECT COUNT(*) FROM publishing_queue WHERE status = 'PUBLISHED'"),
                "total_media_assets": scalar("SELECT COUNT(*) FROM assets")
            }

    def record_oauth_state(self, nonce: str, provider: str = "instagram", created_at: Optional[float] = None, expires_at: Optional[float] = None) -> bool:
        """Stores a cryptographically random OAuth state nonce with expiration in SQLite."""
        c_at = created_at if created_at is not None else time.time()
        e_at = expires_at if expires_at is not None else (c_at + 600.0)
        with self.transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO oauth_states (nonce, provider, created_at, expires_at, consumed)
                VALUES (?, ?, ?, ?, 0)
                """,
                (nonce, provider, c_at, e_at),
            )
            return True

    def consume_oauth_state(self, nonce: str, provider: str = "instagram", max_age_seconds: int = 600) -> bool:
        """
        Atomically validates and consumes an OAuth state token.
        Guarantees single-use consumption and thread-safe replay protection.
        """
        now = time.time()
        min_created = now - max_age_seconds
        with self.transaction() as conn:
            cursor = conn.cursor()
            # Atomic update: only succeeds if nonce matches, provider matches, not consumed, and not expired
            cursor.execute(
                """
                UPDATE oauth_states 
                SET consumed = 1, consumed_at = ?
                WHERE nonce = ? 
                  AND provider = ? 
                  AND consumed = 0 
                  AND expires_at >= ?
                  AND created_at >= ?
                """,
                (now, nonce, provider, now, min_created),
            )
            consumed = cursor.rowcount > 0

            # Prune states older than 24 hours
            cursor.execute("DELETE FROM oauth_states WHERE expires_at < ?", (now - 86400,))
            return consumed


def get_db() -> Database:
    return Database()
