import datetime
import glob
import os
import random
import re
import shlex
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import List, Optional

import arrow
import black
import fire
import frontmatter
import nbformat
import requests
from loguru import logger

quantide_api_url = os.environ.get("QUANTIDE_API_URL")

API_TOKEN = os.environ.get("QUANTIDE_API_TOKEN")

pictures = [
    "https://images.jieyu.ai/images/hot/adventure.jpg",
    "https://images.jieyu.ai/images/hot/mybook/book-by-hand.jpg",
    "https://images.jieyu.ai/images/hot/mybook/book-on-curtain.png",
    "https://images.jieyu.ai/images/hot/mybook/book-with-course.png",
    "https://images.jieyu.ai/images/hot/mybook/book-with-flower.png",
    "https://images.jieyu.ai/images/hot/mybook/book-with-hand.jpg",
    "https://images.jieyu.ai/images/hot/mybook/by-swimming-pool.jpg",
    "https://images.jieyu.ai/images/hot/mybook/christmas.jpg",
    "https://images.jieyu.ai/images/hot/mybook/gift.jpg",
    "https://images.jieyu.ai/images/hot/mybook/girl-hold-book-face.jpg",
    "https://images.jieyu.ai/images/hot/mybook/girl-on-sofa.jpg",
    "https://images.jieyu.ai/images/hot/mybook/girl-reading.png",
    "https://images.jieyu.ai/images/hot/mybook/iphone-6.jpg",
    "https://images.jieyu.ai/images/hot/mybook/mac-and-book.jpg",
    "https://images.jieyu.ai/images/hot/mybook/mac-cd-book.jpg",
    "https://images.jieyu.ai/images/hot/mybook/man-wearing-tank-top.jpg",
    "https://images.jieyu.ai/images/hot/mybook/men-wearing-tank.jpg",
    "https://images.jieyu.ai/images/hot/mybook/poster-on-wall.jpg",
    "https://images.jieyu.ai/images/hot/mybook/promotion-long.png",
    "https://images.jieyu.ai/images/hot/mybook/reading-content.jpg",
    "https://images.jieyu.ai/images/hot/mybook/screen-shot-and-book.png",
    "https://images.jieyu.ai/images/hot/mybook/sports-bra-1.jpg",
    "https://images.jieyu.ai/images/hot/mybook/sports-bra-2.jpg",
    "https://images.jieyu.ai/images/hot/mybook/swimsuit.jpg",
    "https://images.jieyu.ai/images/hot/mybook/three-books.png",
    "https://images.jieyu.ai/images/hot/mybook/women-holding-swear.jpg",
    "https://images.jieyu.ai/images/hot/mybook/women-sweatshirt-indoor.jpg",
    "https://images.jieyu.ai/images/university/Mackey_Auditorium-Colorado.jpg",
    "https://images.jieyu.ai/images/university/university-college-london-library.jpg",
    "https://images.jieyu.ai/images/university/ucl-wilkins-building.jpg",
]

img_mode = "card-img-top"

github_item = """
<div>
<h3>{title}</h3>
<img src="{img_url}" style="height: 200px" align="right"/>
<p><span>内容摘要:<br></span>{excerpt}</p>

<p><span style="margin-right:20px">发表于 {date} 人气 {readers} </span><span><a href="{link}">点击阅读</a></span></p>

</div><!--end-article-->
<br/>
<br/>
"""

web_item = """
<div class="card">
    <a href="{link}">
    <img class="{img_mode} img-responsive" src="{img_url}"/>
    <div class="card-body">
        <h4 class="card-title">{title}</h4>
        <p class="card-text">{excerpt}</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>{date}</small></p>
    </div>
    </a>
</div><!--end-card-->
"""

container_tpl = """
<div class="as-grid m-t-md">
<div class="card-columns">
    {cards}
</div>
</div>
"""

mystAdmons = {
    "info": "hint",
    "hint": "hint",
    "warning": "warning",
    "attention": "warning",
    "note": "note",
    "tip": "tip",
    "failure": "error",
    "more": "seealso",
    "important": "important",
    "bug": "error",
}


def get_copyrights() -> str:
    copyright = """\n```{attention} 版权声明
本课程全部文字、图片、代码、习题等所有材料，除声明引用外，版权归<b>匡醍</b>所有。所有草稿版本均通过第三方服务进行管理，作为拥有版权的证明。未经作者书面授权，请勿引用和传播。联系我们：公众号 Quantide\n```"""

    return copyright


