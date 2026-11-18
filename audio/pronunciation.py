"""
SUPER.INTELLIGENCEEE — Technical Pronunciation Lexicon & Preprocessor
Phonetically prepares technical AI, ML, hardware, mathematics, and unit tokens
for natural, accurate text-to-speech synthesis with Piper.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple


class TechnicalPronunciationLexicon:
    """
    Transforms dense technical terminology, Big-O notations, acronyms,
    quantization formats, and model sizing into phonetically unambiguous strings
    that TTS voices pronounce accurately and naturally.
    """

    # Exact token or phrase mappings (case-sensitive or normalized)
    PHRASE_MAPPINGS: List[Tuple[re.Pattern, str]] = [
        # Big-O notations
        (re.compile(r"\bO\(N\^2\)", re.IGNORECASE), "O of N squared"),
        (re.compile(r"\bO\(N\^3\)", re.IGNORECASE), "O of N cubed"),
        (re.compile(r"\bO\(N\s*log\s*N\)", re.IGNORECASE), "O of N log N"),
        (re.compile(r"\bO\(N\)", re.IGNORECASE), "O of N"),
        (re.compile(r"\bO\(1\)", re.IGNORECASE), "O of 1"),
        (re.compile(r"\bO\(log\s*N\)", re.IGNORECASE), "O of log N"),

        # Academic & Project Names
        (re.compile(r"\barXiv\b", re.IGNORECASE), "archive"),
        (re.compile(r"\bPyTorch\b", re.IGNORECASE), "Py-Torch"),
        (re.compile(r"\bTensorFlow\b", re.IGNORECASE), "Tensor-Flow"),
        (re.compile(r"\bHuggingFace\b", re.IGNORECASE), "Hugging Face"),
        (re.compile(r"\bGitHub\b", re.IGNORECASE), "Git-Hub"),
        (re.compile(r"\bGitLab\b", re.IGNORECASE), "Git-Lab"),
        (re.compile(r"\bFastAPI\b", re.IGNORECASE), "Fast-A-P-I"),
        (re.compile(r"\bOpenAI\b", re.IGNORECASE), "Open A-I"),
        (re.compile(r"\bDeepMind\b", re.IGNORECASE), "Deep-Mind"),
        (re.compile(r"\bAnthropic\b", re.IGNORECASE), "An-thropic"),

        # Model Names & Families
        (re.compile(r"\bLLaMA[- ]?3\.1\b", re.IGNORECASE), "Llama 3.1"),
        (re.compile(r"\bLLaMA[- ]?3\b", re.IGNORECASE), "Llama 3"),
        (re.compile(r"\bLLaMA\b", re.IGNORECASE), "Llama"),
        (re.compile(r"\bMistral\b", re.IGNORECASE), "Miss-tral"),
        (re.compile(r"\bMixtral\b", re.IGNORECASE), "Mix-tral"),
        (re.compile(r"\bQwen\b", re.IGNORECASE), "Q-wen"),
        (re.compile(r"\bPhi[- ]?3\b", re.IGNORECASE), "Fye 3"),
        (re.compile(r"\bPhi[- ]?4\b", re.IGNORECASE), "Fye 4"),
        (re.compile(r"\bGemma\b", re.IGNORECASE), "Jemma"),

        # Architectures & Techniques
        (re.compile(r"\bMoE\b"), "M-o-E"),
        (re.compile(r"\bRAG\b"), "Rag"),
        (re.compile(r"\bLoRA\b"), "Low-rah"),
        (re.compile(r"\bQLoRA\b"), "Q-Low-rah"),
        (re.compile(r"\bSSM\b"), "S-S-M"),
        (re.compile(r"\bSSMs\b"), "S-S-Ms"),
        (re.compile(r"\bMamba\b"), "Mamba"),
        (re.compile(r"\bSOTA\b"), "state of the art"),
        (re.compile(r"\bRLHF\b"), "R-L-H-F"),
        (re.compile(r"\bDPO\b"), "D-P-O"),
        (re.compile(r"\bPPO\b"), "P-P-O"),
        (re.compile(r"\bKV cache\b", re.IGNORECASE), "K-V cache"),

        # Formats & Quantization
        (re.compile(r"\bINT4\b", re.IGNORECASE), "Int 4"),
        (re.compile(r"\bINT8\b", re.IGNORECASE), "Int 8"),
        (re.compile(r"\bFP16\b", re.IGNORECASE), "F-P 16"),
        (re.compile(r"\bFP8\b", re.IGNORECASE), "F-P 8"),
        (re.compile(r"\bFP32\b", re.IGNORECASE), "F-P 32"),
        (re.compile(r"\bBF16\b", re.IGNORECASE), "B-float 16"),
        (re.compile(r"\bGGUF\b", re.IGNORECASE), "G-G-U-F"),
        (re.compile(r"\bAWQ\b", re.IGNORECASE), "A-W-Q"),
        (re.compile(r"\bGPTQ\b", re.IGNORECASE), "G-P-T-Q"),
        (re.compile(r"\bEXL2\b", re.IGNORECASE), "E-X-L 2"),

        # Hardware & Chips
        (re.compile(r"\bVRAM\b"), "V-RAM"),
        (re.compile(r"\bGPUs\b"), "G-P-Us"),
        (re.compile(r"\bGPU\b"), "G-P-U"),
        (re.compile(r"\bCPUs\b"), "C-P-Us"),
        (re.compile(r"\bCPU\b"), "C-P-U"),
        (re.compile(r"\bTPUs\b"), "T-P-Us"),
        (re.compile(r"\bTPU\b"), "T-P-U"),
        (re.compile(r"\bNPUs\b"), "N-P-Us"),
        (re.compile(r"\bNPU\b"), "N-P-U"),
        (re.compile(r"\bRTX\s*(\d{4})\b", re.IGNORECASE), r"R-T-X \1"),
        (re.compile(r"\bRTX\b"), "R-T-X"),
        (re.compile(r"\bH100\b"), "H 100"),
        (re.compile(r"\bH200\b"), "H 200"),
        (re.compile(r"\bA100\b"), "A 100"),
        (re.compile(r"\bB200\b"), "B 200"),
        (re.compile(r"\bGB200\b"), "G-B 200"),
        (re.compile(r"\bGH200\b"), "G-H 200"),

        # Common Tech Acronyms
        (re.compile(r"\bLLMs\b"), "L-L-Ms"),
        (re.compile(r"\bLLM\b"), "L-L-M"),
        (re.compile(r"\bAPIs\b"), "A-P-Is"),
        (re.compile(r"\bAPI\b"), "A-P-I"),
        (re.compile(r"\bSDKs\b"), "S-D-Ks"),
        (re.compile(r"\bSDK\b"), "S-D-K"),
        (re.compile(r"\bCLIs\b"), "C-L-Is"),
        (re.compile(r"\bCLI\b"), "C-L-I"),
        (re.compile(r"\bUI/UX\b", re.IGNORECASE), "U-I and U-X"),
        (re.compile(r"\bUI\b"), "U-I"),
        (re.compile(r"\bUX\b"), "U-X"),
        (re.compile(r"\brepos\b", re.IGNORECASE), "repositories"),
        (re.compile(r"\brepo\b", re.IGNORECASE), "repository"),
        (re.compile(r"\bCUDA\b"), "Coo-dah"),
        (re.compile(r"\bROCm\b"), "Rock-em"),
        (re.compile(r"\bONNX\b"), "On-ix"),
        (re.compile(r"\bTTS\b"), "T-T-S"),
        (re.compile(r"\bSTT\b"), "S-T-T"),
        (re.compile(r"\bASR\b"), "A-S-R"),
        (re.compile(r"\bLUFS\b"), "L-U-F-S"),
        (re.compile(r"\bdBTP\b"), "D-B true peak"),
        (re.compile(r"\bdB\b"), "decibels"),

        # Parameter Counts & Sizes
        (re.compile(r"\b(\d+)B\s+parameters\b", re.IGNORECASE), r"\1 billion parameters"),
        (re.compile(r"\b(\d+)B\s+param\b", re.IGNORECASE), r"\1 billion parameter"),
        (re.compile(r"\b(\d+)B\b"), r"\1 billion"),
        (re.compile(r"\b(\d+)M\s+parameters\b", re.IGNORECASE), r"\1 million parameters"),
        (re.compile(r"\b(\d+)M\s+tokens\b", re.IGNORECASE), r"\1 million tokens"),
        (re.compile(r"\b1M\b"), "one million"),
        (re.compile(r"\b10M\b"), "ten million"),
        (re.compile(r"\b100M\b"), "one hundred million"),
        (re.compile(r"\b1T\b"), "one trillion"),

        # Units and memory
        (re.compile(r"\b(\d+)\s*GB\b", re.IGNORECASE), r"\1 gigabytes"),
        (re.compile(r"\b(\d+)\s*TB\b", re.IGNORECASE), r"\1 terabytes"),
        (re.compile(r"\b(\d+)\s*MB\b", re.IGNORECASE), r"\1 megabytes"),
        (re.compile(r"\b(\d+)\s*ms\b", re.IGNORECASE), r"\1 milliseconds"),
        (re.compile(r"\b(\d+)\s*fps\b", re.IGNORECASE), r"\1 frames per second"),
        (re.compile(r"\b(\d+)\s*tok/s\b", re.IGNORECASE), r"\1 tokens per second"),
        (re.compile(r"\b(\d+)\s*tokens/s\b", re.IGNORECASE), r"\1 tokens per second"),

        # Speedups and Multipliers (e.g., 4.2x, 10x, 2.5X)
        (re.compile(r"\b(\d+(?:\.\d+)?)[xX]\b"), r"\1 times"),
    ]

    @classmethod
    def preprocess_text(cls, text: str) -> str:
        """
        Processes narration text by substituting all technical terminology,
        acronyms, and symbols with phonetically transparent equivalents.
        """
        if not text:
            return ""

        result = text
        for pattern, replacement in cls.PHRASE_MAPPINGS:
            result = pattern.sub(replacement, result)

        # Cleanup redundant whitespaces
        result = re.sub(r"\s+", " ", result).strip()
        return result

