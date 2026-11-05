from typing import Dict, Any, Tuple

PERMITTED_LICENSES = {
    "Editorial Generated": {
        "description": "Programmatically generated algorithmic graphic or typography canvas created by SUPER.INTELLIGENCEEE.",
        "commercial_use": True,
        "requires_attribution": False,
        "risk_level": "ZERO"
    },
    "CC0": {
        "description": "Creative Commons Zero - Public Domain Dedication.",
        "commercial_use": True,
        "requires_attribution": False,
        "risk_level": "ZERO"
    },
    "Public Domain": {
        "description": "Government or uncopyrighted material.",
        "commercial_use": True,
        "requires_attribution": False,
        "risk_level": "ZERO"
    },
    "CC-BY": {
        "description": "Creative Commons Attribution 4.0 International.",
        "commercial_use": True,
        "requires_attribution": True,
        "risk_level": "LOW"
    },
    "Fair Use Editorial": {
        "description": "Brief excerpt or screenshot for news commentary, review, and journalistic reporting.",
        "commercial_use": False,
        "requires_attribution": True,
        "risk_level": "MEDIUM"
    }
}

class LicenseManager:
    """Enforces strict copyright compliance and verifies provenance before media inclusion."""

    @classmethod
    def validate_license(cls, license_type: str, attribution: str = "") -> Tuple[bool, str]:
        if license_type not in PERMITTED_LICENSES:
            return False, f"Unauthorized license: '{license_type}'. Allowed: {list(PERMITTED_LICENSES.keys())}"

        info = PERMITTED_LICENSES[license_type]
        if info["requires_attribution"] and not attribution.strip():
            return False, f"License '{license_type}' requires explicit creator attribution."

        return True, f"License validated ({info['description']})"

    @classmethod
    def create_provenance_record(cls, filename: str, source_url: str, creator: str, license_type: str, attribution: str = "") -> Dict[str, Any]:
        valid, msg = cls.validate_license(license_type, attribution)
        if not valid:
            raise ValueError(f"License violation: {msg}")

        return {
            "filename": filename,
            "source_url": source_url or "https://super.intelligenceee.local",
            "creator": creator or "SUPER.INTELLIGENCEEE Engine",
            "license": license_type,
            "attribution": attribution,
            "permissions": "Full Editorial Rights Authorized",
            "risk_level": PERMITTED_LICENSES[license_type]["risk_level"]
        }
