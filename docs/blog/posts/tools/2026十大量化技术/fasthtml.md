---
title: "量化新基建(三) - FastHTML：Python 全栈开发的终极答案"
date: 2026-01-11
img: https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110212357.png
excerpt: 这是2026量化新基建的第三篇文章了。我们的目标是介绍2026年，要打造一个量化交易系统，你可能（应该）使用的那些技术。今天我们要介绍的是，在2026年，你该使用什么样的技术来构建量化交易系统的前端。
categories: tools
tags: [tools, sqlite, sqlite-utils, fastlite]
addons:
  - slidev_themes/addons/slidev-addon-quantide-layout
  - slidev_themes/addons/slidev-addon-mouse-trail-pen
  - slidev_themes/addons/slidev-addon-array
  - slidev_themes/addons/slidev-addon-interactive-table
  - slidev_themes/addons/slidev-addon-card
aspectRatio: 3/4
layout: cover-random-img-portrait
---


这是2026量化新基建的第三篇文章了。我们的目标是介绍2026年，要打造一个量化交易系统，你可能（应该）使用的那些技术。

今天我们要介绍的是，在2026年，你该使用什么样的技术来构建量化交易系统的前端。

<div style='width:80%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110212357.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>澳大利亚国立大学，抛物面太阳能聚光器</span>
<span style='font-size:0.7em;display:inline-block;width:100%;text-align:center;color:grey'>by Toby Hudson@wikimedia</span>
</div>


在互联网上，人们把提供免费资源和服务的人/公司称为赛博活佛。最有名的赛博活佛当属 cloudflare 了。不过，我愿把 fast.ai 的创始人 Jeremy教授也称为赛博活佛，因为他开发了一系列以 fast 开头的软件产品，比如 fastai, fastlite, fasthtml 等。

时间是为数不多的、每个人都公平拥有的资源之一。在这个意义上，如果有一种技术能提高时间的效率，我想它就能称得上是赛博活佛。

拥抱 fasthtml，原因正是如此。

不过，要真正理解 FastHTML 的革命性，我们需要先回头看看，在这个领域里，目前的统治者是谁，以及它为什么还不够完美。

## 曾经的王者：Streamlit

streamlit 的创始人是Adrien Treuille（CEO），Thiago Teixeira 和 Amanda Kelly，三位创始人此前都曾在 Google X 工作。

Adrien Treuille 曾是卡内基梅隆大学的计算机科学教授，在 Google X 期间，他深刻体会到了数据科学家面临的痛点：作为数据科学家（量化策略研究员也感同身受），他们使用的母语是 Python，而 Python 无法用来构建 Web 应用，因而他们无法独立构建一个哪怕是最简单的数据应用。

要构建一个具有完美交互体验的 web 应用，你需要掌握 html/css/javascript/typescript/react/vuejs 等技术，而这一直是前端工程师的封邑。

Treuille等人于是决定，要开发一个完全基于 Python 的 web 框架。与大家熟悉的 Django, Flask 等Python web框架不同，它不仅同样具有 web 服务器的功能，更重要的是，前端组件也可以只使用 Python对象甚至是 markdown 文本来构建，如此一来，你几乎可以不用掌握前端知识。

在 Streamlit 诞生之前，市场上已经有一些类似的方案，比如 Plotly Dash，这是我们在量化24课中介绍过的。Plotly Dash非常强大和灵活。但是，Complexity is the tax on flexibility，Plotly Dash 的学习曲线并不平缓。

这让 streamlit 获得了出圈的机会。凭借极致的简单，streamlit几乎将开发 web应用的门槛成功降到了零，成为了 Python 数据科学家展示工作的首选工具。截止目前，它已经在 github 上拿到了43k 的 stars，并且在2022年被 snowflake 以8亿美元收购。

![使用 streamlit 开发的量化程序](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110174624.png)

Streamlit 的成功是现象级的，就像当年的《疯狂动物城》一样，一经发布就凭借完美的设定横扫全场。 面对这样一部已经封神的经典，你可能会像现在审视《疯狂动物城2》一样心存疑问：在珠玉在前的情况下，这个赛道里真的还有讲新故事的空间吗？后来者还有机会超越前者留下的天花板吗？

事实上，技术世界里从来没有终局。Streamlit 开发确实很快，但是，一旦你的应用获得成功，你很可能就必须重写它，才能支撑成千上万人使用，并且满足他们对极致交互体验的需求。

看到了这一点的，是 fast.ai 的创始人 Jeremy Howard。他带着 FastHTML 走来了，试图告诉我们： Python 程序员不应该在“简单”和“强大”之间做选择题，我们全都要。


## 不妥协的 fasthtml

Streamlit的极致简单是以牺牲灵活性和性能为代价的。Streamlit 做出来的网页难免有千人一面之感，并且有一些交互场景无法实现。此外，在性能上也有所不足。

