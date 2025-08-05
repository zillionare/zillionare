# 将plain text的对话文件，转换为格式化文件（使用admonition）

input_text = '''**Flora**: 量化好声音 睡前听一听。欢迎大家，我是 Flora
**Aaron**: 我是Aaron
**Flora**: 常常有粉丝来问，我很想入行量化，但是简历就过不了关，怎么办？
**Flora**: Aaron你也招过一些量化研究员了，你能不能给大家支个招，你愿意招什么样的人？
**Aaron**: 好的，这方面可以分享的招数比较多。今天先给大家讲一招，就是打比赛。
**Flora**: 打比赛？能具体一点吗？'''

import base64
import os
import re
import subprocess
from pathlib import Path
from typing import Union

import arrow
import fire
import requests


def upload_audio_to_github(audio_path: str, year: int, month: int) -> str:
    """上传音频文件到 GitHub podcast 仓库

    Args:
        audio_path: 本地音频文件路径
        year: 年份
        month: 月份
        seq: 序号

    Returns:
        上传后的文件 URL
    """
    audio_file = Path(audio_path)
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # 目标文件名
    target_filename = audio_file.name.lower()
    target_path = f"{year:04d}/{month:02d}/{target_filename}"

    # 使用 gh CLI 上传文件
    try:
        # 首先克隆或切换到 podcast 仓库
        podcast_repo_url = "git@github.com:zillionare/podcast.git"
        temp_dir = Path("/tmp/podcast_upload")

        # 清理并创建临时目录
        if temp_dir.exists():
            subprocess.run(["rm", "-rf", str(temp_dir)], check=True)

        # 克隆仓库
        subprocess.run([
            "git", "clone", podcast_repo_url, str(temp_dir)
        ], check=True)

        # 创建目标目录
        target_dir = temp_dir / f"{year:04d}" / f"{month:02d}"
        target_dir.mkdir(parents=True, exist_ok=True)

        # 复制音频文件
        target_file = target_dir / target_filename

        # 检查文件是否已存在且内容相同
        if target_file.exists():
            # 比较文件内容
            with open(audio_file, 'rb') as f1, open(target_file, 'rb') as f2:
                if f1.read() == f2.read():
                    print(f"✅ Audio file already exists and is identical: {target_path}")
                    cdn_url = f"https://cdn.jsdelivr.net/gh/zillionare/podcast@main/{target_path}"
                    return cdn_url

        subprocess.run(["cp", str(audio_file), str(target_file)], check=True)

        # 提交并推送
        os.chdir(temp_dir)
        subprocess.run(["git", "add", "."], check=True)

        # 检查是否有变更需要提交
        result = subprocess.run(["git", "diff", "--staged", "--quiet"], capture_output=True)
        if result.returncode == 0:
            print(f"✅ Audio file already up to date: {target_path}")
            cdn_url = f"https://cdn.jsdelivr.net/gh/zillionare/podcast@main/{target_path}"
            return cdn_url

        subprocess.run([
            "git", "commit", "-m", f"Add podcast {target_filename} audio for {year:04d}-{month:02d}"
        ], check=True)
        subprocess.run(["git", "push"], check=True)

        # 返回 CDN URL
        cdn_url = f"https://cdn.jsdelivr.net/gh/zillionare/podcast@main/{target_path}"
        print(f"✅ Audio uploaded successfully: {cdn_url}")
        return cdn_url

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to upload audio: {e}")
        raise
    finally:
        # 清理临时目录
        if temp_dir.exists():
            subprocess.run(["rm", "-rf", str(temp_dir)], capture_output=True)


def to_gmf_admonition(lines: list[str]):
    output = []
    last_speaker = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ':' in line or "：" in line:
            speaker, content = re.split(r'[:：]', line, 1)
            speaker = speaker.strip('* ').capitalize()  # 首字母大写
            content = content.strip()
        else:
            speaker, content = '', line.strip()

        if content == '':
            continue

        if speaker != last_speaker:
            if last_speaker is not None:
                output.append('')  # 插入空行
            if speaker.lower() == 'flora':
                output.append('>[!tip] Flora: ' + content)
            elif speaker.lower() == 'aaron':
                output.append('>[!note] Aaron: ' + content)
            else:
                output.append('> ' + line.strip())
        else:
            output.append('> ' + content)
        last_speaker = speaker

    return output

def pretty(src: str, dst: Union[Path, str]=""):
    src_ = Path(src)
    if dst == "":
        dst = Path(__file__).parent.parent / "docs/podcast" / src_.name

    with open(src, "r", encoding = "utf-8") as f:
        lines = f.readlines()

    output = to_gmf_admonition(lines)
    
    with open(dst, "w", encoding = "utf-8") as f:
        f.write('\n'.join(output))

    print(f"output: {dst}")

