"""Build the full course from source content and verify each patch in Orca-c."""
import argparse
import html
import importlib.util
import json
from pattern_engine import ROOT, track, save_pattern, render_pattern, verify
spec=importlib.util.spec_from_file_location('lesson_content',ROOT/'course/lessons.py')
content=importlib.util.module_from_spec(spec);spec.loader.exec_module(content)
LESSONS,SOURCES=content.LESSONS,content.SOURCES

def lead(notes,**kw):return track(notes,label='LEAD',**kw)
def harmony(order='JAMN',middle='ECAB',top='GEJK',repeat=1,bass=True):
    rows=[track(order*repeat,step=16,octave=2,velocity=4,gate=10,label='BASS')] if bass else []
    return rows+[track(order*repeat,step=16,octave=3,velocity=3,gate=12,label='ROOT'),track(middle*repeat,step=16,octave=4,velocity=3,gate=12,label='THIRD'),track(top*repeat,step=16,octave=4,velocity=3,gate=12,label='FIFTH')]
def drums():return [track('C',step=4,octave=3,velocity=7,gate=1,channel=9,label='KICK'),track('.D.D',step=4,octave=3,velocity=5,gate=1,channel=9,label='SNARE'),track('f',step=2,octave=3,velocity=3,gate=1,channel=9,label='HAT')]
phrase='CDEGCDEGEGGJCDEG'
base=[lead(phrase,octave=6,velocity=5,gate=2)]
arranged=base+harmony()
final_theme='CDEGEDGCCDEGGEDCEGGJBAGEDEDGEDDC'
assert len(final_theme)==32
final_base=[lead(final_theme,octave=6,velocity=5,gate=2)]+harmony(repeat=2)
VARIANTS={
3:[('rests',[lead('C.D.G.E.')],32,False),('accents',[track('85a585a5',field='velocity',label='ACCENTS')],32,False)],
4:[('intervals',[lead('CDCECGCJ')],32,False),('octaves',[lead('CJCJCJCJ')],32,False)],
5:[('major',[lead('CDEFGABJ')],32,False),('minor',[lead('CDdFGgaJ')],32,False)],
6:[('major-chord',[track(n,step=16,octave=4,velocity=4,gate=12,label=l) for n,l in zip('CEG',['ROOT','THIRD','FIFTH'])],32,False),('minor-chord',[track(n,step=16,octave=4,velocity=4,gate=12,label=l) for n,l in zip('CdG',['ROOT','THIRD','FIFTH'])],32,False)],
7:[('progression',harmony(),64,False),('reordered',harmony('JMAN','EACB','GJEK'),64,False)],
8:[('phrase',[lead(phrase)],64,False),('phrase-variant',[lead('CDEGEGGJCDEGGEDC')],64,False)],
9:[('lead-only',base,64,False),('arranged',arranged,64,False)],
10:[('calm',arranged,64,True),('battle',arranged+drums(),64,True)],
11:[('tail-export',arranged,64,False),('loop-export',arranged,64,True)],
12:[('final-calm',final_base,128,True),('final-battle',final_base+drums(),128,True)],
}
def filename(n,slug):return f'{n:04d}-{slug}.html'
ALL={1:'0001-pulse-and-density.html',2:'0002-four-note-motif.html',**{i['n']:filename(i['n'],i['slug']) for i in LESSONS}}
def esc(text):return html.escape(str(text),quote=True)
def source_links(keys):return '<ol>'+''.join(f'<li><a href="{url}">{esc(label)}</a></li>' for label,url in (SOURCES[key] for key in keys))+'</ol>'
def state_lab(n,variants):
    first,second=variants
    return f'''<div class="panel state-lab" data-state-lab data-bpm="90" data-calm="../audio/{first['audio']}" data-battle="../audio/{second['audio']}"><p class="meta">共享时间线 · 每小节四拍 · 90 BPM</p><div class="controls"><button type="button" data-state-toggle>启动场景试听</button><button type="button" data-state="calm" aria-pressed="true">探索</button><button type="button" data-state="battle" aria-pressed="false">遇敌</button></div><div class="state-stage"><span data-state-scene>旧城高架花园 · 探索</span><div class="bar-progress"><span data-state-progress></span></div></div><p data-state-status role="status" aria-live="polite">启动后选择状态；变化会排到下一个小节。</p><p class="meta">此互动需要通过本地网页服务打开。单独的音频播放器可离线使用。</p></div>'''

