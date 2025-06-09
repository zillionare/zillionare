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
API_TOKEN = os.environ.get("API_TOKEN")

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
    "https://images.jieyu.ai/images/university/ucl-wilkins-building.jpg"
]

img_mode = "card-img-top"

github_item = """
<div>
<h3>{title}</h3>
<img src="{img_url}" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>{excerpt}</p>

<p><span style="margin-right:20px">发表于 {date} 人气 {readers} </span><span><a href="{link}">点击阅读</a></span></p>

</div><!--end-article-->
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
    规则：遇到连续两个空行时结束，但要忽略 fenced code blocks 内部的空行
    """
    in_fenced_block = False
    fenced_pattern = re.compile(r'^\s*```')
    consecutive_empty_lines = 0
    
    for m in range(i, len(lines)):
        line = lines[m]
        
        # 检查是否进入或退出 fenced code block
        if fenced_pattern.match(line):
            in_fenced_block = not in_fenced_block
            consecutive_empty_lines = 0  # 重置空行计数
            continue
        
        # 如果不在 fenced code block 内，检查空行
        if not in_fenced_block:
            if line == "":
                consecutive_empty_lines += 1
                # 如果遇到连续两个空行，则结束 admonition
                if consecutive_empty_lines >= 2:
                    return m - 1  # 返回第一个空行的位置
            else:
                consecutive_empty_lines = 0  # 重置空行计数
        
    return len(lines)

def replace_adnomition(lines, i, m):
    """
    将 admonition 转换为 myst 格式
    处理 fenced code blocks：将 ```python 转换为 ````python
    """
    matched = re.search(r"(tip|warning|note|attention|hint|more)", lines[i], flags=re.I)
    tag = "note"
    if matched is not None:
        tag = mystAdmons.get(matched.group(1).lower())

    # 处理内容，移除 admonition 缩进并转换 fenced code blocks
    content = []
    fenced_pattern = re.compile(r'^(\s*)(```)(.*)')
    
    for line in lines[i + 1 : m]:
        # 移除 admonition 的缩进（4个空格或1个制表符）
        if line.startswith("    "):
            processed_line = line[4:]
        elif line.startswith("\t"):
            processed_line = line[1:]
        else:
            processed_line = line
        
        # 检查是否是 fenced code block 标记
        fenced_match = fenced_pattern.match(processed_line)
        if fenced_match:
            # 将 ``` 转换为 ````（增加一个反引号）
            indent, backticks, rest = fenced_match.groups()
            processed_line = f"{indent}`{backticks}{rest}"
        
        content.append(processed_line)
    
    return [f"``` {{{tag}}}", *content, "```"]


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

def to_gmf_admonition(lines: List[str]):
    """Convert CommonMark admonition format to GitHub Markdown Format (GMF)."""
    
    allowed_types = ["NOTE", "TIP", "CAUTION", "IMPORTANT", "QUESTION", "WARNING"]
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测CommonMark admonition起始行
        if line.startswith('!!! '):
            # 提取admonition类型
            admonition_type = (line[4:].strip()).upper()
            if admonition_type not in allowed_types:
                admonition_type = "NOTE"

            # 收集内容块
            content = []
            j = i + 1
            while j < len(lines) and lines[j].startswith(' ' * 2):
                content.append(lines[j][2:])  # 移除缩进
                j += 1
            
            # 添加转换后的内容
            result.append(f'>[!{admonition_type}]')
            for content_line in content:
                result.append(f'    {content_line}')  # 添加单空格缩进
            
            # 跳过已处理的行
            i = j
        else:
            # 普通行直接添加
            result.append(line)
            i += 1
    
    return result

def strip_html_comments(content: str) -> str:
    return re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

