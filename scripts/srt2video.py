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
        x = 0
    elif col == "center":
        x = (canvas_w - profile_w) // 2
    else:
        x = (canvas_w - profile_w)
    
    if row == "top":
        y = 0
    elif row == "center":
        y = (canvas_h - profile_h) // 2
    else:
        y = (canvas_h - profile_h)

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
    colors: list[str] | None = None,
    font_data_url: str | None = None,
    profile_animation_enabled: bool = True,
    profile_animation_duration_ms: int = 1400,
    y_min: float = 0.0,
    y_max: float = 1.0,
    layout_mode: str = "random",
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
    
    font_face_css = ""
    if font_data_url:
        font_face_css = f"""
    @font-face {{
      font-family: 'CustomFont';
      src: url('{font_data_url}');
    }}
    """

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
        "colors": colors,
        "fontFamily": "CustomFont" if font_data_url else None,
        "animationTypes": animation_types,
        "yMin": y_min,
        "yMax": y_max,
        "layoutMode": layout_mode,
        "animateCssCdn": ANIMATE_CSS_CDN,
    }

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link id="animatecss" rel="stylesheet" href="{ANIMATE_CSS_CDN}">
  <style>
    {font_face_css}
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      {background_css}
      font-family: {"'CustomFont'," if font_data_url else ""} -apple-system, BlinkMacSystemFont, \"PingFang SC\", \"Hiragino Sans GB\", \"Noto Sans CJK SC\", \"Microsoft YaHei\", Arial, sans-serif;
    }}
    #viewport {{
      position: fixed;
      left: 0;
      top: 0;
      width: 100vw;
      height: 100vh;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: center;
      {background_css}
    }}
    #stage {{
      position: relative;
      width: {canvas_w}px;
      height: {canvas_h}px;
      overflow: hidden;
      flex-shrink: 0;
    }}
    @keyframes profileBlink {{
      0%, 100% {{
        opacity: 1;
      }}
      50% {{
        opacity: 0.5;
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
      {"animation: profileBlink " + str(profile_animation_duration_ms) + "ms ease-in-out infinite;" if profile_animation_enabled else ""}
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
      padding: 10px 15px;
      box-sizing: border-box;
      line-height: 1.2;
      color: #ffffff;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), -1px -1px 0 rgba(0, 0, 0, 0.5);
      white-space: nowrap;
      overflow: visible;
      z-index: 2;
      --dur: {animation_duration_ms}ms;
      transition: top 400ms cubic-bezier(0.215, 0.61, 0.355, 1);
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
      const colorPool = Array.isArray(payload.colors) && payload.colors.length ? payload.colors : [];
      const animationTypes = Array.isArray(payload.animationTypes) && payload.animationTypes.length
        ? payload.animationTypes
        : [];
      const yMin = typeof payload.yMin === 'number' ? payload.yMin : 0.0;
      const yMax = typeof payload.yMax === 'number' ? payload.yMax : 1.0;
      const layoutMode = payload.layoutMode || 'random';
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

      window.__activeSubtitles = () => active;

      function randChoice(arr) {{
        if (!arr || arr.length === 0) return null;
        return arr[Math.floor(rng() * arr.length)];
      }}

      function randomReadableColor() {{
        if (colorPool.length > 0) {{
          const c = randChoice(colorPool);
          return c.startsWith('#') ? c : '#' + c;
        }}
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

      function startExit(item, preferredKind) {{
        if (item.exiting) return;
        item.exiting = true;
        const kind = preferredKind || randChoice(exitPool) || 'animate__fadeOut';
        
        setAnimation(item.node, kind, () => {{
          if (item.node && item.node.parentNode) item.node.parentNode.removeChild(item.node);
          active = active.filter((x) => x !== item);
        }});

        // 安全兜底：如果动画回调没触发，1.5秒后强制清理
        setTimeout(() => {{
          if (item.node && item.node.parentNode) {{
            item.node.parentNode.removeChild(item.node);
            active = active.filter((x) => x !== item);
          }}
        }}, 1500);
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

        // 字幕长度处理：20字以内不换行
        const charCount = s.text.length;
        if (charCount <= 20) {{
          node.style.whiteSpace = 'nowrap';
        }} else {{
          node.style.whiteSpace = 'pre-wrap';
          node.style.overflowWrap = 'break-word';
          node.style.width = Math.floor(W * 0.96) + 'px';
        }}

        // 1. 初始字体大小计算：基于屏宽 96% 的保守估算
        // 对于中文，字宽约等于字号，所以 idealFontSize = (W * 0.96) / charCount
        let fs = Math.floor((W * 0.96) / Math.max(1, charCount));
        
        // 限制最大字号为屏宽的 20%，最小为 28px
        fs = Math.max(28, Math.min(fs, Math.floor(W * 0.2)));
        node.style.fontSize = fs + 'px';

        // 2. 动态收缩机制：如果实际宽度溢出，则循环缩小字号
        const maxSafeW = Math.floor(W * 0.98); // 允许的最大安全宽度
        let guard = 0;
        while (node.scrollWidth > maxSafeW && fs > 20 && guard < 20) {{
          fs -= 2;
          node.style.fontSize = fs + 'px';
          guard++;
        }}

        const boxW = node.offsetWidth;
        const boxH = node.offsetHeight;
        
        let rect;
        if (layoutMode === 'scroll_up') {{
          // 向上顶模式：新字幕出现在 yMax 处
          const x = (W - boxW) / 2;
          const y = Math.floor(H * yMax) - boxH - margin;
          rect = {{ x, y, w: boxW, h: boxH, align: 'center' }};
          
          // 将现有的所有 active 字幕向上移动
          const gap = 12; // 字幕间距
          const shift = boxH + gap;
          for (const item of active) {{
            if (!item.exiting) {{
              item.rect.y -= shift;
              item.node.style.top = item.rect.y + 'px';
            }}
          }}
        }} else {{
          rect = pickPosition(boxW, boxH);
        }}
        
        node.style.left = rect.x + 'px';
        node.style.top = rect.y + 'px';
        node.style.textAlign = rect.align;

        const item = {{ node, rect, start: s.start, end: s.end, exiting: false, animating: true }};
        active.push(item);
        
        // 如果是 scroll_up 模式，检查是否达到 5 条，如果是则批量清除前 4 条
        if (layoutMode === 'scroll_up' && active.filter(x => !x.exiting).length >= 5) {{
          const nonExiting = active.filter(x => !x.exiting);
          // 所有的字幕都向同一方向旋转（随机选一个方向，但本批次统一）
          const exitKind = rng() > 0.5 ? 'animate__rotateOutUpLeft' : 'animate__rotateOutUpRight';
          // 倒数第1个是刚加的，所以清除索引 0 到 length-2 的字幕
          for (let i = 0; i < nonExiting.length - 1; i++) {{
            startExit(nonExiting[i], exitKind);
          }}
        }}

        // 初次放置即修正（scroll_up 模式下可能暂时超出 top，但 tick 会持续修正）
        clampToViewport(node, item);

        const finalize = () => {{
          if (!item.animating) return;
          item.animating = false;
          stripAnimationClasses(node);
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
        const now = performance.now();
        const t = (now - t0) / 1000.0;

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
        if (running) return t0;
        running = true;
        t0 = performance.now();
        requestAnimationFrame(tick);
        return t0;
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
    config: str | None = None,
    out: str | None = None,
    seed: int | None = None,
    debug_dir: str | None = None,
    html_only: bool = False,
):
    if not paths:
        raise ValueError("请提供音频与 srt，或仅提供 srt 并加 --html_only=true")

    # 查找配置文件逻辑
    cfg_name = "srt2video.yaml"
    script_dir = Path(__file__).parent.resolve()
    
    if config:
        cfg_path = Path(config).expanduser().resolve()
    else:
        # 优先级 1: 当前工作目录
        cfg_path = Path.cwd() / cfg_name
        if not cfg_path.exists():
            # 优先级 2: 脚本所在目录
            cfg_path = script_dir / cfg_name

    if not cfg_path.exists():
        raise FileNotFoundError(f"未找到配置文件：{cfg_path} (请在当前目录或脚本目录放置 {cfg_name}，或使用 --config 指定)")
    
    cfg = _read_yaml(cfg_path)

    # 解析输入路径逻辑
    first = Path(paths[0]).expanduser().resolve()
    is_first_srt = first.suffix.lower() == ".srt"
    audio_path: Path | None = None
    srt_paths: list[Path] = []
    
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

    out_path: Path | None = None
    if not html_only:
        if out:
            out_path = Path(out).expanduser().resolve()
        elif audio_path:
            # 使用音频文件的 stem (文件名去掉后缀) + .mp4
            out_path = audio_path.with_name(f"{audio_path.stem}.mp4")
        else:
            # 只有 SRT 时，使用第一个 SRT 的 stem
            out_path = srt_paths[0].with_name(f"{srt_paths[0].stem}.mp4")

    # 音频预处理：统一转为标准 CBR 格式以解决 VBR 导致的音画同步漂移
    if audio_path and not html_only:
        ffmpeg = _check_executable("ffmpeg")
        # 创建一个临时文件用于存放处理后的音频
        temp_audio = Path(tempfile.gettempdir()) / f"processed_{audio_path.name}.wav"
        logger.info(f"正在预处理音频以确保同步精度: {audio_path} -> {temp_audio}")
        
        # 转换为 44100Hz, 单声道/双声道可选, 但关键是使用 WAV (无损/CBR) 或固定比特率
        # 这里使用 PCM WAV 是最稳妥的中间格式
        cmd_preprocess = [
            ffmpeg, "-y",
            "-i", str(audio_path),
            "-ar", "44100",
            "-ac", "2",
            str(temp_audio)
        ]
        proc_pre = subprocess.run(cmd_preprocess, capture_output=True, text=True)
        if proc_pre.returncode == 0:
            audio_path = temp_audio
            logger.info("音频预处理完成")
        else:
            logger.warning(f"音频预处理失败，将尝试直接使用原音频: {proc_pre.stderr}")

    width = int(cfg.get("width", 1920))
    if "height" in cfg:
        height = int(cfg["height"])
    else:
        ratio = _parse_ratio(cfg.get("ratio", "16/9"))
        height = int(round(width / float(ratio)))
    
    dpr = float(cfg.get("dpr", 1.0))
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
    
    # 处理自定义字体
    font_path_raw = cfg.get("font")
    font_data_url = None
    if font_path_raw:
        font_path = Path(str(font_path_raw)).expanduser()
        if not font_path.is_absolute():
            font_path = (cfg_path.parent / font_path).resolve()
        if font_path.exists():
            font_data_url = _image_to_data_url(font_path) # 复用 base64 转换逻辑
        else:
            logger.warning(f"未找到字体文件：{font_path}")

    # 处理 BGM
    bgm_cfg = cfg.get("bgm")
    bgm_path: Path | None = None
    bgm_volume = 0.2
    bgm_start = 0.0
    if bgm_cfg and isinstance(bgm_cfg, dict):
        bgm_p = bgm_cfg.get("path")
        if bgm_p:
            bgm_path = Path(str(bgm_p)).expanduser()
            if not bgm_path.is_absolute():
                bgm_path = (cfg_path.parent / bgm_path).resolve()
            if not bgm_path.exists():
                logger.warning(f"未找到 BGM 文件：{bgm_path}")
                bgm_path = None
        bgm_volume = float(bgm_cfg.get("volume", 0.2))
        bgm_start = float(bgm_cfg.get("start", 0.0))

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
        colors=list(cfg.get("colors") or []),
        font_data_url=font_data_url,
        profile_animation_enabled=bool(cfg.get("profile_animation_enabled", True)),
        profile_animation_duration_ms=int(cfg.get("profile_animation_duration_ms", 1400)),
        animation_types=list(cfg.get("subtitle_animation_types") or []),
        y_min=float(cfg.get("y_min", 0.0)),
        y_max=float(cfg.get("y_max", 1.0)),
        layout_mode=str(cfg.get("subtitle_layout_mode", "random")),
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


    if not html_only and audio_path is None:
        raise ValueError("未提供音频，无法合成视频。若仅生成 HTML，请加 --html_only=true")

    _check_executable("ffmpeg")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=dpr,
            record_video_dir=str(work_dir),
            record_video_size={"width": int(width * dpr), "height": int(height * dpr)},
        )
        page = context.new_page()
        # 调试模式下可以开启 console 日志
        # page.on("console", lambda msg: logger.info(f"Browser console: {msg.text}"))
        page.goto(html_path.as_uri(), wait_until="networkidle") # 改为 networkidle 确保资源加载
        # 捕获字幕开始的偏移量（毫秒）
        start_offset_ms = page.evaluate("window.__start()")
        logger.info(f"Subtitle start offset: {start_offset_ms}ms")

        # 录制结束后多等 1000ms 确保尾部完整
        page.wait_for_timeout(int(video_duration * 1000) + 1000)
        video = page.video
        page.close()
        context.close()
        browser.close()

        if not video:
            raise RuntimeError("未生成录屏文件")
        webm_path = Path(video.path()).resolve()

    ffmpeg = _check_executable("ffmpeg")
    start_offset_sec = start_offset_ms / 1000.0
    if bgm_path:
        # 使用 complex filter 混合 BGM
        # adelay 的单位是毫秒，需要对左右声道都设置
        delay_ms = int(bgm_start * 1000)
        filter_complex = (
            f"[1:a]volume=1.0[main_a];"
            f"[2:a]adelay={delay_ms}|{delay_ms},volume={bgm_volume}[bgm_a];"
            f"[main_a][bgm_a]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        cmd = [
               ffmpeg,
               "-y",
               "-ss", str(start_offset_sec),
               "-i", str(webm_path),
               "-i", str(audio_path),
               "-stream_loop", "-1", "-i", str(bgm_path),
               "-filter_complex", filter_complex,
               "-map", "0:v",
               "-map", "[a]",
               "-async", "1",
               "-vsync", "cfr",
               "-c:v", "libx264",
               "-pix_fmt", "yuv420p",
               "-c:a", "aac",
               "-shortest",
               str(out_path),
           ]
    else:
        cmd = [
            ffmpeg,
            "-y",
            "-ss", str(start_offset_sec),
            "-i", str(webm_path),
            "-i", str(audio_path),
            "-async", "1",
            "-vsync", "cfr",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
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
