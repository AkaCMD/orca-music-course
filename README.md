# Orca 原创音乐与游戏配乐：完整基础课程

12 课中文课程，面向乐理与 Orca 零基础学习者。使用终端 Orca，从一个音开始，完成一个八小节、探索与遇敌双状态的原创游戏配乐小项目。

## Orca 简介

[Orca](https://github.com/hundredrabbits/Orca) 是一种用二维字符网格编程的语言与实时编辑环境，常用于创作音序。网格里的字符可以负责计数、触发、选音等操作；程序按帧推进，让这些操作组合成循环或持续变化的音乐规则。你可以在运行时修改网格，边听边调整。

Orca 可以通过 MIDI、OSC 和 UDP 向音频或视觉软件发送指令，实际声音由连接的合成器或采样器产生。本课程使用的发声链是：

```text
Orca 网格 → MIDI 音符 → FluidSynth + GeneralUser GS 音源 → 声音
```

本课程使用 C 语言实现的终端版 [Orca-c](https://github.com/hundredrabbits/Orca-c)。我们通过修改少量字符，对照节奏、音高、和弦与编配的变化，把乐理概念变成能听见、能重复的实验。音源与导出设置见下方「音源与导出」。

## 开始学习

打开 [课程目录](outputs/index.html)。全部课程可直接阅读，每课包含理论说明、对照试听、可运行网格、实际改写任务、即时答题反馈与可打印速查。

| 课 | 内容 | 可观察的成果 |
| --- | --- | --- |
| 1 | [拍子与音符密度](outputs/lessons/0001-pulse-and-density.html) | 保持 BPM，改变触发密度 |
| 2 | [四音动机](outputs/lessons/0002-four-note-motif.html) | 写出自己的四音循环 |
| 3 | [节奏、休止与力度](outputs/lessons/0003-rhythm-and-space.html) | 写出留白与重音 |
| 4 | [音程与八度](outputs/lessons/0004-intervals-and-octaves.html) | 比较小步移动与跳进 |
| 5 | [大调与自然小调](outputs/lessons/0005-major-and-minor.html) | 用限定音集写两版动机 |
| 6 | [三和弦](outputs/lessons/0006-building-triads.html) | 同时发出并转换大、小三和弦 |
| 7 | [和声与低音](outputs/lessons/0007-harmony-and-bass.html) | 改写四小节和弦进行 |
| 8 | [乐句与变化](outputs/lessons/0008-phrases-and-variation.html) | 从动机发展出四小节旋律 |
| 9 | [音区与编配](outputs/lessons/0009-register-and-arrangement.html) | 分清主旋律与背景 |
| 10 | [游戏状态配乐](outputs/lessons/0010-music-and-game-states.html) | 按小节切换探索与遇敌 |
| 11 | [循环音频导出](outputs/lessons/0011-exporting-loops.html) | 导出定长 WAV 并检查接缝 |
| 12 | [结业配乐项目](outputs/lessons/0012-final-game-cue.html) | 交付自己的八小节双状态作品 |

普通讲义、音频和答题可离线打开。[第 10、12 课的状态切换预览](outputs/projects/final-cue/preview.html)需要本地网页服务。在仓库根目录运行：

```sh
python3 -m http.server 18765 --bind 127.0.0.1 --directory outputs
```

浏览器访问 `http://127.0.0.1:18765/index.html`。如该端口已有课程服务，可直接打开地址。[完整课程 ZIP](outputs/orca-music-course-complete.zip)包含讲义、试听、网格、速查、源码与项目示范。

## 在终端中播放

```sh
orca --bpm 90 outputs/patterns/12-final-calm.orca
```

操作按 Orca-c 终端版编写：Ctrl+D 或 F1 打开菜单，空格播放或暂停，Ctrl+R 归零，Ctrl+S 保存。5C 对应 MIDI 60；其他版本的音区编号与快捷键需要另行核对。

## 音源与导出

课程基础音色是 GeneralUser GS 的 Saw Lead，bank 0、program 81、MIDI 通道 0。鼓轨使用同一 SoundFont 的通道 9 鼓组。[course-sound.json](outputs/assets/course-sound.json)保存效果与渲染参数。SoundFont 本体单独安装，本仓库包含课程使用的短音频渲染。来源：[GeneralUser GS 作者页面](https://schristiancollins.com/generaluser.php)。

导出自己的八小节循环：

```sh
python3 scripts/export_orca_audio.py outputs/patterns/12-final-calm.orca \
  --bars 8 --bpm 90 --loop --output outputs/projects/my-loop.wav
```

工具需要 Python 3、libfluidsynth、C 编译器、Orca-c 源码和本地 SoundFont。默认读取 `~/orca-src` 与 `~/.local/share/soundfonts/GeneralUser-GS.sf2`，可通过 `ORCA_SOURCE`、`ORCA_SOUNDFONT_DIR` 指定目录。工具按 profile 中记录的 SoundFont 校验和核对音源。更换音源版本时应更新 profile 并重新渲染试听。工具合成 MIDI 音符，不录制外部硬件或 OSC 效果。循环模式检查连续三个周期的音符序列，并检查输出边界；更复杂的持续演变程序仍需自己确认循环区间。

重新生成第 3-12 课的网格、音频与页面：

```sh
python3 scripts/build_full_course.py
python3 scripts/finish_course.py
python3 scripts/verify_course.py
python3 scripts/package_course.py
```

[构建验证清单](outputs/manifests/course.json)记录每个示例的 MIDI 事件数、音频长度、峰值和循环边界数据。测量不能替代对画面、乐句与听感的判断。

## 课程源文件与学习状态

[course/lessons.py](course/lessons.py)保存第 3-12 课的内容；生成页面位于 `outputs/lessons`，速查位于 `outputs/reference`，网格位于 `outputs/patterns`，试听位于 `outputs/audio`。根目录 `lessons`、`reference`、`assets` 是对应目录的符号链接。

[MISSION.md](MISSION.md)保存目标，[RESOURCES.md](RESOURCES.md)保存资料，[learning-records](learning-records)只记录已展示的理解，[NOTES.md](NOTES.md)保存偏好和工作说明。整套教材已提供，不代表学习者已经完成所有练习。
