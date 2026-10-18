/* 密营 · 燎原：史料关系驱动的红色三维场景与 WebXR 体验。 */
(function () {
'use strict';
const fallback = document.getElementById('fallback');
const loading = document.getElementById('loading');
if (!window.THREE || !window.WebGLRenderingContext) {
  fallback.classList.add('on'); loading.classList.add('off'); return;
}
const D = window.__MIYING__, S = window.__MIYING_STRUCT__;
const EVENTS = (D.events || []).filter(e => e.layer === 'event');
const SITE_EVENTS = (D.events || []).filter(e => e.layer === 'site');   // 遗址：build_web 已并入 events，layer=site
const SITES_WITH_COORDS = SITE_EVENTS.filter(e => e.place && e.place.lat != null && e.place.lng != null);
const YEAR0 = D.meta.year_min, YEAR1 = D.meta.year_max;
const VERD = (D.meta && D.meta.verdicts) || {};
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const STORY_SECONDS = 10;
const STORY_CHAPTERS = [
  { title: '从一条记载出发', from: 1931, to: 1931, ids: ['evt_1931_mgzsw_xuanyan'], camera: [0.08, 1.04, 44], body: '1931 年 9 月 19 日，中共满洲省委发表宣言，指出日本帝国主义武装占领满洲。我们先从这条记载出发，沿着出处进入这段历史。' },
  { title: '抵抗不止一条线', from: 1932, to: 1932, ids: ['evt_1932_jinxi_gujia', 'evt_1932_wangdelin_jiuguojun', 'evt_1932_mgzsw_gaoshu'], camera: [-0.12, 1.12, 46], body: '进入 1932 年，义勇军、救国军与满洲省委的相关记录依次出现。它们属于不同事件；我们逐条查看记载，而不把时间上的相邻说成同一条行动线。' },
  { title: '名字，各有其事', from: 1934, to: 1934, ids: ['evt_1934_yangjingyu_zongzhihuibu', 'evt_1934_tongzhangrong_xisheng'], camera: [0.18, 1.08, 42], body: '1934 年，杨靖宇成立东北抗日联合军总指挥部；童长荣率队作战牺牲。两个名字在同一幕中并列呈现，不表示两件事存在已证实的直接联系。' },
  { title: '队伍成形', from: 1935, to: 1935, ids: ['evt_1935_disanjun_chengli', 'evt_1935_diwujun_chengli'], camera: [-0.08, 1.02, 38], body: '1935 年，哈东支队与绥宁反日同盟军的整编进入年表。名称、编制与组织沿革需要一条一条读，不能只靠一幅壮阔的雪原来代替证据。' },
  { title: '战斗与牺牲', from: 1937, to: 1938, ids: ['evt_1937_songtieyan_xisheng', 'evt_1938_shier_lieshi'], camera: [0.16, 1.02, 35], body: '1937 年密营遭围、宋铁岩牺牲；1938 年小孤山战斗后，十二名战士牺牲。镜头不重演战场，只将现有记载与出处带到观众面前。' },
  { title: '不替证据画线', from: 1938, to: 1940, ids: ['evt_1938_chengbin_toudi', 'evt_1940_yangjingyu_xunguo'], camera: [0.04, 1.06, 48], body: '1938 年有程斌率部投敌的记载；1940 年有杨靖宇牺牲的记载。先后相邻不等于因果关系；数据库没有建立事件级因果边，本片也不补画这条线。' },
  { title: '时间继续向前', from: 1941, to: 1945, ids: ['evt_1941_zhaoshangzhi_xiaobudui', 'evt_1945_riben_touxiang'], camera: [0.02, 1.1, 52], body: '1941 年，赵尚志率小部队活动仍见于记录；1945 年，日本宣布无条件投降。我们把镜头推到这条时间线的末页，再回看每一条记录怎样留下来。' },
  { title: '把出处留在故事里', from: 1945, to: 1945, ids: ['evt_1945_riben_touxiang'], camera: [0.04, 1.08, 100], closing: true, body: '' },
];
document.getElementById('m-events').textContent = EVENTS.length;
document.getElementById('m-sources').textContent = (S.sources || []).length;
document.getElementById('m-sites').textContent = SITES_WITH_COORDS.length;

function noise2(x, z) {
  return Math.sin(x * 0.35 + Math.cos(z * 0.21) * 2.1) * 1.6
       + Math.sin(z * 0.28 + Math.sin(x * 0.17) * 1.7) * 1.1
       + Math.sin((x + z) * 0.11) * 2.4;
}
const TEMP = {
  '牺牲': [1.00, 0.16, 0.12], '惨案': [1.00, 0.06, 0.10],
  '战斗': [1.00, 0.12, 0.07], '会议': [1.00, 0.34, 0.12],
  '宣言': [0.96, 0.10, 0.13], '建军': [1.00, 0.24, 0.08],
  '叛变': [0.62, 0.07, 0.12],
};
function tempOf(e) {
  const t = e.event_type || '';
  for (const k in TEMP) if (t.includes(k)) return TEMP[k];
  return [1.0, 0.18, 0.10];
}

/* ---------- 灯火落位 ---------- */
const SPAN = 64;
function yearOf(e) { return e.date && e.date.start ? +String(e.date.start).slice(0, 4) : YEAR0; }
const TYPES = [...new Set(EVENTS.map(e => e.event_type || '其他'))];
function laneOf(e) {
  const t = e.event_type || '其他';
  let i = TYPES.findIndex(k => t.includes(k) || k.includes(t));
  return (i < 0 ? TYPES.length - 1 : i) - (TYPES.length - 1) / 2;
}
function firePos(e, i) {
  const x = ((yearOf(e) - YEAR0) / (YEAR1 - YEAR0) - 0.5) * SPAN;
  const z = laneOf(e) * 5.2 + ((i * 7919) % 100 / 100 - 0.5) * 3.4;
  const y = terrainHeight(x, z) + 1.5;
  return [x, y, z];
}
const nSources = {};
(S.conclusions || []).forEach(c => { nSources[c.id] = c.sources_count || (c.supports ? c.supports.length : 1); });
function nSrc(e) { return nSources[e.id] != null ? nSources[e.id] : ((e.sources || []).length || 1); }

/* ---------- 场景基座 ---------- */
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x17090d);
scene.fog = new THREE.FogExp2(0x210b10, 0.006);
const camera = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, 0.1, 600);
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
} catch (_) {
  fallback.classList.add('on'); loading.classList.add('off'); return;
}
const mobile = matchMedia('(max-width: 760px), (pointer: coarse)').matches;
renderer.setPixelRatio(Math.min(devicePixelRatio || 1, mobile ? 1.25 : 1.7));
renderer.setSize(innerWidth, innerHeight);
renderer.setClearColor(0x17090d);
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.98;
renderer.xr.enabled = true;
if (renderer.xr.setReferenceSpaceType) renderer.xr.setReferenceSpaceType('local-floor');
if (renderer.xr.setFoveation) renderer.xr.setFoveation(mobile ? 0.82 : 0.68);
if (renderer.xr.setFramebufferScaleFactor) renderer.xr.setFramebufferScaleFactor(mobile ? 0.78 : 0.9);
renderer.domElement.id = 'world';
renderer.domElement.setAttribute('role', 'img');
renderer.domElement.setAttribute('aria-label', '东北抗联史料来源关系三维场景');
document.body.appendChild(renderer.domElement);
renderer.domElement.addEventListener('webglcontextlost', event => {
  event.preventDefault();
  fallback.classList.add('on');
  fallback.querySelector('h2').textContent = '三维场景暂时中断';
  fallback.querySelector('p').textContent = '显卡上下文已中断。恢复后可重新载入场景，或进入 2D 证据结构继续浏览。';
});
renderer.domElement.addEventListener('webglcontextrestored', () => location.reload());

const amb = new THREE.AmbientLight(0x8d2938, 0.72);
scene.add(amb);
const moon = new THREE.DirectionalLight(0xf1c9b2, 0.72);
moon.position.set(-40, 70, -30);
scene.add(moon);
const redFill = new THREE.DirectionalLight(0xb51d31, 0.5);
redFill.position.set(44, 22, 32);
scene.add(redFill);

/* ---------- 夜空 ---------- */
(function stars() {
  const N = 1400, pos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const th = Math.random() * Math.PI * 2, ph = Math.acos(Math.random() * 0.85);
    const r = 260;
    pos[i * 3] = r * Math.sin(ph) * Math.cos(th);
    pos[i * 3 + 1] = r * Math.cos(ph) + 10;
    pos[i * 3 + 2] = r * Math.sin(ph) * Math.sin(th);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial({
    color: 0xf1b6a4, size: 0.85, sizeAttenuation: false, transparent: true, opacity: 0.82 })));
})();

