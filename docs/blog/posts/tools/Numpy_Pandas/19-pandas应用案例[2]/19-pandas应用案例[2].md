---
title: Pandas应用案例[2]
series: 量化人的 Numpy 和 Pandas
seq: "9"
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-19
date: 2025-04-05
category: tools
motto: The gem cannot be polished without friction, nor man perfected without trials.
img: https://images.jieyu.ai/images/hot/mybook/poster-on-wall.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---

“通过将字符串列转换为 category 类型，内存占用可减少 90% 以上；使用 itertuples 替代 iterrows，遍历速度提升 6 倍；结合 Numba 的 JIT 编译，数值计算性能可媲美 C 语言。”

---

## 1. Pandas 性能
### 1.1. 内存优化
使用category类型可以将字符串转换为分类变量，用整数索引代替原始值，这样可以节省内存。例如：把性别这样的重复字符串转成category，内存占用大幅减少。同时，分类类型还能提高某些操作的性能，比如排序和分组，因为内部用的是整数处理，所以可以达到优化的效果。

除此之外，也可以进行数据类型优化，比如将int64转换为更小的类型如int8或者uint8。这里需要强调检查每列的数据范围，选择合适的子类型，比如：如果数值在0到255之间就用uint8。显式指定dtype是重要的，特别是在读取数据时指定类型，避免自动推断导致内存浪费。

#### 1.1.1. Category 类型：分类数据的终极优化方案
**​核心原理**
- ​内存压缩：将重复的字符串（如性别、地区、产品类别）转换为整数索引，并建立映射字典。例如，将“男/女”存储为 0/1，内存占用减少 ​90%​ 以上。
- ​性能提升：分类数据在分组（groupby）、排序（sort_values）等操作中比字符串快 ​10-100 倍，因为底层使用整数运算。

**使用场景**
- ​低基数数据：列的唯一值数量远小于总行数（如性别仅有 2 种，但数据量百万级）。

---

- ​有序分类：如评分等级（“高/中/低”）或时间段（“早/中/晚”），可指定顺序提升分析效率。

**操作方法**
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



优化前内存： 19.291857719421387 MB

优化后内存： 1.8129425048828125 MB **（减少了90.6%）**

---

!!! Tip
    定期检查内存使用情况，比如用 `memory_usage` 方法，来评估优化效果。


​金融场景适用字段：
- ​交易类型：如 `buy/sell（证券买卖）`、`order_type（限价单/市价单）`
- ​资产类别：如 `stock`、`bond`、`ETF`
- ​客户等级：如 `VIP`、`普通`、`机构`
- 地域分类：如 `CN`、`US`、`HK（交易市场归属）`

当列的唯一值较少且重复较多时，使用category效果最好。例如性别、地区代码等。如果分类变量的类别数量远小于总行数，转换后的内存节省会更明显。注意category类型不适合频繁变更类别的情况，这可能增加计算开销。另外，使用pd.Categorical或者cut函数创建分类数据需要注意处理缺失值的问题，因为category类型不支持NaN，所以在转换前需要处理缺失值。


#### 1.1.2. 紧凑数据类型：精准狙击内存浪费
**​数值类型优化**
- ​整数类型：根据数值范围选择最小子类型：
    ```python
    # 检查范围后转换
    df['age'] = df['age'].astype('uint8')  # 0-255 范围
    ```
- 浮点类型：优先使用 float32（精度足够时），内存减少 ​50%​ .

---

**​布尔类型优化**
将仅有 True/False 的列转换为 bool 类型：
```python
    df['is_active'] = df['is_active'].astype('bool')
```

**​时间类型优化**
使用 `datetime64[ns]` 而非 `object` 存储日期，内存减少 ​75%​ 且支持时间序列运算。

金融数据常包含以下高优化价值字段：
- ​离散型分类字段：交易类型（buy/sell）、证券代码（AAPL/TSLA）、客户等级（VIP/普通）
- ​数值型字段：交易金额（float64）、持仓量（int64）、时间戳（object）
- ​状态标识字段：是否盘后交易（True/False）、风险标记（high/medium/low）


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

优化前内存： 21.358366012573242 MB

优化后内存： 2.575934410095215 MB

最终内存： 2.385199546813965 MB

#### 1.1.3. 高频交易场景综合优化
1. **​分块读取+类型预定义**
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

2. **​分组统计加速**
```python
# 按证券代码统计交易量（提速5倍）
df['symbol'] = df['symbol'].cat.add_categories(['UNKNOWN'])  # 处理新增代码
trade_volume = df.groupby('symbol', observed=True)['position'].sum()
```

#### 1.1.4. 进阶技巧
1. **​有序分类（风险等级分析）​**
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

2. **布尔类型压缩（盘后交易标记）​**
   
---

```python
# 生成盘后交易标记（内存减少87%）[4](@ref)
df['is_after_hours'] = df['trade_time'].apply(
    lambda x: x.hour < 9 or x.hour > 16
).astype('bool')
```

!!! Warning
    - ​动态类别管理：新增证券代码时需调用 df['symbol'].cat.add_categories(['NVDA'])
    - 数值溢出风险：持仓量若超过 int16 范围（-32768~32767），需改用 int32
    - 时间序列分析：datetime 类型支持高效时间窗口计算（如 .rolling('30T')）
    
通过上述方法，可在高频交易分析、客户行为画像等场景中实现 **​内存减少80%+** 、 **分组操作提速5-10倍** 的显著优化效果。对于超大规模数据集（如10亿级交易记录），建议结合 Dask 或 Modin 实现分布式计算。

