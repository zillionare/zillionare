import glob
import os
import random
import re
import shlex
import subprocess
from concurrent.futures import ProcessPoolExecutor

import arrow
import frontmatter

img_mode = "card-img-top"

github_item = """
<div>
<h3>{title}</h3>
<img src="{img_url}" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>{excerpt}</p>

<p><span style="margin-right:20px">发表于 {date}</span><span><a href="{link}">点击阅读</a></span></p>

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
    pat = r'(.*?)(?:<!--more-->)'
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

            keys = ["mountain", "cloud", "room", "cats", "dogs", "light", "girls", "food", "drink","flower", "bouquet", "starry-night", "breakfast", "tigger", "teddy", "lion"]
            query = keys[random.randint(0, len(keys) - 1)]
            img = f"https://source.unsplash.com/random/360x200?{query}"
        meta["excerpt"] = excerpt
        meta["img"] = img
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

    date = meta["date"]
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
    for meta in metas[:12]:
        title = meta.get("title")
        date = meta.get("date")
        excerpt = meta.get("excerpt")
        img_url = meta["img"]
        link = meta["link"]

        card = github_item.format_map({
            "title": title,
            "date": date,
            "excerpt": excerpt,
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


def publish():
    web_body, github_body, styles = build_index()
    write_readme(web_body, styles)

    cmd = "mkdocs gh-deploy"
    execute(cmd)

    # 为github生成README
    write_readme(github_body, "")

    for cmd in [
        "git add README.md",
        "git commit -m update",
        "git push",

    ]:
        execute(cmd)

publish()