/* ---------- 雪原 ---------- */
let terrainMesh;
function terrainHeight(x, z) {
  const rim = Math.max(0, (Math.abs(x) + Math.abs(z)) / 340 - 0.32) * 46;
  return noise2(x, z) * 0.42 + rim * rim * 0.015;
}
(function terrain() {
  const W = 340, SEG = 128;
  const g = new THREE.PlaneGeometry(W, W, SEG, SEG);
  g.rotateX(-Math.PI / 2);
  const p = g.attributes.position;
  const colors = new Float32Array(p.count * 3);
  const low = new THREE.Color(0x291c22), high = new THREE.Color(0x594047), color = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), z = p.getZ(i);
    const y = terrainHeight(x, z);
    p.setY(i, y);
    color.copy(low).lerp(high, Math.max(0, Math.min(1, (y + 5) / 24)));
    colors.set([color.r, color.g, color.b], i * 3);
  }
  g.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  g.computeVertexNormals();
  terrainMesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({
    vertexColors: true, roughness: 0.98 }));
  scene.add(terrainMesh);
})();

/* ---------- 远山与林海：程序化山脊、实例化雪松 ---------- */
function buildRidge(centerZ, layer) {
  const g = new THREE.PlaneGeometry(360, 70, 160, 20);
  g.rotateX(-Math.PI / 2);
  const p = g.attributes.position;
  const colors = new Float32Array(p.count * 3);
  const base = new THREE.Color(layer ? 0x251017 : 0x391119);
  const peak = new THREE.Color(layer ? 0x54202a : 0x873039);
  const snowColor = new THREE.Color(0xb98b81);
  const color = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), z = p.getZ(i);
    const cross = Math.max(0, 1 - Math.abs(z) / 35);
    const ridge = 11 + 8 * Math.sin(x * 0.035 + layer * 2) +
      5 * Math.sin(x * 0.081 - layer) + 17 * Math.pow(Math.max(0, Math.sin(x * 0.022 + layer)), 3);
    const y = 8 + ridge * cross + noise2(x, z + centerZ) * 0.25;
    p.setY(i, y);
    color.copy(base).lerp(peak, Math.min(0.8, Math.max(0, (y - 12) / 34)));
    if (y > 31) color.lerp(snowColor, Math.min(0.3, (y - 31) / 60));
    colors.set([color.r, color.g, color.b], i * 3);
  }
  g.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  g.computeVertexNormals();
  const mesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({
    vertexColors: true, roughness: 1, flatShading: true, side: THREE.DoubleSide }));
  mesh.position.z = centerZ;
  scene.add(mesh);
}
buildRidge(-126, 0);
buildRidge(-163, 1);
buildRidge(126, 0);

(function buildForest() {
  const count = mobile ? 280 : 520;
  const foliageMaterial = new THREE.MeshStandardMaterial({ color: 0x51232d, roughness: 1, flatShading: true });
  const foliage = [
    new THREE.InstancedMesh(new THREE.ConeGeometry(2.35, 5.4, 7), foliageMaterial, count),
    new THREE.InstancedMesh(new THREE.ConeGeometry(1.9, 4.2, 7), foliageMaterial, count),
    new THREE.InstancedMesh(new THREE.ConeGeometry(1.45, 3.2, 7), foliageMaterial, count),
  ];
  const trunks = new THREE.InstancedMesh(
    new THREE.CylinderGeometry(0.13, 0.27, 2.2, 5),
    new THREE.MeshStandardMaterial({ color: 0x261014, roughness: 1, flatShading: true }), count);
  const dummy = new THREE.Object3D();
  let seed = 74291;
  const rnd = () => ((seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0) / 4294967296);
  for (let i = 0; i < count; i++) {
    const a = rnd() * Math.PI * 2, r = 78 + rnd() * 76;
    const x = Math.cos(a) * r, z = Math.sin(a) * r;
    const s = 0.62 + rnd() * 0.82;
    const y = terrainHeight(x, z);
    dummy.rotation.set(0, rnd() * Math.PI, 0);
    const tint = new THREE.Color().setHSL(0.98 + rnd() * 0.025, 0.5, 0.18 + rnd() * 0.1);
    const heights = [2.7, 4.55, 6.05];
    foliage.forEach((layer, j) => {
      dummy.position.set(x, y + heights[j] * s, z);
      dummy.scale.set(s, s, s); dummy.updateMatrix();
      layer.setMatrixAt(i, dummy.matrix); layer.setColorAt(i, tint);
    });
    dummy.position.set(x, y + 0.8 * s, z); dummy.scale.set(s, s, s); dummy.updateMatrix();
    trunks.setMatrixAt(i, dummy.matrix);
  }
  foliage.forEach(layer => { layer.instanceMatrix.needsUpdate = true; scene.add(layer); });
  trunks.instanceMatrix.needsUpdate = true;
  scene.add(trunks);
})();

/* ---------- 落雪 ---------- */
const SNOW_N = mobile ? 2600 : 6200;
const snowGeo = new THREE.BufferGeometry();
const snowPos = new Float32Array(SNOW_N * 3);
const snowSeed = new Float32Array(SNOW_N);
for (let i = 0; i < SNOW_N; i++) {
  snowPos[i * 3] = (Math.random() - 0.5) * 200;
  snowPos[i * 3 + 1] = Math.random() * 60;
  snowPos[i * 3 + 2] = (Math.random() - 0.5) * 200;
  snowSeed[i] = Math.random() * 100;
}
snowGeo.setAttribute('position', new THREE.BufferAttribute(snowPos, 3));
snowGeo.setAttribute('aSeed', new THREE.BufferAttribute(snowSeed, 1));
const snowMaterial = new THREE.ShaderMaterial({
  uniforms: { uTime: { value: 0 }, uWind: { value: 0 }, uRate: { value: 1 } },
  vertexShader: `
    attribute float aSeed; uniform float uTime; uniform float uWind; uniform float uRate;
    varying float vAlpha;
    void main(){
      vec3 p=position;
      p.y=mod(position.y+62.0-uTime*(2.4+aSeed*2.0)*uRate,62.0)-2.0;
      p.x+=sin(uTime*0.18+aSeed*17.0)*1.6+uWind*sin(uTime*0.11+aSeed*9.0)*0.24;
      p.z+=cos(uTime*0.14+aSeed*11.0)*1.1;
      vec4 mv=modelViewMatrix*vec4(p,1.0);
      gl_PointSize=clamp((0.08+fract(aSeed*71.3)*0.17)*(190.0/-mv.z),0.7,7.0);
      gl_Position=projectionMatrix*mv;
      vAlpha=0.42+0.52*fract(sin(aSeed*91.7)*23421.0);
    }`,
  fragmentShader: `
    varying float vAlpha;
    void main(){
      float d=length(gl_PointCoord-0.5);
      float a=(1.0-smoothstep(0.06,0.5,d))*vAlpha*0.48;
      gl_FragColor=vec4(0.92,0.78,0.76,a);
    }`,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
});
const snow = new THREE.Points(snowGeo, snowMaterial);
scene.add(snow);
let wind = 0, snowRate = 1;
function snowStep(t) {
  snowMaterial.uniforms.uTime.value = t;
  snowMaterial.uniforms.uWind.value = wind;
  snowMaterial.uniforms.uRate.value = snowRate;
}

/* ---------- 烽燧（先建塔，灯火的光索要连到它） ---------- */
function makeGlow() {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d');
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)');
  gr.addColorStop(0.35, 'rgba(255,255,255,.5)');
  gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}
const glowTex = makeGlow();

const towers = [];
const towerMeshes = [];
(function towersBuild() {
  const srcs = (S.sources || []).slice().sort((a, b) => (b.supports || []).length - (a.supports || []).length);
  const R = 70, arc = Math.PI * 1.88;
  srcs.forEach((s, i) => {
    const th = -arc / 2 + arc * (srcs.length === 1 ? 0.5 : i / (srcs.length - 1));
    const x = Math.sin(th) * R, z = -Math.cos(th) * R - 100;
    const w = (s.supports || []).length;
    const h = 3.2 + Math.min(w, 40) * 0.33;
    const ground = terrainHeight(x, z);
    const body = new THREE.Mesh(
      new THREE.CylinderGeometry(0.38 + w * 0.02, 0.55 + w * 0.025, h, 7),
      new THREE.MeshStandardMaterial({ color: 0x45141d, emissive: 0x1c0509, emissiveIntensity: 0.38, roughness: 0.9 }));
    body.position.set(x, ground + h / 2, z);
    const top = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTex, color: (s.exclusive || 0) ? 0xe34a43 : 0xc8a24a,
      transparent: true, opacity: w ? 0.9 : 0.4, depthWrite: false,
      blending: THREE.AdditiveBlending }));
    top.scale.setScalar(3 + Math.min(w, 30) * 0.25);
    top.position.set(x, ground + h + 1.6, z);
    scene.add(body); scene.add(top);
    towerMeshes.push(body);
    towers.push({ s, x, y: ground + h + 1.6, z, w, top });
  });
})();

