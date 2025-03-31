---
title: Pandas核心语法[5]
series: 量化人的 Numpy 和 Pandas
seq: "5"
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-15
date: 2025-04-01
category: tools
motto: Keep your face to the sunshine and you cannot see a shadow.
img: https://images.jieyu.ai/images/hot/mybook/gift.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---

“Pandas 提供了丰富的 IO 操作功能，支持从 CSV、SQL、Parquet 等多种文件格式中读取数据。通过优化参数如 chunksize、usecols 和 dtype，可以显著提升读取速度并减少内存占用。”

---

## 1. 数据预处理类
<!--_因子分析的预处理过程中，要进行缺失值、缩尾、去重等操作，怎么做？_
fillna, clip, winsorize,dropna-->
在 Pandas 中，DataFrame 的数据预处理是数据分析的关键步骤，包括数据清洗、缺失值处理、缩尾处理、去重等操作。**fillna**、**clip**、**winsorize** 和 **dropna** 是数据预处理中常用的函数，用于处理缺失值、极端值以及修剪数据范围。以下是它们的详细介绍和用法：

### 1.1. fillna：填充缺失值
fillna 用于填充 DataFrame 或 Series 中的缺失值（NaN）。它支持多种填充方式，例如用固定值、前向填充、后向填充、均值填充等。

语法：

```python
DataFrame.fillna(value=None, method=None, axis=None, inplace=False,
                 limit=None, downcast=None)
```

参数说明：
- ​**value**：用于填充缺失值的值，可以是标量、字典、Series 或 DataFrame。
- ​**method**：填充方法，可选 'ffill'（前向填充）、'bfill'（后向填充）。
- ​**axis**：填充的轴，0 表示按行填充，1 表示按列填充。
- ​**inplace**：是否原地修改数据，默认为 False。
- ​**limit**：限制填充的最大连续缺失值数量。

示例：
```python
import pandas as pd
import numpy as np

# 创建示例 DataFrame
data = {'A': [1, 2, np.nan], 'B': [np.nan, 5, 6]}
df = pd.DataFrame(data)
```

---

```python
# 用 0 填充缺失值
df_filled = df.fillna(0)

# 前向填充
df_ffill = df.fillna(method='ffill')

# 用均值填充
df_mean_filled = df.fillna(df.mean())
```

### 1.2. ​clip：修剪数据范围
clip 用于将数据限制在指定的范围内，超出范围的值会被替换为边界值。

```python
DataFrame.clip(lower=None, upper=None, axis=None, inplace=False)
```

参数说明：
- **lower**：下限值，低于此值的会被替换为下限。
- ​**upper**：上限值，高于此值的会被替换为上限。
- **axis**：修剪的轴，0 表示按行修剪，1 表示按列修剪。
- ​**inplace**：是否原地修改数据。

示例：

```python
# 将数据限制在 1 到 5 之间
df_clipped = df.clip(lower=1, upper=5)
```

---

```python
# 对每列设置不同的上下限
lower = pd.Series([1, 2])
upper = pd.Series([4, 5])
df_clipped_custom = df.clip(lower=lower, upper=upper, axis=1)
```

### 1.3. ​winsorize：缩尾处理
winsorize 用于处理极端值，将超出指定分位数的值替换为分位数的值。它通常用于减少极端值对数据分析的影响。语法（通过 scipy.stats.mstats.winsorize）：

```python
from scipy.stats.mstats import winsorize
winsorize(data, limits=[lower_limit, upper_limit])
```

参数说明：
- ​**limits**：指定上下分位数，例如 [0.05, 0.95] 表示将低于 5% 和高于 95% 的值替换为对应分位数的值。

示例：

```python
from scipy.stats.mstats import winsorize

# 对数据进行上下 5% 的缩尾处理
df['A_winsorized'] = winsorize(df['A'], limits=[0.05, 0.95])
```

---

### 1.4. ​**dropna：删除缺失值**
dropna 用于删除包含缺失值的行或列。

```python
DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
```

