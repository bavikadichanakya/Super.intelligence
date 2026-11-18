# PHASE 5 — AUDIO & SOUND DESIGN ARCHITECTURE

**Project:** SUPER.INTELLIGENCEEE  
**Phase:** Phase 5 — Reference-Driven Autonomous Technical Reel Production System  
**Reference Benchmark:** `This is what i want.mp4`  
**Mandatory Operating Cost:** ₹0  
**Target Broadcast Standard:** EBU R128 (-16.0 LUFS ± 1.0, True Peak <= -1.0 dBTP, 48 kHz 24-bit Stereo)

---

## 1. EXECUTIVE SUMMARY & FORENSIC BENCHMARK

Forensic analysis of `This is what i want.mp4` established that audio energy, crisp speech clarity, and subtle musical momentum are critical drivers of audience retention in technical Reels. 

The reference audio profile exhibits:
1. **Narration Speed & Energy:** 146.4 WPM across 74.93 seconds (182 words total). Sentence boundaries are tight (10–18 words per sentence), preventing cognitive fatigue.
2. **Vocal EQ & Compression:** High-frequency presence boost (+2 dB around 3 kHz) for intelligibility on mobile phone speakers, low-frequency rumble filtering (< 80 Hz high-pass), and dynamic compression (3:1 ratio, -20 dB threshold).
3. **Background Music Dynamics:** Warm, low-key lo-fi tech chillhop bed operating at -22 dB relative to voice. When the speaker pauses, the bed smoothly recovers (+6 dB over 350 ms), maintaining rhythmic continuity without drowning technical vocabulary.
4. **Micro-SFX Synchronization:** Micro-acoustic events punctuate visual reveals: soft clicks on kinetic bounding box highlights, low-frequency whooshes on scene transitions, and gentle electronic chimes on timer stops.

---

## 2. VOICE IDENTITY & NARRATION PIPELINE

The voice identity is strictly locked to **Kokoro-82M `am_liam`** (General American English male).

```
[Raw Topic & Research Script]
              │
              ▼
[Phonetic Pre-processor (audio/pronunciation.py)]
  - Expansion of hardware acronyms ("NVMe", "PCIe", "MoE", "FP16")
  - Number cadence ("2.78 trillion", "8.24 gigabytes", "176 kilobytes")
              │
              ▼
[Kokoro-82M Voicebox (am_liam, speed=1.05)]
  - Sample Rate: 24 kHz mono output
  - Pacing: 145–150 WPM
              │
              ▼
[Vocal Mastering Chain (FFmpeg Filter Complex)]
  - High-Pass Filter: 80 Hz (12 dB/octave)
  - Mud Cut: -1.5 dB @ 300 Hz (Q=1.0)
  - Presence Boost: +2.0 dB @ 3000 Hz (Q=1.5)
  - Vocal Compressor: -20 dB threshold, 3:1 ratio, 5 ms attack, 50 ms release
  - Upsampling: 48 kHz stereo
```

Zero silent fallback to pyttsx3 or robotic speech synthesizers is permitted. If Kokoro fails, the pipeline raises an explicit error and stops.

---

## 3. PROCEDURAL LO-FI CHILLHOP BED (₹0 OPERATIONAL COST)

To ensure ₹0 external dependency, `audio/reference_sound_designer.py` incorporates an autonomous procedural lo-fi ambient synthesizer built with NumPy and SciPy:

1. **Harmonic Pad Progression:**
   - Chord sequence: $D\text{m9} \to G13 \to C\text{maj9} \to A\text{m9}$
   - Frequency sets:
     - $D\text{m9}$: 146.83 Hz ($D3$), 220.00 Hz ($A3$), 261.63 Hz ($C4$), 329.63 Hz ($E4$), 440.00 Hz ($A4$)
     - $G13$: 196.00 Hz ($G3$), 246.94 Hz ($B3$), 293.66 Hz ($D4$), 329.63 Hz ($E4$), 392.00 Hz ($G4$)
     - $C\text{maj9}$: 130.81 Hz ($C3$), 196.00 Hz ($G3$), 246.94 Hz ($B3$), 329.63 Hz ($E4$), 392.00 Hz ($G4$)
     - $A\text{m9}$: 110.00 Hz ($A2$), 164.81 Hz ($E3$), 220.00 Hz ($A3$), 261.63 Hz ($C4$), 329.63 Hz ($E4$)
   - Additive harmonics with gentle exponential envelope decay.
2. **Sub-Bass Pulse:**
   - 55.0 Hz fundamental sine wave on beats 1 and 3 of an 80 BPM grid.
   - 350 ms exponential decay envelope ($\exp(-12t)$).
3. **Vinyl Tape Texture:**
   - Butterworth 2nd-order low-pass filtered Gaussian noise ($f_c = 2500\text{ Hz}$).
4. **Stereo Haas Widening:**
   - 1.2 ms channel delay on right stereo channel ($58\text{ samples}$ @ 48 kHz).

---

## 4. DYNAMIC SIDECHAIN DUCKING & SFX MIXING

The final soundtrack mixes speech, music, and sound effects using FFmpeg `sidechaincompress` and `amix`:

```
Voice Input [0:a] ───► [Vocal Format] ────────┬───────────────► [sidechaincompress]
                                              │                       │ (Ducks bed by -22 dB)
Music Input [1:a] ───► [Bed Format]   ────────┼───────────────────────┘
                                              │                       │
                                              │                  [Ducked Bed]
                                              │                       │
                                              ├───────────────────────┤
                                              ▼                       ▼
                                         [Speech Track] + [Ducked Background Bed]
                                                          │
                                                          ▼
                                                      [amix = 2]
                                                          │
SFX Inputs [2..N:a] ──► [adelay = ts] ────────────────────┼
                                                          │
                                                          ▼
                                                      [amix = N]
                                                          │
                                                          ▼
                                                [loudnorm (EBU R128)]
                                                  - I = -16.0 LUFS
                                                  - LRA = 7.0 LU
                                                  - TP = -1.0 dBTP
                                                          │
                                                          ▼
                                              [Broadcast Master WAV]
```

---

## 5. TELEMETRY & COMPLIANCE VERIFICATION

Every generated audio master is forensically analyzed with `ebur128=framelog=verbose` to extract:
- **Integrated Loudness ($I$):** Must be $-16.0 \pm 1.0\text{ LUFS}$.
- **True Peak ($TP$):** Must not exceed $-1.0\text{ dBTP}$ (preventing DAC clipping on mobile devices).
- **Loudness Range ($LRA$):** Target $\le 7.0\text{ LU}$ (ensures consistent vocal dynamics across noisy environments).
- **Sample Rate / Bit Depth:** 48,000 Hz, 16/24-bit stereo PCM.
