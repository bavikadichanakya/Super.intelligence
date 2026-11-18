import React, { useEffect, useRef, useState } from "react";
import {
  continueRender,
  delayRender,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { CHARACTER_GLB_BASE64 } from "../assets/characterGlbBase64";

interface CharacterNodes {
  root: THREE.Group;
  headMesh: THREE.Mesh | null;
  boneHead: THREE.Object3D | null;
  boneNeck: THREE.Object3D | null;
  boneChest: THREE.Object3D | null;
  boneEyeL: THREE.Object3D | null;
  boneEyeR: THREE.Object3D | null;
  boneBrowL: THREE.Object3D | null;
  boneBrowR: THREE.Object3D | null;
  upperLidL: THREE.Mesh | null;
  upperLidR: THREE.Mesh | null;
  boneUpperArmL: THREE.Object3D | null;
  boneForearmL: THREE.Object3D | null;
  boneHandL: THREE.Object3D | null;
  boneUpperArmR: THREE.Object3D | null;
  boneForearmR: THREE.Object3D | null;
  boneHandR: THREE.Object3D | null;
  notebook: THREE.Object3D | null;
  pencil: THREE.Object3D | null;
}

interface Character3DSceneProps {
  preset?: 'validation' | 'front' | 'three_quarter' | 'side' | 'full_body';
}

export const Character3DScene: React.FC<Character3DSceneProps> = ({ preset = 'validation' }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [nodes, setNodes] = useState<CharacterNodes | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const handleRef = useRef<number | null>(null);

  // Initialize Scene, Renderer, and Load 3D Model
  useEffect(() => {
    const handle = delayRender("Loading Kavi 3D GLB Model");
    handleRef.current = handle;

    if (!canvasRef.current) return;

    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = new THREE.Color(0xb5b0a8); // Warm photographic studio grey matching Character 3D.mp4

    const camera = new THREE.PerspectiveCamera(35, width / height, 0.1, 100);
    camera.position.set(0, 1.18, 2.45);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      antialias: true,
      alpha: false,
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(1);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.12;
    rendererRef.current = renderer;

    // Studio Lighting matching Character 3D.mp4
    const ambientLight = new THREE.AmbientLight(0xfff6ee, 0.85);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xfff5eb, 2.2);
    keyLight.position.set(2.2, 3.2, 2.8);
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0xdde8ff, 1.1);
    fillLight.position.set(-2.8, 1.8, 2.0);
    scene.add(fillLight);

    const rimLight = new THREE.DirectionalLight(0xffaa55, 3.2); // Warm golden-amber hair rim
    rimLight.position.set(0, 4.0, -3.0);
    scene.add(rimLight);

    // Studio Ground Shadow Disc
    const groundGeom = new THREE.CircleGeometry(1.8, 32);
    groundGeom.rotateX(-Math.PI / 2);
    const groundMat = new THREE.MeshBasicMaterial({
      color: 0x6e685f,
      transparent: true,
      opacity: 0.35,
    });
    const ground = new THREE.Mesh(groundGeom, groundMat);
    ground.position.y = -0.01;
    scene.add(ground);

    // Soft Studio Vignette Backdrop Glow
    const backGlowGeom = new THREE.PlaneGeometry(8, 12);
    const backGlowMat = new THREE.MeshBasicMaterial({
      color: 0xc4beb4,
      transparent: true,
      opacity: 0.65,
    });
    const backGlow = new THREE.Mesh(backGlowGeom, backGlowMat);
    backGlow.position.set(0, 1.5, -4);
    scene.add(backGlow);

    // Decode Base64 GLB Buffer
    const binaryString = atob(CHARACTER_GLB_BASE64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    const loader = new GLTFLoader();
    loader.parse(
      bytes.buffer,
      "",
      (gltf) => {
        const model = gltf.scene;
        scene.add(model);

        const foundNodes: CharacterNodes = {
          root: model,
          headMesh: null,
          boneHead: null,
          boneNeck: null,
          boneChest: null,
          boneEyeL: null,
          boneEyeR: null,
          boneBrowL: null,
          boneBrowR: null,
          upperLidL: null,
          upperLidR: null,
          boneUpperArmL: null,
          boneForearmL: null,
          boneHandL: null,
          boneUpperArmR: null,
          boneForearmR: null,
          boneHandR: null,
          notebook: null,
          pencil: null,
        };

        model.traverse((node) => {
          if (node.name === "Mesh_Head") foundNodes.headMesh = node as THREE.Mesh;
          if (node.name === "Bone_Head") foundNodes.boneHead = node;
          if (node.name === "Bone_Neck") foundNodes.boneNeck = node;
          if (node.name === "Bone_Chest") foundNodes.boneChest = node;
          if (node.name === "Bone_Eye_L") foundNodes.boneEyeL = node;
          if (node.name === "Bone_Eye_R") foundNodes.boneEyeR = node;
          if (node.name === "Bone_Brow_L") foundNodes.boneBrowL = node;
          if (node.name === "Bone_Brow_R") foundNodes.boneBrowR = node;
          if (node.name === "Mesh_UpperLid_L") foundNodes.upperLidL = node as THREE.Mesh;
          if (node.name === "Mesh_UpperLid_R") foundNodes.upperLidR = node as THREE.Mesh;
          if (node.name === "Bone_UpperArm_L") foundNodes.boneUpperArmL = node;
          if (node.name === "Bone_Forearm_L") foundNodes.boneForearmL = node;
          if (node.name === "Bone_Hand_L") foundNodes.boneHandL = node;
          if (node.name === "Bone_UpperArm_R") foundNodes.boneUpperArmR = node;
          if (node.name === "Bone_Forearm_R") foundNodes.boneForearmR = node;
          if (node.name === "Bone_Hand_R") foundNodes.boneHandR = node;
          if (node.name === "Prop_Technical_Notebook") foundNodes.notebook = node;
          if (node.name === "Prop_Drafting_Pencil") foundNodes.pencil = node;
        });

        setNodes(foundNodes);
        continueRender(handle);
      },
      (err) => {
        console.error("Failed to parse GLB in Remotion:", err);
        continueRender(handle);
      }
    );

    return () => {
      renderer.dispose();
    };
  }, [width, height]);

  // Frame-by-Frame Kinematics and Animation Loop (540 frames, 18.0s @ 30fps)
  useEffect(() => {
    if (!nodes || !rendererRef.current || !sceneRef.current || !cameraRef.current) return;

    const {
      headMesh,
      boneHead,
      boneChest,
      boneEyeL,
      boneEyeR,
      boneBrowL,
      boneBrowR,
      upperLidL,
      upperLidR,
      boneUpperArmL,
      boneForearmL,
      boneUpperArmR,
      boneForearmR,
    } = nodes;

    const camera = cameraRef.current;
    const scene = sceneRef.current;
    const renderer = rendererRef.current;

    // Reset eyelids and brows to neutral
    if (upperLidL) upperLidL.rotation.x = 0;
    if (upperLidR) upperLidR.rotation.x = 0;
    if (boneBrowL) {
      boneBrowL.position.y = 0.105;
      boneBrowL.position.x = 0.082;
    }
    if (boneBrowR) {
      boneBrowR.position.y = 0.105;
      boneBrowR.position.x = -0.082;
    }

    // Helper to safely set morph target influence and propagate to armature nodes
    const setMorph = (name: string, val: number) => {
      const clamped = Math.max(0, Math.min(1, val));
      if (headMesh && headMesh.morphTargetDictionary && headMesh.morphTargetInfluences) {
        const idx = headMesh.morphTargetDictionary[name];
        if (idx !== undefined) {
          headMesh.morphTargetInfluences[idx] = clamped;
        }
      }
      if (name === "browLeftUp" && boneBrowL) {
        boneBrowL.position.y = 0.105 + clamped * 0.015;
      }
      if (name === "browRightUp" && boneBrowR) {
        boneBrowR.position.y = 0.105 + clamped * 0.015;
      }
      if (name === "browFurrow") {
        if (boneBrowL) boneBrowL.position.x = 0.082 - clamped * 0.008;
        if (boneBrowR) boneBrowR.position.x = -0.082 + clamped * 0.008;
      }
    };

    // Reset all morphs to 0 baseline
    if (headMesh && headMesh.morphTargetInfluences) {
      for (let i = 0; i < headMesh.morphTargetInfluences.length; i++) {
        headMesh.morphTargetInfluences[i] = 0;
      }
    }

    // Baseline Breathing & Posture
    const breath = Math.sin(frame * 0.08) * 0.015;
    if (boneChest) {
      boneChest.position.y = 0.45 + breath;
    }

    // Default Arm Poses (Naturally framing torso with hands in front)
    let lUpperArmZ = -0.25;
    let lUpperArmX = -0.22; // Elbows forward, NOT backwards!
    let lForearmX = -1.15; // Forearm bent up holding notebook at chest
    let lForearmZ = 0.25;

    let rUpperArmZ = 0.22;
    let rUpperArmX = -0.18; // Elbow forward
    let rForearmX = -0.85; // Forearm raised ready to gesture
    let rForearmY = -0.20;

    let headYaw = 0;
    let headPitch = 0;
    let headRoll = 0;

    let gazeX = 0;
    let gazeY = 0;

    let camY = 1.22;
    let camZ = 2.45;
    let targetY = 1.20;

    // -------------------------------------------------------------
    // 10-Step Animation Progression
    // -------------------------------------------------------------

    // 1. Frames 0-45 (0.0s-1.5s): Neutral Standing Pose
    if (frame < 45) {
      camY = 1.22;
      camZ = 2.45;
      targetY = 1.20;
      headYaw = 0;
      headPitch = 0;
      gazeX = 0;
      gazeY = 0;
      setMorph("mouthSmile", 0.15); // Calm resting warmth
    }

    // 2. Frames 45-90 (1.5s-3.0s): Head Rotation (3D Volume & Angles)
    else if (frame < 90) {
      const p = (frame - 45) / 45;
      headYaw = Math.sin(p * Math.PI * 2) * 0.38; // Sweeps left and right (+/- 22 deg)
      headRoll = Math.sin(p * Math.PI) * 0.06;
      headPitch = Math.cos(p * Math.PI * 2) * 0.05;
      gazeX = -headYaw * 0.5; // Compensatory gaze maintaining contact
      setMorph("mouthSmile", 0.2);
    }

    // 3. Frames 90-150 (3.0s-5.0s): Eye Tracking (Object Inspection)
    else if (frame < 150) {
      const p = (frame - 90) / 60;
      // Eyes track smoothly to the right (+X), hold, then snap back
      if (p < 0.3) {
        gazeX = interpolate(p, [0, 0.3], [0, 0.32]);
        gazeY = interpolate(p, [0, 0.3], [0, -0.12]);
        headYaw = interpolate(p, [0, 0.3], [0, 0.12]);
      } else if (p < 0.75) {
        gazeX = 0.32;
        gazeY = -0.12;
        headYaw = 0.12;
      } else {
        gazeX = interpolate(p, [0.75, 1.0], [0.32, 0]);
        gazeY = interpolate(p, [0.75, 1.0], [-0.12, 0]);
        headYaw = interpolate(p, [0.75, 1.0], [0.12, 0]);
      }
      setMorph("mouthSmile", 0.15);
    }

    // 4. Frames 150-180 (5.0s-6.0s): Natural Blink Cycle (150ms)
    else if (frame < 180) {
      const blinkFrame = frame - 150;
      // 5-frame cosine blink curve around frame 160
      if (blinkFrame >= 8 && blinkFrame <= 13) {
        const b = Math.sin(((blinkFrame - 8) / 5) * Math.PI);
        setMorph("blinkLeft", b);
        setMorph("blinkRight", b);
        if (upperLidL) upperLidL.rotation.x = b * 0.85;
        if (upperLidR) upperLidR.rotation.x = b * 0.85;
      }
      setMorph("mouthSmile", 0.2);
    }

    // 5. Frames 180-240 (6.0s-8.0s): Curious Expression (Close-Up Transition)
    else if (frame < 240) {
      const p = (frame - 180) / 60;
      // Zoom into medium close-up
      camZ = interpolate(p, [0, 1], [2.45, 1.85]);
      camY = interpolate(p, [0, 1], [1.22, 1.32]);
      targetY = interpolate(p, [0, 1], [1.20, 1.32]);

      headRoll = 0.12; // Inquiring lateral tilt
      headYaw = -0.08;
      headPitch = -0.05;
      gazeX = 0.05;

      setMorph("browRightUp", 0.85); // Asymmetric brow raise
      setMorph("browLeftUp", 0.15);
      setMorph("mouthSmile", 0.4);
      setMorph("mouthOpen", 0.08);
    }

    // 6. Frames 240-300 (8.0s-10.0s): Surprised Expression (Dynamic Recoil)
    else if (frame < 300) {
      const p = (frame - 240) / 60;
      camZ = 1.85;
      camY = 1.32;
      targetY = 1.32;

      if (p < 0.2) {
        // Fast recoil attack
        headPitch = interpolate(p, [0, 0.2], [0, 0.14]);
        setMorph("jawDropWide", interpolate(p, [0, 0.2], [0, 0.85]));
        setMorph("mouthPucker", interpolate(p, [0, 0.2], [0, 0.65]));
        setMorph("browLeftUp", interpolate(p, [0, 0.2], [0, 0.95]));
        setMorph("browRightUp", interpolate(p, [0, 0.2], [0, 0.95]));
      } else if (p < 0.7) {
        headPitch = 0.12;
        setMorph("jawDropWide", 0.85);
        setMorph("mouthPucker", 0.65);
        setMorph("browLeftUp", 0.95);
        setMorph("browRightUp", 0.95);
      } else {
        // Gentle decay
        headPitch = interpolate(p, [0.7, 1.0], [0.12, 0]);
        setMorph("jawDropWide", interpolate(p, [0.7, 1.0], [0.85, 0.2]));
        setMorph("mouthPucker", interpolate(p, [0.7, 1.0], [0.65, 0.1]));
        setMorph("browLeftUp", interpolate(p, [0.7, 1.0], [0.95, 0.3]));
        setMorph("browRightUp", interpolate(p, [0.7, 1.0], [0.95, 0.3]));
      }
    }

    // 7. Frames 300-375 (10.0s-12.5s): Explaining Gesture (Pencil Pointing & Visemes)
    else if (frame < 375) {
      const p = (frame - 300) / 75;
      camZ = interpolate(p, [0, 1], [1.85, 2.30]);
      camY = interpolate(p, [0, 1], [1.32, 1.22]);
      targetY = 1.20;

      // Active conversational visemes
      const viseme = Math.max(0, Math.sin(frame * 0.65)) * 0.6;
      setMorph("mouthOpen", viseme);
      setMorph("mouthSmile", 0.25);
      setMorph("browLeftUp", 0.35 + Math.sin(frame * 0.3) * 0.15);
      setMorph("browRightUp", 0.35 + Math.sin(frame * 0.3) * 0.15);

      // Articulate right arm forward pointing toward viewer
      rUpperArmX = interpolate(p, [0, 0.4], [-0.18, -0.45]);
      rUpperArmZ = interpolate(p, [0, 0.4], [0.22, 0.42]);
      rForearmX = interpolate(p, [0, 0.4], [-0.85, -0.65]);
      rForearmY = interpolate(p, [0, 0.4], [-0.20, -0.30]);
    }

    // 8. Frames 375-435 (12.5s-14.5s): Both-Arm Movement (Notebook Showcase)
    else if (frame < 435) {
      const p = (frame - 375) / 60;
      camZ = 2.35;
      camY = 1.22;
      targetY = 1.20;

      // Right arm conversational waving gesture forward in front of torso
      rUpperArmX = -0.40 + Math.sin(frame * 0.25) * 0.08;
      rUpperArmZ = 0.32;
      rForearmX = -0.75 + Math.cos(frame * 0.25) * 0.12;

      // Left arm raises notebook higher to present to audience
      lUpperArmX = interpolate(p, [0, 0.5], [-0.22, -0.38]);
      lUpperArmZ = -0.22;
      lForearmX = interpolate(p, [0, 0.5], [-1.15, -1.35]);

      setMorph("mouthSmile", 0.45);
      setMorph("mouthOpen", Math.max(0, Math.sin(frame * 0.5)) * 0.3);
      setMorph("browLeftUp", 0.4);
      setMorph("browRightUp", 0.4);
    }

    // 9. Frames 435-495 (14.5s-16.5s): Notebook Interaction (Writing / Inspection)
    else if (frame < 495) {
      const p = (frame - 435) / 60;
      camZ = 2.15;
      camY = 1.25;
      targetY = 1.20;

      // Look down at notebook
      if (p < 0.6) {
        headPitch = interpolate(p, [0, 0.3], [0, -0.28]);
        headYaw = interpolate(p, [0, 0.3], [0, -0.12]);
        gazeY = -0.22;
        gazeX = -0.12;

        // Bring right hand & pencil close to notebook page as if writing in front of chest
        rUpperArmX = -0.35;
        rUpperArmZ = 0.08; // Across body toward left side notebook
        rForearmX = -1.22 + Math.sin(frame * 0.8) * 0.04;
        rForearmY = 0.32;

        lUpperArmX = -0.30;
        lUpperArmZ = -0.22;
        lForearmX = -1.25;

        setMorph("mouthPucker", 0.25); // Thoughtful focus
        setMorph("browFurrow", 0.35);
      } else {
        // Look back up to camera confidently
        headPitch = interpolate(p, [0.6, 1.0], [-0.28, 0]);
        headYaw = interpolate(p, [0.6, 1.0], [-0.12, 0]);
        gazeY = interpolate(p, [0.6, 1.0], [-0.22, 0]);
        gazeX = interpolate(p, [0.6, 1.0], [-0.12, 0]);

        // Right hand relaxes back
        rUpperArmX = interpolate(p, [0.6, 1.0], [-0.35, -0.18]);
        rUpperArmZ = interpolate(p, [0.6, 1.0], [0.08, 0.22]);
        rForearmX = interpolate(p, [0.6, 1.0], [-1.22, -0.85]);
        rForearmY = interpolate(p, [0.6, 1.0], [0.32, -0.20]);

        lUpperArmX = interpolate(p, [0.6, 1.0], [-0.30, -0.22]);
        lUpperArmZ = -0.25;
        lForearmX = interpolate(p, [0.6, 1.0], [-1.25, -1.15]);

        setMorph("mouthSmile", 0.55); // Confident smile
        setMorph("browFurrow", 0);
      }
    }

    // 10. Frames 495-540 (16.5s-18.0s): Return to Neutral Hero Anchor
    else {
      const p = (frame - 495) / 45;
      camZ = interpolate(p, [0, 1], [2.15, 2.45]);
      camY = interpolate(p, [0, 1], [1.25, 1.22]);
      targetY = 1.20;

      headPitch = 0;
      headYaw = 0;
      headRoll = 0;
      gazeX = 0;
      gazeY = 0;

      rUpperArmX = -0.18;
      rUpperArmZ = 0.22;
      rForearmX = -0.85;
      rForearmY = -0.20;

      lUpperArmX = -0.22;
      lUpperArmZ = -0.25;
      lForearmX = -1.15;

      setMorph("mouthSmile", interpolate(p, [0, 1], [0.65, 0.2]));
    }

    // Apply Computed Transforms to Armature Nodes
    if (boneHead) {
      boneHead.rotation.x = headPitch;
      boneHead.rotation.y = headYaw;
      boneHead.rotation.z = headRoll;
    }

    if (boneEyeL) {
      boneEyeL.rotation.y = gazeX;
      boneEyeL.rotation.x = gazeY;
    }
    if (boneEyeR) {
      boneEyeR.rotation.y = gazeX;
      boneEyeR.rotation.x = gazeY;
    }

    if (boneUpperArmL) {
      boneUpperArmL.rotation.x = lUpperArmX;
      boneUpperArmL.rotation.z = lUpperArmZ;
    }
    if (boneForearmL) {
      boneForearmL.rotation.x = lForearmX;
      boneForearmL.rotation.z = lForearmZ;
    }

    if (boneUpperArmR) {
      boneUpperArmR.rotation.x = rUpperArmX;
      boneUpperArmR.rotation.z = rUpperArmZ;
    }
    if (boneForearmR) {
      boneForearmR.rotation.x = rForearmX;
      boneForearmR.rotation.y = rForearmY;
    }

    // Preset Camera & Angle Overrides
    if (preset === 'three_quarter') {
      camera.position.set(1.10, 1.22, 2.15);
      camera.lookAt(0, 1.20, 0);
      if (boneHead) {
        boneHead.rotation.set(0, 0.24, 0);
      }
      setMorph('mouthSmile', 0.25);
      renderer.render(scene, camera);
      return;
    }
    if (preset === 'side') {
      camera.position.set(2.35, 1.22, 0.05);
      camera.lookAt(0, 1.20, 0);
      if (boneHead) {
        boneHead.rotation.set(0, 0, 0);
      }
      setMorph('mouthSmile', 0.20);
      renderer.render(scene, camera);
      return;
    }
    if (preset === 'full_body') {
      camera.position.set(0, 0.95, 3.40);
      camera.lookAt(0, 0.85, 0);
      if (boneHead) {
        boneHead.rotation.set(0, 0, 0);
      }
      setMorph('mouthSmile', 0.25);
      renderer.render(scene, camera);
      return;
    }

    // Camera Framing Update
    camera.position.set(0, camY, camZ);
    camera.lookAt(0, targetY, 0);

    // Render 3D Frame
    renderer.render(scene, camera);
  }, [frame, nodes, preset]);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        background: "#0c0e14",
        overflow: "hidden",
      }}
    >
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        style={{
          width: "100%",
          height: "100%",
          display: "block",
        }}
      />
    </div>
  );
};
