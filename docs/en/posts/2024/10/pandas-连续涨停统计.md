---
title: "Pandas Trick: Detecting Consecutive Daily Limits in China A-Shares ===EXCUT=== This tutorial demonstrates an efficient Pandas-based method to identify consecutive daily limit-up stocks in China A-shares, enabling rapid screening of strong momentum trends without manual looping. ===TAGS=== Pandas, China A-Shares, Daily Limit, Momentum Factor, Quantitative Analysis ===BODY=== ![Header: Harvard University](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/university/harvard.jpg)  Quant researchers often need to rapidly identify the strongest and weakest stocks over a specific period to analyze the characteristics of momentum leaders and laggards.  Using explicit loops for this task is inefficient and inelegant. Let’s explore a concise, high-performance implementation that will also impress your colleagues.  ---  We use 2023 data as an example. The goal is to identify stocks with consecutive daily limit-ups (price limits) exceeding $n$ days, along with the specific dates. This approach can also be adapted to find the year’s strongest performers and their timing.  You can copy the code to verify with your own data. However, if you’re short on time, consider joining our community:  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/logo/zsxq.png)  Members gain access to a Quantide research environment account, allowing direct execution and download of this tutorial.  First, we load the data:  ---  ```python np.random.seed(78) start = datetime.date(2023,1,1) end = datetime.date(2023, 12, 31)  barss = load_bars(start, end, -1) barss.tail() ```  The `load_bars` function is available in our research environment. It returns data in the following format:  <div> <table border=\"1\" class=\"dataframe\">   <thead>     <tr style=\"text-align: right;\">       <th>date</th>       <th>asset</th>       <th>open</th>       <th>high</th>       <th>low</th>       <th>close</th>       <th>volume</th>       <th>amount</th>       <th>price</th>     </tr>   </thead>   <tbody>     <tr>       <th>2023-12-25</th>       <th>****</th>       <td>30.85</td>       <td>31.20</td>       <td>30.06</td>       <td>30.08</td>       <td>3591121.00</td>       <td>109649397.62</td>       <td>30.14</td>     </tr>     <tr>       <th>2023-12-26</th>       <th>****</th>       <td>30.14</td>       <td>30.25</td>       <td>26.00</td>       <td>27.85</td>       <td>9042296.00</td>       <td>251945474.00</td>       <td>27.90</td>     </tr>     <tr>       <th>2023-12-27</th>       <th>****</th>       <td>27.90</td>       <td>28.89</td>       <td>27.18</td>       <td>28.89</td>       <td>5488847.00</td>       <td>155156381.16</td>       <td>28.58</td>     </tr>     <tr>       <th>2023-12-28</th>       <th>****</th>       <td>28.58</td>       <td>29.85</td>       <td>28.44</td>       <td>29.20</td>       <td>5027247.00</td>       <td>147201133.00</td>       <td>29.25</td>     </tr>     <tr>       <th>2023-12-29</th>       <th>****</th>       <td>29.25</td>       <td>30.14</td>       <td>29.25</td>       <td>29.66</td>       <td>3923048.00</td>       <td>116933800.77</td>       <td>NaN</td>     </tr>   </tbody> </table> </div>  We extract only the price data and pivot it to a wide format to calculate daily returns:  ```python pd.options.display.max_columns = 6 returns = barss.close.unstack(\"asset\").pct_change() returns.tail() ```  ---  This yields the following result:  <div> <table border=\"1\" class=\"dataframe\">   <thead>     <tr style=\"text-align: right;\">       <th>date</th>       <th>****</th>       <th>****</th>       <th>****</th>       <th>...</th>       <th>****</th>       <th>****</th>       <th>****</th>     </tr>    </thead>   <tbody>     <tr>       <th>2023-12-25</th>       <td>-0.00</td>       <td>-0.01</td>       <td>-0.02</td>       <td>...</td>       <td>-0.01</td>       <td>-0.03</td>       <td>-0.03</td>     </tr>     <tr>       <th>2023-12-26</th>       <td>-0.01</td>       <td>-0.01</td>       <td>-0.02</td>       <td>...</td>       <td>0.00</td>       <td>-0.02</td>       <td>-0.07</td>     </tr>     <tr>       <th>2023-12-27</th>       <td>0.00</td>       <td>0.00</td>       <td>0.02</td>       <td>...</td>       <td>-0.01</td>       <td>0.00</td>       <td>0.04</td>     </tr>     <tr>       <th>2023-12-28</th>       <td>0.04</td>       <td>0.03</td>       <td>0.01</td>       <td>...</td>       <td>0.03</td>       <td>0.02</td>       <td>0.01</td>     </tr>     <tr>       <th>2023-12-29</th>       <td>-0.01</td>       <td>-0.01</td>       <td>0.02</td>       <td>...</td>       <td>0.00</td>       <td>-0.00</td>       <td>0.02</td>     </tr>   </tbody> </table> <p>5 rows × 5085 columns</p> </div>  Next, we identify days with daily limit-ups. Since this is for research rather than live trading, we allow some tolerance. We define a daily limit-up (excluding Beijing Stock Exchange and ST stocks) as follows:  ```python criteria = ((returns > 0.095) & (returns < 0.105)) |              ((returns > 0.19)& (returns < 0.21)) zt = returns[criteria].notna().astype(int) ```  Key syntax points here include combining multiple conditions and converting `NaN` values to 0 while converting valid matches to 1.  ---  `NaN` values appear because we are working with a wide table. In a wide table, some columns may not meet the condition at a specific row (date), while others do. To preserve the row structure, non-matching values become `NaN`. We then use `notna()` to convert `NaN` to `False` (0) and valid matches to `True` (1), where 1 indicates a daily limit-up.  Next, we count consecutive daily limit-ups for each asset using the following function:  ```python def process_column(series):     g = (series.diff() != 0).cumsum()      g_cumsum = series.groupby(g).cumsum()      result = series.copy()     result[g_cumsum > 1] = g_cumsum[g_cumsum > 1]     return result ```  ---  The **cleverness** of this function lies in its use of difference and cumulative sum operations. Consider the sequence: `0 0 1 1 1 0 0`. The `diff()` result is `NaN, 0, 1, 0, 0, -1, 0`. Non-zero differences indicate a change in the continuity state (either starting or ending a consecutive limit-up streak).  By applying `cumsum` to the difference sequence, we create group identifiers:  | Original Sequence | diff | diff!=0 | cumsum | | ------ | ---- | ------- | ------ | | 0      | NaN  | True    | 1      | | 0      | 0    | False   | 1      | | 1      | 1    | True    | 2      | | 1      | 0    | False   | 2      | | 1      | 0    | False   | 2      | | 0      | -1   | True    | 3      | | 0      | 0    | False   | 3      |  Treating `cumsum` as group IDs, we can use `groupby` to count non-zero values within each group, yielding the number of consecutive daily limit-ups. This is the operation performed on line 4.  **Marvelous!**  ---  Finally, we apply this function:  ```python df_processed = zt.apply(process_column, axis=0) df_processed.stack().nlargest(5) ```  We obtain the following results (partial):  | date       | asset       | Consecutive Limits | | ---------- | ----------- | -------- | | 2023-10-25 | ******.XSHG | 14       | | 2023-10-24 | ******.XSHG | 13       | | 2023-03-21 | ******.XSHE | 12       | | 2023-10-23 | ******.XSHG | 12       | | 2023-03-20 | ******.XSHE | 11       |  Let’s verify one case:  ```python code = \"******.XSHG\"  bars = barss.xs(code, level=\"asset\") bars[\"frame\"] = bars.index  plot_candlestick(bars.to_records(index=False),                  ma_groups=[5,10,20,60]) ```  ---  Here is the candlestick chart:  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/slgf-zt-2023-10-19.jpg)  Finally, let’s encapsulate the function:  ---  ```python def find_buy_limit(closes, low = 0.095, high = 0.105,n=50):     def process_column(series):         group = (series.diff() != 0).cumsum()          group_cumsum = series.groupby(group).cumsum()          result = series.copy()         result[group_cumsum > 1] = group_cumsum[group_cumsum > 1]         return result          returns = closes.unstack(\"asset\").pct_change()     criteria = (returns > low) & (returns < high)      zt = returns[criteria].notna().astype(int)     df_processed = zt.apply(process_column, axis=0)     return df_processed.stack().nlargest(n)  find_buy_limit(barss.close) ```  The Oscar for this year goes to... [Redacted]. (Even with historical data, let’s keep the main actor anonymous.)  When you don’t know where to kick, kick it into the goal! Now, go find patterns in the 14 consecutive daily limit-ups you missed last year!"
date: 2024-10-23
slug: en/posts/tools/pandas-连续涨停统计
tags: [Pandas, China A-Shares, Daily Limit, Momentum Factor]
excerpt: ""
lang: en
translation_of: posts/tools/pandas-连续涨停统计
auto_translated: true
source_sha: 255ffbf00d38ea4c3e236cfd977b13d4b0d8dfaa
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/university/harvard.jpg"
---