/* ---------- 灯火 ---------- */
const FIRE_N = EVENTS.length;
const fireGeo = new THREE.BufferGeometry();
const fPos = new Float32Array(FIRE_N * 3);
const fCol = new Float32Array(FIRE_N * 3);
const fSize = new Float32Array(FIRE_N);
const fPhase = new Float32Array(FIRE_N);
const fYear = new Float32Array(FIRE_N);
const fireMetas = [];
const supportsOf = {};   // event_id -> [towerIndex]
towers.forEach((t, ti) => (t.s.supports || []).forEach(eid => {
  (supportsOf[eid] = supportsOf[eid] || []).push(ti);
}));
const isRemoved = new Set();          // 被抽离的烽燧 short
const alive = new Array(FIRE_N).fill(true);
const dieT = new Array(FIRE_N).fill(Infinity);   // 各火熄灭动画起点
EVENTS.forEach((e, i) => {
  const [x, y, z] = firePos(e, i);
  fPos.set([x, y, z], i * 3);
  fCol.set(tempOf(e), i * 3);
  const n = Math.min(nSrc(e), 5);
  fSize[i] = 5.5 + n * 4.2;
  fYear[i] = yearOf(e);
  fPhase[i] = (i * 2654435761 % 1000) / 1000 * 6.283;
  fireMetas.push({ e, x, y, z, n, idx: i });
});
fireGeo.setAttribute('position', new THREE.BufferAttribute(fPos, 3));
fireGeo.setAttribute('aColor', new THREE.BufferAttribute(fCol, 3));
fireGeo.setAttribute('aSize', new THREE.BufferAttribute(fSize, 1));
fireGeo.setAttribute('aPhase', new THREE.BufferAttribute(fPhase, 1));
fireGeo.setAttribute('aYear', new THREE.BufferAttribute(fYear, 1));
const fireMat = new THREE.ShaderMaterial({
  uniforms: { uTime: { value: 0 }, uStoryYear: { value: YEAR0 }, uStoryMode: { value: 0 } },
  vertexShader: `
    attribute vec3 aColor; attribute float aSize; attribute float aPhase; attribute float aYear;
    uniform float uTime; uniform float uStoryYear; uniform float uStoryMode;
    varying vec3 vC; varying float vF; varying float vPhase; varying float vStory;
    void main(){
      vC = aColor;
      vF = 1.0 + 0.28 * sin(uTime * 2.4 + aPhase) + 0.12 * sin(uTime * 5.1 + aPhase * 2.3);
      vPhase = aPhase + uTime * (1.1 + fract(aPhase) * 0.7);
      float revealed = smoothstep(aYear - 0.35, aYear + 0.12, uStoryYear);
      float focus = exp(-abs(aYear - uStoryYear) * 1.15);
      vStory = mix(1.0, (0.18 + 0.82 * revealed) * (0.28 + 0.72 * focus), uStoryMode);
      vec4 mv = modelViewMatrix * vec4(position, 1.0);
      gl_PointSize = clamp(aSize * vF * mix(1.0, 0.72 + 0.28 * focus, uStoryMode) * (90.0 / -mv.z), 1.2, 32.0);
      gl_Position = projectionMatrix * mv;
    }`,
  fragmentShader: `
    varying vec3 vC; varying float vF; varying float vPhase; varying float vStory;
    void main(){
      vec2 uv = gl_PointCoord;
      float height = 1.0 - uv.y;
      float wave = sin(uv.y * 12.0 + vPhase) * 0.025 + sin(uv.y * 21.0 - vPhase * 0.7) * 0.012;
      float width = max(0.02, 0.035 + 0.47 * pow(uv.y, 0.76) * (1.0 - 0.1 * sin(uv.y * 3.14159)) + wave);
      float body = 1.0 - smoothstep(width, width + 0.065, abs(uv.x - 0.5));
      float base = smoothstep(0.0, 0.11, uv.y);
      float tip = 1.0 - smoothstep(0.88, 1.0, height);
      float a = body * base * tip;
      float core = 1.0 - smoothstep(0.015, width * 0.58, abs(uv.x - 0.5));
      vec3 flame = mix(vC, vec3(1.0, 0.42, 0.15), core * 0.38);
      gl_FragColor = vec4(flame * (0.68 + 0.2 * vF), a * vStory);
    }`,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
});
scene.add(new THREE.Points(fireGeo, fireMat));
const firePoints = scene.children[scene.children.length - 1];
/* 火光底部的地面光斑（Sprite，熄灭时同步缩小） */
const groundGlows = fireMetas.map(m => {
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex, color: 0xe84a40, transparent: true, opacity: 0.18,
    depthWrite: false, blending: THREE.AdditiveBlending }));
  sp.scale.setScalar(m.n > 1 ? 6 : 3.2);
  sp.position.set(m.x, terrainHeight(m.x, m.z) + 0.15, m.z);
  scene.add(sp);
  return sp;
});

/* 红色时间光幕：只标记当前叙事年份，不连接历史事件。 */
const storyGate = new THREE.Group();
const gateMaterial = new THREE.ShaderMaterial({
  uniforms: { uTime: { value: 0 }, uPulse: { value: 0 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
  fragmentShader: `
    varying vec2 vUv; uniform float uTime; uniform float uPulse;
    void main(){
      float edge = smoothstep(0.0, 0.2, vUv.x) * (1.0 - smoothstep(0.8, 1.0, vUv.x));
      float height = smoothstep(0.0, 0.12, vUv.y) * (1.0 - smoothstep(0.72, 1.0, vUv.y));
      float scan = 0.58 + 0.42 * sin(vUv.y * 14.0 - uTime * 1.7);
      float a = edge * height * scan * (0.10 + uPulse * 0.09);
      gl_FragColor = vec4(1.0, 0.035, 0.065, a);
    }`,
  transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
});
const gateCurtain = new THREE.Mesh(new THREE.PlaneGeometry(44, 54), gateMaterial);
gateCurtain.rotation.y = Math.PI / 2;
gateCurtain.position.y = 27;
const gateHalo = new THREE.Mesh(new THREE.TorusGeometry(17, 0.12, 8, 96),
  new THREE.MeshBasicMaterial({ color: 0xff3b3d, transparent: true, opacity: 0.68, depthWrite: false, blending: THREE.AdditiveBlending }));
gateHalo.rotation.y = Math.PI / 2;
gateHalo.position.y = 24;
const gateFloor = new THREE.Mesh(new THREE.TorusGeometry(16, 0.08, 6, 96),
  new THREE.MeshBasicMaterial({ color: 0xe3423e, transparent: true, opacity: 0.34, depthWrite: false, blending: THREE.AdditiveBlending }));
gateFloor.rotation.x = -Math.PI / 2;
gateFloor.position.y = 0.16;
storyGate.add(gateCurtain, gateHalo, gateFloor);
storyGate.visible = false;
scene.add(storyGate);

/* ---------- 光索流光：粒子沿贝塞尔从烽燧流向灯火 ---------- */
const edges = [];
towers.forEach((t, ti) => (t.s.supports || []).forEach(eid => {
  const m = fireMetas.find(f => f.e.id === eid);
  if (!m) return;
  edges.push({ ti, m, a: new THREE.Vector3(t.x, t.y, t.z), c: new THREE.Vector3(m.x, m.y + 0.5, m.z),
    b: new THREE.Vector3((t.x + m.x) / 2, Math.max(t.y, m.y) + 7 + Math.abs(t.x - m.x) * 0.12, (t.z + m.z) / 2) });
}));
const FLOW_PER = 3;
const flowN = edges.length * FLOW_PER;
const flowGeo = new THREE.BufferGeometry();
const flowPos = new Float32Array(flowN * 3);
const flowT = new Float32Array(flowN), flowSpeed = new Float32Array(flowN), flowEdge = new Int32Array(flowN);
for (let i = 0; i < flowN; i++) {
  flowEdge[i] = Math.floor(i / FLOW_PER);
  flowT[i] = Math.random(); flowSpeed[i] = 0.10 + Math.random() * 0.14;
}
flowGeo.setAttribute('position', new THREE.BufferAttribute(flowPos, 3));
const flowMat = new THREE.PointsMaterial({
  map: glowTex, color: 0xe85b4e, size: 1.05, transparent: true, opacity: 0.85,
  depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
const flowPoints = new THREE.Points(flowGeo, flowMat);
scene.add(flowPoints);
const _v = new THREE.Vector3();
function flowStep(dt) {
  const p = flowGeo.attributes.position;
  for (let i = 0; i < flowN; i++) {
    const ed = edges[flowEdge[i]];
    const ts = towers[ed.ti].s;
    if (isRemoved.has(ts.short || ts.full)) {   // 断索：粒子隐藏但相位保留
      p.setXYZ(i, 0, -999, 0); continue;
    }
    let t = flowT[i] + flowSpeed[i] * dt;
    if (t > 1) t = 0;
    flowT[i] = t;
    const u = 1 - t;
    _v.set(0, 0, 0)
      .addScaledVector(ed.a, u * u)
      .addScaledVector(ed.b, 2 * u * t)
      .addScaledVector(ed.c, t * t);
    p.setXYZ(i, _v.x, _v.y, _v.z);
  }
  p.needsUpdate = true;
}

/* ---------- 遗址石碑：34 个带精度标注的国家级遗址坐标锚点 ---------- */
const siteMeshes = [];
(function sites() {
  const pts = SITES_WITH_COORDS;
  const lat0 = pts.length ? pts.reduce((sum, e) => sum + Number(e.place.lat), 0) / pts.length : 0;
  const lng0 = pts.length ? pts.reduce((sum, e) => sum + Number(e.place.lng), 0) / pts.length : 0;
  const kmX = 111.32 * Math.cos(lat0 * Math.PI / 180);
  const projected = pts.map(e => ({ x: (Number(e.place.lng) - lng0) * kmX, z: -(Number(e.place.lat) - lat0) * 111.32 }));
  const extent = Math.max(...projected.map(p => Math.max(Math.abs(p.x), Math.abs(p.z))), 1);
  const scale = 116 / (extent * 2);
  pts.forEach((s, index) => {
    const x = projected[index].x * scale;
    const z = projected[index].z * scale + 50;
    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(0.7, 2.1, 0.5),
      new THREE.MeshStandardMaterial({ color: 0xa6544e, emissive: 0x3b0d12, emissiveIntensity: 0.22, roughness: 0.85 }));
    const ground = terrainHeight(x, z);
    mesh.position.set(x, ground + 1.05, z);
    const cap = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTex, color: 0xaebccb, transparent: true, opacity: 0.35,
      depthWrite: false, blending: THREE.AdditiveBlending }));
    cap.scale.setScalar(1.6);
    cap.position.set(x, ground + 2.5, z);
    scene.add(mesh); scene.add(cap);
    mesh.userData.site = {
      name: s.summary, address: (s.place && (s.place.modern || s.place.name)) || '',
      category: s.category, batch: s.batch, published: s.published,
      precision: s.place && s.place.precision,
    };
    siteMeshes.push(mesh);
  });
})();