def strip_output_region(content: str) ->str:
    """部分输出结果在文章页面是以图片展示的。转换为ipynb前，需要去掉"""
    pattern = r'<!-- BEGIN IPYNB STRIPOUT -->.*?<!-- END IPYNB STRIPOUT -->'
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
    with open(index_file, 'w') as f:
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
    pat = r'(.*?)(?:<!--\s*more\s*-->)'
    result = re.search(pat, text, re.MULTILINE|re.DOTALL)
    excerpt = None
    if result  is not None:
        excerpt = result.group(1).replace("\n\n", "")

    # 如果没有找到 <!--more--> 标记，再看有没有 ---，最后使用前140字符
    if excerpt is None:
        pat = r"(.*?)(?:---\s*)"
        result = re.search(pat, text, re.MULTILINE|re.DOTALL)
        if result is not None:
            excerpt = result.group(1).replace("\n\n", "")
        else:
            excerpt = text[:140] + "..."

    # remove header
    excerpt = excerpt.replace("#", "").replace("\n", "<br>")
    if len(excerpt) > 140:
        excerpt = excerpt[:137] + "..."

    return get_and_remove_img_url(excerpt)

def get_meta(file):
    with open(file, 'r', encoding='utf-8') as f:
        meta, content = frontmatter.parse(f.read())
        
        _, excerpt = get_excerpt(content)
        meta["excerpt"] = excerpt
        return meta

def extract_meta_for_jieyu_index(file):
    if "docs/articles" in file or "index.md" in file: # 这是文章，或者目录
        return None

    meta = get_meta(file)
    if "date" not in meta:
        raise ValueError(f"❌博客文章{file} 没有 date 字段")

    # 对于 blog 文章，始终使用文件路径生成链接，忽略 slug
    # 因为 MkDocs blog 插件基于文件路径生成 URL，不使用 slug
    path = Path(file)
    relpath = path.relative_to("docs/blog/posts")
    link = Path("/blog/posts") / relpath.with_suffix("")
    meta["link"] = str(link) + "/"

    return meta

def build_index():
    """生成README文件"""

    # about = """大富翁 (Zillionare)是开源量化框架，提供数据本地化、回测、交易接入和量化分析底层库支持等一站式服务。<br><br>大富翁的起名有两重寓意，一是希望她的使用者们都能实现财富自由。另一方面，大富翁也是一款投资游戏的名字 -- 财富终究只是一场大富翁游戏，以示提醒大家，不要忽视运气的因素。<br><br>在投资中的运气，其实就是周期。千万不要做逆周期的投资。<br><br>Zillionare 最新版本是2.0，提供了海量数据存储（在我们的生产环境下，存储超过30亿条记录）和高性能访问能力。Zillionare是开源框架，您可以自行研究、拓展该框架。我们也提供付费服务。比如，2.0的Docker-compse 安装版本我们目前只对学员提供。<br><br>关于Zillionare的更多细节请访问[链接](articles/products/)\n\n"""

    # intro = "## 最新文章\n\n"

    metas = []

    posts = glob.glob("./docs/blog/**/*.md", recursive=True)
    with ProcessPoolExecutor() as executor:
        results = executor.map(extract_meta_for_jieyu_index, posts)
        metas.extend([meta for meta in results if (meta is not None and meta.get("date") is not None)])

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

        card = github_item.format_map({
            "title": title,
            "date": date,
            "excerpt": excerpt,
            "readers": random.randint(100, 1000),
            "link": link,
            "img_url": img_url,
            "img_mode": img_mode,
        })

        github_cards.append(card)

        card = web_item.format_map({
            "title": title,
            "date": date,
            "excerpt": excerpt,
            "link": link,
            "img_url": img_url,
            "img_mode": img_mode,
        })
        web_cards.append(card)


    github_body = container_tpl.format_map({
        "cards": "\n".join(github_cards),
    })

    web_body = container_tpl.format_map({
        "cards": "\n".join(web_cards),
    })

    change_last_update()

    styles = ""
    tpl = os.path.join(os.path.dirname(__file__), "docs/assets/templates/homepage.tpl")
    with open(tpl, "r") as f:
        styles = f.read()

    return web_body, github_body, styles


def write_readme(body, styles):
    with open('./README.md', "w", encoding='utf-8') as f:
        # f.write(about)
        # f.write(intro)
        f.write(styles)
        f.write(body)
        f.write("\n\n")

def execute(cmd):
    # work_dir = os.path.dirname(__file__)

    print(f"Executing {cmd}")
    try:
        proc = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
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

