---
title: 做能调教AI的赛博老技师，量化人也该开始装Skills了
date: 2026-03-26
excerpt: Skills Marketplace 让量化人把 Tushare、XtQuant、BaoStock 这类 A 股上下文装进 AI 工作流，比多一个 prompt 更重要。
category: others
tags: [Agent Skills, Skills Marketplace, VS Code, Tushare, XtQuant, BaoStock, A股, 量化]
font: "阿里巴巴普惠体-Regular"
addons:
  - quantide-palette
  - quantide-admonition
  - quantide-layout-xhs
aspectRatio: 3/4
canvasWidth: 600
img: https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/skillsmp.png
layout: cover-photo-down
---

在 AI 时代，作为个人量化者，开发策略似乎已变得更简单：你已可以让 AI 帮你手搓一个动量策略，或者解释多因子中性化。

但个人量化者的核心困境，往往卡在数据获取的“最后一公里”。那些成本上能负担的数据源，经常伴随着 API 命名随意、文档过时或残缺的问题。这种非标准化的基建，不光人写起代码来如履薄冰，就是把 Claude 这种顶级大模型请来，没有正确的上下文它也得犯愁。

而 skill，正是把这些上下文包装成可复用能力的一种方式。

最近我在 [skillsmp.com/zh](https://skillsmp.com/zh) 上看了一圈，发现它已经不只是“程序员玩具市场”了。里面已经有一批和金融、投资、尤其是 A 股量化工作流直接相关的 skills。

## 如果你还不知道什么是 Skill

最早大家用 AI，都是通过写 prompt，谁会描述问题，谁就先占一点便宜。写一个好的提示词并不容易，所以就出现了拿着高薪的提示词工程师岗位。

!!! tip
    2026年，第一批高薪的提示词工程师（prompt engineer）已经下岗了，转行做了『技师』。

但这很快暴露出几个问题：

- 好 prompt 很难复用
- 换一个人、换一次对话，质量就波动
- 需要背景知识的任务，每次都得重新喂上下文
- 只靠 prompt 很难携带脚本、模板和长文档

于是第二阶段出现了 prompt library、prompt file、slash command 这类东西。它们把常用任务收束成一个个模板，解决了“重复输入”的问题，也让团队能共享一部分工作方式。

但问题并没有彻底解决。因为 prompt 再好，本质上仍然偏向“这一次帮我做什么”。它擅长明确任务，不擅长封装长期知识和规范。

这时候，skill 就开始显出必要性了。skill 的核心价值不是多一个命令，而是把知识、最佳实践、工作流以及资源文件打包成可渐进加载的能力单元。模型一开始只看名称和描述，真正相关时再加载完整内容，所以它比“把所有说明都塞进系统提示词”更省 token，也更容易维护。

Anthropic 在 2025 年 10 月围绕 agent skills，连续发布了介绍和使用文档；随后 OpenAI 也在 Codex CLI 和 ChatGPT 里采用了相同格式，到现在， Trae, Vscode 等主力开发工具，以及 Openclaw 都支持了这种格式。Skill 也从 Anthopic 的先锋探索，变成一种跨工具流通的工作流封装格式。


## 为什么量化人应该关心这个 marketplace？

skillsmp 是目前规模最大的 marketplace，到今年3月止，已经上架了超过63万+的技能，许多技能得到了超百万的 star。早期它是由 Manus (现在该团队属于 meta)维护，现在已变成了社区维护，非常活跃。

!!! tip
    skills 现在火到什么程度？当你访问 skillsmp的时候，有很大机会遇到生物体校验。普通的网站上可享受不到这个『待遇』。


![极客范的 skillsmp 网站](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/skillsmp.png)

skillsmp 按类别归类各种 skills，对量化人来说，可以多看看金融与投资分类，这里有20270个技能。当然数据与 AI分类下的机器学习、数据分析等子类，也是值得多看看的。

接下来我们就会推荐几个量化人常用的关键 skills，不过在此之前，我先介绍如何寻找、安装和使用 skills。

在 skillsmp 上除了按分类浏览我们感兴趣的 skills 之外，你还可以直接搜索。比如，如果你想要让 AI 更准确地使用 akshare 的数据 API，就可以用 akshare 作为关键词来搜索，然后看看点赞数最高的几个就好。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/find-akshare.png)

