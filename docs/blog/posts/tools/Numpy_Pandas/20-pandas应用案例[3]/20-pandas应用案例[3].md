---
title: Pandas应用案例[3]
series: 量化人的 Numpy 和 Pandas
seq: "10"
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-20
date: 2025-04-05
category: tools
motto: PDon't watch the clock; do what it does. Keep going.
img: https://images.jieyu.ai/images/hot/mybook/men-wearing-tank.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---

“Modin 通过多核并行加速 Pandas 操作，读取 10GB CSV 文件比 Pandas 快 4-8 倍；Polars 基于 Rust 架构，内存占用仅为 Pandas 的 1/3；Dask 则支持分布式计算，轻松处理 TB 级数据。”

---

### 1.4. 使用eval或者query
<!--使用 isin 筛选 https://zhuanlan.zhihu.com/p/97012199-->

关于 query 方法，我它类似于SQL的where子句，允许用字符串表达式，这样代码更简洁。比如df.query('Q1 > Q2 > 90')，还支持用@符号引入外部变量。比如计算平均分后筛选高于平均分的数据。同时，eval方法类似，但返回布尔索引，需要配合df[]使用，例如：`df[df.eval("Q1 > 90 > Q3 >10")]`。

isin 方法，用于筛选某列的值是否在指定列表中。例如，用 `b1["类别"].isin(["能源","电器"])` 来筛选类别列中的值。此外，还可以结合多个条件，例如：`df[df['ucity'].isin(['广州市','深圳'])]`。


#### 1.4.1. query() 函数：SQL风格的条件筛选
1. **核心语法**
```python
df.query('表达式')  # 表达式需用引号包裹，支持逻辑运算符和列名直接引用
```

2. **金融场景示例**
```python
"""案例1：筛选特定股票代码的高额交易"""
# 筛选AAPL或TSLA股票，且金额超过100万的交易
df.query("symbol in ['AAPL', 'TSLA'] and amount > 1e6")

"""案例2：动态引用外部变量"""
avg_amount = df['amount'].mean()  # 计算平均交易金额
df.query("amount > @avg_amount * 2")  # 筛选金额超过平均2倍的交易[3,5](@ref)
```

---

```python
"""案例3：多条件组合"""
# 筛选2025年Q1买入且成交价高于开盘价的交易
df.query("trade_type == 'buy' and trade_date >= '2025-01-01' and price > open_price")
```

3. ​**性能优势**
- ​表达式优化：底层通过 numexpr 库加速计算，比传统布尔索引快30%以上
- ​列名处理：列名含空格或特殊字符时需用反引号包裹（如 `收盘价` > 100）


#### 1.4.2. eval() 函数：表达式生成布尔索引
1. ​**核心语法**
```python
mask = df.eval("表达式")  # 返回布尔数组
df[mask]  # 用布尔索引筛选数据
```

2. **​金融场景示例**
```python
"""案例1：计算复杂交易条件"""
# 筛选波动率超过阈值且交易量增长的股票
df[df.eval("(high - low)/close > 0.05 and volume > volume.shift(1)")]

"""案例2：动态公式计算"""
# 筛选夏普比率高于行业平均的基金
industry_avg = 1.2
df[df.eval("(returns - risk_free_rate)/std_dev > @industry_avg")]
```

3. **​与query()的区别**
   - eval() 返回布尔数组，需配合 df[] 使用；query() 直接返回筛选后的DataFrame
   - 两者共享相同表达式引擎，性能差异可忽略，按代码简洁性选择即可

---

#### 1.4.3. isin() 函数：多值匹配筛选
1. ​**核心语法**
```python
df[df['列名'].isin(值列表)]  # 筛选列值存在于列表中的行
```

2. **​金融场景示例**
```python
"""案例1：筛选特定股票池"""
blue_chips = ['600519.SH', '000858.SZ', '601318.SH']  # 上证50成分股
df[df['symbol'].isin(blue_chips)]

"""案例2：排除ST/ST风险股"""
risk_stocks = ['*ST长生', 'ST康美']  
df[~df['stock_name'].isin(risk_stocks)]  # 使用~取反[2](@ref)

"""案例3：联合多列筛选"""
# 筛选沪深300且行业为科技或金融的股票
target_industries = ['Technology', 'Financials']
df[df['index'].isin(['000300.SH']) & df['industry'].isin(target_industries)]
```

3. ​**进阶用法**
   - ​字典筛选：多列联合匹配（如 df[df.isin({'symbol':'AAPL', 'exchange':'NASDAQ'})]）
   - 性能优化：对大列表（>1万元素）建议先转换为集合（set()）提升速度

#### 1.4.4. 综合性能优化策略
1. **先筛选再计算**

---

```python
# 错误：先计算全量再筛选
df['return'] = df['close'].pct_change()  
df_filtered = df[df['volume'] > 1e6]

# 正确：先筛选减少计算量
df_filtered = df[df['volume'] > 1e6].copy()  
df_filtered['return'] = df_filtered['close'].pct_change()[6](@ref)
```

2. **​避免链式操作**
```python
# 错误：两次索引降低性能
df[df['symbol'] == 'AAPL']['close']  
# 正确：单次loc操作
df.loc[df['symbol'] == 'AAPL', 'close'][3](@ref)
```

3. **​类型优化**
```python
# 将字符串列转为category提升isin速度
df['symbol'] = df['symbol'].astype('category')[8](@ref)
```

