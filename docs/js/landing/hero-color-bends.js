/**
 * Social R - Hero ColorBends Shader Module (Procedural WebGL)
 * Adapted from Estadística Correlacional Interactiva with Social R's Electric Blue / Indigo / Violet chromatic palette.
 */
import * as THREE from "../vendor/three.module.min.js";

const MAX_COLORS = 8;

const frag = `
#define MAX_COLORS ${MAX_COLORS}
uniform vec2 uCanvas;
uniform float uTime;
uniform float uSpeed;
uniform vec2 uRot;
uniform int uColorCount;
uniform vec3 uColors[MAX_COLORS];
uniform int uTransparent;
uniform float uScale;
uniform float uFrequency;
uniform float uWarpStrength;
uniform vec2 uPointer; // in NDC [-1,1]
uniform float uMouseInfluence;
uniform float uParallax;
uniform float uNoise;
uniform int uIterations;
uniform float uIntensity;
uniform float uBandWidth;
varying vec2 vUv;

float softEllipse(vec2 p, vec2 center, vec2 radius) {
  vec2 d = (p - center) / radius;
  float dist = dot(d, d);
  return 1.0 - smoothstep(0.55, 1.25, dist);
}

void main() {
  float t = uTime * uSpeed;
  vec2 p = vUv * 2.0 - 1.0;
  p += uPointer * uParallax * 0.1;
  vec2 rp = vec2(p.x * uRot.x - p.y * uRot.y, p.x * uRot.y + p.y * uRot.x);
  vec2 q = vec2(rp.x * (uCanvas.x / uCanvas.y), rp.y);
  q /= max(uScale, 0.0001);
  q /= 0.5 + 0.2 * dot(q, q);
  q += 0.2 * cos(t) - 7.56;
  vec2 toward = (uPointer - rp);
  q += toward * uMouseInfluence * 0.2;

  for (int j = 0; j < 5; j++) {
    if (j >= uIterations - 1) break;
    vec2 rr = sin(1.5 * (q.yx * uFrequency) + 2.0 * cos(q * uFrequency));
    q += (rr - q) * 0.15;
  }

  vec3 col = vec3(0.0);
  float a = 1.0;

  if (uColorCount > 0) {
    vec2 s = q;
    vec3 sumCol = vec3(0.0);
    float cover = 0.0;
    for (int i = 0; i < MAX_COLORS; ++i) {
      if (i >= uColorCount) break;
      s -= 0.01;
      vec2 r = sin(1.5 * (s.yx * uFrequency) + 2.0 * cos(s * uFrequency));
      float m0 = length(r + sin(5.0 * r.y * uFrequency - 3.0 * t + float(i)) / 4.0);
      float kBelow = clamp(uWarpStrength, 0.0, 1.0);
      float kMix = pow(kBelow, 0.3);
      float gain = 1.0 + max(uWarpStrength - 1.0, 0.0);
      vec2 disp = (r - s) * kBelow;
      vec2 warped = s + disp * gain;
      float m1 = length(warped + sin(5.0 * warped.y * uFrequency - 3.0 * t + float(i)) / 4.0);
      float m = mix(m0, m1, kMix);
      float w = 1.0 - exp(-uBandWidth / exp(uBandWidth * m));
      sumCol += uColors[i] * w;
      cover = max(cover, w);
    }
    col = clamp(sumCol, 0.0, 1.0);
    a = uTransparent > 0 ? cover : 1.0;
  }

  col *= uIntensity;

  if (uNoise > 0.0001) {
    float n = fract(sin(dot(gl_FragCoord.xy + vec2(uTime), vec2(12.9898, 78.233))) * 43758.5453123);
    col += (n - 0.5) * uNoise;
    col = clamp(col, 0.0, 1.0);
  }

  // Corner masks with gentle organic drift
  vec2 topDrift = vec2(sin(t * 0.23) * 0.035, cos(t * 0.17) * 0.028);
  vec2 bottomDrift = vec2(cos(t * 0.19) * 0.032, sin(t * 0.14) * 0.036);

  float maskTopLeft = softEllipse(vUv, vec2(0.12, 0.18) + topDrift, vec2(0.52, 0.48));
  float maskBottomRight = softEllipse(vUv, vec2(0.88, 0.82) + bottomDrift, vec2(0.52, 0.48));
  float cornerMask = max(maskTopLeft, maskBottomRight);

  // Center text protection
  vec2 centerDelta = (vUv - vec2(0.5)) / vec2(0.34, 0.40);
  float centerMask = exp(-dot(centerDelta, centerDelta));
  float textProtection = 1.0 - centerMask * 0.24;

  col *= cornerMask * textProtection;
  a *= cornerMask * textProtection;

  vec3 rgb = (uTransparent > 0) ? col * a : col;
  gl_FragColor = vec4(rgb, a);
}
`;

const vert = `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position, 1.0);
}
`;