def absolute_path(path: Path) -> Path:
    if not path.is_absolute():
        return (Path(__file__).parent / path).expanduser()
    else:
        return path.expanduser()


def update_notebook_metadata(
    notebook_path: Path,
    title: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    publish_date: Optional[datetime.datetime] = None,
    img: Optional[str] = None,
) -> bool:
    """更新 notebook 的 metadata,来自provision系统

    Args:
        notebook_path: notebook 文件路径
        title: 标题
        description: 描述
        price: 价格
        publish_date: 发布日期
        img: 图片 URL

    Returns:
        bool: 更新是否成功
    """
    try:
        # 读取 notebook
        nb = nbformat.read(notebook_path, as_version=4)

        # 获取当前 metadata
        metadata = nb.get("metadata", {})

        # 更新 metadata
        if title is not None:
            metadata["title"] = title
        if description is not None:
            metadata["excerpt"] = description
        if price is not None:
            metadata["price"] = price
        if publish_date is not None:
            metadata["date"] = publish_date.strftime("%Y-%m-%d %H:%M:%S")
        if img is not None:
            metadata["img"] = img

        # 设置更新后的 metadata
        nb["metadata"] = metadata

        # 写入 notebook
        nbformat.write(nb, notebook_path)

        return True
    except Exception as e:
        logger.error(f"Error updating notebook metadata: {e}")
        return False


def seek_adnomition_end(i, lines):
    """
    寻找 admonition 块的结束位置
    规则：
    1. 遇到连续两个空行时结束，但要忽略 fenced code blocks 内部的空行
    2. 遇到新的 admonition 开始行（!!! 开头）时结束
    3. 其它情况都不算结束
    """
    in_fenced_block = False
    fenced_pattern = re.compile(r"^\s*```")
    consecutive_empty_lines = 0

    for m in range(i, len(lines)):
        line = lines[m]

        # 特殊处理：如果遇到新的 admonition 开始，则结束当前 admonition
        if line.startswith("!!!"):
            return m

        # 检查是否进入或退出 fenced code block
        if fenced_pattern.match(line):
            in_fenced_block = not in_fenced_block
            consecutive_empty_lines = 0  # 重置空行计数
            continue

        # 如果不在 fenced code block 内，检查空行和缩进
        if not in_fenced_block:
            if line == "":
                consecutive_empty_lines += 1
                # 如果遇到连续两个空行，则结束 admonition
                if consecutive_empty_lines >= 2:
                    return m - 1  # 返回第一个空行的位置
            else:
                # 检查是否是有效的 admonition 内容行（以4个空格或制表符开头）
                if not (line.startswith("    ") or line.startswith("\t")):
                    # 遇到非缩进行，admonition 结束
                    return m
                consecutive_empty_lines = 0  # 重置空行计数

    return len(lines)


def replace_adnomition(lines, i, m):
    """replace indented lines to myst adnomition due to myst 2.4.2 bug
    使用4个反引号以避免嵌套fenced code blocks的问题"""
    # 匹配类型和可能的标题（两种格式：带引号和不带引号）
    matched = re.search(
        r"(tip|warning|note|attention|hint|more|info|important|failure|bug)(?:\s+\"([^\"]+)\"|(?:\s+(.+)))?",
        lines[i],
        flags=re.I,
    )
    tag = "note"
    title = ""

    if matched is not None:
        tag = mystAdmons.get(matched.group(1).lower(), "note")  # 提供默认值
        # 检查两种可能的标题格式
        if matched.group(2):  # 引号包裹的标题
            title = matched.group(2)
        elif matched.group(3):  # 不带引号的标题
            title = matched.group(3)

    content = [line.lstrip(" \t") for line in lines[i + 1 : m]]

    # 如果有标题，则添加到MyST格式中
    if title:
        return [f"```` {{{tag}}} {title}", *content, "````"]
    else:
        return [f"```` {{{tag}}}", *content, "````"]


def to_myst_adnomition(lines: List[str]):
    buffer = []
    i: int = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith("!!!"):
            m = seek_adnomition_end(i + 1, lines)
            repl = replace_adnomition(lines, i, m)

            buffer.extend(repl)
            i = m
        else:
            buffer.append(line)
            i += 1

    return buffer


