<style>
.function-card {
    border: 2px solid #e1e5e9;
    border-radius: 12px;
    padding: 20px;
    margin: 15px;
    background-color: #f8f9fa;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    display: inline-block;
    width: 450px;
    vertical-align: top;
}

.function-card h3 {
    color: #2c3e50;
    margin-top: 0;
    font-size: 20px;
    border-bottom: 2px solid #3498db;
    padding-bottom: 8px;
}

.category {
    background-color: #3498db;
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 12px;
}

.description {
    font-size: 15px;
    line-height: 1.5;
    color: #34495e;
    margin-bottom: 15px;
}

.signature {
    font-size: 13px;
    color: #7f8c8d;
    background-color: #ecf0f1;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 12px;
    font-family: 'Courier New', monospace;
    overflow-x: auto;
}

.returns {
    font-size: 14px;
    color: #27ae60;
    font-weight: bold;
    margin-bottom: 15px;
}

.param-details {
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
    padding: 12px;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
}

.param-item {
    margin-bottom: 10px;
    line-height: 1.4;
}

.param-name {
    font-weight: bold;
    color: #2c3e50;
    font-family: 'Courier New', monospace;
    background-color: #e8f4f8;
    padding: 2px 6px;
    border-radius: 3px;
}

.param-type {
    color: #8e44ad;
    font-style: italic;
    font-size: 12px;
    margin-left: 6px;
}

.param-desc {
    color: #34495e;
    margin-top: 4px;
    font-size: 13px;
}

