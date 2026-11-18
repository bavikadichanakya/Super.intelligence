import React from "react";

export interface StudioEnvironmentProps {
  keyLightIntensity?: number; // 0.0 to 2.0
  rimLightIntensity?: number;
}

export const StudioEnvironment: React.FC<StudioEnvironmentProps> = ({
  keyLightIntensity = 1.0,
  rimLightIntensity = 1.0,
}) => {
  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        background:
          "radial-gradient(circle at 50% 28%, #161D2B 0%, #0C1017 55%, #05070A 100%)",
        overflow: "hidden",
      }}
    >
      {/* 1. Warm Key Light Cone (Upper Center-Right) */}
      <div
        style={{
          position: "absolute",
          top: -150,
          right: "15%",
          width: 800,
          height: 800,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(255, 185, 95, 0.12) 0%, rgba(255, 150, 50, 0.03) 50%, transparent 75%)",
          filter: "blur(60px)",
          opacity: keyLightIntensity,
          pointerEvents: "none",
        }}
      />

      {/* 2. Cool Rim Light Kicker (Upper Left) */}
      <div
        style={{
          position: "absolute",
          top: -100,
          left: "10%",
          width: 650,
          height: 650,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(0, 229, 255, 0.08) 0%, rgba(0, 180, 255, 0.02) 55%, transparent 75%)",
          filter: "blur(70px)",
          opacity: rimLightIntensity,
          pointerEvents: "none",
        }}
      />

      {/* 3. Subtle Depth Bokeh Circles */}
      <div
        style={{
          position: "absolute",
          top: "22%",
          left: "18%",
          width: 280,
          height: 280,
          borderRadius: "50%",
          background: "rgba(255, 170, 0, 0.03)",
          filter: "blur(40px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "35%",
          right: "14%",
          width: 320,
          height: 320,
          borderRadius: "50%",
          background: "rgba(16, 185, 129, 0.025)",
          filter: "blur(50px)",
        }}
      />

      {/* 4. Floor Vignette / Ground Horizon */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          width: "100%",
          height: 500,
          background:
            "linear-gradient(to top, rgba(3, 4, 6, 0.95) 0%, rgba(3, 4, 6, 0.4) 60%, transparent 100%)",
          pointerEvents: "none",
        }}
      />
    </div>
  );
};
