/**
 * SUPER.INTELLIGENCEEE — 3D Character Model Generator (Stage B & C)
 * 
 * Generates the canonical 3D character (Kavi) as a genuine GLB asset:
 * - Proper 3D head geometry, cheeks, jawline, chin, nose, ears, neck
 * - Volumetric curly dark hair clusters with 360-degree depth
 * - Sculpted beard and moustache conforming to jaw and upper lip
 * - Independent 3D eye spheres with full gaze tracking kinematics
 * - 3D rectangular acetate glasses with bridge, nose pads, and temples
 * - Full facial morph targets (blendshapes) for 9 expressive states + visemes
 * - Charcoal technical jacket with safety orange trim and collar
 * - Articulated arms (upper arm, elbow, forearm, wrist, 5-finger hands)
 * - Removable / reusable props: Spiral notebook and drafting pencil
 * - Hierarchical skeletal bipedal rig with named control nodes
 */

import * as THREE from 'three';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js';
import fs from 'fs';
import path from 'path';

// Polyfill FileReader for Node.js GLTFExporter
class FileReaderPolyfill {
  readAsArrayBuffer(blob) {
    blob.arrayBuffer().then((ab) => {
      this.result = ab;
      if (this.onloadend) this.onloadend();
    });
  }
}
globalThis.FileReader = FileReaderPolyfill;

console.log('--- Initializing Kavi 3D Character Generation ---');

// 1. Materials Palette
const materials = {
  skin: new THREE.MeshStandardMaterial({
    name: 'mat_skin',
    color: 0xc48c66, // Warm golden-brown / olive skin tone
    roughness: 0.65,
    metalness: 0.05,
    bumpScale: 0.01,
  }),
  hair: new THREE.MeshStandardMaterial({
    name: 'mat_hair',
    color: 0x181818, // Dense dark black hair
    roughness: 0.85,
    metalness: 0.08,
  }),
  beard: new THREE.MeshStandardMaterial({
    name: 'mat_beard',
    color: 0x1a1a1a,
    roughness: 0.88,
    metalness: 0.05,
  }),
  glassesFrame: new THREE.MeshStandardMaterial({
    name: 'mat_glasses_frame',
    color: 0x1a1b1e, // Dark charcoal acetate
    roughness: 0.25,
    metalness: 0.15,
  }),
  glassesLens: new THREE.MeshPhysicalMaterial({
    name: 'mat_glasses_lens',
    color: 0xffffff,
    transmission: 0.85,
    opacity: 0.4,
    transparent: true,
    roughness: 0.1,
    ior: 1.5,
  }),
  sclera: new THREE.MeshStandardMaterial({
    name: 'mat_sclera',
    color: 0xf4f4f6,
    roughness: 0.2,
    metalness: 0.0,
  }),
  iris: new THREE.MeshStandardMaterial({
    name: 'mat_iris',
    color: 0x3d2314, // Deep warm brown iris
    roughness: 0.3,
    metalness: 0.0,
  }),
  pupil: new THREE.MeshStandardMaterial({
    name: 'mat_pupil',
    color: 0x080808,
    roughness: 0.1,
    metalness: 0.0,
  }),
  jacketCharcoal: new THREE.MeshStandardMaterial({
    name: 'mat_jacket_charcoal',
    color: 0x2b2e34, // Signature matte charcoal grey
    roughness: 0.82,
    metalness: 0.1,
  }),
  jacketOrangeTrim: new THREE.MeshStandardMaterial({
    name: 'mat_jacket_orange',
    color: 0xff6b00, // Signature safety / warm orange piping
    roughness: 0.45,
    metalness: 0.15,
  }),
  innerShirt: new THREE.MeshStandardMaterial({
    name: 'mat_inner_shirt',
    color: 0x141416,
    roughness: 0.9,
    metalness: 0.05,
  }),
  notebookCover: new THREE.MeshStandardMaterial({
    name: 'mat_notebook_cover',
    color: 0x242830,
    roughness: 0.7,
    metalness: 0.1,
  }),
  notebookPages: new THREE.MeshStandardMaterial({
    name: 'mat_notebook_pages',
    color: 0xede8dc, // Cream / off-white paper
    roughness: 0.85,
    metalness: 0.0,
  }),
  notebookWire: new THREE.MeshStandardMaterial({
    name: 'mat_notebook_wire',
    color: 0xd0d4dc, // Silver wire spiral
    roughness: 0.25,
    metalness: 0.8,
  }),
  pencilBody: new THREE.MeshStandardMaterial({
    name: 'mat_pencil_body',
    color: 0xf5b82e, // Classic yellow drafting pencil
    roughness: 0.4,
    metalness: 0.1,
  }),
  pencilFerrule: new THREE.MeshStandardMaterial({
    name: 'mat_pencil_ferrule',
    color: 0xc8c8c8,
    roughness: 0.2,
    metalness: 0.85,
  }),
  pencilLead: new THREE.MeshStandardMaterial({
    name: 'mat_pencil_lead',
    color: 0x222222,
    roughness: 0.5,
    metalness: 0.2,
  }),
};

// Root Armature Group
const characterRoot = new THREE.Group();
characterRoot.name = 'Kavi_Character_Root';

// 2. Skeletal Hierarchy (Bones)
const boneHips = new THREE.Bone();
boneHips.name = 'Bone_Hips';
boneHips.position.set(0, 0, 0);
characterRoot.add(boneHips);

const boneSpine = new THREE.Bone();
boneSpine.name = 'Bone_Spine';
boneSpine.position.set(0, 0.5, 0);
boneHips.add(boneSpine);

