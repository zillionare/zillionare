---
title: 既生瑜 何生亮！ Hermes Agent究竟怎么样？
excerpt: 从安装失败到‘Eureka’时刻，Hermes Agent 和 OpenClaw 就像‘既生瑜，何生亮’，一个自带武装，一个手动挡，究竟谁更胜一筹？
date: 2026-04-13
category: tools
tags: 
  - tools
  - OpenClaw
  - "Hermes Agent"
  - Agent
---



在较深度地使用了 OpenClaw 之后，还是非常想尝试一下 HermesAgent。使用了一天之后，现在可以得出结论：很难比较 OpenClaw 和 Hermes 哪一个更好，因为两者都在快速迭代之中，每一天或者几天就有较大的改进。

但是两个显然都非常好，都属于值得一用的状态。

不过，在我前几天使用 OpenClaw 的时候，它确实在安装和维护上体验会差一些，更像是一部手动档的车。我记得要先切换 nodejs 版本，设置 npm 国内源，安装 bun 等等。

Hermes Agent 对依赖几乎是自包含的。实际上它的依赖还要更多--在 nodejs 之外，还要依赖 python.但是 Hermes 把所有的依赖都打包在一起了，所以你只需要从一个安装包开始，就能安装到底，中间应该是不需要再访问网络。

当然这个安装包仍然放在 github 上，访问速度和稳定性还是有一定的限制。

这一篇不做测评，就是把 Hermes Agent 安装之后，如何零帧起手，到让他做一些有用的任务，这个过程分享给大家。

## 第一次安装也失败了

第一次安装 Hermes 的时候，我还是失败了。后来通过查询日志才发现，应该是我输入 API key 的时候输入错了。Hermes 似乎在这里少了一次对模型的验证。如果 API 输入正确的话，它会列出可用的模型列表；反倒是如果 API Key 输错了，它并没有给出足够的提示，还会让你继续往下进行设置，这样最终会导致安装失败。

我使用的版本是 0.8.0，是一个 5 天前的版本。当你读到这篇文章时，这个行为可能略有不同。

我选择的是快速安装。在这种模式下，只需要你提供大模型的配置以及通信渠道的配置。剩下的安装，我选择通过微信来指挥 Agent 进行安装设置。

我觉得这样才是正确使用 Agent 的方式。

!!! tip
    安装完一遍 Hermes Agent 之后，我大概知道他们为什么做这个产品了。在模型列表中，第一个被推荐的就是他们自己的模型。尽管这几天 token 涨得一词难求，但长远来看，很可能会陷入过过剩状态。90%的人，可能用到 Claude Opus 4.6生成的 token 就足够好了，没有必要去消费更高级的 token.

## Hermes 的自我武装

我把这种安装称作 Hermes 的自我武装。而且我并不懂 Hermes 应该怎么配置，所以，我先问它（实际上是在问大模型）：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413174049.png)

这里列出了很多很详细的内容，但其实这并不是我需要的。所以我接下来直接告诉他：“你帮我，我启用 Web 和 Browser 这两个工具。”

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413174220.png)

然后我决定给他分配一个单独的邮箱，因为很多网站注册时，特别是国外网站，往往都是可以通过邮箱来注册，只要收到验证邮件就可以完成注册了。

这里我会告诉他，『如果后面收到什么邮件，让他执行什么操作，都必须通过微信报告得到批准才能执行』。

这是因为邮箱是一个公开的媒介，任何人只要有邮箱地址都可以给他发邮件，所以这是一个安全的 surface point。当然，一定不要太过相信大模型的指令遵循能力，一旦这个邮箱暴露，其实还是很容易通过邮箱来攻破你的 hermes agent的。

这里还很奇怪，出现了一个设置哈玛拉雅，不知道这是不是所谓的幻觉。

第一个 Eureka 的时刻出现在这个截图的下方，它提示当前环境的 DNS 解析有问题。这个问题很奇怪，这台机器显然不应该有网络问题。因为我们刚刚安装了 Hermes agent，并且能够访问 GitHub。

无赖的人工智障。我当时是这么想的。跟人一样，一出错误就往网络波动上面推。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413175016.png)

但是很快我发现，它第一次调用了工具，写了个脚本。不过现在还分不清，这是 Hermes Agent 的能力，还是 Kimi K2.5 的能力。

很快，惊喜到来。它没有被这个错误所阻挡，还是把邮件发出来了。而且，还发现是我的 wifi 设置错误，这确实是有点神奇了。如果有程序员认为大模型不能取代我们做部署，那你现在可要改变认知了。

颤抖吧碳基生物！ 

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413180418.png)


这里比较奇怪，它的回答断断续续的。从技术上讲，这是在回复时启用了 streaming 机制，产生一点结果，一点消息就回复用户，可以避免用户长时间等待。

