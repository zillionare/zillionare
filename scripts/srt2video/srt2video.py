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

配置文件 srt2video.yaml
"""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import sys
import os
import random
import re
import shutil
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import fire
import yaml
from loguru import logger

__version__ = "0.1.0"

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


def _download_resource(url: str, cache_dir: Path, retries: int = 2) -> Path:
    """下载远程资源到本地缓存目录，如果已存在则跳过。"""
    if not url.startswith(("http://", "https://")):
        return Path(url)

    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # 尝试从 URL 提取文件名
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    
    # 如果没有文件名或文件名太乱，使用 URL 的 MD5
    if not filename or "." not in filename or len(filename) > 100:
        ext = ""
        # 尝试通过内容类型判断后缀，但不发完整请求
        filename = hashlib.md5(url.encode()).hexdigest() + ext
    
    local_path = cache_dir / filename
    
    if local_path.exists():
        # logger.debug(f"资源已存在，跳过下载: {local_path}")
        return local_path

    # 下载逻辑，包含镜像切换和重试
    fast_url = url
    if "cdn.jsdelivr.net" in url:
        fast_url = url.replace("cdn.jsdelivr.net", "fastly.jsdelivr.net")
    elif "raw.githubusercontent.com" in url:
        fast_url = url.replace("raw.githubusercontent.com", "raw.fastgit.org") # 尝试镜像
    
    # 增加对 jsdelivr 的直接首选镜像
    if "cdn.jsdelivr.net" in url:
        url = fast_url # 直接用 fastly 镜像作为首选
    
    for attempt in range(retries + 1):
        try:
            current_url = fast_url if attempt > 0 else url
            logger.info(f"正在下载资源 (尝试 {attempt+1}/{retries+1}): {current_url} -> {local_path}")
            
            req = urllib.request.Request(
                current_url, 
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                local_path.write_bytes(content)
                return local_path
        except Exception as e:
            if attempt < retries:
                logger.warning(f"下载失败: {e}，正在重试...")
                time.sleep(1)
            else:
                logger.error(f"资源下载最终失败: {url}, 错误: {e}")
                # 如果下载失败且本地不存在，返回原始 URL 供后续逻辑（如 Base64 转换）尝试
                return Path(url)
    
    return local_path


def _download_to_data_url(url: str, retries: int = 2) -> str:
    # 如果是 jsdelivr 的域名，尝试切换到 fastly 镜像，通常国内访问更稳定
    fast_url = url
    if "cdn.jsdelivr.net" in url:
        fast_url = url.replace("cdn.jsdelivr.net", "fastly.jsdelivr.net")

    for attempt in range(retries + 1):
        try:
            current_url = fast_url if attempt > 0 else url
            logger.info(f"正在下载外部资源 (尝试 {attempt+1}/{retries+1}): {current_url}")
            
            req = urllib.request.Request(
                current_url, 
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            )
            # 缩短单次下载超时，快速进入重试或镜像切换
            with urllib.request.urlopen(req, timeout=8) as response:
                content = response.read()
                mime_type = response.info().get_content_type()
                b64 = base64.b64encode(content).decode("utf-8")
                return f"data:{mime_type};base64,{b64}"
        except Exception as e:
            if attempt < retries:
                logger.warning(f"下载尝试 {attempt+1} 失败: {e}，正在重试...")
                time.sleep(1) # 稍微等待后重试
            else:
                logger.warning(f"下载外部资源最终失败: {url}, 错误: {e}")
    
    return url


def _image_to_data_url(image: Path) -> str:
    mime, _ = mimetypes.guess_type(str(image))
    if not mime:
        mime = "application/octet-stream"
    raw = image.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def _parse_background(value: Any, base_dir: Path) -> tuple[str, str | None]:
    if value is None:
        return "#ffffff", None

    raw = str(value).strip()
    if not raw or raw.lower() == "transparent":
        return "transparent", None

    if re.match(r"^#([0-9a-fA-F]{3}){1,2}$", raw) or re.match(
        r"^(rgb|rgba|hsl|hsla)\(", raw, flags=re.IGNORECASE
    ):
        return raw, None

    if raw.startswith("http://") or raw.startswith("https://"):
        return "#000000", _download_to_data_url(raw)

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
    profile_data_url: str | None = None,
    profile_rect: dict[str, int] | None = None,
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
    logo_url: str | None = None,
    total_duration: float = 0.0,
    animate_css_path: Path | None = None,
    instructor_profiles: list[str] | None = None,
) -> str:
    background_css = f"background: {background_color};"
    if background_image_url:
        # 如果是 jsdelivr 链接且没能 Base64 化，同样切换到镜像
        if background_image_url.startswith("http") and "cdn.jsdelivr.net" in background_image_url:
            background_image_url = background_image_url.replace("cdn.jsdelivr.net", "fastly.jsdelivr.net")
        
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

    # 处理 Animate.css 资源
    animate_url = ANIMATE_CSS_CDN
    if animate_css_path and animate_css_path.exists():
        try:
            content = animate_css_path.read_bytes()
            b64 = base64.b64encode(content).decode("utf-8")
            animate_url = f"data:text/css;base64,{b64}"
            logger.info(f"使用本地 Animate.css: {animate_css_path}")
        except Exception as e:
            logger.warning(f"加载本地 Animate.css 失败: {e}，将回退到 CDN")

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
        "instructorProfiles": instructor_profiles,
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
        "logoUrl": logo_url,
        "totalDuration": total_duration,
        "animateCssCdn": animate_url,
    }

    # Profile Animation Class
    profile_animation_css = ""
    if profile_animation_enabled:
        profile_animation_css = f"animation: profileBlink {profile_animation_duration_ms}ms ease-in-out infinite;"

    # Prepare template context
    template_context = {
        "animate_url": animate_url,
        "font_face_css": font_face_css,
        "background_css": background_css,
        "font_family_custom": "\"CustomFont\", " if font_data_url else "",
        "canvas_w": canvas_w,
        "canvas_h": canvas_h,
        "profile_x": profile_rect["x"] if profile_rect else 0,
        "profile_y": profile_rect["y"] if profile_rect else 0,
        "profile_w": profile_rect["w"] if profile_rect else 0,
        "profile_animation_css_applied": profile_animation_css if profile_rect else "",
        "instructor_header_animation_css": profile_animation_css if instructor_profiles else "",
        "animation_duration_ms": animation_duration_ms,
        "measure_width": int(canvas_w * 0.96),
        "logo_url_safe": logo_url or "",
        "profile_img_tag": "<img id=\"profile\" src=\"{}\" />".format(profile_data_url) if profile_data_url and not instructor_profiles else "",
        "instructor_header_html": (
            "<div class=\"instructor-header\">\n"
            "  <div class=\"instructor-title\">匡醍·量化好声音</div>\n"
            "  <div class=\"instructor-subtitle\">洞悉投资新声 探索量化前沿</div>\n"
            "  <div class=\"instructor-profiles\">\n"
            "    {}\n"
            "  </div>\n"
            "</div>"
        ).format(
            " ".join(["<div class=\"instructor-avatar-wrapper\"><img class=\"instructor-avatar\" src=\"{}\" /></div>".format(url) for url in (instructor_profiles or [])])
        ) if instructor_profiles else "",
        "payload_json": json.dumps(payload, ensure_ascii=False)
    }

    # Load and render template
    tpl_path = os.path.join(os.path.dirname(__file__), "srt2video.tpl")
    try:
        with open(tpl_path, "r", encoding="utf-8") as f:
            template = f.read()
        return template.format(**template_context)
    except FileNotFoundError:
        logger.error(f"Template file not found: {tpl_path}")
        raise


def _split_long_subtitles(subtitles: list[Subtitle], max_words: int) -> list[Subtitle]:
    if max_words <= 0:
        return subtitles

    import logging

    import jieba

    # 禁用 jieba 的调试日志
    jieba.setLogLevel(logging.WARNING)

    new_subtitles = []
    for s in subtitles:
        # 使用 jieba 分词，它能很好地处理中英文混合
        words = list(jieba.cut(s.text))
        count = len(words)

        if count <= max_words:
            new_subtitles.append(s)
            continue

        logger.debug(f"正在拆分长字幕 (词数: {count}): {s.text[:30]}...")

        # 将词分成多个组，每组最多 max_words 个词
        chunks = [words[i : i + max_words] for i in range(0, count, max_words)]
        total_words = count

        current_start = s.start
        duration = s.end - s.start

        for i, chunk in enumerate(chunks):
            chunk_text = "".join(chunk).strip()
            if not chunk_text:
                continue
            chunk_word_count = len(chunk)
            # 按词数比例分配时长
            chunk_duration = (chunk_word_count / total_words) * duration
            chunk_end = current_start + chunk_duration

            # 最后一段确保结束时间准确
            if i == len(chunks) - 1:
                chunk_end = s.end

            new_subtitles.append(Subtitle(start=current_start, end=chunk_end, text=chunk_text))
            current_start = chunk_end

    return new_subtitles


def main(
    *paths: str,
    config: str | None = None,
    out: str | None = None,
    seed: int | None = None,
    debug_dir: str | None = None,
    html_only: bool = False,
    max_words_per_line: int | None = None,
    version: bool = False,
):
    if version:
        print(f"srt2video version {__version__}")
        return

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

    # 缓存目录处理
    cache_dir_cfg = cfg.get("cache_dir", "resources")
    cache_dir = Path(cache_dir_cfg).expanduser()
    if not cache_dir.is_absolute():
        # 默认相对于脚本所在目录
        cache_dir = (script_dir / cache_dir).resolve()
    
    # 预下载/定位背景资源
    bg_raw = cfg.get("background")
    if bg_raw and str(bg_raw).startswith(("http://", "https://")):
        local_bg = _download_resource(str(bg_raw), cache_dir)
        if local_bg.exists():
            cfg["background"] = str(local_bg)

    background_color, background_image_url = _parse_background(cfg.get("background"), cfg_path.parent)

    # 处理 Profile
    profile_raw = cfg.get("profile", "")
    instructor_profiles = []
    
    # 特殊处理：如果 profile 是列表，或者我们有特定的 instructor 要求
    # 这里我们根据用户要求，直接支持双头像模式
    instructor_urls = [
        "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/instructor/portrait-half.jpg",
        "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/instructor/flora-2.jpg"
    ]
    
    # 如果用户没有指定 profile，或者显式想用这两个头像
    # 为了保险，我们先下载这两个头像
    for url in instructor_urls:
        local_p = _download_resource(url, cache_dir)
        if local_p.exists():
            instructor_profiles.append(_image_to_data_url(local_p))
        else:
            instructor_profiles.append(_download_to_data_url(url))

    profile_data_url = None
    profile_rect = None
    
    if not instructor_profiles:
        if str(profile_raw).startswith(("http://", "https://")):
            local_profile = _download_resource(str(profile_raw), cache_dir)
            if local_profile.exists():
                profile_path = local_profile
            else:
                profile_path = Path(str(profile_raw)) # 可能会失败
        else:
            profile_path = Path(str(profile_raw)).expanduser()
            if not profile_path.is_absolute():
                profile_path = (cfg_path.parent / profile_path).resolve()
        
        if not profile_path.exists() and not str(profile_path).startswith("http"):
            raise FileNotFoundError(profile_path)

        position = str(cfg.get("position", "top-left")).strip()
        size = _parse_percent(cfg.get("size", "50%"))
        size = min(max(size, 0.05), 1.0)

        if profile_path.exists():
            profile_img_w, profile_img_h = _ffprobe_image_size(profile_path)
            profile_data_url = _image_to_data_url(profile_path)
        else:
            # 如果是 URL 且没下载成功，尝试直接下载并转为 data URL
            logger.warning(f"Profile 本地文件不存在，尝试从 URL 直接加载: {profile_path}")
            profile_data_url = _download_to_data_url(str(profile_path))
            profile_img_w, profile_img_h = 500, 500 

        profile_w = int(round(width * size))
        profile_h = int(round(profile_w * (profile_img_h / profile_img_w)))
        margin = max(16, int(round(min(width, height) * 0.02)))
        profile_rect = _profile_rect(width, height, profile_w, profile_h, position, margin)

    base_seed = seed if seed is not None else random.randint(1, 2**31 - 1)

    merged = _merge_srts(srt_paths)
    if not merged:
        raise ValueError("未能从 srt 中解析到任何字幕")

    subtitles: list[Subtitle] = []
    for start, end, text in merged:
        subtitles.append(Subtitle(start=start, end=end, text=text))

    # 处理长字幕拆分
    max_words = max_words_per_line
    if max_words is None:
        # 尝试从配置文件读取
        max_words = cfg.get("max_words_per_line")
    
    if max_words is not None:
        subtitles = _split_long_subtitles(subtitles, int(max_words))

    # 计算视频总时长：最后一个字幕结束时间 + 1.0秒用于显示结尾 logo
    last_sub_end = max(s.end for s in subtitles) if subtitles else 0.0
    video_duration = last_sub_end + 1.0

    # 如果有音频，确保视频时长至少能覆盖音频，同时保证 Logo 能够显示
    if audio_path and not html_only:
        audio_duration = _ffprobe_duration_seconds(audio_path)
        if audio_duration:
            # 视频时长应取【音频时长】和【字幕结束+Logo时间】的最大值
            # 这样即便音频比字幕长，或者字幕比音频长，Logo 都能正常显示
            video_duration = max(video_duration, audio_duration + 1.0)

    video_duration = max(1.0, float(video_duration))

    subtitles_payload = [{"start": s.start, "end": s.end, "text": s.text} for s in subtitles]
    
    # 处理自定义字体
    font_path_raw = cfg.get("font")
    font_data_url = None
    if font_path_raw:
        if str(font_path_raw).startswith(("http://", "https://")):
            font_path = _download_resource(str(font_path_raw), cache_dir)
        else:
            font_path = Path(str(font_path_raw)).expanduser()
            if not font_path.is_absolute():
                font_path = (cfg_path.parent / font_path).resolve()
        
        if font_path.exists():
            font_data_url = _image_to_data_url(font_path) # 复用 base64 转换逻辑
        else:
            logger.warning(f"未找到字体文件：{font_path}")

    # 处理 BGM
    bgm_cfg = cfg.get("bgm")

    # 处理 Animate.css 本地化
    animate_css_path = None
    animate_cfg = cfg.get("animate_css")
    if animate_cfg:
        if str(animate_cfg).startswith(("http://", "https://")):
            animate_css_path = _download_resource(str(animate_cfg), cache_dir)
        else:
            animate_css_path = Path(str(animate_cfg)).expanduser()
            if not animate_css_path.is_absolute():
                animate_css_path = (cfg_path.parent / animate_css_path).resolve()

    # 如果配置中没指定或没找到，默认尝试脚本同目录下的 animate.min.css
    if not animate_css_path or not animate_css_path.exists():
        default_local = Path(__file__).parent / "animate.min.css"
        if default_local.exists():
            animate_css_path = default_local
            logger.info(f"自动检测并使用本地 Animate.css: {animate_css_path}")
        elif animate_cfg:
            logger.warning(f"指定的 Animate.css 未找到：{animate_cfg}，将尝试 CDN")
            animate_css_path = None
    else:
        logger.info(f"使用 Animate.css: {animate_css_path}")

    # 处理 Logo
    logo_path_raw = cfg.get("logo")
    logo_url = None
    if logo_path_raw:
        if str(logo_path_raw).startswith(("http://", "https://")):
            logo_path = _download_resource(str(logo_path_raw), cache_dir)
            if logo_path.exists():
                logo_url = _image_to_data_url(logo_path)
            else:
                # 降级：如果下载失败，尝试直接用 URL
                logo_url = _download_to_data_url(str(logo_path_raw))
        else:
            logo_path = Path(str(logo_path_raw)).expanduser()
            if not logo_path.is_absolute():
                logo_path = (cfg_path.parent / logo_path).resolve()
            if logo_path.exists():
                logo_url = _image_to_data_url(logo_path)
            else:
                logger.warning(f"未找到 Logo 文件：{logo_path}")

    # 如果 Logo 是远程 URL 且没能成功 Base64 化，强制在录制前等待一下，
    # 或者如果对 Logo 要求极高，可以考虑在这里报错或使用本地默认图。
    # 暂且保持现状，但在录制脚本中增加更强的重试。

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
        logo_url=logo_url,
        total_duration=video_duration,
        animate_css_path=animate_css_path,
        instructor_profiles=instructor_profiles,
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
        # 增加超时时间到 90 秒，并捕获 console 日志以方便调试
        page.set_default_timeout(90000)
        page.on("console", lambda msg: logger.debug(f"Browser console: {msg.text}"))
        
        try:
            logger.info(f"正在加载页面: {html_path.as_uri()}")
            # 改为 wait_until="load" 并减小超时时间。因为我们已经尽可能本地化了资源。
            page.goto(html_path.as_uri(), wait_until="load", timeout=60000)
        except Exception as e:
            logger.warning(f"页面加载超时或失败: {e}。尝试继续执行...")

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
               "-t", str(video_duration),
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
               str(out_path),
           ]
    else:
        cmd = [
            ffmpeg,
            "-y",
            "-ss", str(start_offset_sec),
            "-t", str(video_duration),
            "-i", str(webm_path),
            "-i", str(audio_path),
            "-async", "1",
            "-vsync", "cfr",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
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
