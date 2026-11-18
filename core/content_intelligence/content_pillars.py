"""
Content Pillars Architecture Module
Defines the 4 core content pillars of SUPER.INTELLIGENCEEE.
Prevents channel fragmentation and establishes authority in specialized technology niches.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ContentPillar:
    pillar_id: str
    name: str
    target_audience: str
    audience_problem: str
    subtopics: List[str]
    preferred_formats: List[str]
    example_hooks: List[str]
    potential_series: List[str]
    shareability_score: float  # 0.0 - 1.0 (How naturally it triggers DM sends)
    educational_value: float   # 0.0 - 1.0 (Density of genuine knowledge)
    search_demand: str         # "High", "Medium", "Evergreen High"
    relevance_rationale: str


class ContentPillarsManager:
    """Manages channel pillars, topic routing, and pillar distribution balancing."""

    def __init__(self):
        self.pillars: Dict[str, ContentPillar] = self._init_pillars()

    def _init_pillars(self) -> Dict[str, ContentPillar]:
        return {
            "open_frontier": ContentPillar(
                pillar_id="open_frontier",
                name="The Open Frontier (Breakthrough Repos & Open Weights)",
                target_audience="Developers, open-source builders, AI practitioners.",
                audience_problem=(
                    "Proprietary AI is expensive and walled off. Builders need to know which open-source "
                    "models and GitHub repos can replace multi-million-dollar closed systems."
                ),
                subtopics=[
                    "DeepSeek-R1 / V3 reasoning architectures",
                    "BitNet 1-bit LLMs (b1.58)",
                    "Qwen 2.5 / Kimi K3 engineering",
                    "FlashAttention-3 Hopper asynchronous kernels",
                    "Local inference frameworks (Ollama, vLLM, llama.cpp)",
                ],
                preferred_formats=[
                    "Interactive Terminal Code Walkthrough",
                    "GitHub Repo Breakdown & Star Milestone",
                    "Benchmark Side-by-Side Showdown",
                ],
                example_hooks=[
                    "Silicon Valley spent $100M on human reasoning data. This open repo just beat them with pure math.",
                    "This single GitHub repository dropped GPU memory consumption by 93%. Here is the exact math.",
                    "Why everyone is running DeepSeek-R1 locally on M-series MacBooks instead of paying cloud API fees.",
                ],
                potential_series=[
                    "Repo Spotlight: 100k Star Open AI",
                    "Sovereign AI: Run It on Your Laptop",
                    "Architectural Autopsy",
                ],
                shareability_score=0.95,
                educational_value=0.92,
                search_demand="Evergreen High",
                relevance_rationale="Core anchor of SUPER.INTELLIGENCEEE. Delivers direct utility to engineers.",
            ),
            "autonomous_systems": ContentPillar(
                pillar_id="autonomous_systems",
                name="Autonomous Systems & Agentic Workflows",
                target_audience="Software engineers, automation builders, technical founders.",
                audience_problem=(
                    "How do we move from simple chatbot prompts to autonomous multi-agent systems "
                    "that browse the web, write clean code, and execute complex workflows without hallucinating?"
                ),
                subtopics=[
                    "Browser-Use & Web Automation Agents",
                    "Manus / Open-Manus multi-agent coordination",
                    "MCP (Model Context Protocol) tool integration",
                    "Self-correcting code execution loops",
                    "Deterministic evaluation & sandboxing",
                ],
                preferred_formats=[
                    "Live Screen Demonstration",
                    "Architecture Flowchart & Decision Tree",
                    "Autonomous Agent Failure & Healing",
                ],
                example_hooks=[
                    "This open-source AI agent can browse the live web, buy airline tickets, and solve captchas autonomously.",
                    "Stop building chat bots. This 5-stage agent architecture actually writes and debugs production code.",
                    "Anthropic's Model Context Protocol just unified how AI agents connect to local tools. Here is why it matters.",
                ],
                potential_series=[
                    "Agent Architecture Decoded",
                    "Building Autonomous Workflows",
                    "MCP Deep Dive",
                ],
                shareability_score=0.88,
                educational_value=0.90,
                search_demand="High",
                relevance_rationale="Aligns directly with modern developer trends and autonomous coding workflows.",
            ),
            "hardware_physics": ContentPillar(
                pillar_id="hardware_physics",
                name="Deep Compute & Semiconductor Physics",
                target_audience="Hardware enthusiasts, engineers, students, technology purists.",
                audience_problem=(
                    "AI scaling is hitting physical power and memory walls. Viewers want to understand the "
                    "physical hardware: quantum chips, HBM3e memory, wafer-scale engines, and photonic compute."
                ),
                subtopics=[
                    "Quantum error correction (Google Willow below-threshold milestone)",
                    "High-Bandwidth Memory (HBM3e) and the memory bandwidth wall",
                    "Wafer-scale compute (Cerebras WSE-3)",
                    "Sub-1nm lithography & GAAFET transistors (TSMC A16, Intel 14A)",
                    "Optical & Photonic neuromorphic computing",
                ],
                preferred_formats=[
                    "3D Architectural Drafting & Exploded Hardware View",
                    "Physical Cryostat & Dilution Refrigerator Telemetry",
                    "Physical Scaling Limit Infographics",
                ],
                example_hooks=[
                    "This golden chandelier is kept at 10 millikelvin—colder than deep space—just to stabilize 105 qubits.",
                    "The GPU memory crisis is not a software problem. It is a physical copper wire bottleneck.",
                    "How Cerebras built a single computer chip the size of an entire dinner plate.",
                ],
                potential_series=[
                    "Quantum Frontier",
                    "Hardware at the Physical Limit",
                    "The Semiconductor War",
                ],
                shareability_score=0.85,
                educational_value=0.98,
                search_demand="Evergreen High",
                relevance_rationale="Provides awe-inspiring scientific depth and high visual production prestige.",
            ),
            "systems_security": ContentPillar(
                pillar_id="systems_security",
                name="Systems Security, eBPF & AI Jailbreaks",
                target_audience="Security researchers, sysadmins, DevOps engineers, hackers.",
                audience_problem=(
                    "How do modern systems protect against kernel-level zero-days, eBPF exploitation, "
                    "and LLM indirect prompt injection attacks?"
                ),
                subtopics=[
                    "eBPF kernel tracing and verifier exploits",
                    "Adversarial LLM attacks & ASCII art jailbreaks",
                    "Supply chain attacks in Python/npm packages",
                    "Memory-safe languages (Rust in Linux kernel)",
                    "Hardware side-channel vulnerabilities (Spectre, Rowhammer)",
                ],
                preferred_formats=[
                    "Terminal Disassembly & Hex Dump",
                    "Attack Vector Exploit Reproduction",
                    "Security Patch Forensic Breakdown",
                ],
                example_hooks=[
                    "A single whitespace bug in the Linux kernel eBPF verifier bypassed root security entirely.",
                    "Why AI models can be tricked into revealing API keys using simple ASCII art.",
                    "This microscopic electrical vibration can read passwords directly off a CPU.",
                ],
                potential_series=[
                    "Exploit Forensics",
                    "Breaking the Kernel",
                    "AI Red Teaming",
                ],
                shareability_score=0.92,
                educational_value=0.94,
                search_demand="High",
                relevance_rationale="High-stakes educational value that engineers immediately bookmark and share.",
            ),
        }

    def get_pillar(self, pillar_id: str) -> Optional[ContentPillar]:
        return self.pillars.get(pillar_id)

    def route_topic_to_pillar(self, topic: str, keywords: List[str]) -> ContentPillar:
        """Determines best-matching pillar based on topic semantic tags."""
        t_lower = (topic + " " + " ".join(keywords)).lower()
        if any(w in t_lower for w in ["quantum", "qubit", "hardware", "chip", "semiconductor", "tsmc", "hbm"]):
            return self.pillars["hardware_physics"]
        if any(w in t_lower for w in ["agent", "browser", "manus", "workflow", "mcp", "scrape"]):
            return self.pillars["autonomous_systems"]
        if any(w in t_lower for w in ["security", "exploit", "ebpf", "kernel", "jailbreak", "cve"]):
            return self.pillars["systems_security"]
        return self.pillars["open_frontier"]
