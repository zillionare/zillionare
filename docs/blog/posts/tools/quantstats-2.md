---
title: 算收益，用算术平均好还是几何平均好?
excerpt: "同样是 30% 收益，A 策略跑 30 天，B 策略跑 25 天，谁更牛？Ran Aroussi 的 QuantStats 库藏着答案！这个获 5.8k 星标的 Python 工具，能用 compsum、comp 等函数拆穿收益骗局，可为何几何均值总比算术均值 “矮一截”？"
date: 2025-08-02
categories: tools
tags:
    - quantstats
    - 几何收益
---

假设我们已构建一套投资策略，并通过回测工具获取了该策略的每日历史回测收益数据。下一步的核心工作是对策略进行全面评估，包括其有效性、风险水平及收益表现，**QuantStats**的设计目标即在于此。



![](https://fastly.jsdelivr.net/gh/bucketio/img14@main/images/2025/08/1754140031515-8bc2da28-02cd-4083-8c6b-c698c4cf5e36.png)


Quantstats是 Ran Aroussi 的一个开源项目，是一款用于**交易策略绩效分析**的 Python 库，深受量化圈用户喜爱，在 Github 上获得了<span style="text-decoration: dashed underline #00A86B; text-decoration-thickness: 2px;">超过 5.8k 的 stars</span>。

!!! tip 它主要由3部分组成：

**quantstats.stats**：用于计算多种性能指标，如夏普比率、胜率等
**quantstats.plots**：用于性能、下降趋势、月度回报等绩效指标的可视化
**quantstats.reports**：用于生成度量报告，可保存为html文件


由于前段时间原作者长期未维护，导致新安装的 Quantstats，尤其是在 Python 3.12 及以上高版本中，几乎无法运行，因此，前段时间我们出手维护,带来了**Quantstats Reloaded**，欢迎大家安装使用!
```python
!pip install quantstats-reloaded
```


评价策略表现的具体量化依据为各类指标,例如: <span style="text-decoration: dashed underline #00A86B; text-decoration-thickness: 2px;">信息比率、夏普比率、最大回撤，以及 α 收益、β 收益</span> 等。需明确的是，这些指标的计算遵循客观、标准化的公式，具备严格的数理规则；但对指标结果的解读与评价则具有主观性，往往与使用者的风险偏好相关。

!!! tip 
因此，不存在绝对的 “好坏判定阈值”，关键在于深入理解各指标背后的经济逻辑与风险收益内涵，进而结合自身投资目标与风险承受能力形成独立判断。


光是QuantStats中的Stats库下就有几十种计算指标。我们今天先来介绍Stats库中的<span style="text-decoration: dashed underline #00A86B; text-decoration-thickness: 2px;">compsum()、comp()、expected_return()</span> 这三个函数，看看这三个函数有什么用处？它们之间有着怎样的联系呢？
    
## 基础统计
**1. compsum(): 将收益率序列转换为累积复合收益率序列（累积乘积）**
```python
函数: compsum(returns)

# 参数介绍
returns(pd.Series, 推荐)
• 收益率序列,通常是日收益率数据
格式: [0.01, -0.02, 0.03, ...] 
• 表示1%, -2%, 3%
• 计算公式: (1 + returns).cumprod() - 1

# 示例用法
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
cumulative = qs.stats.compsum(returns)

# 输出结果
[0.01, -0.0098, 0.0207, 0.0105, 0.0307]
```

!!! tip
compsum函数返回的是「一串序列」，且长度与输入序列一致! !它能用于「可视化收益率」是怎么从「初始状态」变化到「最终状态」的。它就像是一部纪录片,记载了一只股票在策略执行下的浮浮沉沉，效果类似于下图


![](https://fastly.jsdelivr.net/gh/bucketio/img14@main/images/2025/08/1754138614424-3c94d9d1-2058-4ef3-a5d4-e1f2a5c0fab6.png)


**2. comp() : 计算总复合收益率（最终累积收益）- 整个期间的总收益率**
```python
函数: comp(returns)

#参数介绍
returns(pd.Series, 推荐)
• 收益率序列
计算公式: (1 + returns).prod() - 1
• 等同于 compsum() 的最后一个值

# 示例用法
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
total_return = qs.stats.comp(returns)
print(f"总收益率: {total_return:.4f}")

# 等价计算方法
cumulative = qs.stats.compsum(returns)
print(f"最后值: {cumulative.iloc[-1]:.4f}")
```

!!! tip 
与compsum函数相比,comp函数的区别是:它返回的是「一个数值」,而不是一串序列(体现在计算公式上)。并且这个数值是compsum函数返回序列的最后一个值!因此，comp返回的是某个期间的最终总收益率




 **3. expected_return() : 计算期望收益率（几何平均数)**
```python
函数: expected_return(returns, aggregate=None, compounded=True, prepare_returns=True)

#参数介绍
returns(pd.Series, 推荐)
•收益率序列
aggregate(str, 可选)
• 聚合周期: 'D'(日), 'W'(周), 'M'(月), 'Q'(季), 'Y'(年)
compounded(bool, 默认=True)
• 是否使用复合收益率计算
prepare_returns(bool, 默认=True)
• 是否预处理数据（去除NaN等）

# 示例用法
returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
# 计算日度期望收益
expected_ret = qs.stats.expected_return(returns)
print(f"日度期望收益: {expected_ret:.4f}")

# 计算公式: (∏(1 + returns))^(1/n) - 1
# 几何平均数，考虑复利效应
```

**假设有A、B两个策略，其中：**

 	
A策略：已运行30天，区间总计累积收益为30%**（使用comp计算得到）**
B策略：已运行25天，区间总计累积收益为20%**（使用comp计算得到）**
	
    
!!! question A策略与B策略相比，谁更好？
Answer：因为「时间长度不一样」，所以不能直接用30%与20%做比较。建议计算两者「平均每天的收益率」，这样才有可比性

	
!!! question **平均数的计算方式分为：「算术平均数」和「几何平均数」，用哪个更好？
Answer：当然是「几何平均数」！**(通过expected_return计算**)。因为它不仅考虑了「复利」的影响，还能精准还原最终的累计净值大小


    
现在,我们通过下方代码生成一系列随机数，我们可以生成很多个上涨或下跌情况下的净值走势以及它们的算术平均数和几何平均数从起点到终点的变化路径

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




**我们发现，无论是上涨还是下跌，蓝线始终在红线上方**





![](https://fastly.jsdelivr.net/gh/bucketio/img1@main/images/2025/08/1754140954570-f3b2099a-7c1d-4f0d-a779-f72746745288.jpg)

![](https://fastly.jsdelivr.net/gh/bucketio/img3@main/images/2025/08/1754141671086-ea326a34-7b55-4d94-bacb-f7a20f4f1452.png)


!!! question 为什么无论上涨或是下跌，蓝线永远在红线上方？
Answer：根据均值不等式: 算数平均数 ≥ 几何平均数


![](https://fastly.jsdelivr.net/gh/bucketio/img16@main/images/2025/08/1754141556739-bab818f5-1e52-49f1-b1f7-31ed70cadc62.png)



<span style="text-decoration: dashed underline #00A86B; text-decoration-thickness: 2px;">我们高中就学过的均值不等式，你还记得吗....</span>


