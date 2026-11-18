# SUPER.INTELLIGENCEEE — PHASE 4.2A.3 FACTUAL VERIFICATION

**Auditor:** Independent Scientific Fact-Checker & Research Auditor  
**Primary Source Document:** *"Unpacking the Compute Efficiency of Strong-to-Weak OPD against GRPO"* (arXiv:2611.08453, Salesforce AI Research & UIUC)  
**Verification Date:** November 7, 2026  

---

## 1. Primary Source Investigation & Core Architecture

The audited paper investigates the compute efficiency of On-Policy Distillation (OPD) compared to Group Relative Policy Optimization (GRPO) for post-training large reasoning language models.

### Mathematical Formulation
On-Policy Distillation minimizes the reverse-Kullback-Leibler (KL) divergence over rollouts generated on-policy by the student model:
$$\mathcal{L}_{\text{OPD}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(\cdot|x)} \left[ \sum_{t=1}^{|y|} D_{\text{KL}}\left(\pi_\theta(\cdot|x, y_{<t}) \;\Vert\; \pi_{\text{ref}}(\cdot|x, y_{<t})\right) \right]$$

Key algorithmic constraints verified:
1. **On-Policy Sampling:** Trajectories $y$ are sampled from the student policy $\pi_\theta$.
2. **Frozen Teacher:** Teacher policy $\pi_{\text{ref}}$ provides reference logit distributions at each token step $t$; teacher weights receive zero gradient updates.
3. **Dense Supervision:** KL divergence provides dense, per-token supervision rather than a single scalar sequence-level reward.

---

## 2. Forensic Audit of Primary Empirical Claims

### CLAIM 1: The 50× Compute Efficiency Ratio
*Prototype Statement:* `"When the teacher is the student's own checkpoint, OPD matches full GRPO accuracy on math benchmarks with 50x fewer distillation FLOPs than RL needed to reach that accuracy."`

- **Exact Experimental Setting in Paper:**
  - **Teacher Architecture:** "Self-GRPO Teacher" — specifically the student's own checkpoint saved at the end of GRPO training.
  - **Student Initialization:** Initialized from the pre-RL base model or early checkpoint.
  - **Benchmarks:** Math reasoning benchmarks (MATH-500 and AIME 2024).
  - **Measured Metric:** FLOPs expended during the *distillation stage only* to recover the teacher checkpoint's final benchmark accuracy, compared to the FLOPs required during direct GRPO reinforcement learning to reach that same accuracy.
- **What is Excluded:**
  - Does NOT include the FLOPs already expended to train the teacher checkpoint via GRPO.
  - Does NOT indicate a 50× inference latency acceleration.
  - Does NOT apply to arbitrary external teacher models.
- **Auditor Evaluation:** **VERIFIED WITH MANDATORY QUALIFICATION.**
  - The statement in Phase 4.2A.2 Directive 1 correctly scopes the claim to distillation FLOPs on a self-checkpoint.
  - *Editorial Observation:* As noted in Section 4.1 of the paper, single-domain self-distillation carries a practical redundancy (the practitioner already possesses the GRPO checkpoint). The true production value of this efficiency emerges in multi-teacher multi-domain distillation.

---

### CLAIM 2: External Teacher Underperformance vs Direct GRPO
*Prototype Statement:* `"Under the matched experimental settings studied, external-teacher distillation generally trails direct GRPO in accuracy per training FLOP."`

- **Exact Experimental Setting in Paper:**
  - **Teacher Architecture:** An external post-trained teacher (a model trained independently or with a different post-training recipe/family).
  - **Comparison:** Distilling into a target student via vanilla reverse-KL OPD versus training that student directly using GRPO at matched total training FLOP budgets.
  - **Paper Finding (Section 4.2 & Figure 4):** External-teacher OPD achieves lower accuracy per training FLOP across benchmarks compared to direct GRPO.
  - **Underlying Mechanism in Paper:** **Response-Length Inflation.** The paper discovers that when students distill from external teachers, they suffer from uncontrolled generation length expansion, wasting valuable FLOPs on verbose tokens that do not yield proportional accuracy improvements.
