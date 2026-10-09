---
title: "Pandas Performance: Memory & Speed Hacks for Quant Data"
date: 2025-04-05
slug: en/articles/python/numpy-pandas/19-pandas应用案例-2
tags: [Pandas, Performance Optimization, Memory Management, Numba]
excerpt: "Reduce memory by 90%+ using category types and compact dtypes. Boost iteration speed 6x with itertuples. Achieve C-level performance in numerical calculations via Numba JIT compilation for high-frequency trading data."
lang: en
translation_of: articles/python/numpy-pandas/19-pandas应用案例-2
auto_translated: true
source_sha: 82f7f9d476157b208d3f8670c9b82ef329abd7e4
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/poster-on-wall.jpg"
---

"By converting string columns to `category` type, memory usage can be reduced by over 90%; replacing `iterrows` with `itertuples` improves iteration speed by 6x; and combining Numba’s JIT compilation allows numerical computation performance to rival C language."

---

## 1. Pandas Performance
### 1.1. Memory Optimization
Using the `category` type converts strings into categorical variables, replacing original values with integer indices to save memory. For example, converting repetitive strings like gender to `category` significantly reduces memory footprint. Additionally, categorical types can improve the performance of certain operations, such as sorting and grouping, because they use integer processing internally, achieving optimization effects.

Furthermore, data type optimization is possible, such as converting `int64` to smaller types like `int8` or `uint8`. It is crucial to check the range of each column and select the appropriate subtype; for instance, use `uint8` if the values are between 0 and 255. Explicitly specifying `dtype` is important, especially when reading data, to avoid automatic inference that leads to memory waste.

#### 1.1.1. Category Type: The Ultimate Optimization for Categorical Data
**Core Principles**
- **Memory Compression**: Converts repetitive strings (e.g., gender, region, product category) into integer indices and establishes a mapping dictionary. For example, storing "Male/Female" as 0/1 reduces memory usage by **over 90%**.
- **Performance Improvement**: Categorical data is **10-100 times faster** than strings for operations like `groupby` and `sort_values` because it uses integer arithmetic at the底层 (low level).

**Use Cases**
- **Low Cardinality Data**: When the number of unique values in a column is much smaller than the total number of rows (e.g., only 2 types of gender, but millions of rows).

---

- **Ordered Categories**: Such as rating levels ("High/Medium/Low") or time periods ("Early/Mid/Late"), where specifying the order improves analysis efficiency.

**Operation Method**
```python
import pandas as pd
import numpy as np

# 模拟金融数据：10万条交易记录
dates = pd.date_range('2025-01-01', periods=100000, freq='T')  # 分钟级交易

df = pd.DataFrame({
    'trade_type': np.random.choice(['buy', 'sell', 'cancel'], 
    size=100000),  # 交易类型
    'symbol': np.random.choice(['AAPL', 'MSFT', 'GOOGL', 'TSLA'], 
    size=100000),  # 股票代码
    'client_type': np.random.choice(['retail', 'institution', 'vip'], 
    size=100000),  # 客户类型
    'amount': np.random.uniform(1000, 1e6, size=100000)#交易金额
}, index=dates)

# 优化前内存占用
print("优化前内存：", df.memory_usage(deep=True).sum() / 1024**2, "MB")

# 转换为Category类型
cat_cols = ['trade_type', 'symbol', 'client_type']
df[cat_cols] = df[cat_cols].astype('category')

# 优化后内存对比
print("优化后内存：", df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

Memory before optimization: 19.291857719421387 MB

Memory after optimization: 1.8129425048828125 MB **(Reduced by 90.6%)**

---

!!! Tip
    Regularly check memory usage, for example, using the `memory_usage` method, to evaluate the optimization effect.


**Fields Suitable for Financial Scenarios:**
- **Transaction Type**: e.g., `buy/sell`, `order_type` (Limit/Market orders)
- **Asset Class**: e.g., `stock`, `bond`, `ETF`
- **Customer Tier**: e.g., `VIP`, `Retail`, `Institutional`
- **Geographic Classification**: e.g., `CN`, `US`, `HK` (Market attribution)

Using `category` is most effective when a column has few unique values and high repetition, such as gender or region codes. If the number of categories in a categorical variable is significantly smaller than the total number of rows, the memory savings after conversion will be more pronounced. Note that the `category` type is not suitable for scenarios where categories change frequently, as this may increase computational overhead. Additionally, when creating categorical data using `pd.Categorical` or `cut`, pay attention to handling missing values, as the `category` type does not support `NaN`. Missing values must be handled before conversion.


#### 1.1.2. Compact Data Types: Precisely Targeting Memory Waste
**Numerical Type Optimization**
- **Integer Types**: Select the smallest subtype based on the value range:
    ```python
    # Convert after checking range
    df['age'] = df['age'].astype('uint8')  # Range 0-255
    ```
- **Floating Point Types**: Prioritize `float32` (when precision is sufficient), reducing memory by **50%**.

---

**Boolean Type Optimization**
Convert columns containing only `True`/`False` to `bool` type:
```python
    df['is_active'] = df['is_active'].astype('bool')