![Header: Harvard University](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/university/harvard.jpg)

Quant researchers often need to rapidly identify the strongest and weakest stocks over a specific period to analyze the characteristics of momentum leaders and laggards.

Using explicit loops for this task is inefficient and inelegant. Let’s explore a concise, high-performance implementation that will also impress your colleagues.

---

We use 2023 data as an example. The goal is to identify stocks with consecutive daily limit-ups (price limits) exceeding $n$ days, along with the specific dates. This approach can also be adapted to find the year’s strongest performers and their timing.

You can copy the code to verify with your own data. However, if you’re short on time, consider joining our community:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/logo/zsxq.png)

Members gain access to a Quantide research environment account, allowing direct execution and download of this tutorial.

First, we load the data:

---

```python
np.random.seed(78)
start = datetime.date(2023,1,1)
end = datetime.date(2023, 12, 31)

barss = load_bars(start, end, -1)
barss.tail()
```

The `load_bars` function is available in our research environment. It returns data in the following format:

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

We extract only the price data and pivot it to a wide format to calculate daily returns:

```python
pd.options.display.max_columns = 6
returns = barss.close.unstack("asset").pct_change()
returns.tail()
```

---

This yields the following result:

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

Next, we identify days with daily limit-ups. Since this is for research rather than live trading, we allow some tolerance. We define a daily limit-up (excluding Beijing Stock Exchange and ST stocks) as follows:

