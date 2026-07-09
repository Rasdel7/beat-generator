import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Beat Generator",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Beat Generator")
st.markdown("Create drum patterns, control BPM "
            "and mix beats in your browser.")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.markdown("🥁 **16-step sequencer**")
col2.markdown("🎚️ **BPM + volume control**")
col3.markdown("🎸 **6 drum instruments**")

beat_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  * { box-sizing: border-box; margin: 0;
      padding: 0; }
  body {
    background: #0d1117;
    font-family: 'Courier New', monospace;
    color: #cdd9e5;
    padding: 16px;
    user-select: none;
  }
  h2 {
    color: #58a6ff;
    text-align: center;
    margin-bottom: 16px;
    font-size: 1.2rem;
    letter-spacing: 2px;
  }
  #controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }
  .ctrl-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  .ctrl-label {
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .ctrl-value {
    font-size: 1rem;
    color: #58a6ff;
    font-weight: bold;
    min-width: 50px;
    text-align: center;
  }
  input[type=range] {
    width: 120px;
    accent-color: #58a6ff;
    cursor: pointer;
  }
  #transport {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  .btn {
    padding: 10px 24px;
    border: none;
    border-radius: 8px;
    font-size: 0.95rem;
    font-family: monospace;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.15s;
    letter-spacing: 1px;
  }
  .btn-play {
    background: #2ecc71;
    color: #000;
  }
  .btn-play:hover { background: #27ae60; }
  .btn-stop {
    background: #e74c3c;
    color: #fff;
  }
  .btn-stop:hover { background: #c0392b; }
  .btn-clear {
    background: #30363d;
    color: #cdd9e5;
  }
  .btn-clear:hover { background: #444; }
  .btn-random {
    background: #9b59b6;
    color: #fff;
  }
  .btn-random:hover { background: #8e44ad; }
  #sequencer {
    max-width: 900px;
    margin: 0 auto;
  }
  .track {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    gap: 8px;
  }
  .track-label {
    width: 80px;
    font-size: 0.8rem;
    color: #8b949e;
    text-align: right;
    padding-right: 8px;
    flex-shrink: 0;
  }
  .track-emoji {
    font-size: 1rem;
    width: 28px;
    text-align: center;
    flex-shrink: 0;
  }
  .steps {
    display: flex;
    gap: 4px;
    flex: 1;
  }
  .step {
    flex: 1;
    height: 36px;
    border-radius: 5px;
    border: 1px solid #30363d;
    background: #161b22;
    cursor: pointer;
    transition: background 0.1s;
    min-width: 0;
  }
  .step.active {
    background: var(--track-color, #58a6ff);
    border-color: var(--track-color, #58a6ff);
    box-shadow: 0 0 6px var(--track-color,
                            #58a6ff);
  }
  .step.playing {
    outline: 2px solid #fff;
    outline-offset: 1px;
  }
  .step.beat-marker {
    border-left: 2px solid #444;
  }
  .track-vol {
    width: 60px;
    accent-color: #58a6ff;
  }
  #beat-display {
    text-align: center;
    margin: 12px 0;
    height: 20px;
  }
  .bar-viz {
    display: inline-flex;
    gap: 3px;
    align-items: flex-end;
  }
  .bar-viz span {
    display: inline-block;
    width: 6px;
    background: #2ecc71;
    border-radius: 2px;
    transition: height 0.1s;
  }
  #presets {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  .preset-btn {
    padding: 6px 14px;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #cdd9e5;
    font-family: monospace;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.15s;
  }
  .preset-btn:hover {
    background: #30363d;
    border-color: #58a6ff;
  }
  #step-counter {
    text-align: center;
    color: #8b949e;
    font-size: 0.8rem;
    margin-bottom: 8px;
  }
</style>
</head>
<body>

<h2>⬡ STEP SEQUENCER</h2>

<div id="presets">
  <button class="preset-btn"
    onclick="loadPreset('hiphop')">
    🎤 Hip-Hop</button>
  <button class="preset-btn"
    onclick="loadPreset('rock')">
    🎸 Rock</button>
  <button class="preset-btn"
    onclick="loadPreset('electronic')">
    ⚡ Electronic</button>
  <button class="preset-btn"
    onclick="loadPreset('reggae')">
    🌴 Reggae</button>
  <button class="preset-btn"
    onclick="loadPreset('jazz')">
    🎷 Jazz</button>
</div>

<div id="controls">
  <div class="ctrl-group">
    <span class="ctrl-label">BPM</span>
    <input type="range" id="bpm"
      min="60" max="200" value="120"
      oninput="updateBPM(this.value)">
    <span class="ctrl-value"
      id="bpm-val">120</span>
  </div>
  <div class="ctrl-group">
    <span class="ctrl-label">Master Vol</span>
    <input type="range" id="master-vol"
      min="0" max="1" step="0.05" value="0.7"
      oninput="updateMasterVol(this.value)">
    <span class="ctrl-value"
      id="vol-val">70%</span>
  </div>
  <div class="ctrl-group">
    <span class="ctrl-label">Reverb</span>
    <input type="range" id="reverb"
      min="0" max="0.8" step="0.05" value="0.1"
      oninput="updateReverb(this.value)">
    <span class="ctrl-value"
      id="rev-val">10%</span>
  </div>
  <div class="ctrl-group">
    <span class="ctrl-label">Swing</span>
    <input type="range" id="swing"
      min="0" max="0.3" step="0.01" value="0"
      oninput="updateSwing(this.value)">
    <span class="ctrl-value"
      id="sw-val">0%</span>
  </div>
</div>

<div id="transport">
  <button class="btn btn-play"
    onclick="startSeq()">▶ PLAY</button>
  <button class="btn btn-stop"
    onclick="stopSeq()">■ STOP</button>
  <button class="btn btn-clear"
    onclick="clearAll()">✕ CLEAR</button>
  <button class="btn btn-random"
    onclick="randomize()">🎲 RANDOM</button>
</div>

<div id="beat-display">
  <div class="bar-viz" id="viz">
    <span id="v0" style="height:4px"></span>
    <span id="v1" style="height:4px"></span>
    <span id="v2" style="height:4px"></span>
    <span id="v3" style="height:4px"></span>
    <span id="v4" style="height:4px"></span>
    <span id="v5" style="height:4px"></span>
    <span id="v6" style="height:4px"></span>
    <span id="v7" style="height:4px"></span>
  </div>
</div>

<div id="step-counter">Step: 1/16</div>

<div id="sequencer"></div>

<script>
const TRACKS = [
  {id:'kick',  label:'Kick',   emoji:'🥁',
   color:'#e74c3c', freq:60,  type:'kick'},
  {id:'snare', label:'Snare',  emoji:'🎯',
   color:'#f39c12', freq:200, type:'snare'},
  {id:'hihat', label:'Hi-Hat', emoji:'🔔',
   color:'#f1c40f', freq:800, type:'hihat'},
  {id:'open',  label:'Open HH',emoji:'🎶',
   color:'#2ecc71', freq:600, type:'open'},
  {id:'clap',  label:'Clap',   emoji:'👏',
   color:'#3498db', freq:300, type:'clap'},
  {id:'perc',  label:'Perc',   emoji:'🎵',
   color:'#9b59b6', freq:150, type:'perc'},
];
const STEPS = 16;

let ctx = null;
let masterGain = null;
let reverbNode = null;
let reverbGain = null;
let dryGain    = null;

let bpm       = 120;
let masterVol = 0.7;
let reverbAmt = 0.1;
let swingAmt  = 0;

let isPlaying   = false;
let currentStep = 0;
let nextTime    = 0;
let timerID     = null;

// Grid: tracks x steps
let grid = {};
let trackVols = {};
TRACKS.forEach(t => {
  grid[t.id] = new Array(STEPS).fill(false);
  trackVols[t.id] = 0.8;
});

function initAudio() {
  if (ctx) return;
  ctx = new (window.AudioContext ||
             window.webkitAudioContext)();
  masterGain = ctx.createGain();
  masterGain.gain.value = masterVol;

  // Simple reverb via convolver
  reverbNode = ctx.createConvolver();
  reverbGain = ctx.createGain();
  dryGain    = ctx.createGain();
  reverbGain.gain.value = reverbAmt;
  dryGain.gain.value    = 1 - reverbAmt;

  // Create impulse response
  const len = ctx.sampleRate * 1.5;
  const buf = ctx.createBuffer(2, len,
                                ctx.sampleRate);
  for (let c = 0; c < 2; c++) {
    const d = buf.getChannelData(c);
    for (let i = 0; i < len; i++) {
      d[i] = (Math.random() * 2 - 1) *
             Math.pow(1 - i/len, 3);
    }
  }
  reverbNode.buffer = buf;

  masterGain.connect(dryGain);
  masterGain.connect(reverbNode);
  reverbNode.connect(reverbGain);
  dryGain.connect(ctx.destination);
  reverbGain.connect(ctx.destination);
}

function playSound(type, freq, time, vol) {
  if (!ctx) return;
  const g = ctx.createGain();
  g.connect(masterGain);
  g.gain.setValueAtTime(vol * 1.2, time);

  if (type === 'kick') {
    const osc = ctx.createOscillator();
    osc.connect(g);
    osc.frequency.setValueAtTime(freq, time);
    osc.frequency.exponentialRampToValueAtTime(
      30, time + 0.3);
    g.gain.exponentialRampToValueAtTime(
      0.001, time + 0.4);
    osc.start(time);
    osc.stop(time + 0.4);

  } else if (type === 'snare') {
    const noise = ctx.createBufferSource();
    const buf = ctx.createBuffer(
      1, ctx.sampleRate * 0.2,
      ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++)
      d[i] = Math.random() * 2 - 1;
    noise.buffer = buf;
    const filt = ctx.createBiquadFilter();
    filt.type = 'bandpass';
    filt.frequency.value = freq;
    filt.Q.value = 0.5;
    noise.connect(filt);
    filt.connect(g);
    g.gain.exponentialRampToValueAtTime(
      0.001, time + 0.15);
    noise.start(time);
    noise.stop(time + 0.2);

  } else if (type === 'hihat') {
    const noise = ctx.createBufferSource();
    const buf = ctx.createBuffer(
      1, ctx.sampleRate * 0.05,
      ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++)
      d[i] = Math.random() * 2 - 1;
    noise.buffer = buf;
    const filt = ctx.createBiquadFilter();
    filt.type = 'highpass';
    filt.frequency.value = 8000;
    noise.connect(filt);
    filt.connect(g);
    g.gain.exponentialRampToValueAtTime(
      0.001, time + 0.05);
    noise.start(time);
    noise.stop(time + 0.06);

  } else if (type === 'open') {
    const noise = ctx.createBufferSource();
    const buf = ctx.createBuffer(
      1, ctx.sampleRate * 0.4,
      ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++)
      d[i] = Math.random() * 2 - 1;
    noise.buffer = buf;
    const filt = ctx.createBiquadFilter();
    filt.type = 'highpass';
    filt.frequency.value = 6000;
    noise.connect(filt);
    filt.connect(g);
    g.gain.exponentialRampToValueAtTime(
      0.001, time + 0.4);
    noise.start(time);
    noise.stop(time + 0.45);

  } else if (type === 'clap') {
    for (let i = 0; i < 3; i++) {
      const noise = ctx.createBufferSource();
      const buf = ctx.createBuffer(
        1, ctx.sampleRate * 0.02,
        ctx.sampleRate);
      const d = buf.getChannelData(0);
      for (let j = 0; j < d.length; j++)
        d[j] = Math.random() * 2 - 1;
      noise.buffer = buf;
      const filt = ctx.createBiquadFilter();
      filt.type = 'bandpass';
      filt.frequency.value = 1200;
      noise.connect(filt);
      filt.connect(g);
      const t2 = time + i * 0.01;
      noise.start(t2);
      noise.stop(t2 + 0.025);
    }
    g.gain.exponentialRampToValueAtTime(
      0.001, time + 0.12);

  } else {
    const osc = ctx.createOscillator();
    osc.type = 'triangle';
    osc.connect(g);
    osc.frequency.value = freq;
    g.gain.exponentialRampToValueAtTime(
      0.001, time + 0.1);
    osc.start(time);
    osc.stop(time + 0.12);
  }
}

function scheduleStep(step, time) {
  TRACKS.forEach(t => {
    if (grid[t.id][step]) {
      playSound(t.type, t.freq,
                time, trackVols[t.id]);
    }
  });
}

function scheduler() {
  const stepSec = (60 / bpm) / 4;
  while (nextTime 
         ctx.currentTime + 0.1) {
    const swing_offset =
      (currentStep % 2 === 1)
      ? swingAmt * stepSec : 0;
    scheduleStep(
      currentStep,
      nextTime + swing_offset);
    updateUI(currentStep, nextTime);
    nextTime += stepSec;
    currentStep = (currentStep + 1) % STEPS;
  }
  timerID = setTimeout(scheduler, 25);
}

function updateUI(step, time) {
  const delay = Math.max(
    0, (time - (ctx ? ctx.currentTime : 0))
    * 1000);
  setTimeout(() => {
    document.querySelectorAll('.step')
      .forEach(s => s.classList.remove(
        'playing'));
    document.querySelectorAll(
      '.step[data-step="' + step + '"]')
      .forEach(s => s.classList.add(
        'playing'));
    document.getElementById('step-counter')
      .textContent =
        'Step: ' + (step + 1) + '/16';

    // Visualizer
    let active = 0;
    TRACKS.forEach(t => {
      if (grid[t.id][step]) active++;
    });
    for (let i = 0; i < 8; i++) {
      const h = i < active
        ? 4 + Math.random() * 24 : 4;
      const el = document.getElementById(
        'v' + i);
      if (el) el.style.height = h + 'px';
    }
  }, delay);
}

function startSeq() {
  initAudio();
  if (ctx.state === 'suspended')
    ctx.resume();
  if (isPlaying) return;
  isPlaying   = true;
  currentStep = 0;
  nextTime    = ctx.currentTime;
  scheduler();
}

function stopSeq() {
  isPlaying = false;
  clearTimeout(timerID);
  document.querySelectorAll('.step')
    .forEach(s => s.classList.remove(
      'playing'));
  for (let i = 0; i < 8; i++) {
    const el = document.getElementById(
      'v' + i);
    if (el) el.style.height = '4px';
  }
  document.getElementById('step-counter')
    .textContent = 'Step: 1/16';
}

function clearAll() {
  TRACKS.forEach(t => {
    grid[t.id] = new Array(STEPS).fill(false);
  });
  renderGrid();
}

function randomize() {
  TRACKS.forEach((t, ti) => {
    const density = ti === 0 ? 0.4
      : ti === 1 ? 0.25
      : ti === 2 ? 0.5
      : 0.2;
    grid[t.id] = Array.from(
      {length: STEPS},
      () => Math.random() < density);
  });
  renderGrid();
}

function updateBPM(v) {
  bpm = parseInt(v);
  document.getElementById('bpm-val')
    .textContent = v;
}
function updateMasterVol(v) {
  masterVol = parseFloat(v);
  if (masterGain)
    masterGain.gain.value = masterVol;
  document.getElementById('vol-val')
    .textContent = Math.round(v * 100) + '%';
}
function updateReverb(v) {
  reverbAmt = parseFloat(v);
  if (reverbGain && dryGain) {
    reverbGain.gain.value = reverbAmt;
    dryGain.gain.value = 1 - reverbAmt;
  }
  document.getElementById('rev-val')
    .textContent = Math.round(v * 100) + '%';
}
function updateSwing(v) {
  swingAmt = parseFloat(v);
  document.getElementById('sw-val')
    .textContent = Math.round(v * 100) + '%';
}

const PRESETS = {
  hiphop: {
    kick:  [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    snare: [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    hihat: [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    open:  [0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
    clap:  [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    perc:  [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
  },
  rock: {
    kick:  [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
    snare: [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    hihat: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    open:  [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    clap:  [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    perc:  [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0],
  },
  electronic: {
    kick:  [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    snare: [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    hihat: [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    open:  [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    clap:  [0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0],
    perc:  [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],
  },
  reggae: {
    kick:  [1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
    snare: [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    hihat: [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    open:  [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    clap:  [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0],
    perc:  [0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0],
  },
  jazz: {
    kick:  [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
    snare: [0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0],
    hihat: [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    open:  [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    clap:  [0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
    perc:  [0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0],
  }
};

function loadPreset(name) {
  const p = PRESETS[name];
  if (!p) return;
  TRACKS.forEach(t => {
    if (p[t.id])
      grid[t.id] = p[t.id].map(
        v => v === 1);
  });
  renderGrid();
}

function toggleStep(trackId, step) {
  grid[trackId][step] =
    !grid[trackId][step];
  const btn = document.querySelector(
    '.step[data-track="' + trackId +
    '"][data-step="' + step + '"]');
  if (btn) {
    if (grid[trackId][step])
      btn.classList.add('active');
    else
      btn.classList.remove('active');
  }
}

function renderGrid() {
  const seq = document.getElementById(
    'sequencer');
  seq.innerHTML = '';

  TRACKS.forEach(t => {
    const track = document.createElement('div');
    track.className = 'track';

    const emoji = document.createElement('div');
    emoji.className = 'track-emoji';
    emoji.textContent = t.emoji;

    const label = document.createElement('div');
    label.className = 'track-label';
    label.textContent = t.label;

    const steps = document.createElement('div');
    steps.className = 'steps';

    for (let s = 0; s < STEPS; s++) {
      const btn = document.createElement('button');
      btn.className = 'step' +
        (s % 4 === 0 ? ' beat-marker' : '') +
        (grid[t.id][s] ? ' active' : '');
      btn.dataset.track = t.id;
      btn.dataset.step  = s;
      btn.style.setProperty(
        '--track-color', t.color);
      btn.onclick = () =>
        toggleStep(t.id, s);
      steps.appendChild(btn);
    }

    const vol = document.createElement('input');
    vol.type  = 'range';
    vol.min   = '0';
    vol.max   = '1';
    vol.step  = '0.05';
    vol.value = trackVols[t.id];
    vol.className = 'track-vol';
    vol.title = t.label + ' volume';
    vol.oninput = e => {
      trackVols[t.id] = parseFloat(e.target.value);
    };

    track.appendChild(emoji);
    track.appendChild(label);
    track.appendChild(steps);
    track.appendChild(vol);
    seq.appendChild(track);
  });
}

// Init
loadPreset('hiphop');
</script>
</body>
</html>
"""

components.html(beat_html, height=680)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🥁 How to Use
    1. **Pick a preset** — Hip-Hop, Rock, Electronic, Reggae or Jazz
    2. **Press ▶ PLAY** to start the beat
    3. **Click grid cells** to toggle sounds on/off
    4. **Adjust BPM** for tempo (60–200)
    5. **Reverb** adds space/depth to the sound
    6. **Swing** adds groove/shuffle feel
    7. **🎲 RANDOM** generates a random beat
    8. **Volume sliders** on each track row
    """)

with col2:
    st.markdown("""
    ### 🎚️ Instruments
    | Icon | Track | Sound Type |
    |------|-------|-----------|
    | 🥁 | Kick | Low freq oscillator |
    | 🎯 | Snare | Bandpass noise |
    | 🔔 | Hi-Hat | Highpass noise (short) |
    | 🎶 | Open HH | Highpass noise (long) |
    | 👏 | Clap | Triple burst noise |
    | 🎵 | Perc | Triangle oscillator |

    ### ⚡ Tips
    - Add **kick on beats 1 and 9** for stability
    - **Snare on 5 and 13** is classic
    - **Hi-hat every step** = 16th note feel
    - Lower BPM + swing = hip-hop groove
    """)

st.markdown("---")
st.markdown(
    "Built by **Jyotiraditya** | "
    "Beat Generator | "
    "Web Audio API + Streamlit"
)