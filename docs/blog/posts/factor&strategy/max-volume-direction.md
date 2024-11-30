---
title: 捕捉主力-最大成交量因子
date: 2024-11-13
category: factor&strategy
slug: herd-behaviour-max-volume-direction
motto: 因为黑夜，更能看见满天星光
img: https://images.jieyu.ai/images/2024/11/starry-night.jpg
stamp_width: 60%
stamp_height: 60%
tags: [factor, strategy, herd-behaviour]
---

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/11/starry-night.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>因为黑夜，更能看见满天星光 | ©️ Nathan Jennings</span>
</div>



今天跟一位朋友聊天，他想换到量化行业，有点担心是否有点为时已晚，又或者大环境不好。于是我用这句话鼓励他：

**因为黑夜，更能看见满天星光。**

低谷之中，必有转机，熬过黑暗，前方自有光明。

其实在我身边，已经有好几位『普通人』成功地转向了量化。我之前有一位策略研究员，前几天跟我通了个电话，告诉我已经有私募接洽他，希望买他的策略。他已经注册了自己的公司。他是一个真正的传奇，我会在恰当的时候，讲述他的故事，带给更多人启迪。

做你热爱的事情，不用管其它人给现在的你打上的标签，不要被他人定义。

**You gotta be brave。**

只要你还愿意追逐梦想，你就不是平庸的。

言归正转。

在第十二课，我承诺给大家讲如何发现新的因子。这活儿光说不练不行，我得真真正正拿出一个还没有广泛传播的因子（策略）出来。今天就来兑现这个承诺。我们探索因子，无非就是量价时空四大维度。这里面关于成交量的因子最少，所以，今天就介绍一个我自己探索的因子。

如有雷同，纯属巧合（读书太少）。这个因子是基于成交量，运用羊群效应的原理构建的。

## 因子还没被挖完吗？

在说书之前，先回答一个问题。因子难道还没有被挖掘完吗？毕竟，全世界有这么多做量化的人。

事实是，这世界算力不够，所以，还存在大量的关系没有发掘出来。小市值因子之父，Rolf Banz探索小市值因子的故事，也许能很好说明这一点。



1980年前后，Rolf Banz发表了一篇论文《The relationship between return and market value of common stocks》，向世界介绍了小市值因子。

Banz 的这篇论文并不复杂，只有 16 页纸。论文中并没有使用高深的数学，只是使用了基础的统计科学，GLS 和 OLS。如果当时有计算机可用的话，这个推导过程会显得格外简单。

甚至，我们可以仅凭他论文中的这张图来理解小市值因子：

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/09/low-beta-factor.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>收益与市值分导关系</span>
</div>



在这张图中，Banz把资产按市值大小分成了5组，第一组是市值最小的一组，第5组是市值最大的一组。很显然，其它几组的收益都与市值大小有着线性关系，但第一组，即小市值组有更大的月度收益，不能被线性回归。

就是这样简单的一个事实，帮助Banz获得了小市值之父的称号。如果说威廉.夏普发现了第一个因子的话，Banz就是发现第二个因子的人。

Banz 用到的数据来自 1926 年到 1975 年。这些数据就在芝大的 CRSP 数据库里。在漫长的 50 多年时间里，一直在静静地等待有人发现她的价值。芝大经济学人才辈出，期间不知道有多少人接触过这份数据。如此低垂和芳香的果实最终却被 Banz 采摘。

我想，这足以说明，**在任何时代，在任何圈子，都会有一些低垂的果实，等待有心人去采摘**。

但是，更加惊人的是，另一颗低垂的果实，就出现在Banz自己的论文里。在上图中，资产实际上是被分成了25组。在按市值划分的每个组内，Banz又按波动率将资产分成了5组（在图上纵向分布）。第一组是波动率最大的一组，第5组则是波动率最小的一组。

很显然，在每一个组合中，低波动率的资产收益都大于高波动率的资产。

实际上，这里出现了另外一个因子，就是低波动因子。我们回测过，日线低波动因子可以达到16.4%的年化Alpha。月线可以达到6.3%左右的年化，因子IC是0.04，相当可观。

然后，直到10年之后，Haugen和Baker才发现和命名了低波动因子。Banz做完了几乎所有工作，但却与这项发明失之交臂。


**低垂的果实永远都会有的**

## 最大成交量因子

这个因子也可以叫做主力因子。它的构造原理是，价格的方向是由资金里的主力决定的。因为当个体处于群体中时，其行为和决策受到群体影响，往往会失去理性，变得更加情绪化和冲动。个体往往会受到他人引导，最终会跟随头羊的方向前进，这就是羊群效应。

