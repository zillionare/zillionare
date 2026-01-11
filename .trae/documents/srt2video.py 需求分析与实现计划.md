## 新增约束：HTML 端依赖全部使用 CDN
- animate.css 等前端依赖不打包、不要求用户本地提供。
- 代价：运行时需要可访问外网 CDN；否则脚本应明确报错。

## 依赖清单（最终版）
- Python：`playwright` + Chromium（由用户安装）。
- CLI：`fire`（仓库已依赖）。
- 配置：`pyyaml`（仓库已依赖）。
- 合成音频：`ffmpeg`（把录屏 webm 与 mp3 合成 mp4）。
- 网络：可访问 CDN（用于加载 animate.css）。

## HTML/CDN 方案设计
### 1) animate.css 通过 CDN 引入
- HTML 里使用：
  - `https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css`

### 2) 动画名全集的获取（保证“所有效果都实现”）
- 因为 CDN 的跨域样式在浏览器里无法读取 `cssRules`（受同源策略限制），所以**不在浏览器里解析动画列表**。
- 改为在 Python 侧：
  - 用 `requests.get(CDN_URL)` 下载 `animate.min.css` 文本
  - 正则提取所有 `.animate__<name>` 的 `<name>`（去重并过滤基础类）
  - 退出动画集合：从上述集合中筛选 `name` 包含 `Out` 或等于 `hinge` 等。

## 字幕展示规则（按你最新要求）
- 新字幕：随机位置出现（但严格避开 profile 区域）。
- 老字幕：不整体上移；当需要移除时用随机退出动画。
- 同屏最多 5 条：超过 5 条时，对最早的一条触发随机退出动画并删除。

## 随机位置与避让 profile 的实现
- Python 根据 YAML 计算 profile 显示矩形（W×H + 九宫格位置 + size 缩放）。
- 页面渲染时：
  - 新字幕节点先渲染到隐藏层测量宽高
  - 在可用区域内随机采样 (x,y)，保证字幕矩形不与 profile 矩形相交（含 margin）
  - （可选）尽量避免与现有字幕矩形相交；多次尝试失败后允许与字幕重叠，但仍不碰 profile。

## profile 资源处理（避免本地静态资源依赖）
- profile 图片读取后转为 **data URL（base64）** 直接内嵌进 HTML。
- 这样你用 `file://index.html` 或调试目录打开都不会缺图。

## 调试输出（你提出的“生成 HTML”）
- 增加 `--debug_dir`：输出并保留：
  - `index.html`（引用 animate.css CDN）
  - `timeline.json`（字幕时间轴与每条字幕选中的入场/退场动画名）
- 你可以直接打开 `index.html` 做肉眼调试。

## CLI（fire）
- `main(audio: str, *srts: str, config: str = "srt2video.yaml", out: str | None = None, seed: int | None = None, debug_dir: str | None = None)`
- 默认输出：音频同目录同名 `.mp4`。

## 渲染与合成流程
1. 读取 YAML → 计算 W×H、profile 区域。
2. 解析/合并 SRT → 生成 timeline。
3. 拉取 animate.css（CDN）→ 解析动画名全集 → 为每条字幕分配入场/退场动画。
4. 生成 HTML（临时目录或 debug_dir）。
5. Playwright 打开 HTML 并录屏（时长≈音频或最后字幕结束）。
6. ffmpeg：webm + mp3 → mp4。

## 验收标准
- 任意时刻字幕 ≤ 5。
- 新字幕随机位置出现且不覆盖 profile。
- 移除字幕时随机退出动画后消失。
- 输出 mp4 含音轨，字幕与 srt 时间同步。

确认后我将开始实现 `scripts/srt2video.py`（只新增这一文件）。