---
title: 圣杯依然闪耀
slug: the-holy-grail-still-works
date: 2024-07-22
category: factors
motto: 一念天堂 一念地狱 so choose wisely
img: https://images.jieyu.ai/images/2024/07/Indiana-Jones-and-the-Last-Crusade.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - 策略
---

圣杯依然闪耀 RSI 永远是我最爱的指标 -- 因为潮汐和回归是这个蓝色星球的生命年轮，这样的轮回也存在于交易世界。而 RSI 就是刻画市场中的潮汐和回归的最好指标之一。

年初我介绍过 Connor's RSI。这次我们将探索 Connors 提出的一个基于短时 RSI 的均值回归策略，重点是介绍策略优化应该从哪些方面入手。

<claimer>策略实验及评测数据来自于Quantitativo 网。</claimer>

---

## 策略概要

所有人应该都已经熟悉 RSI 指标了。我们常用的 RSI 指标是基于 6,12 和 24 周期计算出来的。

$$
RS = \frac{\text{SMMA}(U,n)}{\text{SMMA}(D,n)}
$$

$$
RSI = 100\cdot\frac{\text{SMMA}(U,n)}{\text{SMMA}(U,n) + \text{SMMA}(D,n)} = 100 - { 100 \over {1 + RS} }
$$

但是 Larry Connors 认为，2 周期的 RSI 可以更好的反映市场趋势，很可能是技术指标中的圣杯。他把这个观点发表在 2008 年出版的《华尔街的顶级交易员》一书中。在此后的 Connor's RSI 指标中，streak 的 RSI 正是使用 2 周期来计算的。

基于这样的 RSI,Connors 给出了以下均值回归策略：

1. 标普 500 指数超过 200 日均线；
2. 标普 500 指数的 2 周期 RSI 低于 5；
3. 信号发出时，按收盘价买入；
4. 当标普 500 高于 5 日均线时卖出。

用交易员的话来讲，这是一个在**牛市**（指数大于 200 日均线）**短线回调**（RSI 低于 5）时的买入策略。

---

## 因子检验

首先 quantitativo 进行了单因子检验。检验方法是对对所有 2 天 RSI 收于 5 以下的标的进行买入并持有 5 天，再计算收益。

