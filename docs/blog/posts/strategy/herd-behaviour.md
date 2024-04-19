---
title: 羊群效应及其因子化
slug: herd-behaviour
date: 2023-12-28
motto: 凌晨两点 我看到海棠花未眠
lunar: 冬月十六
categories:
    - strategy
tags:
    - strategy
---

![R50](https://images.jieyu.ai/images/2023/12/structual-modeling-herd-behaviour.png)

在之前的笔记中，我们多次将现代金融理论与A股中流行的股谚、规律和大V的经验之谈结合起来，我们戏称为现代金融理论的中国化。本篇笔记将继续沿着这一思路展开，介绍羊群效应，以及在A股中，它有哪些表现，如何实现因子化，等等。

今天我们要介绍的股谚，是<red>养家心法</red>里中的一条，<red>得散户者得天下</red>。它实际上讲的是要充分利用羊群效应。

<!--more-->

羊群效应理论 ( The Effect of Sheep Flock)，也称为羊群行为（Herd Behavior）、从众心理（Herd Instinct），是行为金融学的重要理论之一。

---

经济学里经常用“羊群效应”来描述经济个体的从众跟风心理。羊群是一种很散乱的组织，只要一只领头羊带动，其它的羊就会跟着走，根本不会思考前方是否会有狼（<red>危险</red>），或者正在远离丰茂的水草（<red>利益</red>）。

在投资领域，羊群效应几乎无时不刻在发挥作用。即使是在价值投资领域，这种效应也是非常明显的。比如，人们会花数百万元买下巴菲特的午餐时间，就是为了得到他的投资上的指点。巴菲特与 A 股最著名的例子是购买并推荐了某石油，这导致大批散户跟风，被套在 6000 点的山冈上。

Christie and Huang 在 1995 年，率先对全市场范围下的羊群效应进行了实证研究，该研究没有发现美国、日本和香港市场存在羊群效应的证据，但在台湾、韩国市场则比较肯定地发现了羊群效应。

![](https://images.jieyu.ai/images/2023/12/herd-behaviour.png)

作为量化博主，我更关心如何将这种效应因子化。下面，就介绍几个相关的因子。

---

## 新开户人数因子

新开户人数可以通过 akshare 来获取：

```python
import akshare as ak

# 得到每月新开户人数
accounts_df = ak.stock_account_statistics_em()
accounts_df
```

这样我们得到了 2015 年 4 月以来的投资者账户数据。

![](https://images.jieyu.ai/images/2023/12/investor-account.jpg)

它的返回值中，有一列为数据日期，其格式形如"2015-04"，我们需要将其转换成为正规的日期格式。

```python
# 这里演示了如何取 DATAFRAME 的数据单元
end = accounts_df.iloc[0]["数据日期"]
start = accounts_df.iloc[-1]["数据日期"]

yr, month = end.split("-")
end = datetime.date(int(yr), int(month) + 1, 1)

```

---

```python
# tf.floor 是 OMICRON 的函数，它将日期对齐到上一个已结束的周期
# 在 OMICRON 中，提供了大量时间运算函数，是量化中必备的
end = tf.floor(end, FrameType.MONTH)

yr, month = start.split("-")
start = datetime.date(int(yr), int(month) + 1, 1)
start = tf.floor(start, FrameType.MONTH)
```

我们得到了投资者账户数据中的起止时间，现在就可以取指数行情，并进行绘图。

```python

# 获取上证指数
bars = await Stock.get_bars_in_range("000001.XSHG", 
                                    FrameType.MONTH, 
                                    start, end)

# 将新增投资者人数与上证指数走势对应起来
df = pd.DataFrame({"xshg": bars["close"][::-1] / 10, 
                   "investor": accounts_df["新增投资者-数量"]})
df.index = accounts_df["数据日期"]

fig = px.line(df)
fig.update_layout(hovermode="x unified")
fig.show()
```

对应关系如下图所示：

![75%](https://images.jieyu.ai/images/2023/12/20231227214221.png)

---

可以看出，月新增投资者的人数的上限大约是在 220 万左右，下限在 100 万左右。这个上下限，与随后上证的指数走势，有一定的相关性。目前我们可以数出来的是，大约新增投资者人数处于下限时，上证大约有 70%左右的概率处于底部；新增投资者人数处于上限时，上证也大约有 70%处在头部。

这只是一个视觉上的规律。在课程的第三部分（统计科学与 Python 数据分析），会介绍如何用统计学的规律来描述这种相关性。另外，在学习了第三部分之后，我们也将知道：如果当月新增投资者人数达到 200 万，下个月投资者人数继续增加的可能性会是多少？

这一点很重要。毕竟，在击鼓传花的游戏中，鼓点是不能停的。

## 人气指数因子

Akshare中有一个函数，它可以获取股吧里，某个标的的人气指数。显然，人气指数是一个典型的散户指数，毕竟，机构钱多，散户人多。

这个方法是：

```python
import akshare

akshare.stock_hot_rank_detail_realtime_em("SZ000665")
```

输出结果为：

---

![75%](https://images.jieyu.ai/images/2023/12/hot_rank_detail_realtime.jpg)

这里的数据足够丰富，能否成为一个因子，大家可以拿alphalens来做做看。

## 结束语

A股是一个有着明显羊群效应的市场，得散户者得天下。这里只举了两个因子的例子，还有更多的因子有待发掘。

作为一名量化框架开发者，我非常认可和强调向牛散和大 V 学习，后面会有更多笔记，发掘大V操作经验背后的现代金融理论原理，并尝试将其量化。

建了一个[小红书学习打卡群](https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c)，坚持学习的朋友可以进来打卡。今日打卡语录：

<div style="font-size: 2.5vw;color:grey; font-style:italic">
凌晨两点 我看到海棠花未眠<br>
怀念起当年不眠不休 一起赶due的时光<br>
坚持学习 <br>
在未来 遇见更好的自己<br>
</div>
