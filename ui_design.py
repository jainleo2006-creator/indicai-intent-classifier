"""
ui_design.py — IndicAI Futuristic UI System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cyberpunk / Holographic / JARVIS-style UI layer for the IndicAI
Multilingual Intent Classifier.

Import this ONCE at the top of app.py and call the functions in order:
    from ui_design import *
    load_ui()           # inject CSS + JS (call after st.set_page_config)
    render_particles()  # canvas particle field
    render_3d_background()  # animated mesh / aurora
    render_header()     # cinematic top bar
    render_sidebar()    # animated sidebar chrome
    render_footer()     # status bar

Then wrap your content blocks with:
    render_glass_container(content_html)
    render_result_card(result, INTENT_META)
    render_loading_animation()
    render_hologram_effect(label)

All functions return or inject HTML/CSS/JS via st.markdown(unsafe_allow_html=True).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import streamlit as st

# ══════════════════════════════════════════════════════════════════════════
# COLOUR TOKENS  (single source of truth)
# ══════════════════════════════════════════════════════════════════════════

COLORS = {
    "bg":           "#050816",
    "bg2":          "#0a0f2e",
    "surface":      "rgba(255,255,255,0.04)",
    "surface2":     "rgba(255,255,255,0.08)",
    "border":       "rgba(139,92,246,0.25)",
    "neon_purple":  "#8b5cf6",
    "neon_blue":    "#00f5ff",
    "neon_pink":    "#ff4ecd",
    "neon_green":   "#00ff9f",
    "text":         "#e2e8f0",
    "muted":        "#64748b",
}

# ══════════════════════════════════════════════════════════════════════════
# MASTER CSS
# ══════════════════════════════════════════════════════════════════════════

_MASTER_CSS = """
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

/* ── CSS Variables ────────────────────────────────────────────────────── */
:root {
  --bg:          #050816;
  --bg2:         #0a0f2e;
  --surface:     rgba(255,255,255,0.04);
  --surface2:    rgba(255,255,255,0.08);
  --border:      rgba(139,92,246,0.25);
  --neon-purple: #8b5cf6;
  --neon-blue:   #00f5ff;
  --neon-pink:   #ff4ecd;
  --neon-green:  #00ff9f;
  --text:        #e2e8f0;
  --muted:       #64748b;
  --font-display: 'Orbitron', monospace;
  --font-body:    'Rajdhani', sans-serif;
  --font-mono:    'Share Tech Mono', monospace;
  --glow-purple:  0 0 20px rgba(139,92,246,0.6), 0 0 60px rgba(139,92,246,0.2);
  --glow-blue:    0 0 20px rgba(0,245,255,0.6),  0 0 60px rgba(0,245,255,0.2);
  --glow-pink:    0 0 20px rgba(255,78,205,0.6), 0 0 60px rgba(255,78,205,0.2);
  --transition:   all 0.35s cubic-bezier(0.23,1,0.32,1);
}

/* ── Kill Streamlit chrome ────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
.viewerBadge_container__r5tak { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stStatusWidget { display: none !important; }

/* ── Root background ──────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--font-body) !important;
}

/* ── Scrollbar ────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--neon-purple), var(--neon-blue));
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--neon-pink); }

/* ── Block container ──────────────────────────────────────────────────── */
.block-container {
  padding-top: 1rem !important;
  max-width: 860px !important;
  animation: fadeSlideUp 0.8s ease forwards;
}

/* ── Sidebar ──────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #06091f 0%, #0a0f2e 100%) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 4px 0 40px rgba(139,92,246,0.12) !important;
}
[data-testid="stSidebar"] * {
  font-family: var(--font-body) !important;
  color: var(--text) !important;
}
[data-testid="stSidebar"] h3 {
  font-family: var(--font-display) !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.15em !important;
  color: var(--neon-blue) !important;
  text-transform: uppercase;
}
[data-testid="stSidebar"] .stMarkdown code {
  font-family: var(--font-mono) !important;
  background: rgba(0,245,255,0.07) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  border-radius: 4px !important;
  color: var(--neon-blue) !important;
  font-size: 0.78rem !important;
}

/* ── Inputs ───────────────────────────────────────────────────────────── */
.stTextArea textarea, .stSelectbox select,
[data-testid="stTextArea"] textarea {
  background: rgba(10,15,46,0.9) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  font-family: var(--font-body) !important;
  font-size: 1rem !important;
  transition: var(--transition) !important;
  box-shadow: inset 0 2px 12px rgba(0,0,0,0.4) !important;
  caret-color: var(--neon-blue);
}
.stTextArea textarea:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--neon-purple) !important;
  box-shadow:
    inset 0 2px 12px rgba(0,0,0,0.4),
    0 0 0 2px rgba(139,92,246,0.25),
    var(--glow-purple) !important;
  outline: none !important;
}

