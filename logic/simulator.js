/**
 * Auto Do - Interactive Application Simulator & Virtual Macro Engine
 */

class AutoDoSimulator {
  constructor() {
    this.statusEl = document.getElementById('app-status');
    this.recordBtn = document.getElementById('btn-record');
    this.stopBtn = document.getElementById('btn-stop');
    this.playBtn = document.getElementById('btn-play');
    this.saveBtn = document.getElementById('btn-save');
    this.loadBtn = document.getElementById('btn-load');
    this.helpBtn = document.getElementById('btn-help');
    this.helpModal = document.getElementById('help-modal');
    this.closeHelpBtn = document.getElementById('btn-close-help');
    this.canvas = document.getElementById('sim-canvas');
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.cursorEl = document.getElementById('sim-cursor');
    this.appBody = document.querySelector('.app-body');

    this.state = 'idle'; // 'idle' | 'recording' | 'playing'
    this.recordedActions = [];
    this.playbackAnimationId = null;
    this.recordTimer = null;
    this.audioCtx = null;

    this.init();
  }

  init() {
    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());

    // Event listeners for App Buttons
    if (this.recordBtn) this.recordBtn.addEventListener('click', () => this.startRecording());
    if (this.stopBtn) this.stopBtn.addEventListener('click', () => this.stop());
    if (this.playBtn) this.playBtn.addEventListener('click', () => this.play());
    if (this.saveBtn) this.saveBtn.addEventListener('click', () => this.saveMacro());
    if (this.loadBtn) this.loadBtn.addEventListener('click', () => this.loadMacro());
    if (this.helpBtn) this.helpBtn.addEventListener('click', () => this.toggleHelp(true));
    if (this.closeHelpBtn) this.closeHelpBtn.addEventListener('click', () => this.toggleHelp(false));

    if (this.helpModal) {
      this.helpModal.addEventListener('click', (e) => {
        if (e.target === this.helpModal) this.toggleHelp(false);
      });
    }

    // Keyboard Shortcuts (F11, F12, F10, Esc)
    window.addEventListener('keydown', (e) => {
      if (e.key === 'F11') {
        e.preventDefault();
        this.startRecording();
      } else if (e.key === 'F12') {
        e.preventDefault();
        this.stop();
      } else if (e.key === 'F10') {
        e.preventDefault();
        this.play();
      } else if (e.key === 'Escape') {
        this.toggleHelp(false);
      }
    });

    // Capture movements inside mockup when recording
    if (this.appBody) {
      this.appBody.addEventListener('mousemove', (e) => {
        if (this.state === 'recording') {
          const rect = this.appBody.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          this.recordedActions.push({ x, y, time: Date.now() });
          this.updateStatus(`Status: Recording (${this.recordedActions.length} actions)...`);
          this.drawDot(x, y, '#fb6f6f');
        }
      });
    }

