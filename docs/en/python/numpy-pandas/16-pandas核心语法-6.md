---
title: "Pandas Essentials: Datetime & String Ops for Quant Data"
date: 2025-04-02
slug: en/articles/python/numpy-pandas/16-pandas核心语法-6
tags: [Pandas, Data Preprocessing, Quantitative Finance, Data Engineering]
excerpt: "Master Pandas datetime parsing, timezone handling, and string manipulation for robust quantitative data preprocessing and factor engineering workflows."
lang: en
translation_of: articles/python/numpy-pandas/16-pandas核心语法-6
auto_translated: true
source_sha: 00970d024e5903ac0a4a74744ef4d40f44f5d10b
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/three-books.png"
---

“Pandas offers robust datetime handling, enabling seamless conversion from strings to timestamps, timezone adjustments, and formatted output. Additionally, string operations such as replacement, splitting, and filtering are efficiently executed via the `str` accessor.”

---

## 1. Datetime and Time

### 1.1. Converting Strings to Datetime
If time or date data is in string format, use the `pd.to_datetime()` function to convert it to Pandas’ datetime type.

```python
import pandas as pd

# 示例数据
data = {'date': ['2023-01-01', '2023-02-01', '2023-03-01']}
df = pd.DataFrame(data)

# 将 'date' 列转换为 datetime 类型
df['date'] = pd.to_datetime(df['date'])
print(df)
```

Output:

```python
        date
0 2023-01-01
1 2023-02-01
2 2023-03-01
```

Parameter explanations:
- `format`: Specifies the format of the date string, e.g., `'%Y-%m-%d'`.

---

- `errors`: Defines how to handle errors: `'raise'` (raise an error), `'coerce'` (convert invalid values to NaT), or `'ignore'` (keep original values).
- `unit`: Specifies the time unit, such as `'s'` (seconds) or `'ms'` (milliseconds).

### 1.2. Handling Multiple Date Formats
If date strings have multiple formats, you can ignore unparseable dates using `errors='coerce'` or specify the format using the `format` parameter.

```python
data = {'date': ['2023-01-01', '01/02/2023', 'March 3, 2023']}
df = pd.DataFrame(data)

# 处理多种日期格式
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print(df)
```

Output:

```python
        date
0 2023-01-01
1 2023-01-02
2 2023-03-03
```

### 1.3. Converting from Timestamps
If data is in timestamp format (e.g., Unix timestamps), use `pd.to_datetime()` to convert it to datetime type.

---

Example:

```python
data = {'timestamp': [1672531199, 1672617599, 1672703999]}
df = pd.DataFrame(data)

# 将时间戳转换为 datetime
df['date'] = pd.to_datetime(df['timestamp'], unit='s')
print(df)
```

Output:

```python
   timestamp                date
0  1672531199 2023-01-01 00:00:00
1  1672617599 2023-01-02 00:00:00
2  1672703999 2023-01-03 00:00:00
```

### 1.4. Extracting Datetime Information
After conversion, use the `dt` accessor to extract specific components of the datetime, such as year, month, day, or hour.

Example:

```python
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
print(df)
```

---

Output:

```python
                date  year  month  day
0 2023-01-01 00:00:00  2023      1    1
1 2023-01-02 00:00:00  2023      1    2
2 2023-01-03 00:00:00  2023      1    3
```

### 1.5. Handling Timezone Information
If data includes timezone information, use `tz_convert()` and `tz_localize()` for timezone conversion.

Example:

```python
# 添加时区信息
df['date'] = pd.to_datetime(df['date']).dt.tz_localize('UTC')
# 转换为本地时区
df['date'] = df['date'].dt.tz_convert('Asia/Shanghai')
print(df)
```

### 1.6. Converting Datetime to Strings

If you need to convert datetime type to a specific string format, use `dt.strftime()`.

Example:

---

```python
df['date_str'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
print(df)
```

Output:

```python
                date           date_str
0 2023-01-01 08:00:00  2023-01-01 08:00:00
1 2023-01-02 08:00:00  2023-01-02 08:00:00
2 2023-01-03 08:00:00  2023-01-03 08:00:00
```

## 2. String Operations

### 2.1. String Operations on DataFrame

In Pandas, string operations on a `DataFrame` can be performed using the `str` accessor. Below are some common string operation methods:

#### 2.1.1. Converting to Uppercase or Lowercase

```python
df['column_name'] = df['column_name'].str.upper()  # 转换为大写
df['column_name'] = df['column_name'].str.lower()  # 转换为小写
```

#### 2.1.2. Replacing Substrings

---

```python
df['column_name'] = df['column_name'].str.replace('old', 'new')  # 替换子字符串
```

#### 2.1.3. Extracting Substrings

```python
df['new_column'] = df['column_name'].str[:3]  # 提取前 3 个字符
```

#### 2.1.4. Splitting Strings
```python
df[['part1', 'part2']] = df['column_name'].str.split(' ', expand=True)  # 按空格分割
```

#### 2.1.5. Checking for Substring Inclusion
```python
df['contains_substring'] = df['column_name'].str.contains('substring')  # 检查是否包含
```

#### 2.1.6. Calculating String Length
```python
df['length'] = df['column_name'].str.len()  # 计算字符串长度
```

#### 2.1.7. Removing Whitespace

```python
df['column_name'] = df['column_name'].str.strip()  # 去除两端空格
```

---

#### 2.1.8. Regular Expression Matching

```python
df['matches'] = df['column_name'].str.contains(r'\d')  # 检查是否包含数字
```

### 2.2. Excluding STAR Market Securities

STAR Market (Shanghai Stock Exchange Science and Technology Innovation Board) securities typically have codes starting with `688`. Assuming a `DataFrame` column named `code` holds security codes, you can exclude STAR Market securities using the following methods:

#### Method 1: Using `~` and `str.startswith()`

```python
df_filtered = df[~df['code'].str.startswith('688')]
```

#### Method 2: Using `str.contains()` and Regular Expressions

```python
df_filtered = df[~df['code'].str.contains(r'^688')]
```

#### Method 3: Using the `query()` Method

```python
df_filtered = df.query("not code.str.startswith('688')", engine='python')
```

---

Example:

```python
import pandas as pd

# 示例数据
data = {'code': ['600001', '688001', '000001', '688002'], 'name': ['A', 'B', 'C', 'D']}
df = pd.DataFrame(data)

# 排除科创板
df_filtered = df[~df['code'].str.startswith('688')]
print(df_filtered)
```

Output:

```python
     code name
0  600001    A
2  000001    C
```

!!! Notes
    Summary
    - **String Operations**: The `str` accessor enables case conversion, replacement, extraction, splitting, and checking.
    - **Excluding STAR Market**: Use `str.startswith()` or regular expressions to filter out security codes starting with 688.
