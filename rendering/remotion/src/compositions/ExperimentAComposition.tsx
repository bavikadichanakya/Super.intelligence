import React from "react";
import {
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ExperimentACharacter } from "../components/ExperimentACharacter";
import { StudioEnvironment } from "../components/StudioEnvironment";

export const ExperimentAComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tSec = frame / fps;

  // Total Duration: 540 frames (18.0 seconds @ 30 FPS)

  // -------------------------------------------------------------------------
  // 1. Camera Framing: 3 Shots (Full View -> Medium -> Close-Up -> Hero)
  // -------------------------------------------------------------------------
  // Shot 1: Full View (0 - 135) -> scale: 0.62, y: 320
  // Transition 1 (135 - 165) -> pushes to Medium: scale: 0.95, y: 440
  // Shot 2: Medium Shot (165 - 285)
  // Transition 2 (285 - 315) -> pushes to Close-Up: scale: 1.62, y: 720
  // Shot 3: Close-Up (315 - 435)
  // Transition 3 (435 - 465) -> pulls back to Hero: scale: 0.80, y: 380
  // Shot 4: Hero Resolution (465 - 540)

  const camScale = interpolate(
    frame,
    [0, 135, 165, 285, 315, 435, 465, 540],
    [0.62, 0.62, 0.95, 0.95, 1.62, 1.62, 0.80, 0.80],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const camY = interpolate(
    frame,
    [0, 135, 165, 285, 315, 435, 465, 540],
    [300, 300, 440, 440, 720, 720, 380, 380],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // -------------------------------------------------------------------------
  // 2. Active Expression State Progression
  // -------------------------------------------------------------------------
  let expression: "neutral" | "curious" | "surprised" | "thinking" | "explaining" = "neutral";
  let stateLabel = "STATE 1: NEUTRAL (Natural Resting Expression)";

  if (frame >= 0 && frame < 75) {
    expression = "neutral";
    stateLabel = "STATE 1: NEUTRAL (Natural Resting Expression)";
  } else if (frame >= 75 && frame < 165) {
    expression = "curious";
    stateLabel = "STATE 2: CURIOUS (Attentive Eyes & Head Tilt)";
  } else if (frame >= 165 && frame < 240) {
    expression = "surprised";
    stateLabel = "STATE 3: SURPRISED (Exaggerated Reaction & Gasp)";
  } else if (frame >= 240 && frame < 360) {
    expression = "thinking";
    stateLabel = "STATE 4: THINKING (Thoughtful Gaze & Object Tracking)";
  } else if (frame >= 360 && frame < 465) {
    expression = "explaining";
    stateLabel = "STATE 5: EXPLAINING (Expressive Speaking Posture)";
  } else {
    expression = "neutral";
    stateLabel = "RESOLUTION: CONFIDENT REST (Seamless Integration)";
  }

  // -------------------------------------------------------------------------
  // 3. Head Kinematics: Tilt, Nod, Breathing
  // -------------------------------------------------------------------------
  // Continuous Biometric Breathing (0.35 Hz)
  const breathDy = 3.5 * Math.sin(2.0 * Math.PI * 0.35 * tSec);

  // Head Tilt (Smooth transition between states)
  let headTiltDeg = 0;
  if (frame >= 75 && frame < 165) {
    // Curious inquisitive tilt to +2.8 deg
    headTiltDeg = interpolate(frame, [75, 105, 145, 165], [0, 2.8, 2.8, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 165 && frame < 240) {
    // Surprised slight recoil upright
    headTiltDeg = interpolate(frame, [165, 185], [0, -0.8], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 240 && frame < 360) {
    // Thinking contemplative tilt to -2.2 deg
    headTiltDeg = interpolate(frame, [240, 275, 330, 360], [0, -2.2, -2.2, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 360 && frame < 465) {
    // Explaining rhythmic speaking sway
    headTiltDeg = 1.2 * Math.sin(2.0 * Math.PI * 0.6 * tSec);
  }

  // Head Nod (speaking cadence during Explaining)
  let headNodDy = 0;
  if (frame >= 360 && frame < 465) {
    headNodDy = 2.5 * Math.sin(2.0 * Math.PI * 1.4 * tSec);
  }

  // -------------------------------------------------------------------------
  // 4. Controlled Eye Movement (Gaze Vector & Object Tracking)
  // -------------------------------------------------------------------------
  let gazeX = 0;
  let gazeY = 0;

  if (frame >= 75 && frame < 145) {
    // Curious: Look slightly upper-right
    gazeX = 5;
    gazeY = -3;
  } else if (frame >= 165 && frame < 240) {
    // Surprised: Lock wide onto camera
    gazeX = 0;
    gazeY = 0;
  } else if (frame >= 240 && frame < 300) {
    // Thinking Part 1: Gaze shifts up-left in contemplation
    gazeX = interpolate(frame, [240, 265], [0, -8], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    gazeY = interpolate(frame, [240, 265], [0, -7], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 300 && frame < 350) {
    // Thinking Part 2: OBJECT GAZE TRACKING (eyes track an imagined object moving left to center)
    gazeX = interpolate(frame, [300, 345], [-8, 2], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    gazeY = interpolate(frame, [300, 345], [-7, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 350 && frame < 370) {
    // Eyes DART back to lock directly onto the camera!
    gazeX = interpolate(frame, [350, 360], [2, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    gazeY = 0;
  } else {
    // Neutral & Explaining: Direct engaged eye contact with camera
    gazeX = 0;
    gazeY = 0;
  }

  // -------------------------------------------------------------------------
  // 5. Natural Blinking (Deterministic 150ms cycles at frames 42, 355, 495)
  // -------------------------------------------------------------------------
  const blink1 = frame >= 40 && frame <= 46;
  const blink2 = frame >= 353 && frame <= 359;
  const blink3 = frame >= 492 && frame <= 498;
  const isBlinking = blink1 || blink2 || blink3;
  const blinkAlpha = isBlinking ? 1.0 : 0.0;

  // -------------------------------------------------------------------------
  // 6. Speech Visemes & Arm Pose
  // -------------------------------------------------------------------------
  let viseme: "closed" | "slight" | "open" | "round" | "thinking" | "surprised" = "closed";
  let armPose: "rest" | "thinking_chin" | "explaining_gesture" = "rest";
  let armRotDeg = 0;

  if (expression === "thinking") {
    armPose = "thinking_chin";
    viseme = "thinking";
  } else if (expression === "surprised") {
    armPose = "rest";
    viseme = "surprised";
  } else if (expression === "curious") {
    armPose = "rest";
    viseme = "slight";
  } else if (expression === "explaining") {
    armPose = "explaining_gesture";
    armRotDeg = 4.0 * Math.sin(2.0 * Math.PI * 1.2 * tSec);
    // Cycle visemes for natural speech articulation
    const cycle = (tSec * 4.5) % 1.0;
    if (cycle < 0.2) viseme = "slight";
    else if (cycle < 0.5) viseme = "open";
    else if (cycle < 0.75) viseme = "round";
    else viseme = "closed";
  } else {
    armPose = "rest";
    viseme = "closed";
  }

  return (
    <div
      style={{
        position: "relative",
        width: 1080,
        height: 1920,
        backgroundColor: "#080B11",
        overflow: "hidden",
      }}
    >
      {/* 1. Professional Studio Lighting Environment */}
      <StudioEnvironment keyLightIntensity={1.2} rimLightIntensity={1.0} />

      {/* 2. Character Canvas with Dynamic Camera Framing */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "flex-end",
          transform: `scale(${camScale}) translateY(${camY}px)`,
          transformOrigin: "540px 1100px",
          transition: "transform 0.1s linear",
        }}
      >
        {/* Soft Ground Contact Shadow */}
        <div
          style={{
            position: "absolute",
            bottom: 300,
            width: 700,
            height: 140,
            borderRadius: "50%",
            backgroundColor: "rgba(0, 0, 0, 0.55)",
            filter: "blur(30px)",
            transform: "translateY(50px)",
            pointerEvents: "none",
          }}
        />

        {/* The Animated Character Rig */}
        <ExperimentACharacter
          expression={expression}
          transitionProgress={1.0}
          gazeX={gazeX}
          gazeY={gazeY}
          isBlinking={isBlinking}
          blinkAlpha={blinkAlpha}
          headTiltDeg={headTiltDeg}
          headNodDy={headNodDy}
          breathDy={breathDy}
          isSpeaking={expression === "explaining"}
          viseme={viseme}
          armPose={armPose}
          armRotDeg={armRotDeg}
        />
      </div>

      {/* 3. Subtle, Minimal State & Framing Readout (Clean Editorial Safe-Zone) */}
      <div
        style={{
          position: "absolute",
          bottom: 110,
          left: 0,
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            background: "rgba(10, 14, 22, 0.75)",
            border: "1px solid rgba(255, 255, 255, 0.12)",
            borderRadius: 24,
            padding: "10px 28px",
            backdropFilter: "blur(12px)",
          }}
        >
          <span
            style={{
              fontFamily: "Segoe UI, sans-serif",
              fontSize: 22,
              fontWeight: 600,
              color: "#F5F7FA",
              letterSpacing: "0.04em",
            }}
          >
            {stateLabel}
          </span>
        </div>
        <div
          style={{
            marginTop: 8,
            fontFamily: "Segoe UI, monospace",
            fontSize: 16,
            color: "rgba(160, 175, 200, 0.7)",
            letterSpacing: "0.08em",
          }}
        >
          EXPERIMENT A // FRAME {frame}/540 ({(tSec).toFixed(1)}s) // SHOT:{" "}
          {frame < 135
            ? "FULL VIEW"
            : frame < 285
            ? "MEDIUM SHOT"
            : frame < 435
            ? "FACIAL CLOSE-UP"
            : "HERO RESOLUTION"}
        </div>
      </div>
    </div>
  );
};