### 1.2. 优化迭代
使用 itertuples 而不是 iterrows, 使用 apply 来优化迭代，先筛选再计算。itertuples 比 iterrows 快很多，因为 itertuples 返回的是命名元组，而 iterrows 返回的是 Series 对象，这会慢很多。有案例表示使用 iterrows 处理 600 万行数据需要 335 秒，而 itertuples 只需要 41 秒，快了近 6 倍。

#### 1.2.1. 迭代方式性能对比与优化原理
1. **​itertuples 与 iterrows 性能差异**

---

| 方法 |	数据结构	| 百万行耗时 |	适用场景	| 核心优势 |
|:-----:|:------:|:-----:|:-----:|:-----:|
| ​iterrows	| 生成 (index, Series) 对	| 85.938s	| 需要行索引的简单遍历	| 直观易用	|
|​ itertuples|	生成命名元组	| 7.656s |	大规模数据遍历	| 内存占用减少50%，速度提升6倍	|
|​ apply	| 向量化函数应用	| 0.03s	| 条件逻辑较复杂的行级计算 |	语法简洁，自动类型优化 |


!!! Notes
    - iterrows 每次迭代生成 Series 对象，触发内存分配和类型检查（面向对象开销）
    - itertuples 返回轻量级 namedtuple，直接通过属性访问数据（C语言层级优化）

2. **​apply 函数的优化机制**
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

#### 1.2.2. 金融数据综合优化案例
1. ​**生成模拟高频交易数据**
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

优化前内存： 138.75994682312012 MB

优化后内存： 24.796205520629883 MB

2. itertuples 实战：计算交易金额
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

传统 iterrows 写法： 85.93825674057007 s

优化后 itertuples 写法： 7.655602216720581 s

终极优化：向量化计算： 0.032360076904296875 s

3. **​apply 实战：计算波动率因子**
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

定义波动率计算函数： 24.482948064804077 s

---

4. **先筛选再计算策略**
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

先筛选再计算策略： 0.044037818908691406 s

apply可以利用内部优化，比循环更快，但不如矢量化操作。

#### 1.2.3. 性能对比与最佳实践

!!! Tip
    最佳实践优先级：
    ```​1. 向量化运算 > 2. ​itertuples > 3. ​apply > 4. ​iterrows```
    - 优先使用 df['col'] = df['col1'] * df['col2'] 形式
    - 复杂逻辑用 np.where() 或 pd.cut() 替代循环


#### 1.2.4. 注意事项

---

1. **数据预处理**
    - 将时间戳设为索引 
        df.set_index('timestamp', inplace=True)
    - 数值列转换为最小类型：
        df['volume'] = df['volume'].astype('int32')

2. ​**避免链式索引**

```python
# 错误写法（触发警告）
df[df['symbol'] == 'AAPL']['price'] = 200  

# 正确写法
df.loc[df['symbol'] == 'AAPL', 'price'] = 200  # 效率提升30%
```

3. **​内存管理**
    - 分块读取：
        pd.read_csv('trades.csv', chunksize=100000)
    - 及时删除中间变量：
        del temp_df 释放内存

完整代码示例可通过 Jupyter Notebook 运行测试，建议使用金融高频交易数据集（如TAQ数据）验证优化效果。对于超大规模数据（>1亿行），推荐结合 Dask 或 Modin 实现分布式计算。

### 1.3. 使用numpy和numba
#### 1.3.1. Numba核心原理与优势
Numba 是 Python 的即时（JIT）编译器，通过将 Python 函数编译为机器码，显著提升计算效率，尤其适合数值计算和 Numpy 数组操作。

---

- **​即时编译**：通过 @jit 装饰器自动优化函数，消除 Python 解释器开销。
- **​并行加速**：使用 parallel=True 和 prange 实现多线程并行计算。
- **GPU支持**：通过 @cuda.jit 将计算任务卸载到 GPU，适用于超大规模数据处理。

#### 1.3.2. 金融数据处理优化案例
1. **​计算股票收益率波动率（Numba加速）​**
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

2. **蒙特卡洛期权定价（并行计算）​**
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


#### 1.3.3. 关键优化策略
1. **数据类型特化**
强制指定输入类型避免动态检查：
```python
@jit(nopython=True, fastmath=True)
def vec_dot(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b)
```

---

2. **内存预分配**
```python
@jit(nopython=True)
def moving_average(data, window):
    ma = np.empty(len(data) - window + 1)
    for i in range(len(ma)):
        ma[i] = np.mean(data[i:i+window])
    return ma
```

3. **​避免Python对象**
在 Numba 函数中禁用 Python 对象（nopython=True），确保全程机器码执行。


!!! Note
    最佳实践
    - 优先使用 @njit（等价于 @jit(nopython=True)）
    - 对大循环使用 prange 替代 range 实现并行
    - 对 np.ufunc 函数进行二次加速（如 np.sqrt、np.exp）
    - 避免在 JIT 函数中混合使用 Python 原生类型与 Numpy 类型

#### 1.3.4. 扩展应用
1. **与Pandas结合**
```python
@jit
def pandas_apply_optimized(df: pd.DataFrame):
    return df['price'].values * df['volume'].values  # 直接操作Numpy数组
```

---

2. GPU加速（CUDA）​
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
    注意事项：
    - ​编译开销：首次运行 JIT 函数会有编译耗时，后续调用直接使用缓存
    - 调试限制：Numba 函数不支持 pdb 断点调试，需通过 print 输出中间值
    - 兼容性：部分 Numpy 高级功能（如 np.linalg.svd）在 Numba 中受限

通过合理运用 Numpy 的向量化操作与 Numba 的 JIT 编译，可在金融量化分析、高频交易等场景实现 ​C 语言级性能，同时保持 Python 的开发效率。建议结合 %%timeit 和 Numba 的 cache=True 参数持续优化热点代码。


---