const boneChest = new THREE.Bone();
boneChest.name = 'Bone_Chest';
boneChest.position.set(0, 0.45, 0);
boneSpine.add(boneChest);

const boneNeck = new THREE.Bone();
boneNeck.name = 'Bone_Neck';
boneNeck.position.set(0, 0.45, 0);
boneChest.add(boneNeck);

const boneHead = new THREE.Bone();
boneHead.name = 'Bone_Head';
boneHead.position.set(0, 0.28, 0);
boneNeck.add(boneHead);

// Eye Control Nodes (Gaze Kinematics)
const boneEyeL = new THREE.Bone();
boneEyeL.name = 'Bone_Eye_L';
boneEyeL.position.set(0.18, 0.08, 0.42);
boneHead.add(boneEyeL);

const boneEyeR = new THREE.Bone();
boneEyeR.name = 'Bone_Eye_R';
boneEyeR.position.set(-0.18, 0.08, 0.42);
boneHead.add(boneEyeR);

// Eyebrow Control Nodes
const boneBrowL = new THREE.Bone();
boneBrowL.name = 'Bone_Brow_L';
boneBrowL.position.set(0.18, 0.26, 0.46);
boneHead.add(boneBrowL);

const boneBrowR = new THREE.Bone();
boneBrowR.name = 'Bone_Brow_R';
boneBrowR.position.set(-0.18, 0.26, 0.46);
boneHead.add(boneBrowR);

// Left Arm Chain
const boneClavicleL = new THREE.Bone();
boneClavicleL.name = 'Bone_Clavicle_L';
boneClavicleL.position.set(0.2, 0.35, 0);
boneChest.add(boneClavicleL);

const boneUpperArmL = new THREE.Bone();
boneUpperArmL.name = 'Bone_UpperArm_L';
boneUpperArmL.position.set(0.28, 0, 0);
boneClavicleL.add(boneUpperArmL);

const boneForearmL = new THREE.Bone();
boneForearmL.name = 'Bone_Forearm_L';
boneForearmL.position.set(0, -0.42, 0);
boneUpperArmL.add(boneForearmL);

const boneHandL = new THREE.Bone();
boneHandL.name = 'Bone_Hand_L';
boneHandL.position.set(0, -0.38, 0);
boneForearmL.add(boneHandL);

const propSocketNotebook = new THREE.Group();
propSocketNotebook.name = 'PropSocket_Notebook';
propSocketNotebook.position.set(0.05, -0.05, 0.08);
boneHandL.add(propSocketNotebook);

// Right Arm Chain
const boneClavicleR = new THREE.Bone();
boneClavicleR.name = 'Bone_Clavicle_R';
boneClavicleR.position.set(-0.2, 0.35, 0);
boneChest.add(boneClavicleR);

const boneUpperArmR = new THREE.Bone();
boneUpperArmR.name = 'Bone_UpperArm_R';
boneUpperArmR.position.set(-0.28, 0, 0);
boneClavicleR.add(boneUpperArmR);

const boneForearmR = new THREE.Bone();
boneForearmR.name = 'Bone_Forearm_R';
boneForearmR.position.set(0, -0.42, 0);
boneUpperArmR.add(boneForearmR);

const boneHandR = new THREE.Bone();
boneHandR.name = 'Bone_Hand_R';
boneHandR.position.set(0, -0.38, 0);
boneForearmR.add(boneHandR);

const propSocketPencil = new THREE.Group();
propSocketPencil.name = 'PropSocket_Pencil';
propSocketPencil.position.set(-0.02, -0.05, 0.05);
boneHandR.add(propSocketPencil);

// 3. Head & Facial Geometry Construction with Morph Targets
console.log('Constructing sculpted head geometry and morph targets...');

