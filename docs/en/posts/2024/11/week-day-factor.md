---
title: "Best Day to Buy Stocks: Sharpe 22.5 on Friday!"
date: 2024-11-24
slug: en/posts/factor-strategy/week-day-factor
tags: [Calendar Anomaly, Timing Signal, Factor Mining, Backtest]
excerpt: "This article analyzes China A-shares CSI 1000 index data to determine the optimal weekday for entry. By backtesting buy-and-hold strategies across different days, we reveal a high-Sharpe timing signal hidden in the calendar."
lang: en
translation_of: posts/factor-strategy/week-day-factor
auto_translated: true
source_sha: e7984fd3816103f95430d7a59ff802e384fcd0b1
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/university/caltech-Annenberg_center.jpg"
---

In Lesson 12, we discussed how to expand factors (or strategies) across four dimensions: volume, price, time, and space. In the time dimension, we noted that buying at different points from Monday to Friday yields different returns. This article reveals which day offers the highest return.

The problem is defined as follows:

Assume we buy at the closing price on Monday, Tuesday, ..., Friday, hold for 1, 2, 3, 4, or 5 days, and sell at the closing price. We calculate the average return, cumulative return, and Sharpe ratio. We select the more representative CSI 1000 index as the underlying asset.

## Fetching Market Data

```python
df = pro.index_daily(**{
    "ts_code": "000852.SH"
})

df.index = pd.to_datetime(df.trade_date)
df.sort_index(ascending=True, inplace=True)
df.tail(10)
```

The data we obtain spans from January 4, 2005, to the most recent trading day. In November 2024, this yields approximately 4,800 records.

Let’s first look at its overall trend:

```python
df.close.plot()
```
<!-- BEGIN IPYNB STRIPOUT -->
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/11/中证1000-2005-2024.jpg)
<!-- END IPYNB STRIPOUT -->

If we had bought and held since January 4, 2005, we would have achieved roughly a 5x return over 19 years. Remember this number.

## Calculating Grouped Returns

Next, we calculate the returns for buying on different days and holding for various periods. There is a simple algorithm here: first, calculate the corresponding daily return for each holding period, then group by weekday to obtain the results.

First, we add a grouping flag to `df`:

```python
# Add a column to df as a grouping flag
df["weekday"] = df.index.map(lambda x: x.weekday())

# Convert numbers to more readable weekday names
df["weekday"] = df.weekday.map({
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday"
})
df = df[["close", "weekday"]]
df.tail()
```

<!-- BEGIN IPYNB STRIPOUT -->

At this point, we obtain:

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>close</th>
      <th>weekday</th>
    </tr>
    <tr>
      <th>trade_date</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2024-11-11</th>
      <td>6579.0054</td>
      <td>Monday</td>
    </tr>
    <tr>
      <th>2024-11-12</th>
      <td>6491.9723</td>
      <td>Tuesday</td>
    </tr>
    <tr>
      <th>2024-11-13</th>
      <td>6474.3941</td>
      <td>Wednesday</td>
    </tr>
    <tr>
      <th>2024-11-14</th>
      <td>6272.1911</td>
      <td>Thursday</td>
    </tr>
    <tr>
      <th>2024-11-15</th>
      <td>6125.5126</td>
      <td>Friday</td>
    </tr>
    <tr>
      <th>2024-11-18</th>
      <td>5974.5576</td>
      <td>Monday</td>
    </tr>
    <tr>
      <th>2024-11-19</th>
      <td>6130.2848</td>
      <td>Tuesday</td>
    </tr>
    <tr>
      <th>2024-11-20</th>
      <td>6250.8029</td>
      <td>Wednesday</td>
    </tr>
    <tr>
      <th>2024-11-21</th>
      <td>6262.1644</td>
      <td>Thursday</td>
    </tr>
    <tr>
      <th>2024-11-22</th>
      <td>6030.4882</td>
      <td>Friday</td>
    </tr>
  </tbody>
</table>
</div>

<!-- END IPYNB STRIPOUT -->

Next, we calculate the returns for each period.

```python
for period in range(1, 6):
    df[f"{period}D"] = df.close.pct_change(period).shift(-period)

df.tail(10)
```