def to_cm_admonition(lines: list[str]):
    output = []
    last_speaker = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ':' in line:
            speaker, content = line.split(':', 1)
            speaker = speaker.strip('* ')
            content = content.strip()
        else:
            speaker, content = '', line.strip()

        if content == '':
            continue

        if speaker != last_speaker:
            if last_speaker is not None:
                output.append('')  # 插入空行
            if speaker:
                # CommonMark格式的admonition，说话人作为title
                admon_type = "tip" if speaker == "Flora" else "note"
                output.append(f'!!! {admon_type} "{speaker}"')
                output.append(f'    {content}')
            else:
                output.append(content)
        else:
            if speaker:
                output.append(f'    {content}')
            else:
                output.append(content)
        last_speaker = speaker

    return output

def to_commonmark(src: str, dst: Union[Path, str]="", seq=1):
    """将对话文本转换为CommonMark格式的admonition

    Args:
        src: 源文件路径
        dst: 目标文件路径，默认为/tmp/源文件名
        seq: 播客序号，用于生成音频链接
    """
    src_ = Path(src)
    if dst == "":
        dst = Path(__file__).parent.parent / "docs/podcast" / src_.name

    with open(src, "r", encoding = "utf-8") as f:
        lines = f.readlines()

    output = to_cm_admonition(lines)

    year = arrow.now().year
    month = arrow.now().month

    # 从文件名中提取序号，如果没有则使用传入的seq
    filename_match = re.match(r'^(\d+)', src_.stem)
    if filename_match:
        seq = int(filename_match.group(1))

    frontmatter = [
        "---",
        "title: " + src_.stem,
        "description: " + src_.stem,
        "date: " + arrow.now().format("YYYY-MM-DD"),
        "audio: " + f"https://cdn.jsdelivr.net/gh/zillionare/podcast@main/{year:04d}/{month:02d}/{seq:02d}-final.mp3",
        "---",
        ""
    ]

    with open(dst, "w", encoding = "utf-8") as f:
        f.write("\n".join(frontmatter))
        f.write('\n'.join(output))

    print(f"output: {dst}")
    return dst

def to_alternating_paragraphs(lines: list[str]):
    output = []
    is_odd = True  # 用于交替背景色

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 处理 GMF admonition 格式
        if line.startswith('>[!tip] ') or line.startswith('>[!note] '):
            # 提取说话人和内容
            if line.startswith('>[!tip] '):
                content = line[8:]  # 去掉 '>[!tip] '
            else:  # >[!note]
                content = line[9:]  # 去掉 '>[!note] '

            if ':' in content:
                speaker, text = content.split(':', 1)
                speaker = speaker.strip()
                text = text.strip()
            else:
                speaker, text = '', content.strip()
        elif line.startswith('> '):
            # 处理续行内容
            text = line[2:]  # 去掉 '> '
            speaker = ''
        elif ':' in line:
            # 处理原始格式
            speaker, text = line.split(':', 1)
            speaker = speaker.strip('* ')
            text = text.strip()
        else:
            speaker, text = '', line.strip()

        if text == '':
            continue

        # 交替背景色的CSS类
        bg_class = "bg-light" if is_odd else "bg-dark"
        is_odd = not is_odd

        if speaker:
            # 说话人加粗显示
            output.append(f'<div class="{bg_class}"><p><strong>{speaker}</strong>: {text}</p></div>')
        else:
            output.append(f'<div class="{bg_class}"><p>{text}</p></div>')

    # 添加必要的CSS样式
    css = """
<style>
.bg-light {
    background-color: #fcfefe;
    padding: 10px 15px;
    margin-bottom: 5px;
    border-radius: 5px;
}
.bg-dark {
    background-color: #f8f9fa;
    padding: 10px 15px;
    margin-bottom: 5px;
    border-radius: 5px;
}
</style>
"""
    output.insert(0, css)
    return output