- **Auditor Evaluation:** **VERIFIED.**
  - The phrasing used in Phase 4.2A.2 strictly matches the paper's conclusion.
  - *Improvement Recommendation:* Sequence B and Sequence C attribute this deficit broadly to "policy distribution mismatch." Adding the specific term **"Response-Length Bloat / Inflation"** would significantly elevate the documentary's technical explanatory depth.

---

### CLAIM 3: Multi-Domain Consolidation & Total FLOP Savings
*Paper Evidence (Section 4.3 & Table 3):*
  - In a multi-task setting (e.g. Math + Code), training a single joint GRPO model is prone to cross-domain interference and high compute costs.
  - By training domain-specialist GRPO checkpoints independently, and then consolidating them into a unified student using **Multi-Teacher OPD**, the distillation phase costs only **5.2%** (2-domain mix) and **8.0%** (4-domain mix) of the specialist training FLOPs.
  - The combined pipeline achieves joint-GRPO performance with **42.0% fewer total FLOPs**.
- **Auditor Evaluation:** **OMITTED FROM PROTOTYPE VISUALS.**
  - While Claim 1 (50× distillation FLOPs) and Claim 2 (external teacher deficit) are prominently featured, the paper's actual positive engineering resolution—Multi-Teacher OPD saving 42% total FLOPs—is completely absent from the visual prototypes.
  - *Recommendation:* Sequence C should incorporate the 42% Multi-Teacher Consolidation breakthrough as the third actionable takeaway.

---

### CLAIM 4: The 3-Pillar Conceptual Efficiency Matrix
*Prototype Visual:* Direct GRPO vs Self-Teacher OPD vs External Teacher OPD.

- **Auditor Evaluation:** **FACTUALLY ACCURATE (NO FABRICATION DETECTED).**
  - Unlike Phase 4.2A.1, which fabricated continuous coordinate plots on unverified axes, the 3-pillar conceptual architecture in Phase 4.2A.2 faithfully represents the paper's categorical comparisons without drawing non-existent mathematical curves.
  - Stamping the matrix with `"CONCEPTUAL COMPARISON // LAB SETTING // NOT CONTINUOUS EMPIRICAL CURVE"` satisfies scientific transparency standards.

---

## 3. Claim-by-Claim Verification Ledger

| Claim ID | Proposition | Paper Source Passage | Verification Status | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **CLM-01** | OPD trains student on own rollouts with frozen teacher logits. | Section 3, Formulation | **VERIFIED** | 1.00 |
| **CLM-02** | 50× fewer distillation FLOPs to match self-checkpoint math accuracy. | Abstract & Section 4.1 | **VERIFIED (Scoped)** | 0.98 |
| **CLM-03** | External-teacher OPD underperforms direct GRPO in accuracy/FLOP. | Section 4.2 & Figure 4 | **VERIFIED** | 0.98 |
| **CLM-04** | Response-length inflation is primary failure mode of external OPD. | Section 4.2, Paragraph 3 | **VERIFIED (Missing in visual)** | 0.95 |
| **CLM-05** | Multi-teacher consolidation yields 42% total FLOP savings. | Section 4.3, Table 3 | **VERIFIED (Missing in visual)** | 0.95 |
| **CLM-06** | Research status: Academic preprint (arXiv:2611.08453). | Header & Metadata | **VERIFIED (Disclosed)** | 1.00 |

---

## 4. Scientific Sign-off

The factual representations in Phase 4.2A.2 are **100% compliant with primary source data**. No hallucinations or fabricated numerical data exist in the scripts or on-screen text.

To reach the standard of a world-class technology documentary, the visual narrative should be enriched in the next revision with the paper's two deepest insights:
1. Identifying **Response-Length Bloat** as the exact physical failure mechanism of external teachers.
2. Highlighting **Multi-Teacher OPD (42% Total FLOP Reduction)** as the true architectural breakthrough that solves single-domain redundancy.

