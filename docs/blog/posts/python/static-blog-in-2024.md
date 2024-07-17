---
title: 2024年，免费博客赚钱方案
slug: static-site-in-2024
date: 2024-01-01
category: arsenal
motto:
lunar:
tags: 
    - blog
    - static-site
    - tools
---

几年前，我就推荐过用 Markdown 写作静态博客。静态博客几乎是零托管成本，比较适合个人博客起步。Markdown 便于本地搜索，也可当作是个人知识库方案。

现在有了新的进展。我不仅构建了一个视觉上相当不错的个人网站，还美化了 github、构建了个人出版系统 -- 将文章导出为排版精美的图片和 pdf 的能力。

<!--more-->

这一方案的核心是 Mkdocs 和 Mkdocs-material。前者是 Python 技术文档构建系统，后者是与之适配的主题。我在 [《Python 能做大项目》](http://www.jieyu.ai/articles/python/best-practice-python/chap01/) 这本书中，深入介绍过这两种技术。

现在，基于这两种技术，我们可以走得更远：不仅可以撰写技术文档，更可以打造博客和门户网站。

下图就是截取的 [大富翁量化](https://www.jieyu.ai) 的网站界面：

![66%](https://images.jieyu.ai/images/2024/01/my-home-age.png)

---

你可以在 [大富翁量化](https://www.jieyu.ai) 网站上看到它最新的样式。更有创意的是，虽然它只是一个静态网站，但你每次刷新它，都能看到一些新的内容 -- 至少配图会变！

这是首页。菜单栏、搜索这些是常规配置。标签云、首页的卡片式布局，是提升站点气质的地方。

所有的文档都有版本管理，我使用了 github 来托管文档和图片，所以，也顺便把 github 的个人主页美化了一下：

![75%](https://images.jieyu.ai/images/2024/01/github-profile.jpg)

实在说，之前我没有想过，github 主页也可以做得像个人网站。不得不说一张好图，能大大提升颜值。

---

此外，作为创作者，我还希望自己的文章能在多个渠道上发布，包括公众号、知乎、CSDN 和小红书，有时候还需要把文章导出为 PDF。这些渠道采用的技术大不相同，它们的排版要求也不一样，所以，要想不把时间无谓地浪费在枯燥、重复的排版上，我们就得用好各种工具。

## Mkdocs + Mkdocs - Material

基础搭建我都写在 [《Python 能做大项目》](http://www.jieyu.ai/articles/python/best-practice-python/chap01/) 这本书的第 10 章中了，这里我们只介绍如何开通博客功能，以及定制首页。

Material 自带了博客插件，我们只需要在配置中启用它（以及其它相关插件）:

```yaml
plugins:
  - awesome-pages:
      collapse_single_pages: true
  - blog:
      post_excerpt_separator: <!--more-->
  - tags:
      tags_file: tags.md
  - rss:
      match_path: "(blog|articles)/.*"
      category:
        - categories
        - tags
      date_from_meta:
        as_creation: "date"
        as_update: true
  - rss:
      match_path: "(blog|articles)/.*"
      category:
        - categories
        - tags
      date_from_meta:
        as_creation: "date"
        as_update: true
        datetime_format: "%Y-%m-%d %H:%M"
        default_timezone: Asia/Shanghai
      use_git: false
```

其中 rss 插件需要安装 mkdocs-rss-plugin 插件。关于如何定制标签云，请参考 [Code Inside Out 上的这篇文章](https://www.codeinsideout.com/blog/site-setup/add-new-features/#tag-cloud)。

该文也提到了如何实现最新博文的功能。不过，博主最后决定自己用 Python 撸一个方案，以实现本文开头提到的效果 -- 动态和卡片式，并且能自动更新 github 的 profile。

## 自定义脚本生成卡片式首页和 github profile

这个方案主要使用了 python-frontmatter 库。通过一个脚本，搜索 articles 和 blog 目录下所有的 md 文件，读取它们的 front matter，再按日期排序，将最新发表的文章和博文的摘要、日期、title 和首图抽取出来，通过模板生成一个新的 README.md 文件，放到项目根目录下。

---

github 会读取这个文件作为我们的 profile，mkdocs-material 也会根据这个文件，生成网站首页。

这个 readme.md 实际上是一个带部分 html 标签的 md 片段。我先用脚本生成了供 mkdocs 使用的 README.md，待网站发布后，再生成供 github 的 profile 使用的 readme.md。区别主要在于，github 的 profile 中不能使用'<style\>'标签来定义样式，它只允许在 README.md 中 html 标签中，使用少量的样式语法。

!!! tip
    如果对这个方案的细节感兴趣，可以直接访问 [zillionare](https://github.com/zillionare) 这个项目。mkdocs-material 的定制在 docs/overrides 目录下。构建 Readme.md 的脚本在根目录下，名字为 publish.py。

为了生成响应式的卡片布局，我使用了 bootstrap 中 card 样式。它简单到只要把父容器声明为 card-columns 类，card 元素的样式声明为 card 就可以了。此外，为了根据不同的屏幕大小，显示不同的 card 列数，可以使用媒体查询和 column-count 属性，在 docs/assets/templates/homepage.tpl 文件中有示例。

在 publish.py 脚本中，我使用了 frontmatter 来提取文章中的 meta，但它的速度有点慢。不过这是一个使用多进程加速的好场景：

---

```python
metas = []
articles = glob.glob("./docs/articles/**/*.md", recursive=True)
with ProcessPoolExecutor() as executor:
    results = executor.map(extract_article_meta, articles)
    metas.extend([meta for meta in results if meta is not None])
```

这样就可以多进程处理文件了。最终结果会汇总到 metas 这个数组中。

!!! tip "图片自动换新技巧"
    图片自动换新，可以给静态网站增加动态内容。让读者每次访问，都有不一样的感觉。这是通过 unsplash 网站的 gallery 功能来实现的。unsplash 是一个免费图片资源共享网站，提供了大量高清、很高质量的免费图片。如果我们将 img 元素的 url 指向'https://source.unsplash.com/random/360x200?{word}'这样的地址，unsplash 就会返回一个 360x200，并且其类别为 word 的图片。

## 发布到小红书

小红书发文不能超过 1000 字，并且很难格式化。如果要分享文字、代码并且做到混排，惟一的方法就是将其转换成为图片。这个步骤有点繁琐，不过，这也成为一种壁垒，导致深度内容在小红书上比较稀缺。因此，如果能搞定格式排版，这样就可以有效地利用小红书的分发。

我的方案是使用 slidev。它是一个基于 markdown 语法来创作在线演示的方案，提供了转换为图片的功能。

---

![R50](https://images.jieyu.ai/images/2024/01/xhs-sample.jpg)

因此，我们基于 mkdocs+material 创作的文档，只要加上少量的标记和定制，就可以很容易地转换成为图片。

要实现这个功能，在安装 slidev 之后，先进行主题定制。最重要的是 cover layout 的定制。右图就是我之前为小红书日更设计的一个首页样式。

我们可以设计多个样式，在导出时，使用下面的命令：

```bash
npx slidev export --format png -t /path/to/slidev_themes/special_theme_dir --output /tmp/xhs /path/to/src.md
```

我们需要在 markdown 内容中的合适位置，增加"---"作为分页符，这样就能导出一页页适合在小红书上发布的图片了。

## 发布到微信公众号

![L33](https://images.jieyu.ai/images/2024/01/md-nice.jpg)

微信公众号排版一直是个问题。我甚至一度放弃了公众号创作。作为技术极客，我拒绝了几乎任何不是基于 Markdown 的排版方案 -- 都什么年代了，写个自媒体都是赔钱的，平台还好意思要求我们专门为你们排版？

**直到我遇到了 mdnice。**

它甚至比我自己使用 mkdocs-material 的排版还要漂亮 -- 特别是它对代码的处理部分 -- 我超爱她深色主题下的 50 道阴影！

我现在也超爱写公众号了！不过，什么时候 mdnice 能实现 markdown 的 admonition 语法就更好了。毕竟，这是个信息过载的时代，我们必须用一些留白来缓解密集信息恐惧症，同时用一些闪耀的装饰吸引读者，避免他们走掉。

当然，mdnice 也可以直接发到 CSDN 上。不过，这样会失去定时发布以及自定义标签、选择专栏、定制首图的能力，所以，我宁愿自己登录到 CSDN 的网站上去编辑，好在，它提供了 markdown 编辑器，并且能自动处理图片链接。因此，我并不需要一个个地从本地上传，这省了我不少时间。

## 发布到知乎

如果你使用的是 vscode 来编辑 markdown 的话，就可以使用一个名为 Zhihu On VSCode 的扩展。它支持定时发布（一天以内）、选择专栏，但不支持添加话题，另外，它不能正确处理（去掉）frontmatter。

但是它能处理 markdown 中的图片链接。这样就省去了我上传图片的时间。它对代码也能很好处理。

不过，知乎的文档格式确实太素净了。

## 转换为 pdf
<img src="https://images.jieyu.ai/images/2024/01/mpe-export-as-pdf.jpg" width="180px" align="right">

slidev 也可以转换成为 pdf。不过，我更喜欢使用 vscode 的 markdown preview enhanced 来转换 pdf。最终提供转换的是 chrome+puppetter。通过在文档的 frontmatter 中加上适当的标记，就能生成页眉和页脚。

右图就是它导出的一例。

此外，slidev 也可以导出 pdf。要实现页眉和页脚，需要要定制 global-top 和 global-bottom，一旦定制完成，这种方案似乎更好，毕竟，它是手动分页，我们对页面的控制力更强。

## 赚点小钱

辛苦辛苦写了博客，想办法赚点钱吧。我们可以通过前面提到的 ovrrides 方案，让 mkdocs-material 为每个页面插入一个 js 脚本。

如果你加入了广告联盟，它们一般就会为你提供一个 js 脚本，把这个 js 插入进去就可以了。也可以自己写一个 js，把自己要发布的广告，以 html 片段的形式，放在 docs 目录下的某一个子目录中，然后通过下面的代码把这些片段插入进来：

```js
function insertAd(minParas, minWords){
    var links = document.querySelectorAll("a[href*='" + link + "']");
    if (links.length > 0){
        console.log("已添加")
        return
    }

    var paras = document.querySelectorAll("article p");
    var wordCount = 0
    var paraCount = 0
    var inserted = 0
    for (var i = 0; i < paras.length; i++){
        var p = paras[i];
        paraCount ++
        wordCount += p.innerText.length
        if (inserted >= 2){
            break
        }

        if (paraCount >= minParas && wordCount >= minWords) {
            console.log("find para", p, paraCount, wordCount)
            p.insertAdjacentHTML("afterend", ad)
            paraCount = 0
            wordCount = 0
            inserted += 1
        }
    }
    if (inserted == 0 & paras.length >= 5){
        var article = document.getElementsByTagName("article")[0]
        article.insertAdjacentHTML("beforeend", ad)
    }
}

document$.subscribe(function() {
    console.log("call in ad")
    insertAd(40, 4000)
})
```

这段代码实现了文中和文末插入。只有在文章内容足够长时，才会插入广告。同样地，完整的代码可以在 [zillionare](https://github.com/zillionare) 这个项目下找到。具体位置是 docs/overrides/javascripts/course.js。注意不要使用 ad.js 这样好听好记的名字，它会被 adblock 这样的浏览器扩展拦截！
