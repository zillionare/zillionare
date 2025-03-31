---
title: Pandas核心语法[6]
series: 量化人的 Numpy 和 Pandas
seq: "6"
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-16
date: 2025-04-02
category: tools
motto: Every adversity, every failure, every heartache carries with it the seed on an equivalent or greater benefit.
img: https://images.jieyu.ai/images/hot/mybook/three-books.png
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---

“Pandas 提供了强大的日期时间处理功能，从字符串到时间戳的转换、时区调整到格式化输出，都可以轻松实现。此外，字符串操作如替换、分割、过滤等，也能通过 str 访问器高效完成。”

---

## 1. 日期和时间

### 1.1. ​将字符串转换为日期时间格式
如果时间或日期数据是字符串格式，可以使用 `pd.to_datetime()` 函数将其转换为 Pandas 的 datetime 类型。

```python
import pandas as pd

# 示例数据
data = {'date': ['2023-01-01', '2023-02-01', '2023-03-01']}
df = pd.DataFrame(data)

# 将 'date' 列转换为 datetime 类型
df['date'] = pd.to_datetime(df['date'])
print(df)
```

输出：

```python
        date
0 2023-01-01
1 2023-02-01
2 2023-03-01
```

参数说明：
- format：指定日期字符串的格式，例如 '%Y-%m-%d'。

---

- errors：处理错误的方式，'raise'（报错）、'coerce'（将无效值转换为 NaT）、'ignore'（保留原值）。
- unit：指定时间单位，如 's'（秒）、'ms'（毫秒）。

### 1.2. ​处理多种日期格式
如果日期字符串有多种格式，可以通过 errors='coerce' 参数忽略无法解析的日期，或者使用 format 参数指定格式。

```python
data = {'date': ['2023-01-01', '01/02/2023', 'March 3, 2023']}
df = pd.DataFrame(data)

# 处理多种日期格式
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print(df)
```

输出：

```python
        date
0 2023-01-01
1 2023-01-02
2 2023-03-03
```

### 1.3. ​从时间戳转换
如果数据是时间戳（如 Unix 时间戳），可以使用 pd.to_datetime() 将其转换为 datetime 类型。

---

示例：

```python
data = {'timestamp': [1672531199, 1672617599, 1672703999]}
df = pd.DataFrame(data)

# 将时间戳转换为 datetime
df['date'] = pd.to_datetime(df['timestamp'], unit='s')
print(df)
```

输出：

```python
   timestamp                date
0  1672531199 2023-01-01 00:00:00
1  1672617599 2023-01-02 00:00:00
2  1672703999 2023-01-03 00:00:00
```

### 1.4. ​提取日期时间信息
转换后，可以使用 dt 访问器提取日期时间的各个部分，如年、月、日、小时等。

示例：

```python
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
print(df)
```

---

输出：

```python
                date  year  month  day
0 2023-01-01 00:00:00  2023      1    1
1 2023-01-02 00:00:00  2023      1    2
2 2023-01-03 00:00:00  2023      1    3
```

### 1.5. ​处理时区信息
如果数据包含时区信息，可以使用 tz_convert() 和 tz_localize() 进行时区转换。

示例：

```python
# 添加时区信息
df['date'] = pd.to_datetime(df['date']).dt.tz_localize('UTC')
# 转换为本地时区
df['date'] = df['date'].dt.tz_convert('Asia/Shanghai')
print(df)
```

### 1.6. ​将日期时间转换为字符串

如果需要将 datetime 类型转换为特定格式的字符串，可以使用 dt.strftime()。

示例：

---

```python
df['date_str'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
print(df)
```

输出：

```python
                date           date_str
0 2023-01-01 08:00:00  2023-01-01 08:00:00
1 2023-01-02 08:00:00  2023-01-02 08:00:00
2 2023-01-03 08:00:00  2023-01-03 08:00:00
```

## 2. 字符串操作

### 2.1. DataFrame 的字符串操作

在 Pandas 中，`DataFrame` 的字符串操作可以通过 `str` 访问器来实现。以下是一些常见的字符串操作方法：

#### 2.1.1. 转换为大写或小写

```python
df['column_name'] = df['column_name'].str.upper()  # 转换为大写
df['column_name'] = df['column_name'].str.lower()  # 转换为小写
```

#### 2.1.2. 替换子字符串

---

```python
df['column_name'] = df['column_name'].str.replace('old', 'new')  # 替换子字符串
```

#### 2.1.3. 提取子字符串

```python
df['new_column'] = df['column_name'].str[:3]  # 提取前 3 个字符
```

#### 2.1.4. 分割字符串
```python
df[['part1', 'part2']] = df['column_name'].str.split(' ', expand=True)  # 按空格分割
```

#### 2.1.5. 检查是否包含子字符串
```python
df['contains_substring'] = df['column_name'].str.contains('substring')  # 检查是否包含
```

#### 2.1.6. 计算字符串长度
```python
df['length'] = df['column_name'].str.len()  # 计算字符串长度
```

#### 2.1.7. 去除空格

```python
df['column_name'] = df['column_name'].str.strip()  # 去除两端空格
```

---

#### 2.1.8. 正则表达式匹配

```python
df['matches'] = df['column_name'].str.contains(r'\d')  # 检查是否包含数字
```

### 2.2. 排除科创板证券

科创板证券的代码通常以 `688` 开头。假设 `DataFrame` 中有一列 `code` 存放证券代码，可以通过以下方法排除科创板证券：

#### 方法 1：使用 ~ 和 str.startswith()

```python
df_filtered = df[~df['code'].str.startswith('688')]
```

#### 方法 2：使用 str.contains() 和正则表达式

```python
df_filtered = df[~df['code'].str.contains(r'^688')]
```

#### 方法 3：使用 query() 方法

```python
df_filtered = df.query("not code.str.startswith('688')", engine='python')
```

---

示例：

```python
import pandas as pd

# 示例数据
data = {'code': ['600001', '688001', '000001', '688002'], 'name': ['A', 'B', 'C', 'D']}
df = pd.DataFrame(data)

# 排除科创板
df_filtered = df[~df['code'].str.startswith('688')]
print(df_filtered)
```

输出：

```python
     code name
0  600001    A
2  000001    C
```

!!! Notes
    总结
    - **字符串操作**：通过 str 访问器可以实现大小写转换、替换、提取、分割、检查等操作。
    - **排除科创板**：使用 str.startswith() 或正则表达式过滤掉以 688 开头的证券代码。