def reference(item,variants):
    n=item['n'];name=filename(n,item['slug'])
    terms=''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a,b in item['terms'])
    tables=[]
    for v in variants:
        rows=''.join(f'<tr><td>{esc(t["label"])}</td><td><code>{esc(t["notes"])}</code></td><td>{t["step"]}</td><td>{t["octave"]}</td><td>{t["velocity"]}</td><td>{t["gate"]}</td><td>{t["channel"]}</td></tr>' for t in v['tracks'])
        tables.append(f'<h3>{esc(v["title"])}</h3><div class="table-scroll"><table class="terms"><thead><tr><th>轨道</th><th>T 后数据</th><th>步长/帧</th><th>音区</th><th>力度格</th><th>门长/帧</th><th>MIDI 通道</th></tr></thead><tbody>{rows}</tbody></table></div>')
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(item['title'])} · 速查</title><link rel="stylesheet" href="../assets/course.css"></head><body><main><nav><a href="../lessons/{name}">回到第 {n} 课</a><a href="glossary.html">总速查</a></nav><p class="eyebrow">ORCA / REFERENCE {n:02d}</p><h1>{esc(item['title'])}</h1><section><h2>词汇</h2><table class="terms"><tbody>{terms}</tbody></table></section><section><h2>逐轨参数</h2><p>每帧时长为 60 ÷ BPM ÷ 4 秒。音区按终端 Orca 解释，延伸音名见总速查。参数按生成网格与终端 VM 输出核对。</p>{''.join(tables)}</section><section><h2>编辑位置</h2><p>{esc(item['edit'])}</p><p><a href="../manifests/course.json">文件与音频清单</a>记录各示例的长度、事件数及音源。</p></section><section class="sources"><h2>资料</h2>{source_links(item['sources'])}</section><footer class="footer"><a href="../lessons/{name}">回到练习</a></footer></main></body></html>'''

def lesson_page(item,variants):
    n=item['n'];name=filename(n,item['slug']);prev=ALL[n-1]
    nxt=f'<a href="{ALL[n+1]}">下一课</a>' if n<12 else '<a href="../index.html">回目录</a>'
    knowledge=''.join(f'<h3>{esc(title)}</h3><p>{esc(body)}</p>' for title,body in item['knowledge'])
    previews=''.join(f'''<div class="audio-card"><h3>{esc(v['title'])}</h3><audio controls preload="none" {'loop' if n>=10 else ''} src="../audio/{v['audio']}"></audio><p class="meta"><a href="../patterns/{v['pattern']}" download>下载 Orca 网格</a> · <a href="../audio/{v['audio']}" download>下载 WAV</a> · {'循环区间' if v['loop'] else '含释放尾音'} {v['report']['duration']:.3f} 秒</p></div>''' for v in variants)
    state=state_lab(n,variants) if n in (10,12) else ''
    question,answers,correct,feedback=item['quiz']
    quiz=f'''<div class="panel" data-quiz data-correct="{correct}" data-success="{esc(feedback)}" data-retry="先回到上方说明或试听，控制其他变量，再比较一次。"><p>{esc(question)}</p><div class="controls">{''.join(f'<button type="button" data-answer="{i}">{esc(answer)}</button>' for i,answer in enumerate(answers))}</div><p class="feedback" data-feedback role="status" aria-live="polite">先凭记忆作答，选择后即时反馈。</p></div>'''
    steps='<ol>'+''.join(f'<li>{esc(step)}</li>' for step in item['steps'])+'</ol>'
    code=(ROOT/'outputs/patterns'/variants[0]['pattern']).read_text()
    export=''
    if n in (11,12):
        bars=4 if n==11 else 8
        export=f'''<div class="panel"><h3>在仓库根目录导出</h3><pre class="command">python3 scripts/export_orca_audio.py \\\n  outputs/patterns/{variants[0]['pattern']} \\\n  --bars {bars} --bpm 90 --loop \\\n  --output outputs/projects/my-loop.wav</pre><p class="meta">依赖 Orca-c 源码、C 编译器、libfluidsynth 与课程 SoundFont。源码目录可通过 ORCA_SOURCE 指定。</p></div>'''
    project='<p><a href="../projects/final-cue/brief.md">项目简报</a> · <a href="../projects/final-cue/preview.html">独立场景预览</a> · <a href="../projects/final-cue/score.json">交付元数据</a></p>' if n==12 else ''
    outcomes=''.join(f'<label class="check"><input type="checkbox">{esc(text)}</label>' for text in item['rubric'])
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{n:02d} · {esc(item['title'])} | Orca 创作课</title><link rel="stylesheet" href="../assets/course.css"><script src="../assets/course-widgets.js" defer></script></head><body><main><nav><a href="{prev}">上一课</a><a href="../index.html">目录</a><a href="../reference/{name}">速查</a>{nxt}</nav><p class="eyebrow">ORCA / MUSIC FOR GAMES / LESSON {n:02d}</p><h1>{esc(item['title'])}</h1><p class="lede">{esc(item['subtitle'])}</p><p class="meta">约 {item['minutes']} 分钟 · 终端 Orca · GeneralUser GS</p><p class="callout">完成这一课：{esc(item['win'])}</p><div class="rule"></div><section><h2>先回想一个旧问题</h2><p>{esc(item['recall'])}</p></section><section><h2>这次需要的知识</h2>{knowledge}</section><section id="listen"><h2>先试听，再预测</h2><div class="audio-comparison">{previews}</div><p>比较时保持电脑音量不动，先说出关注哪一项，再播放。播放器之间会互相暂停，避免无意叠音。</p>{state}{project}</section><section id="orca"><h2>在终端中练习</h2><p>先保存已有作品；Ctrl+D 或 F1 打开菜单，在 Open... 加载示例，在 Set BPM... 设 90。空格暂停，Ctrl+R 归零，再开始比较。</p>{steps}<p><strong>编辑提示：</strong>{esc(item['edit'])}</p><details><summary>展开第一版完整网格</summary><pre class="patch compact-patch">{esc(code)}</pre></details><p class="meta"># 开头的行是标签。每个标签下有三行控制结构；保留对齐所需的点号。<a href="../reference/{name}">逐轨参数表</a>可随时核对。</p>{export}</section><section><h2>检查理解</h2>{quiz}<details><summary>显示判断方法</summary><p>{esc(feedback)}先预测再验证，检查自己能否应用概念。</p></details></section><section><h2>做一份自己的版本</h2><p>{esc(item['task'])}</p><p>把原版与自己的版本各保存一份。先只改变一个量做比较，再决定是否保留。</p></section><section><h2>自评与复习</h2>{outcomes}<p>隔一段时间再来：先不看网格说出做法，再打开文件核对。向老师反馈“我改了哪一格、预期怎样、实际听见怎样”，或直接追问不清楚的概念。勾选与答案不会自动变成学习记录。</p></section><section class="sources"><h2>继续阅读</h2>{source_links(item['sources'])}<p>理论定义参考以上一手教材；配乐取舍是练习方案，音频与帧数由脚本实际生成和检查。</p></section><footer class="footer"><a href="{prev}">上一课</a> · {nxt} · <a href="../reference/glossary.html">全课程总速查</a></footer></main></body></html>'''

