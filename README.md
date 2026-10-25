# Orca 原创音乐与游戏配乐

面向乐理与 Orca 零基础学习者的中文课程。使用终端 Orca，为游戏场景创作短小的原创循环。

## 开始学习

用浏览器打开 [课程目录](outputs/index.html)，每课包含试听、终端练习和可打印的速查。音频随仓库保存，网页可离线使用。

1. [第一课：让一个音成为循环](outputs/lessons/0001-pulse-and-density.html)，学习拍子与音符密度。
2. [第二课：写下第一个四音动机](outputs/lessons/0002-four-note-motif.html)，控制音高的顺序。

在终端播放第二课示例：

```sh
orca --bpm 90 outputs/patterns/03-four-note-melody.orca
```

课程操作按 Orca-c 终端版编写。菜单为 Ctrl + D 或 F1，空格播放或暂停；桌面版的音区编号与快捷键可能不同。

## 音源

课程使用本地安装的 GeneralUser GS SoundFont，基础音色为 bank 0、program 81 的 Saw Lead，MIDI 通道编号为 0。网页音频由相同 SoundFont、预置与效果设置生成。

[course-sound.json](outputs/assets/course-sound.json) 保存统一参数。SoundFont 本体需要单独安装，本仓库提供课程所需的短音频样本。来源：[GeneralUser GS 作者页面](https://schristiancollins.com/generaluser.php)。

如需重新生成第二课音频，需要 Python 3、libfluidsynth，以及本地 `~/.local/share/soundfonts/GeneralUser-GS.sf2`：

```sh
python3 scripts/render_lesson2_audio.py
```

## 学习状态

[MISSION.md](MISSION.md) 保存学习目标，[RESOURCES.md](RESOURCES.md) 保存资料来源，[learning-records](learning-records) 只记录已展示的理解，[NOTES.md](NOTES.md) 保存教学偏好与工作说明。

`outputs/lessons` 是课程，`outputs/reference` 是速查，`outputs/patterns` 是 Orca 示例，`outputs/assets` 是共享样式、试听与交互组件。根目录的 `lessons`、`reference`、`assets` 指向这些目录，便于继续使用 teach 技能维护课程。