def replace_admonition_gmf(lines, i, m):
    """
    将 admonition 转换为 GMF 格式
    空行处理：
    - fenced code blocks 内的空行转换为 ">"
    - fenced code blocks 外的空行转换为 "> <br>"
    """
    allowed_types = ["NOTE", "TIP", "CAUTION", "IMPORTANT", "QUESTION", "WARNING"]

    # 提取admonition类型
    matched = re.search(
        r"(tip|warning|note|attention|hint|more|important|caution|question)",
        lines[i],
        flags=re.I,
    )
    admonition_type = "NOTE"
    if matched is not None:
        admonition_type = matched.group(1).upper()
        if admonition_type not in allowed_types:
            admonition_type = "NOTE"

    # 处理内容，移除 admonition 缩进，并跟踪 fenced code blocks
    content = []
    in_fenced_block = False
    fenced_pattern = re.compile(r"^\s*```")

    for line in lines[i + 1 : m]:
        # 移除 admonition 的缩进（4个空格或1个制表符）
        if line.startswith("    "):
            processed_line = line[4:]
        elif line.startswith("\t"):
            processed_line = line[1:]
        else:
            # 空行或其他行保持原样
            processed_line = line

        # 先记录当前的 fenced block 状态
        current_in_fenced = in_fenced_block

        # 然后检查是否进入或退出 fenced code block
        if fenced_pattern.match(processed_line):
            in_fenced_block = not in_fenced_block

        content.append((processed_line, current_in_fenced))

    # 构建GMF格式的admonition
    result = [f">[!{admonition_type}]"]
    for content_line, was_in_fenced in content:
        if content_line == "":
            if was_in_fenced:
                # fenced code blocks 内的空行使用简单的 ">"
                result.append(">")
            else:
                # fenced code blocks 外的空行使用 "> <br>" 来保持原文空行的语义
                result.append("> <br>")
        else:
            result.append(f"> {content_line}")

    return result


def to_gmf_admonition(lines: List[str]):
    """Convert CommonMark admonition format to GitHub Markdown Format (GMF)."""
    buffer = []
    i: int = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith("!!!"):
            m = seek_adnomition_end(i + 1, lines)
            repl = replace_admonition_gmf(lines, i, m)

            buffer.extend(repl)
            i = m
        else:
            buffer.append(line)
            i += 1

    return buffer


def strip_html_comments(content: str) -> str:
    return re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)


def strip_output_region(content: str) -> str:
    """部分输出结果在文章页面是以图片展示的。转换为ipynb前，需要去掉"""
    pattern = r"<!-- BEGIN IPYNB STRIPOUT -->.*?<!-- END IPYNB STRIPOUT -->"
    # 使用 re.sub 替换匹配的内容
    return re.sub(pattern, "", content, flags=re.DOTALL)


def random_pictures():
    return random.choice(pictures)


def change_last_update():
    """主页最后更新日期要通过修改并提交docs/index.md来实现"""
    index_file = os.path.join(os.path.dirname(__file__), "docs/index.md")
    content = '{%\n    include-markdown "../README.md"\n%}\n'
    now = arrow.now()
    content += f'<!--{now.format("YYYY-MM-DD")}-->\n'
    with open(index_file, "w") as f:
        f.write(content)


def get_and_remove_img_url(text: str):
    # 简化函数，避免复杂的正则表达式导致的问题
    try:
        # 查找 markdown 格式的图片
        groups = re.search(r"!\[[^\]]*\]\((.*?)\)", text)
        if groups is not None:
            url = groups.group(1)
            text_without_img = re.sub(r"!\[.*?\]\(.*?\)", "", text)
            return url, text_without_img

        # 查找 HTML 格式的图片
        groups = re.search(r"<img[^>]+src=['\"]([^'\"]+)['\"][^>]*>", text)
        if groups is not None:
            url = groups.group(1)
            text_without_img = re.sub(r"<img[^>]*>", "", text)
            return url, text_without_img

        return None, text
    except Exception as e:
        print(f"Error in get_and_remove_img_url: {e}")
        return None, text


