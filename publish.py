import glob
import os
import random
import re
import shlex
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from typing import List

import arrow
import fire
import frontmatter

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

def seek_adnomition_end(i, lines):
    for m in range(i, len(lines)):
        # 防止在!!! tip之后出现空行
        if lines[m] == "":
            continue

        if not (lines[m].startswith("    ") or lines[m].startswith("\t")):
            return m

def replace_adnomition(lines, i, m):
    """replace indented lines to myst adnomition due to myst 2.4.2 bug"""
    matched = re.search(r"(tip|warning|note|attention|hint|more)", lines[i], flags=re.I)
    tag = "note"
    if matched is not None:
        tag = mystAdmons.get(matched.group(1).lower())

    content = [line.lstrip(" \t") for line in lines[i + 1 : m]]
    return [f"``` {{{tag}}}", *content, "```"]


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

def strip_html_comments(content: str) -> str:
    return re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

def strip_output(content: str) ->str:
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
    groups = re.search(r"!\[[^\]]*\]\((.*?)\)", text)
    if groups is None:
        groups = re.search(r"<\s*img\s+src=[\'\"](.+)\s*>", text)
        if groups is None:
            return None, text
        
        url = groups.group(1)
        return url, re.sub(r"<\s*img\s+src=[\'\"].+\s*[\'\"]>", "", text)

    return groups.group(1), re.sub(r"\!\[.*\]\(.*\)", "", text)

def get_excerpt(text: str):
    pat = r'(.*?)(?:<!--\s*more\s*-->)'
    result = re.search(pat, text, re.MULTILINE|re.DOTALL)
    if result  is not None:
        excerpt = result.group(1).replace("\n\n", "")
    else:
        excerpt = text[:140] + "..."

    # remove header
    excerpt = excerpt.replace("#", "").replace("\n", "<br>")

    return get_and_remove_img_url(excerpt)

def get_meta(file):
    # file = "/apps/zillionare/docs/blog/posts/quantlib/why-click-house-so-fast.md"
    with open(file, 'r', encoding='utf-8') as f:
        meta, content = frontmatter.parse(f.read())
        
        _, excerpt = get_excerpt(content)

        if meta.get("slug") is None:
            print(f"请为文件{file}添加slug！")
            sys.exit(0)

        meta["excerpt"] = excerpt
        return meta

def extract_article_meta(file):
    meta = get_meta(file)
    if "date" not in meta:
        return
    
    if "slug" not in meta:
        print(f"missing slug: {file}")
        part = file.split("articles")[1]
        link = "https://www.jieyu.ai/articles" + part.replace(".md", "")
    else:
        matched = re.match(r".*/articles(.+)/.*\.md", file)
        link = "/articles" + matched.group(1) + "/" + meta["slug"]

    meta["link"] = link

    return meta

def extract_blog_meta(file):
    meta = get_meta(file)
    if "date" not in meta:
        return

    if "slug" not in meta:
        print(f"missing slug: {file}")
        return

    date = arrow.get(meta["date"])
    year, month, day = f"{date.year}", f"{date.month:02d}", f"{date.day:02d}"
    slug = meta["slug"]
    meta["link"] = f"https://www.jieyu.ai/blog/{year}/{month}/{day}/{slug}"

    return meta

def build_index():
    """生成README文件"""

    # about = """大富翁 (Zillionare)是开源量化框架，提供数据本地化、回测、交易接入和量化分析底层库支持等一站式服务。<br><br>大富翁的起名有两重寓意，一是希望她的使用者们都能实现财富自由。另一方面，大富翁也是一款投资游戏的名字 -- 财富终究只是一场大富翁游戏，以示提醒大家，不要忽视运气的因素。<br><br>在投资中的运气，其实就是周期。千万不要做逆周期的投资。<br><br>Zillionare 最新版本是2.0，提供了海量数据存储（在我们的生产环境下，存储超过30亿条记录）和高性能访问能力。Zillionare是开源框架，您可以自行研究、拓展该框架。我们也提供付费服务。比如，2.0的Docker-compse 安装版本我们目前只对学员提供。<br><br>关于Zillionare的更多细节请访问[链接](articles/products/)\n\n"""

    # intro = "## 最新文章\n\n"

    metas = []
    articles = glob.glob("./docs/articles/**/*.md", recursive=True)
    with ProcessPoolExecutor() as executor:
        results = executor.map(extract_article_meta, articles)
        metas.extend([meta for meta in results if meta is not None])

    posts = glob.glob("./docs/blog/**/*.md", recursive=True)
    with ProcessPoolExecutor() as executor:
        results = executor.map(extract_blog_meta, posts)
        metas.extend([meta for meta in results if meta is not None])

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