function createHeadGeometryWithMorphs() {
  const geom = new THREE.SphereGeometry(0.52, 32, 28);
  // Deform spherical base into stylized human head:
  // Taper chin and jaw, define cheekbones, temple indent, forehead
  const pos = geom.attributes.position;
  const count = pos.count;
  const basePositions = new Float32Array(pos.array.length);

  for (let i = 0; i < count; i++) {
    let x = pos.getX(i);
    let y = pos.getY(i);
    let z = pos.getZ(i);

    // Oval head elongation
    y *= 1.18;

    // Jaw tapering below y = 0
    if (y < 0) {
      const taper = 1.0 + y * 0.45;
      x *= Math.max(0.65, taper);
      z *= Math.max(0.75, 1.0 + y * 0.3);
      // Chin thrust forward slightly
      if (y < -0.35 && z > 0) {
        z += 0.08 * Math.cos((y + 0.45) * 5);
      }
    }

    // Forehead and crown widening
    if (y > 0.2) {
      x *= 1.04;
      z *= 1.02;
    }

    // Flatten back of skull slightly
    if (z < -0.2) {
      z *= 0.92;
    }

    // Set sculpted base position
    pos.setXYZ(i, x, y, z);
    basePositions[i * 3 + 0] = x;
    basePositions[i * 3 + 1] = y;
    basePositions[i * 3 + 2] = z;
  }
  geom.computeVertexNormals();

  // Morph Targets (Blendshapes)
  // 1. mouthOpen (Viseme / Speech / Surprise)
  const morphMouthOpen = new Float32Array(count * 3);
  // 2. mouthSmile (Curious / Confident / Excited)
  const morphMouthSmile = new Float32Array(count * 3);
  // 3. mouthPucker (Thinking / Surprise "O")
  const morphMouthPucker = new Float32Array(count * 3);
  // 4. mouthFrown (Confused / Skeptical)
  const morphMouthFrown = new Float32Array(count * 3);
  // 5. blinkLeft (Left Eyelid closure)
  const morphBlinkLeft = new Float32Array(count * 3);
  // 6. blinkRight (Right Eyelid closure)
  const morphBlinkRight = new Float32Array(count * 3);
  // 7. browLeftUp (Curious / Surprised)
  const morphBrowLeftUp = new Float32Array(count * 3);
  // 8. browRightUp (Surprised / Inquiring)
  const morphBrowRightUp = new Float32Array(count * 3);
  // 9. browFurrow (Thinking / Confused)
  const morphBrowFurrow = new Float32Array(count * 3);
  // 10. jawDropWide (Exaggerated Surprise)
  const morphJawDropWide = new Float32Array(count * 3);

  for (let i = 0; i < count; i++) {
    const x = basePositions[i * 3 + 0];
    const y = basePositions[i * 3 + 1];
    const z = basePositions[i * 3 + 2];

    // Mouth Region: y around -0.18 to -0.38, z > 0.35, |x| < 0.25
    const isMouth = y < -0.15 && y > -0.42 && z > 0.32 && Math.abs(x) < 0.26;
    const isLowerJaw = y < -0.25 && z > 0.15;
    const isEyeL = x > 0.08 && x < 0.32 && y > -0.05 && y < 0.22 && z > 0.35;
    const isEyeR = x < -0.08 && x > -0.32 && y > -0.05 && y < 0.22 && z > 0.35;
    const isBrowL = x > 0.06 && x < 0.34 && y > 0.18 && y < 0.38 && z > 0.36;
    const isBrowR = x < -0.06 && x > -0.34 && y > 0.18 && y < 0.38 && z > 0.36;

    // 1. mouthOpen
    if (isLowerJaw) {
      const weight = Math.max(0, 1.0 - Math.abs(x) * 3.0) * Math.max(0, (-y - 0.2) * 2.5);
      morphMouthOpen[i * 3 + 1] = -0.16 * weight;
      morphMouthOpen[i * 3 + 2] = -0.04 * weight;
    }

    // 2. mouthSmile
    if (isMouth) {
      const cornerWeight = Math.abs(x) / 0.25;
      morphMouthSmile[i * 3 + 0] = x * 0.12;
      morphMouthSmile[i * 3 + 1] = 0.06 * cornerWeight;
      morphMouthSmile[i * 3 + 2] = -0.02 * cornerWeight;
    }

    // 3. mouthPucker (O-shape)
    if (isMouth) {
      const distFromCenter = Math.sqrt(x * x + (y + 0.28) * (y + 0.28));
      const puckerWeight = Math.max(0, 1.0 - distFromCenter * 4.0);
      morphMouthPucker[i * 3 + 0] = -x * 0.35;
      morphMouthPucker[i * 3 + 1] = (-0.28 - y) * 0.2;
      morphMouthPucker[i * 3 + 2] = 0.08 * puckerWeight;
    }

    // 4. mouthFrown
    if (isMouth) {
      const cornerWeight = Math.abs(x) / 0.25;
      morphMouthFrown[i * 3 + 1] = -0.05 * cornerWeight;
    }

    // 5. blinkLeft
    if (isEyeL) {
      const eyeCenterY = 0.08;
      const distY = y - eyeCenterY;
      morphBlinkLeft[i * 3 + 1] = -distY * 0.85;
      morphBlinkLeft[i * 3 + 2] = 0.02;
    }

    // 6. blinkRight
    if (isEyeR) {
      const eyeCenterY = 0.08;
      const distY = y - eyeCenterY;
      morphBlinkRight[i * 3 + 1] = -distY * 0.85;
      morphBlinkRight[i * 3 + 2] = 0.02;
    }

    // 7. browLeftUp
    if (isBrowL) {
      morphBrowLeftUp[i * 3 + 1] = 0.08;
      morphBrowLeftUp[i * 3 + 2] = 0.02;
    }

    // 8. browRightUp
    if (isBrowR) {
      morphBrowRightUp[i * 3 + 1] = 0.08;
      morphBrowRightUp[i * 3 + 2] = 0.02;
    }

    // 9. browFurrow
    if (isBrowL) {
      morphBrowFurrow[i * 3 + 0] = -0.04;
      morphBrowFurrow[i * 3 + 1] = -0.03;
    }
    if (isBrowR) {
      morphBrowFurrow[i * 3 + 0] = 0.04;
      morphBrowFurrow[i * 3 + 1] = -0.03;
    }

    // 10. jawDropWide (Surprise / Laugh)
    if (isLowerJaw) {
      const weight = Math.max(0, 1.0 - Math.abs(x) * 2.5) * Math.max(0, (-y - 0.2) * 2.8);
      morphJawDropWide[i * 3 + 1] = -0.28 * weight;
      morphJawDropWide[i * 3 + 2] = -0.06 * weight;
    }
  }

  geom.morphAttributes.position = [
    new THREE.BufferAttribute(morphMouthOpen, 3),
    new THREE.BufferAttribute(morphMouthSmile, 3),
    new THREE.BufferAttribute(morphMouthPucker, 3),
    new THREE.BufferAttribute(morphMouthFrown, 3),
    new THREE.BufferAttribute(morphBlinkLeft, 3),
    new THREE.BufferAttribute(morphBlinkRight, 3),
    new THREE.BufferAttribute(morphBrowLeftUp, 3),
    new THREE.BufferAttribute(morphBrowRightUp, 3),
    new THREE.BufferAttribute(morphBrowFurrow, 3),
    new THREE.BufferAttribute(morphJawDropWide, 3),
  ];

  return geom;
}