def to_alternating(src: str, audio: str, dst: Union[Path, str]=""):
    """将对话文本转换为交替背景色的段落，说话人加粗显示

    Args:
        src: 源文件路径（pretty 命令的输出）
        audio: 音频文件路径
        dst: 目标文件路径，默认为docs/podcast/源文件名
    """
    src_ = Path(src)

    # 如果src_是相对路径，则将其转换为相对于docs/podcast下的文件路径
    if not src_.is_absolute():
        src_ = Path(__file__).parent.parent / "docs/podcast" / src_

    if dst == "":
        dst = Path(__file__).parent.parent / "docs/podcast" / src_
    else:
        dst = Path(dst)

    # 确保目标目录存在
    dst.parent.mkdir(parents=True, exist_ok=True)

    with open(src_, "r", encoding = "utf-8") as f:
        lines = f.readlines()

    output = to_alternating_paragraphs(lines)

    # 生成frontmatter
    year = arrow.now().year
    month = arrow.now().month

    # 上传音频文件到 GitHub
    audio_name = Path(audio).name.lower()
    try:
        audio_url = upload_audio_to_github(audio, year, month)
    except Exception as e:
        print(f"⚠️  Failed to upload audio, using placeholder URL: {e}")
        audio_url = f"https://cdn.jsdelivr.net/gh/zillionare/podcast@main/{year:04d}/{month:02d}/{audio_name}"

    frontmatter = [
        "---",
        "title: " + src_.stem,
        "description: " + src_.stem,
        "date: " + arrow.now().format("YYYY-MM-DD"),
        "audio: " + audio_url,
        "---",
        ""
    ]

    with open(dst, "w", encoding = "utf-8") as f:
        f.write("\n".join(frontmatter))
        f.write('\n'.join(output))

    print(f"output: {dst}")

    # 自动更新索引
    print("Updating podcast index...")
    update_podcast_index()
    print("Podcast published successfully!")

    return dst

def update_podcast_index():
    """更新播客索引页面，扫描所有播客文件并生成索引"""
    podcast_dir = Path(__file__).parent.parent / "docs/podcast"
    index_file = podcast_dir / "index.md"

    # 获取所有播客文件
    podcast_files = []
    for md_file in podcast_dir.glob("*.md"):
        if md_file.name == "index.md":
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_text = parts[1]

                    # 简单解析frontmatter
                    title = ""
                    description = ""
                    date = ""
                    audio = ""

                    for line in frontmatter_text.strip().split('\n'):
                        if line.startswith('title:'):
                            title = line.split(':', 1)[1].strip()
                            # 去掉标题两端的引号
                            if title.startswith('"') and title.endswith('"'):
                                title = title[1:-1]
                            elif title.startswith("'") and title.endswith("'"):
                                title = title[1:-1]
                        elif line.startswith('description:'):
                            description = line.split(':', 1)[1].strip()
                            # 去掉两站的引号
                            if description.startswith('"') and description.endswith('"'):
                                description = description[1:-1]
                            elif description.startswith("'") and description.endswith("'"):
                                description = description[1:-1]
                        elif line.startswith('date:'):
                            date = line.split(':', 1)[1].strip()
                        elif line.startswith('audio:'):
                            audio = line.split(':', 1)[1].strip()

                    podcast_files.append({
                        'filename': md_file.name,
                        'title': title,
                        'description': description,
                        'date': date,
                        'audio': audio,
                        'url': f"/podcast/{md_file.stem}/"
                    })
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    # 按日期排序（最新的在前）
    podcast_files.sort(key=lambda x: x['date'], reverse=True)

    # 生成索引页面内容
    index_content = generate_podcast_index_content(podcast_files)

    # 写入索引文件
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f"Updated podcast index with {len(podcast_files)} episodes.")

def generate_podcast_index_content(podcast_files):
    """生成播客索引页面内容"""
    content = """---
title: 量化好声音播客
---

<div class="podcast-grid">
"""

    for podcast in podcast_files:
        content += f"""  <div class="podcast-card">
    <div class="podcast-info">
      <h3><a href="{podcast['url']}">{podcast['title']}</a></h3>
      <p class="podcast-date">{podcast['date']}</p>
      <p class="podcast-desc">{podcast['description']}</p>
      {f'<audio controls><source src="{podcast["audio"]}" type="audio/mpeg">您的浏览器不支持音频播放。</audio>' if podcast['audio'] else ''}
    </div>
  </div>
"""

    content += """</div>

<style>
.podcast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.podcast-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: #fff;
}

.podcast-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.podcast-info {
  padding: 20px;
}

.podcast-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.2em;
}

.podcast-info h3 a {
  text-decoration: none;
  color: #333;
}

.podcast-info h3 a:hover {
  color: #007acc;
}

.podcast-date {
  color: #666;
  font-size: 0.9em;
  margin: 5px 0;
}

.podcast-desc {
  font-size: 0.95em;
  color: #555;
  margin: 10px 0;
  line-height: 1.4;
}

.podcast-info audio {
  width: 100%;
  margin-top: 15px;
}
</style>
"""

    return content

def test():
    lines = input_text.split('\n')
    output = to_gmf_admonition(lines)
    print('\n'.join(output))

if __name__ == "__main__":
    fire.Fire({
        'pretty': pretty,
        'jieyu': to_alternating,
        "reindex": update_podcast_index,
        "test": test
    })
