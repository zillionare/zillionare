---
title: "Augment Remote Agent: 有了本地Agent，为什么你还需要Remote Agent?"
date: 2025-06-10
img: https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/remote-poster.png
categories:
  - tools
tags:
  - augment
  - remote-agent
  - AI-tools
---

6 月 7 日，当我启动 Augment 准备继续编写策略时，弹出一条消息提示，大致是，我们刚刚发布了 Remote Agent，你要不要试一试？这个试用需要登录 github 账号，所以我的第一直觉就是，关掉它，我不需要它。

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/get-remote-agent.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

但是，当我在使用本地 Agent 解决一个问题时，有时候它会工作很长时间，期间我不能改动工作区的文件，同时操作很容易引起冲突。

于是我又想到了 remote agent，以下是测试报告。

## remote agent 适合在什么场景下使用？

!!! tip
    1. 适合多个功能同时开发。这与传统团队中，多人同时开发多个功能是一样的。但是，现在是由 augment 为你组建了一个新的开发团队，并且配置了机器。
    2. 功能完成了，根据实现的功能来编写文档。
    3. 执行 CI/CD 等任务，并修复 bug，提高测试覆盖率。![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/remote-poster.png)
    4. 在开发功能的同时，有一些紧急的 bug 需要立即修复。
    5. 自信地重构代码（请先确保你一开始就有定整的单元测试以及 CI/CD！）


尽管 remote agent 相当于给我们提供了另外一个开发环境，但这并不是多么明显的优势：你很可能已经购买了机器；使用 remote agent 的 session，也仍然算在你的可用次数之中，所以，与本地 agent 比，它们并没有显著的成本优势。

那么，除了运行 remote agent 时，开发人员还可以继续工作之外，remote agent 究竟还有哪些令人难以抗拒的优点呢？

这我们得先从它的工作方式说起。这部分在网上讲解的比较少，我通过多次试用，有了一些初步的认识。

## Remote Agent 的工作方式

开启 remote agent 时，它会在远程为你创建一个沙盒。我当前工作的一个项目，开发机环境是 mac os arm， python 3.13. 它创建的沙盒是 linux， ubuntu 22.04，python 版本是 3.10。这部分目前没有看到可以配置的地方（也许应该通过 promt 来提示 Augment）。多数情况下，对 Python 开发者来说，不应该是太大的问题。

这个沙盒会从 github 获得你的代码，这需要你的工作的项目是通过 github 托管的。

最终，我看到它把仓库代码下载到了沙盒中/mnt/persist/workspace 目录。

!!! note
    如果你担心代码的安全问题，我觉得要么完全不用 AI，要么就信任一些值得信任的公司。但是，既要 AI 协助开发，又不让他读取代码，理论是不可能的。因此，无论是本地 Agent，还是 remote agent，在完全性上，实际上没有差别。


它对代码的修改都发生在这个目录下。

当它完成任务后，它会通过对话面板告诉你，它进行了哪些修改，并可能会列出修改的代码：

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/remote-agent-apply.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

如果你不熟悉 remote agent 的工作方式，可能会有点不适应。在这个对话面板里，它只是摘要地告诉你它已经完成了的工作。如果我们认可并要应用这些修改，我们无法从这里获取修改后的完整代码，并应用到正在工作的工作区间。这与本地 Agent 的工作方式是不一样的：本地 Agent 会直接修改你的代码。

那么，正确的『应用』方式应该是什么呢？是通过创建 PR：

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/work-with-remote-agent.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

点击『Create a PR』按钮，它就会把远端的代码提交到 github 并创建一个 PR，然后你通过代码合并来应用这次修改。

跟 Claude 4 大模型，以及 Agument 自身训练的模型相比，这只是一个微不足道的小创新，并不需要多么高深的技术。但不得不说，Augment 很懂软件开发流程。这恰恰是当前 AI 的痛点 -- 我们既享受它带来的帮助，又要无时不刻忍受它的幻觉和随意发挥、甚至搞乱我们的代码。如何通过 AI 来促进软件开发质量，从做出基本功能进化到高质量的软件产品，推进先进的开发流程，Augment 率先迈出了一步。

如果你还不适应通过 PR 方式进行代码合并，那么，你也可以通过『Open remote workspace』来浏览它所做的修改。点击这个按钮后，它会打开一个新的 vscode 窗口，只不过工作区显示的是远程目录

## Remote Agent 的优点

在 Augment 的 blog 中，已经介绍了 remote agent 的优点 -- 它的使用场景，就是它的优点。不过，抛开这些不谈，单纯比较本地 Agent 与 remote Agent 的码代码能力，我也有以下感觉：

!!! tip
    * 它似乎能看到更多的代码，修复 bug 的能力更强。如果是这样，也并不奇怪。因为它可以在远程把你整个仓库 clone 到沙盒里；如果 agent 运行在本地，我不确信能否把一个宏大的工程都加载到远程。

    * 它拥有更干净、完全自主可控的环境。因此，它的工作效率似乎更高。在这个环境下，它不受打扰，环境不发生错误，很多时候，是用户、和错误的环境干扰了本地 Agent 的工作。


今天的 local agent 面临的状况，其实就是无数打工牛马面临的状况：一个爱指指戳戳、又不了解情况的老板指挥着你干活，他常常发出错误的指令，而你既要把工作推进下去，还要证明你老板的正确性！

Remote Agent 则是更自由的牛马。它工作在一个不受干扰的理想国。
