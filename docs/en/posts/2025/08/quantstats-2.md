---
title: "Arithmetic vs. Geometric Mean: Why QuantStats’ compsum Reveals the Truth"
date: 2025-08-02
slug: en/posts/tools/quantstats-2
tags: [QuantStats, Backtesting, Geometric Mean, Python]
excerpt: "QuantStats’ compsum and expected_return functions clarify why geometric mean outperforms arithmetic mean in backtesting. Learn to compare strategy efficiency across different time horizons using Python."
lang: en
translation_of: posts/tools/quantstats-2
auto_translated: true
source_sha: edc9a8d4ca212ed5226c3b3dc02f97601857d4f4
---

Assume we have built an investment strategy and obtained its daily historical **backtest** return data using a backtesting tool. The next core step is to comprehensively evaluate the strategy, including its effectiveness, risk level, and **return** performance. **QuantStats** is designed precisely for this purpose.

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261005064947-1754140031515-8bc2da28-02cd-4083-8c6b-c698c4cf5e36.png)

QuantStats is an open-source project by Ran Aroussi, a Python library for **trading strategy performance analysis** that is highly popular among quants. It has garnered **over 5.8k stars** on GitHub.

!!! tip It consists mainly of three components:

**quantstats.stats**: Calculates various performance metrics, such as the **Sharpe ratio** and **win rate**.
**quantstats.plots**: Visualizes performance, drawdowns, monthly returns, and other metrics.
**quantstats.reports**: Generates metric reports, which can be saved as HTML files.

Due to long-term lack of maintenance by the original author, newly installed versions of QuantStats—especially on Python 3.12 and higher—were nearly unusable. To address this, we stepped in to maintain it, releasing **Quantstats Reloaded**. We welcome you to install and use it!

```python
!pip install quantstats-reloaded
```

The specific quantitative basis for evaluating strategy performance lies in various metrics, such as the **Information Ratio**, **Sharpe ratio**, **max drawdown**, and **alpha** and **beta** returns. It is important to note that while the calculation of these metrics follows objective, standardized formulas with strict mathematical rules, the interpretation and evaluation of the results are subjective and often depend on the user’s risk appetite.

!!! tip 
Therefore, there is no absolute "threshold for good or bad." The key is to deeply understand the economic logic and risk-return connotations behind each metric, thereby forming independent judgments based on your own investment objectives and risk tolerance.

The Stats library within QuantStats alone contains dozens of calculation metrics. Today, we will introduce three functions from the Stats library: **compsum()**, **comp()**, and **expected_return()**. What are their uses, and how are they related?

## Basic Statistics
**1. compsum(): Converts a return sequence into a cumulative compound return sequence (cumulative product)**

```python
Function: compsum(returns)

# Parameter Introduction
returns (pd.Series, recommended)
• Return sequence, typically daily return data
Format: [0.01, -0.02, 0.03, ...] 
• Represents 1%, -2%, 3%
• Calculation Formula: (1 + returns).cumprod() - 1

# Example Usage
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
cumulative = qs.stats.compsum(returns)

# Output Result
[0.01, -0.0098, 0.0207, 0.0105, 0.0307]
```

!!! tip
The `compsum` function returns a "sequence," with a length identical to the input sequence. It can be used to "visualize" how returns evolve from an "initial state" to a "final state." It acts like a documentary, recording the ups and downs of a stock under the strategy’s execution, similar to the effect shown below.

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261005064934-1754138614424-3c94d9d1-2058-4ef3-a5d4-e1f2a5c0fab6.png)

**2. comp(): Calculates the total compound return (final cumulative return) - the total return for the entire period**

```python
Function: comp(returns)

# Parameter Introduction
returns (pd.Series, recommended)
• Return sequence
Calculation Formula: (1 + returns).prod() - 1
• Equivalent to the last value of compsum()

# Example Usage
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
total_return = qs.stats.comp(returns)
print(f"Total Return: {total_return:.4f}")

# Equivalent Calculation Method
cumulative = qs.stats.compsum(returns)
print(f"Last Value: {cumulative.iloc[-1]:.4f}")
```

!!! tip
Compared to the `compsum` function, the difference with `comp` is that it returns "a single value" rather than a sequence (as reflected in the calculation formula). This value is the last element of the sequence returned by `compsum`. Therefore, `comp` returns the final total return for a specific period.

**3. expected_return(): Calculates the expected return (geometric mean)**

```python
Function: expected_return(returns, aggregate=None, compounded=True, prepare_returns=True)

# Parameter Introduction
returns (pd.Series, recommended)
• Return sequence
aggregate (str, optional)
• Aggregation period: 'D' (daily), 'W' (weekly), 'M' (monthly), 'Q' (quarterly), 'Y' (yearly)
compounded (bool, default=True)
• Whether to use compound return calculation
prepare_returns (bool, default=True)
• Whether to preprocess data (remove NaNs, etc.)

# Example Usage
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
# Calculate daily expected return
expected_ret = qs.stats.expected_return(returns)
print(f"Daily Expected Return: {expected_ret:.4f}")

# Calculation Formula: (∏(1 + returns))^(1/n) - 1
# Geometric mean, considering the effect of compounding
```

**Suppose there are two strategies, A and B, where:**

 	
Strategy A: Has been running for 30 days, with a total cumulative return of 30% **(calculated using comp)**
Strategy B: Has been running for 25 days, with a total cumulative return of 20% **(calculated using comp)**
	
    
!!! question Comparing Strategy A and Strategy B, which one is better?
Answer: Because the "time horizons are different," you cannot directly compare 30% with 20%. It is recommended to calculate their "average daily return" to make them comparable.

	
!!! question **The calculation methods for averages are divided into "arithmetic mean" and "geometric mean." Which one is better?
Answer: Obviously, the "geometric mean"! **(calculated via `expected_return`)**. It not only considers the impact of "compounding" but also accurately reproduces the final cumulative net asset value.

    
Now, let’s generate a series of random numbers using the code below. We can generate net asset value trajectories under many rising or falling scenarios, along with the paths of their arithmetic and geometric means from start to finish.

```python
dates = pd.date_range("2021-01-01", periods=100)
# np.random.seed(78)
ret = pd.Series(np.random.normal(0, 0.02, size = 100), index=dates) * -1

df_returns = pd.DataFrame({
    "original return": ret,
    "culmulative": compsum(ret).values,
    "mean by daily return": [np.mean(ret)]*100,
    "geometric return": [expected_return(ret)] * 100,

}, index=dates)

df_net_value = pd.DataFrame({
    "daily mean": (df_returns["mean by daily return"] + 1).cumprod(),
    "geometric mean": (df_returns["geometric return"] + 1).cumprod(),
    "cumulative original": (1 + df_returns["culmulative"])
})

df_net_value.plot()

```




**We observe that whether the market is rising or falling, the blue line is always above the red line.**





![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261005065205-1754140954570-f3b2099a-7c1d-4f0d-a779-f72746745288.jpg)

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261005065228-1754141671086-ea326a34-7b55-4d94-bacb-f7a20f4f1452.png)


!!! question Why is the blue line always above the red line, regardless of market direction?
Answer: According to the inequality of arithmetic and geometric means: Arithmetic Mean ≥ Geometric Mean.


![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261005065033-1754141556739-bab818f5-1e52-49f1-b1f7-31ed70cadc62.png)



<span style="text-decoration: dashed underline #00A86B; text-decoration-thickness: 2px;">You learned the inequality of arithmetic and geometric means in high school. Do you still remember it....</span>
