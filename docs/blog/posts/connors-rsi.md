---
title:  Connor's RSI 我愿称之为年度最强指标
date: 2023-12-22
slug: connor-rsi-the-best
categories:
    - strategy
tags:
    - strategy
    - 技术指标
---

人们发明了各种技术指标。这些技术指标中，以价格因子居多，比如均线、ATR、MACD， RSI, JDK等。由于拥挤效应的存在，多数因子的有效性也越来越弱，或者说，它们的使用范围也越来越局限。

但有一个因子，是基于著名的RSI的改进版。如果说在多因子时代，我们可以仅凭一个因子就构建出策略，并且还很有可能跑赢市场的话，它是不二之选。

<!--more-->


这个因子就是Connor's RSI。它被Nirvana Systems称作终极技术指标。我深深地赞同这一点。Nirvana Systems在它的网站上发布了关于如何生成和使用这一指标的文章。著名的回测框架 backtrader及和策略平台TradingView都内置了这一指标。

为什么Conners RSI被称为终极技术指标，它有哪些优势？成功背后的原理是什么，又该如何实现这一指标呢？

## 如何构建Connor's RSI

Conners RSI是在标准RSI的基础上，混合了另外两个指标得到的。

第一个指标就是Streaks。它是统计连续上涨或者下跌的周期数，将上涨与下跌的周期数之比来求得的RSI。下面的代码演示了如何计算Streaks指标：

```python
# 本段代码使用了较强的numpy技巧，建议反复研读
def streaks(close):
    result = []
    conds = [close[1:]>close[:-1], close[1:]<close[:-1]]

    flags = np.select(conds, [1,-1], 0)

    # find_runs函数来自大富翁量化框架。它的作用是划分数组中
    # 连续出现的相同值。是量化中非常基础的一个函数。
    v, _, l = find_runs(flags)
    for i in range(len(v)):
        if v[i] == 0:
            result.extend([0] * l[i])
        else:
            result.extend([v[i] * x for x in range(1, (l[i] + 1))])
            
    return np.insert(result, 0, 0)
```

下图显示了每日收盘价，及由此计算的streaks指标:

![](https://images.jieyu.ai/images/2023/12/how-to-calc-streak.png)

第二个指标就是当日的涨跌幅，在过去一段时间内的的涨跌幅中的排名。percent_rank是一个常用的统计函数，在pandas中就有实现。这里我们给出它的numpy实现：

```python
def percent_rank(close):
    roc = close[1:]/close[:-1] - 1
    return np.array([sum(roc[i + 1 - self.prank:i + 1] < roc[i]) / self.prank for i in range(len(roc))]) * 100
```

这两个指标加上经典RSI，就合成了Conners RSI:

$$
CRSI = [RSI(6) + RSI(Streak, 2) + PercentRank(20)] / 3
$$

## 为什么Connor's RSI应该更有效？

我们先看Streak指标。经典的RSI是关于累积上涨幅度与累积波动幅度（绝对值）的一个分数，是定量的分析。Streak则把上涨与下跌进行了二值化，它相当于是相当于是定性的分析。增加这样一个指标，意义何在呢？

![R50](https://images.jieyu.ai/images/2023/12/galton_box.png)

我们知道，从概率上讲，股票连涨周期数越长，则越可能反生反转（即下跌）；反之亦然。大家可以按照我们在《数据分析与Python实现》那几节课中，介绍的PDF/CDF的方法，来自行估计当某个标的连续上涨N天后，接下来继续上涨的概率有多大。

提示：你也可以把这个问题当成一个正态分布来直接求一个理论上的解答。对一个二值分布的多次实验，它们的累积分布正好是一个正态分布。关于这一点，可以参看[Galton Board](https://en.wikipedia.org/wiki/Galton_board)。

所以，Streak是从另一个角度，但仍然是用概率分析的方法，来捕捉经典RSI所不能捕捉的一些 conner case!

同样地，PercentRank从另一个维度，描绘了当前市场的强弱。如果在过去20天内，只有3天的涨幅低于今天，那么今天的相对强弱就是15%，次日反转可能性大；如果17天的涨幅低于今天，那么今天的相对强弱就是85%，次日下跌的可能性变大。

如果你对K线和波浪理论比较熟悉，你会发现，大涨意味着行情加速赶顶；大跌则是行情加速赶底。而PercentRank则是对这个过程的简单、但有一定准确度的刻画！

!!! tip
    Nirvana Systems开发并发布了这个指标，但Nirvana Systems并没有像我们这样，深入解析它背后的原理。实际上，它既有概率论的理论支撑，也能用行为金融学的原理进行解释。

## 实战中的 Connor's RSI

![L33](https://images.jieyu.ai/images/2023/08/corners_rsi.png)

我们先是用最近1000天的沪指，使用backtrader进行了测试。回测表明，最近4年以来（近似于1000个交易日），沪指仅上涨5.76%，但通过cornner's RSI策略抄底逃顶，我们在指数上竟然获得超过44%的收益。如果是对个股进行操作，收益很可能是数倍。

由于这段时间毕竟沪指是上涨的。如果我们随机盲选，选中了极端不好的行情，Connor's RSI又将表现如何？近两年来恒生指数就宛如下跌的飞刀，没有比这更好的例子了：

![](https://images.jieyu.ai/images/2023/08/crsi_hk_2021.png)
<caption>图片来源: www.taindicators.com</caption>

当然，我们最好不要接下跌中的飞刀。但从他人的回测来看，Connor's RSI还是能抓住其中的一些反弹，而躲过一些下跌，总体上看，要比指数强不少。

我们使用大富翁量化框架随机选择了一些个股进行回测：

![](https://images.jieyu.ai/images/2023/12/connor-rsi-hnpc.png)

这支个股近一年来一直在横盘。buy-and-hold策略表明其收益仅为2.26%，但使用Connor's RSI，收益达到12.14%，胜率则是100%。

我们从2019年1月25日到2023年11月14日期间进行回测。区间内个股全程横盘，但Connor's RSI获得了157.92%的利润率，胜率也达到80.77%，可谓出手便有。另外，它仅仅交易26次，还有相当多的时间是空仓，所以，这段时间的资金还可以分配到其它标的上，从而有可能达到更好的收益。

## 关于Connor's RSI的更深入思考

Connor's RSI是一个天才的发现，充分反映了概率论和行为金融学的一些原理。但由于技术实现上的不足，它的潜力还没有完全释放。

Connor's RSI将三个维度的数据，进行了等权重的平均。在传统的多因子分析方法中，线性回归是运用的最多的技术，Connor's RSI本质上是一种线性回归。这也是传统金融佛界所熟悉的方法。

它被提出来的时候，机器学习方法还没有被金融界所了解和采用。今天，很可能大多数人都了解到，Connor's RSI实际上是一个三因子组合，我们可以通过机器学习，来刻画三个因子之间相互作用、相互弥补的复杂关系。

其次，Nirvana Systems对RSI的拓展，也反映了我们应该如何对待经典技术指标。有一些经典的指标，我们不应该简单地认为它行或者不行（作者也曾经陷入过这个误区），而是应该以扬弃的态度来对待它们，深入分它们是如何起作用的，如何用新的技术来改进它们，或者看看，新的技术条件下，是否为运用这一指标提供了新的可能。毕竟，任何新的发现，终究只是对经典的致敬！

当你进入到这一层次，才算是真正有了独立思考能力，才能真正算是独当一面的量化人。

!!! quote
    老兵不死，他们只是凋零。

![](https://images.jieyu.ai/images/2023/07/welles_wilder.png)
<div style="text-align:right">-- 致敬 WELLES WILDER和他的RSI！</div>