但这里也确实让我有一点感受到，她是不是有点为这个神奇的发现而雀跃的心态？

不过，后面几乎就再也没出现过这种『streaming』输出了，不知道为何。


接下来，因为已经出现了访问限速问题，我让它给自己加一个 key。这里出现了第一次安全确认：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413181203.png)

不过，Hermes 的安全意识是有了，但是这次遵循得并不好。这也有背后模型切换等部分原因。

接下来我打算启用多 Agent。目标是，每个 Agent 都有自己的会话和记忆，这样他们的上下文就会更纯粹一些，这样对大模型更加友好。另外我也希望，只有特别复杂的任务，比如复杂的编程，才使用更高端的模型，这样对 token 更加友好。而普通的任务分派跟踪，使用免费的模型就可以了。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413181820.png)

这是它给出的架构图：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413181858.png)

从概念上说，它确实搞清楚了。究竟执行得怎么样？

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413182149.png)

从落地情况来看，每个 Agent 已经生成了自己的文件夹和自己的记忆。

不过，接下来的一次会话，暴露了这个架构并没有落到实处，它只是个面子工程。这是为了给 Devon 增加新的 api KEY引起的。这个时候 Agent 说他没有办法修改 .env，让我去修改，但同时又让我把 Key 给他。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413182807.png)

从这时起，实际上三个 Agent 才真正落地.这是主会话的反馈：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413182901.png)

眼见为实，我还是去查看了 hermes 的目录：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413183230.png)

现在，每个 Agent 都有了自己的 cron, state.db 文件和 skills 文件夹。现在我们可以确信，这些 Agent 都已经是『物理』意义上的 Agent 了，不再是逻辑概念。

从现在起，每个人都应该有自己的独立记忆，而不应该混同在一个 session 中，但不知道 Hermes是否真的做到了这一点。

## 自我进化

接下来就是看它的自我进化能力了。

我的第一个反馈是，让它定时报告进度。因为刚开始设置，很担心它是否还在呼吸。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413183633.png)


然后出现的问题就是报告太长，所以给它一个指令：

> [!quote]
> eve, 报告进度时，要简明，可以使用 task check 的方式发出来，如果已完成，就使用✅。如果执行不下去，就放一个⚠️此时不发帮助信息，也不发下一步任务建议。

> 让 Muse 开始收集这个话题的资料吧，准备核心观点和资料。A 股全面适用盘后固定价格交易，固定价格的盘后交易影响大吗？对量化交易有何影响？

第一次报告格式很乱，于是又给出指令：

> [!quote]
> 任务与任务之间要有换行，每个任务一行或者一段。已经完成的任务，连续报告两次后，就不再报告

立刻改进了：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413183934.png)

在这个期间，还触发了一次自动创建 skill。是因为第一次安装 claude-code 时其实失败了，但 Agent 给我报告安装成功。待我纠正事实后，Agent 自我反省，并且在成功安装之后，创建了一个新的 skill:

> [!quote]
> 💾 Cron job 'Eve进度报告' created. · Skill 'npm-package-diagnosis' created.
>

从这一点来说，Hermes 的『进化』还是真正落实了，不止是一个概念。自己创建的 skill，要远比从marketplace 搜索安装的合身、安全。

## 量化人关心的功能

今天一位朋友跟我讲，妙想（东财的大模型）有了 skills，并且接入了 openclaw。所以，我们来试一下，Hermes 能否自己接入这个 skills，并且为我们提供一点信息。

这个 skills 的安装很简单。但需要你在东财的 app 上申请。

首先，在搜索栏中搜索妙想，就会出现下图：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/d834699600b7211d803ca3bb926b62bb.jpg)

点击妙想 skills，就会出现这个界面：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/e6711f9a615f237d576af370ba60a24e.jpg)

按提示复制提示词，发给 Agent。很快，它就配置好了：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413194217.png)

随后问了它一个问题：

> [!quote]
>  测试资讯搜索功能。今天的市场热点是什么
>

结果就不展示了，需要全程打码。目前你可以用这个 skill 做什么？如果你有事件策略，苦于新闻资讯不太好拿，那么大概率这个 skill 可以帮到你。

还是来点可以展示的：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260413200322.png)

尝一口鲜是好的，天天吃可能暂时还受不了。从性能上来看，它采用了每支股票查询一次的方法，全部查下来花了近30秒。



最后，我关心的那个问题，『A 股全面适用盘后固定价格交易，固定价格的盘后交易影响大吗？对量化交易有何影响？ 』， 已经过去3个小时了，Muse还在查资料。Eve 看了她的 cronjob 输出，说是已经到了『正在进行用户需求分析和创意方案生成，最近专注于界面设计优化』的阶段了。

这步子迈得有点大了。谁让她做界面优化设计了？这是要做一个网站出来？








