"""示例：

python scripts/srt2video.py  /tmp/srt2video_test.mp3 /tmp/srt2video_demo.srt --config scripts/srt2video.yaml

配置文件（保存为 yaml）

width: 720 # 生成的视频宽度
ratio: 9/16 # 生成的视频的长宽比
profile: /tmp/flora-3.jpg # 人物图像
position: top-left # 图像位置
size: 50% # profile 的显示大小
background: /tmp/flora-3.jpg # 背景图或颜色
subtitle_animation_duration_ms: 600
subtitle_random_color: true
y_min: 0.5 # 字幕出现的最小 Y 坐标百分比 (0.0 - 1.0)
y_max: 0.9 # 字幕出现的最大 Y 坐标百分比 (0.0 - 1.0)
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import random
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import fire
import yaml
from loguru import logger

ANIMATE_CSS_CDN = "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"


@dataclass(frozen=True)
class Subtitle:
    start: float
    end: float
    text: str


def _parse_ratio(ratio: str) -> Fraction:
    ratio = str(ratio).strip()
    if "/" in ratio:
        a, b = ratio.split("/", 1)
        return Fraction(int(a.strip()), int(b.strip()))
    if ":" in ratio:
        a, b = ratio.split(":", 1)
        return Fraction(int(a.strip()), int(b.strip()))
    return Fraction(ratio)


def _parse_percent(size: str) -> float:
    raw = str(size).strip()
    if raw.endswith("%"):
        return float(raw[:-1].strip()) / 100.0
    return float(raw)


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("yaml 配置必须是一个 dict")
    return data


def _time_to_seconds(t: str) -> float:
    t = t.strip()
    hh, mm, rest = t.split(":", 2)
    if "," in rest:
        ss, ms = rest.split(",", 1)
    elif "." in rest:
        ss, ms = rest.split(".", 1)
    else:
        ss, ms = rest, "0"
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0


def _parse_srt(path: Path) -> list[tuple[float, float, str]]:
    content = path.read_text(encoding="utf-8-sig", errors="replace")
    blocks = re.split(r"\n\s*\n", content.strip(), flags=re.MULTILINE)
    items: list[tuple[float, float, str]] = []
    for block in blocks:
        lines = [ln.rstrip("\r") for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        time_line = lines[1] if re.search(r"\d+:\d+:\d+", lines[1]) else lines[0]
        m = re.match(
            r"^\s*(\d{2}:\d{2}:\d{2}[,\.]\d{1,3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{1,3})",
            time_line,
        )
        if not m:
            continue
        start = _time_to_seconds(m.group(1))
        end = _time_to_seconds(m.group(2))
        text_lines = lines[2:] if time_line == lines[1] else lines[1:]
        text = "\n".join(text_lines).strip()
        if not text:
            continue
        items.append((start, end, text))
    return items


def _merge_srts(paths: list[Path]) -> list[tuple[float, float, str]]:
    merged: list[tuple[float, float, str]] = []
    for p in paths:
        merged.extend(_parse_srt(p))
    merged.sort(key=lambda x: (x[0], x[1]))
    return merged


def _check_executable(name: str) -> str:
    exe = shutil.which(name)
    if not exe:
        raise RuntimeError(f"未找到可执行文件：{name}")
    return exe


def _ffprobe_duration_seconds(media: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    proc = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(media),
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    out = (proc.stdout or "").strip()
    try:
        return float(out)
    except Exception:
        return None


def _ffprobe_image_size(image: Path) -> tuple[int, int]:
    ffprobe = _check_executable("ffprobe")
    proc = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "json",
            str(image),
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"无法读取图片尺寸：{image}")
    data = json.loads(proc.stdout)
    streams = data.get("streams") or []
    if not streams:
        raise RuntimeError(f"无法读取图片尺寸：{image}")
    w = int(streams[0]["width"])
    h = int(streams[0]["height"])
    return w, h


def _image_to_data_url(image: Path) -> str:
    mime, _ = mimetypes.guess_type(str(image))
    if not mime:
        mime = "application/octet-stream"
    raw = image.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def _parse_background(value: Any, base_dir: Path) -> tuple[str, str | None]:
    if value is None:
        return "#000000", None
    raw = str(value).strip()
    if not raw:
        return "#000000", None

    if re.match(r"^#([0-9a-fA-F]{3}){1,2}$", raw) or re.match(
        r"^(rgb|rgba|hsl|hsla)\(", raw, flags=re.IGNORECASE
    ):
        return raw, None

    if raw.startswith("http://") or raw.startswith("https://"):
        return "#000000", raw

    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    if path.exists():
        return "#000000", _image_to_data_url(path)

    return raw, None


def _profile_rect(
    canvas_w: int,
    canvas_h: int,
    profile_w: int,
    profile_h: int,
    position: str,
    margin: int,
) -> dict[str, int]:
    pos = position.strip().lower().replace("_", "-")
    col = "center"
    row = "center"
    if "-" in pos:
        row, col = pos.split("-", 1)
    if row not in {"top", "center", "bottom"}:
        row = "center"
    if col not in {"left", "center", "right"}:
        col = "center"

    if col == "left":
        x = margin
    elif col == "center":
        x = (canvas_w - profile_w) // 2
    else:
        x = canvas_w - profile_w - margin

    if row == "top":
        y = margin
    elif row == "center":
        y = (canvas_h - profile_h) // 2
    else:
        y = canvas_h - profile_h - margin

    return {"x": int(x), "y": int(y), "w": int(profile_w), "h": int(profile_h)}


def _html(
    *,
    canvas_w: int,
    canvas_h: int,
    background_color: str,
    background_image_url: str | None,
    profile_data_url: str,
    profile_rect: dict[str, int],
    subtitles: list[dict[str, Any]],
    seed: int,
    animation_duration_ms: int,
    random_color: bool,
    animation_types: list[str] | None,
    y_min: float = 0.0,
    y_max: float = 1.0,
) -> str:
    background_css = f"background: {background_color};"
    if background_image_url:
        background_css = (
            f"background-color: {background_color};"
            f"background-image: url('{background_image_url}');"
            "background-size: cover;"
            "background-position: center;"
            "background-repeat: no-repeat;"
        )
    payload = {
        "canvas": {
            "w": canvas_w,
            "h": canvas_h,
            "backgroundColor": background_color,
            "backgroundImage": background_image_url,
        },
        "profile": {
            "src": profile_data_url,
            "rect": profile_rect,
        },
        "subtitles": subtitles,
        "seed": seed,
        "animationDurationMs": animation_duration_ms,
        "randomColor": random_color,
        "animationTypes": animation_types,
        "yMin": y_min,
        "yMax": y_max,
        "animateCssCdn": ANIMATE_CSS_CDN,
    }

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link id="animatecss" rel="stylesheet" href="{ANIMATE_CSS_CDN}">
  <style>
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      {background_css}
      font-family: -apple-system, BlinkMacSystemFont, \"PingFang SC\", \"Hiragino Sans GB\", \"Noto Sans CJK SC\", \"Microsoft YaHei\", Arial, sans-serif;
    }}
    #viewport {{
      position: fixed;
      left: 0;
      top: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
    }}
    #stage {{
      position: relative;
      width: {canvas_w}px;
      height: {canvas_h}px;
      overflow: hidden;
      transform-origin: top left;
    }}
    @keyframes profileBlink {{
      0%, 100% {{
        filter: drop-shadow(0 0 0 rgba(255, 255, 255, 0));
        opacity: 1;
      }}
      50% {{
        filter: drop-shadow(0 0 22px rgba(255, 255, 255, 0.75));
        opacity: 0.95;
      }}
    }}
    #profile {{
      position: absolute;
      left: {profile_rect["x"]}px;
      top: {profile_rect["y"]}px;
      width: {profile_rect["w"]}px;
      height: auto;
      z-index: 1;
      border-radius: 18px;
      animation: profileBlink 1.4s ease-in-out infinite;
    }}

    @keyframes subZoomIn {{
      0% {{ transform: scale(0.6); opacity: 0; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}
    @keyframes subZoomOutIn {{
      0% {{ transform: scale(1.35); opacity: 0; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}
    @keyframes subRotateInLeft {{
      0% {{ transform: translateX(-60px) rotate(-12deg); opacity: 0; }}
      100% {{ transform: translateX(0) rotate(0); opacity: 1; }}
    }}
    @keyframes subRotateInRight {{
      0% {{ transform: translateX(60px) rotate(12deg); opacity: 0; }}
      100% {{ transform: translateX(0) rotate(0); opacity: 1; }}
    }}
    @keyframes subFlipIn {{
      0% {{ transform: perspective(800px) rotateY(80deg); opacity: 0; }}
      100% {{ transform: perspective(800px) rotateY(0deg); opacity: 1; }}
    }}
    @keyframes subExit {{
      0% {{ opacity: 1; transform: translateY(0) scale(1); }}
      100% {{ opacity: 0; transform: translateY(10px) scale(0.98); }}
    }}

    .enter-zoom-in {{ animation: subZoomIn var(--dur) ease-out both; }}
    .enter-zoom-out {{ animation: subZoomOutIn var(--dur) ease-out both; }}
    .enter-rotate-left {{ animation: subRotateInLeft var(--dur) ease-out both; }}
    .enter-rotate-right {{ animation: subRotateInRight var(--dur) ease-out both; }}
    .enter-flip {{ animation: subFlipIn var(--dur) ease-out both; }}
    .exit-default {{ animation: subExit 420ms ease-in both; }}

    .subtitle {{
      position: absolute;
      padding: 18px 22px;
      box-sizing: border-box;
      line-height: 1.3;
      font-size: {max(24, int(canvas_h * 0.05))}px;
      color: #ffffff;
      background: rgba(0, 0, 0, 0.55);
      border-radius: 18px;
      backdrop-filter: blur(8px);
      white-space: pre-wrap;
      overflow-wrap: break-word;
      z-index: 2;
      --dur: {animation_duration_ms}ms;
    }}
    #measure {{
      position: absolute;
      left: -99999px;
      top: -99999px;
      visibility: hidden;
      width: {int(canvas_w * 0.96)}px;
    }}
  </style>
</head>
<body>
  <div id="viewport">
    <div id="stage">
      <img id="profile" src="{profile_data_url}" />
      <div id="measure"></div>
    </div>
  </div>
  <script type="application/json" id="payload">{json.dumps(payload, ensure_ascii=False)}</script>
  <script>
    (() => {{
      const payload = JSON.parse(document.getElementById('payload').textContent);
      const viewport = document.getElementById('viewport');
      const stage = document.getElementById('stage');
      const measure = document.getElementById('measure');
      const profileRect = payload.profile.rect;
      const W = payload.canvas.w;
      const H = payload.canvas.h;
      const margin = Math.max(16, Math.floor(Math.min(W, H) * 0.02));
      const maxActive = 5;
      const subtitles = payload.subtitles || [];
      const animationDurationMs = payload.animationDurationMs || 600;
      const randomColorEnabled = !!payload.randomColor;
      const animationTypes = Array.isArray(payload.animationTypes) && payload.animationTypes.length
        ? payload.animationTypes
        : [];
      const yMin = typeof payload.yMin === 'number' ? payload.yMin : 0.0;
      const yMax = typeof payload.yMax === 'number' ? payload.yMax : 1.0;
      let nextIndex = 0;
      let active = [];
      let running = false;
      let t0 = 0;
      let zCounter = 10;
      
      let animatePool = [];
      let enterPool = [];
      let exitPool = [];

      async function loadAnimateCss() {{
        const link = document.getElementById('animatecss');
        try {{
          const resp = await fetch(link.href);
          const text = await resp.text();
          const found = new Set();
          const re = /\.animate__(?:animated|([a-zA-Z0-9]+))/g;
          let m;
          while ((m = re.exec(text)) !== null) {{
            if (m[1]) found.add('animate__' + m[1]);
          }}
          animatePool = Array.from(found);
          exitPool = animatePool.filter(n => (n.toLowerCase().includes('out') || n.toLowerCase().includes('hinge')));
          enterPool = animatePool.filter(n => !(n.toLowerCase().includes('out') || n.toLowerCase().includes('hinge')));
        }} catch (e) {{
          console.error('Failed to load Animate.css:', e);
          // Fallback if fetch fails
          enterPool = ['animate__zoomIn', 'animate__fadeIn', 'animate__backInDown'];
          exitPool = ['animate__zoomOut', 'animate__fadeOut'];
        }}
      }}
      loadAnimateCss();

      window.__animateReady = false;
      window.__animateError = null;
      window.__animateReady = true;

      function mulberry32(seed) {{
        let a = seed >>> 0;
        return function() {{
          a |= 0;
          a = (a + 0x6D2B79F5) | 0;
          let t = Math.imul(a ^ (a >>> 15), 1 | a);
          t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
          return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        }};
      }}

      const rng = mulberry32(payload.seed || 1);
      const rngColor = mulberry32(((payload.seed || 1) ^ 0x9e3779b9) >>> 0);

      function updateScale() {{
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        const scale = Math.min(vw / W, vh / H);
        stage.style.transform = `scale(${{scale}})`;
        // 居中显示
        viewport.style.display = 'flex';
        viewport.style.justifyContent = 'center';
        viewport.style.alignItems = 'center';
        stage.style.position = 'relative'; 
      }}
      window.addEventListener('resize', updateScale);
      updateScale();

      function randChoice(arr) {{
        if (!arr || arr.length === 0) return null;
        return arr[Math.floor(rng() * arr.length)];
      }}

      function randomReadableColor() {{
        const h = Math.floor(rngColor() * 360);
        const s = 85;
        const l = 60;
        return 'hsl(' + h + ' ' + s + '% ' + l + '%)';
      }}

      function intersects(a, b) {{
        return !(
          a.x + a.w <= b.x ||
          b.x + b.w <= a.x ||
          a.y + a.h <= b.y ||
          b.y + b.h <= a.y
        );
      }}

      function expandedRect(r, pad) {{
        return {{ x: r.x - pad, y: r.y - pad, w: r.w + pad * 2, h: r.h + pad * 2 }};
      }}

      function measureTextBox(text) {{
        const tmp = document.createElement('div');
        tmp.className = 'subtitle';
        tmp.style.position = 'static';
        tmp.style.left = '';
        tmp.style.top = '';
        tmp.textContent = text;
        measure.appendChild(tmp);
        const rect = {{ width: tmp.offsetWidth, height: tmp.offsetHeight }};
        measure.removeChild(tmp);
        return {{ w: Math.ceil(rect.width), h: Math.ceil(rect.height) }};
      }}

      function pickPosition(boxW, boxH) {{
        const mode = randChoice(['left', 'center', 'right']);
        let x = margin;
        if (mode === 'center') x = (W - boxW) / 2;
        else if (mode === 'right') x = W - boxW - margin;
        
        const yStart = Math.floor(H * yMin);
        const yEnd = Math.floor(H * yMax);
        const safeY0 = Math.max(margin, yStart);
        const safeY1 = Math.max(safeY0, Math.min(H - margin - boxH, yEnd - boxH));
        
        const y = safeY0 + Math.floor(rng() * (safeY1 - safeY0 + 1));
        return {{ x, y, w: boxW, h: boxH, align: mode }};
      }}

      function setAnimation(node, name, onEnd) {{
        if (!name) {{
          if (onEnd) onEnd();
          return;
        }}
        node.style.setProperty('--dur', animationDurationMs + 'ms');
        if (name.startsWith('animate__')) {{
          node.classList.add('animate__animated');
        }}
        node.classList.add(name);
        if (!onEnd) return;
        const handler = (ev) => {{
          if (ev.target !== node) return;
          node.removeEventListener('animationend', handler);
          onEnd();
        }};
        node.addEventListener('animationend', handler);
      }}

      function stripAnimationClasses(node) {{
        // Remove all animate.css classes
        const cls = Array.from(node.classList);
        for (const c of cls) {{
          if (c.startsWith('animate__')) node.classList.remove(c);
        }}
        node.classList.remove('animate__animated');
      }}

      function startExit(item) {{
        if (item.exiting) return;
        item.exiting = true;
        // 如果用户指定了动画类型，且包含 exit 类，可以优先从用户指定中选；
        // 否则从全局 exitPool 中选。这里简化为从全局选。
        const kind = randChoice(exitPool) || 'animate__fadeOut';
        setAnimation(item.node, kind, () => {{
          if (item.node && item.node.parentNode) item.node.parentNode.removeChild(item.node);
          active = active.filter((x) => x !== item);
        }});
      }}

      function clampToViewport(node, item) {{
        const w = node.offsetWidth;
        const h = node.offsetHeight;
        let x = parseFloat(node.style.left || '0');
        let y = parseFloat(node.style.top || '0');
        if (x < margin) x = margin;
        if (x + w > W - margin) x = Math.max(margin, (W - margin) - w);
        if (y < margin) y = margin;
        if (y + h > H - margin) y = Math.max(margin, (H - margin) - h);
        node.style.left = x + 'px';
        node.style.top = y + 'px';
        item.rect = {{ x, y, w, h }};
      }}

      function addSubtitle(s) {{
        const node = document.createElement('div');
        node.className = 'subtitle';
        node.textContent = s.text;
        node.style.zIndex = String(zCounter++);
        if (randomColorEnabled) {{
          node.style.color = randomReadableColor();
        }}
        stage.appendChild(node);

        // 核心布局逻辑：先根据文本量预设一个“理想宽度”
        const limitW = Math.floor(W * 0.95);
        const isLong = s.text.length > 12 || s.text.includes('\\n');
        
        // 如果是长句，直接占满 92% 宽度；短句占 65% 宽度
        const targetW = isLong ? Math.floor(W * 0.92) : Math.floor(W * 0.65);
        node.style.width = targetW + 'px';
        node.style.maxWidth = limitW + 'px';

        const baseFont = parseFloat(getComputedStyle(node).fontSize || '32');
        const minFont = Math.max(18, Math.floor(baseFont * 0.6));
        const maxH = Math.floor(H * 0.35); // 允许单条字幕占 35% 高度
        let fs = Math.floor(baseFont);
        node.style.fontSize = fs + 'px';
        
        let guard = 0;
        while (node.offsetHeight > maxH && fs > minFont && guard < 25) {{
          fs -= 2;
          node.style.fontSize = fs + 'px';
          guard += 1;
        }}

        // 重新收缩宽度：如果文本其实没那么长，就收缩到内容宽度
        // 增加一个“视觉舒适”的最小宽度
        const minComfortW = Math.floor(isLong ? W * 0.7 : W * 0.4);
        const contentW = node.scrollWidth + 48; // padding + margin 缓冲区
        const finalW = Math.min(limitW, Math.max(minComfortW, contentW));
        node.style.width = finalW + 'px';

        const boxW = node.offsetWidth;
        const boxH = node.offsetHeight;
        const rect = pickPosition(boxW, boxH);
        
        node.style.left = rect.x + 'px';
        node.style.top = rect.y + 'px';
        node.style.textAlign = rect.align;

        const item = {{ node, rect, start: s.start, end: s.end, exiting: false, animating: true }};
        active.push(item);
        // 初次放置即修正
        clampToViewport(node, item);

        const finalize = () => {{
          if (!item.animating) return;
          item.animating = false;
          stripAnimationClasses(node);
          // 彻底清除 transform，防止干扰最终定位
          node.style.transform = 'none';
          requestAnimationFrame(() => clampToViewport(node, item));
        }};

        const kind = randChoice(animationTypes);
        if (kind === 'typewriter') {{
          node.style.opacity = '1';
          const full = s.text;
          node.textContent = '';
          const duration = Math.max(250, Math.min(animationDurationMs, Math.floor((s.end - s.start) * 1000 * 0.8)));
          const steps = Math.max(2, Math.min(80, full.length));
          const stepMs = Math.max(16, Math.floor(duration / steps));
          let i = 0;
          const timer = setInterval(() => {{
            i += 1;
            const n = Math.floor((i / steps) * full.length);
            node.textContent = full.slice(0, n);
            if (i >= steps) {{
              clearInterval(timer);
              node.textContent = full;
              finalize();
            }} else {{
              clampToViewport(node, item);
            }}
          }}, stepMs);
          return;
        }}

        let cls = '';
        if (!kind) {{
          cls = randChoice(enterPool) || 'enter-zoom-in';
        }} else if (kind.startsWith('animate__')) {{
          cls = kind;
        }} else {{
          cls = {{
            'zoom_in': 'enter-zoom-in',
            'zoom_out': 'enter-zoom-out',
            'rotate_left': 'enter-rotate-left',
            'rotate_right': 'enter-rotate-right',
            'flip': 'enter-flip',
          }}[kind] || 'enter-zoom-in';
        }}

        setAnimation(node, cls, finalize);
        setTimeout(() => {{ if (node.isConnected) finalize(); }}, animationDurationMs + 120);
      }}

      function tick() {{
        if (!running) return;
        const t = (performance.now() - t0) / 1000.0;

        while (nextIndex < subtitles.length && subtitles[nextIndex].start <= t) {{
          addSubtitle(subtitles[nextIndex]);
          nextIndex += 1;
        }}

        while (active.filter(x => !x.exiting).length > maxActive) {{
          const candidate = active.find((x) => !x.exiting);
          if (!candidate) break;
          startExit(candidate);
        }}

        for (const item of active) {{
          if (!item.exiting && !item.animating) {{
            clampToViewport(item.node, item);
          }}
        }}

        requestAnimationFrame(tick);
      }}

      window.__start = () => {{
        running = true;
        t0 = performance.now();
        requestAnimationFrame(tick);
      }};

      function autoStart() {{
        if (running) return;
        window.__start();
      }}

      setTimeout(autoStart, 0);
    }})();
  </script>
</body>
</html>"""


