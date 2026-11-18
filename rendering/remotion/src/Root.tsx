import React from "react";
import { Composition } from "remotion";
import { ExperimentAComposition } from "./compositions/ExperimentAComposition";
import { Character3DValidationComposition } from "./compositions/Character3DValidationComposition";
import { Character3DScene } from "./components/Character3DScene";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Character3DValidation"
        component={Character3DValidationComposition}
        durationInFrames={540}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CharacterFront"
        component={() => <Character3DScene preset="front" />}
        durationInFrames={1}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CharacterThreeQuarter"
        component={() => <Character3DScene preset="three_quarter" />}
        durationInFrames={1}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CharacterSide"
        component={() => <Character3DScene preset="side" />}
        durationInFrames={1}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CharacterFullBody"
        component={() => <Character3DScene preset="full_body" />}
        durationInFrames={1}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="ExperimentA"
        component={ExperimentAComposition}
        durationInFrames={540}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