    // Default sample macro routine if user clicks Play immediately
    this.createDefaultRoutine();
  }

  resizeCanvas() {
    if (!this.canvas || !this.appBody) return;
    this.canvas.width = this.appBody.clientWidth;
    this.canvas.height = this.appBody.clientHeight;
  }

  playAudio(freq = 440, type = 'sine', duration = 0.08) {
    try {
      if (!this.audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) this.audioCtx = new AudioContext();
      }
      if (!this.audioCtx) return;
      if (this.audioCtx.state === 'suspended') {
        this.audioCtx.resume();
      }

      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
      gain.gain.setValueAtTime(0.05, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start();
      osc.stop(this.audioCtx.currentTime + duration);
    } catch {
      // Audio playback context fallback
    }
  }

  updateStatus(text, highlightColor = null) {
    if (this.statusEl) {
      this.statusEl.textContent = text;
      if (highlightColor) {
        this.statusEl.style.color = highlightColor;
      } else {
        this.statusEl.style.color = '';
      }
    }
  }

  createDefaultRoutine() {
    if (this.recordedActions.length === 0) {
      // Create a smooth circular / figure-8 automated demo routine
      const w = this.canvas ? this.canvas.width || 340 : 340;
      const h = this.canvas ? this.canvas.height || 260 : 260;
      const cx = w / 2;
      const cy = h / 2;
      const points = [];
      const totalPoints = 60;

      for (let i = 0; i <= totalPoints; i++) {
        const angle = (i / totalPoints) * Math.PI * 2;
        const x = cx + Math.sin(angle) * (w * 0.35);
        const y = cy + Math.sin(angle * 2) * (h * 0.25);
        points.push({ x, y, time: i * 25 });
      }
      this.recordedActions = points;
    }
  }

  startRecording() {
    if (this.state === 'recording') return;
    this.state = 'recording';
    this.recordedActions = [];
    this.clearCanvas();
    this.playAudio(650, 'triangle', 0.12);

    if (this.recordBtn) this.recordBtn.classList.add('recording-active');
    if (this.playBtn) this.playBtn.classList.remove('playing-active');
    if (this.cursorEl) this.cursorEl.classList.remove('active');

    this.updateStatus('Status: Recording... (Move mouse here)', '#fb6f6f');
    window.showToast('⏺️ Recording started. Move mouse inside window or press F9 to stop.', 'info');
  }

  stop() {
    if (this.state === 'idle') return;
    this.playAudio(380, 'sine', 0.1);
    
    if (this.state === 'playing' && this.playbackAnimationId) {
      cancelAnimationFrame(this.playbackAnimationId);
    }

    this.state = 'idle';
    if (this.recordBtn) this.recordBtn.classList.remove('recording-active');
    if (this.playBtn) this.playBtn.classList.remove('playing-active');
    if (this.cursorEl) this.cursorEl.classList.remove('active');

    const count = this.recordedActions.length;
    this.updateStatus(`Status: Ready (${count} steps recorded)`, '#4ade80');
    window.showToast(`⏹️ Stopped. Captured ${count} automation coordinates.`, 'success');
  }

  play() {
    if (this.state === 'playing') return;
    if (this.recordedActions.length === 0) {
      this.createDefaultRoutine();
    }

    this.state = 'playing';
    this.clearCanvas();
    this.playAudio(880, 'sine', 0.15);

    if (this.playBtn) this.playBtn.classList.add('playing-active');
    if (this.recordBtn) this.recordBtn.classList.remove('recording-active');
    if (this.cursorEl) this.cursorEl.classList.add('active');

    const isInfinite = document.getElementById('sim-infinite-check')?.checked || false;
    const maxLoops = isInfinite ? 0 : Math.max(1, parseInt(document.getElementById('sim-loop-count')?.value || '1', 10));
    let currentLoop = 1;

    const updateLoopStatus = () => {
      const loopText = isInfinite ? `Loop ${currentLoop} - Infinite ∞` : `Loop ${currentLoop}/${maxLoops}`;
      this.updateStatus(`Status: Replaying (${loopText})...`, '#4ade80');
    };

    updateLoopStatus();
    window.showToast(`▶️ Replaying sequence (${isInfinite ? 'Infinite Loops ∞' : maxLoops + ' loop(s)'})...`, 'success');

    let index = 0;
    const total = this.recordedActions.length;

    const step = () => {
      if (this.state !== 'playing') return;

      if (index < total) {
        const point = this.recordedActions[index];
        if (this.cursorEl) {
          this.cursorEl.style.left = `${point.x}px`;
          this.cursorEl.style.top = `${point.y}px`;
        }

        if (index > 0) {
          const prev = this.recordedActions[index - 1];
          this.drawLine(prev.x, prev.y, point.x, point.y, '#4ade80');
        }

        index++;
        this.playbackAnimationId = requestAnimationFrame(step);
      } else {
        if (isInfinite || currentLoop < maxLoops) {
          currentLoop++;
          index = 0;
          this.clearCanvas();
          updateLoopStatus();
          this.playbackAnimationId = requestAnimationFrame(step);
        } else {
          this.state = 'idle';
          if (this.playBtn) this.playBtn.classList.remove('playing-active');
          if (this.cursorEl) this.cursorEl.classList.remove('active');
          this.updateStatus(`Status: Playback Completed (${maxLoops} loops, ${total} actions)`, '#a5b4fc');
          window.showToast('✅ Macro playback finished perfectly!', 'success');
        }
      }
    };

    this.playbackAnimationId = requestAnimationFrame(step);
  }

  saveMacro() {
    this.playAudio(520, 'sine', 0.1);
    if (this.recordedActions.length === 0) {
      this.createDefaultRoutine();
    }

    const data = {
      app: 'DENM Auto-Do',
      version: '2.4.0',
      timestamp: new Date().toISOString(),
      actionCount: this.recordedActions.length,
      actions: this.recordedActions
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'autodo_macro_profile.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    this.updateStatus('Status: Macro Saved Successfully');
    window.showToast('💾 Macro profile exported as JSON file!', 'success');
  }

  loadMacro() {
    this.playAudio(600, 'sine', 0.1);
    // Create a rich simulated multi-click macro
    this.recordedActions = [];
    const w = this.canvas ? this.canvas.width || 340 : 340;
    const h = this.canvas ? this.canvas.height || 260 : 260;

    // Pattern: Zigzag grid sweep
    for (let row = 0; row < 4; row++) {
      const y = (h * 0.2) + (row * (h * 0.2));
      for (let col = 0; col < 8; col++) {
        const x = row % 2 === 0 ? (w * 0.15) + col * (w * 0.1) : (w * 0.85) - col * (w * 0.1);
        this.recordedActions.push({ x, y, time: (row * 8 + col) * 30 });
      }
    }

    this.clearCanvas();
    this.updateStatus(`Status: Loaded 'Precision_Grid_Sweep.json' (${this.recordedActions.length} steps)`);
    window.showToast("📂 Loaded profile: 'Precision_Grid_Sweep.json'", 'info');
  }

  toggleHelp(show) {
    if (!this.helpModal) return;
    this.playAudio(show ? 700 : 300, 'sine', 0.08);
    if (show) {
      this.helpModal.classList.add('open');
    } else {
      this.helpModal.classList.remove('open');
    }
  }

  drawDot(x, y, color) {
    if (!this.ctx) return;
    this.ctx.fillStyle = color;
    this.ctx.beginPath();
    this.ctx.arc(x, y, 2.5, 0, Math.PI * 2);
    this.ctx.fill();
  }

  drawLine(x1, y1, x2, y2, color) {
    if (!this.ctx) return;
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = 2.5;
    this.ctx.lineCap = 'round';
    this.ctx.shadowColor = color;
    this.ctx.shadowBlur = 8;
    this.ctx.beginPath();
    this.ctx.moveTo(x1, y1);
    this.ctx.lineTo(x2, y2);
    this.ctx.stroke();
    this.ctx.shadowBlur = 0;
  }

  clearCanvas() {
    if (!this.ctx || !this.canvas) return;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
  window.autoDoSim = new AutoDoSimulator();
});