<!-- BEGIN IPYNB STRIPOUT -->
At this point, we obtain:

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>close</th>
      <th>weekday</th>
      <th>1D</th>
      <th>2D</th>
      <th>3D</th>
      <th>4D</th>
      <th>5D</th>
    </tr>
    <tr>
      <th>trade_date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2024-11-11</th>
      <td>6579.0054</td>
      <td>Monday</td>
      <td>-0.013229</td>
      <td>-0.015901</td>
      <td>-0.046635</td>
      <td>-0.068930</td>
      <td>-0.091875</td>
    </tr>
    <tr>
      <th>2024-11-12</th>
      <td>6491.9723</td>
      <td>Tuesday</td>
      <td>-0.002708</td>
      <td>-0.033854</td>
      <td>-0.056448</td>
      <td>-0.079701</td>
      <td>-0.055713</td>
    </tr>
    <tr>
      <th>2024-11-13</th>
      <td>6474.3941</td>
      <td>Wednesday</td>
      <td>-0.031231</td>
      <td>-0.053886</td>
      <td>-0.077202</td>
      <td>-0.053149</td>
      <td>-0.034535</td>
    </tr>
    <tr>
      <th>2024-11-14</th>
      <td>6272.1911</td>
      <td>Thursday</td>
      <td>-0.023386</td>
      <td>-0.047453</td>
      <td>-0.022625</td>
      <td>-0.003410</td>
      <td>-0.001599</td>
    </tr>
    <tr>
      <th>2024-11-15</th>
      <td>6125.5126</td>
      <td>Friday</td>
      <td>-0.024644</td>
      <td>0.000779</td>
      <td>0.020454</td>
      <td>0.022309</td>
      <td>-0.015513</td>
    </tr>
    <tr>
      <th>2024-11-18</th>
      <td>5974.5576</td>
      <td>Monday</td>
      <td>0.026065</td>
      <td>0.046237</td>
      <td>0.048139</td>
      <td>0.009361</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2024-11-19</th>
      <td>6130.2848</td>
      <td>Tuesday</td>
      <td>0.019659</td>
      <td>0.021513</td>
      <td>-0.016279</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2024-11-20</th>
      <td>6250.8029</td>
      <td>Wednesday</td>
      <td>0.001818</td>
      <td>-0.035246</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2024-11-21</th>
      <td>6262.1644</td>
      <td>Thursday</td>
      <td>-0.036996</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2024-11-22</th>
      <td>6030.4882</td>
      <td>Friday</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>
<!-- END IPYNB STRIPOUT -->

Now, let’s calculate the cumulative returns when buying at different times:

```python
def cum_weekday_returns(df, period):
    return ((1 + df[f"{period}D"]).cumprod() - 1).reset_index(drop=True)

returns_1d = df.groupby('weekday').apply(lambda x: cum_weekday_returns(x, 1))
returns_1d.swaplevel().unstack().plot()
```

<!-- BEGIN IPYNB STRIPOUT -->
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/11/week-day-factor-cum-returns-1.jpg)
<!-- END IPYNB STRIPOUT -->

From the cumulative return chart, we can see that buying on Friday yields the highest return, approximately 5.47x. This result looks only slightly better than a simple buy-and-hold strategy. However, the capital occupancy is only 20% of that required for buy-and-hold. Therefore, if we calculate the annualized Alpha, it is significantly higher than buy-and-hold.

Of course, we have better metrics to evaluate the effectiveness of the Friday-buying strategy: the Sharpe ratio. Let’s first look at the Sharpe ratio for daily trading:

```python
from empyrical import sharpe_ratio
sharpe_ratio(df.close.pct_change())
```

The result we obtain is 0.46. Next, we calculate the Sharpe ratios for buying on different days from Monday to Friday:

```python
for tm in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"):
    returns = returns_1d.swaplevel().unstack()[tm]

    print(tm, f"{sharpe_ratio(returns):.1f}")
```

The results show that buying on Tuesday even yields a higher Sharpe ratio. However, the Sharpe ratios for buying on Wednesday and Thursday are negative, which explains why the daily buy-in Sharpe ratio is not high.

## The Ultimate Boss

Above, we only introduced the returns for buying on Friday and holding for one day. Considering that buying on Monday and Tuesday yields high Sharpe ratios, it is obvious that if we buy on Friday and hold for multiple days, the returns might be even higher. How many days should we hold to maximize returns, and how much higher will they be? **It may exceed your imagination!**

<!-- BEGIN IPYNB STRIPOUT -->
You may have read many articles and spent considerable time trying to replicate them, only to end up with nothing: either the code was incomplete, the data was inaccessible, or the article was fundamentally flawed. But we don’t want to give you such a negative experience. Like other articles on this platform, the conclusions in this article are replicable, and the data used is equally accessible to you. You can join my community and run/verify this article via the Quantide Research platform. If you verify its effectiveness, you can then copy the code to your local environment and incorporate it into your timing strategy. If the results cannot be verified, you can also leave the community.

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/logo/zsxq.png'>
<span style='font-size:0.6rem'></span>
</div>

<!-- END IPYNB STRIPOUT -->

```python
def cum_weekday_returns(df, period):
    return ((1 + df[f"{period}D"]).cumprod() - 1).reset_index(drop=True)

for period in range(1, 6):
    returns = df.groupby('weekday').apply(lambda x: cum_weekday_returns(x, period))
    returns.swaplevel().unstack().plot(title=f"Holding {period} Days")
```