const headGeom = createHeadGeometryWithMorphs();
const headMesh = new THREE.Mesh(headGeom, materials.skin);
headMesh.name = 'Mesh_Head';
headMesh.morphTargetDictionary = {
  mouthOpen: 0,
  mouthSmile: 1,
  mouthPucker: 2,
  mouthFrown: 3,
  blinkLeft: 4,
  blinkRight: 5,
  browLeftUp: 6,
  browRightUp: 7,
  browFurrow: 8,
  jawDropWide: 9,
};
headMesh.morphTargetInfluences = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
boneHead.add(headMesh);

// 4. Nose Geometry
const noseGeom = new THREE.ConeGeometry(0.065, 0.16, 12);
noseGeom.rotateX(Math.PI / 2.6);
const noseMesh = new THREE.Mesh(noseGeom, materials.skin);
noseMesh.name = 'Mesh_Nose';
noseMesh.position.set(0, -0.03, 0.49);
boneHead.add(noseMesh);

// 5. Ears Geometry
const earGeom = new THREE.CapsuleGeometry(0.065, 0.12, 8, 12);
earGeom.rotateZ(0.2);
const earMeshL = new THREE.Mesh(earGeom, materials.skin);
earMeshL.name = 'Mesh_Ear_L';
earMeshL.position.set(0.48, 0.02, -0.04);
earMeshL.rotation.y = 0.35;
boneHead.add(earMeshL);

const earMeshR = earMeshL.clone();
earMeshR.name = 'Mesh_Ear_R';
earMeshR.position.set(-0.48, 0.02, -0.04);
earMeshR.rotation.y = -0.35;
earMeshR.rotation.z = -0.2;
boneHead.add(earMeshR);

// 6. Eyes (Left and Right Independent 3D Eye Spheres)
console.log('Constructing 3D orbital eye spheres and gaze controllers...');
function createEyeMesh(name) {
  const eyeGroup = new THREE.Group();
  eyeGroup.name = name;

  // Sclera eyeball
  const scleraGeom = new THREE.SphereGeometry(0.092, 20, 20);
  const scleraMesh = new THREE.Mesh(scleraGeom, materials.sclera);
  eyeGroup.add(scleraMesh);

  // Iris
  const irisGeom = new THREE.CylinderGeometry(0.048, 0.048, 0.02, 20);
  irisGeom.rotateX(Math.PI / 2);
  const irisMesh = new THREE.Mesh(irisGeom, materials.iris);
  irisMesh.position.set(0, 0, 0.084);
  eyeGroup.add(irisMesh);

  // Pupil
  const pupilGeom = new THREE.CylinderGeometry(0.024, 0.024, 0.025, 16);
  pupilGeom.rotateX(Math.PI / 2);
  const pupilMesh = new THREE.Mesh(pupilGeom, materials.pupil);
  pupilMesh.position.set(0, 0, 0.086);
  eyeGroup.add(pupilMesh);

  // Specular Highlight Glint
  const glintGeom = new THREE.SphereGeometry(0.01, 8, 8);
  const glintMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const glintMesh = new THREE.Mesh(glintGeom, glintMat);
  glintMesh.position.set(0.016, 0.018, 0.094);
  eyeGroup.add(glintMesh);

  return eyeGroup;
}

const eyeMeshL = createEyeMesh('Eye_Orbital_L');
boneEyeL.add(eyeMeshL);

const eyeMeshR = createEyeMesh('Eye_Orbital_R');
boneEyeR.add(eyeMeshR);

// 7. Eyebrows (Arched 3D polygonal geometry)
console.log('Constructing articulated 3D eyebrows...');
function createEyebrow(name, isLeft) {
  const geom = new THREE.BoxGeometry(0.18, 0.04, 0.035);
  // Slight curvature
  const pos = geom.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i);
    const curve = -Math.pow(x, 2) * 0.8;
    pos.setY(i, pos.getY(i) + curve);
  }
  geom.computeVertexNormals();

  const mesh = new THREE.Mesh(geom, materials.hair);
  mesh.name = name;
  mesh.rotation.z = isLeft ? -0.1 : 0.1;
  mesh.position.set(0, 0, 0);
  return mesh;
}

const browMeshL = createEyebrow('Mesh_Brow_L', true);
boneBrowL.add(browMeshL);

const browMeshR = createEyebrow('Mesh_Brow_R', false);
boneBrowR.add(browMeshR);

// 8. Canonical Rectangular Spectacles (Dark acetate, bridge, nose pads, temples)
console.log('Constructing canonical 3D rectangular glasses...');
const glassesGroup = new THREE.Group();
glassesGroup.name = 'Glasses_Rig';
glassesGroup.position.set(0, 0.075, 0.45);

