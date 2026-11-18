import fs from 'fs';
import path from 'path';

const glbPath = path.resolve('public/models/super_character/character.glb');
const buf = fs.readFileSync(glbPath);
const b64 = buf.toString('base64');
fs.mkdirSync('src/assets', { recursive: true });
fs.writeFileSync('src/assets/characterGlbBase64.ts', `export const CHARACTER_GLB_BASE64 = "${b64}";\n`);
console.log(`Generated src/assets/characterGlbBase64.ts: ${(fs.statSync('src/assets/characterGlbBase64.ts').size / 1024).toFixed(1)} KB`);
