# PHASE 4.3.3.1 — SCIENTIFIC EVIDENCE & CLAIM AUDIT

**Project:** SUPER.INTELLIGENCEEE  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Phase:** 4.3.3.1  
**Paper Evaluated:** *Metal Sandbox: Isolated Execution and Command Scheduling for GPU Coding Agents on Apple Silicon*  
**arXiv Identifier:** `arXiv:2611.17294v1` (#499)  
**Publishing Venue:** arXiv.org Computer Science (Distributed, Parallel, and Cluster Computing)  
**Production Job:** Job #57 | **Approval Record:** Approval #27  
**Overall Evidence Audit Result:** **PASSED (100% GROUNDED)**

---

## 1. Itemized Empirical Metric Audit

Every numerical metric, hardware claim, and benchmark percentage displayed on-screen or uttered in narration has been forensically verified against primary source materials:

| Metric / Parameter | Displayed Value | Metric Classification | Primary Source Citation | Exact Section / Table | Testbed Condition / Configuration |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Command Throughput Gain** | **1.68× – 2.05×** | `MEASURED_HARDWARE` | arXiv:2611.17294v1 | Section 4 (Empirical Evaluation), Fig. 5 | 4× Apple Mac mini M4 nodes under concentrated agent command demand |
| **Batch Elapsed Time Reduction** | **-22.3%** | `MEASURED_TRACE_REPLAY` | arXiv:2611.17294v1 | Section 4.2 (Batch Scheduling Performance), Table 2 | Trace replay of 16 static agent execution sessions under dynamic scheduling |
| **Tool Waiting Latency Reduction**| **-18.8%** | `MEASURED_TRACE_REPLAY` | arXiv:2611.17294v1 | Section 4.2 (Latency Profiling), Table 2 | Mean reduction in agent idle waiting time via cross-node task migration |
| **Sustained Replay Gain** | **2.14×** | `ESTIMATED_TRACE_MODEL`| arXiv:2611.17294v1 | Section 4.3 (Scaling Analysis), Text Paragraph 3 | Estimated sustained throughput gain for 4 sessions/node vs 1 (trace assumption) |
| **Mac mini CPU Configuration** | **10-Core (4P + 6E)** | `OFFICIAL_HARDWARE_SPEC`| Apple Inc. | Apple Mac mini (2024) Tech Specs | 4 Performance cores + 6 Efficiency cores (Standard M4 base chip) |
| **Mac mini GPU Configuration** | **10-Core GPU** | `OFFICIAL_HARDWARE_SPEC`| Apple Inc. | Apple Mac mini (2024) Tech Specs | 10-core integrated GPU with hardware-accelerated ray tracing |
| **Unified Memory Capacity** | **16 GB Unified Memory**| `OFFICIAL_HARDWARE_SPEC`| Apple Inc. | Apple Mac mini (2024) Tech Specs | 16GB standard base memory configuration |
| **Memory Bandwidth** | **120 GB/s** | `OFFICIAL_HARDWARE_SPEC`| Apple Inc. | Apple Mac mini (2024) Tech Specs | 120 GB/s unified memory subsystem bandwidth |
| **Cluster Node Count** | **4 Nodes** | `EMPIRICAL_TESTBED` | arXiv:2611.17294v1 | Section 3.1 (Testbed Architecture) | 4 interconnected Apple Mac mini computers on local Gigabit Ethernet |

---

## 2. Purge of Unsupported Illustrative Numbers

In Phase 4.3.3, illustrative duty cycle numbers (`38% -> 78%`) were used on the comparison cards. While conceptually illustrative of increased silicon occupancy, these specific percentage figures were not reported in arXiv:2611.17294v1.

In Phase 4.3.3.1:
1. **The numbers `38%` and `78%` have been 100% removed** from all graphics, animations, code strings, contracts, and narration.
2. The comparison visualizer in Scene 1 (Dual Timeline) explicitly presents the mechanism as a **`Conceptual Agent Rollout Model`**, illustrating how LLM inference pauses and tool calls leave accelerators idle without quoting unmeasured percentages.
3. The empirical visualizer in Scene 3 presents strictly the verified numbers: `1.68x - 2.05x`, `-22.3%`, `-18.8%`, and `2.14x`.

---

## 3. Calibration of Security & Isolation Claims

In Phase 4.3.3, the security panel contained absolute, unqualified claims ("Zero memory bleed", "100% isolation", "Zero credential leakage", "Guaranteed secure execution"). 

In computer security and systems engineering, such absolute claims are unprovable and technically inaccurate when evaluating shared hardware accelerators.

In Phase 4.3.3.1, all security assertions were calibrated against the actual evaluated properties in arXiv:2611.17294v1:

```
===================================================================================================
PREVIOUS UNQUALIFIED CLAIM         CALIBRATED GROUNDED REPLACEMENT             EVIDENCE BASIS
===================================================================================================
"100% isolation"                   "Restricted per-instance filesystem boundary" Process chroot/sandbox confinement
"Zero memory bleed"                "Process confined · no directory traversal"   Restricted path rules enforced
"Zero credential leakage"          "Restricted host paths (/System, keys)"       Host directories inaccessible
"Guaranteed secure execution"      "Evaluated Architectural Property"            Controlled experimental testbed
"Isolated accelerator memory"      "Metal shared via scheduling; files isolated" Distinguishes compute from storage
===================================================================================================
```

Unit test `test_10_evidence_traceability_and_calibration` verified that:
- `"Zero memory bleed"`: **ABSENT**
- `"100% isolation"`: **ABSENT**
- `"Zero credential leakage"`: **ABSENT**
- `"Guaranteed secure execution"`: **ABSENT**
- `"completely unhackable"`: **ABSENT**

---

## 4. Dossier Claim Grounding Ledger

All storyboard scenes and evidence items map deterministically to verified Research Dossier entries:

```json
{
  "claim_001": {
    "scene": "scene_01",
    "text": "Four interconnected Apple Mac mini M4 nodes provide local accelerator capacity, but single-tenant agent rollouts leave silicon idle during sequential decision cycles.",
    "status": "VERIFIED",
    "publisher": "arXiv.org",
    "url": "https://arxiv.org/abs/2611.17294v1"
  },
  "claim_002": {
    "scene": "scene_02",
    "text": "Metal Sandbox enforces per-instance filesystem boundaries while scheduling commands onto shared queues, isolating agent workspace files while utilizing local GPU pipelines.",
    "status": "VERIFIED",
    "publisher": "arXiv.org",
    "url": "https://arxiv.org/abs/2611.17294v1"
  },
  "claim_003": {
    "scene": "scene_03",
    "text": "Dynamic scheduling across four M4 nodes achieves 1.68x to 2.05x throughput gains and reduces batch elapsed time by 22.3% and tool waiting latency by 18.8% on trace replay.",
    "status": "VERIFIED",
    "publisher": "arXiv.org",
    "url": "https://arxiv.org/abs/2611.17294v1"
  }
}
```

- **Total Claims Evaluated:** 3  
- **Claims Verified:** 3 (100%)  
- **Unverified Claims:** 0 (0%)  

---

## 5. Evidence Audit Verdict

All factual claims, specifications, and performance numbers are **100% grounded in verified technical evidence**. No unsupported claims or absolute guarantees remain in the production output.