参数说明：
- **axis**：删除的轴，0 表示删除行，1 表示删除列。
- ​**how**：删除条件，'any'（默认）表示只要有一个缺失值就删除，'all' 表示只有全部为缺失值才删除。
- ​**thresh**：保留非缺失值的最小数量。
- ​**subset**：指定检查缺失值的列。
- ​**inplace**：是否原地修改数据。

示例：

```python
# 删除包含缺失值的行
df_dropped = df.dropna()

# 删除包含缺失值的列
df_dropped_cols = df.dropna(axis=1)

# 只删除指定列中包含缺失值的行
df_dropped_subset = df.dropna(subset=['A'])
```

---

!!! 总结
    - ​**fillna**：用于填充缺失值，支持多种填充方式。
    - **clip**：用于将数据限制在指定范围内，处理极端值。
    - **winsorize**：用于缩尾处理，减少极端值的影响。
    - **dropna**：用于删除包含缺失值的行或列。

## 2. IO 操作
<!--_如何将数据从csv,网页,数据库,parquet等地方读进来_-->
Pandas 中的 DataFrame 提供了丰富的 IO 操作功能，支持从多种文件格式中读取数据，并将数据写入到不同的文件格式中。

### 2.1. csv
<!--_除基本操作外，还将介绍读取 csv 时如何加速_-->
#### 2.1.1. 读取 csv
CSV 是最常用的文件格式之一，Pandas 提供了 `read_csv` 函数来读取 CSV 文件。
```python
import pandas as pd
df = pd.read_csv('data.csv')
```

常用参数：
- sep：指定分隔符，默认为逗号 ,。
- header：指定标题行，默认为 0（第一行）。

---

- index_col：指定哪一列作为索引。
- encoding：指定文件编码，如 utf-8 或 gbk。
- na_values：指定哪些值应被视为缺失值。

示例：

```python
df = pd.read_csv('data.csv', sep=';', header=0, index_col='ID', encoding='utf-8')
```

#### 2.1.2. 读取 csv 时如何加速
在读取大型 CSV 文件时，除了基本的 pd.read_csv 操作外，可以通过以下方法显著提升读取速度：

[分块读取 (chunksize)]

对于非常大的文件，一次性加载到内存可能会导致内存不足。可以使用 chunksize 参数分块读取数据，逐块处理。

```python
chunk_size = 10000  # 每次读取 10000 行
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process(chunk)  # 自定义处理函数
```

这种方法可以有效减少内存占用，并允许边读边处理。

[指定列读取 (usecols)]

如果只需要部分列的数据，可以使用 usecols 参数指定要读取的列，避免加载不必要的数据。

---

```python
df = pd.read_csv('large_file.csv', usecols=['column1', 'column2'])
```

这样可以减少内存使用并加快读取速度。

[优化数据类型 (dtype)]

Pandas 默认会推断每列的数据类型，但这可能会导致内存浪费。通过显式指定 dtype，可以减少内存占用并提升性能。

```python
dtypes = {'column1': 'int32', 'column2': 'float32'}
df = pd.read_csv('large_file.csv', dtype=dtypes)
```

例如，将 int64 改为 int32 可以节省内存。

[使用更高效的解析器 (engine='pyarrow')]

Pandas 1.4 版本引入了 pyarrow 作为 CSV 解析器，相比默认的解析器，速度更快。

```python
df = pd.read_csv('large_file.csv', engine='pyarrow')
```

pyarrow 支持并行解析，特别适合处理**大文件**。

[​跳过无用数据 (skiprows, nrows)]

如果文件中有不需要的行或数据，可以使用 skiprows 跳过指定行，或使用 nrows 只读取前几行。

---

```python
df = pd.read_csv('large_file.csv', skiprows=[1, 2], nrows=1000)
```

这样可以减少数据处理量。

[​并行处理 (Dask 或 Multiprocessing)]

对于非常大的数据集，可以使用并行处理工具如 Dask 来加速读取和处理。

```python
import dask.dataframe as dd
df = dd.read_csv('large_file.csv')
result = df.groupby('column1').mean().compute()
```

