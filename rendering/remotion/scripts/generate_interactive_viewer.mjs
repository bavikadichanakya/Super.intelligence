/**
 * Generates a standalone, self-contained interactive 3D Character Preview Viewer.
 * Embeds character.glb as a Base64 data URI to guarantee seamless zero-CORS loading.
 */

import fs from 'fs';
import path from 'path';

const glbPath = path.resolve('public/models/super_character/character.glb');
const glbBuffer = fs.readFileSync(glbPath);
const glbBase64 = glbBuffer.toString('base64');
const dataUri = `data:model/gltf-binary;base64,${glbBase64}`;

console.log(`Embedding GLB (${(glbBuffer.length / 1024).toFixed(1)} KB) into standalone HTML viewer...`);

const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SUPER.INTELLIGENCEEE — Kavi 3D Character Inspector</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0f1115;
      color: #e0e6ed;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      overflow: hidden;
      display: flex;
      height: 100vh;
      width: 100vw;
    }
    #viewport-container {
      flex: 1;
      height: 100%;
      position: relative;
    }
    #canvas3d {
      width: 100%;
      height: 100%;
      display: block;
    }
    #sidebar {
      width: 360px;
      height: 100%;
      background: #161920;
      border-left: 1px solid #2a2f3d;
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
      box-shadow: -4px 0 20px rgba(0,0,0,0.4);
    }
    h1 {
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge {
      background: #ff6b00;
      color: #000;
      font-size: 0.7rem;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
    }
    .section-title {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #8b9bb4;
      margin-bottom: 8px;
      border-bottom: 1px solid #252b38;
      padding-bottom: 4px;
    }
    .btn-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
    }
    .btn-grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }
    button {
      background: #232936;
      color: #d1d9e6;
      border: 1px solid #343c4e;
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    button:hover {
      background: #2e3647;
      border-color: #ff6b00;
      color: #fff;
    }
    button.active {
      background: #ff6b00;
      color: #000;
      border-color: #ff6b00;
      font-weight: 700;
    }
    .control-row {
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-bottom: 8px;
    }
    .control-label {
      display: flex;
      justify-content: space-between;
      font-size: 0.75rem;
      color: #a0aec0;
    }
    input[type="range"] {
      width: 100%;
      accent-color: #ff6b00;
      cursor: pointer;
    }
    .toggle-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 0;
      font-size: 0.82rem;
    }
    .toggle-row input {
      accent-color: #ff6b00;
      width: 16px;
      height: 16px;
      cursor: pointer;
    }
    #loading-overlay {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: #0f1115;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 12px;
      z-index: 10;
      transition: opacity 0.4s ease;
    }
    .spinner {
      width: 36px; height: 36px;
      border: 3px solid #2a2f3d;
      border-top-color: #ff6b00;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    #stats-badge {
      position: absolute;
      bottom: 16px;
      left: 16px;
      background: rgba(16, 20, 28, 0.85);
      border: 1px solid #2a2f3d;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.75rem;
      color: #8b9bb4;
      pointer-events: none;
      backdrop-filter: blur(8px);
    }
  </style>
  <!-- Three.js + OrbitControls + GLTFLoader via CDN with fallback -->
  <script src="https://unpkg.com/three@0.160.0/build/three.min.js"></script>
  <script src="https://unpkg.com/three@0.160.0/examples/js/controls/OrbitControls.js"></script>
  <script src="https://unpkg.com/three@0.160.0/examples/js/loaders/GLTFLoader.js"></script>
