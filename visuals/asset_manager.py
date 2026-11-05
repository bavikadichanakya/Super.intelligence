"""
SUPER.INTELLIGENCEEE — Visual Asset Manager Module
Catalogs, validates, and manages media assets with strict provenance tracking in SQLite.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_config
from core.database import Database
from core.provenance import LegalProvenanceRecord, LicenseType

logger = logging.getLogger("super_intelligence.asset_manager")


class VisualAssetManager:
    """Manages visual assets, thumbnails, and background media."""

    def __init__(self, db: Optional[Database] = None, config=None):
        self.config = config or get_config()
        self.db = db or Database()
        self.images_dir = self.config.resolve_path(self.config.get("paths.images_dir", "assets/images"))
        self.video_dir = self.config.resolve_path(self.config.get("paths.video_dir", "assets/video"))
        self.brand_dir = self.config.resolve_path("assets/brand")
        self.fonts_dir = self.config.resolve_path(self.config.get("paths.fonts_dir", "assets/fonts"))

        for d in [self.images_dir, self.video_dir, self.brand_dir, self.fonts_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def compute_file_hash(self, file_path: Path | str) -> str:
        """Calculates SHA256 checksum of an asset file."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def register_asset(
        self,
        file_path: Path | str,
        asset_type: str,
        name: str,
        license_type: LicenseType = LicenseType.EDITORIAL_GENERATED,
        source_url: Optional[str] = None,
        author: str = "SUPER.INTELLIGENCEEE",
        tags: Optional[List[str]] = None,
    ) -> int:
        """Registers a visual asset into the database with legal provenance."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Asset file does not exist: {path}")

        file_hash = self.compute_file_hash(path)
        file_size = path.stat().st_size

        prov = LegalProvenanceRecord(
            license_type=license_type,
            source_url=source_url,
            author_or_creator=author,
            verification_notes=f"Auto-registered by AssetManager. Type: {asset_type}",
        )

        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO assets (
                    name, asset_type, file_path, file_hash, file_size_bytes,
                    license_type, source_url, author, tags, is_verified
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    name,
                    asset_type,
                    str(path.resolve()),
                    file_hash,
                    file_size,
                    prov.license_type.value,
                    prov.source_url,
                    prov.author_or_creator,
                    ",".join(tags or []),
                ),
            )
            asset_id = cursor.lastrowid
            logger.info(f"Registered asset #{asset_id}: '{name}' ({asset_type}) at {path.name}")
            return asset_id

    def list_assets(self, asset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists registered assets from SQLite."""
        query = "SELECT * FROM assets"
        params = []
        if asset_type:
            query += " WHERE asset_type = ?"
            params.append(asset_type)
        query += " ORDER BY id DESC"

        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

