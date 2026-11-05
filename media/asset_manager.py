from pathlib import Path
from typing import List, Dict, Any, Optional

from core.database import get_db
from core.logger import get_logger
from core.config_manager import get_config
from media.license_manager import LicenseManager
from media.media_validator import MediaValidator

logger = get_logger("AssetManager")

class AssetManager:
    """Manages local media files, licensing provenance, and asset registry queries."""

    def __init__(self):
        self.db = get_db()
        self.config = get_config()
        self.assets_dir = self.config.resolve_path(self.config.get("paths.assets_dir", "assets"))

    def register_asset(self, file_path: str, asset_type: str, license_type: str = "Editorial Generated", source_url: str = "", creator: str = "SUPER.INTELLIGENCEEE", attribution: str = "") -> Optional[int]:
        p = Path(file_path).resolve()
        if not p.exists():
            logger.error(f"Cannot register missing asset: {p}")
            return None

        width, height, duration = 0, 0, 0.0
        if asset_type == "image":
            valid, _, meta = MediaValidator.validate_image(str(p))
            if valid:
                width = meta.get("width", 0)
                height = meta.get("height", 0)
        elif asset_type == "video":
            valid, _, meta = MediaValidator.validate_video(str(p))
            if valid:
                width = meta.get("width", 0)
                height = meta.get("height", 0)
                duration = meta.get("duration", 0.0)

        prov = LicenseManager.create_provenance_record(
            filename=p.name,
            source_url=source_url,
            creator=creator,
            license_type=license_type,
            attribution=attribution
        )

        record = {
            "filename": p.name,
            "file_path": str(p),
            "asset_type": asset_type,
            "source_url": prov["source_url"],
            "creator": prov["creator"],
            "license": prov["license"],
            "attribution": prov["attribution"],
            "permissions": prov["permissions"],
            "width": width,
            "height": height,
            "duration": duration
        }

        asset_id = self.db.register_media_asset(record)
        logger.info(f"Registered media asset ID {asset_id}: {p.name} ({asset_type}) [{license_type}]")
        return asset_id

    def list_assets(self, asset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.db.get_media_assets(asset_type)

    def scan_default_assets(self):
        """Scans the assets directory and registers any unregistered local media files."""
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
            for f in self.assets_dir.rglob(ext):
                self.register_asset(str(f), "image", "Editorial Generated")
        for ext in ("*.mp4", "*.mov"):
            for f in self.assets_dir.rglob(ext):
                self.register_asset(str(f), "video", "Editorial Generated")
        for ext in ("*.mp3", "*.wav"):
            for f in self.assets_dir.rglob(ext):
                self.register_asset(str(f), "audio", "CC0", creator="Open Source Archive")
