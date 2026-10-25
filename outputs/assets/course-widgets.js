'use strict';
for (const quiz of document.querySelectorAll('[data-quiz]')) {
  for (const button of quiz.querySelectorAll('[data-answer]')) button.addEventListener('click', () => {
    quiz.querySelector('[data-feedback]').textContent = button.dataset.answer === quiz.dataset.correct ? quiz.dataset.success : quiz.dataset.retry;
  });
}
for (const audio of document.querySelectorAll('audio')) audio.addEventListener('play', () => {
  for (const other of document.querySelectorAll('audio')) if (other !== audio) other.pause();
  for (const stop of window.orcaCourseStops || []) stop();
});
window.orcaCourseStops ||= [];
for (const root of document.querySelectorAll('[data-state-lab]')) {
  let ctx, sources=[], gains=[], buffers, loading=false, playing=false, generation=0;
  let origin=0, current='calm', desired='calm', pendingAt=null, animation;
  const bpm=Number(root.dataset.bpm), barSeconds=240/bpm;
  const toggle=root.querySelector('[data-state-toggle]'), status=root.querySelector('[data-state-status]');
  const scene=root.querySelector('[data-state-scene]'), progress=root.querySelector('[data-state-progress]');
  function paint(){
    for(const button of root.querySelectorAll('[data-state]'))button.setAttribute('aria-pressed',String(button.dataset.state===desired));
    scene.textContent='旧城高架花园 · '+(current==='calm'?'探索':'遇敌');
    root.classList.toggle('danger',current==='battle');
  }
  function stop(){
    generation++;playing=false;loading=false;cancelAnimationFrame(animation);
    const now=ctx?.currentTime||0;
    gains.forEach(g=>{g.gain.cancelScheduledValues(now);g.gain.setTargetAtTime(0,now,.012);});
    sources.forEach(source=>{try{source.stop(now+.06);}catch{}});
    sources=[];gains=[];pendingAt=null;progress.style.width='0%';
    toggle.textContent='启动场景试听';status.textContent='已停止。选择状态后可再次启动。';paint();
  }
  function draw(){
    if(!playing)return;
    const now=ctx.currentTime;
    if(pendingAt!==null&&now>=pendingAt){current=desired;pendingAt=null;status.textContent='当前状态：'+(current==='calm'?'探索':'遇敌')+'；保持同一音乐时间线。';paint();}
    progress.style.width=(Math.max(0,now-origin)%barSeconds/barSeconds*100)+'%';
    animation=requestAnimationFrame(draw);
  }
  async function start(){
    const token=++generation;loading=true;toggle.textContent='加载两种状态…';
    for(const audio of document.querySelectorAll('audio'))audio.pause();
    try{
      ctx ||= new (window.AudioContext||window.webkitAudioContext)();await ctx.resume();
      if(!buffers)buffers=await Promise.all([root.dataset.calm,root.dataset.battle].map(async url=>{
        const response=await fetch(url);if(!response.ok)throw new Error('Audio unavailable');
        return ctx.decodeAudioData(await response.arrayBuffer());
      }));
      if(token!==generation)return;
      if(Math.abs(buffers[0].duration-buffers[1].duration)>1/ctx.sampleRate)throw new Error('State lengths differ');
      current=desired;origin=ctx.currentTime+.1;
      sources=buffers.map((buffer,index)=>{
        const source=ctx.createBufferSource(), gain=ctx.createGain();
        source.buffer=buffer;source.loop=true;source.loopEnd=buffer.duration;
        gain.gain.value=(index===0)===(current==='calm')?1:0;
        source.connect(gain).connect(ctx.destination);gains.push(gain);source.start(origin);return source;
      });
      playing=true;loading=false;toggle.textContent='停止场景试听';status.textContent='播放中。请选择探索或遇敌，比较下一个小节的变化。';paint();draw();
    }catch(error){
      if(token!==generation)return;
      stop();status.textContent='互动暂不可用。请从本地网页服务打开本页；仍可使用上方音频试听两个状态。';
    }
  }
  for(const button of root.querySelectorAll('[data-state]'))button.addEventListener('click',()=>{
    desired=button.dataset.state;paint();
    if(!playing)return;
    const now=ctx.currentTime;
    pendingAt=origin+Math.max(1,Math.floor((now-origin)/barSeconds)+1)*barSeconds;
    gains.forEach((gain,index)=>{
      gain.gain.cancelScheduledValues(now);
      gain.gain.setValueAtTime((index===0)===(current==='calm')?1:0,now);
      gain.gain.setValueAtTime((index===0)===(current==='calm')?1:0,pendingAt);
      gain.gain.linearRampToValueAtTime((index===0)===(desired==='calm')?1:0,pendingAt+.04);
    });
    status.textContent='已排队：下个小节进入'+(desired==='calm'?'探索':'遇敌')+'。';
  });
  toggle.addEventListener('click',()=>playing||loading?stop():start());
  window.orcaCourseStops.push(stop);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  window.addEventListener('pagehide',stop);paint();
}
