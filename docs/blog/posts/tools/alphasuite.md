---
title: "不只是另一个量化轮子，AlphaSuite还带来了CANSLIM模型的提示词"
date: 2025-09-17
category: tools
slug: alphasuite-canslim
img: https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/square/food/16.jpg
except: |
    AlphaSuite，又一个开源量化新项目。不过，这个轮子至少引入了 CANSLIM投资模型，也为我们使用 LLM 进行投资分析打了个样
tags:
  - risk-management
  - llm
  - prompt
  - CANSLIM
---


许多量化人都会构建自己的量化库，为此投入了大量时间。这样做真的值得吗？我个人的答案是肯定的，因为我也是千千万万个自己造轮子的人之一。

探索的意义就在于探索本身。物理学家费曼一生留下许多名言，这一句正好说明了为什么值得重复去造轮子：

!!! info
    What I cannot create, I do not understand。
    1988年2月，费曼去世后，人们在他的办公室黑板上发现了这句话。

上个世纪的司机，往往也是会自己修理汽车的人。有的水手喜欢亲手打造自己的帆船。自己造框架的量化人也是这样。我们追求的，也许并不是要造出一艘永不沉没的巨轮，而是在拼接每一块木板，校准每一根缆绳的过程中，学会倾听风的声音，读懂浪的脾气。

今天要介绍的，是一个在 Github 上开源才三周的项目，目前也才寥寥数星。但它以小到仅有30多个250行左右的文件，为一个特定群体 -- 那些有一定交易经验、懂些编程，但并非专业程序员（尽管 AlphaSuite 的作者似乎有较强的人工智能背景），也无法投入大量时间去构建复杂系统的人 -- 提供了一个很有参考价值的轮子范本。

更为重要的是，作者似乎颇有专业知识，他还带来了构建风险预警和 CANSLIM 分析策略模型的提示词。

## 1. AlphaSuite的由来

这个库展示了如何围绕自己的投资理念，快速搭建一个“小而能用”的个人投研体系。根据作者的自述，他自己做了若干个基于 lightgbm 的策略模型，并且在美国和加拿大市场上都取得了不错的成绩，因此决定把项目开源：

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250916210416.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>回测曲线，由 Richard Shu 提供</span>
</div>

当然大家对看到的任何收益曲线都要谨慎对待哈。并且，作者没没有公布他的模型。在代码中尽管使用了 lightgbm，但是特征工程和最终模型都是没有的。代码中明确给出的策略只有双均线策略和唐安奇通道策略。

## 2. 如何让 LLM 去搜索风险预警？

这个库中的News_Intelligence.py文件值得看下。它定义了几个经典的宏观风险框架，比如“信贷与房地产危机”、“通胀与联储政策冲击”、“地缘政治与供应链中断”以及“科技行业健康与集中度风险”。在每一个框架中，作者都定义了相应的提示词。这部分的功能还没来得及实现，不过，它使用的提示词可以参考。这里摘录一小段：

```md
Focus on signs of stress in credit markets and real estate. Look for:
- News about rising corporate or consumer loan defaults.
- Failures or significant distress in regional banks, especially related to 
Commercial Real Estate (CRE) loans.
- Reports of falling commercial property values or rising office vacancies.
- Warnings from credit rating agencies about specific sectors or companies.
- A sudden freeze in the high-yield ("junk") bond market.
```

## 3. CANSLIM 模型

这个项目另一个有趣的地方，是它引入了 CANSLIM 投资模型。CANSLIM 是威廉.奥尼尔提出的一套经典成长股投资策略，核心是通过 7 个关键维度筛选具有高增长潜力、能持续跑赢市场的优质股票，本质是 “基本面 + 技术面” 结合的选股框架。

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/CANSLIM.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>CANSLIM 模型</span>
</div>

实现这个分析，它使用了以下提示词：

```md
You are a financial analyst specializing in the CANSLIM investment strategy. 
Analyze the provided data for {ticker}.

**Ticker:** {ticker}
**Company Information:** {company_info}
**Recent News Snippets:** {company_news}
**Overall Market Posture (SPY Trend):** {market_posture}
**Competitive Landscape Summary:**
{industry_analysis_summary}
**CANSLIM Metrics Table:**
{canslim_metrics_md}

**Analysis Task:**
Provide a concise and confident analysis based on the data.

1.  **CANSLIM Summary:** Briefly evaluate the stock against the key CANSLIM 
criteria (Earnings, Financial Strength, Relative Strength, Volume).
2.  **"N" Factor (New Things):** Discuss any new products, management 
changes, or significant news that could act as a catalyst.
3.  **Investment Thesis:** Conclude with a clear Bull vs. Bear thesis, 
considering its position within its industry. What are the primary reasons to
 be bullish or bearish on this stock right now?

Present your analysis in a structured, easy-to-read format.
```