def get_excerpt(text: str):
    """第一个<!--more-->之前的正式文本作为文章摘要，或者前140字符"""
    pat = r"(.*?)(?:<!--\s*more\s*-->)"
    result = re.search(pat, text, re.MULTILINE | re.DOTALL)
    excerpt = None
    if result is not None:
        excerpt = result.group(1).replace("\n\n", "")

    # 如果没有找到 <!--more--> 标记，再看有没有 ---，最后使用前140字符
    if excerpt is None:
        pat = r"(.*?)(?:---\s*)"
        result = re.search(pat, text, re.MULTILINE | re.DOTALL)
        if result is not None:
            excerpt = result.group(1).replace("\n\n", "")
        else:
            excerpt = text[:140] + "..."

    # remove header
    excerpt = excerpt.replace("#", "").replace("\n", "<br>")
    excerpt = remove_incomplete_html_tags(excerpt)

    if len(excerpt) > 140:
        excerpt = excerpt[:137] + "..."

    return excerpt


def get_meta(file):
    with open(file, "r", encoding="utf-8") as f:
        meta, content = frontmatter.parse(f.read())

        if not "excerpt" in meta:
            meta["excerpt"] = get_excerpt(content)
        return meta


def extract_meta_for_jieyu_index(file):
    name = Path(file).name
    if name == "index.md" or name.startswith("_"):
        return None

    meta = get_meta(file)
    if "date" not in meta and "docs/blog" in file:
        print(file, name)
        raise ValueError(f"❌博客文章{file} 没有 date 字段")

    # 对于 blog 文章，始终使用文件路径生成链接，忽略 slug
    # 因为 MkDocs blog 插件基于文件路径生成 URL，不使用 slug
    if "docs/blog" in file:
        path = Path(file)
        relpath = path.relative_to("docs/blog/posts")
        link = Path("/blog/posts") / relpath.with_suffix("")
        meta["link"] = "https://www.jieyu.ai" + str(link) + "/"
    else:
        path = Path(file)
        relpath = path.relative_to("docs/articles")
        link = Path("/articles") / relpath.with_suffix("")
        meta["link"] = "https://www.jieyu.ai" + str(link) + "/"


    return meta


def build_index():
    """web 首页和github profile"""
    metas = []

    posts = glob.glob("./docs/blog/**/*.md", recursive=True)
    articles = glob.glob("./docs/articles/express/*.md", recursive=True)
    with ProcessPoolExecutor() as executor:
        results = executor.map(extract_meta_for_jieyu_index, posts + articles)
        metas.extend(
            [
                meta
                for meta in results
                if (meta is not None and meta.get("date") is not None)
            ]
        )

    metas = sorted(metas, key=lambda x: arrow.get(x["date"]), reverse=True)

    web_cards = []
    github_cards = []
    random.seed(78)
    for meta in metas[:12]:
        title = meta.get("title")
        date = meta.get("date")
        excerpt = meta.get("excerpt")
        img_url = meta.get("img") or random_pictures()
        link = meta["link"]

        card = github_item.format_map(
            {
                "title": title,
                "date": date,
                "excerpt": excerpt,
                "readers": random.randint(100, 1000),
                "link": link,
                "img_url": img_url,
                "img_mode": img_mode,
            }
        )

        github_cards.append(card)

        card = web_item.format_map(
            {
                "title": title,
                "date": date,
                "excerpt": excerpt,
                "link": link,
                "img_url": img_url,
                "img_mode": img_mode,
            }
        )
        web_cards.append(card)

    about_me = "I'm a software developer, quantitative trader and entrepreneur。 Teaching machine learning, trading and software development. Author of 'Best Practices for Python'. \n\n我是一名软件工程师、量化交易人和创业者。《Python高效编程最佳实践指南》的作者。我也是一系列开源软件的开发者或者维护者。"

    latest_article = container_tpl.format_map(
        {
            "cards": "\n".join(github_cards[:3]),
        }
    )

    tip = "\n".join(
        [
            ">[!tip]",
            ">我们教授《匡醍.量化24课》、《匡醍.因子分析与机器学习策略》和《匡醍.量化人的Numpy和Pandas》等系列课程，帮助你从入门到精通，完全掌握量化交易。课程都配有视频、在线运行的Notebook、习题和答疑。请前往公众号 Quantide 咨询",
            "",
            "## 最新文章",
        ]
    )

    github_body = "\n".join(
        [
            about_me,
            tip,
            latest_article,
            "更多精彩好文，请访问[匡醍量化](https://www.jieyu.ai)",
        ]
    )

    web_body = container_tpl.format_map(
        {
            "cards": "\n".join(web_cards),
        }
    )

    change_last_update()

    styles = ""
    tpl = os.path.join(os.path.dirname(__file__), "docs/assets/templates/homepage.tpl")
    with open(tpl, "r") as f:
        styles = f.read()

    return web_body, github_body, styles


