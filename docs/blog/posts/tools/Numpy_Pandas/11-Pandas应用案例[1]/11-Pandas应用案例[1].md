---
title: 量化人怎么用Pandas——应用案例[1]：金融数据的处理与清洗
slug: numpy-pandas-for-quant-trader-11
date: 2025-03-17
category: tools
motto: 
img: https://images.jieyu.ai/images/2024/12/book-of-sun-le.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---


Pandas 在金融量化中的应用极为广泛，其高效的数据处理能力和灵活的时间序列分析能力使其成为量化金融领域的核心工具。下面我们重点总结一下 Pandas 库在金融数据的处理和清洗方面的应用。

## 1. 数据获取与整合
### 1.1. Pandas DataFrame

---

#### 1.1.1. 创建
通过 `dict[str, List]` 来创建，其中 `key` 为 `column` 名字，`value` 为对应 `column` 的值。
```python 
df = pd.DataFrame({
    "a": [1,2,3],
    "b": [4, 5, 6]
})
```
也可以是通过二维数组来创建，自行指定 `column`：
```python
df = pd.DataFrame([
    [1, 2, 3],
    [4, 5, 6]
], columns = ['a', 'b', 'c'])
```
#### 1.1.2. 数据访问
在 `pandas.DataFrame` 中访问和定位数据与 `numpy` 不一样。`pandas` 提供了 `iloc` 和 `loc`, `at` 和 `iat` 这样的方法来访问数据。
```python
# 选择第 1、第 2 行
cprint("select second row: \n{}", df.iloc[1:2])
cprint("select all rows, but 1, 2 cols only:\n{}", df.iloc[:,[1,2]])
cprint("loc can use column label:\n{}", df.loc[:, ['b','c']])
```