// Left Rectangular Rim
function createGlassesRim(name, isLeft) {
  const rimGroup = new THREE.Group();
  rimGroup.name = name;

  const w = 0.22;
  const h = 0.15;
  const d = 0.03;
  const t = 0.024; // Thickness of frame

  // Top bar
  const topBar = new THREE.Mesh(new THREE.BoxGeometry(w, t, d), materials.glassesFrame);
  topBar.position.set(0, h / 2, 0);
  rimGroup.add(topBar);

  // Bottom bar
  const bottomBar = new THREE.Mesh(new THREE.BoxGeometry(w, t, d), materials.glassesFrame);
  bottomBar.position.set(0, -h / 2, 0);
  rimGroup.add(bottomBar);

  // Outer bar
  const outerBar = new THREE.Mesh(new THREE.BoxGeometry(t, h, d), materials.glassesFrame);
  outerBar.position.set(isLeft ? w / 2 : -w / 2, 0, 0);
  rimGroup.add(outerBar);

  // Inner bar
  const innerBar = new THREE.Mesh(new THREE.BoxGeometry(t, h, d), materials.glassesFrame);
  innerBar.position.set(isLeft ? -w / 2 : w / 2, 0, 0);
  rimGroup.add(innerBar);

  // Glass Lens
  const lens = new THREE.Mesh(new THREE.PlaneGeometry(w - t, h - t), materials.glassesLens);
  lens.name = `${name}_Lens`;
  lens.position.set(0, 0, 0);
  rimGroup.add(lens);

  return rimGroup;
}

const rimL = createGlassesRim('Rim_L', true);
rimL.position.set(0.18, 0, 0);
glassesGroup.add(rimL);

const rimR = createGlassesRim('Rim_R', false);
rimR.position.set(-0.18, 0, 0);
glassesGroup.add(rimR);

// Glasses Bridge
const bridgeGeom = new THREE.BoxGeometry(0.12, 0.025, 0.028);
const bridgeMesh = new THREE.Mesh(bridgeGeom, materials.glassesFrame);
bridgeMesh.name = 'Glasses_Bridge';
bridgeMesh.position.set(0, 0.03, 0);
glassesGroup.add(bridgeMesh);

// Nose Pads
const padGeom = new THREE.CylinderGeometry(0.015, 0.015, 0.04, 8);
const padL = new THREE.Mesh(padGeom, materials.glassesFrame);
padL.position.set(0.06, -0.02, -0.03);
padL.rotation.z = -0.3;
glassesGroup.add(padL);

const padR = new THREE.Mesh(padGeom, materials.glassesFrame);
padR.position.set(-0.06, -0.02, -0.03);
padR.rotation.z = 0.3;
glassesGroup.add(padR);

// Glasses Side Temples (extending back to ears)
const templeGeom = new THREE.BoxGeometry(0.02, 0.022, 0.46);
const templeL = new THREE.Mesh(templeGeom, materials.glassesFrame);
templeL.name = 'Glasses_Temple_L';
templeL.position.set(0.30, 0.03, -0.22);
templeL.rotation.y = 0.05;
glassesGroup.add(templeL);

const templeR = new THREE.Mesh(templeGeom, materials.glassesFrame);
templeR.name = 'Glasses_Temple_R';
templeR.position.set(-0.30, 0.03, -0.22);
templeR.rotation.y = -0.05;
glassesGroup.add(templeR);

boneHead.add(glassesGroup);

// 9. Volumetric Curly Hair (Cluster system providing 360-degree organic volume)
console.log('Constructing volumetric curly hair clusters (360-degree coverage)...');
const hairGroup = new THREE.Group();
hairGroup.name = 'Hair_Curly_Volume';

// Generate organic 3D curl lobes across crown, temples, hairline, and back of head
const curlPositions = [
  // Crown Top
  [0, 0.48, 0.08, 0.16],
  [0.14, 0.46, 0.06, 0.15],
  [-0.14, 0.46, 0.06, 0.15],
  [0.26, 0.42, 0.04, 0.14],
  [-0.26, 0.42, 0.04, 0.14],
  [0, 0.48, -0.08, 0.16],
  [0.16, 0.45, -0.10, 0.15],
  [-0.16, 0.45, -0.10, 0.15],
  // Hairline Front Curls (above forehead)
  [0, 0.44, 0.26, 0.13],
  [0.12, 0.42, 0.28, 0.13],
  [-0.12, 0.42, 0.28, 0.13],
  [0.24, 0.38, 0.26, 0.12],
  [-0.24, 0.38, 0.26, 0.12],
  [0.06, 0.36, 0.32, 0.10],
  [-0.06, 0.36, 0.32, 0.10],
  // Temples & Sideburns Left
  [0.38, 0.30, 0.16, 0.14],
  [0.42, 0.18, 0.12, 0.13],
  [0.44, 0.06, 0.06, 0.12],
  [0.42, -0.04, 0.04, 0.10],
  // Temples & Sideburns Right
  [-0.38, 0.30, 0.16, 0.14],
  [-0.42, 0.18, 0.12, 0.13],
  [-0.44, 0.06, 0.06, 0.12],
  [-0.42, -0.04, 0.04, 0.10],
  // Rear Skull & Nape (Full 360 volume)
  [0, 0.40, -0.26, 0.16],
  [0.18, 0.36, -0.24, 0.15],
  [-0.18, 0.36, -0.24, 0.15],
  [0.30, 0.30, -0.20, 0.15],
  [-0.30, 0.30, -0.20, 0.15],
  [0, 0.24, -0.34, 0.16],
  [0.18, 0.20, -0.32, 0.15],
  [-0.18, 0.20, -0.32, 0.15],
  [0.32, 0.14, -0.26, 0.14],
  [-0.32, 0.14, -0.26, 0.14],
  [0, 0.08, -0.36, 0.15],
  [0.16, 0.04, -0.34, 0.14],
  [-0.16, 0.04, -0.34, 0.14],
  [0, -0.06, -0.34, 0.13],
  [0.14, -0.10, -0.30, 0.12],
  [-0.14, -0.10, -0.30, 0.12],
];