/* ---------- 对勘电弧：日期分歧的火光头顶红色脉冲弧 ---------- */
const arcs = [];
(function dateArcs() {
  const CONFLICTED = new Set(EVENTS.filter(e =>
    new Set((e.date_variants || []).map(v => v && v.value).filter(Boolean)).size > 1
  ).map(e => e.id));
  fireMetas.forEach(m => {
    if (!CONFLICTED.has(m.e.id)) return;
    const cpts = [];
    for (let i = 0; i <= 24; i++) {
      const t = i / 24;
      const x = m.x + (t - 0.5) * 9;
      const y = m.y + 3.2 + Math.sin(t * Math.PI) * 2.6;
      cpts.push(new THREE.Vector3(x, y, m.z));
    }
    const g = new THREE.BufferGeometry().setFromPoints(cpts);
    const mat = new THREE.LineBasicMaterial({ color: 0xb23a2e, transparent: true, opacity: 0.55 });
    scene.add(new THREE.Line(g, mat));
    arcs.push(mat);
  });
})();

/* ---------- 相机 ---------- */
let theta = 0.06, phi = 1.18, radius = mobile ? 67 : 74, dragging = false, px = 0, py = 0;
let pointerOrigin = null, selectedSource = -1;
let autoPan = 0, autoPanZ = -4, targetY = 2;
const activePointers = new Map();
let pinchDistance = 0;
function pointerGap() {
  const points = [...activePointers.values()];
  return points.length < 2 ? 0 : Math.hypot(points[0].x - points[1].x, points[0].y - points[1].y);
}
function applyCam() {
  phi = Math.max(0.5, Math.min(1.45, phi));
  radius = Math.max(24, Math.min(170, radius));
  const cx = autoPan;
  camera.position.set(cx + Math.sin(theta) * Math.sin(phi) * radius,
    Math.cos(phi) * radius + 6,
    Math.cos(theta) * Math.sin(phi) * radius);
  camera.lookAt(cx, targetY, autoPanZ);
}
renderer.domElement.addEventListener('pointerdown', e => {
  stopTour();
  activePointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  renderer.domElement.setPointerCapture(e.pointerId);
  if (e.pointerType === 'touch' && activePointers.size >= 2) {
    pointerOrigin = null; dragging = false; pinchDistance = pointerGap(); return;
  }
  pointerOrigin = { x: e.clientX, y: e.clientY, id: e.pointerId };
  dragging = false; px = e.clientX; py = e.clientY;
});
renderer.domElement.addEventListener('pointerup', e => {
  activePointers.delete(e.pointerId);
  if (activePointers.size < 2) pinchDistance = 0;
  if (!pointerOrigin || pointerOrigin.id !== e.pointerId) return;
  if (!dragging && !renderer.xr.isPresenting) {
    mouse.x = e.clientX / innerWidth * 2 - 1;
    mouse.y = -(e.clientY / innerHeight) * 2 + 1;
    pick();
    if (hoverFire >= 0) {
      showTip();
      const m = fireMetas[hoverFire];
      autoPan = m.x; autoPanZ = m.z; targetY = m.y; radius = mobile ? 44 : 50; applyCam();
    } else if (hoverSite >= 0) showTip();
    else if (hoverTower >= 0) {
      if (selectedSource === hoverTower && mode === 'calm') startStorm(hoverTower);
      else if (mode === 'calm') {
        selectedSource = hoverTower; autoPan = towers[hoverTower].x; autoPanZ = towers[hoverTower].z;
        targetY = towers[hoverTower].y; radius = 42; applyCam(); showTip();
      }
    }
  }
  pointerOrigin = null; dragging = false;
});
renderer.domElement.addEventListener('pointercancel', e => {
  activePointers.delete(e.pointerId); pinchDistance = 0; pointerOrigin = null; dragging = false;
});
addEventListener('pointermove', e => {
  if (activePointers.has(e.pointerId)) {
    activePointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (e.pointerType === 'touch' && activePointers.size >= 2) {
      const gap = pointerGap();
      if (pinchDistance > 0 && gap > 0) radius = Math.max(22, Math.min(170, radius * pinchDistance / gap));
      pinchDistance = gap; pointerOrigin = null; dragging = false; applyCam(); return;
    }
  }
  if (pointerOrigin && pointerOrigin.id === e.pointerId &&
      Math.abs(e.clientX - pointerOrigin.x) + Math.abs(e.clientY - pointerOrigin.y) > 6) dragging = true;
  if (dragging && pointerOrigin) {
    theta -= (e.clientX - px) * 0.004;
    phi -= (e.clientY - py) * 0.003;
    px = e.clientX; py = e.clientY;
    applyCam();
  }
  mouse.x = (e.clientX / innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / innerHeight) * 2 + 1;
  tip.style.left = Math.min(e.clientX + 16, innerWidth - 400) + 'px';
  tip.style.top = Math.min(e.clientY + 14, innerHeight - 220) + 'px';
});
addEventListener('wheel', e => { stopTour(); radius = Math.max(22, Math.min(170, radius * (1 + Math.sign(e.deltaY) * 0.08))); applyCam(); }, { passive: true });
applyCam();