![50%](https://images.jieyu.ai/images/2025/03/054.png)

---

`at` 和 `iat` 是 `loc` 和 `iloc` 的快速版本。前二者返回的是标量，后二者返回的是向量。使用哪一类方法，取决于我们接下来要进行什么操作。
```python
# 这里必须使用 ROW ID(INT) 和标签 (STR)
cprint('access cell by at: {}', df.at[1, 'b'])

# 此时必须使用全整数下标
cprint('access cell by iat: {}', df.iat[1, 0])

# 可以给单元格赋值
df.iat[1, 0] = 99
cprint('after write, the dataframe is:\n{}', df)
```

![50%](https://images.jieyu.ai/images/2025/03/055.png)

#### 1.2. 应用：获取股票历史数据
```python
import plotly.express as px
import pandas as pd

bars = await Stock.get_bars_in_range("000001.XSHG", FrameType.MONTH, start, end)

df = pd.DataFrame({"xshg": bars["close"][::-1] / 10, "investor": accounts_df["新增投资者-数量"]})
df.index = accounts_df["数据日期"]
```

`bars = await Stock.get_bars_in_range("000001.XSHG", FrameType.MONTH, start, end)` 这里用异步方法获取股票代码为“000001.XSHG”(上证指数)的月度K线数据。

---

获取的bars包含开盘价、收盘价等数据。
`df = pd.DataFrame({"xshg": bars["close"][::-1] / 10, "investor": accounts_df["新增投资者-数量"]})` 这里是按照收盘价对数据进行翻转，使用 Pandas 创建了一个新的二维数组 `df`，包含两列数据：​xshg​（上证指数收盘价调整值）和 ​investor​（新增投资者-数量）。
`df.index = accounts_df["数据日期"]` 设置索引。


![50%](https://images.jieyu.ai/images/2025/03/053.png)

获取金融数据后，Pandas 的 DataFrame 结构可快速整合多源数据（如股票价格、财务指标、宏观经济数据）。现在，我们来取对应的上证指数，并将其绘制成图：
```python
fig = px.line(df)
fig.update_layout(hovermode="x unified")
fig.show()
```

---

![](https://images.jieyu.ai/images/2025/03/062.png)

## 2. 数据清洗与标准化
### 2.1. 异常值处理（以均值标准差修正法为例）
将偏离均值3倍标准差的数据拉回3倍标准差，这种修正法也称为$3\sigma$法。这是因为，基于正态分布的假设，超过均值$3\sigma$的数值就非常罕见了。
在代码实现上， pandas和numpy都提供了一个名为`clip`的函数：
```python
import pandas as pd
import numpy as np

# 生成示例数据（模拟股票日收益率）
np.random.seed(42)  # 固定随机种子确保结果可复现
dates = pd.date_range("2023-01-01", periods=100)
returns = np.random.normal(loc=0.001, scale=0.02, size=100)  # 均值0.1%，标准差2%

# 人为添加两个极端值（模拟异常值）
returns[10] = 0.15  # 异常高收益
returns[20] = -0.12 # 异常低收益

# 创建DataFrame
df = pd.DataFrame({"date": dates, "daily_return": returns})

mean = series.mean()
std = series.std()
df["return_clipped"] = series.clip(mean - 3 * std, mean + 3 * std)
```

---

```python
# 输出结果对比
print("原始数据统计:")
print(df["daily_return"].describe())
print("\n修正后数据统计:")
print(df["return_clipped"].describe())
```

![50%](https://images.jieyu.ai/images/2025/03/056.png)

`clip`函数的第一个参数是待处理的数组，第二个参数和第三个参数分别是要替换的边界值。超过这个边界值的数据，都将分别被这两个值替换。

当数据量比较小时，个别的离群值将显著影响到std的计算，从而导致`clip`方法失效（即所有的点都落在$±3\sigma$内）。大家可以通过缩小第3行中，`np.random.randint`中的`size`参数，可以自行尝试下。

### 2.2. 缺失值处理
在因子分析的预处理过程中，常常遇到使用 `pandas` 的 `fillna` 函数来进行缺失值处理（也可以用 `numpy` 来实现）。

---

财务类因子有可能出现某些数据缺失；一些分析师评级数据更是常常出现没有覆盖到某个标的的情况；有一部分技术指标类的因子，常常会有冷启动情况，表现为前几项往往无法计算，于是表示为`np.nan`。

在这些情况下，我们都要先进行缺失值处理。对不同的因子，我们处理方法是不一样的。一般有延用上一期有效数据（也即`pandas.fillna`中`mode='ffill'`的情况）、中位数替代法、相似公司替代法等。

对财务因子，我们一般延用上期因子值；其它因子需要根据具体情况具体分析，可以延用上一期值，也可以考虑其它不影响分析的替代值；如果因子值缺失过多，导致覆盖度特别低，则应该考虑剔除。

一些文章建议把缺失值处理放在去极值之前进行。这可能是有争议的。

```python
import pandas as pd
import numpy as np

# 创建一个包含缺失值的示例DataFrame
data = {
    "日期": pd.date_range("2023-01-01", periods=5),
    "销售额": [100, np.nan, 150, np.nan, 200],
    "客单价": [50, 55, np.nan, 60, np.nan],
    "访问量": [1000, 1200, np.nan, np.nan, 1500]
}
df = pd.DataFrame(data)
print("原始数据:\n", df)
```

原始数据：
|     日期     |  销售额  |  客单价  |  访问量  |
|:------------:|:-------:|:-------:|:-------:|
| 2023-01-01 |   100   |    50   |  1000   |
| 2023-01-02 |   nan   |    55   |   1200   |
| 2023-01-03 |   150   |   nan   |   nan   |
| 2023-01-04 |   nan   |    60   |   nan   |
| 2023-01-05 |   200   |   nan   |  1500   |


---


```python
# 方法1：用固定值填充缺失值
df_fixed = df.fillna(0)  # 所有缺失值填充为0
print("\n固定值填充结果:\n", df_fixed)
```
固定值填充结果：
|     日期     | 销售额 | 客单价 | 访问量  |
|:------------:|:------:|:------:|:-------:|
| 2023-01-01 |  100   |   50   |  1000  |
| 2023-01-02 |   0    |   55   |  1200  |
| 2023-01-03 |  150   |   0    |    0    |
| 2023-01-04 |   0    |   60   |    0    |
| 2023-01-05 |  200   |   0    |  1500  |

```python
# 方法2：前向填充（ffill）
df_ffill = df.fillna(method="ffill")  # 用前一行的值填充
print("\n前向填充结果:\n", df_ffill)
```
前向填充结果：
|     日期     | 销售额 | 客单价 | 访问量  |
|:------------:|:------:|:------:|:-------:|
| 2023-01-01 |   100  |   50   |  1000  |
| 2023-01-02 |   100  |   55   |  1200  |
| 2023-01-03 |   150  |   55   |  1200  |
| 2023-01-04 |   150  |   60   |  1200  |
| 2023-01-05 |   200  |   60   |  1500  |

```python
# 方法3：后向填充（bfill）
df_bfill = df.fillna(method="bfill")  # 用后一行的值填充
print("\n后向填充结果:\n", df_bfill)
```
后向填充结果：
|     日期     | 销售额 | 客单价 | 访问量  |
|:------------:|:------:|:------:|:-------:|
| 2023-01-01 |   100  |   50   |  1000  |
| 2023-01-02 |   150  |   55   |  1200  |
| 2023-01-03 |   150  |   60   |  1500  |
| 2023-01-04 |   200  |   60   |  1500  |
| 2023-01-05 |   200  |  NaN   |  1500  |

```python
# 方法4：用列均值填充
df_mean = df.copy()
df_mean["销售额"] = df["销售额"].fillna(df["销售额"].mean())  # 销售额列均值填充
df_mean["客单价"] = df["客单价"].fillna(df["客单价"].median())  # 客单价列中位数填充
print("\n均值/中位数填充结果:\n", df_mean)
```
用均值/中位数填充结果：
|     日期     | 销售额 | 客单价 | 访问量  |
|:------------:|:------:|:------:|:-------:|
| 2023-01-01 |   100  |   50   |  1000  |
| 2023-01-02 |   150  |   55   |  1200  |
| 2023-01-03 |   150  |   55   |   NaN  |
| 2023-01-04 |   150  |   60   |   NaN  |
| 2023-01-05 |   200  |   55   |  1500  |

### 2.3. 中性化
因子对不同的行业，其暴露程度是不一样的。比如，如果我们在2022年用市盈率因子选股，我们会发现市盈率最低的（且为正），多是银行股。如果我们凭这个因子来选股，实际上选择的是银行股，其涨跌是受政策宏观调控与经济周期的系统性影响，不能选择出具有独特 alpha 的个股。

---

我们常做的中性化有行业中性化和市值中性化。

对离散数据的回归，一般采用哑变量线性回归法。行业中性化常常使用这种方法，其公式为：

$$
Y = \sum_{j=1}^nIndustry * \beta_j + \alpha  + \epsilon \tag 1
$$

这里的常量，或者称残差 $\epsilon$ 就是行业中性化后的因子。

市值中性化回归公式如下：
$$
Y = \beta * \log(MarketValue) + \alpha + \epsilon \tag 2
$$

我们可以同时进行市值中性化和行业中性化，并且可以对多个因子同时实施。其代码实现如下：
```python
# copy industry.csv to each students docker container home
import pandas as pd
from coursea import *

await init()

codes = [
    '000001.XSHE',
    '000002.XSHE',
    '000004.XSHE',
    '000006.XSHE',
    '000007.XSHE',
    '000008.XSHE',
    '000009.XSHE',
    '000011.XSHE'
]

end = datetime.date(2023, 6, 26)
start = tf.day_shift(end, -10)

```

---

```python
factors = []
async for code, bars in Stock.batch_get_day_level_bars_in_range(codes, FrameType.DAY, start, end):
    df = pd.DataFrame()
    df["date"] = bars["frame"][1:]
    df["instrument"] = [code] * (len(bars) - 1)
    df["factor"] = bars["close"][1:] / bars["close"][:-1] - 1
  
    factors.append(df)

factors = pd.concat(factors)
factors
```

![50%](https://images.jieyu.ai/images/2025/03/057.png)

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("/data/.common/industry.csv")
pd.options.display.max_columns = 10
display(df)
```

---

```python
# get_dummies是一个 one-hot 编码的矩阵
industry = pd.get_dummies(df["industry_zx"])
lncap = np.log(df[["MKT_CAP_FLOAT"]])

# y可以是一个矩阵，但这里我们只有一个因子要中性化，所以是一个(1,n)的矩阵
y = factors[factors["date"]==datetime.datetime(2023, 6, 26)][["factor"]]

y = y.dropna(how="any", axis=1)
    
X = pd.concat([lncap, industry], axis=1)

model = LinearRegression(fit_intercept = False)
res = model.fit(X, y)

# 根据公式求残差，这个残差，就是我们新的因子
coef = res.coef_
residue = y - np.dot(X, coef.T)
display(residue)
```

![](https://images.jieyu.ai/images/2025/03/058.png)

---


![50%](https://images.jieyu.ai/images/2025/03/059.png)


最终我们求得的残差，就是进行了中性化之后的因子。

!!! Attention
    我们常常对市值因子进行分布调整，但要注意，分布调整与市值中性化是相区别的。分布调整直接作用在市值因子上。而中性化是其他因子，借由市值因子来进行中性化。

---
朋友！以上，我们简单列举了 Python中 Pandas 库在金融数据的处理和清洗上的应用。下一章，我们继续深入探讨 Pandas 在 ARIMA 模型进行时间序列上的使用，敬请期待！