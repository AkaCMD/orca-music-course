"""Build the course index, reference, and final-project delivery materials."""
from pathlib import Path
import html
import importlib.util
import json
from build_full_course import ALL,LESSONS,SOURCES
from pattern_engine import ROOT

O=ROOT/'outputs'
items=[dict(n=1,title='让一个音成为循环',win='拍子、速度与音符密度',minutes=8),dict(n=2,title='写下第一个四音动机',win='音高顺序、上行与下行',minutes=10)]+LESSONS
cards=[]
for item in items:
    n=item['n']
    cards.append(f'<a class="lesson-card" href="lessons/{ALL[n]}"><span class="eyebrow">LESSON {n:02d} · {item["minutes"]} MIN</span><strong>{html.escape(item["title"])}</strong><p>{html.escape(item["win"])}</p></a>')
index='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>完整课程 · Orca 原创音乐与游戏配乐</title><link rel="stylesheet" href="assets/course.css"></head><body><main><nav><a href="#lessons">12 课目录</a><a href="reference/glossary.html">总速查</a><a href="projects/final-cue/preview.html">结业作品试听</a><a href="orca-music-course-complete.zip" download>下载完整课程</a></nav><p class="eyebrow">ORCA / ORIGINAL MUSIC & GAME SCORING</p><h1>从第一个音，<br>写到一个游戏场景。</h1><p class="lede">12 课中文基础课程。用终端 Orca 学乐理，完成一个包含探索与遇敌状态的原创配乐小项目。</p><p class="meta">全部课程开放 · 示例使用 GeneralUser GS · 每课含试听、网格、练习与速查</p><div class="rule"></div><section><h2>从声音走到作品</h2><p>第 1至4 课控制拍子、音高与距离；第 5至8 课组织音阶、和声与乐句；第 9至12 课安排层次、响应游戏状态并导出循环。</p><p>每次先预测、再试听，只改一个变量做对照。你可以先读完全部课程，再分次实际练习；看到答案不等于已经掌握，记录自己能独立完成的动作。</p><p class="callout">当前仍使用终端 Orca。音区编号按终端版本解释，5C 对应 MIDI 60。桌面版的快捷键与音区编号不要直接套用。</p></section><section id="lessons"><h2>完整课程</h2><div class="curriculum">'''+''.join(cards)+'''</div></section><section><h2>带走一份作品</h2><p>结业示例“旧城高架花园”包含 8 小节探索、遇敌两版。先用互动预览理解切换，再改写自己的主题和结构。</p><p><a href="projects/final-cue/preview.html">打开双状态场景试听</a> · <a href="projects/final-cue/brief.md">项目简报</a> · <a href="manifests/course.json">示例与音频清单</a></p></section><section><h2>使用方式</h2><p>普通课程的讲义、音频和答题可离线打开。第 10、12 课的状态切换预览需要本地网页服务；在仓库根目录运行以下命令，再打开浏览器中的地址。</p><pre class="command">python3 -m http.server 18765 --bind 127.0.0.1 --directory outputs
http://127.0.0.1:18765/index.html</pre><p>音频导出方法在第 11 课。遇到疑问，回到聊天告诉老师你正在第几课、改了哪一格，以及预期和实际听感。</p></section><footer class="footer"><a href="reference/glossary.html">音名、参数与乐理总速查</a> · <a href="https://github.com/AkaCMD/orca-music-course">GitHub 仓库</a></footer></main></body></html>'''
(O/'index.html').write_text(index)
terms=[('拍 / BPM','拍是计数单位；BPM 是每分钟拍数。'),('帧 / 门长','本课程每拍 4 帧；门长控制音符保持帧数。'),('音高 / 音区','音高的高低与所在范围；音区变化不改变 BPM。'),('半音 / 八度','相邻 MIDI 编号相差一半音；同名音相差八度为 12 半音。'),('音程','两个音高的距离；本课常用 C-E 大三度与 C-G 纯五度。'),('主音 / 音阶','围绕的中心音，以及按一定关系排列的音集。'),('动机 / 变化','短小可辨认的音乐想法，以及保留特征的改写。'),('三和弦','三音结构；大三和弦 0-4-7，小三和弦 0-3-7。'),('和弦进行','和弦出现的顺序；本课示例 C-Am-F-G。'),('编配','安排不同音乐层的角色、音区、力度与时间位置。'),('状态 / 边界','游戏处境与允许音乐变化的拍、小节或乐句位置。'),('循环 / 交付','准确重复的音乐区间，以及可编辑网格、音频和元数据。')]
notes=[('C','C','60'),('c','C♯','61'),('D','D','62'),('d','D♯ / E♭','63'),('E','E','64'),('F','F','65'),('f','F♯','66'),('G','G','67'),('g','G♯ / A♭','68'),('A / H','A','69'),('a / h','A♯ / B♭','70'),('B / I','B','71'),('J','下一音区 C','72'),('K','下一音区 D','74'),('L','下一音区 E','76'),('M','下一音区 F','77'),('N','下一音区 G','79'),('O','下一音区 A','81')]
refs=''.join(f'<li><a href="{url}">{html.escape(title)}</a></li>' for title,url in SOURCES.values())
glossary=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>全课程总速查</title><link rel="stylesheet" href="../assets/course.css"></head><body><main><nav><a href="../index.html">课程目录</a></nav><p class="eyebrow">ORCA / DESK REFERENCE</p><h1>声音、代码与时间。</h1><section><h2>常用词</h2><table class="terms"><tbody>{''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a,b in terms)}</tbody></table></section><section><h2>本课拍号与音值</h2><p>4/4 表示每小节四个四分音符的时值，本课以四分音符为一拍。四分音符为 1 拍，八分音符为半拍，十六分音符为四分之一拍，二分音符为 2 拍，全音符为 4 拍。对应休止也按同样时长计数。MIDI 门长与起音间隔分开控制，不能仅凭 D4 就认定声音持续了一整拍。</p></section><section><h2>终端版音名</h2><p>表中 MIDI 编号按音区 5。换音区时，每增加 1，加 12。小写音名升半音；字母作为运算符与数据时的用途由所在端口决定。</p><table class="terms"><thead><tr><th>Orca 字符</th><th>发声</th><th>MIDI</th></tr></thead><tbody>{''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in notes)}</tbody></table><p>终端 5C = MIDI 60，常见科学音高记法把 MIDI 60 记为 C4。完整乐理分析中仍使用符合音阶结构的升降记号。</p></section><section><h2>数字与运算符</h2><p>Orca 使用 36 进制单字符数值：a=10，c=12，g=16，w=32。大写字母在数值端口也可转换为相应数值，但音名端口有自己的含义。</p><table class="terms"><tbody><tr><td>D4</td><td>左侧留空时，每 4 帧输出触发。</td></tr><tr><td>4C4</td><td>每 4 帧推进一次 0、1、2、3 的循环计数。</td></tr><tr><td>04TCDEG</td><td>T 读取左侧两格的计数与长度，从右侧表选一个字符输出到下方。</td></tr><tr><td>:05C81</td><td>MIDI 通道 0、音区 5、音名 C、力度 8、门长 1 帧。</td></tr><tr><td>#LABEL</td><td>整行注释标签。</td></tr><tr><td>MIDI 通道 9</td><td>通常称第 10 通道，本课使用 GeneralUser GS 鼓组。</td></tr></tbody></table></section><section><h2>四个常用和弦</h2><table class="terms"><thead><tr><th>和弦</th><th>组成音</th><th>C 大调内级数</th></tr></thead><tbody><tr><td>C</td><td>C E G</td><td>I</td></tr><tr><td>Am</td><td>A C E</td><td>vi</td></tr><tr><td>F</td><td>F A C</td><td>IV</td></tr><tr><td>G</td><td>G B D</td><td>V</td></tr></tbody></table></section><section><h2>循环长度公式</h2><p>秒数 = 小节数 × 每小节拍数 × 60 ÷ BPM。采样帧数 = 秒数 × 采样率；若结果不是整数，导出时需要明确取整，重新核对边界。</p><p>本课 90 BPM、每小节四拍、48 kHz：4 小节为 512000 帧，8 小节为 1024000 帧。MIDI 网格本身不保存课程的 BPM 设置。</p></section><section><h2>终端操作</h2><p>Ctrl+D 或 F1 打开菜单，Open... 打开文件，Set BPM... 设速度，MIDI Output... 选音源。空格播放或暂停，Ctrl+R 归零，Ctrl+S 保存。</p></section><section class="sources"><h2>主要来源</h2><ol>{refs}</ol><p>具体代码映射与示例事件来自本地 Orca-c 源码及 VM 验证。</p></section></main></body></html>'''
(O/'reference/glossary.html').write_text(glossary)
project=O/'projects/final-cue';project.mkdir(parents=True,exist_ok=True)
(project/'brief.md').write_text('''# 旧城高架花园：八小节双状态配乐

## 场景
角色穿过被植物覆盖的旧城高架。探索时需要持续行走和观察；遇敌时需要更明确的行动脉冲。两版共用地点主题。

## 音乐约定
- 90 BPM，4/4，8 小节。
- 以 C 大调为音集，和弦 C-Am-F-G 重复两次。
- 主旋律、低音与三条和弦声部共用；遇敌版加入大鼓、军鼓与踩镲。
- GeneralUser GS，旋律通道 0 的 Saw Lead，通道 9 的鼓组。
- 48 kHz、16-bit、立体声；每版循环 1024000 个采样帧。

## 状态约定
探索与遇敌共用播放起点。收到状态请求后，在下一个小节边界切换，预览采用 40 ms 淡变。实际游戏应根据目标引擎的音频调度接口实现并重新测试。

## 修改要求
至少改写主旋律的两个小节，或做一次清楚可解释的材料结构变化。保留原版供对照。两版共同部分保持一致，允许独立设计鼓层。

## 自评
1. 能跟唱或用手势记住主题。
2. 能指出每一音乐层的用途。
3. 两版长度、拍点、和声位置相容。
4. 连续听三轮没有额外拖拍，能双向切换状态。
5. 交付自己的网格、音频与状态说明，并记录一次具体修改。
''')
manifest=json.loads((O/'manifests/course.json').read_text())
final=manifest['lessons'][-1]['variants']
score=dict(title='旧城高架花园',bpm=90,beats_per_bar=4,bars=8,key='C major',sample_rate=48000,sample_frames=1024000,transition='next bar, 40 ms fade',soundfont='GeneralUser-GS.sf2',states={v['id']:dict(audio='../../audio/'+v['audio'],pattern='../../patterns/'+v['pattern'],report=v['report']) for v in final})
(project/'score.json').write_text(json.dumps(score,ensure_ascii=False,indent=2)+'\n')
from build_full_course import state_lab
lab=state_lab(12,final).replace('../audio/','../../audio/')
preview='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>旧城高架花园 · 配乐预览</title><link rel="stylesheet" href="../../assets/course.css"><script src="../../assets/course-widgets.js" defer></script></head><body><main><nav><a href="../../lessons/0012-final-game-cue.html">第 12 课</a><a href="brief.md">简报</a><a href="score.json">交付元数据</a></nav><p class="eyebrow">FINAL CUE / INTERACTIVE PREVIEW</p><h1>旧城高架花园</h1><p class="lede">同一个地点主题，从探索进入遇敌，再回到探索。先听完整一轮，再比较状态变化。</p>'''+lab+'''<section><h2>直接试听或下载</h2><p>探索版</p><audio controls loop src="../../audio/12-final-calm.wav"></audio><p>遇敌版</p><audio controls loop src="../../audio/12-final-battle.wav"></audio></section><footer class="footer">这是课程示范作品。按第 12 课要求改写主题或结构，完成自己的版本。</footer></main></body></html>'''
(project/'preview.html').write_text(preview)
# Join the previously authored second lesson to the complete sequence.
p=O/'lessons/0002-four-note-motif.html';s=p.read_text()
if '0003-rhythm-and-space.html' not in s:s=s.replace('<footer class="footer">','<footer class="footer"><a href="0003-rhythm-and-space.html">下一课：节奏与留白</a> · ',1)
p.write_text(s)
for path in [O/'patterns/05-rhythm-rests.orca',O/'patterns/05-rhythm-accents.orca']:
    if path.exists():path.unlink()
print('Index, glossary, and final cue project generated.')
