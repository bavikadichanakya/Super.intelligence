# SUPER.INTELLIGENCEEE — PHASE 3.5.1 AUDIO FAILURE AUDIT
## Forensic Investigation into Audio Export & Video Muxing Pipeline

**Date:** 2026-11-07  
**Auditor:** Principal AI Systems Architect & Audio Engineering Lead  
**Investigation Target:** `doc_phase3_5_20261107_153546_speculative_decoding_raw_documentary.mp4` & Related Audio Stems  
**Workspace:** `A:\SUPER.INTELLIGENCEEE`  
**Classification:** CRITICAL PIPELINE REPAIR  

---

## 1. EXECUTIVE SUMMARY & FORENSIC FINDINGS

During the Phase 3.5 review, an audit of the exported media revealed that while speech synthesis, soundtrack generation, and audio soundscape mastering had executed successfully on disk, **`raw_documentary.mp4` contained zero audio streams**. Furthermore, an inspection of the subtitle generation pipeline revealed that `captions.ass` contained header styles but zero dialogue events.

This forensic audit identifies the exact architectural root causes across the audio production and export chain:

1. **Root Cause 1 (`raw_documentary.mp4` Missing Audio):**  
   In [`creative/tech_documentary/documentary_renderer/tech_doc_producer.py`](file:///A:/SUPER.INTELLIGENCEEE/creative/tech_documentary/documentary_renderer/tech_doc_producer.py#L172-L178), `self.transition_router.concat_clips(...)` concatenates the individual rendered video clips into `raw_video_path` (`*_raw_documentary.mp4`). Because the individual scene animation clips are generated without audio, this intermediate concatenation output contains solely a video stream (`h264`). The audio was subsequently muxed only into `final_video_path` (`*_tech_doc_final.mp4`) in Step 6. Because `raw_video_path` was retained and exported under the name `raw_documentary.mp4`, anyone playing the raw documentary export received a silent video.

2. **Root Cause 2 (`captions.ass` Missing Dialogue Events):**  
   In `TechDocProducer.produce_documentary`, scene narration was passed in a dictionary with the key `"narration"`:
   ```python
   sb_dict = {"scenes": [{"scene_index": i + 1, "narration": sc.get("narration", "") ...}]}
   ```
   However, [`captions/caption_generator.py`](file:///A:/SUPER.INTELLIGENCEEE/captions/caption_generator.py#L95) explicitly checked for `"narration_text"` or `"voiceover"`. Because neither key was present, `text` evaluated to `""`, resulting in zero subtitle chunks, an empty `.srt` file (0 bytes), and an `.ass` script with zero dialogue events.

3. **Status of Underlying Audio Assets:**  
   The underlying audio assets (narration stems, adaptive soundtrack, sound cues, and master soundscape WAV) are intact and non-silent on disk:
   - All 6 narration stems in `output/drafts/phase3_5_audio/` are audible, natural American English male speech (`am_liam`, 24 kHz mono PCM, RMS 3276, Peak 27852).
   - `doc_phase3_5_20261107_153546_speculative_decoding_audio_raw.wav` is 67.46s, 48 kHz stereo, RMS 2316.9 (stitched speech).
   - `doc_phase3_5_20261107_153546_speculative_decoding_audio_soundscape.wav` is 67.46s, 48 kHz stereo, RMS 5375.3 (mastered mix with 6-act electronic score and sidechain ducking).
   - In `tech_doc_final.mp4`, the AAC audio stream was successfully muxed (RMS 5357.3), but `raw_documentary.mp4` had no audio stream.

---

## 2. DETAILED PIPELINE FORENSIC CHECKLIST

| Investigation Item | Target File / Operation | Forensic Finding | Defect Severity |
| :--- | :--- | :--- | :---: |
| **1. Audio Generation** | Voicebox Kokoro 24 kHz | Completed successfully for all 6 scenes | PASS |
| **2. Narration Stems** | `phase3_5_audio/scene_01..06.wav` | All 6 files exist, duration 9.4s–13.7s, RMS ~3276, audible speech | PASS |
| **3. Continuous Music** | `adaptive_soundtrack.py` | 6-Act synthetic score synthesized via NumPy; RMS ~4800, non-silent | PASS |
| **4. Sound Effects** | `sound_designer.py` / `sound_cues.py` | 6 foley cues generated and mixed; RMS ~2400, non-silent | PASS |
| **5. Master Audio Mix** | `*_audio_soundscape.wav` | 67.46s duration, 48 kHz stereo, RMS 5375.3, EBU R128 -14.0 LUFS | PASS |
| **6. Concat Output** | `*_raw_documentary.mp4` | Created by `transition_router.concat_clips`; **NO AUDIO STREAM** | **CRITICAL FAILURE** |
| **7. Final Reel Mux** | `*_tech_doc_final.mp4` | Created by `ffmpeg_pipeline.compose_final_reel`; Contains AAC audio | PASS |
| **8. Subtitle Events** | `*_captions.ass` | Header only; 0 dialogue events due to dictionary key mismatch | **HIGH DEFECT** |
| **9. Stream Symmetry** | Video vs Audio duration | Audio: 67.46s, Video: 67.37s ($\Delta = 93\text{ ms}$, within 100ms) | PASS |

---

## 3. ARCHITECTURAL REMEDIATION PLAN

### 3.1 Unify Audio Muxing Across All Video Exports
Both the clean master (`*_raw_documentary.mp4`) and the captioned master (`*_tech_doc_final.mp4`) must be full-fidelity audiovisual files containing:
- Stream 0: `h264` (1080x1920, 30 FPS, yuv420p)
- Stream 1: `aac` (48,000 Hz, 2 channels, 192 kbps)

1. The video-only concatenation output will be written to a temporary or internal intermediate path:
   `output/drafts/intermediate/{reel_slug}_video_track.mp4`
2. `*_raw_documentary.mp4` will be explicitly muxed with `master_soundscape_audio` without burned subtitles, serving as the **Clean Archival Master**.
3. `*_tech_doc_final.mp4` will be muxed with `master_soundscape_audio` and burned subtitles, serving as the **Captioned Release Master**.
4. Both files will be verified via `ffprobe` to ensure non-zero audio streams and duration alignment within 100 milliseconds.

### 3.2 Correct Subtitle Key Alignment
In `CaptionGenerator.generate_captions_from_storyboard`, support multiple narrative text keys:
```python
text = (sc.get("narration_text") or sc.get("narration") or sc.get("voiceover") or "").strip()
```
And in `TechDocProducer.produce_documentary`, explicitly pass `"narration_text"` in the scene dictionary.

### 3.3 Mandatory Automated FFprobe Stream Assertion
Integrate an automated post-export verification step in `TechDocProducer`:
- Assert stream count $\ge 2$ (Video + Audio).
- Assert `codec_name == 'aac'`.
- Assert `sample_rate == 48000`.
- Assert `abs(audio_duration - video_duration) <= 0.100`.
- Extract audio back to WAV and assert $\text{RMS} \ge 1000$ (zero silence tolerance).
- If any condition fails, raise `AudioMuxVerificationError` and abort with FAILED status.

