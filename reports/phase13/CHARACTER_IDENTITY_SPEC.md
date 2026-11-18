# CHARACTER IDENTITY SPECIFICATION — PHASE 13
**Project:** SUPER.INTELLIGENCEEE  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Execution Timestamp:** 2026-11-17T17:22:00+05:30  
**Canonical Reference File:** `character.me.png`  
**Asset Directory:** `assets/character/`  
**Host Working Identifier:** Kavi (Provisional working choice for engineering integration)

---

## 1. OFFICIAL VISUAL IDENTITY SUMMARY

The official visual identity of the recurring documentary host for SUPER.INTELLIGENCEEE is defined by the canonical master asset `character.me.png`.

The visual style is a **premium stylized vector illustration with dimensional enamel pin aesthetic**, characterized by bold dark metallic outer contour lines, refined inner specular highlights, warm cel-shaded gradient tones, and an intelligent, friendly human expression.

```
+--------------------------------------------------------------------------+
|                       CANONICAL IDENTITY CONTRACT                         |
|                                                                          |
|  * Hair:         Curly, voluminous dark black locks with warm rim-light  |
|  * Eyewear:      Prominent dark-framed rectangular glasses (dark acetate)|
|  * Eyes:         Deep expressive brown, warm catchlights, curious gaze   |
|  * Facial Hair:  Neatly groomed full beard & moustache framing the jaw   |
|  * Wardrobe:     Charcoal-grey technical jacket with warm safety orange  |
|                  detailing along collar, shoulders, and zipper seams     |
|  * Signature:    Spiral-bound technical field notebook & wooden pencil   |
|  * Persona:      Lead Engineering Investigator & Documentary Host        |
|  * Voice Link:   Kokoro-82M neural TTS ('am_liam', General American)     |
+--------------------------------------------------------------------------+
```

---

## 2. MACHINE-READABLE SPECIFICATION OVERVIEW

The full specification is stored in `assets/character/character_profile.json`.

### A. Working Identity & Provisional Name
- **Provisional Name:** `Kavi` (Documented working choice. Does not replace or override future brand revisions).
- **Official On-Screen Title:** Host & Lead Technical Investigator.
- **Editorial Brand:** SUPER.INTELLIGENCEEE ("Understand What's Next").

### B. Defining Physical Traits & Constraints
1. **Curly Dark Black Hair:**
   - Voluminous curls arranged in distinct stylized locks.
   - Warm specular highlights along the outer rim.
   - **Constraint:** Texture must remain curly/wavy; never flatten, straighten, or recolor.
2. **Rectangular Eyewear:**
   - Heavy dark-framed rectangular acetate frames with slightly rounded corners.
   - Distinct corner rivets/hinges in metallic tone.
   - **Constraint:** Eyewear is permanent. The host must NEVER be depicted without glasses.
3. **Facial Hair & Structure:**
   - Well-groomed full beard and moustache following the jawline and chin contour.
   - Friendly, confident, slight asymmetrical smile.
   - Warm golden-brown/olive complexion (`#C28966`).
   - **Constraint:** Never remove beard, shave moustache, or alter facial bone structure.
4. **Technical Outerwear:**
   - Matte charcoal-grey technical jacket (`#2C2F33`) designed for clean engineering aesthetics.
   - Safety orange detailing (`#FF6B00` / `#F97316`) on collar edges, shoulder seams, and zipper track.
   - Black crew-neck undershirt (`#141414`).
   - **Constraint:** Never swap clothing for suits, casual hoodies, or fantasy garments.
5. **Signature Field Tools:**
   - Spiral-bound technical notebook (silver metal wire coil, tan/cream sheets).
   - Sharpened wooden drafting pencil held ready to annotate technical findings.

---

## 3. COLOR PALETTE DIRECTORY

| Color Component | Hex Code | RGB Values | Usage |
|---|---|---|---|
| **Jacket Base Charcoal** | `#2C2F33` | `(44, 47, 51)` | Primary jacket fabric |
| **Safety Orange Accent** | `#FF6B00` | `(255, 107, 0)` | Collar piping, zipper accents, shoulder stripes |
| **Metallic Outer Rim** | `#3C3229` | `(60, 50, 41)` | Outlines, glasses acetate frames, enamel border |
| **Inner Specular Silver** | `#E2DDD9` | `(226, 221, 217)` | Metallic bevel reflection, wire binding |
| **Complexion Base** | `#C28966` | `(194, 137, 102)` | Face, ears, neck, hands |
| **Hair & Beard Dark** | `#191412` | `(25, 20, 18)` | Hair curls, beard fill, pupil centers |
| **Eye Sclera White** | `#F8F9FA` | `(248, 249, 250)` | Eye whites, specular catchlights |
| **Notebook Cover/Pages**| `#A39684` | `(163, 150, 132)` | Field notebook paper block |

---

## 4. EDITORIAL ROLE & APPEARANCE RULES

The host is an **investigative guide**, not a decorative mascot or distracting cartoon.

### Where the Host Appears:
- **A. Opening Hook (Seconds 0.0 – 6.0):** Presenting the core paradox, breakthrough metric, or technological mystery directly to the viewer.
- **B. Investigation (Seconds 6.0 – 16.0):** Observing a realistic physical silicon processor, chip die, or robotics system and pointing out architectural features.
- **C. Mechanism Explanation (Seconds 16.0 – 28.0):** Anchored in a supporting lower corner (e.g. `lower_right`) while the primary screen real-estate is given to clean, unoccluded technical diagrams and dataflows.
- **D. Closing Takeaway (Seconds 30.0 – 38.0):** Delivering a concise, thoughtful conclusion and audience callout.

### Prohibited Usages:
1. **Never Occlude Technical Evidence:** The character must never cover semiconductor layouts, benchmark charts, or code snippets.
2. **Never Overlap Captions:** Character coordinates are strictly banned from entering the subtitle zone (`y = 1640 .. 1820`).
3. **No Decorative Filler:** The character appears only when his presence clarifies the viewer's learning journey. When a schematic is self-explanatory, the host steps off-screen.
