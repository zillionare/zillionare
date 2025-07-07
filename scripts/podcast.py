# 将plain text的对话文件，转换为格式化文件（使用admonition）

input_text = '''**Flora**: 量化好声音 睡前听一听。欢迎大家，我是 Flora
**Aaron**: 我是Aaron
**Flora**: 常常有粉丝来问，我很想入行量化，但是简历就过不了关，怎么办？
**Flora**: Aaron你也招过一些量化研究员了，你能不能给大家支个招，你愿意招什么样的人？
**Aaron**: 好的，这方面可以分享的招数比较多。今天先给大家讲一招，就是打比赛。
**Flora**: 打比赛？能具体一点吗？'''

from pathlib import Path

import fire


def to_gmf_admonition(lines: list[str]):
    output = []
    last_speaker = None
    for line in lines:
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
            if speaker == 'Flora':
                output.append('>[!tip] Flora: ' + content)
            elif speaker == 'Aaron':
                output.append('>[!note]Aaron: ' + content)
            else:
                output.append('> ' + line.strip())
        else:
            output.append('> ' + content)
        last_speaker = speaker

    return output

def pretty(src: str, dst: Path|str=""):
    src_ = Path(src)
    if dst == "":
        dst = Path("/tmp/") / src_.name

    with open(src, "r", encoding = "utf-8") as f:
        lines = f.readlines()

    output = to_gmf_admonition(lines)
    
    with open(dst, "w", encoding = "utf-8") as f:
        f.write('\n'.join(output))

    print(f"output: {dst}")


def test():
    lines = input_text.split('\n')
    output = to_gmf_admonition(lines)
    print('\n'.join(output))

fire.Fire({
    'pretty': pretty,
    "test": test
})