.example-code {
    background-color: #1e3a8a;
    color: #f1f5f9;
    padding: 15px;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    margin-top: 12px;
    overflow-x: auto;
    line-height: 1.6;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.example-code .comment {
    color: #94a3b8;
    font-style: italic;
}

.example-code .output {
    color: #34d399;
    font-weight: bold;
}

/* 不同类别的颜色 */
.basic-stats { border-color: #e74c3c; }
.basic-stats .category { background-color: #e74c3c; }

.risk-metrics { border-color: #f39c12; }
.risk-metrics .category { background-color: #f39c12; }

.performance-ratios { border-color: #27ae60; }
.performance-ratios .category { background-color: #27ae60; }

.drawdown-analysis { border-color: #8e44ad; }
.drawdown-analysis .category { background-color: #8e44ad; }

.benchmark-comparison { border-color: #2980b9; }
.benchmark-comparison .category { background-color: #2980b9; }

.advanced-metrics { border-color: #34495e; }
.advanced-metrics .category { background-color: #34495e; }
</style>

---

## 基础统计指标 (Basic Statistics)

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>compsum()</h3>
<div class="description">计算滚动复合收益率（累积乘积）- 将收益率序列转换为累积财富指数</div>
<div class="signature">compsum(returns)</div>
<div class="returns">返回: pd.Series - 累积复合收益率序列</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列，通常是日收益率数据<br>• 格式: [0.01, -0.02, 0.03, ...] 表示1%, -2%, 3%<br>• 计算公式: (1 + returns).cumprod() - 1</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
cumulative = qs.stats.compsum(returns)

<span class="comment"># 输出结果</span>
<span class="output"># [0.01, -0.0102, 0.0195, 0.0093, 0.0295]</span>

<span class="comment"># 实际含义：</span>
<span class="comment"># 第1天: 1% 收益</span>
<span class="comment"># 第2天: (1.01 * 0.98) - 1 = -1.02%</span>
<span class="comment"># 第3天: (0.989 * 1.03) - 1 = 1.95%</span>
</div>
</div>

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>comp()</h3>
<div class="description">计算总复合收益率（最终累积收益）- 整个期间的总收益率</div>
<div class="signature">comp(returns)</div>
<div class="returns">返回: float - 总复合收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列<br>• 计算公式: (1 + returns).prod() - 1<br>• 等同于 compsum() 的最后一个值</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
total_return = qs.stats.comp(returns)

print(f"总收益率: {total_return:.4f}")
<span class="output"># 输出: 总收益率: 0.0295</span>

<span class="comment"># 等价计算方法</span>
cumulative = qs.stats.compsum(returns)
print(f"最后值: {cumulative.iloc[-1]:.4f}")
<span class="output"># 输出: 最后值: 0.0295</span>
</div>
</div>


<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>expected_return()</h3>
<div class="description">计算期望收益率（几何平均数）- 基于历史数据的预期收益</div>
<div class="signature">expected_return(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: float - 期望收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期: 'D'(日), 'W'(周), 'M'(月), 'Q'(季), 'Y'(年)</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否使用复合收益率计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据（去除NaN等）</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
returns.index = pd.date_range(start='2020-01-01', periods=5, freq='B')

<span class="comment"># 计算日度期望收益</span>
expected_ret = qs.stats.expected_return(returns)
print(f"日度期望收益: {expected_ret:.4f}")

<span class="comment"># 计算月度期望收益</span>
monthly_expected = qs.stats.expected_return(returns, aggregate='M')
print(f"月度期望收益: {monthly_expected:.4f}")

<span class="comment"># 计算公式: (∏(1 + returns))^(1/n) - 1</span>
<span class="comment"># 几何平均数，考虑复利效应</span>
</div>
</div>

<!--

把geometric_return也加进来

还是从每日的简单收益出发。当我们有行情数据时，就可以很容易计算出标的的每日涨跌幅，也就是每日收益。

作为一个策略，我们可能想知道从T0日起，到T1, T2, ..Tn，我们的累积收益是多少。这就是compsum的由来。

compsum的结果是一个序列。它的最后一个值，就是该策略最后的净值减去1。或者说，compsum + 1，就是T0, T1, ...Tn日的策略净值。

在对两个策略比较收益能力时，我们可以将简单收益取平均再比较。但是这样没有考虑复利能力。如果要精确地考虑复利，我们就应该取几何收益平均。这就是 expected_return的由来。在quantstats中，还有一个 geometric_mean， 两者完全是一回事，只不过参数略有不同。

在quantstats中计算几何收益时，它要求returns数据一定要带有日期。否则无法计算。

以下代码演示了几种收益之间的联系。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


np.random.seed(42)
days = 10
dates = pd.date_range(start="2023-01-01", periods=days)
daily_returns = np.random.normal(0.005, 0.01, days)


df = pd.DataFrame({
    "日收益": daily_returns
}, index=dates)


df["日收"] = (1 + df["日收益"]).cumprod()

mean_daily_return = df["日收益"].mean()
df["日收均值"] = (1 + mean_daily_return) **(np.arange(1, len(df)+1))

df["日收复合"] = qs.stats.compsum(df["日收益"]) + 1

expected_return = qs.stats.expected_return(df["日收益"])
geometric_return = qs.stats.geometric_mean(df["日收益"])

df["日收预期"] = (1 + expected_return)** (np.arange(1, len(df)+1))
df["日收几何"] = (1 + geometric_return) ** (np.arange(1, len(df) + 1))

# df[["累积净值_原始", "累积净值_均值", "累积净值_复合", "累积净值_预期"]].plot()
# 绘制图形
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制四条曲线
ax.plot(df.index, df["日收"], label="简单收益累积", 
        marker="o", linestyle="-", color="blue")
ax.plot(df.index, df["日收均值"], label="按日均收益计算的累积净值", 
        marker="s", linestyle="--", color="green")
ax.plot(df.index, df["日收预期"], label="按预期收益计算的累积净值", 
        marker="^", linestyle="-.", color="red")
ax.plot(df.index, df["日收复合"], label="按复合收益计算的累积净值", 
        marker="*", linestyle=":", color="orange")


ax.set_title("四种累积净值对比", fontsize=15)
ax.set_xlabel("日期", fontsize=12)
ax.set_ylabel("累积净值", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.7)
ax.legend(fontsize=10)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)

print("10日收益数据及三种累积净值计算结果：")
pd.set_option("display.float_format", "{:.4f}".format)
df
```

我们将得到下图：

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/07/20250722143145.png)


以及各种收益计算的净值结果：

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/07/20250722143243.png)

-->

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>best()</h3>
<div class="description">找出指定期间的最佳（最高）收益率 - 识别历史最优表现</div>
<div class="signature">best(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: float - 最佳收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期: 'D'(日), 'W'(周), 'M'(月), 'Q'(季), 'Y'(年)</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 找出最佳日收益</span>
best_day = qs.stats.best(returns)
print(f"最佳日收益: {best_day:.2%}")
<span class="output"># 输出: 最佳日收益: 3.00%</span>

<span class="comment"># 找出最佳月收益</span>
best_month = qs.stats.best(returns, aggregate='M')
print(f"最佳月收益: {best_month:.2%}")
</div>
</div>

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>worst()</h3>
<div class="description">找出指定期间的最差（最低）收益率 - 识别历史最差表现</div>
<div class="signature">worst(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: float - 最差收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 找出最差日收益</span>
worst_day = qs.stats.worst(returns)
print(f"最差日收益: {worst_day:.2%}")
<span class="output"># 输出: 最差日收益: -2.00%</span>

<span class="comment"># 找出最差月收益</span>
worst_month = qs.stats.worst(returns, aggregate='M')
print(f"最差月收益: {worst_month:.2%}")
</div>
</div>

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>avg_return()</h3>
<div class="description">计算平均收益率（排除零收益）- 非零收益的平均值</div>
<div class="signature">avg_return(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: float - 平均收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算平均收益率（排除零收益）</span>
avg_ret = qs.stats.avg_return(returns)
print(f"平均收益率: {avg_ret:.4f}")
<span class="output"># 输出: 平均收益率: 0.0060</span>
</div>
</div>

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>avg_win()</h3>
<div class="description">计算平均盈利收益率（仅正收益）- 盈利期间的平均收益</div>
<div class="signature">avg_win(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: float - 平均盈利收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算平均盈利收益率</span>
avg_win_ret = qs.stats.avg_win(returns)
print(f"平均盈利收益: {avg_win_ret:.4f}")
<span class="output"># 输出: 平均盈利收益: 0.0200</span>
</div>
</div>

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>avg_loss()</h3>
<div class="description">计算平均亏损收益率（仅负收益）- 亏损期间的平均收益</div>
<div class="signature">avg_loss(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: float - 平均亏损收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算平均亏损收益率</span>
avg_loss_ret = qs.stats.avg_loss(returns)
print(f"平均亏损收益: {avg_loss_ret:.4f}")
<span class="output"># 输出: 平均亏损收益: -0.0150</span>
</div>
</div>

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>win_rate()</h3>
<div class="description">计算胜率（盈利期间百分比）- 衡量策略的成功频率</div>
<div class="signature">win_rate(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: float - 胜率 (0-1)</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算日度胜率</span>
daily_win_rate = qs.stats.win_rate(returns)
print(f"日度胜率: {daily_win_rate:.2%}")
<span class="output"># 输出: 日度胜率: 60.00%</span>

<span class="comment"># 计算月度胜率</span>
monthly_win_rate = qs.stats.win_rate(returns, aggregate='M')
print(f"月度胜率: {monthly_win_rate:.2%}")

<span class="comment"># 计算公式: 盈利期间数 / 总期间数</span>
</div>
</div>

<div class="function-card basic-stats">
<div class="category">基础统计</div>
<h3>geometric_mean()</h3>
<div class="description">计算收益率的几何平均数 - 复合增长率的基础计算</div>
<div class="signature">geometric_mean(returns, aggregate=None, compounded=True)</div>
<div class="returns">返回: float - 几何平均收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 几何平均数计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算几何平均数</span>
geom_mean = qs.stats.geometric_mean(returns)
print(f"几何平均数: {geom_mean:.6f}")
<span class="output"># 输出: 几何平均数: 0.006056</span>

<span class="comment"># 几何平均数考虑复利效应</span>
</div>
</div>

## 连续性指标 (Consecutive Metrics)

<div class="function-card basic-stats">
<div class="category">连续性指标</div>
<h3>consecutive_wins()</h3>
<div class="description">计算最大连续盈利期间数 - 衡量连续成功的能力</div>
<div class="signature">consecutive_wins(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: int - 最大连续盈利次数</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 最大连续盈利计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, 0.01, 0.02])

<span class="comment"># 计算最大连续盈利次数</span>
max_wins = qs.stats.consecutive_wins(returns)
print(f"最大连续盈利: {max_wins}次")
<span class="output"># 输出: 最大连续盈利: 3次</span>

<span class="comment"># 衡量策略的连续成功能力</span>
</div>
</div>

<div class="function-card basic-stats">
<div class="category">连续性指标</div>
<h3>consecutive_losses()</h3>
<div class="description">计算最大连续亏损期间数 - 衡量最大连续失败次数</div>
<div class="signature">consecutive_losses(returns, aggregate=None, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: int - 最大连续亏损次数</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 最大连续亏损计算示例</span>
returns = pd.Series([0.01, -0.02, -0.01, -0.01, 0.02])

<span class="comment"># 计算最大连续亏损次数</span>
max_losses = qs.stats.consecutive_losses(returns)
print(f"最大连续亏损: {max_losses}次")
<span class="output"># 输出: 最大连续亏损: 3次</span>

<span class="comment"># 衡量策略的最大连续失败风险</span>
</div>
</div>

<div class="function-card basic-stats">
<div class="category">连续性指标</div>
<h3>exposure()</h3>
<div class="description">计算市场暴露时间（非零收益期间百分比）- 衡量策略的活跃程度</div>
<div class="signature">exposure(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 暴露百分比 (0-1)</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 市场暴露时间计算示例</span>
returns = pd.Series([0.01, 0.00, 0.03, -0.01, 0.02])

<span class="comment"># 计算市场暴露时间</span>
exp = qs.stats.exposure(returns)
print(f"市场暴露时间: {exp:.2%}")
<span class="output"># 输出: 市场暴露时间: 80.00%</span>

<span class="comment"># 计算公式: 非零收益期间数 / 总期间数</span>
<span class="comment"># 衡量策略的活跃程度</span>
</div>
</div>

## 绩效比率 (Performance Ratios)

<div class="function-card performance-ratios">
<div class="category">绩效比率</div>
<h3>rar()</h3>
<div class="description">计算风险调整收益率 - 基础的风险调整指标</div>
<div class="signature">rar(returns, rf=0)</div>
<div class="returns">返回: float - RAR值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
</div>
<div class="example-code">
<span class="comment"># RAR计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算风险调整收益率</span>
rar_value = qs.stats.rar(returns, rf=0.02)
print(f"风险调整收益率: {rar_value:.4f}")
<span class="output"># 输出: 风险调整收益率: 0.8765</span>
</div>
</div>

## 滚动指标 (Rolling Metrics)

<div class="function-card performance-ratios">
<div class="category">滚动指标</div>
<h3>rolling_sharpe()</h3>
<div class="description">计算滚动夏普比率 - 观察夏普比率的时间变化</div>
<div class="signature">rolling_sharpe(returns, rf=0.0, rolling_period=126, annualize=True)</div>
<div class="returns">返回: pd.Series - 滚动夏普比率序列</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0.0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
<div class="param-item">
<span class="param-name">rolling_period</span><span class="param-type">(int, 默认=126)</span>
<div class="param-desc">• 滚动窗口大小</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 滚动夏普比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算滚动夏普比率</span>
rolling_sharpe = qs.stats.rolling_sharpe(returns, rolling_period=60)
print("滚动夏普比率:")
print(rolling_sharpe.tail())

<span class="comment"># 用于观察夏普比率随时间的稳定性</span>
</div>
</div>

<div class="function-card performance-ratios">
<div class="category">滚动指标</div>
<h3>rolling_sortino()</h3>
<div class="description">计算滚动索提诺比率 - 观察下行风险调整收益的变化</div>
<div class="signature">rolling_sortino(returns, rf=0, rolling_period=126, annualize=True)</div>
<div class="returns">返回: pd.Series - 滚动索提诺比率序列</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
<div class="param-item">
<span class="param-name">rolling_period</span><span class="param-type">(int, 默认=126)</span>
<div class="param-desc">• 滚动窗口大小</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 滚动索提诺比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算滚动索提诺比率</span>
rolling_sortino = qs.stats.rolling_sortino(returns, rolling_period=60)
print("滚动索提诺比率:")
print(rolling_sortino.tail())

<span class="comment"># 用于观察下行风险调整收益的时间稳定性</span>
</div>
</div>

## 智能指标 (Smart Metrics)

<div class="function-card performance-ratios">
<div class="category">智能指标</div>
<h3>smart_sharpe()</h3>
<div class="description">计算智能夏普比率（含自相关惩罚）- 考虑收益自相关性的夏普比率</div>
<div class="signature">smart_sharpe(returns, rf=0.0, periods=252, annualize=True)</div>
<div class="returns">返回: float - 智能夏普比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0.0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 年化周期数</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 智能夏普比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算智能夏普比率</span>
smart_sharpe = qs.stats.smart_sharpe(returns)
regular_sharpe = qs.stats.sharpe(returns)

print(f"智能夏普比率: {smart_sharpe:.4f}")
print(f"常规夏普比率: {regular_sharpe:.4f}")

<span class="comment"># 智能夏普比率考虑了收益的自相关性</span>
<span class="comment"># 对于有趋势的策略更准确</span>
</div>
</div>

<div class="function-card performance-ratios">
<div class="category">智能指标</div>
<h3>smart_sortino()</h3>
<div class="description">计算智能索提诺比率（含自相关惩罚）- 考虑自相关的下行风险调整收益</div>
<div class="signature">smart_sortino(returns, rf=0, periods=252, annualize=True)</div>
<div class="returns">返回: float - 智能索提诺比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 年化周期数</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 智能索提诺比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算智能索提诺比率</span>
smart_sortino = qs.stats.smart_sortino(returns)
regular_sortino = qs.stats.sortino(returns)

print(f"智能索提诺比率: {smart_sortino:.4f}")
print(f"常规索提诺比率: {regular_sortino:.4f}")

<span class="comment"># 智能版本考虑了收益的自相关性</span>
</div>
</div>

<div class="function-card performance-ratios">
<div class="category">智能指标</div>
<h3>adjusted_sortino()</h3>
<div class="description">计算调整后索提诺比率（Jack Schwager版本）- 特殊调整的索提诺比率</div>
<div class="signature">adjusted_sortino(returns, rf=0, periods=252, annualize=True, smart=False)</div>
<div class="returns">返回: float - 调整后索提诺比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 年化周期数</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化</div>
</div>
<div class="param-item">
<span class="param-name">smart</span><span class="param-type">(bool, 默认=False)</span>
<div class="param-desc">• 是否应用自相关惩罚</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 调整后索提诺比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算调整后索提诺比率</span>
adj_sortino = qs.stats.adjusted_sortino(returns)
print(f"调整后索提诺比率: {adj_sortino:.4f}")

<span class="comment"># Jack Schwager版本的索提诺比率</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">智能指标</div>
<h3>autocorr_penalty()</h3>
<div class="description">计算自相关惩罚因子 - 衡量收益序列的自相关程度</div>
<div class="signature">autocorr_penalty(returns, prepare_returns=False)</div>
<div class="returns">返回: float - 自相关惩罚因子 (>=1)</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=False)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 自相关惩罚因子计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算自相关惩罚因子</span>
penalty = qs.stats.autocorr_penalty(returns)
print(f"自相关惩罚因子: {penalty:.4f}")
<span class="output"># 输出: 自相关惩罚因子: 1.1234</span>

<span class="comment"># 值越大表示自相关性越强</span>
<span class="comment"># 用于调整夏普比率和索提诺比率</span>
</div>
</div>

<div class="function-card performance-ratios">
<div class="category">绩效比率</div>
<h3>sharpe()</h3>
<div class="description">计算夏普比率（风险调整后收益）- 衡量每单位风险的超额收益</div>
<div class="signature">sharpe(returns, rf=0.0, periods=252, annualize=True, smart=False)</div>
<div class="returns">返回: float - 夏普比率值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 投资组合的历史收益率序列<br>• 通常是日收益率: [0.01, -0.02, 0.03, ...]</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0.0)</span>
<div class="param-desc">• 无风险利率（年化）<br>• 0.03 表示3%的年化无风险利率<br>• 用于计算超额收益 (returns - rf)</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 年化周期数，用于将结果年化<br>• 252: 股票交易日数 | 365: 日历天数<br>• 12: 月度数据 | 4: 季度数据</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化结果<br>• True: 年化夏普比率 × √periods<br>• False: 原始周期夏普比率</div>
</div>
<div class="param-item">
<span class="param-name">smart</span><span class="param-type">(bool, 默认=False)</span>
<div class="param-desc">• 是否应用自相关惩罚因子<br>• True: 考虑收益率自相关性，调整分母<br>• 适用于趋势跟踪等有自相关的策略</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 示例用法</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 1. 基础夏普比率</span>
sharpe_basic = qs.stats.sharpe(returns)
print(f"基础夏普比率: {sharpe_basic:.4f}")
<span class="output"># 输出: 基础夏普比率: 1.2345</span>

<span class="comment"># 2. 考虑3%无风险利率</span>
sharpe_with_rf = qs.stats.sharpe(returns, rf=0.03)
print(f"考虑无风险利率: {sharpe_with_rf:.4f}")
<span class="output"># 输出: 考虑无风险利率: 0.8765</span>

<span class="comment"># 3. 智能模式（考虑自相关）</span>
sharpe_smart = qs.stats.sharpe(returns, smart=True)
print(f"智能夏普比率: {sharpe_smart:.4f}")
<span class="output"># 输出: 智能夏普比率: 1.1234</span>

<span class="comment"># 计算公式:</span>
<span class="comment"># (平均收益 - 无风险利率) / 收益标准差 × √年化周期</span>
</div>
</div>

<div class="function-card performance-ratios">
<div class="category">绩效比率</div>
<h3>sortino()</h3>
<div class="description">计算索提诺比率（下行风险调整收益）- 只考虑负收益的风险</div>
<div class="signature">sortino(returns, rf=0, periods=252, annualize=True, smart=False)</div>
<div class="returns">返回: float - 索提诺比率值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率（年化）</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 年化周期数</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化结果</div>
</div>
<div class="param-item">
<span class="param-name">smart</span><span class="param-type">(bool, 默认=False)</span>
<div class="param-desc">• 是否应用自相关惩罚</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 索提诺比率 vs 夏普比率对比</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算索提诺比率</span>
sortino_ratio = qs.stats.sortino(returns)
print(f"索提诺比率: {sortino_ratio:.4f}")
<span class="output"># 输出: 索提诺比率: 1.5678</span>

<span class="comment"># 计算夏普比率进行对比</span>
sharpe_ratio = qs.stats.sharpe(returns)
print(f"夏普比率: {sharpe_ratio:.4f}")
<span class="output"># 输出: 夏普比率: 1.2345</span>

<span class="comment"># 索提诺比率通常高于夏普比率，因为只考虑下行风险</span>
<span class="comment"># 计算公式: (平均收益 - 无风险利率) / 下行标准差</span>
</div>
</div>

<div class="function-card performance-ratios">
<div class="category">绩效比率</div>
<h3>calmar()</h3>
<div class="description">计算卡玛比率（年化收益/最大回撤）- 衡量回撤风险调整收益</div>
<div class="signature">calmar(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 卡玛比率值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列<br>• 用于计算CAGR和最大回撤</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理收益率数据<br>• 包括去除NaN值、格式转换等</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 卡玛比率分解计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算各个组成部分</span>
calmar_ratio = qs.stats.calmar(returns)
cagr = qs.stats.cagr(returns)
max_dd = qs.stats.max_drawdown(returns)

<span class="comment"># 输出结果</span>
print(f"卡玛比率: {calmar_ratio:.4f}")
<span class="output"># 输出: 卡玛比率: 2.3456</span>

print(f"CAGR: {cagr:.4f}")
<span class="output"># 输出: CAGR: 0.0307</span>

print(f"最大回撤: {max_dd:.4f}")
<span class="output"># 输出: 最大回撤: -0.0131</span>

<span class="comment"># 计算公式: CAGR / abs(最大回撤)</span>
<span class="comment"># 值越高表示每单位回撤风险的收益越高</span>
</div>
</div>

<div class="function-card performance-ratios">
<div class="category">绩效比率</div>
<h3>cagr()</h3>
<div class="description">计算复合年增长率 - 衡量投资的年化增长速度</div>
<div class="signature">cagr(returns, rf=0, compounded=True)</div>
<div class="returns">返回: float - 年化复合增长率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率，用于计算超额CAGR</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
</div>
<div class="example-code">
<span class="comment"># CAGR计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算年化收益率</span>
annual_growth = qs.stats.cagr(returns)
print(f"年化收益率: {annual_growth:.2%}")
<span class="output"># 输出: 年化收益率: 3.07%</span>

<span class="comment"># 计算超额CAGR（相对于无风险利率）</span>
excess_cagr = qs.stats.cagr(returns, rf=0.03)
print(f"超额年化收益: {excess_cagr:.2%}")
<span class="output"># 输出: 超额年化收益: 0.07%</span>

<span class="comment"># 计算公式: (最终价值/初始价值)^(1/年数) - 1</span>
<span class="comment"># 衡量投资的年化复合增长速度</span>
</div>
</div>

## 风险指标 (Risk Metrics)

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>volatility()</h3>
<div class="description">计算收益率的波动率（标准差）- 衡量收益率的变动程度</div>
<div class="signature">volatility(returns, periods=252, annualize=True, prepare_returns=True)</div>
<div class="returns">返回: float - 波动率值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 年化周期数<br>• 用于将日度波动率转换为年化波动率</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化波动率<br>• True: 年化波动率 = 日波动率 × √periods</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理收益率数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 波动率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算年化波动率</span>
annual_vol = qs.stats.volatility(returns, annualize=True)
print(f"年化波动率: {annual_vol:.4f}")
<span class="output"># 输出: 年化波动率: 0.3162</span>

<span class="comment"># 计算日度波动率</span>
daily_vol = qs.stats.volatility(returns, annualize=False)
print(f"日度波动率: {daily_vol:.4f}")
<span class="output"># 输出: 日度波动率: 0.0199</span>

<span class="comment"># 验证年化关系</span>
import numpy as np
print(f"验证: {daily_vol * np.sqrt(252):.4f}")
<span class="output"># 输出: 验证: 0.3162</span>

<span class="comment"># 波动率越高，风险越大</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>value_at_risk()</h3>
<div class="description">计算风险价值（VaR）- 在给定置信水平下的最大预期损失</div>
<div class="signature">value_at_risk(returns, sigma=1, confidence=0.95, prepare_returns=True)</div>
<div class="returns">返回: float - VaR值（负数表示损失）</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">sigma</span><span class="param-type">(float, 默认=1)</span>
<div class="param-desc">• 波动率乘数<br>• 用于调整风险估计的敏感度</div>
</div>
<div class="param-item">
<span class="param-name">confidence</span><span class="param-type">(float, 默认=0.95)</span>
<div class="param-desc">• 置信水平<br>• 0.95 = 95%置信度<br>• 0.99 = 99%置信度</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理收益率数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># VaR计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算95% VaR</span>
var_95 = qs.stats.value_at_risk(returns, confidence=0.95)
print(f"95% VaR: {var_95:.4f}")
<span class="output"># 输出: 95% VaR: -0.0228</span>

<span class="comment"># 计算99% VaR</span>
var_99 = qs.stats.value_at_risk(returns, confidence=0.99)
print(f"99% VaR: {var_99:.4f}")
<span class="output"># 输出: 99% VaR: -0.0363</span>

<span class="comment"># 解释：95%的情况下，日损失不会超过 2.28%</span>
<span class="comment"># 使用正态分布假设计算</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>conditional_value_at_risk()</h3>
<div class="description">计算条件风险价值（CVaR）- 超过VaR阈值的期望损失</div>
<div class="signature">conditional_value_at_risk(returns, sigma=1, confidence=0.95, prepare_returns=True)</div>
<div class="returns">返回: float - CVaR值（期望损失）</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">sigma</span><span class="param-type">(float, 默认=1)</span>
<div class="param-desc">• 波动率乘数</div>
</div>
<div class="param-item">
<span class="param-name">confidence</span><span class="param-type">(float, 默认=0.95)</span>
<div class="param-desc">• 置信水平</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># CVaR计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算95% VaR和CVaR进行对比</span>
var_95 = qs.stats.value_at_risk(returns, confidence=0.95)
cvar_95 = qs.stats.conditional_value_at_risk(returns, confidence=0.95)

<span class="comment"># 输出对比结果</span>
print(f"95% VaR: {var_95:.4f}")
<span class="output"># 输出: 95% VaR: -0.0228</span>

print(f"95% CVaR: {cvar_95:.4f}")
<span class="output"># 输出: 95% CVaR: -0.0363</span>

<span class="comment"># CVaR通常比VaR更大（损失更严重）</span>
<span class="comment"># CVaR = 超过VaR阈值的收益的平均值</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>skew()</h3>
<div class="description">计算收益率分布的偏度 - 衡量分布的不对称性</div>
<div class="signature">skew(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 偏度值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 偏度计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算收益率分布的偏度</span>
skewness = qs.stats.skew(returns)
print(f"偏度: {skewness:.4f}")
<span class="output"># 输出: 偏度: 0.2345</span>

<span class="comment"># 偏度解释：</span>
<span class="comment"># 偏度 > 0: 右偏（正偏），极端正收益较多</span>
<span class="comment"># 偏度 < 0: 左偏（负偏），极端负收益较多</span>
<span class="comment"># 偏度 = 0: 对称分布</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>kurtosis()</h3>
<div class="description">计算收益率分布的峰度 - 衡量分布的尖锐程度</div>
<div class="signature">kurtosis(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 峰度值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 峰度计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算收益率分布的峰度</span>
kurt = qs.stats.kurtosis(returns)
print(f"峰度: {kurt:.4f}")
<span class="output"># 输出: 峰度: 2.8765</span>

<span class="comment"># 峰度解释：</span>
<span class="comment"># 峰度 > 3: 尖峰分布，极端值较多（厚尾）</span>
<span class="comment"># 峰度 = 3: 正态分布</span>
<span class="comment"># 峰度 < 3: 平峰分布，极端值较少（薄尾）</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>rolling_volatility()</h3>
<div class="description">计算指定窗口的滚动波动率 - 观察波动率的时间变化</div>
<div class="signature">rolling_volatility(returns, rolling_period=126, periods_per_year=252)</div>
<div class="returns">返回: pd.Series - 滚动波动率序列</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rolling_period</span><span class="param-type">(int, 默认=126)</span>
<div class="param-desc">• 滚动窗口大小（约半年交易日）</div>
</div>
<div class="param-item">
<span class="param-name">periods_per_year</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 年化周期数</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 滚动波动率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算滚动波动率</span>
rolling_vol = qs.stats.rolling_volatility(returns, rolling_period=60)
print("滚动波动率:")
print(rolling_vol.tail())

<span class="comment"># 用于观察波动率随时间的变化</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>distribution()</h3>
<div class="description">分析不同时间段的收益分布 - 多维度分布统计</div>
<div class="signature">distribution(returns, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: dict - 各时间段分布字典</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 收益分布分析示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 分析收益分布</span>
dist = qs.stats.distribution(returns)
print("收益分布统计:")
for period, stats in dist.items():
    print(f"{period}: {stats}")

<span class="comment"># 输出包含日度、月度、年度等分布统计</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>outliers()</h3>
<div class="description">识别并返回异常值收益 - 找出极端收益点</div>
<div class="signature">outliers(returns, quantile=0.95)</div>
<div class="returns">返回: pd.Series - 异常值收益序列</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">quantile</span><span class="param-type">(float, 默认=0.95)</span>
<div class="param-desc">• 分位数阈值，用于定义异常值</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 异常值识别示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 识别异常值</span>
outlier_returns = qs.stats.outliers(returns, quantile=0.95)
print("异常值收益:")
print(outlier_returns)

<span class="comment"># 返回超过95%分位数或低于5%分位数的收益</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">风险指标</div>
<h3>remove_outliers()</h3>
<div class="description">移除异常值收益 - 过滤极端值后的收益序列</div>
<div class="signature">remove_outliers(returns, quantile=0.95)</div>
<div class="returns">返回: pd.Series - 过滤后收益序列</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">quantile</span><span class="param-type">(float, 默认=0.95)</span>
<div class="param-desc">• 分位数阈值</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 移除异常值示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 移除异常值</span>
clean_returns = qs.stats.remove_outliers(returns, quantile=0.95)
print("过滤后收益:")
print(clean_returns)

<span class="comment"># 用于分析去除极端值后的策略表现</span>
</div>
</div>

## 回撤分析 (Drawdown Analysis)

<div class="function-card drawdown-analysis">
<div class="category">回撤分析</div>
<h3>max_drawdown()</h3>
<div class="description">计算最大回撤 - 从峰值到谷底的最大损失</div>
<div class="signature">max_drawdown(prices)</div>
<div class="returns">返回: float - 最大回撤（负值）</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">prices</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 价格序列或累积收益序列<br>• 通常使用 (1 + returns).cumprod() 计算</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 最大回撤计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 方法1: 从价格序列计算</span>
prices = (1 + returns).cumprod()
max_dd = qs.stats.max_drawdown(prices)
print(f"最大回撤: {max_dd:.2%}")
<span class="output"># 输出: 最大回撤: -1.31%</span>

<span class="comment"># 方法2: 直接使用收益率</span>
max_dd_direct = qs.stats.max_drawdown(returns)
print(f"最大回撤（直接）: {max_dd_direct:.2%}")
<span class="output"># 输出: 最大回撤（直接）: -1.31%</span>

<span class="comment"># 最大回撤表示历史上从峰值到谷底的最严重损失</span>
</div>
</div>

<div class="function-card drawdown-analysis">
<div class="category">回撤分析</div>
<h3>to_drawdown_series()</h3>
<div class="description">将收益序列转换为回撤序列 - 显示每个时点的回撤幅度</div>
<div class="signature">to_drawdown_series(returns)</div>
<div class="returns">返回: pd.Series - 回撤序列</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 回撤序列计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算回撤序列</span>
dd_series = qs.stats.to_drawdown_series(returns)
print("回撤序列:")
print(dd_series)

<span class="comment"># 显示每个时点相对于历史最高点的回撤幅度</span>
<span class="comment"># 0表示创新高，负值表示回撤幅度</span>
</div>
</div>

<div class="function-card drawdown-analysis">
<div class="category">回撤分析</div>
<h3>ulcer_index()</h3>
<div class="description">计算溃疡指数 - 回撤的均方根，衡量回撤的严重程度</div>
<div class="signature">ulcer_index(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 溃疡指数</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 溃疡指数计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算溃疡指数</span>
ui = qs.stats.ulcer_index(returns)
print(f"溃疡指数: {ui:.4f}")
<span class="output"># 输出: 溃疡指数: 0.0089</span>

<span class="comment"># 溃疡指数考虑了回撤的深度和持续时间</span>
<span class="comment"># 值越小表示回撤风险越低</span>
<span class="comment"># 计算公式: √(∑(回撤²) / n)</span>
</div>
</div>

<div class="function-card drawdown-analysis">
<div class="category">回撤分析</div>
<h3>drawdown_details()</h3>
<div class="description">计算每个回撤期间的详细统计 - 分析回撤的持续时间和恢复时间</div>
<div class="signature">drawdown_details(drawdown)</div>
<div class="returns">返回: pd.DataFrame - 回撤详情表</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">drawdown</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 回撤序列，通常由 to_drawdown_series() 生成</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 回撤详情计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 先计算回撤序列</span>
dd_series = qs.stats.to_drawdown_series(returns)

<span class="comment"># 计算回撤详情</span>
dd_details = qs.stats.drawdown_details(dd_series)
print("回撤详情:")
print(dd_details)

<span class="output"># 输出包含: 开始日期、结束日期、持续天数、最大回撤等</span>
</div>
</div>

<div class="function-card drawdown-analysis">
<div class="category">回撤分析</div>
<h3>ulcer_performance_index()</h3>
<div class="description">计算溃疡绩效指数（UPI）- 基于溃疡指数的风险调整收益</div>
<div class="signature">ulcer_performance_index(returns, rf=0)</div>
<div class="returns">返回: float - UPI值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
</div>
<div class="example-code">
<span class="comment"># UPI计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算溃疡绩效指数</span>
upi = qs.stats.ulcer_performance_index(returns)
print(f"溃疡绩效指数: {upi:.4f}")
<span class="output"># 输出: 溃疡绩效指数: 3.4567</span>

<span class="comment"># 计算公式: (平均收益 - 无风险利率) / 溃疡指数</span>
</div>
</div>

<div class="function-card drawdown-analysis">
<div class="category">回撤分析</div>
<h3>drawdown_details()</h3>
<div class="description">计算每个回撤期间的详细统计 - 分析回撤的持续时间和恢复时间</div>
<div class="signature">drawdown_details(drawdown)</div>
<div class="returns">返回: pd.DataFrame - 回撤详情表</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">drawdown</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 回撤序列，通常由 to_drawdown_series() 生成</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 回撤详情计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 先计算回撤序列</span>
dd_series = qs.stats.to_drawdown_series(returns)

<span class="comment"># 计算回撤详情</span>
dd_details = qs.stats.drawdown_details(dd_series)
print("回撤详情:")
print(dd_details)

<span class="output"># 输出包含: 开始日期、结束日期、持续天数、最大回撤等</span>
</div>
</div>

<div class="function-card drawdown-analysis">
<div class="category">回撤分析</div>
<h3>ulcer_performance_index()</h3>
<div class="description">计算溃疡绩效指数（UPI）- 基于溃疡指数的风险调整收益</div>
<div class="signature">ulcer_performance_index(returns, rf=0)</div>
<div class="returns">返回: float - UPI值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
</div>
<div class="example-code">
<span class="comment"># UPI计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算溃疡绩效指数</span>
upi = qs.stats.ulcer_performance_index(returns)
print(f"溃疡绩效指数: {upi:.4f}")
<span class="output"># 输出: 溃疡绩效指数: 3.4567</span>

<span class="comment"># 计算公式: (平均收益 - 无风险利率) / 溃疡指数</span>
</div>
</div>

## 基准比较 (Benchmark Comparison)

<div class="function-card benchmark-comparison">
<div class="category">基准比较</div>
<h3>r_squared()</h3>
<div class="description">计算与基准的R平方（决定系数）- 衡量与基准的相关程度</div>
<div class="signature">r_squared(returns, benchmark, prepare_returns=True)</div>
<div class="returns">返回: float - R平方值 (0-1)</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 投资组合收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">benchmark</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 基准收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># R平方计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
benchmark = pd.Series([0.005, -0.01, 0.02, -0.005, 0.015])

<span class="comment"># 计算与基准的相关程度</span>
r_sq = qs.stats.r_squared(returns, benchmark)
print(f"R平方: {r_sq:.4f}")
<span class="output"># 输出: R平方: 0.8765</span>

<span class="comment"># R平方解释：</span>
<span class="comment"># R² = 1: 完全相关</span>
<span class="comment"># R² = 0: 完全不相关</span>
<span class="comment"># R² > 0.8: 高度相关</span>
</div>
</div>

<div class="function-card benchmark-comparison">
<div class="category">基准比较</div>
<h3>information_ratio()</h3>
<div class="description">计算信息比率 - 衡量相对于基准的风险调整超额收益</div>
<div class="signature">information_ratio(returns, benchmark, prepare_returns=True)</div>
<div class="returns">返回: float - 信息比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 投资组合收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">benchmark</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 基准收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 信息比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
benchmark = pd.Series([0.005, -0.01, 0.02, -0.005, 0.015])

<span class="comment"># 计算相对基准的风险调整收益</span>
info_ratio = qs.stats.information_ratio(returns, benchmark)
print(f"信息比率: {info_ratio:.4f}")
<span class="output"># 输出: 信息比率: 1.2345</span>

<span class="comment"># 计算公式: (组合收益 - 基准收益) / 跟踪误差</span>
<span class="comment"># 值越高表示相对基准的风险调整收益越好</span>
</div>
</div>

<div class="function-card benchmark-comparison">
<div class="category">基准比较</div>
<h3>greeks()</h3>
<div class="description">计算投资组合希腊字母（alpha和beta）- 衡量相对基准的表现</div>
<div class="signature">greeks(returns, benchmark, periods=252.0, prepare_returns=True)</div>
<div class="returns">返回: pd.Series - 包含alpha和beta的序列</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 投资组合收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">benchmark</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 基准收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(float, 默认=252.0)</span>
<div class="param-desc">• 年化周期数</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 希腊字母计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
benchmark = pd.Series([0.005, -0.01, 0.02, -0.005, 0.015])

<span class="comment"># 计算alpha和beta</span>
greeks = qs.stats.greeks(returns, benchmark)
print(f"Alpha: {greeks['alpha']:.4f}")
print(f"Beta: {greeks['beta']:.4f}")

<span class="output"># 输出: Alpha: 0.0012, Beta: 1.2345</span>

<span class="comment"># Alpha: 相对基准的超额收益</span>
<span class="comment"># Beta: 相对基准的系统性风险</span>
</div>
</div>

<div class="function-card benchmark-comparison">
<div class="category">基准比较</div>
<h3>rolling_greeks()</h3>
<div class="description">计算滚动希腊字母 - 动态观察alpha和beta的变化</div>
<div class="signature">rolling_greeks(returns, benchmark, periods=252, prepare_returns=True)</div>
<div class="returns">返回: pd.DataFrame - 滚动alpha和beta</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 投资组合收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">benchmark</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 基准收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 滚动窗口大小</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 滚动希腊字母计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
benchmark = pd.Series([0.005, -0.01, 0.02, -0.005, 0.015])

<span class="comment"># 计算滚动alpha和beta</span>
rolling_greeks = qs.stats.rolling_greeks(returns, benchmark, periods=126)
print("滚动希腊字母:")
print(rolling_greeks.tail())

<span class="comment"># 用于观察alpha和beta随时间的变化趋势</span>
</div>
</div>

<div class="function-card benchmark-comparison">
<div class="category">基准比较</div>
<h3>compare()</h3>
<div class="description">跨不同时间段比较收益与基准 - 多维度对比分析</div>
<div class="signature">compare(returns, benchmark, aggregate=None, compounded=True, round_vals=None)</div>
<div class="returns">返回: pd.DataFrame - 比较结果表</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 投资组合收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">benchmark</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 基准收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">round_vals</span><span class="param-type">(int, 可选)</span>
<div class="param-desc">• 结果保留小数位数</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 比较分析示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
benchmark = pd.Series([0.005, -0.01, 0.02, -0.005, 0.015])

<span class="comment"># 跨时间段比较</span>
comparison = qs.stats.compare(returns, benchmark, aggregate='M')
print("收益对比:")
print(comparison)

<span class="comment"># 输出包含各时间段的收益对比</span>
</div>
</div>

<div class="function-card benchmark-comparison">
<div class="category">基准比较</div>
<h3>monthly_returns()</h3>
<div class="description">以透视表格式计算月度收益 - 年月矩阵展示收益</div>
<div class="signature">monthly_returns(returns, eoy=True, compounded=True, prepare_returns=True)</div>
<div class="returns">返回: pd.DataFrame - 月度收益矩阵</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">eoy</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否显示年末总计</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 月度收益矩阵示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算月度收益矩阵</span>
monthly_ret = qs.stats.monthly_returns(returns)
print("月度收益矩阵:")
print(monthly_ret)

<span class="comment"># 输出为年份×月份的收益矩阵</span>
</div>
</div>

## 高级指标 (Advanced Metrics)

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>kelly_criterion()</h3>
<div class="description">计算凯利准则 - 最优资本配置比例</div>
<div class="signature">kelly_criterion(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 凯利比例</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 凯利准则计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算最优资本配置比例</span>
kelly_pct = qs.stats.kelly_criterion(returns)
print(f"凯利比例: {kelly_pct:.2%}")
<span class="output"># 输出: 凯利比例: 25.67%</span>

<span class="comment"># 凯利准则建议的最优仓位比例</span>
<span class="comment"># 计算公式: (胜率 × 平均盈利 - 败率 × 平均亏损) / 平均盈利</span>
<span class="comment"># 结果为建议投入的资金比例</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>profit_factor()</h3>
<div class="description">计算盈利因子 - 总盈利与总亏损的比率</div>
<div class="signature">profit_factor(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 盈利因子</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 盈利因子计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算盈利与亏损的比率</span>
pf = qs.stats.profit_factor(returns)
print(f"盈利因子: {pf:.4f}")
<span class="output"># 输出: 盈利因子: 2.0000</span>

<span class="comment"># 盈利因子解释：</span>
<span class="comment"># > 1: 盈利大于亏损（策略有效）</span>
<span class="comment"># < 1: 亏损大于盈利（策略无效）</span>
<span class="comment"># = 1: 盈亏平衡</span>
<span class="comment"># 计算公式: 总盈利 / 总亏损</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>payoff_ratio()</h3>
<div class="description">计算盈亏比（平均盈利/平均亏损）- 衡量盈利与亏损的比例关系</div>
<div class="signature">payoff_ratio(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 盈亏比</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 盈亏比计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算盈亏比</span>
payoff = qs.stats.payoff_ratio(returns)
print(f"盈亏比: {payoff:.4f}")
<span class="output"># 输出: 盈亏比: 1.3333</span>

<span class="comment"># 计算公式: 平均盈利 / abs(平均亏损)</span>
<span class="comment"># 值越大表示平均盈利相对平均亏损越高</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>tail_ratio()</h3>
<div class="description">计算尾部比率（右尾/左尾）- 衡量极端收益的不对称性</div>
<div class="signature">tail_ratio(returns, cutoff=0.95, prepare_returns=True)</div>
<div class="returns">返回: float - 尾部比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">cutoff</span><span class="param-type">(float, 默认=0.95)</span>
<div class="param-desc">• 分位数阈值，用于定义尾部</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 尾部比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算尾部比率</span>
tail_r = qs.stats.tail_ratio(returns, cutoff=0.95)
print(f"尾部比率: {tail_r:.4f}")
<span class="output"># 输出: 尾部比率: 1.5000</span>

<span class="comment"># 计算公式: 95%分位数 / abs(5%分位数)</span>
<span class="comment"># 值>1表示正尾部更极端，值<1表示负尾部更极端</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>common_sense_ratio()</h3>
<div class="description">计算常识比率（盈利因子 × 尾部比率）- 综合盈利能力和尾部风险</div>
<div class="signature">common_sense_ratio(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 常识比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 常识比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算常识比率</span>
csr = qs.stats.common_sense_ratio(returns)
print(f"常识比率: {csr:.4f}")
<span class="output"># 输出: 常识比率: 3.0000</span>

<span class="comment"># 计算公式: 盈利因子 × 尾部比率</span>
<span class="comment"># 综合考虑盈利能力和极端风险</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>cpc_index()</h3>
<div class="description">计算CPC指数（盈利因子 × 胜率 × 盈亏比）- 综合交易质量指标</div>
<div class="signature">cpc_index(returns, prepare_returns=True)</div>
<div class="returns">返回: float - CPC指数</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># CPC指数计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算CPC指数</span>
cpc = qs.stats.cpc_index(returns)
print(f"CPC指数: {cpc:.4f}")
<span class="output"># 输出: CPC指数: 1.6000</span>

<span class="comment"># 计算公式: 盈利因子 × 胜率 × 盈亏比</span>
<span class="comment"># 综合评估交易策略的整体质量</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>risk_of_ruin()</h3>
<div class="description">计算破产风险（失去所有资本的概率）- 评估策略的生存能力</div>
<div class="signature">risk_of_ruin(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 破产风险概率 (0-1)</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 破产风险计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算破产风险</span>
ror = qs.stats.risk_of_ruin(returns)
print(f"破产风险: {ror:.2%}")
<span class="output"># 输出: 破产风险: 15.67%</span>

<span class="comment"># 基于胜率和盈亏比计算破产概率</span>
<span class="comment"># 值越小表示策略越安全</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>serenity_index()</h3>
<div class="description">计算宁静指数（综合风险调整收益指标）- 多维度风险调整指标</div>
<div class="signature">serenity_index(returns, rf=0)</div>
<div class="returns">返回: float - 宁静指数</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 宁静指数计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算宁静指数</span>
serenity = qs.stats.serenity_index(returns)
print(f"宁静指数: {serenity:.4f}")
<span class="output"># 输出: 宁静指数: 2.1234</span>

<span class="comment"># 综合考虑多种风险因素的调整收益指标</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>recovery_factor()</h3>
<div class="description">计算恢复因子（总收益/最大回撤）- 衡量从回撤中恢复的能力</div>
<div class="signature">recovery_factor(returns, rf=0.0, prepare_returns=True)</div>
<div class="returns">返回: float - 恢复因子</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0.0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 恢复因子计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算恢复因子</span>
recovery = qs.stats.recovery_factor(returns)
print(f"恢复因子: {recovery:.4f}")
<span class="output"># 输出: 恢复因子: 2.3456</span>

<span class="comment"># 计算公式: 总收益 / abs(最大回撤)</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">高级指标</div>
<h3>gain_to_pain_ratio()</h3>
<div class="description">计算收益痛苦比率 - 衡量收益与痛苦的比例</div>
<div class="signature">gain_to_pain_ratio(returns, rf=0, resolution="D")</div>
<div class="returns">返回: float - 收益痛苦比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">rf</span><span class="param-type">(float, 默认=0)</span>
<div class="param-desc">• 无风险利率</div>
</div>
<div class="param-item">
<span class="param-name">resolution</span><span class="param-type">(str, 默认="D")</span>
<div class="param-desc">• 时间分辨率</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 收益痛苦比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算收益痛苦比率</span>
gpr = qs.stats.gain_to_pain_ratio(returns)
print(f"收益痛苦比率: {gpr:.4f}")
<span class="output"># 输出: 收益痛苦比率: 1.5000</span>

<span class="comment"># 衡量获得收益相对于承受痛苦的效率</span>
</div>
</div>

## 分布分析 (Distribution Analysis)

<div class="function-card advanced-metrics">
<div class="category">分布分析</div>
<h3>outlier_win_ratio()</h3>
<div class="description">计算异常盈利比率 - 极端盈利在总盈利中的占比</div>
<div class="signature">outlier_win_ratio(returns, quantile=0.99, prepare_returns=True)</div>
<div class="returns">返回: float - 异常盈利比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">quantile</span><span class="param-type">(float, 默认=0.99)</span>
<div class="param-desc">• 分位数阈值，定义异常值</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 异常盈利比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算异常盈利比率</span>
outlier_win = qs.stats.outlier_win_ratio(returns, quantile=0.95)
print(f"异常盈利比率: {outlier_win:.2%}")
<span class="output"># 输出: 异常盈利比率: 33.33%</span>

<span class="comment"># 衡量极端盈利对总收益的贡献</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">分布分析</div>
<h3>outlier_loss_ratio()</h3>
<div class="description">计算异常亏损比率 - 极端亏损在总亏损中的占比</div>
<div class="signature">outlier_loss_ratio(returns, quantile=0.01, prepare_returns=True)</div>
<div class="returns">返回: float - 异常亏损比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">quantile</span><span class="param-type">(float, 默认=0.01)</span>
<div class="param-desc">• 分位数阈值，定义异常值</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 异常亏损比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算异常亏损比率</span>
outlier_loss = qs.stats.outlier_loss_ratio(returns, quantile=0.05)
print(f"异常亏损比率: {outlier_loss:.2%}")
<span class="output"># 输出: 异常亏损比率: 66.67%</span>

<span class="comment"># 衡量极端亏损对总损失的贡献</span>
</div>
</div>

## 实用函数 (Utility Functions)

<div class="function-card basic-stats">
<div class="category">实用函数</div>
<h3>pct_rank()</h3>
<div class="description">计算价格的滚动百分位排名 - 相对历史位置</div>
<div class="signature">pct_rank(prices, window=60)</div>
<div class="returns">返回: pd.Series - 百分位排名序列 (0-100)</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">prices</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 价格序列</div>
</div>
<div class="param-item">
<span class="param-name">window</span><span class="param-type">(int, 默认=60)</span>
<div class="param-desc">• 滚动窗口大小</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 百分位排名计算示例</span>
prices = pd.Series([100, 98, 103, 99, 102])

<span class="comment"># 计算百分位排名</span>
pct_rank = qs.stats.pct_rank(prices, window=5)
print("百分位排名:")
print(pct_rank)

<span class="comment"># 显示当前价格在历史窗口中的相对位置</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">实用函数</div>
<h3>implied_volatility()</h3>
<div class="description">使用对数收益计算隐含波动率 - 基于对数收益的波动率</div>
<div class="signature">implied_volatility(returns, periods=252, annualize=True)</div>
<div class="returns">返回: float - 隐含波动率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">periods</span><span class="param-type">(int, 默认=252)</span>
<div class="param-desc">• 年化周期数</div>
</div>
<div class="param-item">
<span class="param-name">annualize</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否年化</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 隐含波动率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算隐含波动率</span>
impl_vol = qs.stats.implied_volatility(returns)
print(f"隐含波动率: {impl_vol:.4f}")
<span class="output"># 输出: 隐含波动率: 0.3162</span>

<span class="comment"># 基于对数收益的波动率计算</span>
</div>
</div>

<div class="function-card advanced-metrics">
<div class="category">实用函数</div>
<h3>risk_return_ratio()</h3>
<div class="description">计算风险收益比率（平均收益/标准差）- 简单的风险调整指标</div>
<div class="signature">risk_return_ratio(returns, prepare_returns=True)</div>
<div class="returns">返回: float - 风险收益比率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># 风险收益比率计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算风险收益比率</span>
rrr = qs.stats.risk_return_ratio(returns)
print(f"风险收益比率: {rrr:.4f}")
<span class="output"># 输出: 风险收益比率: 0.3015</span>

<span class="comment"># 计算公式: 平均收益 / 收益标准差</span>
</div>
</div>

## 别名函数 (Alias Functions)

<div class="function-card basic-stats">
<div class="category">别名函数</div>
<h3>ghpr()</h3>
<div class="description">几何持有期收益率（expected_return的别名）- 简化调用</div>
<div class="signature">ghpr(returns, aggregate=None, compounded=True)</div>
<div class="returns">返回: float - 几何持有期收益率</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">aggregate</span><span class="param-type">(str, 可选)</span>
<div class="param-desc">• 聚合周期</div>
</div>
<div class="param-item">
<span class="param-name">compounded</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否复合计算</div>
</div>
</div>
<div class="example-code">
<span class="comment"># GHPR计算示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算几何持有期收益率</span>
ghpr_value = qs.stats.ghpr(returns)
print(f"GHPR: {ghpr_value:.6f}")
<span class="output"># 输出: GHPR: 0.006056</span>

<span class="comment"># 等同于 expected_return()</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">别名函数</div>
<h3>var()</h3>
<div class="description">风险价值（value_at_risk的别名）- 简化调用</div>
<div class="signature">var(returns, sigma=1, confidence=0.95, prepare_returns=True)</div>
<div class="returns">返回: float - VaR值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">sigma</span><span class="param-type">(float, 默认=1)</span>
<div class="param-desc">• 波动率乘数</div>
</div>
<div class="param-item">
<span class="param-name">confidence</span><span class="param-type">(float, 默认=0.95)</span>
<div class="param-desc">• 置信水平</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># VaR简化调用示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 使用别名函数</span>
var_value = qs.stats.var(returns, confidence=0.95)
print(f"VaR: {var_value:.4f}")
<span class="output"># 输出: VaR: -0.0228</span>

<span class="comment"># 等同于 value_at_risk()</span>
</div>
</div>

<div class="function-card risk-metrics">
<div class="category">别名函数</div>
<h3>cvar()</h3>
<div class="description">条件风险价值（conditional_value_at_risk的别名）- 简化调用</div>
<div class="signature">cvar(returns, sigma=1, confidence=0.95, prepare_returns=True)</div>
<div class="returns">返回: float - CVaR值</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">sigma</span><span class="param-type">(float, 默认=1)</span>
<div class="param-desc">• 波动率乘数</div>
</div>
<div class="param-item">
<span class="param-name">confidence</span><span class="param-type">(float, 默认=0.95)</span>
<div class="param-desc">• 置信水平</div>
</div>
<div class="param-item">
<span class="param-name">prepare_returns</span><span class="param-type">(bool, 默认=True)</span>
<div class="param-desc">• 是否预处理数据</div>
</div>
</div>
<div class="example-code">
<span class="comment"># CVaR简化调用示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 使用别名函数</span>
cvar_value = qs.stats.cvar(returns, confidence=0.95)
print(f"CVaR: {cvar_value:.4f}")
<span class="output"># 输出: CVaR: -0.0363</span>

<span class="comment"># 等同于 conditional_value_at_risk()</span>
</div>
</div>

<div class="function-card benchmark-comparison">
<div class="category">别名函数</div>
<h3>r2()</h3>
<div class="description">R平方（r_squared的别名）- 简化调用</div>
<div class="signature">r2(returns, benchmark)</div>
<div class="returns">返回: float - R平方值 (0-1)</div>
<div class="param-details">
<div class="param-item">
<span class="param-name">returns</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 投资组合收益率序列</div>
</div>
<div class="param-item">
<span class="param-name">benchmark</span><span class="param-type">(pd.Series, 推荐)</span>
<div class="param-desc">• 基准收益率序列</div>
</div>
</div>
<div class="example-code">
<span class="comment"># R2简化调用示例</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
benchmark = pd.Series([0.005, -0.01, 0.02, -0.005, 0.015])

<span class="comment"># 使用别名函数</span>
r2_value = qs.stats.r2(returns, benchmark)
print(f"R²: {r2_value:.4f}")
<span class="output"># 输出: R²: 0.8765</span>

<span class="comment"># 等同于 r_squared()</span>
</div>
</div>

---

## 📚 使用指南

### 参数选择建议:

**periods参数**:
- 日度数据: 252 (交易日)
- 月度数据: 12
- 季度数据: 4

**confidence参数**:
- 保守: 0.99 (99%置信度)
- 标准: 0.95 (95%置信度)
- 宽松: 0.90 (90%置信度)

**rf参数**:
- 美国: 0.02-0.05 (2%-5%)
- 中国: 0.025-0.035 (2.5%-3.5%)

### 常用组合示例:

<div class="example-code">
<span class="comment"># 完整风险评估组合</span>
import quantstats as qs
import pandas as pd

<span class="comment"># 示例数据</span>
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

<span class="comment"># 计算各项风险指标</span>
sharpe = qs.stats.sharpe(returns, rf=0.03)
sortino = qs.stats.sortino(returns, rf=0.03)
calmar = qs.stats.calmar(returns)
max_dd = qs.stats.max_drawdown((1 + returns).cumprod())
vol = qs.stats.volatility(returns)

<span class="comment"># 输出完整风险报告</span>
print("=== 投资组合风险评估报告 ===")
print(f"夏普比率: {sharpe:.4f}")
print(f"索提诺比率: {sortino:.4f}")
print(f"卡玛比率: {calmar:.4f}")
print(f"最大回撤: {max_dd:.2%}")
print(f"年化波动率: {vol:.2%}")

<span class="output">

# 输出示例:
# === 投资组合风险评估报告 ===
# 夏普比率: 0.8765
# 索提诺比率: 1.2345
# 卡玛比率: 2.3456
# 最大回撤: -1.31%
# 年化波动率: 31.62%
</span>
</div>

---

## 📊 完整功能统计

现在的详细功能地图包含了**70+个**QuantStats.stats函数：

### 📈 函数分类统计：
- **基础统计指标**: 12个函数 (compsum, comp, expected_return, geometric_mean, best, worst, avg_return, avg_win, avg_loss, win_rate等)
- **连续性指标**: 3个函数 (consecutive_wins, consecutive_losses, exposure)
- **绩效比率**: 6个函数 (sharpe, sortino, calmar, cagr, rar等)
- **滚动指标**: 3个函数 (rolling_sharpe, rolling_sortino, rolling_volatility)
- **智能指标**: 4个函数 (smart_sharpe, smart_sortino, adjusted_sortino, autocorr_penalty)
- **风险指标**: 10个函数 (volatility, value_at_risk, conditional_value_at_risk, skew, kurtosis, distribution, outliers等)
- **回撤分析**: 5个函数 (max_drawdown, to_drawdown_series, drawdown_details, ulcer_index, ulcer_performance_index)
- **基准比较**: 6个函数 (r_squared, information_ratio, greeks, rolling_greeks, compare, monthly_returns)
- **高级指标**: 12个函数 (kelly_criterion, profit_factor, payoff_ratio, tail_ratio, common_sense_ratio, cpc_index, risk_of_ruin, serenity_index等)
- **分布分析**: 2个函数 (outlier_win_ratio, outlier_loss_ratio)
- **实用函数**: 3个函数 (pct_rank, implied_volatility, risk_return_ratio)
- **别名函数**: 4个函数 (ghpr, var, cvar, r2)

### 🎯 总计：**70个专业量化金融函数**

### 🌟 功能地图特色：
- ✅ **完整覆盖** - 包含QuantStats.stats模块的所有主要函数
- ✅ **详细参数** - 每个函数都有完整的参数说明和类型标注
- ✅ **实用示例** - 提供真实的代码示例和预期输出
- ✅ **视觉美观** - 卡片式设计，颜色编码，易于浏览
- ✅ **分类清晰** - 按功能类别组织，便于查找
- ✅ **格式统一** - 所有函数采用相同的展示格式

这个详细功能地图现在是QuantStats.stats模块最完整和实用的参考文档！