Fasthtml则完全没有这样的问题，这得益于它构建于两种非常出色的框架之上： starlette和htmx。

Starlette 是一个基于 ASGI 协议的轻量级 Python web 框架，它也是当下最热门的 FastAPI 的核心基石。简单来说，**FastAPI = Starlette + Pydantic（数据验证）+ OpenAPI（自动文档）**；而 Jeremy Howard 教授构建的 **FastHTML**，则是 **Starlette + HTMX + Python 组件系统**。它利用 Starlette 保证了后端的高性能，引入 HTMX 解决了无需编写 JS 即可实现的前端交互，并将 HTML 标签封装为 Python 对象，让开发者能以纯 Python 的方式构建现代 Web 应用。

对于大多数 Python 开发者来说，Starlette 已经是老朋友了，它是 FastAPI 的坚实地基，以高性能和稳定性著称。这里我们不再赘述。

真正让 FastHTML 拥有“点石成金”魔力的，是 **HTMX**。

## 魔法的核心：HTMX

如果你是一个典型的后端开发者，你可能对前端的复杂性深恶痛绝：为了让一个按钮更新页面的一部分，你不得不引入 React/Vue，配置 Webpack，并且编写后端 API 进行联调。

HTMX 的出现，就是为了终结这场噩梦。它允许你直接在 HTML 标签中使用属性（attributes）来驱动现代化的交互。

比如，传统的 HTML 只能通过 `<a>` 和 `<form>` 发起请求。而 HTMX 允许任何元素（比如 `<div>`, `<button>`）发起 HTTP 请求（GET, POST, PUT, DELETE），并且用服务器返回的 HTML 片段直接替换页面上的某一部分。

这意味着，**你不再需要编写 JavaScript 来处理前后端通信和 DOM 更新**。所有的逻辑，都回到了你最熟悉的 Python 后端。

这正是 FastHTML 的精髓所在。它利用 Python 的表达力，将 HTML 标签封装为一个个 Python 对象（组件）。当代码运行时，这些对象被“编译”成带有 HTMX 属性的标准 HTML。这意味着，你可以用纯 Python 代码，轻松定义出能够**局部刷新**的页面组件。

相比而言，Streamlit 的设计哲学是“一旦有交互，重跑整个脚本（Rerun）”。这种机制虽然简单，但在处理复杂交互时显得笨重。虽然 Streamlit 在 **1.37.0** 版本（2024年中）终于推出了 `st.fragment` 装饰器来试图实现类似的局部刷新功能，但相比于 FastHTML 从底层就基于“组件+局部交换”的设计，前者更像是一个迟到的补丁，而后者则是原生的高性能引擎。

## 炙手可热的新星

这种“回归简单”的理念，正在席卷整个开发界。

*   **HTMX**：它已经是前端领域的“当红炸子鸡”。在 2024 年的 JavaScript Rising Stars 评选中，HTMX 的 GitHub Star 增长数甚至超过了 React 和 Vue，目前总星标数已突破 **44k**。它代表了一种反思：也许我们并不需要那么复杂的 JS 框架。
*   **FastHTML**：作为 Python 界的 HTMX 最佳拍档，它虽然在 **2024 年 8 月**才刚刚发布，但凭借 Jeremy Howard 的号召力和直击痛点的设计，短短几个月内就在 GitHub 上斩获了超过 **6.6k** stars（截至 2026 年初）。

这不仅仅是两个库的结合，更是一场“去复杂化”的运动。删繁就简三秋树，标新立异二月花。fasthtml 正是同时做到了化简和创新。

## FastHTML 快速上手

FastHTML 的设计哲学是“显式优于隐式”，同时保持极致的简洁。你不需要配置路由表、不需要设置模板目录，甚至不需要手动启动服务器（如果你使用 `serve()`）。

### 1. Hello, World!

让我们看一个最小的 FastHTML 应用：

```python
from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("FastHTML Demo", 
        Div(
            H1("Hello, World!"),
            P("这是我的第一个 FastHTML 应用")
        )
    )

serve()
```

运行这段代码，一个完整的 Web 服务器就启动了。这里有几个关键点：
*   **`fast_app()`**：初始化应用，返回 `app` 对象和路由装饰器 `rt`。
*   **Python 组件**：`Div`, `H1`, `P` 都是 Python 类。你不再需要手写 `<p>...</p>` 这样的标签，而是像搭积木一样用 Python 对象构建页面。这不仅避免了拼写错误，还能享受到 IDE 的自动补全。

### 2. 添加交互 (HTMX)

现在的页面是静态的。让我们加点“魔法”，做一个无需 JS 的计数器：

