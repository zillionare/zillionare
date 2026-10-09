---
title: "QMT Adjustment Factor Too Slow? 100x Faster Vectorized Method"
date: 2024-03-10
slug: en/posts/python/qmt-how-to-handle-dr-adjust
tags: [QMT, Adjustment Factors, Vectorization]
excerpt: "Still looping with XtQuant's example to compute adjustment factors? This vectorized approach converts dividend data to factors in bulk, running 100x+ faster for market-data storage and backtest prep."
lang: en
translation_of: posts/python/qmt-how-to-handle-dr-adjust
auto_translated: true
source_sha: dce1d9e6871c54c0d9b5957e048afce55cce342b
---

QMT's XtQuant library provides the data you need for quant research. Some of its APIs are designed fairly low-level, so application code usually needs an extra wrapper — adjustment is a good example.

This post shows a high-performance algorithm for converting XtQuant ex-rights and dividend info into the adjustment factors you actually use. It's over 100x faster than the official example.

---

!!! info
    With XtQuant's `get_market_data_ex` API, you can pull already-adjusted bars directly. But if you want to store market data more efficiently yourself, you should store raw unadjusted prices plus adjustment factors, and compute adjusted prices on the fly for whatever window you need. That means you also need to store the factors.

XtQuant doesn't provide adjustment factors directly. Instead, its `get_divid_factors` method returns more granular dividend, bonus-share, and rights-issue details, like this:

<div>
<table border="1" class="z-table">
  <thead>
    <tr style="text-align: right;">
      <th>date</th>
      <th>interest</th>
      <th>stockBonus</th>
      <th>stockGift</th>
      <th>allotNum</th>
      <th>allotPrice</th>
      <th>gugai</th>
      <th>dr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>20121019</td>
      <td>0.100</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.007457</td>
    </tr>
    <tr>
      <td>20130620</td>
      <td>0.170</td>
      <td>0.6</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.614093</td>
    </tr>
    <tr>
      <td>20230614</td>
      <td>0.285</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.025261</td>
    </tr>
  </tbody>
</table>
</div>

<br>The information is very complete, but using it directly for price adjustment is tedious. In most quant workflows, a single factor-ratio is enough to compute forward- and backward-adjusted prices. So we need to convert the data above into adjustment factors.

XtQuant's examples already include a snippet that does this conversion. Because it's meant for illustration, it favors readability and uses a loop instead of vectorized operations.

---

Here is the official example code:

```python
def gen_divid_ratio(bars, divid_datas):
    drl = []
    dr = 1.0
    qi = 0
    qdl = len(bars)
    di = 0
    ddl = len(divid_datas)
    while qi < qdl and di < ddl:
        qd = bars.iloc[qi]
        dd = divid_datas.iloc[di]
        if qd.name >= dd.name:
            dr *= dd['dr']
            di += 1
        if qd.name <= dd.name:
            drl.append(dr)
            qi += 1
    while qi < qdl:
        drl.append(dr)
        qi += 1
    return pd.DataFrame(drl, index = bars.index, 
                        columns = bars.columns)

# 获取除权信息
dd = xtdata.get_divid_factors(s, start_time="20050104")

# 获取未复权行情
bars = xtdata.get_market_data(field_list, ["000001.SZ"], 
                                '1d', 
                                dividend_type = 'none', 
                                start_time='20050104', 
                                end_time='20240308')
%timeit gen_divid_ratio(bars["close"].T， dd)
```

---

This code computes the adjustment factor for 000001.SZ (Ping An Bank) since January 4, 2005. Starting at 1, the factor is multiplied by `dr` on each ex-dividend / ex-rights date. The result is therefore generally an increasing series starting from 1.

In a notebook, this runs in about 407ms±14ms.

Below, we'll show how to vectorize it for a 100x speedup.

```python
def get_factor_ratio(symbol: str, start: datetime.date, end: datetime.date)->pd.Series:
    """获取`symbol`在`start`到`end`期间的复权因子
    
    复权因子以EPOCH日为1，依次向后增加。返回值取整个复权因子区间
    中[start, end]这一段。

    Args:
        symbol: 个股代码，以.SZ/.SH等结尾
        start: 起始日期，不得早于EPOCH
        end: 结束日期，不得晚于当前时间

    Returns:
        以日期为index的Series
    """
    if start < tf.int2date(EPOCH):
        raise ValueError(f"start date should not be earlier than {EPOCH}: {start}")
    
    start_ = tf.date2int(start)
    end_ = tf.date2int(end)
    df = xt.get_divid_factors(symbol, EPOCH)

```

---

```python
    df.index = df.index.astype(int)
    frames = pd.DataFrame([], index=tf.day_frames)
    factor = pd.concat([frames, df["dr"]], axis=1)
    factor.sort_index(inplace=True)
    factor.fillna(1, inplace=True)

    query = f'index >= {start_} and index <= {end_}'
    return factor.cumprod().query(query)["dr"]
```

We set EPOCH to January 4, 2005 — the year China's split-share reform kicked off full circulation. Corporate governance changed materially around that point, so for backtests there is generally little need to use earlier data.

!!! info
    Rome wasn't built in a day, and neither was the reform. For quite a while afterward you could still see tickers starting with S, meaning the company hadn't completed the split-share reform. Still, you have to go with the majority. Many people think quantitative investing is purely about algorithms, but understanding and cleaning messy data matters just as much for returns as the algorithm itself.

The core idea is simple: dd['dr'] is sparse, timestamped data. First we expand it into a dense series:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/convert-dr-factor.jpg)

---

From there, a single cumprod gives you the factor ratio you need.

The first step is effectively a join. We join an empty DataFrame indexed by consecutive trading days with dd['dr']: where a record exists in dd['dr'] we take its value, otherwise we get a null.

Then we use pandas fillna to replace all nulls with 1. Finally, since we only need factors in [start, end], we filter with DataFrame.query.

This produces the same result as the official example, but runs in only 3.96ms±251 — more than 100x faster than the loop version.

We developed this method as part of the zillionare integration for XtQuant data. In that setup we use ClickHouse to store market data for better backtest performance, so we also have to handle incremental updates. The idea is straightforward: save the factor ratios computed above into ClickHouse; on each daily update, read the last update date (T0) of the factor ratios for all stocks, use it as the lower bound to pull the latest ex-rights info via `xtdata.get_divid_factors`, recompute factors since T0 the same way, multiply by the T0 factor value, and write back to ClickHouse.

The Zillionare build with XtQuant support will be version 2.1, expected in June.