def write_readme(body, styles):
    with open("./README.md", "w", encoding="utf-8") as f:
        # f.write(about)
        # f.write(intro)
        f.write(styles)
        f.write(body)
        f.write("\n\n")


def execute(cmd):
    # work_dir = os.path.dirname(__file__)

    print(f"Executing {cmd}")
    try:
        proc = subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        (out, err) = proc.communicate()
        ret_code = proc.wait()
    except Exception as e:
        print(e)
        print(f"!!! FAILED: {cmd}")


def build():
    web_body, github_body, styles = build_index()
    write_readme(web_body, styles)


def publish_jieyu():
    web_body, github_body, styles = build_index()

    # 为github生成README
    write_readme(github_body, "")

    for cmd in [
        "git add .",
        "git commit -m update",
        "git push",
    ]:
        execute(cmd)

    write_readme(web_body, styles)

    cmd = "mkdocs gh-deploy"
    execute(cmd)


def format_code_blocks_in_markdown(content: str):
    code_block_pattern = re.compile(r"```\s*python(.*?)```", re.DOTALL)

    def format_match(match):
        code = match.group(1).strip()
        try:
            # 使用 Black 格式化代码
            formatted_code = black.format_str(code, mode=black.FileMode())
            return f"```python\n{formatted_code}\n```"
        except Exception as e:
            print(f"Error formatting code block: {e}")
            return match.group(0)

    # 替换所有代码块
    formatted_content = code_block_pattern.sub(format_match, content)
    return formatted_content


def preprocess(
    in_file: Path,
    out_file: Path,
    strip_output: bool = False,
    copy_right: bool = False,
    admon_style: str | None = None,
    strip_paid: bool = False,
) -> dict:
    meta = get_meta(in_file)

    def replace_paid_content(match):
        # if getattr(replace_paid_content, 'called', False) == False:
        #     replace_paid_content.called = True
        #     return f"<!--PAID CONTENT START-->\n" \
        #         f"{prompt}\n" \
        #         f"<!--PAID CONTENT END-->"
        # else:
        #     return f"<!--PAID CONTENT START-->\n<!--PAID CONTENT END-->"
        return f"<!--PAID CONTENT START-->\n<!--PAID CONTENT END-->"

    with open(in_file, "r") as f:
        content = f.read()
        if strip_output:
            content = strip_output_region(content)

        if strip_paid:
            pattern = re.compile(
                r"<!--PAID CONTENT START-->(.*?)<!--PAID CONTENT END-->", re.DOTALL
            )
            content = pattern.sub(replace_paid_content, content)

        content = strip_html_comments(content)
        content = format_code_blocks_in_markdown(content)

        if admon_style == "myst":
            lines = to_myst_adnomition(content.split("\n"))
        elif admon_style == "gmf":
            lines = to_gmf_admonition(content.split("\n"))
        elif admon_style is None:
            lines = content.split("\n")  # 保持原始 admonition 格式不变
        else:
            raise ValueError(f"Invalid admon_style: {admon_style}")

        with open(out_file, "w", encoding="utf-8") as f:
            content = "\n".join(lines)
            f.write(content)

            if content.find("版权声明") == -1 and copy_right:
                f.write(get_copyrights())

        return meta


def convert_to_ipynb(in_file: str | Path) -> Path:
    """将markdown转换为notebook，存放在in_file同一目录下。"""
    src = absolute_path(Path(in_file))
    dst = src.with_suffix(".ipynb")

    print(f"converting {src} to {dst}")
    os.system(f"notedown --match=python {src} > {dst}")
    return dst


def preview_notebook(file: str):
    """将markdown转换为ipynb，部署到本地的~/courses/blog目录"""
    src = absolute_path(Path(file))
    tmp_md = Path("/tmp") / src.name
    preprocess(src, tmp_md, strip_output=True, admon_style="myst")

    notebook = convert_to_ipynb(tmp_md)

    dst = Path("~/courses/blog/articles/").expanduser()
    if not dst.exists():
        dst.mkdir(parents=True)

    shutil.copy(notebook, dst / notebook.name)


