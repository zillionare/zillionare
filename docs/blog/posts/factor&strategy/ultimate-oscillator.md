---
title: "一门三杰 一年翻十倍的男人发明了 UO 指标"
date: 2024-10-29
category: factor&strategy
slug: ultimate-oscillator
motto: 
img: https://images.jieyu.ai/images/2024/10/larry-willimans-card.jpg
stamp_width: 60%
stamp_height: 60%
tags: [factor,indicators,alpha]
---

![Larry Williams，1987 年世界期货交易大赛冠军](https://images.jieyu.ai/images/2024/10/larry-willimans-card.jpg)

指标 Ultimate Oscillator（终极振荡器）是由 Larry Williams 在 1976 年发表的技术分析因子。

Larry 是个牛人，不打嘴炮的那种。他发明了 William's R（即 WR）和 ultimate ocsillator 这样两个指标。著有《我如何在去年的期货交易中赢得百万美元》一书。他还是 1987 年世界期货交易大赛的冠军。在这场比赛中，他以 11.37 倍回报获得冠军。

更牛的是，在交易上，他们家可谓是一门三杰。

![](https://images.jieyu.ai/images/2024/10/michell-williams.jpg)

这是他女儿，michelle williams。她是知名女演员，出演过《断臂山》等名片，前后拿了 4 个奥斯卡最佳女配提名。更厉害的是，她在 1997 年也获得了世界期货交易大赛的冠军，同样斩获了 10 倍收益。在这个大赛的历史上，有这样收益的，总共只有三人，他们家占了俩。

这件事说明，老 williams 的一些交易技巧，历经 10 年仍然非常有效。

![](https://images.jieyu.ai/images/2024/10/worldcupchanpion-michelle-larry.jpg)

Larry Williams 的儿子是位心理医生，著有《交易中的心理优势》一书。近水楼台先得月，身边有两位世界冠军，确实不愁写作素材。

这是指标的计算公式。

$$
\text{True Low} = \min(\text{Low}, \text{Previous Close}) \\
\text{True High} = \max(\text{High}, \text{Previous Close}) \\
\text{BP} = \text{Close} - \text{True Low} \\
\text{True Range} = \text{True High} - \text{True Low} \\
\text{Average BP}_n = \frac{\sum_{i=1}^{n} BP_i}{\sum_{i=1}^nTR_i} \\
ULTOSC_t=\frac{4Avg_t(7) + 2Avg_t(14) + Avg_t(28)}{4+2+1} \times 100
$$


它旨在通过结合不同时间周期的买入压力来减少虚假信号，从而提供更可靠的超买和超卖信号。Ultimate Oscillator 考虑了三个不同的时间周期，通常为 7 天、14 天和 28 天，以捕捉短期、中期和长期的市场动量。

这个公式计算步骤比较多，主要有 true low, true high 和 true ange, bull power 等概念。

用这个图来解释会更清楚。

![](https://images.jieyu.ai/images/2024/10/ultimate-oscillator.jpg)

所谓的 true range，就是把前收也考虑进行，与当天的最高价、最低价一起，来求一个最大振幅。然后计算从 true low 到现价的一个涨幅，作为看涨力道（Bull Power）。

最后，用**看涨力道**除以**真实波幅**，再在一定窗口期内做平均，这样就得到了归一化的看涨力道均值。

最后，它结合长中短三个周期平均，生成最终的指标。

从构造方法来讲，它与 RSI 最重要的区别是，加入了 high 和 low 两个序列的数据。

做过交易的人知道，关键时刻最高价和最低价，都是多空博弈出来的，它是隐含了重要信息的。如果实时盯过盘口的人，可能感受更深。

像最高点，它是主力一口气向上吃掉多少筹码才拿到的这个最高点。**上面的筹码吃不掉，最高价就定在这个地方。吃不掉的筹码是更大的资金的成本或者其它什么心理价位，就是未来的压力位**。

因此，ultimate oscillator 与 RSI 相比，是包含了更多的信息量的。希望这部分解读，能对大家今后探索因子起到一定的启迪作用。

这个图演示了实际中的 uo 指标，看起来是什么样的。从视觉上看起来，它跟 RSI 差不多，都是在一定区间震荡的。

![](https://images.jieyu.ai/images/2024/10/ultimate-oscillator-visualize.jpg)


这个因子在回测中的表现如何？在回测中，从 2018 年到 2023 年的 6 年中，它的 alpha 年化达到了 13.7%，表现还是很优秀的。

![](https://images.jieyu.ai/images/2024/10/uo-alpha.jpg)

不过因子收益主要由做空贡献。大家看这张分层收益图，收益主要由第 1 层做空时贡献。在纯多的情况下，alpha 并不高，只有 1.6%，收益主要由 beta 贡献，所以组合收益的波动比较大。

![](https://images.jieyu.ai/images/2024/10/uo-quantile-returns.jpg)

所以，这个指标在期货上会更好使。

在多空组合下，6 年的收益达到了 2.2 倍。

![](https://images.jieyu.ai/images/2024/10/uo-cumulative-returns.jpg)

最后我们看一下因子密度分布图。看上去很符合正态分布，尽显对称之美。

![](https://images.jieyu.ai/images/2024/10/uo-factor-distplot.jpg)

从分层均值收益图来看，我们在交易中还可以做一点小小的优化，就是淘汰第8层之上的因子。这样调优之后，在2018年到2022年间，年化Alpha达到了24%，5年累计收益达到了2.75倍。

我们保留了2023年的数据作为带外数据供测试。在这一年的回测中，年化Alpha达到了13%，表明并没有出现过拟合。2023年的累计收益曲线如下：

![](https://images.jieyu.ai/images/2024/10/ultimate-oscillator-2023-cum-returns.jpg)


同期沪指是以下跌为主。8月底开启的上涨，在时间上与DMA策略上涨巧合了。

![](https://images.jieyu.ai/images/2024/10/sh-2023-plot.jpg)

完整测试代码加入星球后即可获取。

![](https://images.jieyu.ai/images/hot/logo/zsxq.png)