/* ---------- 悬停 ---------- */
const tip = document.getElementById('tip');
const ray = new THREE.Raycaster();
ray.params.Points.threshold = 1.6;
const mouse = new THREE.Vector2(-9, -9);
function esc(s) { return String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
function provBlock(p) {
  if (!p || p.depth === 'none') return '<div class="pv">检索：尚未逐条检索，此处不冒充已查</div>';
  const pr = (p.probes || []).map(b => '查「' + esc(b.q) + '」').join('；');
  const ns = p.not_searched && p.not_searched.length ? '<div class="pv">未查：' + esc(p.not_searched.join('、')) + '</div>' : '';
  return '<div class="pv">' + pr + '</div>' + ns;
}
function archBlock(sources) {
  const links = (sources || []).flatMap(s => {
    const name = (s.book || '来源').split('《')[0];
    return [
      s.archive && { url: s.archive, label: '本地快照' },
      s.url && { url: s.url, label: '来源网页' },
    ].filter(Boolean).map(link => {
      const href = /^https?:/.test(link.url) ? link.url : '../' + link.url;
      return '<a href="' + esc(href) + '" target="_blank" rel="noopener">' +
        esc(name + ' · ' + link.label) + '</a>';
    });
  });
  const hasSnapshot = (sources || []).some(s => s.archive && !/^https?:/.test(s.archive));
  return links.length ? '<div class="pv">来源核查：' + links.join(' · ') +
    (hasSnapshot ? '（本地快照哈希见 manifest.json）' : '') + '</div>' : '';
}
function dvBlock(e) {
  const dvs = (e.date_variants || []).filter(v => v.value);
  if (dvs.length < 2) return '';
  const uniq = [...new Map(dvs.map(v => [v.source + v.value, v])).values()].slice(0, 3);
  return '<div class="dv"><b>对勘</b>' + uniq.map(v =>
    esc(v.value) + '（' + esc(v.source.split('《')[0]) + '）').join('　vs　') + '</div>';
}
let hoverFire = -1, hoverTower = -1, hoverSite = -1;
function pick() {
  ray.setFromCamera(mouse, camera);
  hoverFire = -1; hoverTower = -1; hoverSite = -1;
  const hf = ray.intersectObject(firePoints, false);
  if (hf.length) { hoverFire = hf[0].index; return; }
  const hs = ray.intersectObjects(siteMeshes, false);
  if (hs.length) { hoverSite = siteMeshes.indexOf(hs[0].object); return; }
  let best = 1e9;
  towers.forEach((t, i) => {
    const v = new THREE.Vector3(t.x, t.y, t.z).project(camera);
    if (v.z < 1) {
      const sx = (v.x + 1) / 2 * innerWidth, sy = (-v.y + 1) / 2 * innerHeight;
      const d2 = (sx - (mouse.x + 1) / 2 * innerWidth) ** 2 + (sy - (-mouse.y + 1) / 2 * innerHeight) ** 2;
      if (d2 < 26 ** 2 && d2 < best) { best = d2; hoverTower = i; }
    }
  });
}
function showTip() {
  if (hoverFire >= 0) {
    const m = fireMetas[hoverFire], e = m.e;
    const q = (e.sources || [])[0] || {};
    tip.innerHTML =
      '<div class="t">' + esc(e.event_type || '记载') + ' · ' + (e.date && e.date.start ? esc(e.date.start) : '') +
      (e.place && e.place.name ? ' · ' + esc(e.place.name) : '') + '</div>' +
      esc(e.summary || '') +
      '<div class="q">「' + esc(q.quote || '') + '」<br>——' + esc(q.book || '') + '</div>' +
      (m.n === 1 ? '<div class="w">库内目前只有一家来源机构记载；不等于历史只有这一种记载。</div>' : '') +
      dvBlock(e) +
      (e.conflict_group && VERD[e.conflict_group]
        ? '<div class="dv"><b>裁决</b>' + esc(VERD[e.conflict_group].ruling) + ' 基准 ' + esc(VERD[e.conflict_group].adopt) + '</div>' : '') +
      archBlock(e.sources) + provBlock(e.provenance);
    tip.classList.add('on');
  } else if (hoverTower >= 0) {
    const t = towers[hoverTower];
    tip.innerHTML =
      '<div class="t">烽燧 · ' + esc(t.s.short || '') + '</div>' + esc(t.s.full || '') +
      '<div class="q">支撑 ' + (t.s.supports || []).length + ' 条记载 · 单点支撑 ' + (t.s.exclusive || 0) + ' 条 · 可靠性标签 ' + esc(t.s.reliability_cn || '') + '</div>' +
      '<div class="pv">机构数量表示记载覆盖，不证明史源相互独立。点击烽燧两次，可按库内关系执行风雪试验。</div>';
    tip.classList.add('on');
  } else if (hoverSite >= 0) {
    const s = siteMeshes[hoverSite].userData.site;
    tip.innerHTML =
      '<div class="t">国家级抗战遗址 · 地理锚点</div>' + esc(s.name) +
      '<div class="q">' + esc(s.address || '') + '<br>' + esc(s.category || '') + ' · 国务院第 ' + esc(s.batch) + ' 批名录（' + esc(s.published) + '）</div>' +
      '<div class="pv">坐标精度：' + esc(s.precision || '未注明') + '。场景按经纬关系等比缩放；不代表海拔、道路或遗址现场复原。</div>';
    tip.classList.add('on');
  } else tip.classList.remove('on');
}

/* ---------- 风雪夜 / 程斌之夜 / 余烬 / 复原 ---------- */
const CHAIN = ['evt_1938_chengbin_toudi', 'evt_1940_yangjingyu_xunguo'];   // 叙事并置，不代表已验证因果边
let mode = 'calm', stormStart = 0;
const tour = { active: false, started: 0, elapsed: 0, stage: -1, year: YEAR0, goal: null };
const storyCap = document.getElementById('cap');
const storyStep = document.getElementById('cap-step');
const storyTitle = document.getElementById('cap-title');
const storyBody = document.getElementById('cap-copy');
const storySource = document.getElementById('cap-source');
const storyClock = document.getElementById('cap-clock');
const storyProgressBar = document.getElementById('cap-progress');
const storyNav = document.getElementById('cap-nav');
const storyProgress = [...document.querySelectorAll('#cap-progress button')];
const storyPrev = document.getElementById('b-story-prev');
const storyNext = document.getElementById('b-story-next');
let storyGlowYear = NaN;
function yearToX(year) {
  return ((year - YEAR0) / Math.max(1, YEAR1 - YEAR0) - 0.5) * SPAN;
}
function updateStoryGlow(year) {
  if (Number.isFinite(storyGlowYear) && Math.abs(year - storyGlowYear) < 0.025) return;
  storyGlowYear = year;
  groundGlows.forEach((glow, i) => {
    const eventYear = yearOf(fireMetas[i].e);
    const revealed = Math.max(0, Math.min(1, (year - eventYear + 0.2) / 0.75));
    const focus = Math.exp(-Math.abs(eventYear - year) * 0.7);
    glow.material.opacity = 0.18 * (0.22 + 0.78 * revealed) * (0.36 + 0.64 * focus);
  });
}
function storyClockText(seconds) {
  const n = Math.max(0, Math.min(STORY_CHAPTERS.length * STORY_SECONDS, Math.floor(seconds)));
  return Math.floor(n / 60) + ':' + String(n % 60).padStart(2, '0') + ' / 1:20';
}
function updateStoryProgress(elapsed) {
  const index = Math.max(0, Math.min(STORY_CHAPTERS.length - 1, Math.floor(elapsed / STORY_SECONDS)));
  const within = Math.max(0, Math.min(1, (elapsed - index * STORY_SECONDS) / STORY_SECONDS));
  storyProgress.forEach((button, i) => {
    const fill = i < index ? 1 : i === index ? within : 0;
    const fillValue = (fill * 100) + '%';
    if (button.style.getPropertyValue('--fill') !== fillValue) button.style.setProperty('--fill', fillValue);
    if (button.classList.contains('past') !== (i < index)) button.classList.toggle('past', i < index);
    if (button.classList.contains('current') !== (i === index)) button.classList.toggle('current', i === index);
    if (i === index && button.getAttribute('aria-current') !== 'step') button.setAttribute('aria-current', 'step');
    else if (i !== index && button.hasAttribute('aria-current')) button.removeAttribute('aria-current');
  });
  const clockText = storyClockText(elapsed);
  if (storyClock.textContent !== clockText) storyClock.textContent = clockText;
  if (storyPrev.disabled !== (index === 0)) storyPrev.disabled = index === 0;
  if (storyNext.disabled !== (index === STORY_CHAPTERS.length - 1)) storyNext.disabled = index === STORY_CHAPTERS.length - 1;
}
function renderStoryChapter(index) {
  const chapter = STORY_CHAPTERS[index];
  if (!chapter) return;
  const exact = chapter.ids.map(id => fireMetas.find(m => m.e.id === id)).filter(Boolean);
  const candidates = exact.length ? exact : fireMetas.filter(m => yearOf(m.e) >= chapter.from && yearOf(m.e) <= chapter.to);
  const nearest = candidates.length ? candidates : fireMetas.slice().sort((a, b) =>
    Math.abs(yearOf(a.e) - chapter.from) - Math.abs(yearOf(b.e) - chapter.from)).slice(0, 1);
  const focus = nearest.length ? nearest : fireMetas;
  const center = focus.reduce((p, m) => ({ x: p.x + m.x / focus.length, y: p.y + m.y / focus.length, z: p.z + m.z / focus.length }), { x: 0, y: 0, z: 0 });
  const [nextTheta, nextPhi, nextRadius] = chapter.camera;
  if (reducedMotion) tour.goal = null;
  else setTourView(center.x, center.y + 1.6, center.z, nextTheta, nextPhi, nextRadius);
  tour.year = chapter.from;
  fireMat.uniforms.uStoryYear.value = tour.year;
  fireMat.uniforms.uStoryMode.value = 1;
  updateStoryGlow(tour.year);
  storyGate.visible = true;
  storyGate.position.set(yearToX(tour.year), terrainHeight(yearToX(tour.year), 0), 0);
  storyStep.textContent = '第 ' + String(index + 1).padStart(2, '0') + ' 幕 / 08  ·  ' + chapter.from + (chapter.to !== chapter.from ? '—' + chapter.to : '');
  storyTitle.textContent = chapter.title;
  if (chapter.closing) {
    const multi = EVENTS.filter(e => nSrc(e) > 1).length;
    const firstHand = EVENTS.filter(e => (e.sources || []).some(s => s.reliability === 'A')).length;
    storyBody.textContent = '当前数据库收录 ' + EVENTS.length + ' 条事件记载，其中 ' + multi + ' 条有两家以上来源机构记载；机构数量不等于独立史源。A 类一手档案支撑 ' + firstHand + ' / ' + EVENTS.length + ' 条，尚未补齐的也如实留下。核查，是纪念的一种方式。';
    storySource.textContent = '当前数据快照 · 每一簇火光均可查看对应记载与出处';
  } else {
    storyBody.textContent = chapter.body;
    storySource.textContent = '本幕 ' + focus.length + ' 条事件记载 · 选择火光可继续核对出处';
  }
  storyCap.classList.add('on');
  storyProgressBar.hidden = false;
  storyNav.hidden = false;
  document.body.classList.add('story-active');
  tour.stage = index;
  updateStoryProgress(tour.elapsed);
}
function setCaption(title, copy, note) {
  storyCap.classList.add('on');
  storyProgressBar.hidden = true;
  storyNav.hidden = true;
  document.body.classList.remove('story-active');
  storyStep.textContent = title || '';
  storyTitle.textContent = '';
  storyBody.textContent = copy || '';
  storySource.textContent = note || '';
  storyProgress.forEach(button => button.classList.remove('past', 'current'));
}
function hideStory() {
  tour.active = false; tour.elapsed = 0; tour.stage = -1; tour.goal = null;
  storyCap.classList.remove('on');
  storyProgressBar.hidden = true;
  storyNav.hidden = true;
  document.body.classList.remove('story-active');
  storyGate.visible = false;
  fireMat.uniforms.uStoryMode.value = 0;
  fireMat.uniforms.uStoryYear.value = YEAR0;
  storyGlowYear = NaN;
  groundGlows.forEach(glow => { glow.material.opacity = 0.18; });
  const button = document.getElementById('b-tour');
  button.textContent = '剧情漫游'; button.classList.remove('on');
}
function stopTour(label) {
  if (!tour.active) return;
  tour.elapsed = Math.min(STORY_CHAPTERS.length * STORY_SECONDS, Math.max(0, performance.now() / 1000 - tour.started));
  tour.active = false; tour.goal = null;
  const button = document.getElementById('b-tour');
  button.textContent = label || '继续剧情'; button.classList.remove('on');
}

function computeDeaths() {
  const dead = [];
  fireMetas.forEach((m, i) => {
    const sup = supportsOf[m.e.id] || [];
    const liveSup = sup.filter(ti => !isRemoved.has(towers[ti].s.short || towers[ti].s.full));
    if (sup.length && liveSup.length === 0) dead.push(i);
  });
  return dead;
}
function startStorm(sourceIndex, fromTour) {
  if (!fromTour) stopTour();
  hideStory();
  if (!towers.length) return;
  if (mode !== 'calm') reset();
  mode = 'storm'; stormStart = performance.now() / 1000;
  selectedSource = Number.isInteger(sourceIndex) ? Math.max(0, Math.min(towers.length - 1, sourceIndex)) : 0;
  isRemoved.add(towers[selectedSource].s.short || towers[selectedSource].s.full);
  const dead = computeDeaths();
  const t0 = performance.now() / 1000;
  dead.forEach((idx, k) => { dieT[idx] = t0 + 0.4 + k * 0.10; alive[idx] = false; });
  /* 风起 */
  wind = 2.4; snowRate = 4.0;
  scene.fog.density = 0.020;
  amb.intensity = 0.45; moon.intensity = 0.25;
  flowMat.opacity = 0.25;
}
function startEmbers() {
  stopTour();
  if (mode !== 'calm') reset();
  hideStory();
  mode = 'embers'; stormStart = performance.now() / 1000;
  fireMetas.forEach((m, i) => {
    if (yearOf(m.e) >= 1941) { dieT[i] = stormStart + 1.0 + (i % 8) * 0.12; alive[i] = false; }
  });
  autoPan = fireMetas.reduce((a, m) => a + m.x, 0) / FIRE_N - SPAN / 2 + 6;
  setCaption('十四年 · 余烬', '1941 年之后的条目在这一体验模式中熄灭。',
    '本库 ' + FIRE_N + ' 条记载中，' + fireMetas.filter(m => nSrc(m.e) > 1).length +
    ' 条有多家来源机构记载。机构数量不代表史源彼此独立；熄灭效果也不表示据点的实际存续时间。');
}
function reset() {
  if (tour.active) stopTour();
  tour.elapsed = 0; tour.stage = -1; tour.goal = null;
  mode = 'calm';
  selectedSource = -1;
  hideStory();
  isRemoved.clear();
  alive.fill(true); dieT.fill(Infinity);
  panelShown = false;
  wind = 0; snowRate = 1; autoPan = 0; autoPanZ = -4; targetY = 2;
  scene.fog.density = 0.006;
  amb.intensity = 0.72; moon.intensity = 0.72;
  flowMat.opacity = 0.9;
  theta = 0.06; phi = 1.18; radius = mobile ? 67 : 74;
  /* 火光属性整体复位（含熄灭中被改写的大小/颜色/光斑） */
  fireMetas.forEach((m, i) => {
    fireGeo.attributes.aSize.setX(i, 5.5 + Math.min(m.n, 5) * 4.2);
    const c = tempOf(m.e);
    fireGeo.attributes.aColor.setXYZ(i, c[0], c[1], c[2]);
    groundGlows[i].material.opacity = 0.18;
    groundGlows[i].scale.setScalar(m.n > 1 ? 6 : 3.2);
  });
  fireGeo.attributes.aSize.needsUpdate = true;
  fireGeo.attributes.aColor.needsUpdate = true;
  if (chainLine) {
    scene.remove(chainLine);
    chainLine.geometry.dispose();
    chainLine.material.dispose();
    chainLine = null;
  }
  document.getElementById('panel').classList.remove('on');
  xrCard.visible = false;
  ['b-storm', 'b-chengbin', 'b-embers'].forEach(id => document.getElementById(id).classList.remove('on'));
  if (!renderer.xr.isPresenting) applyCam();
}
let chainLine = null;
let panelShown = false;
function showPeopleThread() {
  stopTour();
  hideStory();
  if (mode !== 'calm') reset();
  mode = 'people';
  const m1 = fireMetas.find(m => m.e.id === CHAIN[0]);
  const m2 = fireMetas.find(m => m.e.id === CHAIN[1]);
  if (m1 && m2) {
    const control = new THREE.Vector3((m1.x + m2.x) / 2,
      Math.max(m1.y, m2.y) + 8, (m1.z + m2.z) / 2);
    const pts = [];
    for (let i = 0; i <= 36; i++) {
      const t = i / 36, u = 1 - t;
      pts.push(new THREE.Vector3(
        u * u * m1.x + 2 * u * t * control.x + t * t * m2.x,
        u * u * m1.y + 2 * u * t * control.y + t * t * m2.y,
        u * u * m1.z + 2 * u * t * control.z + t * t * m2.z));
    }
    chainLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(pts),
      new THREE.LineDashedMaterial({ color: 0xe34a43, transparent: true, opacity: 0.9, dashSize: 1.2, gapSize: 0.8 }));
    chainLine.computeLineDistances(); scene.add(chainLine);
    autoPan = (m1.x + m2.x) / 2; autoPanZ = (m1.z + m2.z) / 2;
    targetY = (m1.y + m2.y) / 2; radius = 54; theta = 0.12; phi = 1.1; applyCam();
    setCaption('人物脉络', '两条人物相关记载以虚线并置。', '本库未建立事件级因果关系；此线不进入来源支撑与风雪结算。');
  } else {
    setCaption('人物脉络', '当前数据未同时找到这两条人物相关记载。', '');
  }
  document.getElementById('b-chengbin').classList.add('on');
}
function maybeSettle(now) {
  if (panelShown || mode !== 'storm') return;
  const finite = dieT.filter(Number.isFinite);
  const last = finite.length ? Math.max(...finite) : stormStart;
  if (now < last + 1.2) return;
  panelShown = true;
  const died = alive.filter(a => !a).length;
  const left = FIRE_N - died;
  const multiLeft = fireMetas.filter((m, i) => alive[i] && m.n > 1).length;
  const removedKey = [...isRemoved][0];
  const removedTower = towers.find(t => (t.s.short || t.s.full) === removedKey) || towers[0];
  document.getElementById('b-storm').classList.add('on');
  const lines = '<em>' + esc(removedTower.s.short || removedTower.s.full) + '</em> 被抽离后，按本库支撑关系计算，有 ' + died +
      ' 条记载失去全部剩余来源支撑。';
  document.getElementById('p-h').textContent = '风 雪 夜 · 结 算';
  document.getElementById('p-big').innerHTML = '熄灭 <b>' + died + '</b> 条 · 幸存 <b>' + left + '</b> 条（其中多家来源机构记载 ' + multiLeft + ' 条）';
  document.getElementById('p-lines').innerHTML = lines +
    '<br><span style="opacity:.6;font-size:11px">熄灭依据是支撑关系计算；来源记录数量不等于独立史源数量。</span>';
  if (renderer.xr.isPresenting) {
    xrCardText('风雪夜 · 结算', '熄灭 ' + died + ' 条 · 幸存 ' + left + ' 条',
      removedTower.s.short || removedTower.s.full, '扣动任一扳机复原场景');
  } else document.getElementById('panel').classList.add('on');
}
document.getElementById('b-storm').onclick = () => startStorm();
document.getElementById('b-chengbin').onclick = showPeopleThread;
document.getElementById('b-embers').onclick = () => startEmbers();
document.getElementById('b-reset').onclick = reset;
document.getElementById('p-close').onclick = reset;