curlPositions.forEach(([x, y, z, rad], idx) => {
  const curlGeom = new THREE.DodecahedronGeometry(rad, 1);
  // Add organic perturbation to vertices
  const pos = curlGeom.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const px = pos.getX(i);
    const py = pos.getY(i);
    const pz = pos.getZ(i);
    const noise = (Math.sin(px * 15 + idx) + Math.cos(py * 12 + idx)) * 0.015;
    pos.setXYZ(i, px + noise, py + noise, pz + noise);
  }
  curlGeom.computeVertexNormals();

  const curlMesh = new THREE.Mesh(curlGeom, materials.hair);
  curlMesh.name = `Curl_Lobe_${idx}`;
  curlMesh.position.set(x, y, z);
  hairGroup.add(curlMesh);
});

boneHead.add(hairGroup);

// 10. Beard & Moustache (Sculpted 3D facial hair)
console.log('Constructing 3D beard and moustache geometry...');
const beardGroup = new THREE.Group();
beardGroup.name = 'Beard_FacialHair_Rig';

// Jawline & Chin Beard Wrap
const beardCurveGeom = new THREE.TorusGeometry(0.36, 0.075, 12, 24, Math.PI * 0.9);
beardCurveGeom.rotateX(Math.PI / 2.3);
beardCurveGeom.rotateZ(-Math.PI * 0.95);
const beardMesh = new THREE.Mesh(beardCurveGeom, materials.beard);
beardMesh.name = 'Mesh_Beard_Jaw';
beardMesh.position.set(0, -0.26, 0.12);
beardGroup.add(beardMesh);

// Chin Tuft Volume
const chinTuftGeom = new THREE.SphereGeometry(0.12, 12, 12);
chinTuftGeom.scale(1.2, 0.8, 0.9);
const chinTuftMesh = new THREE.Mesh(chinTuftGeom, materials.beard);
chinTuftMesh.name = 'Mesh_Beard_Chin';
chinTuftMesh.position.set(0, -0.38, 0.32);
beardGroup.add(chinTuftMesh);

// Moustache (Sitting on upper lip under nose)
const stacheGeomL = new THREE.CapsuleGeometry(0.032, 0.12, 6, 8);
stacheGeomL.rotateZ(Math.PI / 3);
const stacheMeshL = new THREE.Mesh(stacheGeomL, materials.beard);
stacheMeshL.name = 'Mesh_Moustache_L';
stacheMeshL.position.set(0.08, -0.14, 0.46);
beardGroup.add(stacheMeshL);

const stacheMeshR = new THREE.Mesh(stacheGeomL, materials.beard);
stacheMeshR.name = 'Mesh_Moustache_R';
stacheMeshR.position.set(-0.08, -0.14, 0.46);
stacheMeshR.rotation.z = -Math.PI / 1.5;
beardGroup.add(stacheMeshR);

boneHead.add(beardGroup);

// 11. Neck Cylinder
const neckGeom = new THREE.CylinderGeometry(0.18, 0.22, 0.32, 16);
const neckMesh = new THREE.Mesh(neckGeom, materials.skin);
neckMesh.name = 'Mesh_Neck';
neckMesh.position.set(0, 0.12, 0);
boneNeck.add(neckMesh);

// 12. Torso & Charcoal Technical Jacket
console.log('Constructing torso and technical jacket with safety orange trim...');
const torsoGroup = new THREE.Group();
torsoGroup.name = 'Jacket_Torso_Rig';

// Main Jacket Body
const jacketBodyGeom = new THREE.CylinderGeometry(0.42, 0.36, 0.75, 20);
jacketBodyGeom.scale(1.15, 1.0, 0.82); // Flatten chest/back vs shoulders
const jacketBodyMesh = new THREE.Mesh(jacketBodyGeom, materials.jacketCharcoal);
jacketBodyMesh.name = 'Mesh_Jacket_Body';
jacketBodyMesh.position.set(0, 0.1, 0);
torsoGroup.add(jacketBodyMesh);

// Inner Shirt Throat Notch
const innerShirtGeom = new THREE.CylinderGeometry(0.20, 0.22, 0.12, 16);
const innerShirtMesh = new THREE.Mesh(innerShirtGeom, materials.innerShirt);
innerShirtMesh.name = 'Mesh_Inner_Shirt';
innerShirtMesh.position.set(0, 0.42, 0.04);
torsoGroup.add(innerShirtMesh);

// High Standing Technical Collar
const collarGeom = new THREE.CylinderGeometry(0.25, 0.28, 0.16, 20, 1, true);
collarGeom.scale(1.05, 1.0, 0.95);
const collarMesh = new THREE.Mesh(collarGeom, materials.jacketCharcoal);
collarMesh.name = 'Mesh_Jacket_Collar';
collarMesh.position.set(0, 0.45, 0);
torsoGroup.add(collarMesh);

// Orange Piping on Collar Rim
const orangeCollarTrimGeom = new THREE.TorusGeometry(0.26, 0.016, 8, 24);
orangeCollarTrimGeom.rotateX(Math.PI / 2);
orangeCollarTrimGeom.scale(1.05, 0.95, 1.0);
const orangeCollarTrim = new THREE.Mesh(orangeCollarTrimGeom, materials.jacketOrangeTrim);
orangeCollarTrim.name = 'Mesh_Collar_Orange_Trim';
orangeCollarTrim.position.set(0, 0.53, 0);
torsoGroup.add(orangeCollarTrim);

