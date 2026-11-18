# SUPER.INTELLIGENCEEE — PHASE 3.5 AMERICAN VOICE EVALUATION
## Forensic Acoustic Audit, Voice Candidate Benchmarks & Voice Transformation Decision

**Date:** 2026-11-07  
**Auditor:** Senior Documentary Audio Director & American English Voice Director  
**Engine:** Voicebox AI Voice Studio (Kokoro-82M ONNX Runtime on CPU)  
**Sample Rate:** 24,000 Hz Mono PCM  
**Test Script:**
> *"Frontier AI models are abandoning traditional brute-force scaling. By optimizing test-time compute through speculative verification, autonomous systems achieve a three-hundred percent acceleration without degrading precision."* (25 words)

---

## 1. VOICE CANDIDATE DISCOVERY

Inspection of the Voicebox Kokoro registry revealed 8 native General American English male voice profiles:

| Voice ID | Display Name | Gender | Accent | Kokoro Class | Status in Voicebox |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `am_adam` | Adam | Male | General American | `en-us` | Available & Preloaded |
| `am_michael` | Michael | Male | General American | `en-us` | Available & Preloaded |
| `am_eric` | Eric | Male | General American | `en-us` | Available & Preloaded |
| `am_liam` | Liam | Male | General American | `en-us` | Available & Preloaded |
| `am_onyx` | Onyx | Male | General American | `en-us` | Available |
| `am_echo` | Echo | Male | General American | `en-us` | Available |
| `am_fenrir` | Fenrir | Male | General American | `en-us` | Available |
| `am_puck` | Puck | Male | General American | `en-us` | Available |

The previous default voice, `bm_george` (British RP Male), has been **permanently deprecated and blocked by hard validation**.

---

## 2. STANDARDIZED ACOUSTIC BENCHMARK RESULTS

All four top American male candidates were generated through Voicebox using the identical script and evaluated on disk at `output/voice_samples/`:

| Voice Candidate | WAV Sample | Duration | Pacing (WPM) | Peak dB | RMS dB | ZCR (/sec) | Pause Ratio |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`am_adam`** | [`sample_am_adam.wav`](file:///A:/SUPER.INTELLIGENCEEE/output/voice_samples/sample_am_adam.wav) | 13.62s | 110.1 WPM | -1.41 dB | -20.00 dB | 3,006.2 | 20.2% |
| **`am_michael`** | [`sample_am_michael.wav`](file:///A:/SUPER.INTELLIGENCEEE/output/voice_samples/sample_am_michael.wav) | 15.44s | 97.2 WPM | -1.41 dB | -20.07 dB | 2,766.8 | 22.7% |
| **`am_eric`** | [`sample_am_eric.wav`](file:///A:/SUPER.INTELLIGENCEEE/output/voice_samples/sample_am_eric.wav) | 12.42s | 120.8 WPM | -2.85 dB | -20.00 dB | 2,282.5 | 18.1% |
| **`am_liam`** | [`sample_am_liam.wav`](file:///A:/SUPER.INTELLIGENCEEE/output/voice_samples/sample_am_liam.wav) | 12.80s | 117.2 WPM | -1.41 dB | -20.00 dB | 3,096.6 | 19.1% |

---

## 3. QUALITATIVE AUDIT & PHONETIC ANALYSIS

### Candidate 1: `am_adam` ("Adam" — The Resonant Investigator)
- **Acoustic Signature:** Rich low-mid fundamental (~115 Hz), authoritative, clear American rhoticity (/r/ sounds are round and natural without British dropping).
- **Pros:** Sounds like an investigative PBS Frontline or Nova science presenter. Excellent gravitas for opening hooks and architectural breakdowns.
- **Cons:** Slightly deliberate tempo (110 WPM); requires concise scripting so scenes do not stretch duration.
- **Suitability Score:** **9.3 / 10**

### Candidate 2: `am_michael` ("Michael" — The Deliberate Explainer)
- **Acoustic Signature:** Warmer tone, but noticeably dragged cadence (97.2 WPM) with 22.7% dead air between phrases.
- **Pros:** Relaxed, conversational warmth.
- **Cons:** Too slow for high-momentum, 60–75 second short-form technology documentaries. Pushes script lengths beyond allowable timing windows.
- **Suitability Score:** **7.1 / 10**

### Candidate 3: `am_eric` ("Eric" — The Rapid Specialist)
- **Acoustic Signature:** Fast delivery (120.8 WPM), energetic, rapid inflection.
- **Pros:** Fast synthesis speed; keeps video moving quickly.
- **Cons:** Lower zero-crossing rate (2,282.5/s) results in softer consonant definition on technical polysyllables like "speculative verification" and "three-hundred percent".
- **Suitability Score:** **8.0 / 10**

### Candidate 4: `am_liam` ("Liam" — The Modern Tech Director)
- **Acoustic Signature:** Modern General American cadence (117.2 WPM), high phoneme articulation (ZCR 3,096.6/s), energetic yet natural intonation.
- **Pros:** Hits the ideal documentary tempo (115–120 WPM). Clear, curious, confident, and crisp articulation on technical terminology. Perfectly balanced pauses (19.1%).
- **Cons:** Slightly brighter presence requires gentle warm EQ low-pass shelf (~12 kHz) during mastering.
- **Suitability Score:** **9.6 / 10 (WINNER)**

---

## 4. EXECUTIVE SELECTION & CODE-LEVEL ENFORCEMENT

1. **Primary Production Voice:** **`am_liam`** (General American Male, Modern Tech Director) is selected as the primary narrator for Phase 3.5.
2. **Alternate Production Voice:** **`am_adam`** (General American Male, Deep Investigative) is certified as the secondary American profile for long-form deep-dives.
3. **Hard Validation Added:**
   In `audio/narration/narration_service.py` and `audio/providers/voicebox_provider.py`:
   - Any default voice request for `bm_george`, `bm_daniel`, `bm_lewis`, or any `bm_*` / `bf_*` British voice is **intercepted and rejected with an explicit `ValueError`**.
   - The default voice ID across all configuration files and services is updated to `am_liam`.
   - The production manifest records `accent: "GENERAL_AMERICAN"` and `voice_id: "am_liam"`.

