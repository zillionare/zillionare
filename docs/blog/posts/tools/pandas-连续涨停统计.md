---
title: "Pandas连续涨停统计"
date: 2024-10-23
category: tools
slug: how-to-count-continuous-buy-limit
img: https://images.jieyu.ai/images/university/harvard.jpg
tags: [tools, pandas]
---


![题图: 哈佛大学](https://images.jieyu.ai/images/university/harvard.jpg)

常常需要快速统计出一段时间内，最强的股和最弱的股，以便研究该区间内，强势股和弱势股有什么特点。

如果使用循环，这就跟掰着手指头数数没啥区别，各位藤校生一定是不屑的。所以，我们来看看如何简洁优雅地实现这一功能，同时可以在同事面前zhuangbility.

---

这里我们以2023年的数据为例，要求统计出连续涨停在n天以上的个股，并且给出涨停时间。同样的方案也可以找出当年最终的股，以及它们的时间。

你可以对着屏幕把代码copy下来，自己找来数据验证。不过要是赶时间的话，建议加入我的部落：

![](https://images.jieyu.ai/images/hot/logo/zsxq.png)

加入部落者，即可获得Quantide研究环境账号，直接运行和下载本教程。

我们先加载数据：

---

```python
np.random.seed(78)
start = datetime.date(2023,1,1)
end = datetime.date(2023, 12, 31)

barss = load_bars(start, end, -1)
barss.tail()
```

load_bars函数在我们的研究环境下可用。这将得到以下格式的数据：

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>date</th>
      <th>asset</th>
      <th>open</th>
      <th>high</th>
      <th>low</th>
      <th>close</th>
      <th>volume</th>
      <th>amount</th>
      <th>price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-12-25</th>
      <th>****</th>
      <td>30.85</td>
      <td>31.20</td>
      <td>30.06</td>
      <td>30.08</td>
      <td>3591121.00</td>
      <td>109649397.62</td>
      <td>30.14</td>
    </tr>
    <tr>
      <th>2023-12-26</th>
      <th>****</th>
      <td>30.14</td>
      <td>30.25</td>
      <td>26.00</td>
      <td>27.85</td>
      <td>9042296.00</td>
      <td>251945474.00</td>
      <td>27.90</td>
    </tr>
    <tr>
      <th>2023-12-27</th>
      <th>****</th>
      <td>27.90</td>
      <td>28.89</td>
      <td>27.18</td>
      <td>28.89</td>
      <td>5488847.00</td>
      <td>155156381.16</td>
      <td>28.58</td>
    </tr>
    <tr>
      <th>2023-12-28</th>
      <th>****</th>
      <td>28.58</td>
      <td>29.85</td>
      <td>28.44</td>
      <td>29.20</td>
      <td>5027247.00</td>
      <td>147201133.00</td>
      <td>29.25</td>
    </tr>
    <tr>
      <th>2023-12-29</th>
      <th>****</th>
      <td>29.25</td>
      <td>30.14</td>
      <td>29.25</td>
      <td>29.66</td>
      <td>3923048.00</td>
      <td>116933800.77</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>


我们只取价格数据，然后展开成宽表，以求出每天的涨跌符：

```python
pd.options.display.max_columns = 6
returns = barss.close.unstack("asset").pct_change()
returns.tail()
```

---

现在我们将得到这样的结果：

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>date</th>
      <th>****</th>
      <th>****</th>
      <th>****</th>
      <th>...</th>
      <th>****</th>
      <th>****</th>
      <th>****</th>
    </tr>

  </thead>
  <tbody>
    <tr>
      <th>2023-12-25</th>
      <td>-0.00</td>
      <td>-0.01</td>
      <td>-0.02</td>
      <td>...</td>
      <td>-0.01</td>
      <td>-0.03</td>
      <td>-0.03</td>
    </tr>
    <tr>
      <th>2023-12-26</th>
      <td>-0.01</td>
      <td>-0.01</td>
      <td>-0.02</td>
      <td>...</td>
      <td>0.00</td>
      <td>-0.02</td>
      <td>-0.07</td>
    </tr>
    <tr>
      <th>2023-12-27</th>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.02</td>
      <td>...</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>0.04</td>
    </tr>
    <tr>
      <th>2023-12-28</th>
      <td>0.04</td>
      <td>0.03</td>
      <td>0.01</td>
      <td>...</td>
      <td>0.03</td>
      <td>0.02</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>2023-12-29</th>
      <td>-0.01</td>
      <td>-0.01</td>
      <td>0.02</td>
      <td>...</td>
      <td>0.00</td>
      <td>-0.00</td>
      <td>0.02</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 5085 columns</p>
</div>


接下来，我们要判断哪一天为涨停。因为我们的目标并不是执行量化交易，只是为了研究，所以，这里可以容忍一定的误差。我们用以下方式决定是否涨停（排除北交所、ST）：

```python
criteria = ((returns > 0.095) & (returns < 0.105)) | 
            ((returns > 0.19)& (returns < 0.21))
zt = returns[criteria].notna().astype(int)
```

这里的语法要点是，如何使用多个条件的组合，以及如何将nan的值转换为0，而其它值转换为1。

---

这里会出现nan，是因为我们处理的是宽表。在宽表中，有一些列在某个点上（行）不满足条件，而在该点上，其它列满足条件，导致该行必须被保留；不满足条件的列，在该行的值就是nan。然后我们用notna将nan转换为False，其它值转换为True，最后通过astype转换为整数0和1，1代表该天有涨停。

接下来，我们就要对每一个资产，统计它的连续涨停天数。我们用以下函数来处理：

```python
def process_column(series):
    g = (series.diff() != 0).cumsum()

    g_cumsum = series.groupby(g).cumsum()

    result = series.copy()
    result[g_cumsum > 1] = g_cumsum[g_cumsum > 1]
    return result
```

---

这个函数的**巧妙之处**是，它先计算每一行与前一行的差值，并进行累加。如果有这样一个序列: 0 0 1 1 1 0 0，那么diff的结果就是nan, 0, 1, 0, 0, -1, 0。这里不为0的地方，就表明序列的连续状态发生了变化：要么出现连续涨停，要么连续涨停中止。

然后它通过cumsum累计差分序列。这样就与原序列形成如下的对应关系：

| 原序列 | diff | diff!=0 | cumsum |
| ------ | ---- | ------- | ------ |
| 0      | nan  | true    | 1      |
| 0      | 0    | false   | 1      |
| 1      | 1    | true    | 2      |
| 1      | 0    | false   | 2      |
| 1      | 0    | false   | 2      |
| 0      | -1   | true    | 3      |
| 0      | 0    | false   | 3      |

如果把这里的cumsum看成组号，那么就可以通过groupby分组，然后计算每组中非0的个数，就得到组内连续涨停次数。这就是第4行的工作。

**Marvelous!**

---

最后，我们来应用这个函数：

```python
df_processed = zt.apply(process_column, axis=0)
df_processed.stack().nlargest(5)
```

我们得到以下结果（部分）：

| date       | asset       | 连续涨停 |
| ---------- | ----------- | -------- |
| 2023-10-25 | ******.XSHG | 14       |
| 2023-10-24 | ******.XSHG | 13       |
| 2023-03-21 | ******.XSHE | 12       |
| 2023-10-23 | ******.XSHG | 12       |
| 2023-03-20 | ******.XSHE | 11       |

我们拿其中一个验证一下：

```python
code = "******.XSHG"

bars = barss.xs(code, level="asset")
bars["frame"] = bars.index

plot_candlestick(bars.to_records(index=False), 
                ma_groups=[5,10,20,60])
```

---

我们来看下k线图：

![](https://images.jieyu.ai/images/2024/10/slgf-zt-2023-10-19.jpg)


最后，我们把函数封装一下：

---

```python
def find_buy_limit(closes, low = 0.095, high = 0.105,n=50):
    def process_column(series):
        group = (series.diff() != 0).cumsum()

        group_cumsum = series.groupby(group).cumsum()

        result = series.copy()
        result[group_cumsum > 1] = group_cumsum[group_cumsum > 1]
        return result
    
    returns = closes.unstack("asset").pct_change()
    criteria = (returns > low) & (returns < high)

    zt = returns[criteria].notna().astype(int)
    df_processed = zt.apply(process_column, axis=0)
    return df_processed.stack().nlargest(n)

find_buy_limit(barss.close)
```

最后，这一届的奥斯卡颁给...的主力（算了，哪怕是历史数据，也不要透露了）。

当你不知道该往哪里踢时，就往球门里踢！现在，对着你去年错过的连接14个涨停，来找找规律吧！