/* ── Selectbox ────────────────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
  background: rgba(10,15,46,0.9) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  transition: var(--transition) !important;
}
[data-testid="stSelectbox"] > div > div:hover {
  border-color: var(--neon-blue) !important;
  box-shadow: var(--glow-blue) !important;
}

/* ── Buttons ──────────────────────────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, rgba(139,92,246,0.25), rgba(0,245,255,0.15)) !important;
  border: 1px solid rgba(139,92,246,0.5) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  font-family: var(--font-display) !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  padding: 0.55rem 1.4rem !important;
  transition: var(--transition) !important;
  position: relative;
  overflow: hidden;
}
.stButton > button::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
  transition: left 0.5s ease;
}
.stButton > button:hover::before { left: 100%; }
.stButton > button:hover {
  border-color: var(--neon-purple) !important;
  box-shadow: var(--glow-purple), 0 8px 32px rgba(0,0,0,0.5) !important;
  transform: translateY(-2px) scale(1.02) !important;
  color: #fff !important;
}
.stButton > button:active {
  transform: translateY(1px) scale(0.98) !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.4) !important;
}
/* Primary button accent */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, rgba(139,92,246,0.6), rgba(0,245,255,0.3)) !important;
  border-color: var(--neon-purple) !important;
  color: #fff !important;
  font-weight: 700 !important;
}
.stButton > button[kind="primary"]:hover {
  background: linear-gradient(135deg, var(--neon-purple), var(--neon-blue)) !important;
  box-shadow: var(--glow-purple), 0 12px 40px rgba(0,0,0,0.6) !important;
}

/* ── Expander ─────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(12px) !important;
}
[data-testid="stExpander"] summary {
  color: var(--neon-blue) !important;
  font-family: var(--font-display) !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.08em !important;
}

/* ── Progress bars ────────────────────────────────────────────────────── */
[data-testid="stProgress"] > div > div {
  background: linear-gradient(90deg, var(--neon-purple), var(--neon-blue)) !important;
  border-radius: 100px !important;
  box-shadow: var(--glow-blue) !important;
  animation: pulseGlow 2s ease-in-out infinite !important;
}
[data-testid="stProgress"] > div {
  background: rgba(139,92,246,0.1) !important;
  border-radius: 100px !important;
}

/* ── Alert / error / warning ──────────────────────────────────────────── */
[data-testid="stAlert"] {
  background: rgba(10,15,46,0.85) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(8px) !important;
  border-left-width: 3px !important;
}
.stAlert[data-baseweb="notification"] {
  font-family: var(--font-body) !important;
}

/* ── Section labels ───────────────────────────────────────────────────── */
.stMarkdown h3 {
  font-family: var(--font-display) !important;
  font-size: 0.82rem !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  color: var(--neon-blue) !important;
  margin-bottom: 0.6rem !important;
}

/* ── Spinner ──────────────────────────────────────────────────────────── */
[data-testid="stSpinner"] {
  color: var(--neon-purple) !important;
}

/* ══ KEYFRAME ANIMATIONS ══════════════════════════════════════════════════ */
@keyframes fadeSlideUp {
  from { opacity:0; transform:translateY(24px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes pulseGlow {
  0%,100% { opacity:1; }
  50%      { opacity:0.7; }
}
@keyframes neonPulse {
  0%,100% { text-shadow: 0 0 8px currentColor, 0 0 20px currentColor; }
  50%      { text-shadow: 0 0 16px currentColor, 0 0 40px currentColor, 0 0 80px currentColor; }
}
@keyframes borderRun {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes float {
  0%,100% { transform: translateY(0px); }
  50%      { transform: translateY(-8px); }
}
@keyframes scanLine {
  0%   { top: -4px; opacity:0; }
  10%  { opacity:0.4; }
  90%  { opacity:0.4; }
  100% { top: 100%; opacity:0; }
}
@keyframes rotateOrb {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position:  200% center; }
}
@keyframes flicker {
  0%,19%,21%,23%,25%,54%,56%,100% { opacity:1; }
  20%,22%,24%,55%                  { opacity:0.4; }
}
@keyframes auroraShift {
  0%   { transform: translate(-5%,-5%) rotate(0deg)   scale(1); }
  33%  { transform: translate(5%,10%)  rotate(120deg) scale(1.1); }
  66%  { transform: translate(-8%,5%)  rotate(240deg) scale(0.95); }
  100% { transform: translate(-5%,-5%) rotate(360deg) scale(1); }
}
@keyframes matrixFall {
  0%   { transform: translateY(-100%); opacity:1; }
  100% { transform: translateY(100vh);  opacity:0; }
}
@keyframes glassReveal {
  from { opacity:0; transform:perspective(800px) rotateX(8deg) translateY(20px); }
  to   { opacity:1; transform:perspective(800px) rotateX(0deg) translateY(0); }
}
@keyframes breathe {
  0%,100% { box-shadow: 0 0 20px rgba(139,92,246,0.3); }
  50%      { box-shadow: 0 0 50px rgba(139,92,246,0.7), 0 0 100px rgba(0,245,255,0.2); }
}
@keyframes slideInLeft {
  from { opacity:0; transform:translateX(-30px); }
  to   { opacity:1; transform:translateX(0); }
}
@keyframes pulseRing {
  0%   { transform:scale(0.8); opacity:1; }
  100% { transform:scale(2.4); opacity:0; }
}
@keyframes typewriter {
  from { width:0; }
  to   { width:100%; }
}
@keyframes cursorBlink {
  0%,100% { border-right-color: var(--neon-blue); }
  50%      { border-right-color: transparent; }
}

/* ── Glass card utility ───────────────────────────────────────────────── */
.glass-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(139,92,246,0.2);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0,0,0,0.4),
    inset 0 1px 0 rgba(255,255,255,0.06);
  position: relative;
  overflow: hidden;
  animation: glassReveal 0.6s cubic-bezier(0.23,1,0.32,1) forwards;
}
.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139,92,246,0.5), rgba(0,245,255,0.5), transparent);
  animation: shimmer 3s ease infinite;
  background-size: 200%;
}
.glass-card:hover {
  border-color: rgba(139,92,246,0.45);
  box-shadow:
    0 12px 48px rgba(0,0,0,0.5),
    0 0 40px rgba(139,92,246,0.15),
    inset 0 1px 0 rgba(255,255,255,0.1);
  transform: perspective(1000px) translateZ(4px);
  transition: var(--transition);
}