![](https://images.jieyu.ai/images/2024/07/factor-rsi-2-buy-and-hold-5.jpg)

这个统计包含了超过 21000 个标的，超过 250 万次事件（标普 500 收于 200 天均线之上）。测试中的亮点：

1. 当任何给定股票的 2 天 RSI 低于 5 并在牛市中持有 5 天时，买入其平均回报率为 3.3%;
2. 其中 60% 的事件获得正回报，每笔交易的预期回报为 9.8%;
3. 40%的交易是负面的，每笔交易的预期回报率为-6.6%;
4. 分布呈正偏。

---

quantitativo 还统计了反过来的情形，即如果我们在每只标的的 2 天 RSI 收于 5 以上时买入每只股票，并在牛市中持有 5 天的数据。我们将得到：

1. 当任何给定股票的 2 天 RSI 高于 5 时，买入其预期回报率为 0.3%;
2. 交易转为正值的可能性为 52%，预期回报率为 5.5%;
3. 交易转为负值的可能性为 48%，预期回报率为 -5.1%。

quantitativo 还对两次测试是否属于同一分布进行了假设检验，结果 p 值远低于 0.05，证明两个分布显著不同。因此，第一次测试中的因子是存在 Alpha 的。

## 策略回测

接下来quantitativo进行了策略回测。这里策略设计如下：

1. 使用SPY作为测试标的。
2. 当以下条件满足时，在下一次开盘时买入SPY：
   1. 标普指数的RSI(2)收于5之下
   2. SPY高于200日均线
3. 退出条件
   1. 当SPY收盘价高于前一天高点，则在下一次开盘时退出。
   2. 如果SPY收盘价低于200日均线

可以看出，回测策略与Connor提出的策略略有不同。为什么要进行这样的差异化？

---

这里的差异化，其实就是回测与实盘的差异。Connor给出的策略更理想化，而quantitativo的验证策略则更加接近实盘。这是我们做策略时一定要考虑的。

首先，尽管我们可以用标普500来回测，但在实盘中，更切合实际的方法是购买对应的ETF。这里的SPY就是以标普500为标的的ETF。

第二，Connor的策略是以收盘价买入。如果你的回测系统不够精确的话，最好是以次日开盘价买入。当然，如果你的回测系统和行情数据精确到分钟级，那么在国内，也可以利用集合竞价前一分钟的收盘价计算信号，再以集合竞价买入。

退出条件的差异，可以看成是quantitativo对原策略的一个优化。不过，我并没有看出来这个优化的意义。它的背后似乎并不存在任何交易上的原理支撑。看起来，这更像是quantitativo通过数据做出的过拟合。

!!! question
    quantitativo在本次实验中，使用了长达25年的数据进行测试。如果经过这么长的时间回测，数据表现仍然很好，是否就可以说不存在过拟合？我很想知道你们怎么看。


那么，quantitativo的实验结果又是如何呢？

---

在SPY上的测试简直就是灾难。在整个回测期（25 年）中，使用 SPY 交易此策略提供了 67% 的回报。主要原因是交易次数太少，仅执行了 157 笔交易。

接着quantitativo改用了纳斯达克100指数ETF（QQQ）和三倍杠杆纳斯达克100ETF（TQQQ）。结果表明，在TQQQ上表现不错：

![](https://images.jieyu.ai/images/2024/07/performance-qqq-tqqq.jpeg)

夏普比率分别达到了2.3（QQQ）和1.92（TQQQ），对指数标的而言，是相当不错的指标（特别是与A股对比）。

---

## 改进策略：增加因子

在前一次实验的基础上，quantitativo增加了资产组合。

他们把资金分成十份(10 slots)，用于购买前一天RSI收于5以下的标的；如果universe中有10支以上的标的触发了入场信号，将按市值进行排序，优先考虑市值较小的股票。退出条件改为收盘价低于标的200日均线。

此外，他们还限制只交易流动性较好的标的：
1. 只交易过去3个月内完全没有停牌的标的
2. 如果标的过去3个月日均成交量中位数不足资金份额的20倍，则不纳入




<!-- 

1. 多因子策略也可以以某个因子为主，在交易过程中，以限制条件的方式引入其它因子。不过，这样的方式不利于因子作用分析。
2. 判断流动性的的方法
3. 当使用财务数据时，如何确保它是PIT的？
-->

![](https://images.jieyu.ai/images/2024/07/new-experiments-1.jpg)

---

!!! tip
    实际上，在这里quantitativo已经引入了另一个因子，小市值因子，只不过它的权重比较低--是在RSI触发之后才应用权重因子。


这次的结果很不错，整体年回报率达到17.8%，是基准的3倍。但也存在问题，即所有这些都是在前8-9年实现的。该策略在 2008 年后停止执行，并从那时起输给基准。

原因何在？通过分析25年回测期间进行的11,380笔交易，quantitativo发现了很多退市。这种幼稚方法的问题在于，该策略优先考虑小盘股（在通过流动性过滤器后），它们退市的概率为 +70%。

## 第二次改进：降低退市风险

quantitativo再次改进了策略，这次的改进是将universe限制在只交易大型和超大盘股，这些股票的退市概率较低（分别为35%和9%）。

这一次效果非常明显。策略的年化回报达到了23.9%，是同期基准的4倍，夏普达到1.23%，最大回撤为32%，几乎只有标普的一半。

但是，之前就存在的一个问题，交易次数过于频繁仍然存在。现在一年仍然会交易461次。

---

![](https://images.jieyu.ai/images/2024/07/new-experiment-2.jpg)

<!-- quantitativo 在对25年回测期间进行的11,380笔交易进行分析之后，发现了很多退市，但是，这个时间本可以避免 -->

## 第三次改进：减少slots

之前的实验使用了10个slots，这可能是导致交易次数过多的主要原因。于是，quantitativo将同时持有的标的数减少到2支。

现在，交易笔数由461次/年下降到90笔/年。并且实现30.3%的年回报率，是基准的5倍。

这里抛一个问题，年化上升，夏普会跟着上升吗？多给自己一点思考时间，会比全盘接受别人的观点更好。因此，我不在这里公布答案，你可以在留言问我答案，也可以在quantitativo网站上寻找这个答案。

---

## 结论

这篇文章介绍了一个基于短时RSI的均值回归策略，并在最后，给出了年化达30.3%的一个实现（未考虑滑点和交易手续费）。

这个策略的内核是短时RSI，尽管这个指标发明以来已经超过45年，但回测结果表明，只要你研究一件事足够深入，就很可能取得成功。

!!! quote
    It's not that I'm so smart; it's just that I stay with problems longer. -- Albert Einstein

这个方案已经值回你的阅读时间，但更为重要的是，我们讨论了策略发现的一般流程和优化角度。我们再梳理一次，作为本篇的结束语：

1. RSI代表着潮汐和回归，其背后是人性，因此它永远不会过时。
2. 多因子策略也可以以某个因子为主，在交易过程中，以限制条件的方式引入其它因子。
3. 文中给出了判断标的流动性强弱的方法，你也可以将其作为一个因子。
4. 研发策略的步骤往往从单因子检验开始，再编写简单回测，然后根据回测结果一步步优化。
5. 在优化过程中，quantitativo先是使用ETF，然后改用了10个slots，最终回到2个slots的方案。
