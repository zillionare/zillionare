import glob
import os
import random
import re

import arrow
import frontmatter
from numpy import rec

fade_modes = ["fadeInLeft", "fadeInUp", "fadeInRight", "fadeInDown"]
# img_modes = [f"card-img-{item}" for item in ("bottom", "overlay", "top")]
img_mode = "card-img-top"

style_files = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.4.0/animate.min.css">
<style>
.md-sidebar--primary {
    width: 0%;
}
</style>
"""

cell = """
<div class="col-xs-12 col-md-6">
    <article class="card animated {fade_mode}">
    <img class="{img_mode} img-responsive" src="{img_url}"/>
    <div class="card-block">
        <h4 class="card-title">{title}</h4>
        <h6 class="text-muted">{date}</h6>
        <p class="card-text">{excerpt}</p>
        <a href="{link}" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>
"""

row_tpl = """
<div class="row">
{cells}
</div>
"""
container_tpl = """
<div class="container m-t-md">
    {rows}
</div>
"""

def change_last_update():
    """主页最后更新日期要通过修改并提交docs/index.md来实现"""
    index_file = os.path.join(os.path.dirname(__file__), "docs/index.md")
    content = '{%\n    include-markdown "../README.md"\n%}\n'
    now = arrow.now()
    content += f'<!--{now.format("YYYY-MM-DD")}-->\n'
    with open(index_file, 'w') as f:
        f.write(content)

def get_and_remove_img_url(text: str):
    groups = re.search(r"\!\[.*\]\((.*)\)", text)
    if groups is None:
        groups = re.search(r"<\s*img\s+src=[\'\"](.+)\s*>", text)
        if groups is None:
            return None, text
        
        url = groups.group(1)
        return url, re.sub(r"<\s*img\s+src=[\'\"].+\s*[\'\"]>", "", text)

    return groups.group(1), re.sub(r"\!\[.*\]\(.*\)", "", text)

def get_excerpt(text: str):
    pat = r"(.+)<!--more-->"
    result = re.search(pat, text, re.MULTILINE|re.DOTALL)
    if result  is not None:
        excerpt = result.group(1).replace("\n\n", "")
    else:
        excerpt = text[:140] + "..."

    # remove header
    excerpt = excerpt.replace("#", "").replace("\n", "<br>")

    return get_and_remove_img_url(excerpt)

def get_meta(file):
    with open(file, 'r', encoding='utf-8') as f:
        meta, content = frontmatter.parse(f.read())
        img, excerpt = get_excerpt(content)
        if img is None:
            print(f"请为文件{file}配图！")

            keys = ["mountain", "cloud", "room", "cats", "dogs", "light", "girls", "food", "drink"]
            query = keys[random.randint(0, len(keys) - 1)]
            img = f"https://source.unsplash.com/random/360x200?{query}"
        meta["excerpt"] = excerpt
        meta["img"] = img
        return meta

def build_index():
    """生成README文件"""

    # about = """大富翁 (Zillionare)是开源量化框架，提供数据本地化、回测、交易接入和量化分析底层库支持等一站式服务。<br><br>大富翁的起名有两重寓意，一是希望她的使用者们都能实现财富自由。另一方面，大富翁也是一款投资游戏的名字 -- 财富终究只是一场大富翁游戏，以示提醒大家，不要忽视运气的因素。<br><br>在投资中的运气，其实就是周期。千万不要做逆周期的投资。<br><br>Zillionare 最新版本是2.0，提供了海量数据存储（在我们的生产环境下，存储超过30亿条记录）和高性能访问能力。Zillionare是开源框架，您可以自行研究、拓展该框架。我们也提供付费服务。比如，2.0的Docker-compse 安装版本我们目前只对学员提供。<br><br>关于Zillionare的更多细节请访问[链接](articles/products/)\n\n"""

    # intro = "## 最新文章\n\n"

    metas = []
    articles = glob.glob("./docs/articles/**/*.md", recursive=True)
    for file in articles:
        meta = get_meta(file)
        if "date" not in meta:
            continue
        
        if "slug" not in meta:
            print(f"missing slug: {file}")
            part = file.split("articles")[1]
            link = "/articles" + part.replace(".md", "")
        else:
            matched = re.match(r".*/articles(.+)/.*\.md", file)
            link = "/articles" + matched.group(1) + "/" + meta["slug"]

        meta["link"] = link

        metas.append(meta)

    posts = glob.glob("./docs/blog/**/*.md", recursive=True)
    for file in posts:
        meta = get_meta(file)
        if "date" not in meta:
            continue

        if "slug" not in meta:
            print(f"missing slug: {file}")
            continue

        year, month, day = meta["date"].split("-")
        slug = meta["slug"]
        meta["link"] = f"blog/{year}/{month}/{day}/{slug}"

        metas.append(meta)

    metas = sorted(metas, key=lambda x: arrow.get(x["date"]), reverse=True)

    cells = []
    rows = []
    for i, meta in enumerate(metas[:12]):
        title = meta.get("title")
        date = meta.get("date")
        excerpt = meta.get("excerpt")
        img_url = meta["img"]
        link = meta["link"]

        fade_mode = fade_modes[i%4]
        card = cell.format_map({
            "title": title,
            "date": date,
            "excerpt": excerpt,
            "link": link,
            "img_url": img_url,
            "fade_mode": fade_mode,
            "img_mode": img_mode,
        })

        cells.append(card)
        if (i + 1) % 2 == 0:
            rows.append(row_tpl.format_map({"cells": "\n".join(cells)}))
            cells = []


    body = container_tpl.format_map({
        "rows": "\n".join(rows),
    })


    with open('./README.md', "w", encoding='utf-8') as f:
        # f.write(about)
        # f.write(intro)
        f.write(style_files)
        f.write(body)
        f.write("\n\n")

    change_last_update()

build_index()

