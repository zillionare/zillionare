---
title: 龙凤呈祥：这种无底限炒作，如何用量化方法发现它？
slug: magic-hot-word-factor
date: 2024-01-23
img: https://images.jieyu.ai/images/2024/01/dragon-and-phoenix.jpg
category: strategy
motto: 这世界是个草台班子 但你我不是
lunar:
tags: 
    - strategy
    - 涨停板
---

作为量化人，我们敏锐地观察市场，不放过任何一个可能产生利润的机会。一旦发现这样的机会，我们决不会在乎其它人怎么看怎么想，书上有没有这么讲。**但是，大胆假设，小心求证。**

今天带来的因子，挺魔幻的，我把它叫做魔性汉字。如果你难以接受这种无底线的炒作，那么，我们换一个名字：另类因子。

<!--more-->


2023年底，市场开始炒作龙字，后来又开始炒凤字，被戏称为龙凤呈祥。2024年的年度汉字可能是华。这是一种魔幻和无厘头的炒作。但就像一年有四季一样，A股一年至少会这样魔幻地炒一次。

在历史上并不罕见。老股民会记得在2018年底，2019年初，出现了一支十倍牛股，东方通信。它带动了对”东方“这个词的炒作。一时间，只要标的名称中带有”东方“两字的，都能沾上一点雨露。

现在我们就来看看，要怎么实现这个因子。

!!! tip 思路
    1. 取当天攻击力最强的标的（也就是涨停了的个股）
    2. 通过分词技术，找出计数最高的词
    3. 找出包含该词，但当天未涨停个股，组成板块
    4. 获取板块后10天行情数据，按照1天、5天和10天周期，计算pnl。

 我们略过如何获取涨停名单的过程。无论是使用akshare,还是jqdatasdkq都可以拿到历史涨停数据。

 在寻找最热的词时，我们先是去掉”股份、科技和控股“这几个词。它们在名称中出现太过频繁，按照TF-IDF的理论，过于频繁出现的词是没有信息量的。



```python
# 使用的数据源在证券名称上，没有提供PIT数据。当前已退市的标的，
# 其名字为None。我们要先滤掉这部分。注意这里已经引入了一个回测
# 偏差
text = " ".join(filter(lambda x: x, df["alias"]))

# 排除掉没有信息量的词
cleaned = re.sub(r"股份|科技|控股", "", text)
```

接下来我们处理热词。根据观察，热词可能是像”东方“这样的两个字的词，也可能是像”龙“、”兔“这样的单字词。所以我们要分两批处理，并且把两字词放在前面。

```python
    for word in jieba.cut(cleaned):
        if word == " " and len(word) != 2:
            continue
        if word in two:
            two[word] += 1
        else:
            two[word] = 1
```

这里我们使用了结巴分词(jieba)。我不太清楚现在的情况，但直到2021年，它一定是Python汉语分词的翘楚。它的作用是，将”东方通信“这样的词，分解为”东方“和”通信“这样两个词。如果”东方航空“也上榜的话，那么它会被分解为”东方“和”航空“，从而”东方“获得两分，通信和航空各获得1分。

类似的方法处理单字词。我们得到的结果（像two)是一个集合。为了取计数最高的字（词），我们要对其进行排序：

```python
two = sorted(two, key = lambda x: x[1], reverse=True)
```

这是非常常用的语法了。



构建板块并不难，但是我们得利用证券列表。这也是我们讲的，任何数据源，在你购买之前，必须要考察它是否具务的几个基本API。如果像证券列表这样的API没有的话，那么几乎无法编写任何策略。

获得某日未涨停个股的清单后，我们就可以取该日及此后10天的行情数据，然后通过pandas的pct_change来计算1，5和10日持有收益。

在因子分析中，这类函数通常叫forward_returns，所以，我们这里也将其命名为get_forward_returns，这样代码更容易阅读。

```python
async def get_forward_returns(dt: datetime.date, n=10):
    ...
    end = tf.day_shift(dt, n)
    barss = {}
    for sec in secs:
        bars = await Stock.get_bars(sec, n+1, FrameType.DAY, end=end)
        if len(bars) != n + 1:
            continue
        barss[sec] = bars["close"]

    df = pd.DataFrame.from_dict(barss)
    returns = []
    for period in (1, 5, 10):
        returns.append(df.pct_change(period).mean())

    df = pd.concat(returns, axis=1).rename(columns={0:"1d", 1:"5d", 2:"10d"})
    mn = df.mean()
    print(f"{dt} {concept} 1D: {mn.iloc[0]:.2%} 5D: {mn.iloc[1]:.2%} 10D: {mn.iloc[2]:.2%}")
    return df
```



在处理过程中，我们就已经打印出了当日板块的1、5和10日未来收益（如果当天存在这种题材炒作的话），以便调试。另外，我们也返回这个收益结果，以方便进一步处理。

最后，我们选择2019-2-10到2019-3-5这个区间运行了一下，结果是：

![](https://images.jieyu.ai/images/2024/01/magic-word-factor-forward-returns.jpg)

你的钱就是这样被赚走的。打不过就加入吧！

源代码自本文发布一周内，支持免费预览。预览方法见[【这里】](http://www.jieyu.ai/articles/coursea/24lectures/preview/)


