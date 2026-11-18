import React from "react";
import {
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Img,
} from "remotion";

export interface CharacterHostProps {
  pose?: "presenter" | "investigator" | "explainer";
  gesture?: "idle" | "explaining" | "pointing";
  isSpeaking?: boolean;
  speechIntensity?: number;
  targetX?: number;
  targetY?: number;
  targetLabel?: string;
  position?: "center" | "left" | "right";
  scale?: number;
  ambientTintHex?: string;
}

export const CharacterHost: React.FC<CharacterHostProps> = ({
  pose = "presenter",
  gesture = "explaining",
  isSpeaking = true,
  speechIntensity = 1.0,
  targetX,
  targetY,
  targetLabel,
  position = "center",
  scale = 0.65,
  ambientTintHex = "#00E5FF",
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const tSec = frame / fps;

  // 1. Biometric Respiration & Micro-Tilt
  const breathFreq = 0.35;
  const breathDy = 3.5 * Math.sin(2.0 * Math.PI * breathFreq * tSec);

  const tiltFreq = 0.18;
  const baseTilt =
    pose === "investigator" ? 2.5 : pose === "explainer" ? -2.0 : 0.0;
  const tiltDeg = baseTilt + 0.8 * Math.sin(2.0 * Math.PI * tiltFreq * tSec);

  // 2. Deterministic Eyelid Blink Cycle (150ms every 3.2s)
  const blinkCycle = 3.2;
  const modT = tSec % blinkCycle;
  const isBlinking = modT < 0.15;
  const blinkAlpha = isBlinking ? Math.sin((modT / 0.15) * Math.PI) : 0.0;

  // 3. Mouth Viseme Selection (Speech-Synchronized)
  let visemeFile = "mouth_closed.png";
  if (isSpeaking && speechIntensity > 0.05) {
    const speechFreq = 4.8; // Hz
    const cycle = (tSec * speechFreq) % 1.0;
    if (cycle < 0.15 || (cycle >= 0.6 && cycle < 0.85)) {
      visemeFile = "mouth_slight.png";
    } else if (cycle >= 0.15 && cycle < 0.6) {
      const alt = Math.floor(tSec * 2.4) % 3;
      visemeFile = alt === 2 ? "mouth_round.png" : "mouth_open.png";
    }
  }

  // 4. Arm Kinematics & Pointing
  let armRotDeg = 0.0;
  let armDx = 0.0;
  let armDy = 0.0;
  let pointingActive = false;

  if (gesture === "pointing") {
    pointingActive = true;
    const entry = Math.min(1.0, (tSec % 5.0) / 0.4);
    const ease = 1.0 - Math.pow(1.0 - entry, 3);
    armRotDeg = -16.0 * ease + 1.2 * Math.sin(2.0 * Math.PI * 0.8 * tSec);
    armDx = 15.0 * ease;
    armDy = -35.0 * ease;
  } else if (gesture === "explaining") {
    if (isSpeaking) {
      const cadence = Math.sin(2.0 * Math.PI * 0.9 * tSec);
      armRotDeg = -5.0 * (0.5 + 0.5 * cadence);
      armDy = -14.0 * (0.5 + 0.5 * cadence);
    }
  }

  // 5. Screen Anchoring
  let anchorX = width * 0.5;
  let anchorY = height * 0.82;
  let flipH = false;

  if (position === "left") {
    anchorX = width * 0.25;
    anchorY = height * 0.83;
  } else if (position === "right") {
    anchorX = width * 0.75;
    anchorY = height * 0.83;
    flipH = true;
  }

  const targetH = 1050 * scale;
  const targetW = targetH; // 1:1 aspect

  return (
    <div
      style={{
        position: "absolute",
        left: anchorX - targetW / 2,
        top: anchorY - targetH + breathDy,
        width: targetW,
        height: targetH,
        transform: `rotate(${tiltDeg}deg) ${flipH ? "scaleX(-1)" : ""}`,
        transformOrigin: "50% 75%",
        pointerEvents: "none",
        zIndex: 50,
      }}
    >
      {/* Contact Drop Shadow */}
      <div
        style={{
          position: "absolute",
          left: 12,
          top: 16,
          width: "100%",
          height: "100%",
          filter: "blur(18px)",
          opacity: 0.65,
          zIndex: 1,
        }}
      >
        <Img
          src={staticFile("character/character_cutout_transparent.png")}
          style={{ width: "100%", height: "100%", filter: "brightness(0)" }}
        />
      </div>

      {/* Base Body Canvas (Open Eyes vs Blinking Eyes) */}
      <div style={{ position: "absolute", width: "100%", height: "100%", zIndex: 2 }}>
        <Img
          src={staticFile(
            blinkAlpha > 0.35
              ? "character/character_blinking.png"
              : "character/character_cutout_transparent.png"
          )}
          style={{ width: "100%", height: "100%", objectFit: "contain" }}
        />
      </div>

      {/* Mouth Viseme Layer (Synchronized Speech) */}
      <div
        style={{
          position: "absolute",
          left: `${(950 / 2048) * 100}%`,
          top: `${(920 / 2048) * 100}%`,
          width: `${(260 / 2048) * 100}%`,
          height: `${(140 / 2048) * 100}%`,
          zIndex: 3,
        }}
      >
        <Img
          src={staticFile(`character/${visemeFile}`)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            borderRadius: "50%",
          }}
        />
      </div>

      {/* Articulated Arm & Hand Layer */}
      <div
        style={{
          position: "absolute",
          left: `${(399 / 2048) * 100}%`,
          top: `${(1167 / 2048) * 100}%`,
          width: `${((875 - 399) / 2048) * 100}%`,
          height: `${((1535 - 1167) / 2048) * 100}%`,
          transformOrigin: `${((460 - 399) / (875 - 399)) * 100}% ${
            ((1200 - 1167) / (1535 - 1167)) * 100
          }%`,
          transform: `rotate(${armRotDeg}deg) translate(${armDx}px, ${armDy}px)`,
          zIndex: 4,
        }}
      >
        <Img
          src={staticFile("character/arm_pencil_layer.png")}
          style={{ width: "100%", height: "100%", objectFit: "contain" }}
        />
      </div>

      {/* Ambient Lighting Wash */}
      {ambientTintHex && (
        <div
          style={{
            position: "absolute",
            width: "100%",
            height: "100%",
            backgroundColor: ambientTintHex,
            opacity: 0.08,
            mixBlendMode: "screen",
            zIndex: 5,
          }}
        />
      )}

      {/* Holographic Laser Pointer HUD (in pointing mode) */}
      {pointingActive && targetX !== undefined && targetY !== undefined && (
        <svg
          style={{
            position: "fixed",
            left: 0,
            top: 0,
            width: width,
            height: height,
            pointerEvents: "none",
            zIndex: 60,
          }}
        >
          {/* Laser Core */}
          <line
            x1={anchorX + 80}
            y1={anchorY - targetH * 0.4}
            x2={targetX}
            y2={targetY}
            stroke="#00E5FF"
            strokeWidth="2"
            strokeOpacity="0.85"
          />
          {/* Laser Glow */}
          <line
            x1={anchorX + 80}
            y1={anchorY - targetH * 0.4}
            x2={targetX}
            y2={targetY}
            stroke="#00E5FF"
            strokeWidth="6"
            strokeOpacity="0.25"
          />
          {/* Target Reticle */}
          <circle
            cx={targetX}
            cy={targetY}
            r={24}
            fill="none"
            stroke="#00E5FF"
            strokeWidth="2"
            strokeDasharray="4 4"
          />
          <circle cx={targetX} cy={targetY} r={4} fill="#FFAB00" />
          {targetLabel && (
            <text
              x={targetX + 30}
              y={targetY + 6}
              fill="#00E5FF"
              fontSize="16"
              fontFamily="monospace"
              fontWeight="bold"
            >
              [ {targetLabel} ]
            </text>
          )}
        </svg>
      )}
    </div>
  );
};