function softEllipseJS(nx, ny, centerX, centerY, radiusX, radiusY) {
  const dx = (nx - centerX) / radiusX;
  const dy = (ny - centerY) / radiusY;
  const dist = dx * dx + dy * dy;
  if (dist >= 1.25) return 0;
  if (dist <= 0.55) return 1;
  const t = (dist - 0.55) / (1.25 - 0.55);
  return 1.0 - (t * t * (3 - 2 * t));
}

export function sampleColorBendsInfluence(nx, ny, timeSec, pointer = { x: 0, y: 0 }) {
  const t = timeSec * 0.18;
  const topDriftX = Math.sin(t * 0.23) * 0.035;
  const topDriftY = Math.cos(t * 0.17) * 0.028;
  const bottomDriftX = Math.cos(t * 0.19) * 0.032;
  const bottomDriftY = Math.sin(t * 0.14) * 0.036;

  const topMask = softEllipseJS(nx, ny, 0.12 + topDriftX, 0.18 + topDriftY, 0.52, 0.48);
  const bottomMask = softEllipseJS(nx, ny, 0.88 + bottomDriftX, 0.82 + bottomDriftY, 0.52, 0.48);

  const wave = 0.5 + 0.5 * Math.sin(nx * 8 + Math.cos(ny * 6) + timeSec * 0.6 + pointer.x * 0.5);
  const cornerMask = Math.max(topMask, bottomMask);

  const cdx = (nx - 0.5) / 0.34;
  const cdy = (ny - 0.5) / 0.40;
  const centerMask = Math.exp(-(cdx * cdx + cdy * cdy));
  const textProtection = 1.0 - centerMask * 0.24;

  return Math.min(1, cornerMask * (0.30 + wave * 0.70) * textProtection);
}

