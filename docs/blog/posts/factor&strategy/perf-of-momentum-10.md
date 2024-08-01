---
title: 7月：斜率动量因子表现回顾
slug: perf-of-momentum-10
date: 2024-08-02
category: factors
motto: Learning how to fall teaches you how to land, and learning to land gives you the courage to jump higher
img: https://m.media-amazon.com/images/I/61YULEKe2uL._SL1360_.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - 因子策略
    - momentum
    - 因子评估
---


<!--这一轮牛市持续了86400秒！文明再次进入了休眠状态-->

斜率因子是动量因子中的一种，它由Andreas F. Clenow 首先发表在[Stocks on the Move: Beating the Market with Hedge Fund Momentum Strategy](https://www.amazon.com/Stocks-Move-Beating-Momentum-Strategies/dp/1511466146)一书中。

这个因子比起卡哈特的动量因子更符合人的直觉，特别是喜欢看K线的投资者，因此也得到了很多人的喜爱。其实现在Quantopian和[QuantConnect](https://www.quantconnect.com/forum/discussion/3136/andreas-f-clenow-momentum/p1)网站上都有文章讨论。

<claimer>题图：Andreas Clenow的著作： Stock on the Move 封面</claimer>


---

!!! tip
    我们简单回顾一下Mark Carhart提出的动量因子，它是计算单个股票过去一年的回报率，排除最近一个月数据（以防股价操纵），再按回报率排序，取前10%的股票作为买入信号，末尾10%的股票作为卖出信号。

在Andreas Clenow的策略中，他使用了过去90天的年化指数的回归斜率作为动量因子。由于信号只响应过去90天的数据，因此，信号就比卡哈特的动量因子更灵敏一些。

不过，我们今天测试的因子，是用过去10天的回归斜率作为动量因子。主要目标是尝试下新的可能性，也是考虑到在A股，动量因子的半衰期一般比较短的缘故。

我们的计算方法如以下代码所示：

```python
def moving_slope(close: NDArray, win:int, *args):
    # 创建滑动窗口的视图
    shape = (win, close.size - win + 1)
    strides = (close.itemsize, close.itemsize)
    cw = np.lib.stride_tricks.as_strided(close, 
                                         shape=shape, 
                                         strides=strides)
    
    # 对每个窗口应用linregress，获取斜率
    x = np.arrange(win)
    slopes = np.apply_along_axis(lambda y: linregress(x, y)[0],
                                  axis=0, arr=cw)
    
    return slopes

```


<!--

Momentum因子，即动量因子，是在金融领域中用来衡量证券价格趋势持续性的因素。它最早是由纳拉辛汉·贾格迪什（Narasimhan Jegadeesh）和谢尔登·科汉（Sheldon Grossman）以及后来的马克·卡哈特（Mark Carhart）在其学术研究中提出的。

纳拉辛汉·贾格迪什和谢尔登·科汉在1993年的论文《The Profitability of Trading on Observed Returns》中首次提供了关于动量策略有效性的实证证据。他们发现，过去表现好的股票在未来一段时间内倾向于继续表现出色，而过去表现差的股票则倾向于继续表现不佳。

随后，马克·卡哈特在1997年的论文《On Persistence in Mutual Fund Performance》中进一步研究了动量因子，并将其纳入了他提出的四因子模型中，该模型除了市场因子、规模因子（SMB）、价值因子（HML）之外，还加入了动量因子（MOM）。

因此，虽然动量效应的概念在贾格迪什和科汉的研究中被首次提出，但卡哈特的工作使其在投资界得到了更广泛的认可，并将其正式化为一个独立的风险因子。


卡哈特的动量因子（PR1YR）是通过以下步骤计算的：

计算单个股票的过去一年回报率：排除最近一个月的数据，计算过去11个月的累计回报率。

形成赢家和输家组合：将所有股票按其过去一年的回报率排序，分别形成赢家组合（最高回报率的股票）和输家组合（最低回报率的股票）。

构建动量因子：动量因子是赢家组合和输家组合的平均回报率之差。也就是说，卡哈特构建的动量因子是通过买入过去表现最好的股票（赢家组合）并卖空过去表现最差的股票（输家组合）来实现的。
-->


测试参数如下：随机抽取2000支，从今年的1月4日，测试到7月31日，计算斜率时，使用过去10天的收盘价；计算收益时，使用开盘价，从次日起。

---

因子分层如下：

![](https://images.jieyu.ai/images/2024/08/slope-factor-quantile.jpg)



分层收益均值图如下：

![](https://images.jieyu.ai/images/2024/08/slope-mpwr.jpg)


显然，10期的斜率因子成了反向指标，也就是短期上涨越快，买入后亏损越多。

---

既然如此，我们就取斜率因子的负数作为新的因子，再运行一次：


![](https://images.jieyu.ai/images/2024/08/slope-mpwr-2.jpg)

理所当然，这个图只是前面的图的镜像。我们来看看收益：

![](https://images.jieyu.ai/images/2024/08/slope-cum-returns-1.jpg)


7个月的累积收益接近15%了，最大回撤5%左右，在今年来看，表现还可以。

!!! tip
    上一篇RSI的因子测试中，我们也对因子构成做了一些微调。有同学认为，微调之后，数据变好，这是过拟合了。今天写这个因子时，想起来在Alpha101中，他们抛弃掉了动量最大前n%的因子，这也是一种修正。警惕过拟合是对的，但不是数据一变好就是过拟合。

---

再深入到分层累积收益：

![](https://images.jieyu.ai/images/2024/08/slope-cum-return-by-quantile.jpg)

可以看出，因子的稳定性比较好，期间没有发生明显的风格转换的情况。

当然这个因子要投入实战的话，可能不适合个人和中小机构。因为从分层图来看，它的收益主要是由做空产生的。


如果我们没有机会做空，因子的表现又将如何？下图是纯多情况下的收益：

![](https://images.jieyu.ai/images/2024/08/slope-cum-returns-long-only.jpg)

这个表现并不出人意料。在2月有一个强反弹，在此期间，因子的表现不错。但随后市场越走越弱，动量因子的半衰期越来越短，单多收益就一路走低。

---

![L50](https://m.media-amazon.com/images/I/61YULEKe2uL._SL1360_.jpg)

前天，七八月之交，A股出现一轮牛市，跨越两个月，长达86400秒。随后再次进入休眠状态。这个现象，也许不能用今天的介绍的动量因子来预测，但动量因子表现如此之弱，却能在一定程度上，说明为什么连续上涨未能出现。

另一个结论，正是因为做空的收益比较确定，所以易跌难涨。方主席下岗了，看看后面做空机制上能否有所变化。毕竟，能做空的机构也只是少数。制度应该对所有参与者都公平。

左图是Andreas Clenow的著作，Stocks on the Move: Beating the Market with Hedge Fund Momentum Strategy。Andreas Clenow是一位瑞典裔瑞士籍作家、资产管理人及企业家，现居于苏黎世，在一家家族办公室担任首席投资官。在其辉煌的职业生涯中，他曾是一名科技创业者、金融顾问、对冲基金经理、金融工程师、量化交易员、财务顾问、董事会成员，以及企业中层管理官僚。

在这本书中，Clenow详细解释了动量策略的原理，即买入过去表现优秀的股票，卖出或做空表现不佳的股票，利用市场趋势的持续性来获利。书中对比了技术分析和基本面分析在动量策略中的应用，以及如何结合两者的优势来提高交易效果。