```python
from fasthtml.common import *
count = 0

app, rt = fast_app()
@rt("/")
def get():
    return Titled("计数器",
        Div(
            H1(f"当前计数: {count}"),
            # 点击按钮时，向 /increment 发送 POST 请求
            # 并将返回的内容替换掉 id 为 'counter' 的元素
            Button("点我 +1", hx_post="/increment", hx_target="#counter", hx_swap="innerHTML"),
            id="counter"
        )
    )

@rt("/increment")
def post():
    global count
    count += 1
    # 只返回更新后的部分 HTML
    return Div(
        H1(f"当前计数: {count}"),
        Button("点我 +1", hx_post="/increment", hx_target="#counter", hx_swap="innerHTML")
    )

serve()
```

在这个例子中：
1.  `hx_post="/increment"`：告诉前端，点击按钮时向 `/increment` 发送 POST 请求。
2.  `hx_target="#counter"`：告诉前端，拿到服务器返回的结果后，找到页面上 `id="counter"` 的元素。
3.  `hx_swap="innerHTML"`：用返回的内容替换掉目标元素内部的内容。
   
![fasthtml 生成的SPA应用](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110213304.png)

整个过程**没有一行 JavaScript**，不可思议地简洁，但用户体验却是无刷新的、流畅的单页应用（SPA）级体验。

## Jeremy 的“个人印记”

如果你了解 fast.ai 的创始人 Jeremy Howard，就会发现 FastHTML 的每一个设计细节，都深深打上了他的个人哲学烙印：**实用主义**与**探索式编程**。

### 1. 像数据分析一样写 Web (nbdev 基因)

Jeremy 是 **Jupyter Notebook** 的狂热信徒，他甚至开发了 `nbdev` 系统，倡导直接在 Notebook 中开发生产级代码。他认为，编程不应该是“盲写代码 -> 启动服务 -> 刷新浏览器”的循环，而应该是**实时交互与反馈**的过程。

FastHTML 完美继承了这一基因。你可以直接在 Notebook 单元格中定义路由、编写组件，然后调用 `serve()`。应用会直接在 Notebook 输出区运行，支持热重载。

这意味着，Web 开发终于可以像数据分析一样：写一行代码，立刻看到结果。对于习惯了 REPL 体验的 Python 开发者来说，这种“探索式编程”的快感是难以抗拒的。

### 2. 为 AI 时代而生 (AI-First)

作为顶级 AI 专家，Jeremy 比任何人都清楚：**在 2024 年，如果一个新框架不能被 AI 熟练掌握，它就没有未来。**

由于 FastHTML 太新，ChatGPT 等大模型对它一无所知。Jeremy 没有等待模型重新训练，而是主动出击，制定了 **`llms.txt`** 标准，并为 FastHTML 提供了专门的“AI 知识胶囊”：`/llms-ctx.txt`。

这体现了他一贯的务实风格：**不仅要让人觉得好用，还要让 AI 觉得好懂。** 你只需要把这个文件喂给 Cursor 或 Claude，它们瞬间就能变身 FastHTML 专家。这种“AI 原生”的文档设计，可能是未来所有开源项目的标配。

## 关于美学？

这是一个非常现实的问题。长期以来，Python 开发者构建的 Web 应用（比如早期的 Streamlit 或 Gradio）总有一种“工科生的粗犷感”，很难达到商业级的美感。

FastHTML 在这方面做了两手准备：

**下限很高（Pico CSS）**：默认情况下，FastHTML 会自动启用 **Pico CSS**。这是一个极简的 CSS 框架，它不需要你写任何 class，就能让标准的 HTML 元素（按钮、表单、表格）拥有现代、干净的外观，并且自动支持深色模式。这意味着，即使你对 CSS 一窍不通，写出来的应用也是“体面”的。

**上限无限（Tailwind CSS 等）**：如果你对美观度有极致追求，FastHTML 生成的本质上是标准 HTML，因此它兼容所有的 CSS 生态。所以，你可以直接使用 **Tailwind CSS**（目前最流行的原子化 CSS 框架）来定制每一个像素。同时，你可以引入任何第三方的 CSS 库或自定义样式表。

## 结语：让技术回归服务

FastHTML 的官网是 [fastht.ml](https://fastht.ml)，你可以在上面找到更多的示例和文档。

---

至此，我们的**“2026 量化新基建”**系列已经介绍了三块拼图：

1.  **uv & Pydantic**：用极速的包管理和严格的数据验证，夯实了**工程地基**。
2.  **SQLite (WAL)**：用无需运维的高性能单文件数据库，解决了**数据存储**的痛点。
3.  **FastHTML**：用纯 Python 的 Web 框架，打通了**交互与展示**的最后一公里。

这一系列技术选型的共同点是：**反内卷，重实效**。它们都不追求“大而全”的企业级架构，而是致力于让个人开发者和小团队以最小的认知负担，构建出高性能、高可用的量化系统。

在 2026 年，技术的门槛应该被踏平，而不是被筑高。希望这套“新基建”能帮你从繁琐的基建工作中解放出来，把最宝贵的精力，投入到 Alpha 的挖掘中去。

