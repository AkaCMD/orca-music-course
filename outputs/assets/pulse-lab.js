'use strict';
// Shared lesson component: a fixed-tempo comparison and immediate quiz feedback.
for (const root of document.querySelectorAll('[data-pulse-lab], [data-melody-lab]')) {
  const melodyMode = root.hasAttribute('data-melody-lab');
  let sequence = melodyMode ? 'CDEG' : 'CCCC';
  const bpm = Number(root.dataset.bpm || 90);
  const frameSeconds = 60 / bpm / 4;
  let rate = 4, ctx, timer, playing = false, loading = false, generation = 0;
  let nextTime = 0, frame = 0, raf, samplePromise;
  let samples;
  const activeVoices = new Set();
  const scheduled = [];
  const frames = root.querySelector('.frames');
  const status = root.querySelector('[data-status]');
  const toggle = root.querySelector('[data-toggle]');
  for (let i = 0; i < 16; i++) {
    const el = document.createElement('span');
    el.className = 'frame';
    el.textContent = i % 4 === 0 ? String(i / 4 + 1) : '·';
    el.setAttribute('aria-hidden', 'true');
    frames.append(el);
  }
  function paint() {
    [...frames.children].forEach((el, i) => el.classList.toggle('on', i % rate === 0));
    if (melodyMode) {
      [...frames.children].forEach((el, i) => { el.textContent = i % 4 === 0 ? sequence[i / 4] : '·'; });
      root.querySelector('[data-patch-sequence]').textContent = sequence;
      root.querySelectorAll('[data-note-select]').forEach((select, i) => { select.value = sequence[i]; });
      root.querySelectorAll('[data-sequence]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.sequence === sequence)));
    }
    for (const btn of root.querySelectorAll('[data-rate]')) btn.setAttribute('aria-pressed', String(Number(btn.dataset.rate) === rate));
    const patchRate = root.querySelector('[data-patch-rate]');
    if (patchRate) patchRate.textContent = String(rate);
  }
  function note(time, name) {
    const source = ctx.createBufferSource(), gain = ctx.createGain();
    source.buffer = samples[name];
    source.connect(gain).connect(ctx.destination);
    const voice = { source, gain };
    activeVoices.add(voice);
    source.onended = () => { activeVoices.delete(voice); source.disconnect(); gain.disconnect(); };
    source.start(time);
  }
  function schedule() {
    while (playing && nextTime < ctx.currentTime + 0.12) {
      if (frame % rate === 0) note(nextTime, sequence[Math.floor(frame / rate) % sequence.length]);
      scheduled.push({ time: nextTime, index: frame % 16 });
      frame++; nextTime += frameSeconds;
    }
  }
  function draw() {
    if (!playing) return;
    while (scheduled.length && scheduled[0].time <= ctx.currentTime) {
      const current = scheduled.shift().index;
      [...frames.children].forEach((el, i) => el.classList.toggle('current', i === current));
    }
    raf = requestAnimationFrame(draw);
  }
  function stop() {
    generation++; loading = false;
    playing = false; clearInterval(timer); cancelAnimationFrame(raf);
    for (const voice of activeVoices) {
      try {
        voice.gain.gain.setValueAtTime(1, ctx.currentTime);
        voice.gain.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.015);
        voice.source.stop(ctx.currentTime + 0.02);
      } catch {}
    }
    scheduled.length = 0;
    [...frames.children].forEach(el => el.classList.remove('current'));
    toggle.textContent = '开始试听'; toggle.setAttribute('aria-pressed', 'false');
    status.textContent = melodyMode ? '已停止。可以修改四个音，再次试听。' : '已停止。可以切换 D4 和 D2，再次试听。';
  }
  async function start() {
    const token = ++generation;
    loading = true;
    toggle.textContent = '加载音色…'; toggle.setAttribute('aria-pressed', 'true');
    try {
      ctx ??= new (window.AudioContext || window.webkitAudioContext)();
      await ctx.resume();
      const bank = melodyMode ? window.OrcaMelodyAudio : window.OrcaCourseAudio;
      if (!bank || bank.bpm !== bpm || bank.gate_frames !== 1) throw new Error('Course sound profile mismatch');
      samplePromise ??= Promise.all(Object.entries(bank.samples || { C: bank.wav_base64 }).map(async ([name, base64]) =>
        [name, await ctx.decodeAudioData(Uint8Array.from(atob(base64), ch => ch.charCodeAt(0)).buffer)]))
        .then(entries => Object.fromEntries(entries))
        .catch(error => { samplePromise = null; throw error; });
      samples = await samplePromise;
      if (generation !== token || document.hidden) return;
      loading = false;
      playing = true; frame = 0; nextTime = ctx.currentTime + 0.05;
      toggle.textContent = '停止试听'; toggle.setAttribute('aria-pressed', 'true');
      status.textContent = melodyMode ? `播放中：${sequence.split('').join(' → ')} · ${bank.preset_name} · ${bpm} BPM。` : `播放中：${bank.preset_name} · ${bpm} BPM。请匀速数 1、2、3、4。`;
      schedule(); timer = setInterval(schedule, 25); draw();
    } catch {
      if (generation !== token) return;
      stop(); status.textContent = '音色未能加载。请刷新教材，或在终端 Orca 中打开练习文件。';
    }
  }
  toggle.addEventListener('click', () => playing || loading ? stop() : start());
  for (const btn of root.querySelectorAll('[data-rate]')) btn.addEventListener('click', () => {
    rate = Number(btn.dataset.rate); const resume = playing || loading;
    if (resume) stop(); paint(); if (resume) start();
  });
  function setSequence(value) {
    if (!/^[CDEG]{4}$/.test(value)) return;
    const resume = playing || loading;
    if (resume) stop();
    sequence = value; paint();
    if (resume) start();
  }
  for (const button of root.querySelectorAll('[data-sequence]')) button.addEventListener('click', () => setSequence(button.dataset.sequence));
  for (const select of root.querySelectorAll('[data-note-select]')) select.addEventListener('change', () =>
    setSequence([...root.querySelectorAll('[data-note-select]')].map(input => input.value).join('')));
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  window.addEventListener('pagehide', stop);
  paint();
}
for (const quiz of document.querySelectorAll('[data-quiz]')) {
  for (const button of quiz.querySelectorAll('[data-answer]')) button.addEventListener('click', () => {
    const correct = button.dataset.answer === quiz.dataset.correct;
    quiz.querySelector('[data-feedback]').textContent = correct ? quiz.dataset.success : quiz.dataset.retry;
  });
}