def build(render_audio=True,start=3):
    (ROOT/'outputs/manifests').mkdir(exist_ok=True)
    manifest={'bpm':90,'beats_per_bar':4,'sample_rate':48000,'source_profile':'../assets/course-sound.json','lessons':[]}
    for item in LESSONS:
        n=item['n'];variants=[]
        for title,key in item['variants']:
            _,tracks,frames,loop=next(v for v in VARIANTS[n] if v[0]==key)
            pattern=f'{n:02d}-{key}.orca';audio=f'{n:02d}-{key}.wav'
            path=save_pattern(pattern,tracks)
            verify(path,tracks,frames*2)
            if render_audio and n>=start:
                report=render_pattern(path,tracks,frames,audio,loop)
                (ROOT/'work'/f'{n:02d}-{key}-report.json').write_text(json.dumps(report))
            else:report=json.loads((ROOT/'work'/f'{n:02d}-{key}-report.json').read_text())
            variants.append(dict(title=title,id=key,tracks=tracks,frames=frames,loop=loop,pattern=pattern,audio=audio,report=report))
        name=filename(n,item['slug'])
        (ROOT/'outputs/lessons'/name).write_text(lesson_page(item,variants))
        (ROOT/'outputs/reference'/name).write_text(reference(item,variants))
        manifest['lessons'].append(dict(number=n,title=item['title'],page='lessons/'+name,variants=variants))
        print(f'Lesson {n:02d}: {item["title"]} · 2 patterns and previews verified',flush=True)
    (ROOT/'outputs/manifests/course.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--pages-only',action='store_true');parser.add_argument('--start',type=int,default=3);args=parser.parse_args()
    build(not args.pages_only,args.start)
