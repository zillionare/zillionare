---
title: "CAPM Explained: Risk, Beta, and Python Implementation"
date: 2023-12-13
slug: en/articles/investment/策略研究/capm
tags: [Capital Asset Pricing Model, Beta Calculation, Python Quant, Risk Premium]
excerpt: "Learn the Capital Asset Pricing Model (CAPM) and its core components: risk-free rate, market return, and beta. This guide demonstrates practical Python implementation using akshare data to calculate expected returns and visualize stock-market correlations."
lang: en
translation_of: articles/investment/策略研究/capm
auto_translated: true
source_sha: f8608d19edacee34e133b8462ff720fbf4461214
---

The Capital Asset Pricing Model (CAPM) describes the relationship between an asset’s expected return and its systematic market risk. Proposed by William Sharpe and others in the 1960s, CAPM earned Sharpe the 1990 Nobel Memorial Prize in Economic Sciences. It is widely regarded as one of the seven foundational theories in economics.

CAPM states that an asset’s expected return equals the risk-free rate plus a risk premium. The model assumes investors are rational, seeking to maximize returns while minimizing risk. Consequently, CAPM calculates the risk premium relative to the risk-free rate, allowing investors to estimate the return they should expect for a given level of risk.

## Core Concepts

### Risk-Free Rate

When investors purchase high-risk assets like stocks, their goal is to achieve returns higher than those from risk-free assets. Generally, bank deposit rates and government bond yields are considered risk-free. However, since government bond yields typically exceed bank deposit rates for the same term, we often use government bond yields as the risk-free rate.

Different maturities of government bonds have different yields. When benchmarking, it is best to match the maturity with the expected investment horizon of the risky asset. For example, if investing in highly liquid stocks with a short holding period, use the one-year government bond yield as the risk-free rate. For real estate or long-term holdings, use the five-year government bond yield.

How can we obtain government bond yields? We can use `akshare`:

```python
import akshare as ak
import arrow
import numpy as np
import random
import pandas as pd

random.seed(78)

now = arrow.now()
start = now.shift(years=-1)
end = f"{now.year}{now.month:02d}{now.day:02d}"
start = f"{start.year}{start.month:02d}{start.day:02d}"

bond = ak.bond_china_yield(start_date=start, end_date=end)
bond.set_index(keys='曲线名称', inplace=True)
bond
```

This retrieves various bond yields over the past year. We can treat the one-year average of the "China Government Bond Yield Curve" as the one-year government bond yield:

```python
rf = bond[bond.index=='中债国债收益率曲线']['1年'].mean()
print(rf)

rf = rf / 100
```

The output is 2.06. This value should be interpreted as 2.06%.

### Market Return $r_m$

The market return, denoted as $r_m$, includes all securities in the market. However, we typically use specific indices, such as the SSE 50 or CSI 300. If your investment preference is for growth stocks, you might use the CSI 1000.

### Beta ($\beta$)

Beta ($\beta$) is a metric that measures a stock’s volatility relative to the overall market (e.g., the CSI 300 index). In other words, $\beta$ represents the slope of the regression line, illustrating the relationship between market returns and individual stock returns.

In CAPM, $\beta$ describes the relationship between systematic (market) risk and an asset’s expected return. By definition, the market’s beta is 1.0. Individual stocks are ranked based on their volatility relative to the market:

*   If a stock’s Beta = 1.0, its price is perfectly correlated with the market.
*   If Beta < 1.0 (termed "defensive"), the security’s theoretical volatility is lower than the market’s.
*   If Beta > 1.0 (termed "aggressive"), the asset’s price is more volatile than the market.

## CAPM Formula

The formula is defined as follows:

$$
r_i = r_f + \beta(r_m - r_f)
$$

Where:
*   $r_i$ is the expected return of the security (individual stock).
*   $r_f$ is the risk-free rate.
*   $\beta_i$ is the beta of the security relative to the market.
*   $r_m - r_f$ is known as the risk premium.

Let’s interpret this formula with an example. If the S&P 500’s overall return is 12.4%, the risk-free rate is 0%, and Apple’s (AAPL) beta is 1.1, an investor buying AAPL would expect a 13.7% return to compensate for the additional risk taken.

To apply the CAPM model, the core task is calculating the beta of individual stocks relative to the market portfolio (index). Below, we implement this using Python.

## CAPM Implementation in Python

We use the CSI 300 as our market portfolio and extract individual stocks from it. We will randomly select 10 stocks for calculation.

### Data Acquisition

To ensure accessibility for all readers, we continue using `akshare`.

First, we retrieve the historical data for the CSI 300 over the past year:

```python
import akshare as ak

hs300 = ak.stock_zh_index_daily(symbol="sz399300")
hs300.index = pd.to_datetime(hs300["date"])
print(hs300)
```

