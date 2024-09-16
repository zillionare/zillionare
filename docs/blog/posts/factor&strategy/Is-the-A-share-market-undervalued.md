---
title: 节前迎来揪心一幕！谁来告诉我，A股现在有没有低估？
date: 2024-09-16
category: factor&strategy
slug: Is the A-share market undervalued?
motto: 
img: https://images.jieyu.ai/images/2024/09/eastmoney-pe-stats.png
stamp_width: 60%
stamp_height: 60%
tags: [strategy, pe]
---


节前迎来揪心一幕，主要指数均创出今年最低周收盘。很自然，我们也想知道，现在处于什么状态，存在着低估机会吗？这篇文章，我们从市盈利的角度来探讨是存在机会，还是要警惕陷阱。

我们通过akshare来获取沪指导市盈率。实际上，akshare中的这个数据又来自乐咕乐股网站。

```python
import akshare as ak

pe = ak.stock_market_pe_lg(symbol="上证")
pe.set_index("日期", inplace=True)
pe.index.name = "date"
pe.rename(columns={"平均市盈率": "pe", "指数": "price"}, inplace=True)
pe.tail(15)
```

我们将得到从1999年以来的所有数据。它的格式如下：

![表1 市盈率与指数](https://images.jieyu.ai/images/2024/09/pe-vs-index.jpg)

## 低估的八月？

我们可以通过quantile函数，找出PE的25%， 50%和75%分位数：

```python
percentiles = []
for i in range(1, 4):
    percentiles.append(pe["pe"].quantile(i/4))

percentiles
```

我们发现，从1999年以来，25%， 50%和75%分位数分别是 13.9， 17.4和 33.5。

那么，到上个月底（2024年8月），沪指的市盈率处于什么位置呢？

我们可以用以下方法来计算出这个位置：

```python
rank = pe.rank().loc[datetime.date(2024,8,30), "pe"]
percentile = rank / len(pe)
percentile
```

结果显示，当前的市盈率处在10.6%分位数左右，也就是属于1999年以来较低的位置。

如果仅根据统计数据来看，显然沪指在2024年8月底，是被低估了，换句话说，这里出现了买入机会。

但是，**分位数是静态的，它不能反映数据的运行趋势**。

## 趋势中的PE

如果你打开东财的客户端，找到沪指的资料页，就可以看到PE的历史走势。近十年的走势图如下：

![](https://images.jieyu.ai/images/2024/09/eastmoney-pe-stats.png)

不过这似乎也给出不了更多信息。从这个图来看，沪指目前也是在低估中。

那么，我们把历年的价格走势叠加到PE走势上，看看PE的峰谷是否真的会对应价格的峰谷。

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig, ax1 = plt.subplots(figsize=(60,6))

color = "tab:blue"
ax1.plot(pe["price"], label="Index", color=color)
ax1.set_xlabel("Year")
ax1.set_ylabel("Index", color="tab:blue")
ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[2, 5, 8, 11]))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 

color = "tab:red"
ax2 = ax1.twinx()
ax2.plot(pe["pe"], label="PE", color=color)
ax2.set_ylabel("PE", color=color)

for i in range(1, 4):
    quantile = pe["pe"].quantile(i/4)
    ax2.axhline(quantile, color='gray', linestyle='--', label=f"{i/4:02.0%}")

plt.title("Index vs PE")

fig.tight_layout()
for date in pe.index[::3]:
    ax1.axvline(date, color='gray', linestyle=':', linewidth=0.5)
plt.gcf().autofmt_xdate()

plt.legend(loc="upper left")
plt.show()
```

我们会得到如下所示的绘图：

![1999年-2024年](https://images.jieyu.ai/images/2024/09/index-vs-pe-1999-2024.png)

从图中可以看出，从1999年到2024年间，总体上存在沪指上涨，PE下降的趋势。沪指上涨应该是反应了GDP增长的长期趋势；而PE下降，则主要是由于资产供应数量的增加，导致资产泡沫不断被挤出的趋势。

为了能研究细节部分，我们将上图切割成为5个子图：

![1999年1月-2004年5月](https://images.jieyu.ai/images/2024/09/index-vs-pe-199901-200405.jpg)

![2004年6月-2009年5月](https://images.jieyu.ai/images/2024/09/index-vs-pe-200402-2009-05.png)

![2009年6月-2014年7月](https://images.jieyu.ai/images/2024/09/index-vs-pe-2009-06-2014-08.png)

![2014年6月-2019年10月](https://images.jieyu.ai/images/2024/09/index-vs-pe-2014-05-2019-11.png)

![2019年8月-2024年8月](https://images.jieyu.ai/images/2024/09/index-vs-pe-2019-08-2024-08.png)

## 思考与结论

* 思考： 在哪些阶段，PE走势与沪指完全一致？在这种走势中，谁是因变量，谁是自变量？它反应什么样的现象？

* 回答：在1999年到2001年，2005年8月到2008年5月，以及2014年5月到1015年5月等时间段PE的走势与沪指完全一致。在这种走势中，由于市场炒作十分激烈，公司盈利的变化相对于股价的变化而言，完全可以忽略不计，PE的走势完全由股价决定，从而导致PE曲线与股价走势极为相似。一旦出现这种现象，就说明市场已经过度投机了。

* 思考：大约从2023年8月起，似乎可以看出，沪指的下降速度快于PE的下降速度。比如，2024年2月，沪指出现阶段低点，PE也出现阶段低点。但2024年9月，沪指创新低之后，PE并没有创新低。这种背离反映了什么现象？能否用一个常见的术语来表述它？
* 回答: 在2024年9月，沪指创新低之后，PE并没有创新低，出现了背离。这种情况其实从峰值分析也可以看出来。比如，2024年6月（参见表我1），PE值创2023年8月以来的新高，但沪指却低于2023年8月后任何一个高点。这种背离可以用低市盈率陷阱来描述。这个指标提醒我们，当前指数虽然在下跌，但上市公司的盈利能力也可能在下降，从而出现指数小涨，PE大涨；指数跌得多，PE跌得少的情况。

因此，如果仅从分位数统计来看，当下的A股是低估的。但如果考虑到市盈率总体上一直在下降的趋势，以及最近一年来PE与指数涨跌的背离情况，判断A股是否已经低估还存有疑问，应该纳入更多维度进行判断。

文章来源于《因子分析与机器学习策略》第2课的习题。
