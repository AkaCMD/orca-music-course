# Orca 与音乐基础资源

## Knowledge

- [Orca 官方手册](https://github.com/hundredrabbits/Orca/blob/main/README.md)
  用于核对 Orca 的定位、MIDI 参数与命令。第一课只阅读 Operators 中的 D、* 和 MIDI 部分。
- [Orca 官方运算符实现](https://github.com/hundredrabbits/Orca/blob/main/desktop/sources/scripts/core/library.js)
  用于核对 D 的端口位置及触发间隔。示例程序还应在本地引擎中运行验证。
- [Orca 官方时钟实现](https://github.com/hundredrabbits/Orca/blob/main/desktop/sources/scripts/clock.js)
  用于核对内部时钟的每拍 4 帧关系。外部 MIDI 时钟与具体安装版本应另行核对。
- [Open Music Theory: Meter and time signatures](https://openmusictheory.github.io/meter.html)
  开放乐理教材；用于解释拍的分组与细分。第一课只使用四拍分组这一小部分。

- [Orca-c 终端版作者手册](https://github.com/hundredrabbits/Orca-c)
  用于核对终端版菜单和快捷键。音区编号按本地 tui_main.c 核对，避免套用桌面版映射。

- [GeneralUser GS 作者页面](https://schristiancollins.com/generaluser.php)
  课程当前使用的 SoundFont。实际 bank、预置名和音频按本地安装版本核对。
- [FluidSynth SoundFont 管理文档](https://www.fluidsynth.org/api/group__soundfont__management.html)
  用于加载同一音源并生成网页试听；具体课程参数由 course-sound.json 统一保存。

- [Open Music Theory: Scales and scale degrees](https://openmusictheory.github.io/scales.html)
  用于第二课核对 C 大调音名、音高排列与唱名；只引入四个音，不要求背音阶公式。

- [Robert Hutchinson: Motive](https://musictheory.pugetsound.edu/mt21c/MotiveSection.html)
  University of Puget Sound 乐理教材；用于动机的定义与重复、变化练习。

## Wisdom (Communities)

- [Orca 官方仓库讨论入口](https://github.com/hundredrabbits/Orca#orca)
  作者列出的论坛、聊天室与邮件列表入口。适合日后展示一个短循环并征求具体反馈；目前不要求加入。

## 完整课程追加资料

- [Open Music Theory：时值与休止](https://openmusictheory.github.io/rhythmicValues.html)
  第 3 课的持续时间与休止概念。
- [Open Music Theory：音高与音区](https://openmusictheory.github.io/pitches.html)
  第 4 课的音区与常见科学音高记法，代码映射另按终端源码核对。
- [Open Music Theory：音程](https://openmusictheory.github.io/intervals.html)
  半音计数与音程的级数、性质。
- [Open Music Theory：三和弦](https://openmusictheory.github.io/triads.html)
  第 6、7 课的和弦构成。
- [Open Music Theory：和声功能](https://openmusictheory.github.io/harmonicFunctions.html)
  理解调性语境中的和声位置，避免把某一进行当成通用情绪公式。
- [Ableton Learning Synths：包络](https://learningsynths.ableton.com/en/envelopes/synthesizer-envelopes)
  第 3、9 课的起音、保持与释放，亦可作为课后音色设计练习。网页需要 JavaScript。
- [Audiokinetic：互动音乐中的水平与垂直结构](https://www.audiokinetic.com/download/documents/customer_profiles/MGR_Wwise_BGM_en.pdf)
  游戏状态配乐的组织思路。搜索索引可核对两种结构，本文档下载在本次网页工具中返回 403；课程的具体切换行为以本地实现和测试为准。
- [Godot 官方文档：音频导入与循环](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html)
  第 11、12 课的 WAV 循环导入，可作引擎侧示例；其他引擎需要查其各自文档。

## 仍需学习者补充的背景

具体游戏与参考音乐尚未指定；完整课程使用“旧城高架花园”作示范。后续作品评审应以学习者选择的画面与用途为准。