// Orange Zipper Placket Down Front
const orangeZipperGeom = new THREE.BoxGeometry(0.024, 0.65, 0.02);
const orangeZipper = new THREE.Mesh(orangeZipperGeom, materials.jacketOrangeTrim);
orangeZipper.name = 'Mesh_Zipper_Orange_Placket';
orangeZipper.position.set(0, 0.12, 0.31);
torsoGroup.add(orangeZipper);

boneChest.add(torsoGroup);

// 13. Left and Right Articulated Arm Assemblies
console.log('Constructing articulated arms, elbows, forearms, and 5-finger hands...');

function createArmAssembly(isLeft) {
  const armGroup = new THREE.Group();
  armGroup.name = isLeft ? 'ArmAssembly_L' : 'ArmAssembly_R';
  const sign = isLeft ? 1 : -1;

  // Shoulder / Upper Arm Sleeve
  const upperArmGeom = new THREE.CylinderGeometry(0.13, 0.11, 0.38, 14);
  const upperArmMesh = new THREE.Mesh(upperArmGeom, materials.jacketCharcoal);
  upperArmMesh.name = isLeft ? 'Mesh_UpperArm_L' : 'Mesh_UpperArm_R';
  upperArmMesh.position.set(0, -0.19, 0);
  armGroup.add(upperArmMesh);

  return armGroup;
}

function createForearmAssembly(isLeft) {
  const forearmGroup = new THREE.Group();
  forearmGroup.name = isLeft ? 'ForearmAssembly_L' : 'ForearmAssembly_R';

  // Elbow Joint Sphere
  const elbowGeom = new THREE.SphereGeometry(0.10, 10, 10);
  const elbowMesh = new THREE.Mesh(elbowGeom, materials.jacketCharcoal);
  elbowMesh.position.set(0, 0, 0);
  forearmGroup.add(elbowMesh);

  // Forearm Sleeve
  const forearmGeom = new THREE.CylinderGeometry(0.11, 0.085, 0.34, 14);
  const forearmMesh = new THREE.Mesh(forearmGeom, materials.jacketCharcoal);
  forearmMesh.name = isLeft ? 'Mesh_Forearm_L' : 'Mesh_Forearm_R';
  forearmMesh.position.set(0, -0.17, 0);
  forearmGroup.add(forearmMesh);

  return forearmGroup;
}

function createHandWithFingers(isLeft) {
  const handGroup = new THREE.Group();
  handGroup.name = isLeft ? 'HandRig_L' : 'HandRig_R';
  const sign = isLeft ? 1 : -1;

  // Palm
  const palmGeom = new THREE.BoxGeometry(0.10, 0.11, 0.045);
  const palmMesh = new THREE.Mesh(palmGeom, materials.skin);
  palmMesh.name = isLeft ? 'Mesh_Palm_L' : 'Mesh_Palm_R';
  palmMesh.position.set(0, -0.05, 0);
  handGroup.add(palmMesh);

  // Thumb
  const thumbGeom = new THREE.CapsuleGeometry(0.018, 0.05, 6, 8);
  const thumbMesh = new THREE.Mesh(thumbGeom, materials.skin);
  thumbMesh.name = isLeft ? 'Mesh_Thumb_L' : 'Mesh_Thumb_R';
  thumbMesh.position.set(sign * 0.06, -0.03, 0.02);
  thumbMesh.rotation.z = -sign * 0.45;
  thumbMesh.rotation.x = 0.3;
  handGroup.add(thumbMesh);

  // 4 Articulated Fingers
  const fingerNames = ['Index', 'Middle', 'Ring', 'Pinky'];
  fingerNames.forEach((fname, fidx) => {
    const flen = fidx === 1 ? 0.065 : fidx === 0 ? 0.06 : fidx === 2 ? 0.058 : 0.048;
    const fGeom = new THREE.CapsuleGeometry(0.015, flen, 6, 8);
    const fMesh = new THREE.Mesh(fGeom, materials.skin);
    fMesh.name = `${isLeft ? 'Mesh_Finger_L_' : 'Mesh_Finger_R_'}${fname}`;
    const xPos = sign * (0.035 - fidx * 0.024);
    fMesh.position.set(xPos, -0.11 - flen / 2, 0);
    handGroup.add(fMesh);
  });

  return handGroup;
}

// Assemble Left Arm Hierarchy
boneUpperArmL.add(createArmAssembly(true));
boneForearmL.add(createForearmAssembly(true));
boneHandL.add(createHandWithFingers(true));

// Assemble Right Arm Hierarchy
boneUpperArmR.add(createArmAssembly(false));
boneForearmR.add(createForearmAssembly(false));
boneHandR.add(createHandWithFingers(false));

// 14. Signature Props: Technical Notebook & Drafting Pencil
console.log('Constructing signature props: Spiral Technical Notebook & Drafting Pencil...');

