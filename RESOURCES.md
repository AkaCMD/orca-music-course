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

## Gaps

- 尚未确定用户喜欢的游戏、作曲家与目标场景。
- 尚需为后续音高、和声与游戏音频导出课程补充相应的一手教材。
- 作者网站 https://100r.co/site/orca.html 被本次网页工具的 robots 访问规则阻止；使用作者的官方 GitHub 资料交叉核对。
