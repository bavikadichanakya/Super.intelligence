# Critical Algorithmic Claim Audit: Vyral Content Skills vs. Official Engineering & Platform Realities

**Project:** SUPER.INTELLIGENCEEE  
**Phase:** 12 — Content Intelligence, Viral Pattern Analysis & Audience Growth Engine  
**Document:** `reports/phase12/VYRAL_SKILLS_CLAIM_AUDIT.md`  
**Scope:** Rigorous critical audit of algorithmic assertions in `vyralcontent/content-skills` across YouTube Shorts and Instagram Reels.

---

## 1. Audit Framework & Classification Standard

Every significant claim made in the installed Vyral skills has been audited against current official documentation from Google/YouTube, Meta/Instagram, and verified developer API schemas (YouTube Data API v3, Meta Graph API v21.0).

Claims are categorized under seven definitive standards:
1. `OFFICIALLY_VERIFIED`: Committed in official platform documentation, help centers, or API specifications.
2. `SUPPORTED_BY_PLATFORM_STATEMENT`: Publicly stated on the record by executive leaders (e.g., Adam Mosseri, YouTube Creator Insider, René Ritchie).
3. `THIRD_PARTY_RESEARCH`: Documented by independent data aggregators (e.g., Buffer, Hootsuite, Tubular Labs), but not a committed platform specification.
4. `CREATOR_HEURISTIC`: A practical rule-of-thumb or creative framework that functions well as creative guidance, but is not an immutable algorithm law.
5. `UNVERIFIED`: Speculative claims or folklore without empirical or official documentation.
6. `OUTDATED`: Formerly accurate claims that have been superseded by platform architectural updates.
7. `CONTRADICTED`: Claims directly refuted by current platform engineering, API behavior, or official policy.

---

## 2. Comprehensive Claim-by-Claim Audit Table

