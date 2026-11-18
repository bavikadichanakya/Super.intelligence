import React from "react";
import { AbsoluteFill } from "remotion";
import { Character3DScene } from "../components/Character3DScene";

export const Character3DValidationComposition: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#b5b0a8" }}>
      <Character3DScene />
    </AbsoluteFill>
  );
};
