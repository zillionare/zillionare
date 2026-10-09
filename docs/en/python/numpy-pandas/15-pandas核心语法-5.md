---
title: "Pandas Core Syntax 5: Data Preprocessing & High-Performance IO"
date: 2025-04-01
slug: en/articles/python/numpy-pandas/15-pandas核心语法-5
tags: [Pandas, Data Preprocessing, Quantitative IO, Performance Optimization]
excerpt: "Master Pandas data preprocessing with fillna, clip, and winsorize. Optimize IO operations for CSV, Parquet, and SQL using chunksize, dtype, and pyarrow for faster, memory-efficient quantitative data pipelines."
lang: en
translation_of: articles/python/numpy-pandas/15-pandas核心语法-5
auto_translated: true
source_sha: 650e223fb607f7d580708cf03aa44e03b20eaba6
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/gift.jpg"
---

“Pandas 提供了丰富的 IO 操作功能，支持从 CSV、SQL、Parquet 等多种文件格式中读取数据。通过优化参数如 chunksize、usecols 和 dtype，可以显著提升读取速度并减少内存占用。”

---

## 1. Data Preprocessing
<!--_In the preprocessing phase of factor analysis, how do we handle missing values, outlier clipping, and deduplication?_
fillna, clip, winsorize, dropna-->
In Pandas, DataFrame data preprocessing is a critical step in data analysis, encompassing data cleaning, missing value handling, outlier clipping, and deduplication. **fillna**, **clip**, **winsorize**, and **dropna** are commonly used functions for handling missing values, extreme values, and data range trimming. Below is a detailed introduction to their usage:

### 1.1. fillna: Filling Missing Values
`fillna` is used to fill missing values (NaN) in a DataFrame or Series. It supports various filling methods, such as using a fixed value, forward fill, backward fill, or mean fill.

Syntax:

```python
DataFrame.fillna(value=None, method=None, axis=None, inplace=False,
                 limit=None, downcast=None)
```

Parameter Description:
- **value**: The value used to fill missing values, which can be a scalar, dictionary, Series, or DataFrame.
- **method**: The filling method, optional 'ffill' (forward fill) or 'bfill' (backward fill).
- **axis**: The axis along which to fill, 0 for row-wise filling, 1 for column-wise filling.
- **inplace**: Whether to modify the data in place, default is False.
- **limit**: The maximum number of consecutive missing values to fill.

Example:
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

### 1.2. clip: Trimming Data Range
`clip` is used to restrict data to a specified range, replacing values outside the range with the boundary values.

```python
DataFrame.clip(lower=None, upper=None, axis=None, inplace=False)
```

Parameter Description:
- **lower**: The lower bound; values below this will be replaced by the lower bound.
- **upper**: The upper bound; values above this will be replaced by the upper bound.
- **axis**: The axis along which to clip, 0 for row-wise clipping, 1 for column-wise clipping.
- **inplace**: Whether to modify the data in place.

Example:

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

### 1.3. winsorize: Outlier Clipping
`winsorize` is used to handle extreme values by replacing values beyond specified quantiles with the quantile values. It is typically used to reduce the impact of extreme values on data analysis. Syntax (via `scipy.stats.mstats.winsorize`):

```python
from scipy.stats.mstats import winsorize
winsorize(data, limits=[lower_limit, upper_limit])
```

Parameter Description:
- **limits**: Specifies the upper and lower quantiles, e.g., [0.05, 0.95] indicates replacing values below the 5th percentile and above the 95th percentile with the corresponding quantile values.

Example:

```python
from scipy.stats.mstats import winsorize

# 对数据进行上下 5% 的缩尾处理
df['A_winsorized'] = winsorize(df['A'], limits=[0.05, 0.95])
```

---

### 1.4. **dropna: Deleting Missing Values**
`dropna` is used to delete rows or columns containing missing values.

```python
DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
```

Parameter Description:
- **axis**: The axis along which to drop, 0 for deleting rows, 1 for deleting columns.
- **how**: The deletion condition, 'any' (default) means delete if any missing value exists, 'all' means delete only if all values are missing.
- **thresh**: The minimum number of non-missing values to retain.
- **subset**: Specifies the columns to check for missing values.
- **inplace**: Whether to modify the data in place.

Example:

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
    - **fillna**: Used to fill missing values, supporting various filling methods.
    - **clip**: Used to restrict data to a specified range, handling extreme values.
    - **winsorize**: Used for outlier clipping, reducing the impact of extreme values.
    - **dropna**: Used to delete rows or columns containing missing values.

## 2. IO Operations
<!--_How to import data from CSV, web pages, databases, Parquet, etc.?_-->
Pandas DataFrames provide rich IO operation capabilities, supporting reading data from various file formats and writing data to different file formats.

### 2.1. CSV
<!--_In addition to basic operations, we will also introduce how to accelerate CSV reading._-->
#### 2.1.1. Reading CSV
CSV is one of the most commonly used file formats. Pandas provides the `read_csv` function to read CSV files.
```python
import pandas as pd
df = pd.read_csv('data.csv')
```

Common Parameters:
- sep: Specifies the delimiter, default is comma `,`.
- header: Specifies the header row, default is 0 (first row).

---

- index_col: Specifies which column to use as the index.
- encoding: Specifies the file encoding, such as utf-8 or gbk.
- na_values: Specifies which values should be treated as missing values.

Example:

```python
df = pd.read_csv('data.csv', sep=';', header=0, index_col='ID', encoding='utf-8')
```