def publish():
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

def convert_to_ipynb(in_file: str):
    stem = os.path.splitext(os.path.basename(in_file))[0]

    preprocessed = os.path.join("/tmp/", f"{stem}.md")
    preprocess(in_file, preprocessed)

    if out_file is None:
        out_dir = os.path.dirname(in_file)
        out_file = os.path.join(out_dir, f"{stem}.ipynb")
    print(f"converting {preprocessed} to {out_file}")

    os.system(f"notedown --match=python {preprocessed} > {out_file}")
    # cmd = f"pandoc -f markdown -t ipynb {preprocessed} -o {out_file}"
    # os.system(cmd)
    return out_file
def paid(src, dst, preview=False):
    """隐藏付费内容

    Args:
        src: 输入文章路径
        dst: 因子，算法和策略, Numpy&Pandas中的一个
        preview: 是否在浏览器中预览
    
    1. 将<!-- BEGIN IPYNB STRIPOUT -->与<!-- BEGIN IPYNB STRIPOUT -->之间的内容删除
    2. 基于1，将文章复制到/tmp下，转换为ipynb并拷贝到reseach环境
    3. 将<!--PAID CONTENT START-->与<!--PAID CONTENT END-->之间的内容删除注释掉并保存
    """
    prompt = '<a class="weapp_text_link js_weapp_entry" style="font-size:17px;" data-miniprogram-appid="wx4f706964b979122a" data-miniprogram-path="pages/topics/topics?group_id=28885284828481" data-miniprogram-applink="" data-miniprogram-nickname="知识星球" href="" data-miniprogram-type="text" data-miniprogram-servicetype=""><div><img src="https://images.jieyu.ai/images/hot/logo/zsxq.png"><div style="width:100%;text-align:center;color:blue">完整代码在星球中。点击链接|扫码 加入星球，即可解锁</div></div></a>'
    root = os.path.dirname(__file__)
    src = os.path.join(root, src)

    # 先备份
    execute(f"git add {src}")
    execute(f"git commit -m {src}")

    # 发布到研究环境
    with open(src, "r", encoding='utf-8') as f:
        content = f.read()
        lines = strip_html_comments(strip_output(content)).split("\n")
        lines = to_myst_adnomition(lines)

    filename = os.path.basename(src)
    out_md = os.path.join("/tmp", filename)
    with open(out_md, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))

    out_ipynb = out_md.replace(".md", ".ipynb")
    os.system(f"notedown --match=python {out_md} > {out_ipynb}")
    if not preview:
        print(f"copy {out_ipynb} to research:{dst}")
        os.system(f"scp {out_ipynb} omega:/data/course/notebooks/research/readonly/{dst}")

    # 准备发布到网站、公众号的内容
    pattern = re.compile(r'<!--PAID CONTENT START-->(.*?)<!--PAID CONTENT END-->',
                         re.DOTALL)

    def replace_paid_content(match):
        code = match.group(1).split("\n")[:10]
        code.extend(["...",
                     "余下代码，请加入星球后阅读",
                     "```\n"])
        code = "\n".join(code)
        return f"<!--PAID CONTENT START-->\n" \
               f"{code}\n{prompt}\n" \
               f"<!--PAID CONTENT END-->"

    new_content = pattern.sub(replace_paid_content, content)

    with open(out_md, "w", encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    fire.Fire({
        "build": build,
        "publish": publish,
        "paid": paid
    })