def publish_quantide(src: str, category: str, price: int = 40):
    """将文章发布到quantide课程平台

    1. 删除markdown中，代码的运行结果（避免与notebook的运行结果重复）
    2. 添加copyright
    3. 将admonition转换为myst格式
    4. 转换为notebook，增加元数据，发布到quantide
    5. 向后台注册资源

    Args:
        src: 输入文章路径
        category: 分类
    """
    md = absolute_path(Path(src))
    preprocessed = Path("/tmp") / md.name
    meta = preprocess(
        md, preprocessed, strip_output=True, copy_right=True, admon_style="myst"
    )

    notebook = convert_to_ipynb(preprocessed)
    update_notebook_metadata(
        notebook,
        meta.get("title", ""),
        meta.get("excerpt", ""),
        meta.get("price", 0),
        meta.get("date", arrow.now().date()),
        meta.get("img", ""),
    )

    meta["course"] = "blog"
    meta["division"] = "blog"
    meta["resource"] = "articles"
    meta["description"] = meta.get("excerpt", "")
    meta["rel_path"] = f"articles/{category}/{notebook.name}"
    meta["publish_date"] = arrow.get(meta.get("date", arrow.now())).format("YYYY-MM-DD")
    if "date" in meta:
        del meta["date"]

    if price not in (0, 360):
        meta["price"] = price - 0.1
    else:
        meta["price"] = price

    # 将文件部署到quantide课程平台
    cmd = f'ssh omega "mkdir -p ~/courses/blog/articles/{category}"'
    os.system(cmd)

    cmd = f"scp {notebook} omega:~/courses/blog/articles/{category}/{notebook.name}"
    os.system(cmd)

    if API_TOKEN:
        response = requests.post(
            f"{quantide_api_url}/api/admin/resources/publish",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_TOKEN}",
            },
            json={"meta": meta, "allow_all": price == 0},
        )
        if response.status_code == 200:
            print("✅ 发布成功")
        else:
            print("❌ 发布失败")
            print(response.text)


def prepare_gzh(src: str):
    """将文章复制到/tmp下，转换为ipynb并拷贝到research环境"""
    md = absolute_path(Path(src))
    preprocessed = Path("/tmp") / md.name
    preprocess(md, preprocessed, strip_paid=True)
    print(f"✅ 文章已适合作为公众号发表，请前往{preprocessed}查看")


def remove_incomplete_html_tags(text):
    """
    移除未闭合的HTML标签及其后面的内容
    
    Args:
        text (str): 需要处理的文本
        
    Returns:
        str: 处理后的文本
    """
    # 使用栈来跟踪未闭合的标签
    tag_stack = []
    result = []
    i = 0
    
    while i < len(text):
        if text[i] == '<':
            # 找到标签的结束位置
            tag_end = text.find('>', i)
            if tag_end == -1:
                # 未找到结束的>，这是一个不完整的标签，移除它及其后面所有内容
                break
            
            tag_content = text[i:tag_end+1]
            result.append(tag_content)
            
            # 解析标签
            if tag_content.startswith('</'):
                # 结束标签
                tag_name = tag_content[2:-1].strip().split()[0]
                if tag_stack and tag_stack[-1] == tag_name:
                    tag_stack.pop()
            elif tag_content.endswith('/>'):
                # 自闭合标签
                pass
            else:
                # 开始标签
                tag_name = tag_content[1:-1].strip().split()[0]
                # 不将自闭合标签放入栈中
                if tag_name.lower() not in ['img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr']:
                    tag_stack.append(tag_name)
            
            i = tag_end + 1
        else:
            result.append(text[i])
            i += 1
    
    # 如果还有未闭合的标签，我们需要找到导致问题的标签并截断
    if tag_stack:
        # 找到文本中最后一个未闭合标签的开始位置
        for j in range(len(result) - 1, -1, -1):
            if isinstance(result[j], str) and result[j].startswith('<') and not result[j].startswith('</') and not result[j].endswith('/>'):
                tag_name = result[j][1:-1].strip().split()[0]
                if tag_name in tag_stack:
                    # 截断到这个标签之前
                    return ''.join(result[:j])
    
    return ''.join(result)


if __name__ == "__main__":
    fire.Fire(
        {
            "build": build,
            "jieyu": publish_jieyu,
            "quantide": publish_quantide,
            "gzh": prepare_gzh,
            "meta": extract_meta_for_jieyu_index,
            "preview": preview_notebook,
        }
    )
