# SUPER.INTELLIGENCEEE — OWNER APPROVAL BAR POLICY
<!-- POLICY VERSION: 2.0 | OWNER CONTROLLED: IMMUTABLE BY AGENTS -->

## 1. Core Governance Invariant
> [!CRITICAL]
> **HUMAN EDITORIAL APPROVAL IS STRICTLY MANDATORY BEFORE PUBLISHING ANY CONTENT TO ANY PLATFORM.**
> Under no circumstances may any agent, worker, or automated playbook publish content, post comments, or distribute media without affirmative human authorization.

## 2. Automated vs. Gated Operations
| Operation Stage | Autonomy Level | Action Upon Completion |
|---|---|---|
| **Topic Discovery & RSS Collection** | Automated | Ingest into `topics` table |
| **Multi-Dimensional Opportunity Scoring** | Automated | Rank in `topics` table |
| **Script Generation & Storyboarding** | Automated | Save draft to `scripts` & `storyboards` |
| **Claim-Level Fact Checking** | Automated | Audit evidence; flag ungrounded metrics |
| **Audio Synthesis & Loudnorm** | Automated | Synthesize local WAV and normalize |
| **Visual Synthesis & Video Rendering** | Automated | Render 1080x1920 MP4 video draft |
| **Technical QA (FFprobe & Whisper)** | Automated | Validate codec, fps, duration, audio |
| **Submission to Approval Queue** | Automated | Transition job to `NEEDS_REVIEW` |
| **External Publishing (Instagram Reels)** | **GATED (Human Owner)** | Requires `status == 'APPROVED'` in `approvals` |
| **External Publishing (YouTube)** | **GATED (Human Owner)** | Requires `status == 'APPROVED'` in `approvals` |
| **Direct Messaging / Lead Responses** | **GATED (Human Owner)** | Outbound messages require human ok |
| **Financial / Credit Card Actions** | **GATED (Human Owner)** | Zero autonomy; strictly blocked |

## 3. Human Approval Criteria
The human owner / editor will evaluate items in `queue/needs-your-ok/` against:
1. **Factual Grounding:** Are all quantitative claims backed by primary source URLs?
2. **Audio/Video Sync:** Are on-screen headlines and spoken narration aligned?
3. **Brand Voice:** Does the narrative adhere to `owner/brand-voice.md`?
4. **Mobile Readability:** Are subtitles positioned above the 340px Instagram UI zone?

## 4. Urgent Escalation Triggers
The orchestrator must immediately dispatch high-priority notifications via Telegram / local alerts for:
- Activation of the Global Kill Switch (`owner/STOP`).
- OAuth token expiration or revoked platform permissions.
- Hard FFprobe validation failure across 2 consecutive render attempts.
- Detection of ungrounded or contradictory scientific/technical claims.