export function initHeroColorBends(customOptions = {}) {
  const hero = document.querySelector(".sr-hero");
  if (!hero) return null;

  const directCanvas = hero.querySelector("#sr-hero-color-bends");
  const container = hero.querySelector(".sr-hero-bends-container") || directCanvas;
  if (!container) return null;
  if (container.dataset.initialized === "true") return null;
  container.dataset.initialized = "true";

  const existingCanvas = container instanceof HTMLCanvasElement ? container : container.querySelector("canvas");

  // Social R Chromatic Palette: Electric Blue + Indigo + Violet
  const options = {
    rotation: 90,
    speed: 0.18,
    colors: [
      "#0a1033", // Deep Midnight Blue
      "#1e1b4b", // Deep Indigo
      "#2563eb", // Social R Electric Blue
      "#4f46e5", // Electric Indigo
      "#7c3aed", // Vibrant Royal Violet
      "#9333ea"  // Luminous Purple
    ],
    transparent: true,
    autoRotate: 0,
    scale: 1,
    frequency: 1,
    warpStrength: 1,
    mouseInfluence: 0.55,
    parallax: 1.1,
    noise: 0.06,
    iterations: 1,
    intensity: 1.20,
    bandWidth: 6,
    useExternalLoop: false,
    ...customOptions
  };

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const geometry = new THREE.PlaneGeometry(2, 2);
  const uColorsArray = Array.from({ length: MAX_COLORS }, () => new THREE.Vector3(0, 0, 0));

  const material = new THREE.ShaderMaterial({
    vertexShader: vert,
    fragmentShader: frag,
    uniforms: {
      uCanvas: { value: new THREE.Vector2(1, 1) },
      uTime: { value: 0 },
      uSpeed: { value: options.speed },
      uRot: { value: new THREE.Vector2(1, 0) },
      uColorCount: { value: 0 },
      uColors: { value: uColorsArray },
      uTransparent: { value: options.transparent ? 1 : 0 },
      uScale: { value: options.scale },
      uFrequency: { value: options.frequency },
      uWarpStrength: { value: options.warpStrength },
      uPointer: { value: new THREE.Vector2(0, 0) },
      uMouseInfluence: { value: options.mouseInfluence },
      uParallax: { value: options.parallax },
      uNoise: { value: options.noise },
      uIterations: { value: options.iterations },
      uIntensity: { value: options.intensity },
      uBandWidth: { value: options.bandWidth }
    },
    premultipliedAlpha: true,
    transparent: true
  });

  const toVec3 = (hex) => {
    const h = hex.replace('#', '').trim();
    const v = h.length === 3
      ? [parseInt(h[0] + h[0], 16), parseInt(h[1] + h[1], 16), parseInt(h[2] + h[2], 16)]
      : [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    return new THREE.Vector3(v[0] / 255, v[1] / 255, v[2] / 255);
  };

  const arr = (options.colors || []).filter(Boolean).slice(0, MAX_COLORS).map(toVec3);
  for (let i = 0; i < MAX_COLORS; i++) {
    const vec = material.uniforms.uColors.value[i];
    if (i < arr.length) vec.copy(arr[i]);
    else vec.set(0, 0, 0);
  }
  material.uniforms.uColorCount.value = arr.length;

  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas: existingCanvas || undefined,
      antialias: false,
      powerPreference: "high-performance",
      alpha: true
    });
  } catch (err) {
    console.warn("[Social R] WebGL not available. Applying CSS fallback.", err);
    container.classList.add("no-webgl");
    return {
      destroy: () => {},
      resize: () => {},
      setPointer: () => {},
      sampleInfluence: (nx, ny, timeSec) => sampleColorBendsInfluence(nx, ny, timeSec)
    };
  }

  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
  renderer.setClearColor(0x000000, options.transparent ? 0 : 1);

  if (!existingCanvas) {
    renderer.domElement.style.width = "100%";
    renderer.domElement.style.height = "100%";
    renderer.domElement.style.display = "block";
    container.appendChild(renderer.domElement);
  }

  const clock = new THREE.Clock();
  const pointerTarget = new THREE.Vector2(0, 0);
  const pointerCurrent = new THREE.Vector2(0, 0);
  const pointerSmooth = 8;
  let animationFrameId = null;
  let isDestroyed = false;
  let resizeRaf = null;
  let width = 0;
  let height = 0;
  let pageLeft = 0;
  let pageTop = 0;
  let lastRenderTime = null;

  const resize = () => {
    if (isDestroyed || !renderer) return;
    const rect = container.getBoundingClientRect();
    const nextWidth = Math.max(1, Math.round(rect.width || container.clientWidth || 1));
    const nextHeight = Math.max(1, Math.round(rect.height || container.clientHeight || 1));
    pageLeft = rect.left + window.scrollX;
    pageTop = rect.top + window.scrollY;

    if (Math.abs(nextWidth - width) < 1 && Math.abs(nextHeight - height) < 1) return;

    width = nextWidth;
    height = nextHeight;
    renderer.setSize(width, height, false);
    material.uniforms.uCanvas.value.set(width, height);
  };

  const scheduleResize = () => {
    if (resizeRaf !== null) return;
    resizeRaf = requestAnimationFrame(() => {
      resizeRaf = null;
      resize();
    });
  };

  resize();

  let resizeObserver = null;
  if ("ResizeObserver" in window) {
    resizeObserver = new ResizeObserver(() => scheduleResize());
    resizeObserver.observe(container);
  } else {
    window.addEventListener("resize", resize);
  }

  const handlePointerMove = (e) => {
    const x = ((e.pageX - pageLeft) / (width || 1)) * 2 - 1;
    const y = -(((e.pageY - pageTop) / (height || 1)) * 2 - 1);
    pointerTarget.set(x, y);
  };
  container.addEventListener("pointermove", handlePointerMove, { passive: true });

  const render = (timeSec) => {
    if (isDestroyed) return;

    if (lastRenderTime === null) {
      lastRenderTime = timeSec;
    }
    const dt = Math.min(Math.max(timeSec - lastRenderTime, 0), 0.05);
    lastRenderTime = timeSec;
    material.uniforms.uTime.value = timeSec;

    const deg = (options.rotation % 360) + options.autoRotate * timeSec;
    const rad = (deg * Math.PI) / 180;
    material.uniforms.uRot.value.set(Math.cos(rad), Math.sin(rad));

    pointerCurrent.lerp(pointerTarget, Math.min(1, dt * pointerSmooth));
    material.uniforms.uPointer.value.copy(pointerCurrent);

    renderer.render(scene, camera);
  };

  const loop = () => {
    if (isDestroyed) return;
    animationFrameId = requestAnimationFrame(loop);

    if (document.hidden) return;

    const dt = clock.getDelta();
    const elapsed = clock.elapsedTime;
    material.uniforms.uTime.value = elapsed;

    const deg = (options.rotation % 360) + options.autoRotate * elapsed;
    const rad = (deg * Math.PI) / 180;
    material.uniforms.uRot.value.set(Math.cos(rad), Math.sin(rad));

    pointerCurrent.lerp(pointerTarget, Math.min(1, dt * pointerSmooth));
    material.uniforms.uPointer.value.copy(pointerCurrent);

    renderer.render(scene, camera);
  };

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!prefersReducedMotion && !options.useExternalLoop) {
    animationFrameId = requestAnimationFrame(loop);
  } else {
    render(prefersReducedMotion ? 2.5 : 0.5);
  }

  const setPointer = (x, y) => {
    pointerTarget.set(x, y);
  };

  const sampleInfluence = (nx, ny, timeSec) => {
    return sampleColorBendsInfluence(nx, ny, timeSec, pointerCurrent);
  };

  const destroy = () => {
    isDestroyed = true;
    if (animationFrameId !== null) cancelAnimationFrame(animationFrameId);
    if (resizeRaf !== null) cancelAnimationFrame(resizeRaf);
    if (resizeObserver) resizeObserver.disconnect();
    else window.removeEventListener("resize", resize);
    container.removeEventListener("pointermove", handlePointerMove);

    geometry.dispose();
    material.dispose();
    renderer.dispose();
    renderer.forceContextLoss();
    if (!existingCanvas && renderer.domElement && renderer.domElement.parentElement === container) {
      container.removeChild(renderer.domElement);
    }
  };

  return {
    destroy,
    resize,
    render,
    setPointer,
    sampleInfluence
  };
}

if (typeof window !== "undefined") {
  window.initHeroColorBends = initHeroColorBends;
  window.sampleColorBendsInfluence = sampleColorBendsInfluence;
}