/* ---------- 八幕剧情漫游：按事件年份推进的实时镜头 ---------- */
const tourButton = document.getElementById('b-tour');
function setTourView(x, y, z, nextTheta, nextPhi, nextRadius) {
  tour.goal = { x, y, z, theta: nextTheta, phi: nextPhi, radius: nextRadius };
}
function jumpToChapter(index) {
  const next = Math.max(0, Math.min(STORY_CHAPTERS.length - 1, index));
  if (mode !== 'calm') reset();
  const now = performance.now() / 1000;
  tour.elapsed = next * STORY_SECONDS;
  tour.started = now - tour.elapsed;
  tour.active = true;
  tour.stage = -1;
  tour.goal = null;
  tourButton.textContent = '暂停剧情'; tourButton.classList.add('on');
  document.body.classList.add('story-active');
  tourStep(now, 0);
}
function tourStep(now, dt) {
  if (!tour.active) return;
  const total = STORY_CHAPTERS.length * STORY_SECONDS;
  const elapsed = Math.min(total, Math.max(0, now - tour.started));
  tour.elapsed = elapsed;
  if (elapsed >= total) {
    tour.active = false; tour.goal = null;
    tourButton.textContent = '重看剧情'; tourButton.classList.remove('on');
    updateStoryProgress(total);
    return;
  }
  const stage = Math.min(STORY_CHAPTERS.length - 1, Math.floor(elapsed / STORY_SECONDS));
  if (stage !== tour.stage) renderStoryChapter(stage);
  const chapter = STORY_CHAPTERS[stage];
  const portion = reducedMotion ? 0 : Math.max(0, Math.min(1, (elapsed - stage * STORY_SECONDS) / STORY_SECONDS));
  const eased = portion * portion * (3 - 2 * portion);
  tour.year = chapter.from + (chapter.to - chapter.from) * eased;
  fireMat.uniforms.uStoryYear.value = tour.year;
  updateStoryGlow(tour.year);
  storyGate.position.x = yearToX(tour.year);
  storyGate.position.y = terrainHeight(storyGate.position.x, 0);
  gateMaterial.uniforms.uPulse.value = reducedMotion ? 0.45 : 0.5 + 0.5 * Math.sin(now * 1.2);
  updateStoryProgress(elapsed);
  if (!tour.goal) return;
  const k = reducedMotion ? 0 : 1 - Math.exp(-dt * 1.1);
  autoPan += (tour.goal.x - autoPan) * k;
  autoPanZ += (tour.goal.z - autoPanZ) * k;
  targetY += (tour.goal.y - targetY) * k;
  const angle = Math.atan2(Math.sin(tour.goal.theta - theta), Math.cos(tour.goal.theta - theta));
  theta += angle * k; phi += (tour.goal.phi - phi) * k; radius += (tour.goal.radius - radius) * k;
}
tourButton.addEventListener('click', () => {
  if (tour.active) {
    stopTour('继续剧情');
    return;
  }
  const resumable = tour.elapsed > 0 && tour.elapsed < STORY_CHAPTERS.length * STORY_SECONDS && mode === 'calm' && document.body.classList.contains('story-active');
  if (!resumable) reset();
  const now = performance.now() / 1000;
  tour.started = now - tour.elapsed;
  tour.active = true; tour.stage = -1; tour.goal = null;
  tourButton.textContent = '暂停剧情'; tourButton.classList.add('on');
  document.body.classList.add('story-active');
  tourStep(now, 0);
});
storyProgress.forEach((button, index) => button.addEventListener('click', () => jumpToChapter(index)));
storyPrev.addEventListener('click', () => jumpToChapter(Math.min(STORY_CHAPTERS.length - 1, Math.floor(tour.elapsed / STORY_SECONDS)) - 1));
storyNext.addEventListener('click', () => jumpToChapter(Math.min(STORY_CHAPTERS.length - 1, Math.floor(tour.elapsed / STORY_SECONDS)) + 1));

