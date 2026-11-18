import fs from 'fs';
import path from 'path';

const glbPath = path.resolve('A:/SUPER.INTELLIGENCEEE/output/experiment_a3/character.glb');
const glbBase64 = fs.readFileSync(glbPath).toString('base64');
const dataUri = `data:model/gltf-binary;base64,${glbBase64}`;

// Embed key reference frames from Character 3D.mp4
const refDir = path.resolve('A:/SUPER.INTELLIGENCEEE/output/experiment_a3/reference_study');
const refFrames = ['ref_f01.png', 'ref_f03.png', 'ref_f07.png', 'ref_f10.png', 'ref_f15.png', 'ref_f20.png'];
const refDataUris = {};

refFrames.forEach((rf) => {
  const p = path.join(refDir, rf);
  if (fs.existsSync(p)) {
    const b64 = fs.readFileSync(p).toString('base64');
    refDataUris[rf] = `data:image/png;base64,${b64}`;
  }
});

console.log('Generating interactive comparison viewer with embedded GLB & reference frames...');

const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SUPER.INTELLIGENCEEE — Experiment A.3 Reference-Accurate Inspector</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0d0f14;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      overflow: hidden;
      display: flex;
      height: 100vh;
      width: 100vw;
    }
    #main-layout {
      flex: 1;
      display: flex;
      height: 100%;
      position: relative;
    }
    .panel {
      flex: 1;
      height: 100%;
      position: relative;
      display: flex;
      flex-direction: column;
      border-right: 1px solid #232936;
      background: #0d0f14;
    }
    .panel-header {
      background: #151922;
      padding: 10px 16px;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #232936;
      color: #94a3b8;
    }
    .panel-content {
      flex: 1;
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    #ref-image {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }
    #canvas3d {
      width: 100%;
      height: 100%;
      display: block;
    }
    #sidebar {
      width: 360px;
      height: 100%;
      background: #141720;
      border-left: 1px solid #262e3d;
      padding: 18px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: -4px 0 20px rgba(0,0,0,0.5);
    }
    h1 {
      font-size: 1.1rem;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge {
      background: #ff6200;
      color: #000;
      font-size: 0.68rem;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
    }
    .section-title {
      font-size: 0.76rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #7dd3fc;
      margin-bottom: 6px;
      border-bottom: 1px solid #232a38;
      padding-bottom: 4px;
    }
    .btn-grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }
    .btn-grid-2 {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
    }
    button {
      background: #1f2533;
      color: #cbd5e1;
      border: 1px solid #333d52;
      padding: 7px 8px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    button:hover {
      background: #2a3346;
      border-color: #ff6200;
      color: #fff;
    }
    button.active {
      background: #ff6200;
      color: #000;
      border-color: #ff6200;
      font-weight: 700;
    }
    .control-row {
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-bottom: 6px;
    }
    .control-label {
      display: flex;
      justify-content: space-between;
      font-size: 0.72rem;
      color: #94a3b8;
    }
    input[type="range"] {
      width: 100%;
      accent-color: #ff6200;
      cursor: pointer;
    }
    .toggle-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 4px 0;
      font-size: 0.78rem;
    }
    .toggle-row input {
      accent-color: #ff6200;
      width: 15px;
      height: 15px;
      cursor: pointer;
    }
    #loading-overlay {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: #0d0f14;
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
      border: 3px solid #232936;
      border-top-color: #ff6200;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
  <script src="https://unpkg.com/three@0.160.0/build/three.min.js"></script>
  <script src="https://unpkg.com/three@0.160.0/examples/js/controls/OrbitControls.js"></script>
  <script src="https://unpkg.com/three@0.160.0/examples/js/loaders/GLTFLoader.js"></script>
