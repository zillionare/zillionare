---
title: "年终特稿：这个指标我愿称之为年度最强发现"
date: 2023-12-29
lunar: 冬月十七
motto: Fate wishpers to the warrrior, you can't withstand the storm. The warrrior whispers back, I am the storm!
slug: connor-rsi-the-best
category: strategy
tags:
    - strategy
    - 技术指标
---

如果说在多因子时代，我们可以仅凭一个因子就构建出策略，并且还很有可能跑赢市场的话，这个因子就是不二之选。

<!--more-->

这个因子就是 Connor's RSI。它被 Nirvana Systems 称作终极技术指标。我深深地赞同这一点。Nirvana Systems 在它的网站上发布了关于如何生成和使用这一指标的文章。著名的回测框架 backtrader 及和策略平台 TradingView 都内置了这一指标。

!!! tip 墙裂推荐！
    本文最初发表于某乎，一周内收获超 800 次赞藏。我们特别将其选录为小红书年度收官之作，内容丰富，建议赞藏以备今后阅读。

---

为什么 Conners RSI 被称为终极技术指标，它有哪些优势？成功背后的原理是什么，又该如何实现这一指标呢？

## 如何构建 Connor's RSI

Conners RSI 是在标准 RSI 的基础上，混合了另外两个指标得到的。

第一个指标就是 Streaks。它是统计连续上涨或者下跌的周期数，将上涨与下跌的周期数之比来求得的 RSI。下面的代码演示了如何计算 Streaks 指标：

```python
# 本段代码使用了较强的 NUMPY 技巧，建议反复研读
def streaks(close):
    result = []
    conds = [close[1:]>close[:-1], close[1:]<close[:-1]]

    flags = np.select(conds, [1,-1], 0)

    # FIND_RUNS 函数来自大富翁量化框架。它的作用是划分数组中
    # 连续出现的相同值。是量化中非常基础的一个函数。
    v, _, l = find_runs(flags)
    for i in range(len(v)):
        if v[i] == 0:
            result.extend([0] * l[i])
        else:
            result.extend([v[i] * x for x in range(1, (l[i] + 1))])
            
    return np.insert(result, 0, 0)
```
---

下图显示了每日收盘价，及由此计算的 streaks 指标：