Dask 会自动将文件分块并并行处理。

[​使用更高效的文件格式 (如 Parquet)]

如果可能，将 CSV 文件转换为 Parquet 格式，Parquet 是一种列式存储格式，读取速度更快。

```python
df = pd.read_parquet('large_file.parquet', engine='fastparquet')
```

Parquet 文件不仅读取速度快，还能显著减少存储空间。

[​内存映射文件 (memory_map)]

---

对于特别大的文件，可以使用 memory_map 参数将文件映射到内存中，减少内存占用。

```python
df = pd.read_csv('large_file.csv', memory_map=True)
```

这种方法适合处理**超大型文件**。

#### 2.1.3. 写入 csv
使用 to_csv 函数将数据写入 CSV 文件。

```python
df.to_csv('output.csv', index=False)
```


常用参数：
- index：是否写入索引，默认为 True。
- header：是否写入列名，默认为 True。
- encoding：指定文件编码。

### 2.2. pkl 和 hdf5
在 Pandas 中，DataFrame 可以方便地对 .pkl 和 .hdf5 文件进行读写操作。以下是详细的方法和示例：
​
.pkl 文件是 Python 的序列化文件格式，通常用于保存和加载 Python 对象，包括 DataFrame。使用 `read_pickle` 方法从 .pkl 文件中加载 DataFrame，使用 `to_pickle` 方法将 DataFrame 保存为 .pkl 文件。

---

```python
import pandas as pd

# 创建示例 DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# 保存为 .pkl 文件
df.to_pickle('data.pkl')

# 从 .pkl 文件加载 DataFrame
df = pd.read_pickle('data.pkl')
print(df)
```

.hdf5 是一种高效的存储格式，适合存储大规模数据。Pandas 提供了 HDFStore 和 to_hdf/read_hdf 方法来操作 .hdf5 文件。
```python
# 保存为 .hdf5 文件
df.to_hdf('data.h5', key='df', mode='w')

# 从 .hdf5 文件加载 DataFrame
df = pd.read_hdf('data.h5', key='df')
print(df)
```

HDFStore 提供了更灵活的操作方式，支持多个数据集的存储和读取：
```python
# 创建 HDFStore 对象
store = pd.HDFStore('data.h5')
```

---

```python
# 存储多个 DataFrame
store.put('df1', df1)
store.put('df2', df2)

# 读取特定 DataFrame
df1 = store['df1']
df2 = store.get('df2')

# 关闭 HDFStore
store.close()
```

!!! Notes
    总结：
    - **.pkl 文件**：适合保存和加载单个 DataFrame，操作简单。
    - **.hdf5 文件**：适合存储大规模数据，支持多个数据集和高效压缩。

### 2.3. parquet
Pandas 支持读取 Parquet 文件，使用 read_parquet 函数。
```python
import pandas as pd
df = pd.read_parquet('data.parquet')
```

常用参数：
- engine：指定引擎，如 pyarrow 或 fastparquet。
- columns：指定要读取的列。

---

示例：
```python
df = pd.read_parquet('data.parquet', engine='pyarrow', columns=['col1', 'col2'])
```

### 2.4. html 和 md
<!--换个思路，就是爬虫-->
Pandas 的 read_html 函数可以从网页中读取 HTML 表格数据。
```python
url = 'http://example.com/table.html'
tables = pd.read_html(url)
df = tables[0]  # 获取第一个表格
```

如果需要处理复杂的网页数据，可以结合 `requests` 和 `BeautifulSoup` 库：

```python
import requests
from bs4 import BeautifulSoup

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))[0]
```

---

### 2.5. sql
Pandas 支持从 SQL 数据库中读取数据，使用 read_sql 函数。
```python
import sqlite3

# 连接到数据库
conn = sqlite3.connect('database.db')

# 执行 SQL 查询并读取数据
df = pd.read_sql('SELECT * FROM table_name', conn)

# 关闭数据库连接
conn.close()
```

如果需要连接其他数据库（如 MySQL、PostgreSQL），可以使用相应的数据库驱动（如 pymysql、psycopg2）。