/* ── Neon text ────────────────────────────────────────────────────────── */
.neon-text {
  font-family: var(--font-display);
  color: var(--neon-blue);
  animation: neonPulse 3s ease-in-out infinite;
}
.neon-pink  { color: var(--neon-pink);   animation: neonPulse 2.5s ease-in-out infinite; }
.neon-green { color: var(--neon-green);  animation: neonPulse 2s ease-in-out infinite; }

/* ── Hologram overlay ─────────────────────────────────────────────────── */
.hologram-overlay {
  position: relative;
  overflow: hidden;
}
.hologram-overlay::after {
  content: '';
  position: absolute;
  top: -4px; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
  animation: scanLine 3s ease-in-out infinite;
  pointer-events: none;
}

/* ── Animated border card ─────────────────────────────────────────────── */
.border-run-card {
  position: relative;
  border-radius: 14px;
  padding: 2px;
  background: linear-gradient(270deg, var(--neon-purple), var(--neon-blue), var(--neon-pink), var(--neon-purple));
  background-size: 600% 600%;
  animation: borderRun 6s ease infinite;
}
.border-run-inner {
  background: var(--bg2);
  border-radius: 12px;
  padding: 20px 24px;
}

/* ── Confidence bar ───────────────────────────────────────────────────── */
.conf-bar-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 6px 0;
}
.conf-bar-label {
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--muted);
  min-width: 160px;
}
.conf-bar-track {
  flex: 1;
  height: 6px;
  background: rgba(255,255,255,0.06);
  border-radius: 100px;
  overflow: hidden;
}
.conf-bar-fill {
  height: 100%;
  border-radius: 100px;
  background: linear-gradient(90deg, var(--neon-purple), var(--neon-blue));
  box-shadow: 0 0 8px rgba(0,245,255,0.5);
  transform-origin: left;
  animation: barGrow 0.8s cubic-bezier(0.23,1,0.32,1) forwards;
}
@keyframes barGrow {
  from { width: 0 !important; }
}
.conf-bar-val {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--neon-blue);
  min-width: 44px;
  text-align: right;
}

/* ── AI ORB ───────────────────────────────────────────────────────────── */
.ai-orb {
  display: inline-block;
  width: 40px; height: 40px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, var(--neon-blue), var(--neon-purple), #050816);
  box-shadow: 0 0 20px var(--neon-purple), 0 0 40px rgba(0,245,255,0.3);
  animation: float 3s ease-in-out infinite, rotateOrb 8s linear infinite;
  position: relative;
  flex-shrink: 0;
}
.ai-orb::after {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  border: 1.5px solid transparent;
  background: linear-gradient(var(--bg), var(--bg)) padding-box,
              linear-gradient(90deg, var(--neon-purple), var(--neon-blue)) border-box;
  animation: rotateOrb 4s linear infinite reverse;
}

/* ── Pulse ring ───────────────────────────────────────────────────────── */
.pulse-ring {
  position: absolute;
  border-radius: 50%;
  border: 2px solid var(--neon-purple);
  animation: pulseRing 2s ease-out infinite;
}

/* ── Flicker text ─────────────────────────────────────────────────────── */
.flicker { animation: flicker 4s infinite; }