```python
criteria = ((returns > 0.095) & (returns < 0.105)) | 
            ((returns > 0.19)& (returns < 0.21))
zt = returns[criteria].notna().astype(int)
```

Key syntax points here include combining multiple conditions and converting `NaN` values to 0 while converting valid matches to 1.

---

`NaN` values appear because we are working with a wide table. In a wide table, some columns may not meet the condition at a specific row (date), while others do. To preserve the row structure, non-matching values become `NaN`. We then use `notna()` to convert `NaN` to `False` (0) and valid matches to `True` (1), where 1 indicates a daily limit-up.

Next, we count consecutive daily limit-ups for each asset using the following function:

```python
def process_column(series):
    g = (series.diff() != 0).cumsum()

    g_cumsum = series.groupby(g).cumsum()

    result = series.copy()
    result[g_cumsum > 1] = g_cumsum[g_cumsum > 1]
    return result
```

---

The **cleverness** of this function lies in its use of difference and cumulative sum operations. Consider the sequence: `0 0 1 1 1 0 0`. The `diff()` result is `NaN, 0, 1, 0, 0, -1, 0`. Non-zero differences indicate a change in the continuity state (either starting or ending a consecutive limit-up streak).

By applying `cumsum` to the difference sequence, we create group identifiers:

| Original Sequence | diff | diff!=0 | cumsum |
| ------ | ---- | ------- | ------ |
| 0      | NaN  | True    | 1      |
| 0      | 0    | False   | 1      |
| 1      | 1    | True    | 2      |
| 1      | 0    | False   | 2      |
| 1      | 0    | False   | 2      |
| 0      | -1   | True    | 3      |
| 0      | 0    | False   | 3      |

Treating `cumsum` as group IDs, we can use `groupby` to count non-zero values within each group, yielding the number of consecutive daily limit-ups. This is the operation performed on line 4.

**Marvelous!**

---

Finally, we apply this function:

```python
df_processed = zt.apply(process_column, axis=0)
df_processed.stack().nlargest(5)
```

We obtain the following results (partial):

| date       | asset       | Consecutive Limits |
| ---------- | ----------- | -------- |
| 2023-10-25 | ******.XSHG | 14       |
| 2023-10-24 | ******.XSHG | 13       |
| 2023-03-21 | ******.XSHE | 12       |
| 2023-10-23 | ******.XSHG | 12       |
| 2023-03-20 | ******.XSHE | 11       |

Let’s verify one case:

```python
code = "******.XSHG"

bars = barss.xs(code, level="asset")
bars["frame"] = bars.index

plot_candlestick(bars.to_records(index=False), 
                ma_groups=[5,10,20,60])
```

---

Here is the candlestick chart:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/slgf-zt-2023-10-19.jpg)

Finally, let’s encapsulate the function:

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

The Oscar for this year goes to... [Redacted]. (Even with historical data, let’s keep the main actor anonymous.)

When you don’t know where to kick, kick it into the goal! Now, go find patterns in the 14 consecutive daily limit-ups you missed last year!