#### 1.4.5. 方法对比与适用场景
|方法	|适用场景	|性能优势	|
|:------:|----------|----------|
|query()|	复杂多条件组合，需动态变量引用	|表达式优化加速	|
|eval()	|生成中间布尔索引，用于后续处理	|与query性能接近	|
|isin()	|快速匹配离散值列表（如股票代码）|	集合加速+类型优化|

实践建议：
- ​高频筛选：优先用 query() 保持代码简洁

---

- ​超大列表：用 isin() + 集合类型提升速度
- ​动态计算：eval() 适合嵌入数学公式或跨列运算

### 1.5. Pandas 的其它替代方案
#### 1.5.1. modin：单机多核并行加速器
_一行代码，实现pandas替代，并拥有多核、不受内存限制的计算能力。_

1. **​核心原理**
   - ​并行化改造：将 Pandas 的 DataFrame 拆分为多个分区，利用多核 CPU 并行处理，底层支持 Ray 或 Dask 引擎。
   - ​语法兼容性：仅需修改导入语句（import modin.pandas as pd），即可无缝替代原生 Pandas，支持 90% 以上常用 API。

2. **​性能优势**
   - 读取加速：读取 10GB CSV 文件时，比 Pandas 快 4-8 倍。
   - ​计算优化：groupby 等聚合操作在 4 核机器上提速 3-5 倍，内存占用减少 30%。
   - ​适用场景：单机环境下处理 100MB~50GB 数据集，适合金融高频交易日志分析、用户行为数据清洗等。

3. **​使用案例**
```python
# 读取大规模交易数据（并行加速）
import modin.pandas as pd
df = pd.read_csv("trades.csv", parse_dates=["timestamp"])
```

---

```python
# 实时计算每分钟交易量
volume_by_minute = df.groupby(pd.Grouper(key="timestamp", freq="T"))["amount"].sum().compute()
```

4. **​注意事项**
   - ​小数据集劣势：处理 <100MB 数据时可能比 Pandas 更慢（启动开销）。
   - ​内存消耗：需预留 2-3 倍数据大小的内存，避免 OOM。

#### 1.5.2. polars：Rust 驱动的极速引擎
_最快的tableu解决方案_


1. **​核心原理**
   - ​Rust + Arrow 架构：基于 Rust 语言和 Apache Arrow 内存格式，支持零拷贝数据处理与 SIMD 指令优化。
   - ​多线程与惰性执行：自动并行化计算，通过 lazy() 延迟执行并优化查询计划。

2. **​性能优势**
   - 速度对比：同等操作比 Pandas 快 5-10 倍，1 亿行 groupby 计算仅需 11 秒（Pandas 需 187 秒）。
   - ​内存效率：内存占用仅为 Pandas 的 1/3，支持处理内存不足时的核外计算。

3. **​适用场景**
   - ​高频金融数据：如实时波动率计算、订单簿快照分析。
   - ​复杂聚合：多条件统计、时间窗口滚动计算（如 VWAP）。

4. ​**代码示例**

---

```python
import polars as pl
# 惰性执行优化查询
df = pl.scan_csv("market_data.csv")
result = (
   df.filter(pl.col("price") > 100)
   .groupby("symbol")
   .agg([pl.col("volume").sum(), pl.col("price").mean()])
   .collect()  # 触发计算
)
```

!!! Tip
    ​注意事项
    - ​语法差异：部分 Pandas 方法需改写（如 df[df.col > 0] → df.filter(pl.col("col") > 0)）。
    - ​可视化兼容性：需转换为 Pandas 或 NumPy 才能使用 Matplotlib/seaborn。

#### 1.5.3. dask：分布式计算的瑞士军刀
_分布式tableu，可运行在数千结点上_


1. **​核心原理**
   - ​分布式任务调度：将任务拆分为 DAG（有向无环图），支持单机多核或集群分布式执行。
   - ​核外计算：通过分区处理超出内存的数据集（如 TB 级日志）。

---

2. **​性能优势**
   - ​横向扩展：在 16 核机器上处理 50GB 数据比 Pandas 快 10 倍，支持扩展到千节点集群。
   - ​兼容生态：无缝对接 XGBoost、Dask-ML 等库，支持分布式模型训练。

3. **​适用场景**
   - ​超大规模数据：如全市场历史行情分析、社交网络图谱计算。
   - ​ETL 流水线：多步骤数据清洗与特征工程（需依赖管理）。

4. ​**实战技巧**
    ```python
    import dask.dataframe as dd
    # 分块读取与处理
    ddf = dd.read_csv("s3://bucket/large_file_*.csv", blocksize="256MB")
    # 并行计算每支股票的年化波动率
    volatility = ddf.groupby("symbol")["return"].std().compute()
    ```

!!! Tip
    ​注意事项
    - ​调试复杂性：需用 Dask Dashboard 监控任务状态，定位数据倾斜问题。
    - ​配置优化：合理设置分区大小（建议 100MB~1GB），避免调度开销。

---

#### 1.5.4. 选型决策树

|场景|	​推荐工具|	​理由|
|---|----------|----------|
|单机中数据（<50GB）|	Modin	|零代码修改，快速提升现有 Pandas 脚本性能|
|高频计算/内存受限	|Polars	|极致速度与低内存消耗，适合量化交易场景|
|分布式/超大数据（>1TB）|	Dask	|支持集群扩展，生态完善|

​注：实际测试显示，Polars 在单机性能上全面领先，而 Dask 在分布式场景下更具优势。建议结合数据规模与硬件资源综合选择。
