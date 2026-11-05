import re
import random
from typing import Dict, Any, List

HOOK_PATTERNS = {
    "Breaking AI News": [
        "A major breakthrough in AI just dropped, and it changes how we work.",
        "Frontier AI labs just released something that shifts the entire industry.",
        "This new AI milestone just proved the next generation is arriving faster than expected."
    ],
    "New AI Models & Releases": [
        "Here is what happens when you combine extreme reasoning with raw scale.",
        "A brand new model architecture was just unveiled, and the benchmark numbers are wild.",
        "This AI release is quietly outperforming systems twice its size."
    ],
    "AI Tools & Workflows": [
        "This AI tool can eliminate hours of manual engineering in seconds.",
        "Stop doing this manually. A new AI workflow just automated the entire process.",
        "Here is the fastest way modern engineers are leveraging the latest AI release."
    ],
    "Cybersecurity & Threats": [
        "A critical vulnerability was just discovered in modern AI infrastructure.",
        "Researchers just exposed a major security flaw you need to understand.",
        "This security discovery proves autonomous systems need stronger defenses."
    ],
    "Emerging Technologies": [
        "This breakthrough feels like science fiction, but it is real and happening now.",
        "A massive leap in deep tech was just achieved in the lab.",
        "Here is the emerging technology that will define the next decade of computing."
    ],
    "Default": [
        "Here is the most important technology development you need to know today.",
        "This AI announcement is flying under the radar, but its impact is massive.",
        "Everything you need to know about today's biggest technology milestone."
    ]
}

class HookGenerator:
    """Generates high-retention, non-clickbait hooks for 30-45 second technology Reels."""

    @classmethod
    def generate_hook(cls, title: str, category: str, style: str = "balanced") -> str:
        # Extract key subject from title
        clean_title = re.sub(r'^(new|how to|why|what is)\s+', '', title.strip(), flags=re.IGNORECASE)
        # Shorten subject to a punchy phrase
        words = clean_title.split()
        subject = " ".join(words[:6]) if len(words) > 6 else clean_title

        options = HOOK_PATTERNS.get(category, HOOK_PATTERNS["Default"])
        base_hook = random.choice(options)

        # Contextualize with the subject
        if "Artificial Intelligence News" in category or "New AI Models" in category:
            return f"{base_hook} Here is what you need to know about {subject}."
        elif "Cybersecurity" in category:
            return f"Security alert: {subject}. Here is the breakdown."
        else:
            return f"{base_hook} Let's break down {subject}."
