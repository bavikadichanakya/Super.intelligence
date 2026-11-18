# PHASE 4.3.2C.1 — FORENSIC ARTIFACT & MEDIA INTEGRITY AUDIT

**Project:** SUPER.INTELLIGENCEEE  
**Audit Target:** Autonomous Documentary Production Run (`output/drafts/phase432c_production_run/`)  
**Topic:** Metal Sandbox: Isolated Execution and Command Scheduling for GPU Coding Agents on Apple Silicon (arXiv:2611.17294v1)  
**Date:** 2026-11-14  
**Auditor:** Autonomous Video Production Acceptance Auditor  
**Operating Environment:** Windows 11 Home 64-bit, Python 3.11 (`.venv`), Intel Core i5-1135G7, 8 GB RAM, Intel Iris Xe  

---

## 1. EXECUTIVE SUMMARY

An independent forensic audit of all media assets, scene stems, and metadata generated during Phase 4.3.2C was conducted on-disk at `output/drafts/phase432c_production_run/`.

Every file was checked for physical existence, SHA-256 cryptographic hash integrity, container decoding validity (`ffmpeg -v error -i <file> -f null -`), stream parameter conformity, and consistency against `production_manifest.json` and previous reports.

### Key Audit Findings:
1. **Container & Stream Conformity:** All master files, audio files, and scene stems decode completely cleanly with zero container corruption, zero packet drops, and zero frame decoding errors.
2. **Cryptographic Hashes:** The three rendered scene stems match the SHA-256 hashes recorded in `production_manifest.json` bit-for-bit.
3. **Master Hash Resumption Discrepancy:** The master videos (`captioned_review.mp4` and `clean_master.mp4`) recorded in `reports/PHASE432C_END_TO_END_RUN.md` were captured from an intermediate pre-assembly test prior to final pipeline resumption. The authoritative on-disk hashes have been recomputed and verified.
4. **Duration Discrepancy & Stem Assembly Drift:**
   - Scene 1 Stem: **10.77s**
   - Scene 2 Stem: **20.27s**
   - Scene 3 Stem: **13.53s**
   - Total Stem Duration: **44.57s**
   - Master Narration: **33.44s**
   - Final Master Video Duration: **33.50s**
   - **Root Cause:** Scene 2 was rendered by Manim at 20.27s instead of the script-budgeted 10.21s. During final FFmpeg concatenation and audio multiplexing, the video was aligned to the 33.44s master audio track using `-shortest` / stream truncation, which truncated the tail of Scene 2 / Scene 3 stems.

---

## 2. COMPREHENSIVE ON-DISK ARTIFACT INVENTORY & HASH VERIFICATION

| Artifact Name | Relative Path | File Size | Authoritative SHA-256 Hash | Manifest Match | Decode Health |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Captioned Review Master** | `masters/reel_20261113_224800_metal_sandbox__isolated_execut_captioned_review.mp4` | 2,223,543 B | `6572a2b02322aaf7eae30d1b5180abe8d0d0eec253cf550536527c114b2ccbfb` | Replaces draft | **CLEAN** (0 errors) |
| **Clean Archival Master** | `masters/reel_20261113_224800_metal_sandbox__isolated_execut_clean_master.mp4` | 1,743,156 B | `346e905054e6772b64ae0221b7a8a53658f8d12c611594150f4d50c25b83db60` | Replaces draft | **CLEAN** (0 errors) |
| **Master Narration (16 LUFS)** | `audio/master_narration_16lufs.wav` | 6,419,934 B | `17f2332a9412d75077aad1411aa6b7751615777f4c663ae834da7e8e286d9f0e` | Master track | **CLEAN** (0 errors) |
| **Master Narration (Raw)** | `audio/master_narration_raw.wav` | 6,419,934 B | `fc23bb887e29fdcbd1cc75bc5939cf4117dea307db6b3ae1c6a8db2088fbcf9d` | Archival raw | **CLEAN** (0 errors) |
| **Scene 1 Narration** | `audio/scene_01_narration.wav` | 459,308 B | `b8558c924b8f6e7a61a29d803697f96cda6c2ef3db17dc3de29cc039f0abbf19` | Stem audio | **CLEAN** (0 errors) |
| **Scene 2 Narration** | `audio/scene_02_narration.wav` | 434,732 B | `b28ae944439d81a92046fe082f68aed9a358a3c0a4a2958b960fb4a016c20bfa` | Stem audio | **CLEAN** (0 errors) |
| **Scene 3 Narration** | `audio/scene_03_narration.wav` | 580,652 B | `453f871c9ec5bc7b7e9b3beb1ed000e2d8bda61237da74f6748b7bf5f7139d50` | Stem audio | **CLEAN** (0 errors) |
| **Scene 1 Stem** | `stems/reel_20261113_224800_metal_sandbox__isolated_execut_scene_01.mp4` | 653,288 B | `d8bb453662838681edb660668f05f8c143929d1c783d55e9918ac25a365daccb` | **EXACT MATCH** | **CLEAN** (0 errors) |
| **Scene 2 Stem** | `stems/reel_20261113_224800_metal_sandbox__isolated_execut_scene_02.mp4` | 311,659 B | `264fc1231774b6d7f4735dd795e33ad2f8b45331fa3352b28e4c5e5d52edd14c` | **EXACT MATCH** | **CLEAN** (0 errors) |
| **Scene 3 Stem** | `stems/reel_20261113_224800_metal_sandbox__isolated_execut_scene_03.mp4` | 815,290 B | `d7066c5d450682e771d6be7dcceb80dfa32b273a1766dc7691a3a92a15f6db70` | **EXACT MATCH** | **CLEAN** (0 errors) |
| **ASS Subtitles** | `reel_20261113_224800_metal_sandbox__isolated_execut_subtitles.ass` | 2,019 B | `dbebc4a7ff94fa4e6b9a897e9c3e921d019f6a27e7d9633e5c735d4924c5b3c5` | Script timed | Valid ASS syntax |
| **Visual Contact Sheet** | `qa/reel_20261113_224800_metal_sandbox__isolated_execut_contact_sheet.png` | 186,187 B | `adb32340aad95b99d8481dd59539bae4f9d32691f64e9fc60681ad8f54df9106` | QA artifact | 1620x960 PNG |
| **Expanded Contact Sheet** | `qa/phase432c1_expanded_contact_sheet.png` | 346,378 B | `f0449ec0c0aa45b59762117562f924d62b9a781b0a827fa6c8d3509919f1826f` | New Audit Asset | 1440x2040 PNG |
| **Production Manifest** | `production_manifest.json` | 5,548 B | `2a845cf45934440f82dfb10f81d1134a6254580214a1c5d57b28db86cb11b15c` | Canonical state | Valid JSON |
| **Research Dossier** | `research_dossier.json` | 7,718 B | `88e612f0e0bcba8529288924f7b2c556b6b7a86f91d5828d9ffc71b3e8e1957c` | Canonical state | Valid JSON |
| **Script JSON** | `script.json` | 4,998 B | `a7916bf960b73c21c7a829f0e1f72e3995f3c959b8be9037943d043d83b544e3` | Canonical state | Valid JSON |
| **Storyboard JSON** | `storyboard.json` | 21,048 B | `15e5812e9b0c79db30d7fa9a9fcffc7104b684dc8ff093557e1d13db6c123610` | Canonical state | Valid JSON |