#### 2.1.2. Accelerating CSV Reading
When reading large CSV files, in addition to basic `pd.read_csv` operations, you can significantly improve reading speed using the following methods:

[Chunked Reading (chunksize)]

For very large files, loading them entirely into memory may cause memory overflow. You can use the `chunksize` parameter to read data in chunks and process them piece by piece.

```python
chunk_size = 10000  # 每次读取 10000 行
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process(chunk)  # 自定义处理函数
```

This method effectively reduces memory usage and allows for processing while reading.

[Specifying Columns to Read (usecols)]

If you only need data from specific columns, you can use the `usecols` parameter to specify which columns to read, avoiding loading unnecessary data.

---

```python
df = pd.read_csv('large_file.csv', usecols=['column1', 'column2'])
```

This reduces memory usage and accelerates reading speed.

[Optimizing Data Types (dtype)]

Pandas infers the data type of each column by default, which may lead to memory waste. By explicitly specifying `dtype`, you can reduce memory usage and improve performance.

```python
dtypes = {'column1': 'int32', 'column2': 'float32'}
df = pd.read_csv('large_file.csv', dtype=dtypes)
```

For example, changing `int64` to `int32` can save memory.

[Using a More Efficient Parser (engine='pyarrow')]

Pandas version 1.4 introduced `pyarrow` as a CSV parser, which is faster than the default parser.

```python
df = pd.read_csv('large_file.csv', engine='pyarrow')
```

`pyarrow` supports parallel parsing, making it particularly suitable for processing **large files**.

[Skipping Unnecessary Data (skiprows, nrows)]

If a file contains unnecessary rows or data, you can use `skiprows` to skip specified rows or `nrows` to read only the first few rows.

---

```python
df = pd.read_csv('large_file.csv', skiprows=[1, 2], nrows=1000)
```

This reduces the amount of data processing.

[Parallel Processing (Dask or Multiprocessing)]

For very large datasets, you can use parallel processing tools like Dask to accelerate reading and processing.

```python
import dask.dataframe as dd
df = dd.read_csv('large_file.csv')
result = df.groupby('column1').mean().compute()
```

Dask automatically chunks the file and processes it in parallel.

[Using More Efficient File Formats (e.g., Parquet)]

If possible, convert CSV files to Parquet format. Parquet is a columnar storage format with faster reading speeds.

```python
df = pd.read_parquet('large_file.parquet', engine='fastparquet')
```

Parquet files not only read faster but also significantly reduce storage space.

[Memory-Mapped Files (memory_map)]

---

For exceptionally large files, you can use the `memory_map` parameter to map the file to memory, reducing memory usage.

```python
df = pd.read_csv('large_file.csv', memory_map=True)
```

This method is suitable for processing **ultra-large files**.

#### 2.1.3. Writing CSV
Use the `to_csv` function to write data to a CSV file.

```python
df.to_csv('output.csv', index=False)
```


Common Parameters:
- index: Whether to write the index, default is True.
- header: Whether to write column names, default is True.
- encoding: Specifies the file encoding.

### 2.2. pkl and hdf5
In Pandas, DataFrames can conveniently read and write `.pkl` and `.hdf5` files. Below are the detailed methods and examples:

`.pkl` files are Python serialization file formats, commonly used for saving and loading Python objects, including DataFrames. Use the `read_pickle` method to load a DataFrame from a `.pkl` file, and the `to_pickle` method to save a DataFrame as a `.pkl` file.

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

`.hdf5` is an efficient storage format suitable for storing large-scale data. Pandas provides `HDFStore` and `to_hdf`/`read_hdf` methods to operate on `.hdf5` files.
```python
# 保存为 .hdf5 文件
df.to_hdf('data.h5', key='df', mode='w')

# 从 .hdf5 文件加载 DataFrame
df = pd.read_hdf('data.h5', key='df')
print(df)
```

`HDFStore` provides more flexible operation methods, supporting the storage and reading of multiple datasets:
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
    Summary:
    - **.pkl files**: Suitable for saving and loading individual DataFrames, with simple operations.
    - **.hdf5 files**: Suitable for storing large-scale data, supporting multiple datasets and efficient compression.

### 2.3. Parquet
Pandas supports reading Parquet files using the `read_parquet` function.
```python
import pandas as pd
df = pd.read_parquet('data.parquet')
```

Common Parameters:
- engine: Specifies the engine, such as `pyarrow` or `fastparquet`.
- columns: Specifies the columns to read.

---

Example:
```python
df = pd.read_parquet('data.parquet', engine='pyarrow', columns=['col1', 'col2'])
```

### 2.4. HTML and Markdown
<!--Alternative approach: Web Scraping-->
Pandas' `read_html` function can read HTML table data from web pages.
```python
url = 'http://example.com/table.html'
tables = pd.read_html(url)
df = tables[0]  # 获取第一个表格
```

If you need to process complex web data, you can combine `requests` and `BeautifulSoup` libraries:

```python
import requests
from bs4 import BeautifulSoup

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))[0]
```

---

### 2.5. SQL
Pandas supports reading data from SQL databases using the `read_sql` function.
```python
import sqlite3

# 连接到数据库
conn = sqlite3.connect('database.db')

# 执行 SQL 查询并读取数据
df = pd.read_sql('SELECT * FROM table_name', conn)

# 关闭数据库连接
conn.close()
```

If you need to connect to other databases (such as MySQL, PostgreSQL), you can use the corresponding database drivers (such as `pymysql`, `psycopg2`).
