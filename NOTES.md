# 教学工作笔记

用户目标：自己创作和给游戏配乐。用户自报乐理与 Orca 都是零基础。

Kind: descriptive | Audience: 中文零基础学习者 | Purpose: 以音高顺序写出一个四音循环 | Non-goals: 第二课不要求完整音阶、和声或从零重建计数器。

工作区的 lessons、assets、reference 是指向 outputs 内相应目录的符号链接。用户交付文件统一位于 outputs。共享样式与交互组件分别由 assets/course.css、assets/pulse-lab.js 管理。

本地发现终端版与 Electron 桌面版。讲义快捷键针对终端版；不向正在运行的网格注入内容。系统已有 FluidSynth 会话，当前终端 Orca 已连接其 MIDI 端口；这不代表已确认扬声器实际发声。

2026-10-25 核对本地来源：~/.local/bin/orca-synth、~/.local/opt/orca-desktop/app/sources/scripts/core/library.js、clock.js、client.js。第一课以终端版内部时钟为准，每拍 4 帧。不要把 Orca 的音区编号直接称为其他软件的八度编号。

后续教学建议：确认第一课实际听见声音与预测结果，再依次引入音高与音程、短旋律动机、低音与和弦、乐句和循环、场景的配器与层次。顺序可根据用户反馈调整。不要一次生成整套课程。

课程统一音源：GeneralUser-GS.sf2，bank 0、program 81，实际预置名 Saw Lead；MIDI 通道 0。用户偏好适合合成器音乐且比简单三角波丰满的音色。网页以同一 FluidSynth 引擎、SoundFont 与效果设置生成的单音样本试听，保留 MIDI 60、velocity 63、90 BPM、门长 1 帧。共享 profile 为 outputs/assets/course-sound.json，生成器为 work/render_course_synth.py。两个本地 Orca 启动器读取 ~/.local/share/orca/course-synth-settings.sh，来源是同一个 profile。后续课程增添音高或时值时，须从相同 profile 生成对应样本，不能简单移调这个短音样本来冒充其他 MIDI 事件。作答反馈由页面即时显示，但不会自动同步到学习记录。

只有用户展示理解后，才记录已掌握内容。未设置任何自动提醒。

交付验证：work/verify-course.cjs 使用本地桌面版核心执行两个网格，各运行 32 帧。D4 在 0,4,...,28 产生 8 条 MIDI 事件；D2 在 0,2,...,30 产生 16 条。两者参数均为 [0,5,C,8,1]；终端映射为 MIDI 60。本地文件链接存在，交互脚本语法检查通过。浏览器中实际点击验证开始、切换 D2、停止与正确答案反馈；随后恢复初始状态。未验证扬声器声压或用户的听觉结果。

用户确认使用终端 Orca，要求终端和课程统一为适合合成器音乐的音源。current.sf2 指向 GeneralUser-GS.sf2，课程预置在 ~/.local/share/orca/course-synth-presets.txt。保留旧音源文件；工作脚本备份在 work/audio-backup/synth-course/。

纠正音高编号：本地 tui_main.c 的 MIDI 音高为 octave*12+note，故终端 3C 为 MIDI 36，5C 为 MIDI 60。网页试听维持原来的约 261.626 Hz，教材和练习文件统一使用 :05C81。旧 :03C81 示例属于桌面版映射，不应继续用于终端课。

课程效果设置：gain 0.6、48 kHz，关闭合唱、开启轻混响，参数由共享 profile 保存。网页样本不另加合成器滤镜或包络。单音峰值约 0.053，旋律和和弦示例峰值约 0.083，离线音频未削波。三角波的旧生成器和音源文件仅保留作可回退资产，不再作为当前课程音源。用户已在回忆题中正确辨认固定 BPM 下的密度变化，见 learning-records/0002-density-and-next-step.md。音高顺序的掌握仍待第二课反馈。

教材的正式位置是 /home/cmd/git-repos/orca-music-course，GitHub 目标为 AkaCMD/orca-music-course，私有。旧聊天工作区的 outputs、MISSION.md、RESOURCES.md、NOTES.md、learning-records 保留符号链接指向这里，后续编辑应使用正式仓库路径。不要在旧工作区另外生成一份教材。

第二课使用 outputs/patterns/03-four-note-melody.orca 与 04-descending-melody.orca。终端源码验证 32 帧产生两遍 MIDI 60,62,64,67 或反向序列，间隔为 4 帧、velocity 63、duration 1。追踪器源文件为 scripts/trace_orca_notes.c。音频生成器为 scripts/render_lesson2_audio.py，共享 FluidSynth 渲染函数为 scripts/course_audio.py。四个音分别渲染，未通过移调一个样本冒充其他音高。

第二课浏览器验证：四音样本成功解码并播放；选择 GEDC 后网格和四个选单一致，改末音为 G 后得到 GEDG；正确答案的即时反馈已验证。页面测试不代表学习者已掌握第二课。
