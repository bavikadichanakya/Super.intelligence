import React from "react";
import { Img, staticFile } from "remotion";

export interface ExperimentACharacterProps {
  expression: "neutral" | "curious" | "surprised" | "thinking" | "explaining";
  transitionProgress: number; // 0.0 to 1.0
  nextExpression?: "neutral" | "curious" | "surprised" | "thinking" | "explaining";
  gazeX: number; // -15 to +15 pixels
  gazeY: number; // -15 to +15 pixels
  isBlinking: boolean;
  blinkAlpha: number; // 0.0 to 1.0
  headTiltDeg: number;
  headNodDy: number;
  breathDy: number;
  isSpeaking: boolean;
  viseme: "closed" | "slight" | "open" | "round" | "thinking" | "surprised";
  armPose: "rest" | "thinking_chin" | "explaining_gesture";
  armRotDeg?: number;
}

export const ExperimentACharacter: React.FC<ExperimentACharacterProps> = ({
  expression,
  gazeX,
  gazeY,
  isBlinking,
  blinkAlpha,
  headTiltDeg,
  headNodDy,
  breathDy,
  viseme,
  armPose,
  armRotDeg = 0,
}) => {
  // Master canvas reference space: 2048 x 2048
  // Coordinates:
  // Left eye pupil origin: (881, 745)
  // Right eye pupil origin: (1207, 745)
  // Left brow: (820, 665), Right brow: (1130, 665)
  // Mouth origin: (950, 920), 260x140

  // 1. Compute Eyebrow Transformations based on Expression
  let leftBrowDy = 0;
  let leftBrowRot = 0;
  let rightBrowDy = 0;
  let rightBrowRot = 0;

  switch (expression) {
    case "curious":
      leftBrowDy = -10;
      leftBrowRot = 6;
      rightBrowDy = -2;
      rightBrowRot = -1;
      break;
    case "surprised":
      leftBrowDy = -15;
      leftBrowRot = 4;
      rightBrowDy = -15;
      rightBrowRot = -4;
      break;
    case "thinking":
      leftBrowDy = 5;
      leftBrowRot = -5;
      rightBrowDy = 6;
      rightBrowRot = 5;
      break;
    case "explaining":
      leftBrowDy = -4;
      leftBrowRot = 2;
      rightBrowDy = -4;
      rightBrowRot = -2;
      break;
    case "neutral":
    default:
      leftBrowDy = 0;
      leftBrowRot = 0;
      rightBrowDy = 0;
      rightBrowRot = 0;
      break;
  }

  // 2. Compute Arm Kinematics
  let activeArmRot = armRotDeg;
  let armDx = 0;
  let armDy = 0;

  if (armPose === "thinking_chin") {
    // Arm rises to chin level
    activeArmRot = -32.0;
    armDx = 18;
    armDy = -45;
  } else if (armPose === "explaining_gesture") {
    // Dynamic speaking gesture
    activeArmRot = -12.0 + armRotDeg;
    armDx = 8;
    armDy = -16;
  }

  // 3. Select Mouth Asset
  let mouthFile = "mouth_closed.png";
  if (expression === "surprised") {
    mouthFile = "mouth_surprised.png";
  } else if (expression === "thinking") {
    mouthFile = "mouth_thinking.png";
  } else {
    switch (viseme) {
      case "slight":
        mouthFile = "mouth_slight.png";
        break;
      case "open":
        mouthFile = "mouth_open.png";
        break;
      case "round":
        mouthFile = "mouth_round.png";
        break;
      case "closed":
      default:
        mouthFile = "mouth_closed.png";
        break;
    }
  }

  // 4. Base Image: Open vs. Blinking
  const baseCutout =
    isBlinking && blinkAlpha > 0.35
      ? "character_blinking.png"
      : "character_cutout_transparent.png";

  return (
    <div
      style={{
        position: "relative",
        width: 2048,
        height: 2048,
        transform: `translateY(${breathDy + headNodDy}px) rotate(${headTiltDeg}deg)`,
        transformOrigin: "1040px 1400px",
        willChange: "transform",
      }}
    >
      {/* Layer 1: Base Character Cutout */}
      <Img
        src={staticFile(`character/${baseCutout}`)}
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: 2048,
          height: 2048,
          pointerEvents: "none",
        }}
      />

      {/* Layer 2: Gaze-Controlled Pupils (rendered behind glasses, visible when eyes open) */}
      {!isBlinking && (
        <>
          {/* Left Eye Pupil (Viewer's Left / Character's Right) */}
          <div
            style={{
              position: "absolute",
              left: 855,
              top: 720,
              width: 58,
              height: 48,
              overflow: "hidden",
              borderRadius: "50%",
              pointerEvents: "none",
            }}
          >
            <Img
              src={staticFile("character/pupil_left.png")}
              style={{
                position: "absolute",
                left: 7 + gazeX,
                top: 4 + gazeY,
                width: 44,
                height: 44,
                transition: "transform 0.08s ease-out",
              }}
            />
          </div>

          {/* Right Eye Pupil (Viewer's Right / Character's Left) */}
          <div
            style={{
              position: "absolute",
              left: 1180,
              top: 720,
              width: 58,
              height: 48,
              overflow: "hidden",
              borderRadius: "50%",
              pointerEvents: "none",
            }}
          >
            <Img
              src={staticFile("character/pupil_right.png")}
              style={{
                position: "absolute",
                left: 7 + gazeX,
                top: 4 + gazeY,
                width: 44,
                height: 44,
                transition: "transform 0.08s ease-out",
              }}
            />
          </div>
        </>
      )}

      {/* Layer 3: Articulated Eyebrows (Dynamic Translation & Tilting) */}
      {/* Left Eyebrow */}
      <div
        style={{
          position: "absolute",
          left: 820,
          top: 665,
          width: 140,
          height: 60,
          transform: `translateY(${leftBrowDy}px) rotate(${leftBrowRot}deg)`,
          transformOrigin: "center center",
          pointerEvents: "none",
          transition: "transform 0.2s ease-out",
        }}
      >
        <Img
          src={staticFile("character/eyebrow_left.png")}
          style={{ width: "100%", height: "100%" }}
        />
      </div>

      {/* Right Eyebrow */}
      <div
        style={{
          position: "absolute",
          left: 1130,
          top: 665,
          width: 140,
          height: 60,
          transform: `translateY(${rightBrowDy}px) rotate(${rightBrowRot}deg)`,
          transformOrigin: "center center",
          pointerEvents: "none",
          transition: "transform 0.2s ease-out",
        }}
      >
        <Img
          src={staticFile("character/eyebrow_right.png")}
          style={{ width: "100%", height: "100%" }}
        />
      </div>

      {/* Layer 4: Soft-Masked Parametric Mouth / Viseme */}
      <div
        style={{
          position: "absolute",
          left: 950,
          top: 920,
          width: 260,
          height: 140,
          pointerEvents: "none",
          maskImage:
            "radial-gradient(ellipse at center, black 45%, transparent 72%)",
          WebkitMaskImage:
            "radial-gradient(ellipse at center, black 45%, transparent 72%)",
        }}
      >
        <Img
          src={staticFile(`character/${mouthFile}`)}
          style={{ width: "100%", height: "100%" }}
        />
      </div>

      {/* Layer 5: Dynamic Articulated Right Arm & Pencil */}
      {Math.abs(activeArmRot) > 0.5 && (
        <div
          style={{
            position: "absolute",
            left: 399 + armDx,
            top: 1167 + armDy,
            width: 476,
            height: 368,
            transform: `rotate(${activeArmRot}deg)`,
            transformOrigin: "61px 33px", // Relative shoulder pivot in cropped arm space
            pointerEvents: "none",
            transition: "transform 0.15s ease-out",
          }}
        >
          <Img
            src={staticFile("character/arm_pencil_layer.png")}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
      )}
    </div>
  );
};