然后点击这个卡片，我们就可以看到 akshare 这个 skill 的各项资产。

!!! attention
    skillsmp 不是苹果应用商店。它对上面发布的各项 skills，几乎没有任何审查。考虑到 skills 可以携带各种脚本（比如 python 脚本），它们可能在你本机上被**自动调用并运行**，所以，对 skills 的内容进行安全审查非常重要。顺便提一句，litellm 最近就曝出一个非常严重的安全漏洞，会盗取你机器上一切秘密。你可以使用以下方法自查：`pip show litellm`


找到心水的 skills 之后，就可以根据你如何使用 AI大模型来安装它。

如果你使用的是 openclaw，或者 claude code, GPT codex 等，就可以在命令行下，运行这个命令来安装它（请参考 skills 详情页面右侧的安装命令，以下仅为示意）：

```bash
npx skills add openclaw/skills
```

如果你正在使用 trae 或者 vscode 这一类 IDE 工具，则可以下载相应的 zip 包，再复制到IDE 工具指定的目录。比如，如果你在使用 vscode，则需要把 skills 的 zip 包解压缩（注意根目录下一定要有 SKILL.md 这个文件才对）后，复制到.github/skills 目录下。


下面的图显示了如何下载 skills 的 zip 包。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/skills-how-to-install.png)

安装好 skills之后，你就可以通过 slash 命令来使用它（或者验证安装成功）。我们以后面会安装的 tushare 为例，演示一下在 vscode 中如何验证安装成功。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/tushare-skill-verify.png)

截图来自 vscode 的 AI chat窗口。通过 slash 命令及它的提示，我们验证了安装成功。此后，在你写代码时，这些 skills 会自动触发。

## 量化人必装的 skills

**所有的软件文档都是糟糕的，但其中有一些更糟糕**。

我们安装 skills，可以省下自己去阅读这些天书一般的文档，也可以让 AI 更懂得如何去使用这些 API。

第一个必须要安装的 skills，可能就是 xtquant 的 skills -- 如果你正要使用 qmt/xtquant 来进行实盘交易或者获取行情数据的话。

通过 xtquant 关键词，你会搜索出来好几个 skills，建议点击来自 openclaw/skills 的 xtquant.md这一个，目前它有3.3k star。

下载它的 zip 包之后，我们发现它包含了 xtquant 的全部文档，文件大小有100多k，还包含了一个 demo.py。

前面我们介绍了 akshare 的 skills 也在这个市场上发布了，不过，现在东财对爬虫的限制比较严重，通过 akshare 已经很难大规模获取数据了。

替代方案之一是 tushare。在 skillsmp 上有多个 tushare 的 skills，不过它们都不是官方发布的，所以，在这里也提示一下，**不要从这里安装**。tushare 的skills如何安装，在 tushare 的官网上有介绍。

比如，如果你是在 openclaw 里面，可以这样安装：

```bash
clawhub install tushare-data
```

当使用 vscode 等工具时，可以在 [https://tushare.pro/files/pro/tushare-data.zip](https://tushare.pro/files/pro/tushare-data.zip)这里下载。

baostock 是一个免费的行情数据源。你也可以在skillsmp 上找到如何使用它的 skills。

## 主观投资者

在 skillsmp 中还有一些适合主观投资者使用的 skills。比如， market-research.md，用来进行市场研究、竞争分析、投资者尽职调查和行业情报，附带来源归属和决策导向的摘要。

这里还有一个东财的 skills，eastmoney-trading.md。东方财富证券交易技能，支持自动登录、持仓查询、持仓分析、条件选股、买入、卖出、撤单、委托查询、资金查询等完整交易功能。使用 CDP 连接浏览器，支持验证码自动识别。不过，作者自己也标注出来，这是高风险操作，使用要谨慎。如果要实现 API 级的实盘交易，还是找人开通量化交易接口吧。

如果你觉得实时跟踪财经新闻很重要，可以安装 finance-news-source 这个 skills。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260326151611.png)

不过，如果想要实时获得这些新闻，这个在 trae/vscode 中不太行，还是安装一个 claude code 或者 openclaw 吧。他们是最好的技师。
