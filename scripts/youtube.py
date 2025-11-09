"""给 youtube 视频加中文字幕

1. 先通过 download 4k 下载
2. 在youtube 上通过转写、复制原始字幕
3. 通过本工具将字幕切分
4. 调用 AI 翻译
5. 合并翻译后的字幕

"""

import fire

from pathlib import Path
import re


def split_srt(path: str, end_time: str = None):
    file = Path(path).expanduser()
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    timestamps = ["00:00:00.000"]
    for i in range(len(lines)):  # type: ignore
        if re.match(r"^\d+:\d+", lines[i]):
            time = lines[i].split(":")
            mm = int(time[0])
            ss = int(time[1])
            timestamps.append(f"00:{mm:02d}:{ss:02d}.000")

    if end_time is not None:
        timestamps.append(end_time)
    else:
        timestamps.append(timestamps[-1])

    j = 0
    m = 0
    buffers = []
    for i in range(len(lines)):
        line = lines[i]
        if re.match(r"^\d+:\d+", line):
            j += 1
            buffers.append(f"\n{j}\n")
            line = timestamps[j] + " --> " + timestamps[j + 1] + "\n"
            buffers.append(line)
            continue

        buffers.append(line)
        if len(buffers) > 100:
            m += 1
            to = file.parent / f"srt/{m:02d}.srt"
            with open(to, "w", encoding="utf-8") as f:
                f.writelines(buffers)
                buffers = []

    to = file.parent / f"srt/{m:02d}.srt"
    if len(buffers) > 0:
        with open(to, "w", encoding="utf-8") as f:
            f.writelines(buffers)


def merge_srt(folder: str):
    buffers = []
    for i in range(1, 17):
        print(f"processing {i:02d}")
        file = Path(f"{folder}/{i:02d}-translated.srt").expanduser()
        with open(file, "r", encoding="utf-8") as f:
            buffers.extend(f.readlines())

    to = Path(f"{folder}/translated.srt").expanduser()

    answer = input(f"output: {to}, continue? [y/n]")
    if answer != "y":
        print("放弃写入")
        return

    with open(to, "w", encoding="utf-8") as f:
        f.writelines(buffers)


fire.Fire(
    {
        "split_srt": split_srt,
    }
)
