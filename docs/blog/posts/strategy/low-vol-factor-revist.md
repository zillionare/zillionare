---
title: 低波动因子回顾
subtitle: 
slug: revist-of-low-volatility-factor
date: 2024-04-22
categories:
    - strategy
motto: 买在无人问津处 卖在人声鼎沸时
img: https://ei.marketwatch.com/Multimedia/2013/01/07/Photos/MD/MW-AX868_haugen_20130107141040_MD.jpg
lineNumbers: true
tags: 
    - strategy
    - factor
    - 波动率
---

我们在4月份曾发过一篇笔记：新国九条下，低波动因子重要性提升！现在又过去了几个月，我们来回顾下，这个因子最近几个月的表现。


```python
# 空气指增策略，取全市场股票作为universe
for sec in universe:
    # 获取到6月为止，所有股票41个月的开盘价和收盘价
    bars = ...

    df = pd.DataFrame(bars[["date", "close", "open"]], columns=["date", "close", "open"])
    
    # 计算个股的月收益率及36月波动率（滑动窗口）
    returns = df.close.pct_change()
    df["vol_36"] = 1 / returns.rolling(window=36).std()

    df = df.set_index('date')
    
    dfs.append(df)

df = pd.concat(dfs)
df = (
    df.groupby(['asset', pd.Grouper(freq='M')])
    .agg({'close': 'last', 'vol_36': 'last', 'open': 'first'})
    .reset_index("asset")
    .dropna(how='any')
)

df.groupby("asset").head(2)
```

我们对数据进行了重采样。这么处理的原因是，数据源在返回月线时，如果某支股票当月月底停牌，那么它返回的月线日期就会比其它股票早。这种日期上的不一致，会给后续计算带来很多困难，因此，我们提前通过重采样对其进行对齐。如果你用Alphalens进行日线以上频率的因子检验的话，通过数据重采样进行日期对齐，是保证结果正确性很重要的一环。

最终我们得到的df，数据大致如下：

![](https://images.jieyu.ai/images/2024/07/low-vol-revisit-1.jpg)

在完成数据采集之后，我们就逐月计算波动率最小的20%股票：

```python {class=line-numbers}
def find_low_vol(df):
    n = int(len(universe)* 0.2)

    top_assets_per_day_flat = (
        df
        .groupby(level=0)
        .apply(lambda x: x.nlargest(n, 'vol_36')['asset'])
        .reset_index(level=1, drop=True)
        .groupby(level=0)
        .apply(list)
    )

    return top_assets_per_day_flat.to_dict()
low_vols = find_low_vol(df)

```

最终得到的low_vols共有6项，分别是从今年的1月到6月，波动率最小的20%股票的代码。这里用了比较多的pandas的技巧。比较常用的是，如何对数据进行分组，再取组内的前n个记录。这是代码：

```python
df.groupby(level=0).apply(lambda x: x.nlargest(n, 'vol_36')['asset'])
```

的作用。这里`df`是按日期进行索引的。当我们按索引进行分组时，需要传入`level=0`，表示是按索引进行分组。

另外一个技巧是，取得分组内前n个记录之后，如何提取其中的某列，并转换成为dict。这是代码第8行到第10行的任务。

接下来，我们就计算因子筛选出来的股票，在其后的T1,T2,...T5个月的累计收益率。我们的计算方法是，对T0..T4月筛选出来的股票，分别计算：
   1. T1月的开盘价
   2. 用T1..T5月的收盘价与T1月的开盘价，计算收益率
   3. 为简单起见，仓位分配使用等权分配。注意在Alphalens进行因子检验时，它使用的是按因子权重分配。

上述算法可以用代码表示为：

```python
from collections import defaultdict

def compute_returns(low_vols):
    all_returns = defaultdict(list)
    for dt, assets in low_vols.items():
        month = dt.month
        df1_filter = (df.index.month == month + 1) & df.asset.isin(assets)

        # 提取T1月开盘价
        df1 = df[df1_filter].sort_values("asset")
        df1 = df1.reset_index(drop=True)
        for t in tf.get_frames(dt, datetime.date(2024, 5, 31), FrameType.MONTH):
            t_month = tf.int2date(t).month + 1

            # 提取T1..T5月收盘价
            df2_filter = (df.index.month == t_month) & df.asset.isin(assets)
            df2 = df[df2_filter].sort_values("asset")
            df2 = df2.reset_index(drop=True)

            # 计算收益，这里利用了pandas的向量化计算能力
            returns = df2.close/df1.open-1
            all_returns[dt].append(returns.mean())

    return pd.DataFrame.from_dict(all_returns, orient="index")

result = compute_returns(low_vols)
result.style.format("{:.2%}")
```

在上面的代码中，我们使用了双重循环，但在循环中，利用了pandas的向量化运算以简化操作。为了保证向量化操作结果的正确性，我们使用了`sort_values`对数据进行排序，并且保证df1（用来提取开盘价）和df2（用来提取收盘价）的asset列是相同的。

最终，我们得到下面的结果：

![](https://images.jieyu.ai/images/2024/07/low-vol-factor-revist-result.jpg)

这个结果令人震惊。低波动因子最近几个月的表现会有这么好吗？还是出现计算错误？不过，数据在月度之间的变化，呈现出某种自洽性。比如，1月筛选出来的股票，在2月仅上涨2.89%,在3月上涨7.10%(累计，包括2月，下同)，在4月则上涨147%。但在2月筛选出来的股票中（对低波动因子来说，1月筛选出来的多数股票应该得以保留），同样在3月上涨不大，也是到了4月才大幅上涨，并且上涨幅度与1月股票池上涨幅度相匹配。

尽管如此，这个结果还是难以置信。低波动因子长期看好自有它的道理，今年受国九条影响，短期也确实受到的热捧，绝对收益相对突出也是肯定的，但持有4个月，涨幅接近翻倍，还是比较可疑，需要谨慎对待。

因子检验和回测往往就是这样，当你得到一个结果，如果不是好得令人难以置信，你根本没有机会去怀疑它。

不过，借此机会分享下低波动因子从2008年以来，到2023年底的因子检验表现：

![](https://images.jieyu.ai/images/2024/07/low-vol-factor-alphalens-1.jpg)

因子分层回测表明，最佳的一组，按持有10个月换手，年化收益达到了28.17%。如果看累积收益图的话，我们会发现，2016年之后，收益率明显更好。我对此的解释时，2016年之后，GJ队，公墓基金成为了市场的主力。

![](https://images.jieyu.ai/images/2024/07/low-vol-factor-alphalens-2.jpg)