主力才能决定方向，决定方向的力量也就是主力。因此，主力方向是可以建模的。

<!--PAID CONTENT START-->

```python
import pandas as pd

def max_volume_direction(df, win=40):
    df["flag"] = np.select([
        df["close"] > df["open"],
        df["close"] < df["open"]
    ], [1, -1], 0)
    df["move_vol_avg"] = df["volume"].rolling(window=win, min_periods=win).mean().shift(1)
    df["argmax"] = df['volume'].rolling(win, min_periods=win).apply(lambda x: x.idxmax())
    df.fillna(0, inplace=True)
    df["move_vol_max"] = df.apply(lambda row: df.loc[row['argmax'], 'volume'], axis=1)
    df['vr'] = df['move_vol_max'] / df['move_vol_avg'] * df["flag"]
    df["span"] = df.index - df["argmax"]

    def calc_rolling_net_balance(df):
        pos = df["argmax"].iloc[-1] + 1
        sub = df.loc[pos:,]
        return (sub["flag"] * sub["volume"]).sum() / df["move_vol_max"].iloc[-1]

    balances = []
    for sub in df.rolling(win):
        b = calc_rolling_net_balance(sub)
        balances.append(b)

    df["move_balance"] = balances

    return df[["vr", "move_balance", "span"]]
```
<!--PAID CONTENT END-->

这段代码的逻辑是，如果某个bar的成交量相对于过去一段时间的平均成交量异常放大（用该bar的成交量除以平均成交量，记为vr），那么它就可能是主力的操作。我们认为，该根bar的方向，有较大概率是此后主力的运作方向。

如果这根bar是阳线，它反应的是买入操作；如果这根bar是阴线，它反应的是卖出操作（记为flag）。

主力为了测试对手盘和跟风盘，在试盘之后，有可能中断操作一段时间，借此观察盘面变化。因此，我们要考察该bar之后一段时间的交易情况，把这部分成交量换算成净余成交量（记为move_balance），再除以主力操作的那个bar的成交量（『归一化』）。如果净余成交量与主力bar是同向的，说明对手盘很小（或者没有成为对手的意愿）；如果净余成交量与主力bar相反且较大，则主力的意图有可能难以实现，主力可能暂时放弃操作。

我们拿一个样本测试一下：

```python
import akshare as ak
def test(df):
    df["volume"] = df["volume"].astype(int)
    max_volume_direction(df, 5)

    _, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df["day"], df["close"])

    x = df[df.vr > 4].index
    y = df[df.vr > 4]["close"]
    color = 'r'
    ax.scatter(x, y, c=color, marker="^", s=100)
    for i in x:
        row = df.iloc[i]
        ax.text(i, 
                y[i], 
                f"{row.vr:.1f} {row['day'][5:16]}", 
                fontsize=24, 
                color=color)

    x = df[df.vr < -4].index
    y = df[df.vr < -4]["close"]
    color = 'g'
    ax.scatter(x, y, c=color, marker="v", s=100)
    for i in x:
        row = df.iloc[i]
        ax.text(i, 
                y[i], 
                f"{row.vr:.1f} {row['day'][5:16]}", 
                fontsize=24, 
                color=color)

    ticks = range(0, len(df), 8)
    labels = df['day'].iloc[ticks]
    plt.xticks(ticks, labels, rotation=45, ha='right')
    plt.show()

code = "sz000001"
df = ak.stock_zh_a_minute(symbol=code, period="30", adjust="qfq")
df = df[-240:].copy()
df.index = np.arange(240)

test(df)
```

<!-- BEGIN IPYNB STRIPOUT -->
![](https://images.jieyu.ai/images/2024/11/max-volume-direction-payh.png)
<!-- END IPYNB STRIPOUT -->

在测试中，我们设置vr的阈值为4。在一些比较激进的个股上，设置为8以上可能效果会更好。

在这个简单的例子中，效果比较明显。最初的几个标记需要忽略，因为存在冷启动期。但从9月30日10时起，我们看到：

1. 9月30日10时， 主力的方向是进攻，连续上涨
2. 10月8日10时，主力的方向是下杀，多头抵抗了一段时间，最终下跌
3. 10月14日10时，主力下杀，短期下跌，随后小幅上涨、横盘，最终下跌
4. 10月21日10时，主力下杀，强化了前一个信号。
5. 11月12日10时，主力上攻，未来走势还可以再看看。

当然，重要的是我们自己找到策略思路，并且能用程序的语言将其验证并实施。这些正是《因子分析与机器学习策略》要介绍的内容。在因子创新上，我们从量、价、时、空四个维度，都给出了创新的思路和方向，保持关注，持续为你更新！