Let’s take a quick look at the CSI 300’s performance over the past year:

```python
now = arrow.now()
year_ago = now.shift(years = -1)

year_ago = hs300[hs300.index >= np.datetime64(year_ago)].index[0]
# PRINT(YEAR_AGO)

# 计算买入并持有的收益（最近一年）
buy_price = hs300[hs300.index == year_ago].iloc[0]["close"]
buy_and_hold = hs300["close"][-1]/buy_price - 1
print(f"买入并持收益：{buy_and_hold:.2%}")

# 通过均值推算年化收益
market_returns = hs300["close"].pct_change().dropna()
market_annual = (1 + market_returns[market_returns.index >= year_ago].mean()) ** 242 - 1
print(f"年化收益：{market_annual:.2%}")
```

As observed, over the past year, the CSI 300’s return using a buy-and-hold strategy was -4.22%. If we calculate the mean daily return and annualize it, the return is -3.31%. The difference is negligible.

Next, we retrieve the constituents of the CSI 300 to extract individual stocks for testing:

```python
import akshare as ak
index_stock_cons_df = ak.index_stock_cons(symbol="399300")
print(index_stock_cons_df)
```

Then, we randomly select 10 stocks, retrieve their market data, and calculate daily returns:

```python
np.random.seed(78)

stocks = random.sample(index_stock_cons_df['品种代码'].to_list(), 10)

frames = {}

now = arrow.now()
start = now.shift(years = -1)
end = now.format("YYYYMMDD")
start = start.format("YYYYMMDD")

# 获取 10 支股票的行情数据
for code in stocks:
    bars = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start, end_date=end, adjust="qfq")
    bars.index = pd.to_datetime(bars["日期"])
    frames[code] = bars["收盘"]
    
# 与指数行情数据合并
start = np.datetime64(now.shift(years = -1))
frames["399300"] = hs300[hs300.index >= start]["close"]

df = pd.DataFrame(frames)

# 计算每日收益
returns = df.pct_change()

# 如果存在 NAN，则后面的回归法将无法聚合
returns.dropna(how='any', inplace=True)
returns.style.format('{:,.2%}')
```

### Calculating Beta

We will calculate beta using two methods: regression and covariance.

#### Regression Method

NumPy provides a `polyfit` function for polynomial fitting. When using a first-order fit (linear regression), the resulting coefficient is the desired beta.

```python
cols = df.columns
betas = {}
for name in cols:
    beta, alpha = np.polyfit(returns[name], returns["399300"], deg=1)
    print(name, f"{beta:.2%} {alpha:.2%}")
    betas[name] = beta
```

The results show that one stock has a positive alpha and a beta exceeding 10% (likely meaning high beta contribution, though the text says "10% above beta收益" which is ambiguous, but context implies high beta).

Now, let’s determine the expected return if we were to buy this stock:

Note that our `risk_free` is an annualized yield. Therefore, the expected return we calculate should also be annualized (or both should be converted to daily rates):

```python
code = "002756"
beta = betas[code]

# 回归法得到的预期收益
expected_return = rf + beta * (market_annual - rf)
print(f"code beta: {beta:.2f}, Er: {expected_return:.2%}")
```

We ultimately find that stock 002756 has a beta of 0.11, with an expected annual return of approximately 1.51%.

#### Covariance Method

```python
params = {}

for name in cols:
    cov = np.cov(returns["399300"], returns[name])
    beta = cov[0,1]/cov[1,1]
    
    expected_return = rf + beta * (market_annual - rf)
    print(f"{name} beta: {beta:.2%}, Er: {expected_return:.2%}")
    params[name] = beta
    
beta = params[code]

# 回归法得到的预期收益
expected_return = rf + beta * (market_annual - rf)
print(f"code beta: {beta:.2f}, Er: {expected_return:.2%}")
```

This yields a beta of 0.11 for 002756 and an annualized expected return of 1.51%.

## Visualization

We can visualize the correlation between individual stocks and the CSI 300’s price movements to gain a more intuitive understanding.

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots


ci = sorted(set(returns[code].index).intersection(set(returns["399300"].index)))

y = returns[code][ci]
x = returns["399300"][ci]

df = pd.DataFrame({
    "沪深300": sorted(returns["399300"][ci]),
    "标的": sorted(returns[code][ci])
})

fig = make_subplots(
    rows=1,
    cols=2
)

fig.add_trace(go.Scatter(x=df["沪深300"], y=df["标的"]))
fig2 = px.line(df)
fig.add_trace(fig2["data"][0], row=1, col=2)
fig.add_trace(fig2["data"][1], row=1, col=2)

fig['layout']['xaxis']['title']='沪深300'
fig['layout']['yaxis']['title']='标的'

fig.show()
```

The final plot is shown below:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/capm-q-plot.png)
