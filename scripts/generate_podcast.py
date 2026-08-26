#!/usr/bin/env python3
"""
使用 Qwen3-TTS Voice Design API 生成播客音频。

从 markdown 文件解析对话脚本，为每个角色设计独立的声音，
逐行调用 TTS API 生成音频，最后用 ffmpeg 合成为完整播客。
"""

import re
import os
import sys
import time
import httpx
import subprocess
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────────────
API_BASE = "http://192.168.0.102:8000"
API_KEY = "1234"
MODEL = "Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit"
SCRIPT_FILE = Path(__file__).parent / "docs/_drafts/openclaw-podcast.md"
OUTPUT_DIR = Path(__file__).parent / "podcast_output"
FINAL_OUTPUT = OUTPUT_DIR / "openclaw_podcast.mp3"

# 每句话之间的停顿（秒）
PAUSE_BETWEEN_LINES = 0.6
# 不同说话人切换时的额外停顿
PAUSE_SPEAKER_CHANGE = 0.8

# ── 角色声音设计 ──────────────────────────────────────────────
VOICE_DESIGNS = {
    "Aaron": (
        "一位40岁成熟男性，声音低沉浑厚，普通话略带重庆口音。"
        "语速略快，语调偶尔升高富有感染力，讲关键情节时会稍作停顿增强画面感。"
        "整体风格沉稳大气，像一位有阅历的主持人。"
    ),
    "Devon": (
        "一位25岁男性程序员，声音清亮年轻，略带自信和犹豫交替的语气。"
        "语速时快时慢，讲技术内容时自信流畅，偶尔会轻微结巴。"
        "音色偏中性，吐字清晰，略带思考感。类似Elon Musk讲话风格，偏自信。"
    ),
    "Eve": (
        "一位25岁年轻女性，声音响亮轻快，普通话标准带一点北京腔。"
        "语速略快，是大气御姐型，音色明亮有穿透力。"
        "说话干练利落，偶尔带有俏皮的语调变化。"
    ),
    "Muse": (
        "一位30岁魅力女性，声音性感磁性，语速适中。"
        "普通话带一点上海口音的柔美，英语为伦敦腔。"
        "自信从容，在适当的时候展示魅惑感，声音有画面感，像一位知性优雅的女性。"
    ),
}


def parse_script(filepath: Path) -> list[tuple[str, str]]:
    """解析 markdown 播客脚本，提取 (说话人, 台词) 列表。"""
    text = filepath.read_text(encoding="utf-8")

    # 跳过 HTML 注释中的元数据
    lines = []
    in_comment = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("<!--"):
            in_comment = True
            continue
        if stripped.endswith("-->"):
            in_comment = False
            continue
        if in_comment:
            continue
        if not stripped:
            continue
        lines.append(stripped)

    # 解析对话行: "Speaker: text" 或 "Speaker：text"
    dialogues = []
    pattern = re.compile(r"^(\w+)\s*[:：]\s*(.+)$")

    for line in lines:
        m = pattern.match(line)
        if m:
            speaker = m.group(1)
            content = m.group(2).strip()
            if speaker in VOICE_DESIGNS and content:
                dialogues.append((speaker, content))

    return dialogues


def generate_audio(text: str, instructions: str, output_path: Path) -> bool:
    """调用 Qwen3-TTS Voice Design API 生成一段语音。"""
    payload = {
        "model": MODEL,
        "input": text,
        "task_type": "VoiceDesign",
        "instructions": instructions,
        "language": "Chinese",
        "response_format": "wav",
        "max_new_tokens": 4096,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    try:
        with httpx.Client(timeout=300.0) as client:
            resp = client.post(
                f"{API_BASE}/v1/audio/speech",
                json=payload,
                headers=headers,
            )

        if resp.status_code != 200:
            print(f"  [ERROR] HTTP {resp.status_code}: {resp.text[:200]}")
            return False

        # 检查是否返回了 JSON 错误
        content_type = resp.headers.get("content-type", "")
        if "application/json" in content_type:
            print(f"  [ERROR] Server returned JSON: {resp.text[:200]}")
            return False

        output_path.write_bytes(resp.content)
        return True

    except httpx.TimeoutException:
        print(f"  [ERROR] Request timed out")
        return False
    except httpx.ConnectError:
        print(f"  [ERROR] Cannot connect to {API_BASE}")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def concat_audio(files: list[Path], output: Path):
    """使用 ffmpeg 将多段音频拼接为最终播客文件。"""
    # 创建 ffmpeg concat 文件列表
    concat_file = OUTPUT_DIR / "concat_list.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for fp in files:
            # ffmpeg concat 需要转义特殊字符
            escaped = str(fp).replace("'", "'\\''")
            f.write(f"file '{escaped}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-ar", "24000",
        str(output),
    ]

    print(f"\n合成最终音频: {output}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}")
        sys.exit(1)

    print(f"完成! 最终文件: {output}")
    print(f"文件大小: {output.stat().st_size / 1024 / 1024:.1f} MB")


def generate_pause_wav(duration: float, output_path: Path):
    """生成一段静音 WAV 文件。"""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=r=24000:cl=mono",
        "-t", str(duration),
        "-c:a", "pcm_s16le",
        str(output_path),
    ]
    subprocess.run(cmd, capture_output=True, text=True)