![50%](https://images.jieyu.ai/images/2023/12/how-to-calc-streak.png)

第二个指标就是当日的涨跌幅，在过去一段时间内的的涨跌幅中的排名。percent_rank 是一个常用的统计函数，在 pandas 中就有实现。这里我们给出它的 numpy 实现：

```python
def percent_rank(close):
    roc = close[1:]/close[:-1] - 1
    return np.array([sum(roc[i + 1 - self.prank:i + 1] < roc[i]) / self.prank for i in range(len(roc))]) * 100
```

这两个指标加上经典 RSI，就合成了 Conners RSI:

$$
CRSI = [RSI(6) + RSI(Streak, 2) + PercentRank(20)] / 3
$$


## 为什么 Connor's RSI 应该更有效？

我们先看 Streak 指标。经典的 RSI 是关于累积上涨幅度与累积波动幅度（绝对值）的一个分数，是定量的分析。Streak 则把上涨与下跌进行了二值化，它相当于是定性的分析。增加这样一个指标，意义何在呢？

---

![R50](https://images.jieyu.ai/images/2023/12/galton_box.png)

我们知道，从概率上讲，股票连涨周期数越长，则越可能反生反转（即下跌）；反之亦然。大家可以按照我们在《数据分析与 Python 实现》那几节课中，介绍的 PDF/CDF 的方法，来自行估计当某个标的连续上涨 N 天后，接下来继续上涨的概率有多大。

提示：你也可以把这个问题当成一个正态分布来直接求一个理论上的解答。对一个二值分布的多次实验，它们的累积分布正好是一个正态分布。关于这一点，可以参看 [Galton Board](https://en.wikipedia.org/wiki/Galton_board)。

所以，Streak 是从另一个角度，但仍然是用概率分析的方法，来捕捉经典 RSI 所不能捕捉的一些 conner case!

同样地，PercentRank 从另一个维度，描绘了当前市场的强弱。如果在过去 20 天内，只有 3 天的涨幅低于今天，那么今天的相对强弱就是 15%，次日上涨的可能性大；如果 17 天的涨幅低于今天，那么今天的相对强弱就是 85%，次日下跌的可能性变大。

如果你对 K 线和波浪理论比较熟悉，你会发现，大涨意味着行情加速赶顶；大跌则是行情加速赶底，后面趋势逆转是大概率事件。而 PercentRank 则是对这个过程最简单、但仍有一定准确度的刻画！

---

!!! tip
    Nirvana Systems 开发了这个指标，但 Nirvana Systems 并没有像我们这样，深入解析它背后的原理。实际上，它既有概率论的理论支撑，也能用行为金融学的原理进行解释。

## 实战中的 Connor's RSI

![L33](https://images.jieyu.ai/images/2023/08/corners_rsi.png)

我们先是用最近 1000 天的沪指，使用 backtrader 进行了测试。回测表明，最近 4 年以来（近似于 1000 个交易日），沪指仅上涨 5.76%，但通过 cornner's RSI 策略抄底逃顶，我们在指数上竟然获得超过 44%的收益。如果是对个股进行操作，收益很可能是数倍。

这段时间沪指是上涨的，你可能怀疑，也许Cornnor's RSI的成功只是偶然。

如果我们随机盲选，选中了极端不好的行情，Connor's RSI 又将表现如何？

近两年来恒生指数就宛如下跌的飞刀，没有比这更好的例子了：

---

![](https://images.jieyu.ai/images/2023/08/crsi_hk_2021.png)
<cap>图片来源：www.taindicators.com</cap>

当然，我们最好不要去接下跌中的飞刀。但从他人的回测来看，Connor's RSI 还是能抓住其中的一些反弹，而躲过一些下跌，总体上看，要比指数强不少。

我们使用自己的量化框架随机选择了一些个股进行回测：

---

![](https://images.jieyu.ai/images/2023/12/connor-rsi-hnpc.png)


这支个股近一年来一直在横盘。buy-and-hold 策略表明其收益仅为 2.26%，但使用 Connor's RSI，收益达到 12.14%，胜率则是 100%。

我们从 2019 年 1 月 25 日到 2023 年 11 月 14 日期间进行回测。区间内个股全程横盘，但 Connor's RSI 获得了 157.92%的利润率，胜率也达到 80.77%，可谓出手便有。另外，它仅仅交易 26 次，还有相当多的时间是空仓，所以，这段时间的资金还可以分配到其它标的上，从而有可能达到更好的收益。

<claimer>数据基于历史，仅为演示指标用法，请勿据此操作</claimer>

## 关于 Connor's RSI 的更深入思考

Connor's RSI 是一个天才的发现，充分反映了概率论和行为金融学的一些原理。但由于技术实现上的限制，它的潜力没有完全释放。
wg

Connor's RSI 将三个维度的数据，进行了等权重的平均。在传统的多因子分析方法中，线性回归是运用的最多的技术，Connor's RSI 本质上是一种线性回归。这也是传统金融界所熟悉的方法。

---

在当年，机器学习方法还没有被金融界所了解。但今天，可能很多人都意识到，Connor's RSI 实际上是一个三因子组合，可以通过机器学习，来刻画三个因子之间相互作用、相互弥补的复杂关系。

Nirvana Systems 对 RSI 的拓展，也反映了我们应该如何对待经典的技术指标。有一些经典的指标，我们不应该简单地认为它们好或者不好（作者也曾经陷入过这个误区），而是应该以扬弃的态度，深入分析其作用机制，以检验其在新的技术条件下，是否能焕发新的生机。毕竟，**任何新的发现，终究只是对经典的致敬**！

只有当你进入到这一层次，才算是**真正有了独立思考能力，才能真正算是独当一面的量化人**。

!!! quote
    老兵不死，他们只是凋零。致敬 WELLES WILDER 和他的 RSI！

![75%](https://images.jieyu.ai/images/2023/07/welles_wilder.png)
