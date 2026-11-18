"""
SUPER.INTELLIGENCEEE — Phase 4.3.3 Light-First Cinematic Palette
Defines the authoritative editorial color scheme for technical documentaries.
Replaces dark dashboard styling with warm ivory, soft white, deep obsidian typography,
and crisp technical accents.
"""

from typing import Tuple

# Primary Backgrounds
BG_WARM_IVORY: Tuple[int, int, int] = (250, 247, 242)      # #FAF7F2
BG_SOFT_WHITE: Tuple[int, int, int] = (255, 255, 255)      # #FFFFFF
BG_LIGHT_NEUTRAL: Tuple[int, int, int] = (241, 245, 249)   # #F1F5F9 (slate-50)
BG_SURFACE_CARD: Tuple[int, int, int] = (255, 255, 255)    # #FFFFFF pure white card
BG_SURFACE_SUBTLE: Tuple[int, int, int] = (248, 250, 252)  # #F8FAFC (slate-50)

# Typography
TEXT_OBSIDIAN: Tuple[int, int, int] = (15, 23, 42)         # #0F172A (slate-900)
TEXT_SLATE: Tuple[int, int, int] = (71, 85, 105)           # #475569 (slate-600)
TEXT_MUTED: Tuple[int, int, int] = (148, 163, 184)         # #94A3B8 (slate-400)
TEXT_INVERSE_WHITE: Tuple[int, int, int] = (255, 255, 255) # For dark callout badges

# Accent Colors
ACCENT_TECH_BLUE: Tuple[int, int, int] = (2, 132, 199)     # #0284C7 (sky-600)
ACCENT_TECH_BLUE_LIGHT: Tuple[int, int, int] = (224, 242, 254) # #E0F2FE (sky-100)
ACCENT_EMERALD: Tuple[int, int, int] = (5, 150, 105)       # #059669 (emerald-600)
ACCENT_EMERALD_LIGHT: Tuple[int, int, int] = (209, 250, 229) # #D1FAE5 (emerald-100)
ACCENT_AMBER: Tuple[int, int, int] = (217, 119, 6)         # #D97706 (amber-600)
ACCENT_AMBER_LIGHT: Tuple[int, int, int] = (254, 243, 199) # #FEF3C7 (amber-100)
ACCENT_MUTED_RED: Tuple[int, int, int] = (220, 38, 38)     # #DC2626 (red-600)
ACCENT_MUTED_RED_LIGHT: Tuple[int, int, int] = (254, 226, 226) # #FEE2E2 (red-100)
ACCENT_INDIGO_SILICON: Tuple[int, int, int] = (79, 70, 229) # #4F46E5 (indigo-600)

# Structural Borders & Dividers
BORDER_LIGHT: Tuple[int, int, int] = (226, 232, 240)       # #E2E8F0 (slate-200)
BORDER_STRONG: Tuple[int, int, int] = (203, 213, 225)      # #CBD5E1 (slate-300)
GRID_LINE: Tuple[int, int, int] = (235, 238, 242)          # Subtle architectural grid
