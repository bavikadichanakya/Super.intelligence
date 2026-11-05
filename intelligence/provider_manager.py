import os
import json
import requests
from typing import Dict, Any, Optional

from core.logger import get_logger
from intelligence.fallback_templates import FallbackTemplates

logger = get_logger("ProviderManager")

class AIProvider:
    """Abstract base class for script generation providers."""
    def generate(self, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

class GeminiProvider(AIProvider):
    """Optional free-tier Gemini API provider."""
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    def generate(self, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.api_key:
            return None
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            prompt = f"""
            You are a senior tech journalist for SUPER.INTELLIGENCEEE.
            Write a factual 30-45s Instagram Reel script (~80-100 words) from this technology news story:
            Title: {article.get('title')}
            Publisher: {article.get('publisher')}
            Summary: {article.get('summary')}

            Return ONLY raw JSON with keys:
            - title (string)
            - hook (punchy 12-16 words)
            - context (14-18 words)
            - development (16-20 words)
            - explanation (14-18 words)
            - implications (12-16 words)
            - limitations (10-14 words)
            - takeaway (8-12 words)
            """
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4, "maxOutputTokens": 800}
            }
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                # Clean json codeblocks
                clean_json = text.strip().replace("```json", "").replace("```", "").strip()
                parsed = json.loads(clean_json)
                # Combine into full narration and scenes
                parsed["publisher"] = article.get("publisher")
                parsed["source_url"] = article.get("url")
                parsed["category"] = article.get("category")
                full_narration = " ".join([
                    parsed["hook"], parsed["context"], parsed["development"],
                    parsed["explanation"], parsed["implications"],
                    parsed["limitations"], parsed["takeaway"]
                ])
                parsed["full_narration"] = full_narration
                parsed["word_count"] = len(full_narration.split())
                parsed["est_duration"] = round(parsed["word_count"] / 2.6, 1)
                return parsed
        except Exception as e:
            logger.warning(f"Gemini API request failed, falling back: {e}")
        return None

class OllamaProvider(AIProvider):
    """Optional local Ollama provider (if running locally on user's machine)."""
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = os.getenv("OLLAMA_HOST", host)

    def generate(self, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            res = requests.get(f"{self.host}/api/tags", timeout=1.5)
            if res.status_code != 200:
                return None
            # If server responds, prompt the default small model
            prompt = f"Summarize as a 7-section tech video script (Hook, Context, Development, Explanation, Implications, Limitations, Takeaway): {article.get('title')}. Output JSON."
            payload = {"model": "llama3.2:1b", "prompt": prompt, "stream": False, "format": "json"}
            post_res = requests.post(f"{self.host}/api/generate", json=payload, timeout=15)
            if post_res.status_code == 200:
                data = post_res.json()
                parsed = json.loads(data["response"])
                return parsed
        except Exception:
            pass
        return None

class LocalFallbackProvider(AIProvider):
    """100% deterministic, offline, zero-budget fallback provider."""
    def generate(self, article: Dict[str, Any]) -> Dict[str, Any]:
        return FallbackTemplates.generate_script(article)

class ProviderManager:
    """Coordinates generation with strict zero-budget fallback guarantees."""
    def __init__(self):
        self.gemini = GeminiProvider()
        self.ollama = OllamaProvider()
        self.fallback = LocalFallbackProvider()

    def generate_script(self, article: Dict[str, Any]) -> Dict[str, Any]:
        # Try Gemini if key is provided
        if os.getenv("GEMINI_API_KEY"):
            script = self.gemini.generate(article)
            if script and script.get("hook"):
                logger.info("Script generated via Gemini API")
                return script

        # Try Ollama if running
        ollama_script = self.ollama.generate(article)
        if ollama_script and ollama_script.get("hook"):
            logger.info("Script generated via local Ollama")
            return ollama_script

        # Fallback to local deterministic templates
        logger.info("Script generated via Local Fallback Engine (Zero-Budget Offline)")
        return self.fallback.generate(article)