def main(
    *paths: str,
    config: str = "srt2video.yaml",
    out: str | None = None,
    seed: int | None = None,
    debug_dir: str | None = None,
    html_only: bool = False,
):
    if not paths:
        raise ValueError("请提供音频与 srt，或仅提供 srt 并加 --html_only=true")

    first = Path(paths[0]).expanduser().resolve()
    is_first_srt = first.suffix.lower() == ".srt"
    audio_path: Path | None
    if is_first_srt:
        audio_path = None
        srt_paths = [Path(p).expanduser().resolve() for p in paths]
        if not html_only:
            raise ValueError("未提供音频；若仅生成 HTML，请加 --html_only=true")
    else:
        audio_path = first
        if not audio_path.exists():
            raise FileNotFoundError(audio_path)
        srt_paths = [Path(p).expanduser().resolve() for p in paths[1:]]

    if not srt_paths:
        raise ValueError("请至少提供一个 srt 文件路径")
    for p in srt_paths:
        if not p.exists():
            raise FileNotFoundError(p)

    cfg_path = Path(config).expanduser().resolve()
    if not cfg_path.exists():
        raise FileNotFoundError(cfg_path)
    cfg = _read_yaml(cfg_path)

    width = int(cfg.get("width", 1920))
    ratio = _parse_ratio(cfg.get("ratio", "16/9"))
    height = int(round(width / float(ratio)))
    background_color, background_image_url = _parse_background(cfg.get("background"), cfg_path.parent)

    profile_path = Path(str(cfg.get("profile", ""))).expanduser()
    if not profile_path.is_absolute():
        profile_path = (cfg_path.parent / profile_path).resolve()
    if not profile_path.exists():
        raise FileNotFoundError(profile_path)

    position = str(cfg.get("position", "top-left")).strip()
    size = _parse_percent(cfg.get("size", "50%"))
    size = min(max(size, 0.05), 1.0)

    profile_img_w, profile_img_h = _ffprobe_image_size(profile_path)
    profile_w = int(round(width * size))
    profile_h = int(round(profile_w * (profile_img_h / profile_img_w)))
    margin = max(16, int(round(min(width, height) * 0.02)))
    profile_rect = _profile_rect(width, height, profile_w, profile_h, position, margin)
    profile_data_url = _image_to_data_url(profile_path)

    base_seed = seed if seed is not None else random.randint(1, 2**31 - 1)

    merged = _merge_srts(srt_paths)
    if not merged:
        raise ValueError("未能从 srt 中解析到任何字幕")

    subtitles: list[Subtitle] = []
    for start, end, text in merged:
        subtitles.append(Subtitle(start=start, end=end, text=text))

    video_duration = None if audio_path is None else _ffprobe_duration_seconds(audio_path)
    if video_duration is None:
        video_duration = max(s.end for s in subtitles) + 1.0
    video_duration = max(1.0, float(video_duration))

    subtitles_payload = [{"start": s.start, "end": s.end, "text": s.text} for s in subtitles]
    html = _html(
        canvas_w=width,
        canvas_h=height,
        background_color=background_color,
        background_image_url=background_image_url,
        profile_data_url=profile_data_url,
        profile_rect=profile_rect,
        subtitles=subtitles_payload,
        seed=base_seed,
        animation_duration_ms=int(cfg.get("subtitle_animation_duration_ms", 600)),
        random_color=bool(cfg.get("subtitle_random_color", True)),
        animation_types=list(cfg.get("subtitle_animation_types") or []),
        y_min=float(cfg.get("y_min", 0.0)),
        y_max=float(cfg.get("y_max", 1.0)),
    )

    work_dir: Path
    temp_dir_obj: tempfile.TemporaryDirectory[str] | None = None
    if debug_dir:
        work_dir = Path(debug_dir).expanduser().resolve()
        work_dir.mkdir(parents=True, exist_ok=True)
    else:
        temp_dir_obj = tempfile.TemporaryDirectory(prefix="srt2video_")
        work_dir = Path(temp_dir_obj.name).resolve()

    html_path = work_dir / "index.html"
    timeline_path = work_dir / "timeline.json"
    html_path.write_text(html, encoding="utf-8")
    timeline_path.write_text(
        json.dumps(
            {
                "audio": None if audio_path is None else str(audio_path),
                "srts": [str(p) for p in srt_paths],
                "duration": video_duration,
                "profile_rect": profile_rect,
                "subtitles": subtitles_payload,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    logger.info(f"HTML: {html_path}")
    logger.info(f"Timeline: {timeline_path}")

    if html_only:
        return

    try:
        import importlib

        module_name = "playwright" + ".sync_api"
        sync_playwright = importlib.import_module(module_name).sync_playwright
    except Exception as e:
        raise RuntimeError("缺少 playwright。请先安装 playwright 并安装 chromium。") from e

    if audio_path is None:
        raise ValueError("未提供音频，无法合成视频。若仅生成 HTML，请加 --html_only=true")

    out_path = Path(out).expanduser().resolve() if out else audio_path.with_suffix(".mp4")

    _check_executable("ffmpeg")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": width, "height": height},
            record_video_dir=str(work_dir),
            record_video_size={"width": width, "height": height},
        )
        page = context.new_page()
        page.goto(html_path.as_uri(), wait_until="load")
        page.evaluate("window.__start()")
        page.wait_for_timeout(int(video_duration * 1000) + 400)
        video = page.video
        page.close()
        context.close()
        browser.close()

        if not video:
            raise RuntimeError("未生成录屏文件")
        webm_path = Path(video.path()).resolve()

    ffmpeg = _check_executable("ffmpeg")
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(webm_path),
        "-i",
        str(audio_path),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        str(out_path),
    ]
    logger.info(" ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-2000:] if proc.stderr else "ffmpeg 合成失败")
    logger.info(f"Output: {out_path}")

    if temp_dir_obj is not None:
        temp_dir_obj.cleanup()


if __name__ == "__main__":
    fire.Fire(main)
