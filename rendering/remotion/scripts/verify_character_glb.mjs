import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
import path from 'path';

class FileReaderPolyfill {
  readAsArrayBuffer(blob) {
    blob.arrayBuffer().then((ab) => {
      this.result = ab;
      if (this.onloadend) this.onloadend();
    });
  }
}
globalThis.FileReader = FileReaderPolyfill;

const glbPath = path.resolve('public/models/super_character/character.glb');
console.log(`Verifying GLB at: ${glbPath}`);

const buffer = fs.readFileSync(glbPath);
const arrayBuffer = buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);

const loader = new GLTFLoader();
loader.parse(
  arrayBuffer,
  '',
  (gltf) => {
    console.log('✅ Successfully loaded and parsed GLB!');
    console.log('Scene name:', gltf.scene.name);

    const bones = [];
    const meshes = [];
    const morphs = [];
    const materials = new Set();

    gltf.scene.traverse((node) => {
      if (node.isBone) bones.push(node.name);
      if (node.isMesh) {
        meshes.push(node.name);
        if (node.material) {
          if (Array.isArray(node.material)) {
            node.material.forEach((m) => materials.add(m.name || m.type));
          } else {
            materials.add(node.material.name || node.material.type);
          }
        }
        if (node.morphTargetDictionary) {
          morphs.push({
            mesh: node.name,
            targets: Object.keys(node.morphTargetDictionary),
          });
        }
      }
    });

    console.log(`\n--- Model Verification Audit ---`);
    console.log(`Total Meshes: ${meshes.length}`);
    console.log(`Total Bones/Control Joints: ${bones.length}`);
    console.log(`Distinct Materials: ${materials.size}`);
    console.log(`Materials List:`, Array.from(materials));
    console.log(`Bones List:`, bones);
    console.log(`Meshes with Morph Targets:`, JSON.stringify(morphs, null, 2));

    // Verify key anatomical components
    const requiredNodes = [
      'Mesh_Head',
      'Mesh_Nose',
      'Mesh_Ear_L',
      'Mesh_Ear_R',
      'Eye_Orbital_L',
      'Eye_Orbital_R',
      'Mesh_Brow_L',
      'Mesh_Brow_R',
      'Glasses_Rig',
      'Hair_Curly_Volume',
      'Beard_FacialHair_Rig',
      'Mesh_Jacket_Body',
      'Mesh_Collar_Orange_Trim',
      'Mesh_Zipper_Orange_Placket',
      'Prop_Technical_Notebook',
      'Prop_Drafting_Pencil',
      'Bone_Head',
      'Bone_Eye_L',
      'Bone_Eye_R',
      'Bone_UpperArm_L',
      'Bone_Forearm_L',
      'Bone_Hand_L',
      'Bone_UpperArm_R',
      'Bone_Forearm_R',
      'Bone_Hand_R',
    ];

    console.log('\n--- Checking Mandatory Structural Nodes ---');
    let allFound = true;
    requiredNodes.forEach((req) => {
      const found = gltf.scene.getObjectByName(req);
      if (found) {
        console.log(`  [OK] ${req}`);
      } else {
        console.error(`  [MISSING] ${req}`);
        allFound = false;
      }
    });

    if (allFound) {
      console.log('\n🎉 ALL MANDATORY STRUCTURAL NODES VERIFIED IN GLB!');
    } else {
      console.error('\n❌ SOME STRUCTURAL NODES ARE MISSING!');
      process.exit(1);
    }
  },
  (err) => {
    console.error('Failed to parse GLB:', err);
    process.exit(1);
  }
);