/* 手机方向传感器环视：只提供 3DoF 朝向，不称作头显 VR。 */
const gyroButton = document.getElementById('b-gyro');
let gyroActive = false;
function stopGyro() {
  if (!gyroActive) return;
  removeEventListener('deviceorientation', onDeviceOrientation);
  gyroActive = false; gyroButton.textContent = '开启手机环视'; gyroButton.classList.remove('on');
}
function onDeviceOrientation(event) {
  if (event.alpha == null || event.beta == null || event.gamma == null || renderer.xr.isPresenting) return;
  const radians = Math.PI / 180;
  const screenAngle = (screen.orientation && screen.orientation.angle) || window.orientation || 0;
  const euler = new THREE.Euler(event.beta * radians, event.alpha * radians, -event.gamma * radians, 'YXZ');
  const orientation = new THREE.Quaternion().setFromEuler(euler)
    .multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 0, 1), -screenAngle * radians))
    .multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), -Math.PI / 2));
  const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(orientation);
  theta = Math.atan2(-forward.x, -forward.z);
  phi = Math.acos(Math.max(-1, Math.min(1, -forward.y)));
  applyCam();
}
gyroButton.addEventListener('click', async () => {
  if (gyroActive) { stopGyro(); return; }
  stopTour();
  const Orientation = window.DeviceOrientationEvent;
  if (!Orientation || !isSecureContext) {
    document.getElementById('vr-hint').textContent = '手机环视需要支持方向传感器的设备，并通过 HTTPS 或本机安全来源打开。';
    return;
  }
  try {
    if (typeof Orientation.requestPermission === 'function' && await Orientation.requestPermission() !== 'granted') {
      document.getElementById('vr-hint').textContent = '未获得方向传感器授权；可继续使用触控拖动场景。';
      return;
    }
    addEventListener('deviceorientation', onDeviceOrientation);
    gyroActive = true; gyroButton.textContent = '关闭手机环视'; gyroButton.classList.add('on');
    document.getElementById('vr-hint').textContent = '手机方向环视已开启：仅跟随朝向，不提供 6DoF 位移。';
  } catch (_) {
    document.getElementById('vr-hint').textContent = '方向传感器不可用；可继续使用触控拖动场景。';
  }
});
if (!window.DeviceOrientationEvent) gyroButton.disabled = true;

