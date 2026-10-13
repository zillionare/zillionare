---
title: "Portfolio Theory & Practice (1): Core Concepts & MPT"
date: 2023-12-13
slug: en/articles/investment/策略研究/mpt-1
tags: [Modern Portfolio Theory, Efficient Frontier, Portfolio Optimization, Monte Carlo]
excerpt: "Modern Portfolio Theory (MPT) by Markowitz uses math to optimize risk-return tradeoffs. This article introduces the efficient frontier, Sharpe ratios, and Monte Carlo optimization for portfolio construction."
lang: en
translation_of: articles/investment/策略研究/mpt-1
auto_translated: true
source_sha: 7c2d41b7a1538470cbfaca28c7cc351c4dd8cde1
---

Modern Portfolio Theory (MPT), proposed by Markowitz in 1952, is one of the seven foundational theories of modern finance. It uses mathematical terminology to describe concepts such as diversification and risk management, providing investors with a toolkit for constructing diversified portfolios. Specifically, assuming an investor holds multiple assets, optimization can identify the portfolio with the minimum risk for a given expected return.

All these portfolios form a curve (with the portfolio’s standard deviation on the x-axis and expected return on the y-axis), known as the **efficient frontier curve**. The upper portion of this curve is referred to as the **efficient frontier**.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/portfolio-optimisation.png)

This graph is vertically symmetric. For every point on the lower half, there is a corresponding point on the upper half with the same risk but a higher expected return. Therefore, portfolios on the lower half are **not held by any rational investor**.

Each investor selects their specific portfolio along the efficient frontier based on their risk tolerance (utility function).

Markowitz was awarded the 1990 Nobel Memorial Prize in Economic Sciences for his contributions to MPT. He strongly advocated for diversifying investment risk through portfolio construction, famously stating that “diversification is the only free lunch in investing.”

## Core Concepts
We explain the efficient frontier using the simplest case of a two-risk-asset portfolio:

$$
R_p = w_1R_1 + (1-w_1)R_2
$$

Where:

$R_p$ is the portfolio return
$W_1$ is the weight of Asset 1
$R_1$ is the return of Asset 1.

Portfolio risk is measured by variance:

$$
\sigma_p = \sqrt{w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2Cov(R_1, R_2)}\newline 
        =\sqrt{w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\rho_{1,2}\sigma_1\sigma_2}
$$

Here, $\rho_{1,2}$ is the correlation coefficient between Asset 1 and Asset 2.

When the correlation coefficient between the two assets is 1, the equation simplifies to:

$$
\sigma_p =\sqrt{w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\sigma_1\sigma_2}\newline
        =\sqrt{(w_1\sigma_1 + w_2\sigma_2)^2}\newline 
        = w_1\sigma_1 + w_2\sigma_2
$$

When the correlation coefficient between the two assets is -1:

$$
\sigma_p =\sqrt{w_1^2\sigma_1^2 + w_2^2\sigma_2^2 - 2w_1w_2\sigma_1\sigma_2}\newline
        =\sqrt{(w_1\sigma_1 - w_2\sigma_2)^2}\newline 
        = w_1\sigma_1 - w_2\sigma_2
$$

From these equations, we can see that if two assets are perfectly negatively correlated, an equal-weight allocation results in zero portfolio return, creating a risk-free portfolio. Since $\sigma_p$ equals zero, this point becomes the leftmost point on the graph.

When one asset constitutes 100% of the portfolio, it forms the top and bottom points on the graph.

In this series, we will first demonstrate how to find the optimal asset allocation using four assets, employing both Monte Carlo methods and optimization algorithms. These are lower-level approaches. Once we understand the principles, we can use third-party libraries to automate this process.

### Calculating Returns, Sharpe Ratio, and Volatility

Let’s first assign a random set of weights to observe the **return**, **Sharpe ratio**, and other parameters of the resulting portfolio. In this process, we primarily aim to understand:

1. How to fetch data
2. How to generate random weight vectors (focusing on the constraint that weights sum to 1)
3. How to calculate metrics such as the Sharpe ratio and volatility.

Assume our asset portfolio consists of:

```
600519 贵州茅台
300750 宁德时代
300059 东方财富
601398 工商银行
```

We use the following code to obtain their returns over the past year, saving them in a `returns` DataFrame:

```python
import arrow
import akshare as ak
import pandas as pd
import numpy as np
from IPython.display import display


stocks = ["600519", "300750", "300059", "601398"]

frames = {}

now = arrow.now()
start = now.shift(years = -1)
end = now.format("YYYYMMDD")
start = start.format("YYYYMMDD")

for code in stocks:
    bars = ak.stock_zh_a_hist(symbol=code, 
                              period="daily", 
                              start_date=start, 
                              end_date=end, 
                              adjust="qfq")
    
    bars.index = pd.to_datetime(bars["日期"])
    frames[code] = bars["收盘"]

prices = pd.DataFrame(frames)
returns = prices.pct_change()

returns.dropna(how='any', inplace=True)
display(returns.head().style.format('{:,.2%}'))
```

We have previously encountered this code when discussing CAPM in earlier articles.

Next, we randomly assign a weight vector (the first step of the Monte Carlo method) and calculate its Sharpe ratio:

```python
import numpy as np
from empyrical import sharpe_ratio

weights = np.array(np.random.random(4))
print('Random Weights:')
print(weights)

print('\nRebalance')
weights = weights/np.sum(weights)
print(weights)

# 生成每日每个标的对组合的贡献
weighted_returns = weights * returns
weighted_returns.head()

# 把每一行按列加总，就得到了每日资产收益
port_returns = weighted_returns.sum(axis=1)

# 然后计算组合资产的波动
cov = np.cov(port_returns.T)
port_vol = np.sqrt(np.dot(np.dot(weights, cov), weights.T)) # 0.01

# 使用 sharpe_ratio来计算夏普率
sr = sharpe_ratio(port_returns) # 0.18

print("Sharpe Ratio and Vol")
print(f"{sr:.2f} {port_vol:.2f}")
```

In the code, we first generate a random weight matrix and then normalize it (ensuring the sum of the weight matrix elements equals 1).

Some articles use log returns. However, when calculating variance, most practitioners consider geometric variance meaningless (based on Google search results).

We use the `sharpe_ratio` method from `empyrical` to calculate the Sharpe ratio. For simplicity, we set the `risk_free` rate to 0. `empyrical` is a tool developed and open-sourced by Quantopian for calculating various strategy metrics, such as Sharpe ratio, Sortino ratio, and max drawdown. Common quantitative libraries like this are introduced in the **Monopoly Quant Trading Course**.

Ultimately, we obtain the following results:

```
Random Weights:
[0.48349071 0.32903015 0.85308562 0.64038565]

Rebalance
[0.20966711 0.14268485 0.36994299 0.27770505]
Sharpe Ratio and Vol
0.72 0.01
```

We have determined that the Sharpe ratio for this portfolio is 0.72. Generally, a Sharpe ratio above 1 is considered acceptable for index or blue-chip investments; for other high-risk equity investments, it typically needs to exceed 1.8, though few assets surpass 3. In the **Monopoly Quant Trading Course**, we discuss the relationship between the Sharpe ratio and max drawdown using Monte Carlo methods—specifically, what max drawdowns are likely to occur when the Sharpe ratio is 1, when it is 2, and so on.

With all preparations complete, we will next introduce how to use the Monte Carlo method to determine the optimal allocation for the aforementioned portfolio.
