import glob
import re

import arrow
import frontmatter


def get_excerpt(text: str):
    pat = r"(.+)<!--more-->"
    result = re.search(pat, text, re.MULTILINE|re.DOTALL)
    if result  is not None:
        excerpt = result.group(1).replace("\n\n", "")
    else:
        excerpt = text[:140] + "..."

    # remove header
    excerpt = excerpt.replace("#", "").replace("\n", "<br>")

    # remove img
    excerpt = re.sub(r"\!\[.*\]\(.*\)", "", excerpt)

    return excerpt

def get_meta(file):
    with open(file, 'r', encoding='utf-8') as f:
        meta, content = frontmatter.parse(f.read())
        excerpt = get_excerpt(content)
        meta["excerpt"] = excerpt
        return meta

def build_index():
    """生成README文件"""

    about = """大富翁 (Zillionare)是开源量化框架，提供数据本地化、回测、交易接入和量化分析底层库支持等一站式服务。<br><br>大富翁的起名有两重寓意，一是希望她的使用者们都能实现财富自由。另一方面，大富翁也是一款投资游戏的名字 -- 财富终究只是一场大富翁游戏，以示提醒大家，不要忽视运气的因素。<br><br>在投资中的运气，其实就是周期。千万不要做逆周期的投资。<br><br>Zillionare 最新版本是2.0，提供了海量数据存储（在我们的生产环境下，存储超过30亿条记录）和高性能访问能力。Zillionare是开源框架，您可以自行研究、拓展该框架。我们也提供付费服务。比如，2.0的Docker-compse 安装版本我们目前只对学员提供。<br><br>关于Zillionare的更多细节请访问[链接](articles/products/)\n\n"""

    intro = "---\n\n## 近期文章\n\n"

    latest = []

    metas = []
    articles = glob.glob("./docs/articles/**/*.md", recursive=True)
    for file in articles:
        meta = get_meta(file)
        if "date" not in meta:
            continue
        
        meta["path"] = file
        metas.append(meta)

    posts = glob.glob("./docs/blog/**/*.md", recursive=True)
    for file in posts:
        meta = get_meta(file)
        if "date" not in meta:
            continue

        meta["path"] = file
        metas.append(meta)

    metas = sorted(metas, key=lambda x: arrow.get(x["date"]), reverse=True)

    for meta in metas[:10]:
        title = meta.get("title")
        date = meta.get("date")
        excerpt = meta.get("excerpt")
        
        link = meta["path"]
        readme = f"<text-right>发表于 {date} [阅读]({link})</text-right>"
        content = f'!!! info "{title}"\n    {excerpt}<br>{readme}'

        latest.append(content)

    latest = "\n\n".join(latest)
    with open('./README.md', "w", encoding='utf-8') as f:
        f.write(about)
        f.write(intro)
        f.write(latest)

build_index()