def main():
    print("=" * 60)
    print("  播客生成器 - Qwen3-TTS Voice Design")
    print("=" * 60)

    # 检查 API 连通性
    print(f"\n检查 API 连通性: {API_BASE}")
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{API_BASE}/v1/models", headers={"Authorization": f"Bearer {API_KEY}"})
            if resp.status_code == 200:
                models = resp.json()
                model_ids = [m.get("id", "") for m in models.get("data", [])]
                print(f"  可用模型: {model_ids}")
            else:
                print(f"  API 返回 {resp.status_code}, 继续尝试...")
    except Exception as e:
        print(f"  [WARNING] 无法获取模型列表: {e}")

    # 解析脚本
    print(f"\n解析脚本: {SCRIPT_FILE}")
    dialogues = parse_script(SCRIPT_FILE)
    print(f"  共解析到 {len(dialogues)} 条对话")

    # 统计各角色台词数
    speaker_counts = {}
    for speaker, _ in dialogues:
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
    for speaker, count in speaker_counts.items():
        print(f"    {speaker}: {count} 条")

    # 创建输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 生成静音文件用于间隔
    pause_short = OUTPUT_DIR / "pause_short.wav"
    pause_long = OUTPUT_DIR / "pause_long.wav"
    generate_pause_wav(PAUSE_BETWEEN_LINES, pause_short)
    generate_pause_wav(PAUSE_BETWEEN_LINES + PAUSE_SPEAKER_CHANGE, pause_long)

    # 逐行生成音频
    audio_files = []
    prev_speaker = None
    failed = 0

    for i, (speaker, text) in enumerate(dialogues):
        # 显示进度
        short_text = text[:50] + "..." if len(text) > 50 else text
        print(f"\n[{i+1}/{len(dialogues)}] {speaker}: {short_text}")

        # 如果说话人切换，使用较长停顿
        if prev_speaker and prev_speaker != speaker:
            audio_files.append(pause_long)
        elif prev_speaker:
            audio_files.append(pause_short)

        # 生成音频
        out_path = OUTPUT_DIR / f"line_{i:03d}_{speaker}.wav"
        instructions = VOICE_DESIGNS[speaker]

        success = generate_audio(text, instructions, out_path)
        if success:
            size_kb = out_path.stat().st_size / 1024
            print(f"  -> {out_path.name} ({size_kb:.0f} KB)")
            audio_files.append(out_path)
            prev_speaker = speaker
        else:
            failed += 1
            print(f"  -> 跳过该行")
            # 重试一次
            print(f"  重试...")
            time.sleep(2)
            success = generate_audio(text, instructions, out_path)
            if success:
                size_kb = out_path.stat().st_size / 1024
                print(f"  -> 重试成功: {out_path.name} ({size_kb:.0f} KB)")
                audio_files.append(out_path)
                prev_speaker = speaker
            else:
                print(f"  -> 重试失败，跳过")

    if not audio_files:
        print("\n没有成功生成任何音频文件!")
        sys.exit(1)

    # 合成最终播客
    valid_files = [f for f in audio_files if f.exists()]
    if valid_files:
        concat_audio(valid_files, FINAL_OUTPUT)
    else:
        print("\n没有有效的音频文件可合成!")
        sys.exit(1)

    # 统计
    print(f"\n{'=' * 60}")
    print(f"  生成统计:")
    print(f"    成功: {len(dialogues) - failed} / {len(dialogues)}")
    print(f"    失败: {failed}")
    print(f"    输出: {FINAL_OUTPUT}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