| # | Core Skill Claim | Claim Classification | Platform & Source Reference | Empirical Audit & Engineering Analysis |
| :- | :--- | :---: | :--- | :--- |
| **1** | **Fixed VVSA (Viewed vs Swiped Away) Thresholds**<br/>*"Under ~60% tends to flop. 70-90% tends to break out. 30/70 is dead."* | `CREATOR_HEURISTIC` | YouTube Analytics / Creator Insider | While YouTube Studio explicitly exposes *Viewed vs Swiped Away*, YouTube engineers confirm there is **no fixed global percentage threshold**. Required VVSA is relative to the topic category, competition in that specific niche bucket, and total audience addressability. A 62% VVSA on an ultra-niche quantum computing paper may expand, while a 75% VVSA on generic comedy may stall against stiffer competition. |
| **2** | **Fixed Average Percentage Viewed (APV) Benchmarks**<br/>*"~65% for <30s, ~50% for 30-60s, ~40-45% for 60s+."* | `CREATOR_HEURISTIC` | YouTube Creator Insider | YouTube emphasizes *Total Watch Time* and *Relative Audience Retention* against videos of similar length. Longer Shorts (e.g., 70-180s) generate vastly more absolute seconds of watch time per viewer; thus, demanding a flat 65% APV across all formats misdiagnoses high-depth educational documentaries. |
| **3** | **Claimed Initial Seeding Pool of Exactly 50–500 Viewers**<br/>*"A new Short tends to start with a test pool of roughly 50 to 500 viewers, ~70% non-subs."* | `UNVERIFIED` | None (Creator speculation) | YouTube has never published a fixed numerical seeding bucket. Initial impression allocation is dynamic, determined by upload classification, channel metadata relevance, active viewer session volume, and cold-start indexing. |
| **4** | **Instagram DM Shares Weight 3x to 5x More Than Likes**<br/>*"A DM share carries roughly 3 to 5 times the weight of a like."* | `SUPPORTED_BY_PLATFORM_STATEMENT` / `UNVERIFIED` (Exact Multiplier) | Adam Mosseri (IG Head), Meta Announcements | **Partially Verified:** Adam Mosseri publicly stated that *Sends per Reach* is the #1 signal prioritized for recommending content to non-followers, far above likes. **However, the specific "3x to 5x" numerical multiplier is an unverified creator heuristic.** Meta's ML ranking models use dynamic neural ranking (DLRM) where feature weights vary continuously by user and context. |
| **5** | **Hashtags Do Not Improve Instagram Reach (3–5 Niche Tags Max)**<br/>*"Hashtags are categorization, not a distribution multiplier. 30-tag walls do not help."* | `OFFICIALLY_VERIFIED` / `SUPPORTED_BY_PLATFORM_STATEMENT` | Instagram Creators Official Guidelines / Adam Mosseri | **Accurate.** Instagram Creators official documentation and Mosseri have explicitly confirmed that hashtags function as search/indexing categorizers rather than distribution multipliers. Piling on 30 generic tags triggers spam filtering. 3–5 specific niche keywords are the verified best practice. |
| **6** | **YouTube Shorts 15-Hashtag Hard Cap & `#Shorts` Tag**<br/>*"More than 15 total hashtags per video are ignored by YouTube."* | `OFFICIALLY_VERIFIED` | YouTube Help Center Policy on Hashtags | **Accurate.** YouTube policy explicitly states: *"If a video has more than 15 hashtags, we'll ignore all hashtags on that video."* Overuse may result in video removal under spam policies. `#Shorts` remains an official tag helping categorization. |
| **7** | **Trial Reels Require Exactly 1,000 Followers**<br/>*"The account is public and has at least about 1,000 followers (eligibility)."* | `CONTRADICTED` / `OUTDATED` | Meta Feature Rollouts (2024–2026) | **Contradicted.** Meta rolled out Trial Reels initially in select test regions and expanded it to professional creator accounts without a rigid 1,000 follower gate. Availability is controlled by account standing, region, and app version, not an absolute 1,000 follower cliff. |
| **8** | **Originality Demotions & Watermark Penalties**<br/>*"TikTok watermarks and low-originality reposts get demoted."* | `OFFICIALLY_VERIFIED` | Meta Recommendation Guidelines / YouTube Creator Policy | **Accurate.** Both Meta and YouTube have official recommendation guidelines explicitly stating that videos with third-party watermarks (e.g. TikTok logo) or aggregator reposts without significant transformation are ineligible for recommendation surfaces (Explore, Reels Tab, Shorts Feed). |
| **9** | **Daily Publishing Frequency Advice as Algorithm Necessity**<br/>*"Post 1 to 3 times a day to maintain algorithm momentum."* | `CONTRADICTED` | YouTube Creator Insider / Meta Creator Docs | **Refuted.** YouTube Creator Insider has repeatedly addressed this: the recommendation algorithm does not penalize channels for taking days off, nor does it reward spam publishing. Output quality and viewer satisfaction on individual videos govern distribution. |
| **10** | **Trending Audio Boost for Small Accounts**<br/>*"Small channels under 50k subs don't benefit from trending audio; original audio wins."* | `THIRD_PARTY_RESEARCH` / `CREATOR_HEURISTIC` | Independent creator analytics | While original, high-clarity voiceover is mandatory for technical documentaries, trending audio can provide categorical discovery in consumer niches. However, for deep technical AI explainers, audio licensing restrictions on Instagram Creator/Business accounts make commercial-safe original sound design the legally sound and brand-consistent choice. |
| **11** | **YouTube View Counting Updates (March 2025 & August 2026)**<br/>*"YouTube changed Shorts view counting; raw views != Engaged Views."* | `OFFICIALLY_VERIFIED` | YouTube Creator Updates & API documentation | **Accurate & Crucial.** YouTube officially updated Shorts view counting mechanics to combat botting and accidental feed scrolls. A view requires sustained engagement threshold (Engaged View). Raw impressions in feed are separate from Engaged Views. |
| **12** | **Algorithmic 'Shadowban' Claims**<br/>*"Underperforming videos are shadowbanned."* | `CONTRADICTED` | Instagram Transparency Center / YouTube Communications | **False.** Both platforms have repeatedly refuted the colloquial concept of an untracked, malicious "shadowban." Low reach is virtually always attributable to: (a) explicit Account Status non-recommendability flags, (b) privacy status (e.g., video marked private), (c) early swipe-away / low retention, or (d) lack of topic search demand. |

---

## 3. Core Architectural Takeaways for SUPER.INTELLIGENCEEE

1. **Never Hardcode Universal Percentage Benchmarks:**  
   The system must not reject or diagnose a video based on an arbitrary "60% VVSA" or "50% APV" rule. Instead, it must compute and compare against **our own account baselines** as historical data accumulates.

2. **Differentiate Exposure Failures from Creative Failures:**  
   Before diagnosing a video as having a "bad hook," the system must verify whether it was actually exposed to viewers (`shown_in_feed > 0` on YouTube, `reach > 0` on Instagram) and verify its public visibility setting.

3. **Sends-Driven Engineering for Instagram:**  
   Because Meta's ML ranking heavily weights non-follower distribution on *Sends per Reach*, technical scripts must package insights into shareable, high-utility containers (e.g., naming an architectural breakthrough, resolving a running industry debate) rather than begging for vanity likes.

4. **SEO & On-Screen Text Over Hashtag Stuffing:**  
   Captions and on-screen typography are OCR-indexed and vector-embedded by both YouTube and Meta. Clean, keyword-rich scripts with 3–5 targeted niche tags outperform spam tag blocks every time.