// Spiral Notebook (Held in Left Hand socket)
function createNotebookProp() {
  const nbGroup = new THREE.Group();
  nbGroup.name = 'Prop_Technical_Notebook';

  // Front & Back Cover Slabs
  const coverGeom = new THREE.BoxGeometry(0.24, 0.32, 0.012);
  const frontCover = new THREE.Mesh(coverGeom, materials.notebookCover);
  frontCover.name = 'Notebook_FrontCover';
  frontCover.position.set(0, 0, 0.018);
  nbGroup.add(frontCover);

  const backCover = new THREE.Mesh(coverGeom, materials.notebookCover);
  backCover.name = 'Notebook_BackCover';
  backCover.position.set(0, 0, -0.018);
  nbGroup.add(backCover);

  // Pages Stack (Cream paper)
  const pagesGeom = new THREE.BoxGeometry(0.23, 0.31, 0.026);
  const pagesMesh = new THREE.Mesh(pagesGeom, materials.notebookPages);
  pagesMesh.name = 'Notebook_Pages';
  nbGroup.add(pagesMesh);

  // Spiral Wire Coil along spine (left edge: x = -0.12)
  for (let s = 0; s < 10; s++) {
    const ringGeom = new THREE.TorusGeometry(0.022, 0.005, 6, 12);
    ringGeom.rotateY(Math.PI / 2);
    const ringMesh = new THREE.Mesh(ringGeom, materials.notebookWire);
    ringMesh.position.set(-0.12, -0.13 + s * 0.028, 0);
    nbGroup.add(ringMesh);
  }

  // Tilt naturally into holding orientation
  nbGroup.rotation.x = 0.5;
  nbGroup.rotation.y = 0.2;
  return nbGroup;
}

propSocketNotebook.add(createNotebookProp());

// Drafting Pencil (Held in Right Hand socket)
function createDraftingPencilProp() {
  const pencilGroup = new THREE.Group();
  pencilGroup.name = 'Prop_Drafting_Pencil';

  // Hexagonal wooden body (Yellow)
  const bodyGeom = new THREE.CylinderGeometry(0.014, 0.014, 0.28, 6);
  const bodyMesh = new THREE.Mesh(bodyGeom, materials.pencilBody);
  bodyMesh.name = 'Pencil_Shaft';
  pencilGroup.add(bodyMesh);

  // Metal Ferrule
  const ferruleGeom = new THREE.CylinderGeometry(0.015, 0.015, 0.04, 12);
  const ferruleMesh = new THREE.Mesh(ferruleGeom, materials.pencilFerrule);
  ferruleMesh.name = 'Pencil_Ferrule';
  ferruleMesh.position.set(0, 0.14, 0);
  pencilGroup.add(ferruleMesh);

  // Sharpened Wooden Tip
  const woodTipGeom = new THREE.ConeGeometry(0.014, 0.045, 12);
  const woodTipMat = new THREE.MeshStandardMaterial({ color: 0xdfb88c, roughness: 0.6 });
  const woodTipMesh = new THREE.Mesh(woodTipGeom, woodTipMat);
  woodTipMesh.name = 'Pencil_WoodTip';
  woodTipMesh.position.set(0, -0.16, 0);
  woodTipMesh.rotation.x = Math.PI;
  pencilGroup.add(woodTipMesh);

  // Graphite Lead Tip
  const leadGeom = new THREE.ConeGeometry(0.005, 0.018, 10);
  const leadMesh = new THREE.Mesh(leadGeom, materials.pencilLead);
  leadMesh.name = 'Pencil_Lead';
  leadMesh.position.set(0, -0.19, 0);
  leadMesh.rotation.x = Math.PI;
  pencilGroup.add(leadMesh);

  // Angle into drafting / gesturing grip
  pencilGroup.rotation.x = 0.8;
  pencilGroup.rotation.z = 0.3;
  return pencilGroup;
}

propSocketPencil.add(createDraftingPencilProp());

// Set Default Natural Poses for Presenter
boneUpperArmL.rotation.z = -0.55;
boneUpperArmL.rotation.x = 0.25;
boneForearmL.rotation.x = -1.1; // Bend elbow to hold notebook at chest
boneForearmL.rotation.z = 0.35;

boneUpperArmR.rotation.z = 0.35;
boneUpperArmR.rotation.x = 0.15;
boneForearmR.rotation.x = -0.7; // Forearm raised ready to gesture
boneForearmR.rotation.y = -0.2;

// 15. Export Scene to GLB
console.log('Validating model hierarchy before GLTF export...');
const exportScene = new THREE.Scene();
exportScene.name = 'SUPER_INTELLIGENCEEE_Character_Scene';
exportScene.add(characterRoot);

// Calculate total statistics
let vertexCount = 0;
let meshCount = 0;
exportScene.traverse((child) => {
  if (child.isMesh) {
    meshCount++;
    if (child.geometry && child.geometry.attributes && child.geometry.attributes.position) {
      vertexCount += child.geometry.attributes.position.count;
    }
  }
});
console.log(`Model Statistics: ${meshCount} meshes, ${vertexCount} vertices.`);

const exporter = new GLTFExporter();
const options = {
  binary: true,
  embedImages: true,
  animations: [],
};

const outputPaths = [
  path.resolve('A:/SUPER.INTELLIGENCEEE/public/models/super_character/character.glb'),
  path.resolve('A:/SUPER.INTELLIGENCEEE/rendering/remotion/public/models/super_character/character.glb'),
];

console.log('Exporting GLB binary...');
exporter.parse(
  exportScene,
  (gltf) => {
    const buffer = Buffer.from(gltf);
    outputPaths.forEach((outPath) => {
      fs.mkdirSync(path.dirname(outPath), { recursive: true });
      fs.writeFileSync(outPath, buffer);
      console.log(`Saved GLB to: ${outPath} (${(buffer.length / 1024).toFixed(1)} KB)`);
    });
    console.log('--- GLB Generation Complete ---');
  },
  (err) => {
    console.error('GLTF Export Error:', err);
    process.exit(1);
  },
  options
);
