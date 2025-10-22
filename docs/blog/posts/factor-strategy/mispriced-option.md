
---
title: 不写一行代码，我只靠 AI 实现期权定价策略
date: 2025-10-17
img: https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/landscape/bakery/17.jpg
excerpt: 这篇文章介绍了使用 AI 发现错误期权定价的方法，以及如何交易它。这篇文章昨天刚刚发布，就得到超过1.1k 个赞。非常值得一读。核心不是策略本身，而是如何使用 AI，让本来复杂的期权交易变得更容易参与。
category: strategy
tags: [Future,Options,AI,Trading]
---

这篇文章介绍了**使用 AI 发现错误期权定价**的方法，以及如何交易它。这篇文章昨天刚刚发布，就得到超过1.1k 个赞。非常值得一读。核心不是策略本身，而是如何使用 AI，让本来复杂的期权交易变得更容易参与。注意看截图中的提示词。翻译它们并不困难。

!!! attention
    这篇文章翻译至 PandaMcGee3 的一篇博文。你可以在 [PandaMcGee3](https://www.reddit.com/r/options/comments/1o7prtk/my_method_on_making_money_trading_mispriced/)这里找到原文及联系原作者。

    转载不意味着我们赞同本文观点。本文一切权利归原作者所有。下文中的第一人称都为原作者本人。

我做期权交易大概有三年了。基本上那段时间，我基本上就是在赌博。因为在 Reddit 或 Twitter 上看到一些好东西，就买便宜的看涨期权，然后祈祷能有 10 倍的回报。亏了钱，赚回来，又亏了。散户交易员的惯常做法。

大约六个月前，我厌倦了这种猜测的流程，决定真正学习期权定价背后的数学原理。慢慢地，我开始构建自己的策略，在**人工智能**的帮助下，我可以自信地说，现在我的盈利能力相当不错。更重要的是，我终于觉得自己对期权市场有了相当深入的了解。

这是我在开始期权交易之旅时希望看到的一篇文章，它主要涵盖了我目前使用的策略，也涵盖了一些更基本的概念。如果您经验更丰富，可以跳过部分内容。

## 什么是波动率偏差（以及它为何存在）

把期权定价想象成拉斯维加斯设定 NBA 总决赛赔率。博彩公司首先会根据专家预测，然后随着赛季进展和投注额的增加调整赔率。期权的运作方式大致类似：做市商以 Black-Scholes 模型作为基准，然后价格根据市场实际情况调整。

关键在于： **布莱克-斯科尔斯假设隐含波动率在所有执行价格下都应该保持不变**。理论上，远期价外看涨期权和 ATM 看涨期权应该具有相同的隐含波动率，因为它们投资的是同一只股票。

**但现实并非如此**。价外期权的隐含波动率 (IV) 始终高于自动提款期权。绘制这条曲线，你就能得到波动率偏差。我知道你在想什么，但这不是很正常吗？毕竟，赔率应该会随着赛季的进行而变化，不是吗？你说得对，这完全是正常的市场行为。

**当恐惧或贪婪将这种倾向推向极端时，我们的机会就来了**。当做市商因为大家恐慌性买入看跌期权或因害怕错过而买入看涨期权而抬高价位时，你就会看到异常显著的偏度（abnormally rich skew）。这正是我们正在寻找的。

![SPY 的实际波动率偏差与 Black-Scholes 相比，你可以看到远期 OTM 期权的价格比理论预测的要高得多](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017153712.png)


## 如何找到具有显著 skew 的期权？

并非所有 skew 都生来平等，正如我之前提到的，大多数 skew 都是完全正常的，而且通常价格合理。关键在于拥有一个系统/标准，能够帮助你更一致地识别更显著/异常的偏度。

!!! attention
    在开始提示 AI 之前，你需要确保它拥有真实的最新市场信息。 为此，你可以使用像 Xynth 这样的内置市场数据的 AI，或者从 TradingView 或 Polygon 下载数据，然后将 CSV 文件上传到 ChatGPT 或 Claude，两种方法都可以。


### Skew Z-Score Below -2.0

这会将当前偏度与股票的历史平均值进行比较。z 值 -2.0 表示偏度比正常值高出 2 个标准差，这在统计上很罕见，并且更有可能出现逆转。简而言之：与历史平均值相比，当前连锁店的当前定价损失了多少？

![提示词](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155026.png)



![图表报告](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155826.png)


![详细分析](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155934.png)

### IV/RV Mismatch

比较当前的 IV 与 RV、已实现的波动率，即市场认为股票将要表现的走势与股票最近的表现：

1. 价外执行价（OTM Strikes）：隐含波动率 (IV) 应显著高于实际波动率 → 定价过高
2. ATM 执行价(atm strikes)： IV 应等于或低于实际波动率 → 合理定价
   
当两种情况都发生时，你就会面临一个昂贵的选择和一个便宜的选择。这就是你的价差。

![提示词](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160140.png)

![图表报告](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160215.png)


![详细分析](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160719.png)

### 动量确认

这会告诉您交易的方向：
1. 正动量 + 看涨期权倾斜 → 买入看涨期权价差（买入 ATM 看涨期权，卖出 OTM 看涨期权）
2. 负动量+看跌期权倾斜 →买入看跌期权价差（买入 ATM 看跌期权，卖出 OTM 看跌期权）

![提示词](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160831.png)
![图表报告](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160917.png)
![详细分析](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160943.png)

## 交易：垂直价差

一旦你找到了显著偏度，这就是你想要设置的方式，我主要只做牛市价差，因为我不喜欢做空，但假设你也可以尝试相反的做法：

1. 购买 ATM 期权（价格合理，~50 delta）
2. 卖出 OTM 期权（定价过高，~10-25 delta）

![交易提示词](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161137.png)

![回测](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161210.png)

![详细分析](https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161335.png)

!!! attention
    这些图片是我在 Xynth 聊天中看到的示例。在这笔交易中，评分只有 68/100，主要是因为 ATM 期权的价格已经过高，所以价差并没有给我们带来太多的盈利潜力。不过，概念保持不变。您可以随意调整提示中的变量，并扩大扫描范围，每天甚至每小时对更多股票运行此扫描器。


## 为什么要采用垂直价差？

如果您已经读到这里，那么您可能已经意识到，这种策略的重点并不是纯粹的方向性，而是一种相对价值的发挥，这是一种奇特的说法， 即您同时买入便宜的东西并卖出昂贵的东西。

你不仅仅是在押注股票价格上涨或下跌，你还在押注两种期权之间的定价关系会失衡，并且最终会恢复正常。

此外，如果股票价格出现剧烈波动，您的多头期权也能为您提供保障。您无需承受任何一方的无限风险。

## 结果

我已经运行这个策略大约 2 个月了，所以对这些数字持保留态度，现在还为时过早。

当前统计数据：
1. Win rate: ~38%
2. Average return per winning trade: ~250%
3. Average loss per losing trade: ~60%
4. 净值：尽管亏损比盈利多，但总体仍上涨

这种策略的本质是不对称的。我有一些交易在几周内获得了300-400%的回报，也有一些交易同样迅速地亏损了50-70%。但如果10笔交易中能赢4笔，获得3-4倍的回报，就能轻松弥补6笔亏损。

<hr>

关于偏度（skew） 等更多量化交易概念，在量化24课中有系统讲解。