这里只列举了一部分。在文件technical_analysis_tools.py 中，它还有一些关于技术指标分析的提示词：

```md
...

Analyze trends and signals across daily, weekly, and monthly timeframes. 
Identify confirmations and divergences between timeframes.  Note instances
 where timeframes support or contradict each other.

Indicators and Price Action Analysis:

* Price trends, recent swing highs/lows, support/resistance levels, 
breakouts/breakdowns.
* SMA/EMA trends, moving average crossovers (e.g., 50-day crossing above 
200-day), price relative to SMA/EMA.

...
```

仍然只能展示一部分。但这一小段中，最动人的地方是它要求 LLM 进行多周期分析。这就展示了真正的投资技巧。

## 4. 其它值得一提的事

最后，也是我认为该项目对个人开发者最有启发的一点，是它构建系统的方式。它展示了如何用最低的技术门槛，实现一个功能完整的投研工作台。整个项目几乎完全基于 Python 技术栈，尤其是前端的实现。

它没有选择学习曲线陡峭的前端框架，而是全面拥抱了 Streamlit。从 `pages/` 目录下的一个个 Python 文件就可以看出，每一个页面都是一个独立的脚本。这对于那些主要想验证投资逻辑，而非打磨产品细节的个人开发者来说，是一个明智的选择。它让你能将绝大部分精力放在“如何分析”这个核心问题上，而不是耗费在处理前后端分离、API 调试等繁琐的工程事务中。

Streamlit 是一个可以构建 web 界面的 Python 库，在人工智能社区比较流行。比如 HuggingFace 的 Spaces 就是基于 Streamlit 构建的。使用 Streamlit 构建的前端很难强大、酷炫，应该也无法应对强大的流量请求（但我很好奇 HuggingFace 的流量应该不小？），但是，它最大的优点是解决了 Python 程序员如何快速构建 web 应用的问题。

!!! attention
    不过时代不同了。三年前用 Streamlit 还是一个好主意。但是在2025年，即使你不会前端，要做到 Streamlit 的效果，你只要请一个机器人就够了。所以，Python 打全栈这种事，已经没有三年以前那么性感了。

另外，我注意到项目并没有全程使用 LLM 来进行文本分析。它在情感分析上，使用了vaderSentiment库。这个库我们之前介绍过，有点老派，但是它的优点是简单易用，结果的可靠性可能比 LLM还要高，另外使用上是零成本。不过，它的最后一个发布版本是三年之前，而且也不一定有下一个版本了，所以，我也不推荐大家继续使用了。因为摩尔定律正在 AI 领域生效。Tokens 正在快速贬值。

当然，这个库并非完美。我并非是要推荐你使用 AlphaSuite。AlphaSuite 不算是一个技术上尽善尽美的作品。不客气地说，我甚至挑剔它多于欣赏它。新面孔总是需要一些关注 -- 不管黑的还是红的，总之有了流量就不会寂寞，所以，无论是推荐还是挑剔，总归应该是受发明者欢迎的，这才是我敢于持公平之论的原因。

正如统计学家乔治·博克斯（George Box）所说：“所有的模型都是错的，但有些是有用的。” AlphaSuite 不够完善，但仍然是“有用”的模型。它最大的价值，是为那些希望将自己的投资思考代码化的人，提供了一条清晰、可行的技术路径，同时，为如何使用提示词来获得风险报告、投资建议打了样。

构建一个类似的系统，其意义或许不仅仅在于得到最终的分析结果。更重要的是，这个创造的过程本身，会迫使你将自己脑中模糊的、零散的投资理念，梳理成清晰的、有逻辑的规则和框架。当你能将自己的所思所想构建成一个系统时，你才真正地理解了它。

交易真正的精髓恰恰是那些无法从书本中习得的、对市场风险的直觉与敬畏。正是在这“亲手锻造”的过程中，才被深刻地烙印在我们的认知里。