/* ---------- WebXR：双目 6DoF、手柄选取、地面瞬移与世界空间证据卡 ---------- */
const xrCanvas = document.createElement('canvas');
xrCanvas.width = 1024; xrCanvas.height = 512;
const xrContext = xrCanvas.getContext('2d');
const xrTexture = new THREE.CanvasTexture(xrCanvas);
xrTexture.minFilter = THREE.LinearFilter;
const xrCard = new THREE.Mesh(new THREE.PlaneGeometry(4.0, 2.0), new THREE.MeshBasicMaterial({
  map: xrTexture, transparent: true, depthWrite: false, side: THREE.DoubleSide
}));
xrCard.visible = false;
scene.add(xrCard);
function xrCardText(title, summary, quote, source) {
  const c = xrContext;
  c.clearRect(0, 0, 1024, 512);
  c.fillStyle = 'rgba(22,7,12,.95)'; c.fillRect(0, 0, 1024, 512);
  c.strokeStyle = '#e34a43'; c.lineWidth = 5; c.strokeRect(8, 8, 1008, 496);
  c.fillStyle = '#e4bd78'; c.font = '600 28px serif'; c.fillText(String(title || '').slice(0, 42), 42, 64);
  c.fillStyle = '#fff0e6'; c.font = '34px serif'; c.fillText(String(summary || '').slice(0, 44), 42, 136);
  c.fillStyle = '#f1c58e'; c.font = '25px serif'; c.fillText(String(quote || '').slice(0, 58), 42, 244);
  c.fillStyle = '#c9aaa0'; c.font = '20px serif'; c.fillText(String(source || '').slice(0, 72), 42, 438);
  xrTexture.needsUpdate = true;
  xrCard.visible = renderer.xr.isPresenting;
}
function xrCardPose() {
  if (!xrCard.visible || !renderer.xr.isPresenting) return;
  const xrCamera = renderer.xr.getCamera(camera);
  const position = xrCamera.getWorldPosition(new THREE.Vector3());
  const quaternion = xrCamera.getWorldQuaternion(new THREE.Quaternion());
  const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(quaternion);
  xrCard.position.copy(position).addScaledVector(forward, 2.35);
  xrCard.position.y -= 0.08;
  xrCard.quaternion.copy(quaternion);
}
const xrRay = new THREE.Raycaster();
function setControllerRay(controller) {
  const origin = controller.getWorldPosition(new THREE.Vector3());
  const rotation = controller.getWorldQuaternion(new THREE.Quaternion());
  const direction = new THREE.Vector3(0, 0, -1).applyQuaternion(rotation).normalize();
  xrRay.ray.origin.copy(origin); xrRay.ray.direction.copy(direction);
  xrRay.near = 0.05; xrRay.far = 75;
}
function controllerSelect(controller) {
  if (panelShown) { reset(); return; }
  setControllerRay(controller);
  const fire = xrRay.intersectObject(firePoints, false)[0];
  if (fire && fire.index != null) {
    const m = fireMetas[fire.index], q = (m.e.sources || [])[0] || {};
    xrCardText((m.e.event_type || '记载') + ' · ' + (m.e.date && m.e.date.start || ''), m.e.summary, q.quote, q.book);
    return;
  }
  const towerHit = xrRay.intersectObjects(towerMeshes, false)[0];
  if (towerHit) {
    const index = towerMeshes.indexOf(towerHit.object), tower = towers[index];
    if (selectedSource === index && mode === 'calm') startStorm(index);
    else {
      selectedSource = index;
      xrCardText('烽燧 · ' + (tower.s.short || ''), tower.s.full,
        '支撑 ' + tower.w + ' 条 · 单点支撑 ' + (tower.s.exclusive || 0) + ' 条', '再次扣动扳机：移除该来源');
    }
    return;
  }
  const siteHit = xrRay.intersectObjects(siteMeshes, false)[0];
  if (siteHit) {
    const site = siteHit.object.userData.site;
    xrCardText('地理锚点 · 坐标精度 ' + (site.precision || '未注明'), site.name, site.address, site.category);
  }
}
function controllerTeleport(controller) {
  setControllerRay(controller);
  const ground = xrRay.intersectObject(terrainMesh, false)[0];
  if (!ground) return;
  const head = renderer.xr.getCamera(camera).getWorldPosition(new THREE.Vector3());
  camera.position.x += ground.point.x - head.x;
  camera.position.z += ground.point.z - head.z;
}
const xrControllers = [];
for (let i = 0; i < 2; i++) {
  const controller = renderer.xr.getController(i);
  const pointer = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3(0, 0, -1)]),
    new THREE.LineBasicMaterial({ color: 0xff554d, transparent: true, opacity: 0.8 })
  );
  pointer.scale.z = 75; pointer.frustumCulled = false;
  controller.add(pointer);
  controller.visible = false;
  controller.addEventListener('select', () => controllerSelect(controller));
  controller.addEventListener('squeeze', () => controllerTeleport(controller));
  scene.add(controller); xrControllers.push(controller);
}
const vrButton = document.getElementById('b-vr');
const vrHint = document.getElementById('vr-hint');
let xrSession = null;
async function detectXR() {
  if (!navigator.xr || !isSecureContext) {
    vrButton.disabled = true; vrButton.textContent = '需要 HTTPS 头显浏览器';
    vrHint.textContent = 'WebXR 需要安全来源与兼容头显；手机环视不等于头显 VR。';
    return;
  }
  try {
    const supported = await navigator.xr.isSessionSupported('immersive-vr');
    vrButton.disabled = !supported;
    vrButton.textContent = supported ? '进入沉浸式 VR' : '未检测到 VR 头显';
    vrHint.textContent = supported
      ? '6DoF 双目 · 手柄查看 · 再扣扳机抽离烽燧 · 握把瞬移'
      : '请用 Quest / Pico 等支持 WebXR 的头显浏览器打开 HTTPS 页面。';
  } catch (_) {
    vrButton.disabled = true; vrButton.textContent = 'VR 暂不可用';
    vrHint.textContent = '浏览器未开放 immersive-vr 会话。';
  }
}
renderer.xr.addEventListener('sessionstart', () => {
  stopTour('继续剧情');
  stopGyro();
  for (const controller of xrControllers) controller.visible = true;
  const features = xrSession && xrSession.enabledFeatures || [];
  const floorSpace = features.includes('local-floor');
  camera.position.set(0, floorSpace ? 0 : 1.65, 24);
  camera.quaternion.identity(); camera.updateMatrixWorld(true);
  xrCard.visible = false; vrButton.textContent = '退出沉浸式 VR';
  vrHint.textContent = '扳机：查看 / 选取烽燧 · 再扣扳机：抽离 · 握把：地面瞬移';
});
renderer.xr.addEventListener('sessionend', () => {
  xrSession = null; xrCard.visible = false;
  for (const controller of xrControllers) controller.visible = false;
  applyCam(); detectXR();
});
vrButton.addEventListener('click', async () => {
  if (renderer.xr.isPresenting && xrSession) { await xrSession.end(); return; }
  vrButton.disabled = true; vrButton.textContent = '正在连接头显…';
  try {
    xrSession = await navigator.xr.requestSession('immersive-vr', {
      optionalFeatures: ['local-floor', 'bounded-floor']
    });
    const enabled = xrSession.enabledFeatures || [];
    renderer.xr.setReferenceSpaceType(enabled.includes('local-floor') ? 'local-floor' : 'local');
    await renderer.xr.setSession(xrSession);
    vrButton.disabled = false;
  } catch (error) {
    if (xrSession) { try { await xrSession.end(); } catch (_) {} }
    xrSession = null; vrButton.disabled = false; vrButton.textContent = '重试进入 VR';
    vrHint.textContent = error.message || '头显会话未能启动，请检查连接与浏览器授权。';
  }
});
detectXR();

/* ---------- 熄灭动画 ---------- */
function dieStep(now) {
  const col = fireGeo.attributes.aColor, siz = fireGeo.attributes.aSize;
  let dirty = false;
  fireMetas.forEach((m, i) => {
    if (alive[i]) return;
    const k = reducedMotion
      ? (now < dieT[i] ? -1 : 1)
      : (now - dieT[i]) / 1.6;                   // 减少动态效果时保留分段时序并直接熄灭
    if (k < 0) return;
    dirty = true;
    const base = 5.5 + Math.min(m.n, 5) * 4.2;
    const f = Math.max(0, 1 - k);
    siz.setX(i, Math.max(k >= 1 ? 0 : base * f * (1 - 0.4 * Math.sin(k * 9)), 0));
    const c0 = tempOf(m.e);
    col.setXYZ(i, c0[0] * f + 0.35 * (1 - f), c0[1] * f + 0.18 * (1 - f), c0[2] * f + 0.10 * (1 - f));
    groundGlows[i].material.opacity = Math.max(0, 0.18 * f);
    groundGlows[i].scale.setScalar(Math.max(0.01, (m.n > 1 ? 6 : 3.2) * Math.max(f, 0.01)));
  });
  if (dirty) { col.needsUpdate = true; siz.needsUpdate = true; }
}

/* ---------- 主循环 ---------- */
const stat = document.getElementById('stat');
const clock = new THREE.Clock();
let arcT = 0;
function loop() {
  const now = performance.now() / 1000;
  const dt = reducedMotion ? 0 : Math.min(clock.getDelta(), 0.05);
  const t = reducedMotion ? 0 : clock.elapsedTime;
  fireMat.uniforms.uTime.value = t;
  gateMaterial.uniforms.uTime.value = t;
  arcT += dt;
  arcs.forEach((m, i) => { m.opacity = 0.35 + 0.3 * Math.abs(Math.sin(arcT * 2.2 + i)); });
  snowStep(t);
  flowStep(dt);
  dieStep(now);
  maybeSettle(now);
  if (!renderer.xr.isPresenting) {
    tourStep(now, dt);
    if (mode === 'embers') autoPan += dt * 1.6;
    if (!dragging) applyCam();
    pick(); showTip();
  } else {
    xrCardPose();
  }
  const aliveN = alive.filter(Boolean).length;
  const statusText = mode === 'calm'
    ? (document.body.classList.contains('story-active')
      ? '剧情 ' + String(Math.max(0, tour.stage) + 1).padStart(2, '0') + ' / 08 · ' + (tour.active ? '实时推进' : '可选章节继续浏览')
      : '灯火 ' + FIRE_N + ' · 烽燧 ' + towers.length + ' · 遗址 ' + siteMeshes.length + '（经纬投影） · 流光 ' + flowN)
    : (mode === 'embers' ? '余烬：1941 后的火，和仍然亮着的证据'
      : mode === 'people' ? '人物脉络：虚线并置，不参与支撑关系与熄灭计算'
        : '风雪中的雪原：幸存灯火 ' + aliveN + ' / ' + FIRE_N);
  if (stat.textContent !== statusText) stat.textContent = statusText;
  renderer.render(scene, camera);
}
renderer.setAnimationLoop(loop);
setTimeout(() => document.getElementById('loading').classList.add('off'), 350);
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});
})();