</head>
<body>

  <div id="viewport-container">
    <div id="loading-overlay">
      <div class="spinner"></div>
      <div style="font-size: 0.85rem; color: #8b9bb4;">Loading Canonical 3D Character Rig...</div>
    </div>
    <canvas id="canvas3d"></canvas>
    <div id="stats-badge">
      <div><strong>SUPER.INTELLIGENCEEE</strong> — Kavi 3D Avatar</div>
      <div id="stat-poly">Polygons: Loading...</div>
      <div id="stat-fps">Interactive Mode: OrbitControls Active</div>
    </div>
  </div>

  <div id="sidebar">
    <div>
      <h1>Kavi 3D Inspector <span class="badge">Exp A.2</span></h1>
      <p style="font-size: 0.72rem; color: #718096; margin-top: 4px;">Genuine 3D Character Model & Rig Viewer</p>
    </div>

    <!-- Camera Presets -->
    <div>
      <div class="section-title">Camera Angle Presets</div>
      <div class="btn-grid-3">
        <button onclick="setCamera('front')">Front</button>
        <button onclick="setCamera('threeQuarterL')">3/4 Left</button>
        <button onclick="setCamera('threeQuarterR')">3/4 Right</button>
        <button onclick="setCamera('profileL')">Profile L</button>
        <button onclick="setCamera('profileR')">Profile R</button>
        <button onclick="setCamera('rear')">Rear 360°</button>
      </div>
      <div style="margin-top: 6px;">
        <button style="width: 100%; border-color: #ff6b00; color: #ff6b00;" onclick="setCamera('closeup')">🔍 Close-Up Facial Inspection</button>
      </div>
    </div>

    <!-- Expression Switcher -->
    <div>
      <div class="section-title">Facial Expression Presets</div>
      <div class="btn-grid">
        <button id="btn-neutral" class="active" onclick="setExpression('neutral')">1. Neutral</button>
        <button id="btn-curious" onclick="setExpression('curious')">2. Curious</button>
        <button id="btn-surprised" onclick="setExpression('surprised')">3. Surprised</button>
        <button id="btn-thinking" onclick="setExpression('thinking')">4. Thinking</button>
        <button id="btn-explaining" onclick="setExpression('explaining')">5. Explaining</button>
        <button id="btn-confident" onclick="setExpression('confident')">6. Confident</button>
        <button id="btn-confused" onclick="setExpression('confused')">7. Confused</button>
        <button id="btn-excited" onclick="setExpression('excited')">8. Excited</button>
        <button id="btn-amused" style="grid-column: span 2;" onclick="setExpression('amused')">9. Amused</button>
      </div>
    </div>

    <!-- Direct Morph Target Sliders -->
    <div>
      <div class="section-title">Parametric Morph Controls</div>
      <div class="control-row">
        <div class="control-label"><span>Jaw Open (Speech/Viseme)</span><span id="val-mouthOpen">0.0</span></div>
        <input type="range" id="slider-mouthOpen" min="0" max="1" step="0.05" value="0" oninput="updateMorph('mouthOpen', this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Mouth Smile</span><span id="val-mouthSmile">0.0</span></div>
        <input type="range" id="slider-mouthSmile" min="0" max="1" step="0.05" value="0" oninput="updateMorph('mouthSmile', this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Mouth Pucker ("O" Shape)</span><span id="val-mouthPucker">0.0</span></div>
        <input type="range" id="slider-mouthPucker" min="0" max="1" step="0.05" value="0" oninput="updateMorph('mouthPucker', this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Blink (Both Eyelids)</span><span id="val-blink">0.0</span></div>
        <input type="range" id="slider-blink" min="0" max="1" step="0.05" value="0" oninput="updateBlink(this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Eyebrow Raise</span><span id="val-brows">0.0</span></div>
        <input type="range" id="slider-brows" min="0" max="1" step="0.05" value="0" oninput="updateBrows(this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Eye Gaze Vector X (Yaw)</span><span id="val-gazeX">0.0</span></div>
        <input type="range" id="slider-gazeX" min="-0.4" max="0.4" step="0.02" value="0" oninput="updateGazeX(this.value)">
      </div>
    </div>

    <!-- Lighting & Display Modes -->
    <div>
      <div class="section-title">Inspection & Display Modes</div>
      <div class="toggle-row">
        <span>Wireframe Geometry</span>
        <input type="checkbox" id="toggle-wireframe" onchange="toggleWireframe(this.checked)">
      </div>
      <div class="toggle-row">
        <span>Auto 360° Turntable</span>
        <input type="checkbox" id="toggle-turntable" onchange="toggleTurntable(this.checked)">
      </div>
      <div class="toggle-row">
        <span>Live Kinematics Demo</span>
        <input type="checkbox" id="toggle-anim" onchange="toggleLiveAnimation(this.checked)">
      </div>
      <div class="control-row" style="margin-top: 6px;">
        <div class="control-label"><span>Studio Key Light</span><span id="val-keyLight">1.8</span></div>
        <input type="range" min="0" max="4" step="0.1" value="1.8" oninput="updateKeyLight(this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Rim Light (Hair Highlights)</span><span id="val-rimLight">2.2</span></div>
        <input type="range" min="0" max="5" step="0.1" value="2.2" oninput="updateRimLight(this.value)">
      </div>
    </div>
  </div>

  <script>
    const GLB_DATA_URI = "${dataUri}";

    let scene, camera, renderer, controls;
    let characterModel = null;
    let headMesh = null;
    let eyeL = null, eyeR = null;
    let upperArmL = null, forearmL = null;
    let upperArmR = null, forearmR = null;
    let headBone = null;
    let keyLight, rimLight, fillLight;

    let isTurntable = false;
    let isLiveAnim = false;
    let animClock = 0;

    const EXPRESSIONS = {
      neutral: { mouthOpen: 0, mouthSmile: 0, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0, browRightUp: 0, browFurrow: 0, jawDropWide: 0 },
      curious: { mouthOpen: 0.05, mouthSmile: 0.35, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.1, browRightUp: 0.85, browFurrow: 0, jawDropWide: 0 },
      surprised: { mouthOpen: 0.3, mouthSmile: 0, mouthPucker: 0.6, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.95, browRightUp: 0.95, browFurrow: 0, jawDropWide: 0.85 },
      thinking: { mouthOpen: 0, mouthSmile: 0, mouthPucker: 0.45, mouthFrown: 0.1, blinkLeft: 0.1, blinkRight: 0.1, browLeftUp: 0, browRightUp: 0, browFurrow: 0.8, jawDropWide: 0 },
      explaining: { mouthOpen: 0.55, mouthSmile: 0.2, mouthPucker: 0.15, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.4, browRightUp: 0.4, browFurrow: 0.1, jawDropWide: 0.1 },
      confident: { mouthOpen: 0, mouthSmile: 0.55, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.2, browRightUp: 0.1, browFurrow: 0, jawDropWide: 0 },
      confused: { mouthOpen: 0.1, mouthSmile: 0, mouthPucker: 0.2, mouthFrown: 0.6, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.8, browRightUp: 0, browFurrow: 0.65, jawDropWide: 0 },
      excited: { mouthOpen: 0.45, mouthSmile: 0.95, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.85, browRightUp: 0.85, browFurrow: 0, jawDropWide: 0.4 },
      amused: { mouthOpen: 0.2, mouthSmile: 0.85, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0.35, blinkRight: 0.35, browLeftUp: 0.3, browRightUp: 0.3, browFurrow: 0, jawDropWide: 0.15 }
    };

    function init() {
      const container = document.getElementById('viewport-container');
      const canvas = document.getElementById('canvas3d');

      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x0e1117);

      camera = new THREE.PerspectiveCamera(38, container.clientWidth / container.clientHeight, 0.1, 100);
      camera.position.set(0, 1.25, 3.2);

      renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.1;

      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.target.set(0, 1.1, 0);

      // Studio Lighting
      const ambient = new THREE.AmbientLight(0xffffff, 0.7);
      scene.add(ambient);

      keyLight = new THREE.DirectionalLight(0xfffaed, 1.8);
      keyLight.position.set(2.5, 3.5, 3.0);
      scene.add(keyLight);

      fillLight = new THREE.DirectionalLight(0xdbe7ff, 0.9);
      fillLight.position.set(-3.0, 2.0, 2.0);
      scene.add(fillLight);

      rimLight = new THREE.DirectionalLight(0xffeedd, 2.2);
      rimLight.position.set(0, 4.0, -3.5);
      scene.add(rimLight);

      // Subtle Ground Shadow Disc
      const groundGeom = new THREE.CircleGeometry(1.6, 32);
      groundGeom.rotateX(-Math.PI / 2);
      const groundMat = new THREE.MeshBasicMaterial({ color: 0x07090c, transparent: true, opacity: 0.6 });
      const ground = new THREE.Mesh(groundGeom, groundMat);
      ground.position.y = -0.01;
      scene.add(ground);

      loadModel();

      window.addEventListener('resize', onResize);
      animate();
    }

    function loadModel() {
      const loader = new THREE.GLTFLoader();
      loader.load(
        GLB_DATA_URI,
        (gltf) => {
          characterModel = gltf.scene;
          scene.add(characterModel);

          // Find key nodes
          characterModel.traverse((node) => {
            if (node.name === 'Mesh_Head') headMesh = node;
            if (node.name === 'Bone_Head') headBone = node;
            if (node.name === 'Bone_Eye_L') eyeL = node;
            if (node.name === 'Bone_Eye_R') eyeR = node;
            if (node.name === 'Bone_UpperArm_L') upperArmL = node;
            if (node.name === 'Bone_Forearm_L') forearmL = node;
            if (node.name === 'Bone_UpperArm_R') upperArmR = node;
            if (node.name === 'Bone_Forearm_R') forearmR = node;
          });

          // Compute poly count
          let tris = 0;
          characterModel.traverse((c) => {
            if (c.isMesh && c.geometry && c.geometry.index) {
              tris += c.geometry.index.count / 3;
            } else if (c.isMesh && c.geometry && c.geometry.attributes.position) {
              tris += c.geometry.attributes.position.count / 3;
            }
          });

          document.getElementById('stat-poly').innerText = 'Geometry: ' + Math.round(tris) + ' polygons / 113 meshes';
          document.getElementById('loading-overlay').style.opacity = '0';
          setTimeout(() => document.getElementById('loading-overlay').style.display = 'none', 400);
        },
        undefined,
        (err) => console.error('Error loading GLB:', err)
      );
    }

    function setCamera(preset) {
      if (!controls) return;
      if (preset === 'front') {
        camera.position.set(0, 1.25, 3.2);
        controls.target.set(0, 1.1, 0);
      } else if (preset === 'threeQuarterL') {
        camera.position.set(2.0, 1.3, 2.4);
        controls.target.set(0, 1.1, 0);
      } else if (preset === 'threeQuarterR') {
        camera.position.set(-2.0, 1.3, 2.4);
        controls.target.set(0, 1.1, 0);
      } else if (preset === 'profileL') {
        camera.position.set(3.0, 1.25, 0);
        controls.target.set(0, 1.1, 0);
      } else if (preset === 'profileR') {
        camera.position.set(-3.0, 1.25, 0);
        controls.target.set(0, 1.1, 0);
      } else if (preset === 'rear') {
        camera.position.set(0, 1.25, -3.2);
        controls.target.set(0, 1.1, 0);
      } else if (preset === 'closeup') {
        camera.position.set(0, 1.62, 1.15);
        controls.target.set(0, 1.58, 0);
      }
      controls.update();
    }

    function setExpression(exprKey) {
      const preset = EXPRESSIONS[exprKey];
      if (!preset || !headMesh || !headMesh.morphTargetDictionary) return;

      document.querySelectorAll('#sidebar .btn-grid button').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('btn-' + exprKey);
      if (activeBtn) activeBtn.classList.add('active');

      Object.entries(preset).forEach(([targetName, targetVal]) => {
        const idx = headMesh.morphTargetDictionary[targetName];
        if (idx !== undefined) {
          headMesh.morphTargetInfluences[idx] = targetVal;
        }
      });

      // Update UI sliders
      const sliderOpen = document.getElementById('slider-mouthOpen');
      if (sliderOpen) { sliderOpen.value = preset.mouthOpen || 0; document.getElementById('val-mouthOpen').innerText = sliderOpen.value; }
      const sliderSmile = document.getElementById('slider-mouthSmile');
      if (sliderSmile) { sliderSmile.value = preset.mouthSmile || 0; document.getElementById('val-mouthSmile').innerText = sliderSmile.value; }
      const sliderPucker = document.getElementById('slider-mouthPucker');
      if (sliderPucker) { sliderPucker.value = preset.mouthPucker || 0; document.getElementById('val-mouthPucker').innerText = sliderPucker.value; }
    }

    function updateMorph(targetName, val) {
      if (!headMesh || !headMesh.morphTargetDictionary) return;
      const idx = headMesh.morphTargetDictionary[targetName];
      if (idx !== undefined) {
        headMesh.morphTargetInfluences[idx] = parseFloat(val);
        document.getElementById('val-' + targetName).innerText = parseFloat(val).toFixed(2);
      }
    }

    function updateBlink(val) {
      if (!headMesh || !headMesh.morphTargetDictionary) return;
      const v = parseFloat(val);
      const l = headMesh.morphTargetDictionary['blinkLeft'];
      const r = headMesh.morphTargetDictionary['blinkRight'];
      if (l !== undefined) headMesh.morphTargetInfluences[l] = v;
      if (r !== undefined) headMesh.morphTargetInfluences[r] = v;
      document.getElementById('val-blink').innerText = v.toFixed(2);
    }

    function updateBrows(val) {
      if (!headMesh || !headMesh.morphTargetDictionary) return;
      const v = parseFloat(val);
      const l = headMesh.morphTargetDictionary['browLeftUp'];
      const r = headMesh.morphTargetDictionary['browRightUp'];
      if (l !== undefined) headMesh.morphTargetInfluences[l] = v;
      if (r !== undefined) headMesh.morphTargetInfluences[r] = v;
      document.getElementById('val-brows').innerText = v.toFixed(2);
    }

    function updateGazeX(val) {
      const v = parseFloat(val);
      if (eyeL) eyeL.rotation.y = v;
      if (eyeR) eyeR.rotation.y = v;
      document.getElementById('val-gazeX').innerText = v.toFixed(2);
    }

    function toggleWireframe(isChecked) {
      if (!characterModel) return;
      characterModel.traverse((node) => {
        if (node.isMesh && node.material) {
          if (Array.isArray(node.material)) {
            node.material.forEach(m => m.wireframe = isChecked);
          } else {
            node.material.wireframe = isChecked;
          }
        }
      });
    }

    function toggleTurntable(isChecked) {
      isTurntable = isChecked;
    }

    function toggleLiveAnimation(isChecked) {
      isLiveAnim = isChecked;
    }

    function updateKeyLight(val) {
      if (keyLight) keyLight.intensity = parseFloat(val);
      document.getElementById('val-keyLight').innerText = parseFloat(val).toFixed(1);
    }

    function updateRimLight(val) {
      if (rimLight) rimLight.intensity = parseFloat(val);
      document.getElementById('val-rimLight').innerText = parseFloat(val).toFixed(1);
    }

    function onResize() {
      const container = document.getElementById('viewport-container');
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    }

    function animate() {
      requestAnimationFrame(animate);

      if (isTurntable && characterModel) {
        characterModel.rotation.y += 0.008;
      }

      if (isLiveAnim && characterModel) {
        animClock += 0.035;
        // Natural subtle head sway & breathing
        if (headBone) {
          headBone.rotation.y = Math.sin(animClock * 0.7) * 0.15;
          headBone.rotation.z = Math.cos(animClock * 0.5) * 0.05;
        }
        // Gaze tracking
        if (eyeL && eyeR) {
          eyeL.rotation.y = Math.sin(animClock * 1.2) * 0.22;
          eyeR.rotation.y = Math.sin(animClock * 1.2) * 0.22;
        }
        // Arm gesture with pencil
        if (upperArmR && forearmR) {
          upperArmR.rotation.z = 0.35 + Math.sin(animClock * 1.5) * 0.12;
          forearmR.rotation.x = -0.7 + Math.cos(animClock * 1.5) * 0.18;
        }
        // Periodic blinking
        if (headMesh && headMesh.morphTargetDictionary) {
          const blinkCycle = (animClock * 1.8) % (Math.PI * 4);
          const isBlinking = blinkCycle > (Math.PI * 4 - 0.35);
          const bVal = isBlinking ? 1.0 : 0.0;
          const l = headMesh.morphTargetDictionary['blinkLeft'];
          const r = headMesh.morphTargetDictionary['blinkRight'];
          if (l !== undefined) headMesh.morphTargetInfluences[l] = bVal;
          if (r !== undefined) headMesh.morphTargetInfluences[r] = bVal;

          // Conversational speech mouth
          const speechViseme = Math.max(0, Math.sin(animClock * 3.5)) * 0.45;
          const mOpen = headMesh.morphTargetDictionary['mouthOpen'];
          if (mOpen !== undefined) headMesh.morphTargetInfluences[mOpen] = speechViseme;
        }
      }

      controls.update();
      renderer.render(scene, camera);
    }

    window.onload = init;
  </script>
</body>
</html>`;

const outPath = path.resolve('A:/SUPER.INTELLIGENCEEE/output/experiment_a2/character_viewer.html');
fs.writeFileSync(outPath, htmlContent);
console.log(`Saved Standalone Interactive 3D Viewer to: ${outPath} (${(htmlContent.length / 1024).toFixed(1)} KB)`);