---

## 3. DETAILED STREAM & CONTAINER PARAMETERS

### 3.1 Captioned Review Master (`captioned_review.mp4`)
```json
{
  "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
  "format_duration": 33.500000,
  "bit_rate": 530995,
  "video_stream": {
    "codec_name": "h264",
    "profile": "High",
    "width": 1080,
    "height": 1920,
    "aspect_ratio": "9:16",
    "pix_fmt": "yuv420p",
    "r_frame_rate": "30/1",
    "avg_frame_rate": "30/1",
    "duration": 33.466667,
    "bit_rate": 453189
  },
  "audio_stream": {
    "codec_name": "aac",
    "profile": "LC",
    "sample_rate": 96000,
    "channels": 2,
    "channel_layout": "stereo",
    "duration": 33.500000,
    "bit_rate": 72895
  }
}
```

### 3.2 Clean Archival Master (`clean_master.mp4`)
```json
{
  "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
  "format_duration": 33.500000,
  "bit_rate": 416276,
  "video_stream": {
    "codec_name": "h264",
    "profile": "High",
    "width": 1080,
    "height": 1920,
    "pix_fmt": "yuv420p",
    "r_frame_rate": "30/1",
    "duration": 33.466667,
    "bit_rate": 337968
  },
  "audio_stream": {
    "codec_name": "aac",
    "profile": "LC",
    "sample_rate": 96000,
    "channels": 2,
    "channel_layout": "stereo",
    "duration": 33.500000,
    "bit_rate": 72895
  }
}
```

### 3.3 Scene Stems Breakdown

1. **Scene 1 Stem (`stems/..._scene_01.mp4`):**
   - Video: H.264 (High), 1080x1920 @ 30 fps, Duration: 10.767s, Bitrate: 405 kbps.
   - Audio: AAC, 1 ch, 44,100 Hz, Duration: 10.760s, Bitrate: 69 kbps.
2. **Scene 2 Stem (`stems/..._scene_02.mp4`):**
   - Video: H.264 (High), 1080x1920 @ 30 fps, Duration: 20.267s, Bitrate: 123 kbps.
   - Audio: None (silent video stem generated by Manim Cairo renderer).
3. **Scene 3 Stem (`stems/..._scene_03.mp4`):**
   - Video: H.264 (High), 1080x1920 @ 30 fps, Duration: 13.533s, Bitrate: 407 kbps.
   - Audio: AAC, 1 ch, 44,100 Hz, Duration: 13.520s, Bitrate: 69 kbps.

---

## 4. INTEGRITY DISCREPANCIES & DEFECTS DETECTED

### Defect INT-01: Discrepancy Between Individual Stem Durations and Master Track
- Individual video stems sum to **44.57 seconds** (10.77s + 20.27s + 13.53s).
- Master audio narration is **33.44 seconds** (10.41s + 9.86s + 13.17s).
- The final master video is **33.50 seconds**.
- **Analysis:** Scene 2 was rendered by Manim at 20.27s (nearly double its allocated narration beat of 9.86s). When FFmpeg assembled the video, it truncated the scene stems to conform to the audio duration, causing an uneven temporal compression or cutting of visual elements.

### Defect INT-02: Audio Resampling Artifact (96,000 Hz AAC in Masters)
- The raw narration stems were generated at 22,050 Hz by Piper.
- The master audio track was normalized and mastered to 48,000 Hz 16-bit PCM WAV.
- During master video multiplexing, FFmpeg upsampled the AAC audio stream to **96,000 Hz**.
- While clean and playable, 96 kHz AAC is an unnecessary non-standard sample rate for mobile video delivery (standard is 44,100 Hz or 48,000 Hz) that increases mobile decoder CPU overhead.

---

## 5. PHASE A AUDIT CONCLUSION

The physical artifacts exist, have valid bitstreams, conform to 1080x1920 vertical standards, and decode cleanly without corrupt frames. However, internal temporal misalignment between stems and master audio requires remediation in the compositor assembly layer.

