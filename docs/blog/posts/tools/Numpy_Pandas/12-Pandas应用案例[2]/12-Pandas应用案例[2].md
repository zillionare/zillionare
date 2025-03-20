---
title: 量化人怎么用Pandas——应用案例[2]：ARIMA 模型与时间序列预测
slug: numpy-pandas-for-quant-trader-12
date: 2025-03-20
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

ARIMA 模型全称差分整合移动平均自回归模型（Autoregressive Integrated Moving Average model）。

标准 ARIMA 模型期望输入参数为 3 个参数，即 $p$, $d$, $q$。这里 $p$ 是滞后观测值的数量， $d$ 是差异程度，$q$ 是移动平均窗口的大小/宽度。

我们以上证指数预测为例，来演示该模型的用法：

---

```python
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from pandas import datetime
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from coursea import *
await init()

bars = await Stock.get_bars("000001.XSHG", 250, FrameType.DAY)
```

首先我们检验一下上证指数是否具有自相关特性，这是我们进行 ARIMA 分析的必要条件。我们可以通过 `pandas` 的 `lag_plot` 来查看。

在 `lag_plot` 图中，<font color=LightCoral>如果数据显示线性模式，则表明存在自相关</font>：
- 正线性趋势（即从左到右向上）表明正自相关；
- 负线性趋势（从左到右向下）表明负自相关；
- 数据围绕对角线聚集得越紧密，自相关性就越强；
- 完全自相关的数据将聚集在一条对角线上。



lag_plot的原理

- 核心思想：将时间序列 $x_t$​ 与其滞后 $k$ 期的序列 $x_{t−k}$ 绘制成散点图。
- ​数学表示：对于时间序列 $x_{1}​,x_{2}​,...,x_n$​，滞后 $k$ 的序列为 $x_{1+k}​,x_{2+k}​,...,x_n$​。
    - 横轴：原始序列 $x_t$​（去除前 $k$ 个值）。
    - 纵轴：滞后序列 $x_{t−k}$​。


代码实现：
```python
df = pd.DataFrame(bars)
lag_plot(df['close'], lag = 3)
```

---

运行结果：

![](https://images.jieyu.ai/images/2025/03/063.png)



我们选择的参数是：**p = 4 ， d = 1 ， q = 0**
```python
close = bars["close"]
frames = bars["frame"]

train_data, test_data = close[0:int(len(close)*0.7)], close[int(len(close)*0.7):]

history = list(train_data)
model_predictions = []
N_test_observations = len(test_data)
```

---

```python
for time_point in range(N_test_observations):
    model = ARIMA(history, order=(4,1,0))
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    model_predictions.append(yhat)
    true_test_value = test_data[time_point]
    history.append(true_test_value)
    
MSE_error = mean_squared_error(test_data, model_predictions)
print('Testing Mean Squared Error is {}'.format(MSE_error))
# Testing Mean Squared Error is 392.2329234250518
```

我们得到的 MSE 大约在 600 左右。

我们将训练数据集分为训练集和测试集，然后使用训练集来拟合模型，并为测试集上的每个元素生成预测。

考虑到差分和 AR 模型对先前时间中的观测结果的依赖，需要滚动预测程序。为此，我们在收到每个新观测值后重新创建 ARIMA 模型。 最后，我们手动跟踪称为历史记录的列表中的所有观察结果，该列表以训练数据为种子，并在每次迭代时附加新的观察结果。

现在，让我们把实际走势与预测值对照绘图：
```python
test_set_range = bars["frame"][len(train_data):]
plt.plot(test_set_range, model_predictions, color='#F55892', marker='o', ms = 3, linestyle='dashed',label='Predicted Price')
plt.plot(test_set_range, test_data, color='#F2DCFA', label='Actual Price', alpha=0.8)
plt.title('XSHG Prices Prediction')
plt.xlabel('Date')
plt.ylabel('Prices')
plt.xticks(rotation = 45)
plt.legend()
plt.show()
```

---

![](https://images.jieyu.ai/images/2025/03/064.png)

单从图形上看，可能会感觉预测相当有效。从 MSE 上，如果不与标准差进行对照，我们也很难分辨出预测的好与坏。

```python
from sklearn.metrics import mean_absolute_percentage_error
MAPE_error = mean_absolute_percentage_error(test_data, model_predictions)
print('Testing Mean Absolute Percentage Error is {}'.format(MAPE_error))
# Testing Mean Absolute Percentage Error is 0.005145862946818848
```

但如果我们使用`mean_absolute_percentage_error`，则得到的预测残差大约是 0.5%。考虑到上证多数时间的波动在 1% 以内，因此我们也很难说这个预测有多准。

---

## 总结
在本文中，我们重点介绍了ARIMA模型，并使用 `pandas` 的 `lag_plot` 来查看上证指数的是否具有自相关特性（这是我们进一步使用ARIMA模型的前提）。