/* ── Floating shape ───────────────────────────────────────────────────── */
.float-shape {
  position: fixed;
  border-radius: 4px;
  animation: float 4s ease-in-out infinite;
  pointer-events: none;
  z-index: 0;
}
</style>
"""

# ══════════════════════════════════════════════════════════════════════════
# JAVASCRIPT INTERACTIONS
# ══════════════════════════════════════════════════════════════════════════

_MASTER_JS = """
<script>
(function() {
  // ── 3D mouse-tilt on .glass-card elements ────────────────────────────
  function initTilt() {
    document.querySelectorAll('.glass-card, .border-run-card').forEach(card => {
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width  - 0.5;
        const y = (e.clientY - r.top)  / r.height - 0.5;
        card.style.transform =
          `perspective(900px) rotateY(${x*10}deg) rotateX(${-y*8}deg) translateZ(8px)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(900px) rotateY(0) rotateX(0) translateZ(0)';
        card.style.transition = 'transform 0.6s cubic-bezier(0.23,1,0.32,1)';
      });
    });
  }

  // ── Cursor glow ──────────────────────────────────────────────────────
  function initCursorGlow() {
    const dot = document.createElement('div');
    Object.assign(dot.style, {
      position:'fixed', width:'14px', height:'14px',
      borderRadius:'50%', pointerEvents:'none', zIndex:'99999',
      background:'radial-gradient(circle, rgba(139,92,246,0.9) 0%, transparent 70%)',
      boxShadow:'0 0 20px rgba(139,92,246,0.8)',
      transform:'translate(-50%,-50%)',
      transition:'opacity 0.2s ease',
    });
    document.body.appendChild(dot);

    const ring = document.createElement('div');
    Object.assign(ring.style, {
      position:'fixed', width:'36px', height:'36px',
      borderRadius:'50%', pointerEvents:'none', zIndex:'99998',
      border:'1px solid rgba(0,245,255,0.5)',
      transform:'translate(-50%,-50%)',
      transition:'all 0.12s ease',
    });
    document.body.appendChild(ring);

    let mx=0, my=0;
    document.addEventListener('mousemove', e => {
      mx=e.clientX; my=e.clientY;
      dot.style.left  = mx+'px';
      dot.style.top   = my+'px';
      ring.style.left = mx+'px';
      ring.style.top  = my+'px';
    });
    document.addEventListener('mousedown', () => {
      dot.style.transform  = 'translate(-50%,-50%) scale(1.5)';
      ring.style.transform = 'translate(-50%,-50%) scale(0.8)';
    });
    document.addEventListener('mouseup', () => {
      dot.style.transform  = 'translate(-50%,-50%) scale(1)';
      ring.style.transform = 'translate(-50%,-50%) scale(1)';
    });
  }

  // ── Scan-line on hover for .hologram-overlay ─────────────────────────
  function initScanHover() {
    document.querySelectorAll('.hologram-overlay').forEach(el => {
      el.addEventListener('mouseenter', () => el.style.setProperty('--scan-speed','1.5s'));
      el.addEventListener('mouseleave', () => el.style.setProperty('--scan-speed','3s'));
    });
  }

  // ── Retry until DOM has the elements ─────────────────────────────────
  function tryInit(attempts) {
    if (attempts <= 0) return;
    const cards = document.querySelectorAll('.glass-card');
    if (cards.length > 0) {
      initTilt();
      initScanHover();
    } else {
      setTimeout(() => tryInit(attempts-1), 400);
    }
  }

  // run once on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { initCursorGlow(); tryInit(15); });
  } else {
    initCursorGlow();
    tryInit(15);
  }

  // re-run after Streamlit re-renders
  const obs = new MutationObserver(() => tryInit(3));
  obs.observe(document.body, { childList:true, subtree:true });
})();
</script>
"""

# ══════════════════════════════════════════════════════════════════════════
# CANVAS PARTICLE SYSTEM
# ══════════════════════════════════════════════════════════════════════════

_PARTICLES_HTML = """
<canvas id="indic-particles" style="
  position:fixed; top:0; left:0;
  width:100vw; height:100vh;
  pointer-events:none; z-index:0;
  opacity:0.55;
"></canvas>
<script>
(function(){
  const canvas = document.getElementById('indic-particles');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W = canvas.width  = window.innerWidth;
  let H = canvas.height = window.innerHeight;
  window.addEventListener('resize', () => {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  });

  const COLORS = ['#8b5cf6','#00f5ff','#ff4ecd','#00ff9f'];
  const N = 90;
  const pts = Array.from({length:N}, () => ({
    x: Math.random()*W, y: Math.random()*H,
    vx:(Math.random()-0.5)*0.4, vy:(Math.random()-0.5)*0.4,
    r: Math.random()*1.8+0.4,
    c: COLORS[Math.floor(Math.random()*COLORS.length)],
    alpha: Math.random()*0.6+0.2,
  }));

  let mouseX=-9999, mouseY=-9999;
  window.addEventListener('mousemove', e => { mouseX=e.clientX; mouseY=e.clientY; });

  function draw(){
    ctx.clearRect(0,0,W,H);
    // connect nearby dots
    for(let i=0;i<N;i++){
      for(let j=i+1;j<N;j++){
        const dx=pts[i].x-pts[j].x, dy=pts[i].y-pts[j].y;
        const d=Math.sqrt(dx*dx+dy*dy);
        if(d<120){
          ctx.beginPath();
          ctx.moveTo(pts[i].x,pts[i].y);
          ctx.lineTo(pts[j].x,pts[j].y);
          ctx.strokeStyle=`rgba(139,92,246,${0.12*(1-d/120)})`;
          ctx.lineWidth=0.6;
          ctx.stroke();
        }
      }
    }
    // draw particles
    pts.forEach(p => {
      // mouse repel
      const dx=p.x-mouseX, dy=p.y-mouseY;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<100){ p.vx+=dx/d*0.08; p.vy+=dy/d*0.08; }
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>W) p.vx*=-1;
      if(p.y<0||p.y>H) p.vy*=-1;
      // glow dot
      const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*5);
      g.addColorStop(0,p.c);
      g.addColorStop(1,'transparent');
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r*5,0,Math.PI*2);
      ctx.fillStyle=g;
      ctx.globalAlpha=p.alpha*0.2;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=p.c;
      ctx.globalAlpha=p.alpha;
      ctx.fill();
      ctx.globalAlpha=1;
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
"""

# ══════════════════════════════════════════════════════════════════════════
# AURORA / 3-D BACKGROUND
# ══════════════════════════════════════════════════════════════════════════

_BG_HTML = """
<div id="indic-bg" style="
  position:fixed; inset:0; z-index:0;
  overflow:hidden; pointer-events:none;
  background: #050816;
">
  <!-- aurora blobs -->
  <div style="
    position:absolute; width:70vw; height:70vw;
    border-radius:50%;
    background: radial-gradient(ellipse, rgba(139,92,246,0.18) 0%, transparent 70%);
    top:-20%; left:-20%;
    animation: auroraShift 14s ease-in-out infinite;
  "></div>
  <div style="
    position:absolute; width:60vw; height:60vw;
    border-radius:50%;
    background: radial-gradient(ellipse, rgba(0,245,255,0.12) 0%, transparent 70%);
    bottom:-10%; right:-10%;
    animation: auroraShift 18s ease-in-out infinite reverse;
  "></div>
  <div style="
    position:absolute; width:40vw; height:40vw;
    border-radius:50%;
    background: radial-gradient(ellipse, rgba(255,78,205,0.10) 0%, transparent 70%);
    top:30%; left:50%;
    animation: auroraShift 22s ease-in-out infinite 6s;
  "></div>
  <!-- grid overlay -->
  <div style="
    position:absolute; inset:0;
    background-image:
      linear-gradient(rgba(139,92,246,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(139,92,246,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 40%, transparent 100%);
  "></div>
  <!-- floating cubes -->
  <div class="float-shape" style="
    width:14px;height:14px;top:18%;left:8%;
    border:1px solid rgba(139,92,246,0.4);
    animation-delay:-1s;animation-duration:5s;
  "></div>
  <div class="float-shape" style="
    width:8px;height:8px;top:60%;left:85%;
    border:1px solid rgba(0,245,255,0.4);
    animation-delay:-3s;animation-duration:6s;
    transform:rotate(45deg);
  "></div>
  <div class="float-shape" style="
    width:10px;height:10px;top:80%;left:20%;
    border:1px solid rgba(255,78,205,0.4);
    animation-delay:-2s;animation-duration:7s;
  "></div>
</div>
"""

# ══════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════

_HEADER_HTML = """
<div class="glass-card hologram-overlay" style="
  margin-bottom: 2rem;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  gap: 20px;
  animation: slideInLeft 0.7s cubic-bezier(0.23,1,0.32,1) forwards;
">
  <!-- orb -->
  <div style="position:relative; width:50px; height:50px; flex-shrink:0;">
    <div class="ai-orb" style="width:50px;height:50px;"></div>
    <div class="pulse-ring" style="width:50px;height:50px;top:0;left:0;"></div>
    <div class="pulse-ring" style="width:50px;height:50px;top:0;left:0;animation-delay:0.7s;"></div>
  </div>
  <!-- title block -->
  <div style="flex:1;">
    <div style="
      font-family: 'Orbitron', monospace;
      font-size: clamp(1.1rem, 3vw, 1.7rem);
      font-weight: 900;
      letter-spacing: 0.12em;
      background: linear-gradient(90deg, #8b5cf6, #00f5ff, #ff4ecd);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      background-size: 200%;
      animation: shimmer 4s linear infinite;
    ">INDICAI NEURAL INTERFACE</div>
    <div style="
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.72rem;
      color: rgba(0,245,255,0.6);
      letter-spacing: 0.22em;
      margin-top: 4px;
    ">MULTILINGUAL · INTENT · CLASSIFIER · v1.0</div>
  </div>
  <!-- status badge -->
  <div style="
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    color: #00ff9f;
    border: 1px solid rgba(0,255,159,0.3);
    border-radius: 20px;
    padding: 5px 14px;
    background: rgba(0,255,159,0.06);
    animation: breathe 3s ease-in-out infinite;
    white-space: nowrap;
  ">● ONLINE</div>
</div>
"""

# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR CHROME (injected into st.sidebar)
# ══════════════════════════════════════════════════════════════════════════

_SIDEBAR_CHROME_HTML = """
<div style="
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  color: rgba(0,245,255,0.45);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(139,92,246,0.15);
">
  SYS.ID ▸ IND-AI-001<br>
  BUILD  ▸ 2024.12.REL<br>
  STATUS ▸ <span style="color:#00ff9f;">NOMINAL</span>
</div>
"""

# ══════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════

_FOOTER_HTML = """
<div style="
  margin-top: 3rem;
  padding: 14px 24px;
  border-top: 1px solid rgba(139,92,246,0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.62rem;
  color: rgba(100,116,139,0.7);
  letter-spacing: 0.1em;
">
  <span>INDICAI · COLLEGE PROJECT · v1.0</span>
  <span style="color:rgba(0,245,255,0.4);">NEURAL ENGINE ACTIVE ●</span>
</div>
"""

# ══════════════════════════════════════════════════════════════════════════
# LOADING ANIMATION
# ══════════════════════════════════════════════════════════════════════════

_LOADING_HTML = """
<div id="indic-loader" style="
  display:flex; flex-direction:column;
  align-items:center; gap:16px;
  padding: 32px 0;
">
  <div style="position:relative; width:64px; height:64px;">
    <div style="
      position:absolute; inset:0;
      border-radius:50%;
      border: 2px solid transparent;
      border-top-color: #8b5cf6;
      border-right-color: #00f5ff;
      animation: rotateOrb 1s linear infinite;
    "></div>
    <div style="
      position:absolute; inset:8px;
      border-radius:50%;
      border: 2px solid transparent;
      border-bottom-color: #ff4ecd;
      animation: rotateOrb 0.7s linear infinite reverse;
    "></div>
    <div style="
      position:absolute; inset:18px;
      border-radius:50%;
      background: radial-gradient(circle, #8b5cf6, #050816);
      animation: pulseGlow 1.2s ease-in-out infinite;
    "></div>
  </div>
  <div style="
    font-family:'Orbitron',monospace;
    font-size:0.7rem;
    letter-spacing:0.2em;
    color:rgba(0,245,255,0.7);
    animation:neonPulse 1.5s ease-in-out infinite;
  ">CLASSIFYING…</div>
</div>
"""

# ══════════════════════════════════════════════════════════════════════════
# HOLOGRAM LABEL
# ══════════════════════════════════════════════════════════════════════════

def _hologram_html(label: str) -> str:
    return f"""
<div class="hologram-overlay" style="
  font-family:'Orbitron',monospace;
  font-size:0.68rem;
  letter-spacing:0.2em;
  color:rgba(0,245,255,0.6);
  text-transform:uppercase;
  margin-bottom:8px;
  animation:flicker 5s infinite;
">{label}</div>
"""

# ══════════════════════════════════════════════════════════════════════════
# RESULT CARD
# ══════════════════════════════════════════════════════════════════════════

def _build_result_card_html(result: dict, intent_meta: dict) -> str:
    status = result.get("status")

    if status == "invalid":
        return f"""
<div class="glass-card hologram-overlay" style="padding:24px 28px;border-left:3px solid #ff4ecd;">
  <div style="font-size:1.6rem;margin-bottom:6px;">⚠️</div>
  <div style="font-family:'Orbitron',monospace;font-size:1rem;font-weight:700;color:#ff4ecd;
              animation:neonPulse 2s ease-in-out infinite;">INVALID INPUT</div>
  <div style="font-family:'Rajdhani',sans-serif;font-size:0.88rem;color:#64748b;margin-top:6px;">
    Symbols · numbers · gibberish — cannot be classified.
  </div>
</div>"""

    if status == "low_confidence":
        conf = result.get("confidence", 0)
        all_probs = result.get("all_probs", {})
        bars = _build_conf_bars(all_probs, intent_meta)
        return f"""
<div class="glass-card hologram-overlay" style="padding:24px 28px;border-left:3px solid #ffd93d;">
  <div style="font-size:1.6rem;margin-bottom:6px;">🤔</div>
  <div style="font-family:'Orbitron',monospace;font-size:0.95rem;font-weight:700;color:#ffd93d;
              animation:neonPulse 2s ease-in-out infinite;">LOW CONFIDENCE SIGNAL</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.78rem;color:#64748b;margin-top:4px;">
    BEST CONFIDENCE: {conf:.1%} — BELOW THRESHOLD
  </div>
  <div style="margin-top:20px;">{bars}</div>
</div>"""

    # ── Valid intent ────────────────────────────────────────────────────
    intent   = result.get("intent", "unknown_intent")
    meta     = intent_meta.get(intent, {"icon":"🔵","color":"#8b5cf6","label":intent})
    conf     = result.get("confidence", 0)
    all_probs = result.get("all_probs", {})
    icon, color, label = meta["icon"], meta["color"], meta["label"]
    bars = _build_conf_bars(all_probs, intent_meta)

    # confidence percentage visual
    pct = int(conf * 100)

    return f"""
<div class="border-run-card" style="margin-bottom:16px;animation:glassReveal 0.6s ease forwards;">
  <div class="border-run-inner hologram-overlay">
    <div style="display:flex;align-items:flex-start;gap:20px;margin-bottom:20px;">
      <!-- icon orb -->
      <div style="
        width:56px;height:56px;border-radius:50%;flex-shrink:0;
        background:radial-gradient(circle at 35% 35%, {color}66, {color}11);
        border:2px solid {color}88;
        display:flex;align-items:center;justify-content:center;
        font-size:1.6rem;
        box-shadow:0 0 20px {color}55;
        animation:float 3s ease-in-out infinite;
      ">{icon}</div>
      <!-- info -->
      <div style="flex:1;">
        <div style="
          font-family:'Orbitron',monospace;
          font-size:1.2rem;font-weight:800;
          color:{color};
          animation:neonPulse 3s ease-in-out infinite;
          text-shadow:0 0 20px {color};
        ">{label.upper()}</div>
        <div style="
          font-family:'Share Tech Mono',monospace;
          font-size:0.7rem;color:rgba(100,116,139,0.8);
          letter-spacing:0.15em;margin-top:4px;
        ">INTENT DETECTED · CONFIDENCE: {conf:.1%}</div>
        <!-- confidence ring -->
        <div style="margin-top:12px;display:flex;align-items:center;gap:12px;">
          <div style="position:relative;width:52px;height:52px;">
            <svg viewBox="0 0 52 52" style="transform:rotate(-90deg);width:52px;height:52px;">
              <circle cx="26" cy="26" r="22" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="4"/>
              <circle cx="26" cy="26" r="22" fill="none"
                stroke="{color}" stroke-width="4"
                stroke-dasharray="{int(pct*1.382)} 138.2"
                stroke-linecap="round"
                style="filter:drop-shadow(0 0 6px {color})"/>
            </svg>
            <div style="
              position:absolute;inset:0;
              display:flex;align-items:center;justify-content:center;
              font-family:'Orbitron',monospace;font-size:0.62rem;font-weight:700;
              color:{color};
            ">{pct}%</div>
          </div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:0.82rem;color:#64748b;">
            Signal strength: <span style="color:{color};">
            {'STRONG' if conf>0.85 else 'MODERATE' if conf>0.65 else 'WEAK'}</span>
          </div>
        </div>
      </div>
    </div>
    <!-- probability bars -->
    <div style="border-top:1px solid rgba(139,92,246,0.12);padding-top:16px;">
      <div style="font-family:'Orbitron',monospace;font-size:0.62rem;letter-spacing:0.18em;
                  color:rgba(0,245,255,0.4);margin-bottom:12px;">ALL INTENT SIGNALS</div>
      {bars}
    </div>
  </div>
</div>"""


def _build_conf_bars(all_probs: dict, intent_meta: dict) -> str:
    if not all_probs:
        return ""
    sorted_probs = sorted(all_probs.items(), key=lambda x: -x[1])
    bars_html = ""
    for intent, prob in sorted_probs:
        meta  = intent_meta.get(intent, {"icon":"🔵","color":"#8b5cf6","label":intent})
        color = meta["color"]
        label = f"{meta['icon']} {meta['label']}"
        width = int(prob * 100)
        bars_html += f"""
<div class="conf-bar-wrap">
  <div class="conf-bar-label">{label}</div>
  <div class="conf-bar-track">
    <div class="conf-bar-fill" style="width:{width}%;
      background:linear-gradient(90deg, {color}88, {color});
      box-shadow:0 0 8px {color}66;">
    </div>
  </div>
  <div class="conf-bar-val">{prob:.1%}</div>
</div>"""
    return bars_html


# ══════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════════════════

def load_ui():
    """
    Inject all global CSS + JavaScript into the Streamlit page.
    Call this ONCE, right after st.set_page_config().
    """
    st.markdown(_MASTER_CSS, unsafe_allow_html=True)
    st.markdown(_MASTER_JS,  unsafe_allow_html=True)


def render_3d_background():
    """
    Inject the aurora / grid / floating-cube background layers.
    Call once at the top of your main() before any other content.
    """
    st.markdown(_BG_HTML, unsafe_allow_html=True)


def render_particles():
    """
    Inject the WebGL-style canvas particle field.
    Call once, before or after render_3d_background().
    """
    st.markdown(_PARTICLES_HTML, unsafe_allow_html=True)


def render_header():
    """
    Render the cinematic top header with animated orb, gradient title,
    and online status badge.
    """
    st.markdown(_HEADER_HTML, unsafe_allow_html=True)


def render_sidebar():
    """
    Inject system-status chrome into the top of the sidebar.
    Call from inside  `with st.sidebar:`.
    """
    st.markdown(_SIDEBAR_CHROME_HTML, unsafe_allow_html=True)


def render_footer():
    """
    Render the bottom status bar / footer.
    Call at the very end of main().
    """
    st.markdown(_FOOTER_HTML, unsafe_allow_html=True)


def render_loading_animation():
    """
    Display the triple-ring holographic loading spinner.
    Returns an st.empty() placeholder so you can clear it afterwards.

    Usage:
        placeholder = render_loading_animation()
        # ... do work ...
        placeholder.empty()
    """
    placeholder = st.empty()
    placeholder.markdown(_LOADING_HTML, unsafe_allow_html=True)
    return placeholder


def render_hologram_effect(label: str):
    """
    Render a flickering hologram section label above a block.

    Args:
        label: upper-case label text, e.g. "▸ ENTER QUERY"
    """
    st.markdown(_hologram_html(label), unsafe_allow_html=True)


def render_glass_container(html_content: str):
    """
    Wrap arbitrary HTML content inside a glassmorphism card with
    scan-line overlay, mouse-tilt, and reveal animation.

    Args:
        html_content: inner HTML string to display.
    """
    st.markdown(
        f'<div class="glass-card hologram-overlay" style="padding:24px 28px;margin-bottom:16px;">'
        f'{html_content}</div>',
        unsafe_allow_html=True,
    )


def render_result_card(result: dict, intent_meta: dict):
    """
    Render the full intent-classification result as a cinematic
    holographic card with animated confidence ring + probability bars.

    Args:
        result:      dict returned by predict()
        intent_meta: INTENT_META dict from app.py
    """
    html = _build_result_card_html(result, intent_meta)
    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# CONVENIENCE: styled section divider
# ══════════════════════════════════════════════════════════════════════════

def render_divider():
    """Thin neon gradient divider line."""
    st.markdown(
        '<div style="height:1px;background:linear-gradient(90deg,'
        'transparent,rgba(139,92,246,0.5),rgba(0,245,255,0.5),transparent);'
        'margin:1.5rem 0;"></div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════
# HOW TO INTEGRATE INTO app.py
# ══════════════════════════════════════════════════════════════════════════
#
#  At the top of app.py, add:
#
#      from ui_design import (
#          load_ui, render_3d_background, render_particles,
#          render_header, render_sidebar, render_footer,
#          render_hologram_effect, render_glass_container,
#          render_result_card, render_loading_animation,
#          render_divider,
#      )
#
#  Inside main(), replace the existing render_result() calls with
#  render_result_card(result, INTENT_META), and add the other calls
#  as shown in the integration example below.
#
# ── Integration patch for app.py main() ───────────────────────────────────
#
#  def main():
#      load_ui()
#      render_3d_background()
#      render_particles()
#      render_header()
#
#      encoder = load_encoder()
#      clf, le = load_classifier()
#      if clf is None:
#          ... (unchanged)
#          return
#
#      with st.sidebar:
#          render_sidebar()
#          st.markdown("### 📌 Supported Intents")
#          for key, meta in INTENT_META.items():
#              if key != "unknown_intent":
#                  st.markdown(f"{meta['icon']} **{meta['label']}**")
#          st.markdown("---")
#          st.markdown("### ⚙️ Model Info")
#          st.code(f"Encoder: {EMBEDDING_MODEL}\nThreshold: {CONFIDENCE_THRESHOLD:.0%}")
#
#      render_hologram_effect("▸ ENTER QUERY")
#      examples = ["", "hi, how are you?", ...]
#      selected  = st.selectbox(...)
#      user_input = st.text_area(...)
#
#      col1, col2 = st.columns([1,5])
#      with col1:
#          classify_btn = st.button("CLASSIFY →", type="primary", use_container_width=True)
#
#      if classify_btn:
#          if not user_input.strip():
#              st.error("⚠️  Please enter some text first.")
#          else:
#              placeholder = render_loading_animation()
#              result = predict(user_input.strip(), encoder, clf, le)
#              placeholder.empty()
#              render_hologram_effect("▸ CLASSIFICATION RESULT")
#              render_result_card(result, INTENT_META)
#
#      render_divider()
#      render_footer()
#
# ══════════════════════════════════════════════════════════════════════════