```

**Time Type Optimization**
Use `datetime64[ns]` instead of `object` to store dates, reducing memory by **75%** and enabling time series operations.

Financial data often contains the following fields with high optimization value:
- **Discrete Categorical Fields**: Transaction type (buy/sell), Security code (AAPL/TSLA), Customer tier (VIP/Retail)
- **Numerical Fields**: Transaction amount (float64), Position size (int64), Timestamp (object)
- **Status Indicator Fields**: After-hours trading (True/False), Risk marker (high/medium/low)


```python
import pandas as pd
import numpy as np

# 生成10万条模拟交易数据
dates = pd.date_range('2025-01-01', periods=100000, freq='T')  # 分钟级时间戳
df = pd.DataFrame({
    'trade_type': np.random.choice(['buy', 'sell', 'cancel'], size=100000),
    'symbol': np.random.choice(['AAPL', 'MSFT', 'GOOGL', 'TSLA'], size=100000),
    'client_level': np.random.choice(['VIP', '普通', '机构'], size=100000),
    'amount': np.random.uniform(1000, 1e6, size=100000),
    'position': np.random.randint(1, 10000, size=100000)
}, index=dates)

print("优化前内存：", df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

---

```python
# 转换分类类型
cat_cols = ['trade_type', 'symbol', 'client_level']
df[cat_cols] = df[cat_cols].astype('category')

# 查看内存优化效果
print("优化后内存：", df.memory_usage(deep=True).sum() / 1024**2, "MB")

# 压缩数值类型
df['amount'] = df['amount'].astype('float32')  # 金额压缩为32位浮点
df['position'] = df['position'].astype('int16')  # 持仓量压缩为16位整数

# 时间戳优化（假设原始数据为字符串）
df['trade_time'] = pd.to_datetime(df.index)  # 转为datetime64[ns]

# 最终内存对比
print("最终内存：", df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

Memory before optimization: 21.358366012573242 MB

Memory after optimization: 2.575934410095215 MB

Final memory: 2.385199546813965 MB

#### 1.1.3. Comprehensive Optimization for High-Frequency Trading Scenarios
1. **Chunked Reading + Predefined Types**
```python
# 读取1GB级交易日志时预定义类型
dtypes = {
    'symbol': 'category',
    'amount': 'float32',
    'position': 'int16',
```

---

```python
'trade_type': 'category'
}
chunks = pd.read_csv('trade_log.csv', chunksize=100000, dtype=dtypes)
processed_chunks = [chunk.groupby('symbol')['amount'].sum() 
for chunk in chunks]
final_result = pd.concat(processed_chunks)
```

2. **Accelerated Group Statistics**
```python
# 按证券代码统计交易量（提速5倍）
df['symbol'] = df['symbol'].cat.add_categories(['UNKNOWN'])  # 处理新增代码
trade_volume = df.groupby('symbol', observed=True)['position'].sum()
```

#### 1.1.4. Advanced Techniques
1. **Ordered Categories (Risk Level Analysis)**
```python
from pandas.api.types import CategoricalDtype

# 定义有序风险等级[5](@ref)
risk_order = CategoricalDtype(
    categories=['low', 'medium', 'high'], 
    ordered=True
)
df['risk_level'] = df['risk_level'].astype(risk_order)

# 筛选高风险交易（提速10倍）
   high_risk_trades = df[df['risk_level'] > 'medium']
```

2. **Boolean Type Compression (After-Hours Trading Marker)**
   
---

```python
# 生成盘后交易标记（内存减少87%）[4](@ref)
df['is_after_hours'] = df['trade_time'].apply(
    lambda x: x.hour < 9 or x.hour > 16
).astype('bool')
```

!!! Warning
    - **Dynamic Category Management**: When adding new security codes, call `df['symbol'].cat.add_categories(['NVDA'])`
    - **Numerical Overflow Risk**: If position size exceeds `int16` range (-32768~32767), switch to `int32`.
    - **Time Series Analysis**: `datetime` type supports efficient time window calculations (e.g., `.rolling('30T')`).
    
Through the above methods, significant optimization effects such as **memory reduction of 80%+** and **5-10x speedup in group operations** can be achieved in scenarios like high-frequency trading analysis and customer behavior profiling. For ultra-large-scale datasets (e.g., 1 billion-level transaction records), it is recommended to combine Dask or Modin for distributed computing.

### 1.2. Optimizing Iteration
Use `itertuples` instead of `iterrows`, and use `apply` to optimize iteration: filter first, then calculate. `itertuples` is much faster than `iterrows` because `itertuples` returns named tuples, whereas `iterrows` returns Series objects, which is much slower. A case study shows that processing 6 million rows with `iterrows` takes 335 seconds, while `itertuples` takes only 41 seconds, nearly 6 times faster.

#### 1.2.1. Performance Comparison and Optimization Principles of Iteration Methods
1. **Performance Difference Between `itertuples` and `iterrows`**

---

| Method | Data Structure | Time for 1M Rows | Applicable Scenario | Core Advantage |
| :----------: | :---------------------: | :--------: | :----------------------: | :--------------------------: |
| `iterrows` | Generates (index, Series) pairs | 85.938s | Simple traversal requiring row index | Intuitive and easy to use |
| `itertuples` | Generates named tuples | 7.656s | Large-scale data traversal | 50% less memory usage, 6x speedup |
| `apply` | Vectorized function application | 0.03s | Row-level calculations with complex conditional logic | Concise syntax, automatic type optimization |


!!! Notes
    - `iterrows` generates a Series object for each iteration, triggering memory allocation and type checking (object-oriented overhead).
    - `itertuples` returns a lightweight `namedtuple`, allowing direct data access via attributes (C-level optimization).

2. **Optimization Mechanism of `apply` Function**
```python
# 示例：计算股票交易费用（佣金率分档）
def calc_fee(row):
    if row['volume'] > 10000:
        return row['amount'] * 0.0002
    elif row['volume'] > 5000:
        return row['amount'] * 0.0003
    else:
        return row['amount'] * 0.0005

# 优化点：使用 axis=1 按行应用
df['fee'] = df.apply(calc_fee, axis=1)  # 比循环快3倍
```

#### 1.2.2. Comprehensive Optimization Case for Financial Data
1. **Generate Simulated High-Frequency Trading Data**
```python
# 生成100万条股票交易记录（含时间戳、代码、价格、成交量）
dates = pd.date_range('2025-03-28 09:30', periods=1_000_000, freq='S')
symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']
```

---

```python
df = pd.DataFrame({
    'symbol': np.random.choice(symbols, 1_000_000),
    'price': np.random.uniform(50, 500, 1_000_000).round(2),
    'volume': np.random.randint(100, 50_000, 1_000_000),
    'trade_type': np.random.choice(['buy', 'sell'], 1_000_000)
}, index=dates)

print("优化前内存：", df.memory_usage(deep=True).sum() / 1024**2, "MB")

# 内存优化：分类列转换
df['symbol'] = df['symbol'].astype('category')  # 内存减少85%
df['trade_type'] = df['trade_type'].astype('category')

print("优化后内存：", df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

Memory before optimization: 138.75994682312012 MB

Memory after optimization: 24.796205520629883 MB

2. `itertuples` in Action: Calculating Transaction Amounts
```python
# 传统 iterrows 写法（避免使用！）
import time
t1 = time.time()
total_amount = 0
for idx, row in df.iterrows():  # 预估耗时85秒
    total_amount += row['price'] * row['volume']
t2 = time.time()
print("传统 iterrows 写法：",t2-t1,"s")
```

---

```python
# 优化后 itertuples 写法
total_amount = 0
for row in df.itertuples():  # 耗时约7秒
    total_amount += row.price * row.volume
t3 = time.time()
print("优化后 itertuples 写法：",t3-t2,"s")

# 终极优化：向量化计算（推荐！）
df['amount'] = df['price'] * df['volume']  # 耗时0.03秒
t4 = time.time()
print("终极优化：向量化计算：",t4-t3,"s")
```

Traditional `iterrows` approach: 85.93825674057007 s

Optimized `itertuples` approach: 7.655602216720581 s

Ultimate Optimization: Vectorized Calculation: 0.032360076904296875 s

3. **`apply` in Action: Calculating Volatility Factor**
```python
def volatility_factor(row):  # 定义波动率计算函数
    if row['volume'] > 20000:
        return row['price'] * 0.015
    elif (row['volume'] > 10000) & (row['trade_type'] == 'buy'):
        return row['price'] * 0.010
    else:
        return row['price'] * 0.005
# 应用优化
t5 = time.time()
df['vol_factor'] = df.apply(volatility_factor, axis=1)  # 耗时约3秒
t6 = time.time()
print("定义波动率计算函数：",t6-t5,"s")
```

Defining volatility calculation function: 24.482948064804077 s

---

4. **Filter-Then-Calculate Strategy**
```python
# 非交易时段数据过滤（先筛选）
market_hours = df.between_time('09:30', '16:00')  # 减少30%数据量

# 仅处理大额交易（金额>100万）
large_trades = market_hours[market_hours['amount'] > 1_000_000]

# 分块处理（内存优化）
t7 = time.time()
chunks = (large_trades.groupby('symbol')
                    .apply(lambda x: x['amount'].mean())
                    .reset_index(name='avg_large_trade'))
t8 = time.time()

print("先筛选再计算策略：",t8-t7,"s")
```

Filter-Then-Calculate Strategy: 0.044037818908691406 s

`apply` can leverage internal optimizations and is faster than loops, but not as fast as vectorized operations.

#### 1.2.3. Performance Comparison and Best Practices

!!! Tip
    Best Practice Priority:
    ```1. Vectorized Operations > 2. itertuples > 3. apply > 4. iterrows```
    - Prioritize using `df['col'] = df['col1'] * df['col2']` format.
    - Replace loops with complex logic using `np.where()` or `pd.cut()`.


#### 1.2.4. Precautions

---

1. **Data Preprocessing**
    - Set timestamp as index:
        `df.set_index('timestamp', inplace=True)`
    - Convert numerical columns to minimum type:
        `df['volume'] = df['volume'].astype('int32')`

2. **Avoid Chained Indexing**

```python
# 错误写法（触发警告）
df[df['symbol'] == 'AAPL']['price'] = 200  

# 正确写法
df.loc[df['symbol'] == 'AAPL', 'price'] = 200  # 效率提升30%
```

3. **Memory Management**
    - Chunked reading:
        `pd.read_csv('trades.csv', chunksize=100000)`
    - Timely deletion of intermediate variables:
        `del temp_df` to release memory

Complete code examples can be tested via Jupyter Notebook. It is recommended to use financial high-frequency trading datasets (such as TAQ data) to verify optimization effects. For ultra-large-scale data (>100 million rows), it is recommended to combine Dask or Modin for distributed computing.

### 1.3. Using NumPy and Numba
#### 1.3.1. Core Principles and Advantages of Numba
Numba is a Python Just-In-Time (JIT) compiler that significantly improves computational efficiency by compiling Python functions into machine code, especially suitable for numerical calculations and NumPy array operations.

---

- **Just-In-Time Compilation**: Automatically optimizes functions via the `@jit` decorator, eliminating Python interpreter overhead.
- **Parallel Acceleration**: Implements multi-threaded parallel computing using `parallel=True` and `prange`.
- **GPU Support**: Offloads computation tasks to GPUs via `@cuda.jit`, suitable for ultra-large-scale data processing.

#### 1.3.2. Optimization Cases for Financial Data Processing
1. **Calculating Stock Return Volatility (Numba Accelerated)**
```python
import numpy as np
from numba import jit

# 生成金融数据：100万条股票价格序列
np.random.seed(42)
prices = np.random.normal(100, 5, 1_000_000).cumsum()

# 传统Python实现
def calc_volatility(prices):
    returns = np.zeros(len(prices)-1)
    for i in range(len(prices)-1):
        returns[i] = (prices[i+1] - prices[i]) / prices[i]
    return np.std(returns) * np.sqrt(252)

# Numba优化实现
@jit(nopython=True)
def calc_volatility_numba(prices):
    returns = np.zeros(len(prices)-1)
    for i in range(len(prices)-1):
        returns[i] = (prices[i+1] - prices[i]) / prices[i]
    return np.std(returns) * np.sqrt(252)

# 性能对比
%timeit calc_volatility(prices)    # 约 920 ms
%timeit calc_volatility_numba(prices)  # 约 7.3 ms
```

---

921 ms ± 87 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

7.27 ms ± 183 μs per loop (mean ± std. dev. of 7 runs, 1 loop each)

2. **Monte Carlo Option Pricing (Parallel Computing)**
```python
from numba import njit, prange

@njit(parallel=True)
def monte_carlo_pricing(S0, K, r, sigma, T, n_simulations):
    payoffs = np.zeros(n_simulations)
    for i in prange(n_simulations):
        ST = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*np.random.normal())
        payoffs[i] = max(ST - K, 0)
    return np.exp(-r*T) * np.mean(payoffs)

# 参数设置
params = (100, 105, 0.05, 0.2, 1, 1_000_000)
result = monte_carlo_pricing(*params)  # 约 320 ms（比纯Python快35倍）
```


#### 1.3.3. Key Optimization Strategies
1. **Data Type Specialization**
Force specification of input types to avoid dynamic checks:
```python
@jit(nopython=True, fastmath=True)
def vec_dot(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b)
```

---

2. **Memory Pre-allocation**
```python
@jit(nopython=True)
def moving_average(data, window):
    ma = np.empty(len(data) - window + 1)
    for i in range(len(ma)):
        ma[i] = np.mean(data[i:i+window])
    return ma
```

3. **Avoid Python Objects**
Disable Python objects in Numba functions (`nopython=True`) to ensure machine code execution throughout.


!!! Note
    Best Practices
    - Prioritize using `@njit` (equivalent to `@jit(nopython=True)`).
    - Use `prange` instead of `range` for large loops to achieve parallelism.
    - Secondary acceleration for `np.ufunc` functions (e.g., `np.sqrt`, `np.exp`).
    - Avoid mixing native Python types with NumPy types in JIT functions.

#### 1.3.4. Extended Applications
1. **Integration with Pandas**
```python
@jit
def pandas_apply_optimized(df: pd.DataFrame):
    return df['price'].values * df['volume'].values  # 直接操作Numpy数组
```

---

2. GPU Acceleration (CUDA)
```python
from numba import cuda

@cuda.jit
def cuda_matmul(A, B, C):
    i, j = cuda.grid(2)
    if i < C.shape[0] and j < C.shape[1]:
        tmp = 0.0
        for k in range(A.shape[1]):
            tmp += A[i, k] * B[k, j]
        C[i, j] = tmp
```

!!! Tip
    Precautions:
    - **Compilation Overhead**: The first run of a JIT function incurs compilation time; subsequent calls use the cache directly.
    - **Debugging Limitations**: Numba functions do not support `pdb` breakpoint debugging; intermediate values must be output via `print`.
    - **Compatibility**: Some advanced NumPy features (e.g., `np.linalg.svd`) are limited in Numba.

By reasonably utilizing NumPy's vectorized operations and Numba's JIT compilation, C-level performance can be achieved in financial quantitative analysis and high-frequency trading scenarios while maintaining Python's development efficiency. It is recommended to continuously optimize hot code by combining `%%timeit` and Numba's `cache=True` parameter.


---