</head>
<body>

  <div id="main-layout">
    <!-- Left: Primary Authority Reference Frame -->
    <div class="panel" id="ref-panel">
      <div class="panel-header">
        <span>1. Reference Authority (Character 3D.mp4)</span>
        <span id="ref-label" style="color: #ff6200; font-size: 0.72rem;">Frame: Neutral (0.0s)</span>
      </div>
      <div class="panel-content">
        <img id="ref-image" src="${refDataUris['ref_f01.png'] || ''}" alt="Reference Character Frame" />
      </div>
    </div>

    <!-- Right: Reconstructed 3D Character Model -->
    <div class="panel" id="model-panel">
      <div class="panel-header">
        <span>2. Reconstructed 3D Model (character.glb)</span>
        <span style="color: #38bdf8; font-size: 0.72rem;">Interactive WebGL (OrbitControls)</span>
      </div>
      <div class="panel-content">
        <div id="loading-overlay">
          <div class="spinner"></div>
          <div style="font-size: 0.85rem; color: #94a3b8;">Loading Reference-Accurate 3D Character...</div>
        </div>
        <canvas id="canvas3d"></canvas>
      </div>
    </div>
  </div>

  <!-- Sidebar Controls -->
  <div id="sidebar">
    <div>
      <h1>Kavi 3D Inspector <span class="badge">Exp A.3</span></h1>
      <p style="font-size: 0.7rem; color: #64748b; margin-top: 2px;">Reference-Accurate Reconstruction & Verification</p>
    </div>

    <!-- Reference Frame Selector -->
    <div>
      <div class="section-title">Reference Moment Matching</div>
      <div class="btn-grid-3">
        <button id="btn-ref1" class="active" onclick="setReferenceFrame('ref_f01.png', 'front', 'Neutral (0.0s)')">0.0s Front</button>
        <button id="btn-ref3" onclick="setReferenceFrame('ref_f03.png', 'threeQuarterR', 'Curious (1.0s)')">1.0s 3/4 R</button>
        <button id="btn-ref7" onclick="setReferenceFrame('ref_f07.png', 'threeQuarterL', 'Blink (3.0s)')">3.0s Blink</button>
        <button id="btn-ref10" onclick="setReferenceFrame('ref_f10.png', 'threeQuarterR', 'Gesture (4.5s)')">4.5s Gesture</button>
        <button id="btn-ref15" onclick="setReferenceFrame('ref_f15.png', 'closeup', 'Speaking (7.0s)')">7.0s Closeup</button>
        <button id="btn-ref20" onclick="setReferenceFrame('ref_f20.png', 'front', 'Hero (9.5s)')">9.5s Hero</button>
      </div>
    </div>

    <!-- Camera Angles -->
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
      <div style="margin-top: 5px;">
        <button style="width: 100%; border-color: #ff6200; color: #ff6200;" onclick="setCamera('closeup')">🔍 Close-Up Facial Inspection</button>
      </div>
    </div>

    <!-- Facial Expressions -->
    <div>
      <div class="section-title">Facial Expression Presets</div>
      <div class="btn-grid-2">
        <button id="btn-expr-neutral" class="active" onclick="setExpression('neutral')">1. Neutral</button>
        <button id="btn-expr-curious" onclick="setExpression('curious')">2. Curious</button>
        <button id="btn-expr-surprised" onclick="setExpression('surprised')">3. Surprised</button>
        <button id="btn-expr-thinking" onclick="setExpression('thinking')">4. Thinking</button>
        <button id="btn-expr-explaining" onclick="setExpression('explaining')">5. Explaining</button>
        <button id="btn-expr-confident" onclick="setExpression('confident')">6. Confident</button>
        <button id="btn-expr-confused" onclick="setExpression('confused')">7. Confused</button>
        <button id="btn-expr-excited" onclick="setExpression('excited')">8. Excited</button>
        <button id="btn-expr-amused" style="grid-column: span 2;" onclick="setExpression('amused')">9. Amused</button>
      </div>
    </div>

    <!-- Direct Morph Sliders -->
    <div>
      <div class="section-title">Parametric Morph Controls</div>
      <div class="control-row">
        <div class="control-label"><span>Speech Viseme (Jaw Open)</span><span id="val-mouthOpen">0.0</span></div>
        <input type="range" id="slider-mouthOpen" min="0" max="1" step="0.05" value="0" oninput="updateMorph('mouthOpen', this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Mouth Smile</span><span id="val-mouthSmile">0.0</span></div>
        <input type="range" id="slider-mouthSmile" min="0" max="1" step="0.05" value="0" oninput="updateMorph('mouthSmile', this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Blink (Both Eyelids)</span><span id="val-blink">0.0</span></div>
        <input type="range" id="slider-blink" min="0" max="1" step="0.05" value="0" oninput="updateBlink(this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Eyebrow Elevation</span><span id="val-brows">0.0</span></div>
        <input type="range" id="slider-brows" min="0" max="1" step="0.05" value="0" oninput="updateBrows(this.value)">
      </div>
    </div>

    <!-- Display & Lighting Modes -->
    <div>
      <div class="section-title">Display & Lighting</div>
      <div class="toggle-row">
        <span>Wireframe Geometry</span>
        <input type="checkbox" onchange="toggleWireframe(this.checked)">
      </div>
      <div class="toggle-row">
        <span>Auto 360° Turntable</span>
        <input type="checkbox" onchange="toggleTurntable(this.checked)">
      </div>
      <div class="toggle-row">
        <span>Live Kinematics Demo</span>
        <input type="checkbox" onchange="toggleLiveAnimation(this.checked)">
      </div>
      <div class="control-row" style="margin-top: 6px;">
        <div class="control-label"><span>Studio Key Light</span><span id="val-keyLight">1.8</span></div>
        <input type="range" min="0" max="4" step="0.1" value="1.8" oninput="updateKeyLight(this.value)">
      </div>
      <div class="control-row">
        <div class="control-label"><span>Golden Hair Rim Light</span><span id="val-rimLight">2.4</span></div>
        <input type="range" min="0" max="5" step="0.1" value="2.4" oninput="updateRimLight(this.value)">
      </div>
    </div>
  </div>

  <script>
    const GLB_DATA_URI = "${dataUri}";
    const REF_MAP = ${JSON.stringify(refDataUris)};

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
      neutral: { mouthOpen: 0, mouthSmile: 0.15, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0, browRightUp: 0, browFurrow: 0, jawDropWide: 0 },
      curious: { mouthOpen: 0.05, mouthSmile: 0.35, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.1, browRightUp: 0.85, browFurrow: 0, jawDropWide: 0 },
      surprised: { mouthOpen: 0.25, mouthSmile: 0, mouthPucker: 0.55, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.95, browRightUp: 0.95, browFurrow: 0, jawDropWide: 0.85 },
      thinking: { mouthOpen: 0, mouthSmile: 0, mouthPucker: 0.40, mouthFrown: 0.1, blinkLeft: 0.1, blinkRight: 0.1, browLeftUp: 0, browRightUp: 0, browFurrow: 0.8, jawDropWide: 0 },
      explaining: { mouthOpen: 0.50, mouthSmile: 0.2, mouthPucker: 0.15, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.4, browRightUp: 0.4, browFurrow: 0.1, jawDropWide: 0.1 },
      confident: { mouthOpen: 0, mouthSmile: 0.55, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.2, browRightUp: 0.1, browFurrow: 0, jawDropWide: 0 },
      confused: { mouthOpen: 0.1, mouthSmile: 0, mouthPucker: 0.2, mouthFrown: 0.5, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.8, browRightUp: 0, browFurrow: 0.65, jawDropWide: 0 },
      excited: { mouthOpen: 0.40, mouthSmile: 0.90, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0, blinkRight: 0, browLeftUp: 0.85, browRightUp: 0.85, browFurrow: 0, jawDropWide: 0.4 },
      amused: { mouthOpen: 0.18, mouthSmile: 0.80, mouthPucker: 0, mouthFrown: 0, blinkLeft: 0.35, blinkRight: 0.35, browLeftUp: 0.3, browRightUp: 0.3, browFurrow: 0, jawDropWide: 0.15 }
    };

    function init() {
      const container = document.getElementById('model-panel');
      const canvas = document.getElementById('canvas3d');

      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x0d0f14);

      camera = new THREE.PerspectiveCamera(34, container.clientWidth / container.clientHeight, 0.1, 100);
      camera.position.set(0, 1.25, 3.4);

      renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.15;

      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.target.set(0, 1.12, 0);

      // Studio Lighting
      const ambient = new THREE.AmbientLight(0xffffff, 0.75);
      scene.add(ambient);

      keyLight = new THREE.DirectionalLight(0xfffaed, 1.8);
      keyLight.position.set(2.4, 3.6, 3.0);
      scene.add(keyLight);

      fillLight = new THREE.DirectionalLight(0xcce2ff, 0.95);
      fillLight.position.set(-3.2, 2.0, 2.2);
      scene.add(fillLight);

      rimLight = new THREE.DirectionalLight(0xff9e42, 2.4); // Golden hair rim light
      rimLight.position.set(0, 4.2, -3.5);
      scene.add(rimLight);

      // Studio Ground Shadow Disc
      const groundGeom = new THREE.CircleGeometry(1.6, 32);
      groundGeom.rotateX(-Math.PI / 2);
      const groundMat = new THREE.MeshBasicMaterial({ color: 0x05070a, transparent: true, opacity: 0.65 });
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

          document.getElementById('loading-overlay').style.opacity = '0';
          setTimeout(() => document.getElementById('loading-overlay').style.display = 'none', 400);
        },
        undefined,
        (err) => console.error('Error loading GLB:', err)
      );
    }

    function setReferenceFrame(refKey, camPreset, labelText) {
      const img = document.getElementById('ref-image');
      if (img && REF_MAP[refKey]) {
        img.src = REF_MAP[refKey];
      }
      document.getElementById('ref-label').innerText = 'Frame: ' + labelText;

      document.querySelectorAll('#sidebar .btn-grid-3 button').forEach(b => b.classList.remove('active'));
      const activeBtn = event ? event.target : null;
      if (activeBtn) activeBtn.classList.add('active');

      setCamera(camPreset);
    }

    function setCamera(preset) {
      if (!controls) return;
      if (preset === 'front') {
        camera.position.set(0, 1.25, 3.4);
        controls.target.set(0, 1.12, 0);
      } else if (preset === 'threeQuarterL') {
        camera.position.set(2.0, 1.3, 2.6);
        controls.target.set(0, 1.12, 0);
      } else if (preset === 'threeQuarterR') {
        camera.position.set(-2.0, 1.3, 2.6);
        controls.target.set(0, 1.12, 0);
      } else if (preset === 'profileL') {
        camera.position.set(3.0, 1.25, 0);
        controls.target.set(0, 1.12, 0);
      } else if (preset === 'profileR') {
        camera.position.set(-3.0, 1.25, 0);
        controls.target.set(0, 1.12, 0);
      } else if (preset === 'rear') {
        camera.position.set(0, 1.25, -3.4);
        controls.target.set(0, 1.12, 0);
      } else if (preset === 'closeup') {
        camera.position.set(0, 1.58, 1.25);
        controls.target.set(0, 1.55, 0);
      }
      controls.update();
    }

    function setExpression(exprKey) {
      const preset = EXPRESSIONS[exprKey];
      if (!preset || !headMesh || !headMesh.morphTargetDictionary) return;

      document.querySelectorAll('#sidebar .btn-grid-2 button').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('btn-expr-' + exprKey);
      if (activeBtn) activeBtn.classList.add('active');

      Object.entries(preset).forEach(([targetName, targetVal]) => {
        const idx = headMesh.morphTargetDictionary[targetName];
        if (idx !== undefined) {
          headMesh.morphTargetInfluences[idx] = targetVal;
        }
      });

      const sliderOpen = document.getElementById('slider-mouthOpen');
      if (sliderOpen) { sliderOpen.value = preset.mouthOpen || 0; document.getElementById('val-mouthOpen').innerText = sliderOpen.value; }
      const sliderSmile = document.getElementById('slider-mouthSmile');
      if (sliderSmile) { sliderSmile.value = preset.mouthSmile || 0; document.getElementById('val-mouthSmile').innerText = sliderSmile.value; }
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
      const container = document.getElementById('model-panel');
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
        if (headBone) {
          headBone.rotation.y = Math.sin(animClock * 0.7) * 0.14;
          headBone.rotation.z = Math.cos(animClock * 0.5) * 0.04;
        }
        if (eyeL && eyeR) {
          eyeL.rotation.y = Math.sin(animClock * 1.2) * 0.18;
          eyeR.rotation.y = Math.sin(animClock * 1.2) * 0.18;
        }
        if (upperArmR && forearmR) {
          upperArmR.rotation.z = 0.32 + Math.sin(animClock * 1.4) * 0.10;
          forearmR.rotation.x = -0.72 + Math.cos(animClock * 1.4) * 0.14;
        }
        if (headMesh && headMesh.morphTargetDictionary) {
          const blinkCycle = (animClock * 1.8) % (Math.PI * 4);
          const isBlinking = blinkCycle > (Math.PI * 4 - 0.35);
          const bVal = isBlinking ? 1.0 : 0.0;
          const l = headMesh.morphTargetDictionary['blinkLeft'];
          const r = headMesh.morphTargetDictionary['blinkRight'];
          if (l !== undefined) headMesh.morphTargetInfluences[l] = bVal;
          if (r !== undefined) headMesh.morphTargetInfluences[r] = bVal;

          const speechViseme = Math.max(0, Math.sin(animClock * 3.2)) * 0.40;
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

const outPath = path.resolve('A:/SUPER.INTELLIGENCEEE/output/experiment_a3/character_viewer.html');
fs.writeFileSync(outPath, htmlContent);
console.log(`Saved Reference-Comparison Viewer to: ${outPath} (${(htmlContent.length / 1024).toFixed(1)} KB)`);
