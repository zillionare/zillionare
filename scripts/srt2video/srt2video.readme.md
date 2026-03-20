1. 新建 conda 环境
2. 安装依赖

```bash
pip install playwright && playwright install chromium
pip install fire pyyaml loguru 
```

## 运行和调试

脚本有很多选项，可以修改它们以查看效果。此时应该使用调试模式 -- 这将跳过视频生成，只生成一个 html 文件，打开该文件就可以看到动画效果。这种模式速度非常快。

调试命令是：

```bash
cd path/to/srt2video
python srt2video.py short.srt --html-only --debug-dir /tmp/test
```

对效果满意后，可以运行以下命令生成视频：

```bash
cd path/to/srt2video

# 在目录中已经有 short.mp3和short.srt 文件供演示
# 正式使用时填写真实的文件名
python srt2video.py short.mp3 short.srt
```

## 配置

### 视频长宽比
配置文件与脚本在同一目录，是一个 yaml 格式的文件。

不同平台要求的视频长宽比不一样。因此，脚本允许为每一个平台生成不同长宽比的视频。

视频号倾向的视频是6/7，为保证图像清晰，我们可以将 width 和 height 设置为1200/1400。

### 头像闪烁效果

```yaml
profile_animation_enabled: true      # 是否开启透明度闪烁动画
profile_animation_duration_ms: 3000   # 动画时长（3秒一个周期，会比之前慢很多）
```

动画时间可能长一些更好，太短了可能让人心烦。

背景图版在 background 中指定。

## 字幕
以下配置指定字幕的动画时长、色彩、字体、显示位置和最大长度。
```yaml
subtitle_animation_duration_ms: 600
colors:
  - F7D757
  - ED705E
  - 4F7EF6
  - FEFEFE
font: 庞门正道标题体免费版.ttf # 可使用绝对路径。如果是相对路径，则从当前目录开始搜索。
subtitle_random_color: true
y_min: 0.5 # 字幕出现的最小 Y 坐标百分比 (0.0 - 1.0)
y_max: 0.9 # 字幕出现的最大 Y 坐标百分比 (0.0 - 1.0)
max_words_per_line: 7 # 长字幕自动拆分的最大词数
```

### 背景音乐

```yaml
bgm:
    path: bgm.mp3 # 可使用绝对路径。如果是相对路径，则从当前目录开始搜索。
    volume: 0.2 # 0~1之间，原音量的倍数
    start: 5 # 从第5秒起添加
```

设置背景音乐从第 x秒起，以防和开场音乐冲突。另外，bgm 很难与主音频同步，此时会让 bgm 无限循环，只到主音频结束。

