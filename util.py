#! /home/aaron/miniconda3/envs/coursea/bin/python
"""
deploy courseware (teacher/student) to coursea.jieyu.ai

转换md为pdf命令，在mac下运行：

pandoc --pdf-engine=weasyprint -f markdown -t pdf  -V mainfont='WenQuanYi Micro Hei' -V geometry:"top=2cm,bottom=2cm,left=2cm,right=2cm" input.md  > output.pdf

"""

import logging
import os
import re
import shutil
from typing import List

import fire

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("tonotebook")


def to_myst_img(lines: List[str]):
    buffer = []
    for line in lines:
        matched = re.match(r".*!\[(\d*%?)\]\((.+)\).*", line)
        if matched is not None:
            width, link = matched.groups()

            width = width or "100%"
            repl = f"\n```{{figure}} {link}\n:width: {width}\n:align: center\n```"

            line = re.sub(r"!\[(\d*%?)\]\((.+)\)", repl, line)

        buffer.append(line)
    return buffer


def seek_adnomition_end(i, lines):
    for m in range(i, len(lines)):
        # 防止在!!! tip之后出现空行
        if lines[m] == "":
            continue

        if not (lines[m].startswith("    ") or lines[m].startswith("\t")):
            return m


def replace_adnomition(lines, i, m):
    matched = re.search(r"(tip|warning|note|attention)", lines[i], flags=re.I)
    if matched is not None:
        tag = matched.group(1).lower()
    else:
        logger.warning("unsupported adnomitioin: %s", lines[i])
        tag = "admonition"

    return [f"``` {{{tag}}}", *(lines[i + 1 : m]), "```"]


def to_myst_adnomition(lines: List[str]):
    buffer = []
    i: int = 0

    for j in range(len(lines)):
        if i >= len(lines):
            break

        line = lines[i]
        if line.startswith("!!!"):
            m = seek_adnomition_end(i + 1, lines)
            repl = replace_adnomition(lines, i, m)

            buffer.extend(repl)
            i = m
            continue
        else:
            buffer.append(line)
            i += 1

    return buffer


def strip_front_matter(content: str):
    pattern = r"\n*---\n.+---\n+"
    title = re.match(r"---\n.*title:\s*([^\n]+)\n.*\n---", content, re.I | re.DOTALL)
    if title is not None:
        title = f"# {title.group(1)}\n"
    else:
        title = ""

    return re.sub(pattern, title, content, flags=re.DOTALL)


def preprocess(in_file: str, out_file: str):
    with open(in_file, "r") as f:
        content = f.read()
        content = strip_front_matter(content)

        lines = content.split("\n")

        lines = to_myst_adnomition(lines)
        lines = to_myst_img(lines)

        with open(out_file, "w") as f:
            f.write("\n".join(lines))


def convert_to_ipynb(in_file: str):
    stem = os.path.splitext(os.path.basename(in_file))[0]

    preprocessed = os.path.join("/tmp/", f"{stem}.md")
    preprocess(in_file, preprocessed)

    out_dir = os.path.dirname(in_file)
    out_file = os.path.join(out_dir, f"{stem}.ipynb")
    print(f"converting {preprocessed} to {out_file}")

    os.system(f"notedown --match=python {preprocessed} > {out_file}")
    return out_file


def to_notebook(chap: str):
    if not chap.endswith(".md"):
        chap += ".md"

    infile = os.path.join("/apps/cheese_course/docs/courseware/notes", chap)
    return convert_to_ipynb(infile)


def preview(chap: str):
    converted = to_notebook(chap)

    print(f"scp {converted} to remote")
    os.system(f"scp {converted} omega:/tmp/")

    file = os.path.basename(converted)
    docker_cp_cmd = (
        f"ssh root@omega 'docker cp /tmp/{file} course_aaron:/home/aaron/notebooks/'"
    )
    os.system(docker_cp_cmd)


def deploy(chap: str):
    converted = to_notebook(chap)

    print(f"scp {converted} to remote")
    os.system(f"scp {converted} omega:/data/course/notebooks/courseware/")


def _find_comments_end(lines, istart) -> int:
    for iend in range(istart, len(lines)):
        line = lines[iend]
        if re.match(r"-->\s*\n\s*", line):
            return iend
    else:
        if not lines[-1].endswith("-->"):
            raise ValueError(f"发现未配对注释：{istart}")
        else:
            raise ValueError(f"Something wrong with paring last line: {lines[-1]}")


def _split_by_punctuation(lines: List[str]):
    lines = "".join(lines)
    stripped = re.sub(r"<!--\s*", "", lines)
    stripped = re.sub(r"\s*-->\s*", "", stripped)

    trans = str.maketrans(
        {
            ",": "\n",
            "。": "\n",
            ";": "\n",
            "；": "\n",
            "，": "\n",
            "?": "?\n",
            "？": "？\n",
        }
    )

    return "\n<!--\n" + stripped.translate(trans) + "\n-->\n"


def split_lines(chap: str):
    """对slide稿按标点符号切分成行"""
    if not chap.endswith(".md"):
        chap = chap + ".md"

    file = os.path.join("/apps/cheese_course/docs/courseware/pages/", chap)
    with open(file, "r") as f:
        lines = f.readlines()

    buffer = []
    istart = 0
    while istart < len(lines):
        line = lines[istart]
        if line.startswith("<!--"):
            iend = _find_comments_end(lines, istart)
            buffer.append(_split_by_punctuation(lines[istart:iend]))
            istart = iend + 1
        else:
            istart += 1
            buffer.append(line)

    tmp_file = os.path.join("/tmp/", chap)
    bak_file = os.path.join("/tmp/", f"{chap}.bak")
    with open(tmp_file, "w") as f:
        f.write("".join(buffer))

    shutil.copyfile(file, bak_file)
    shutil.copyfile(tmp_file, file)


def subtitles(file: str):
    """从pages中提取subtitles"""
    if file.startswith("~"):
        file = os.path.expanduser(file)
    elif not file.startswith("/"):
        file = os.path.expanduser(file)

    lines = []
    with open(file, "r") as f:
        content = f.read(-1)
        try:
            lines = re.findall(r"<!--(.*?)-->", content, re.S)
        except Exception as e:
            print(content)

    basename = os.path.basename(file)
    with open(f"./subtitles-{basename}.txt", "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    fire.Fire(
        {
            "subtitles": subtitles,
        }
    )
