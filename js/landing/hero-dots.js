/**
 * Social R - Hero DotField Module (2D Canvas + Cursor Bulge + Glowing SVG Follower)
 * Adapted from Estadística Correlacional Interactiva with Social R's Electric Blue / Indigo / Violet chromatic palette.
 */

export function initHeroDotField(colorBendsInstance, heroMotionState) {
  const hero = document.querySelector(".sr-hero");
  if (!hero) return;

  const container = hero.querySelector(".sr-dot-field-container");
  const canvas = hero.querySelector("#sr-hero-canvas-dots");
  const glowCircle = hero.querySelector("#sr-dot-field-glow-circle");

  if (!container || !canvas) return;
  if (canvas.dataset.initialized === "true") return;
  canvas.dataset.initialized = "true";

  const ctx = canvas.getContext("2d", { alpha: true });
  if (!ctx) return;

  const config = {
    dotRadius: 1.5,
    dotSpacing: 14,
    cursorRadius: 480,
    cursorForce: 0.1,
    bulgeStrength: 45,
    glowRadius: 160
  };

  const state = {
    dots: [],
    width: 0,
    height: 0,
    pageLeft: 0,
    pageTop: 0,
    dpr: 1
  };

  const mouse = {
    x: -9999,
    y: -9999,
    previousX: -9999,
    previousY: -9999,
    speed: 0
  };

  let engagement = 0;
  let glowOpacity = 0;
  let resizeRaf = null;

  function buildDots() {
    state.dots = [];
    const step = config.dotRadius + config.dotSpacing;
    if (step <= 0 || state.width <= 0 || state.height <= 0) return;

    const cols = Math.floor(state.width / step);
    const rows = Math.floor(state.height / step);

    const startX = (state.width - (cols - 1) * step) / 2;
    const startY = (state.height - (rows - 1) * step) / 2;

    for (let row = 0; row < rows; row++) {
      const y = startY + row * step;
      for (let col = 0; col < cols; col++) {
        const x = startX + col * step;
        state.dots.push({
          ax: x,
          ay: y,
          sx: x,
          sy: y,
          light: 0
        });
      }
    }
  }

  function doResize() {
    const rect = container.getBoundingClientRect();
    const nextWidth = Math.max(1, Math.round(rect.width));
    const nextHeight = Math.max(1, Math.round(rect.height));
    const nextDpr = Math.min(window.devicePixelRatio || 1, 2);
    state.pageLeft = rect.left + window.scrollX;
    state.pageTop = rect.top + window.scrollY;

    if (
      Math.abs(nextWidth - state.width) < 1 &&
      Math.abs(nextHeight - state.height) < 1 &&
      Math.abs(nextDpr - state.dpr) < 0.001
    ) {
      return;
    }

    state.width = nextWidth;
    state.height = nextHeight;
    state.dpr = nextDpr;

    canvas.width = Math.round(state.width * state.dpr);
    canvas.height = Math.round(state.height * state.dpr);
    canvas.style.width = `${state.width}px`;
    canvas.style.height = `${state.height}px`;

    ctx.setTransform(state.dpr, 0, 0, state.dpr, 0, 0);

    buildDots();
    if (heroMotionState && heroMotionState.drawDotsFunc) {
      heroMotionState.drawDotsFunc(heroMotionState.timeSec || 0);
    }
  }

  function scheduleResize() {
    if (resizeRaf !== null) return;
    resizeRaf = requestAnimationFrame(() => {
      resizeRaf = null;
      doResize();
      if (heroMotionState && heroMotionState.requestFrame) {
        heroMotionState.requestFrame();
      }
    });
  }

  function onPointerMove(e) {
    mouse.x = e.pageX - state.pageLeft;
    mouse.y = e.pageY - state.pageTop;
    if (heroMotionState && heroMotionState.requestFrame) {
      heroMotionState.requestFrame();
    }
  }

  function onPointerLeave() {
    mouse.x = -9999;
    mouse.y = -9999;
  }

  function updateMouseSpeed() {
    if (mouse.previousX !== -9999 && mouse.x !== -9999) {
      const dx = mouse.x - mouse.previousX;
      const dy = mouse.y - mouse.previousY;
      const dist = Math.sqrt(dx * dx + dy * dy);
      mouse.speed = mouse.speed * 0.8 + dist * 0.2;
    } else {
      mouse.speed = 0;
    }
    mouse.previousX = mouse.x;
    mouse.previousY = mouse.y;
  }

  const drawDots = function(timeSec) {
    updateMouseSpeed();

    const targetEngagement = Math.min(mouse.speed / 5, 1);
    engagement += (targetEngagement - engagement) * 0.06;
    if (engagement < 0.001) engagement = 0;

    glowOpacity += (engagement - glowOpacity) * 0.08;
    if (glowCircle) {
      glowCircle.setAttribute("cx", mouse.x);
      glowCircle.setAttribute("cy", mouse.y);
      glowCircle.style.opacity = glowOpacity.toFixed(3);
    }

    ctx.clearRect(0, 0, state.width, state.height);

    const baseRadius = Math.max(0.68, config.dotRadius * 0.48);
    const cursorRadiusSquared = config.cursorRadius * config.cursorRadius;

    // Social R Chromatic Palette Buckets: Electric Blue -> Indigo -> Violet
    const buckets = [
      { dots: [], color: "rgba(37, 99, 235, 0.20)" },  // Electric Blue low
      { dots: [], color: "rgba(79, 70, 229, 0.35)" },  // Indigo medium
      { dots: [], color: "rgba(124, 58, 237, 0.55)" }, // Violet strong
      { dots: [], color: "rgba(147, 51, 234, 0.75)" }, // Bright Violet
      { dots: [], color: "rgba(192, 132, 252, 0.95)" }  // Luminous Violet Highlight
    ];

    const reduceMotion = heroMotionState ? heroMotionState.reduceMotion : false;

    for (let i = 0; i < state.dots.length; i++) {
      const dot = state.dots[i];
      if (!reduceMotion) {
        const dx = mouse.x - dot.ax;
        const dy = mouse.y - dot.ay;
        const distanceSquared = dx * dx + dy * dy;

        if (distanceSquared < cursorRadiusSquared && engagement > 0.01) {
          const distance = Math.sqrt(distanceSquared);
          const influence = 1 - distance / config.cursorRadius;
          const push = influence * influence * config.bulgeStrength * engagement;
          const angle = Math.atan2(dy, dx);
          const targetX = dot.ax - Math.cos(angle) * push;
          const targetY = dot.ay - Math.sin(angle) * push;

          dot.sx += (targetX - dot.sx) * 0.15;
          dot.sy += (targetY - dot.sy) * 0.15;
        } else {
          dot.sx += (dot.ax - dot.sx) * 0.1;
          dot.sy += (dot.ay - dot.sy) * 0.1;
        }
      } else {
        dot.sx = dot.ax;
        dot.sy = dot.ay;
      }

      // Sample influence from ColorBends WebGL shader
      const nx = dot.ax / state.width;
      const ny = dot.ay / state.height;
      let targetLight = 0;
      if (colorBendsInstance && typeof colorBendsInstance.sampleInfluence === "function") {
        targetLight = colorBendsInstance.sampleInfluence(nx, ny, timeSec);
      }

      dot.light += (targetLight - dot.light) * (targetLight > dot.light ? 0.18 : 0.07);

      const visibility = Math.min(1, 0.12 + dot.light * 0.86);
      const radius = baseRadius * (1.0 + dot.light * 0.48);

      let bucketIdx = 0;
      if (visibility >= 0.80) bucketIdx = 4;
      else if (visibility >= 0.60) bucketIdx = 3;
      else if (visibility >= 0.40) bucketIdx = 2;
      else if (visibility >= 0.22) bucketIdx = 1;
      else bucketIdx = 0;

      dot.currentRadius = radius;
      buckets[bucketIdx].dots.push(dot);
    }

    // High performance drawing per bucket
    for (let b = 0; b < buckets.length; b++) {
      const bucket = buckets[b];
      if (bucket.dots.length === 0) continue;

      ctx.fillStyle = bucket.color;
      ctx.beginPath();
      for (let i = 0; i < bucket.dots.length; i++) {
        const d = bucket.dots[i];
        ctx.moveTo(d.sx + d.currentRadius, d.sy);
        ctx.arc(d.sx, d.sy, d.currentRadius, 0, Math.PI * 2);
      }
      ctx.fill();
    }
  };

  if (heroMotionState) {
    heroMotionState.drawDotsFunc = drawDots;
  }

  const hasFinePointer = window.matchMedia("(pointer: fine)").matches;
  if (hasFinePointer) {
    window.addEventListener("pointermove", onPointerMove, { passive: true });
    container.addEventListener("pointerleave", onPointerLeave, { passive: true });
  }

  const resizeObserver = new ResizeObserver(() => scheduleResize());
  resizeObserver.observe(container);
  doResize();

  return {
    draw: drawDots,
    resize: doResize
  };
}
