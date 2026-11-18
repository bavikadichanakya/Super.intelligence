# SUPER.INTELLIGENCEEE // INSTAGRAM ACCOUNT AUDIT & BASELINE
**Baseline State, Professional Account Verification, and Initial Growth Metrics**
**Date:** 2026-11-16  
**Platform:** Instagram Professional (Meta Graph API v21.0 / Unified Login)  
**App ID:** `995939360234396`  
**Business ID:** `1765114544578811`  
**Configuration ID:** `1681040066712391`  
**Redirect URI:** `http://127.0.0.1:5000/oauth/instagram/callback`  

---

## 1. Authentication & Connection Status

- **Meta App Configuration:** `CONFIGURED` (Meta App ID, Business ID, and Configuration ID configured for Unified Login).
- **Authentication Method:** Meta Unified Login / Facebook Login for Business.
- **Live User Authorization Status:** `AWAITING_OPERATOR_AUTHORIZATION`
- **Reason:** In accordance with Meta security protocols, the account owner must complete authorization in the official Meta dialog via `http://127.0.0.1:5000/oauth/instagram/connect`.
- **Credential Storage:** Authenticated Fernet encryption at rest (`data/secure/instagram_token.enc`) using the shared master key (`data/secure/.master_key`).
- **Permissions Configured:**
  - `instagram_basic`
  - `instagram_content_publish`
  - `instagram_manage_insights`
  - `instagram_manage_comments`

---

## 2. Professional Account Performance Baseline

In strict accordance with the core directive (*"Do not invent missing analytics. If the accounts are new or have insufficient data, mark the baseline as INSUFFICIENT_DATA"*), historical baseline analytics are recorded as follows:

| Metric | Baseline Value | Audit Status | Source |
| :--- | :--- | :--- | :--- |
| **Followers** | `INSUFFICIENT_DATA` (Pending OAuth) | PENDING_FIRST_SYNC | Meta Graph API (`/{ig-user-id}`) |
| **Accounts Reached (30-day)** | `INSUFFICIENT_DATA` | PENDING_FIRST_SYNC | Instagram Insights API |
| **Non-Follower Reach %** | `INSUFFICIENT_DATA` | PENDING_FIRST_SYNC | Instagram Insights API |
| **Average Reel Watch Time** | `INSUFFICIENT_DATA` | PENDING_FIRST_SYNC | Instagram Insights API |
| **Reel Completion Rate** | `INSUFFICIENT_DATA` | PENDING_FIRST_SYNC | Instagram Insights API |
| **DM Sends / Shares** | `INSUFFICIENT_DATA` | PENDING_FIRST_SYNC | Instagram Insights API (Post Metrics) |
| **Saves & Bookmarks** | `INSUFFICIENT_DATA` | PENDING_FIRST_SYNC | Instagram Insights API |
| **Profile Visits Attributed** | `INSUFFICIENT_DATA` | PENDING_FIRST_SYNC | Instagram Insights API |
| **Follows Attributed to Content** | `INSUFFICIENT_DATA` | PENDING_FIRST_SYNC | Instagram Insights API |
| **Account Status / Recommendation Eligibility** | `INSUFFICIENT_DATA` (Assumed Eligible) | PENDING_VERIFICATION | Professional Dashboard |

---

## 3. Account Type & Publishing Eligibility Requirements

1. **Professional Account Mandate:**
   - Meta Graph API publishing requires an **Instagram Professional (Creator or Business) Account**. Personal Instagram accounts cannot publish via API.
   - If the operator's account is currently Personal, conversion to a Creator account is free, instant, and preserves all existing followers, posts, and settings, while unlocking API publishing and Insights.
2. **Business Portfolio Association:**
   - Under Meta Unified Login (`1681040066712391`), the Instagram account must be assigned as an Asset to the operator's Meta Business Portfolio (`1765114544578811`).
3. **Recommendation Guidelines Adherence:**
   - Account Status must remain clear of strikes, intellectual property violations, or community standard flags.

---

## 4. Initial Launch Target Benchmarks

Following the first publishing cycle, the following thresholds will be monitored:
- **Non-Follower Reach Ratio:** $\ge 60\%$ (indicates active algorithm discovery)
- **Shares (DM Sends) per 1k Views:** $\ge 15$
- **Saves per 1k Views:** $\ge 25$
- **Video Format:** 1080x1920, 60 fps, zero third-party watermarks