def preprocess(in_file: Path, out_file: Path, strip_output: bool = False, copy_right: bool = False, admon_style: str = "gmf", strip_paid: bool = False)->dict:
    meta = get_meta(in_file)

    def replace_paid_content(match):
        # if getattr(replace_paid_content, 'called', False) == False:
        #     replace_paid_content.called = True
        #     return f"<!--PAID CONTENT START-->\n" \
        #         f"{prompt}\n" \
        #         f"<!--PAID CONTENT END-->"
        # else:
        #     return f"<!--PAID CONTENT START-->\n<!--PAID CONTENTEND-->"
        return f"<!--PAID CONTENT START-->\n<!--PAID CONTENTEND-->"

    with open(in_file, "r") as f:
        content = f.read()
        if strip_output:
            content = strip_output_region(content)

        if strip_paid:
            pattern = re.compile(r'<!--PAID CONTENT START-->(.*?)<!--PAID CONTENT END-->',
                         re.DOTALL)
            content = pattern.sub(replace_paid_content, content)
            
        content = strip_html_comments(content)
        content = format_code_blocks_in_markdown(content)

        if admon_style == "myst":
            lines = to_myst_adnomition(content.split("\n"))
        elif admon_style == "gmf":
            lines = to_gmf_admonition(content.split("\n"))
        else:
            raise ValueError(f"Invalid admon_style: {admon_style}")

        with open(out_file, "w", encoding="utf-8") as f:
            content = "\n".join(lines)
            f.write(content)

            if content.find("版权声明") == -1 and copy_right:
                f.write(get_copyrights())

        return meta
def convert_to_ipynb(in_file: str|Path)->Path:
    """将markdown转换为notebook，存放在in_file同一目录下。"""
    src = absolute_path(Path(in_file))
    dst = src.with_suffix(".ipynb")

    print(f"converting {src} to {dst}")
    os.system(f"notedown --match=python {src} > {dst}")
    return dst

def preview_notebook(file: str):
    """将markdown转换为ipynb，部署到本地的~/courses/blog目录"""
    src = absolute_path(Path(file))
    tmp_md = Path("/tmp")/src.name
    preprocess(src, tmp_md, admon_style="myst")

    notebook = convert_to_ipynb(tmp_md)
    
    dst = Path("~/courses/blog/articles/").expanduser()
    if not dst.exists():
        dst.mkdir(parents=True)

    shutil.copy(notebook, dst/notebook.name)

def publish_quantide(src: str, category: str = "", price: int = 0):
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
    if price not in (0, 10, 20, 40, 80, 100, 200, 360):
        raise ValueError(f"博客文章的价格必须是:  10, 20, 40, 80, 100, 200, 360中的一个")
    
    md = absolute_path(Path(src))
    preprocessed = Path("/tmp") / md.name
    meta = preprocess(md, preprocessed, strip_output=True, copy_right=True, admon_style="myst")

    notebook = convert_to_ipynb(preprocessed)
    update_notebook_metadata(notebook, 
                             meta.get("title", ""), 
                             meta.get("excerpt", ""), 
                             meta.get("price", 0),
                             meta.get("date", arrow.now().date()),
                             meta.get("img", ""))
    
    meta["course"] = "blog"
    meta["resource"] = "articles"
    meta["description"] = meta.get("excerpt", "")
    meta["rel_path"] = f"articles/{category}/{notebook.name}"
    
    if price not in (0, 360):
        meta["price"] = price - 0.1
    else:
        meta["price"] = price

    # 将文件部署到quantide课程平台
    cmd = f'ssh omega "mkdir -p ~/courses/blog/articles/{category}"'
    os.system(cmd)

    cmd = f'scp {notebook} omega:~/courses/blog/articles/{category}/{notebook.name}'
    os.system(cmd)

    if not API_TOKEN:
        response = requests.post(
            f"{quantide_api_url}/api/admin/resources/publish",
            headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_TOKEN}"
                },
            json={
                "meta": meta,
                "allow_all": price == 0
            }
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
    preprocess(md, preprocessed, strip_paid = True)
    print(f"✅ 文章已适合作为公众号发表，请前往{preprocessed}查看")

if __name__ == "__main__":
    fire.Fire({
        "build": build,
        "jieyu": publish_jieyu,
        "quantide": publish_quantide,
        "gzh": prepare_gzh,
        "meta": extract_meta_for_jieyu_index,
        "preview": preview_notebook
    })
