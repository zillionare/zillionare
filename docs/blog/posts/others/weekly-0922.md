---
title: "[0922] QuanTide Weekly"
date: 2024-09-22
category: others
slug: quantide-weekly-0922
img: 
stamp_width: 60%
stamp_height: 60%
tags: [others, weekly, numpy, pandas]
seq: 第 10 期
---

### 本周要闻
* 何立峰会见中美经济工作组美方代表团
* 公安机关严查资本市场“小作文”，三名造谣者被罚
* 证监会全面优化券商风控指标体系
* 美“生物安全法案”未被纳入参议院2025财年国防授权法案
* 贵州茅台：拟以30亿元-60亿元回购股份用于注销，上市以来首次发布回购计划


### 下周看点
* 中证A500指数周一发布。此前传相关基金提前结束募集
* 2024深圳eVTOL暨低空经济展开幕，首届中国数字人大会在京举办
* 周三、周五，再迎ETF及A50交割日！

### 本周精选

* 连载！量化人必会的 Numpy 编程 (4)

---

* 中美经济工作组9月19日至20日在京会晤。此次会议由财政部副部长廖岷与美国副财长尚博共同主持，两国经济领域相关部门到会交流。何立峰20日会见美国财政部副部长尚博一行。
* 公安机关近日依法查处一起自媒体运营人员恶意编造网络谣言进行吸粉引流、非法牟利、扰乱社会秩序的案件。经公安部网安局调查，刘某(男，36岁)、陈某(男，46岁)、邵某(男，26岁)为博取关注、吸粉引流、谋取利益，故意编造发布涉转融通谣言信息，误导公众认知，涉嫌扰乱金融秩序。
* 证监会发布《证券公司风险控制指标计算标准规定》。业内人士指出，此举预计将释放近千亿元资金，促进有效提升资本使用效率，加大服务实体经济和居民财富管理力度。
* 美当地时间19日，美参议院军事委员会对外公布了参议院版本2025财年国防授权法案（简称NDAA），其中纳入93项修正案，但不包含“生物安全法案”相关提案。此前，美众议院已通过不包含生物安全法案的NDAA，下一步美参众两院将对NDAA进行谈判合并。此前受相关传闻影响，CXO板块持续受到压制。
* 美股三大指数周五收盘涨跌不一，均录得周线两连涨。道指续创新高，本周累涨1.61%；标普累涨1.36%；纳指累涨1.49%。

<claimer>消息来源：财联社</claimer>

---

# Numpy量化场景应用案例[1]

## 连续值统计

在很多量化场景下，我们都需要统计某个事件连续发生了多少次，比如，连续涨跌停、N连阳、计算Connor's RSI中的streaks等等。比如，要判断下列收盘价中，最大的连续涨停次数是多少？最长的N连阳数是多少？

```python
a = [15.28, 16.81, 18.49, 20.34, 21.2, 20.5, 
     22.37, 24.61, 27.07, 29.78, 32.76, 36.04]
```

假设我们以10%的涨幅为限，则可以将上述数组转换为：

```python
pct = np.diff(a) / a[:-1]
pct > 0.1
```

我们将得到以下数组：

```python
flags = [True, False,  True, False, False, False,  True, False,  True,
        True,  True]
```

这仍然不能计算出最大连续涨停次数，但它是很多此类问题的一个基本数据结构，我们将原始的数据按条件转换成类似的数组之后，就可以使用下面的神器了：

---

```python
from numpy.typing import ArrayLike
from typing import Tuple
import numpy as np

def find_runs(x: ArrayLike) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Find runs of consecutive items in an array.

    Args:
        x: the sequence to find runs in

    Returns:
        A tuple of unique values, start indices, and length of runs
    """

    # ensure array
    x = np.asanyarray(x)
    if x.ndim != 1:
        raise ValueError("only 1D array supported")
    n = x.shape[0]

    # handle empty array
    if n == 0:
        return np.array([]), np.array([]), np.array([])

    else:
        # find run starts
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])
        run_starts = np.nonzero(loc_run_start)[0]

        # find run values
        run_values = x[loc_run_start]

        # find run lengths
        run_lengths = np.diff(np.append(run_starts, n))

        return run_values, run_starts, run_lengths


pct = np.diff(a) / a[:-1]
v,s,l = find_runs(pct > 0.099)
(v, s, l)
```

输出结果为：

(array([ True, False,  True]), array([0, 3, 6]), array([3, 3, 5]))

输出结果是一个由三个数组组成的元组，分别表示：

---

- value: unique values
- start: start indices
- length: length of runs

在上面的输出中，v[0]为True，表示这是一系列涨停的开始，s[0]则是对应的起始位置，此时索引为0; l[0]则表示该连续的涨停次数为3次。同样，我们可以知道，原始数组中，最长连续涨停（v[2]）次数为5（l[2]），从索引6（s[2]）开始起。

所以，要找出原始序列中的最大连续涨停次数，只需要找到l中的最大值即可。但要解决这个问题依然有一点技巧，我们需要使用<ref>第4章</ref>中介绍的 mask array。

```python
v_ma = np.ma.array(v, mask = ~v)
pos = np.argmax(v_ma * l)

print(f"最大连续涨停次数{l[pos]}，从索引{s[pos]}:{a[s[pos]]}开始。")
```

在这里，mask array的作用是，既不让 v == False 的数据参与计算（后面的 v_ma * l），又保留这些元素的次序（索引）不变，以便后面我们调用 argmax 函数时，找到的索引跟v, s, l中的对应位置是一致的。

我们创建的v_ma是一个mask array，它的值为：

```python
masked_array(data=[True, --, True],
             mask=[False,  True, False],
       fill_value=True)
```


当它与另一个整数数组相乘时，True就转化为数字1，这样相乘的结果也仍然是一个mask array:

---

```python
masked_array(data=[3, --, 5],
             mask=[False,  True, False],
       fill_value=True)
```

当arg_max作用在mask array时，它会忽略掉mask为True的元素，但保留它们的位置，因此，最终pos的结果为2，对应的 v,s,l中的元素值分别为: True, 6, 5。

<!-- 我们在前面的基础篇介绍了mask array，通过这个例子，我们看到了在量化场景下，mask array如何起作用的。-->

如果要统计最长N连涨呢？这是一个比寻找涨停更容易的任务。不过，这一次，我们将不使用mask array来实现：

```python
v,s,l = find_runs(np.diff(a) > 0)

pos = np.argmax(v * l)
print(f"最长N连涨次数{l[pos]}，从索引{s[pos]}:{a[s[pos]]}开始。")
```

输出结果是： 最长N连涨次数6，从索引5:20.5开始。

这里的关键是，当Numpy执行乘法时，True会被当成数字1，而False会被当成数字0，于是，乘法结果自然消除了没有连续上涨的部分，从而不干扰argmax的计算。

当然，使用mask array可能在语义上更清楚一些，尽管mask array的速度会慢一点，但正确和易懂常常更重要。

## 计算 Connor's RSI中的streaks

Connor's RSI（Connor's Relative Strength Index）是一种技术分析指标，它是由Nirvana Systems开发的一种改进版的相对强弱指数（RSI）。Connor's RSI与传统RSI的主要区别在于它考虑了价格连续上涨或下跌的天数，也就是所谓的“连胜”（winning streaks）和“连败”（losing streaks）。这种考虑使得Connor's RSI能够更好地反映市场趋势的强度。

---

在前面介绍了find_runs函数之后，计算streaks就变得非常简单了。

```python
def streaks(close):
    result = []
    conds = [close[1:]>close[:-1], close[1:]<close[:-1]]

    flags = np.select(conds, [1, -1], 0)
    v, _, l = find_runs(flags)
    for i in range(len(v)):
        if v[i] == 0:
            result.extend([0] * l[i])
        else:
            result.extend([v[i] * x for x in range(1, (l[i] + 1))])
            
    return np.insert(result, 0, 0)
```

这段代码首先将股价序列划分为上涨、下跌和平盘三个子系列，然后对每个子系列计算连续上涨或下跌的天数，并将结果合并成一个新的数组。在streaks中，连续上涨天数要用正数表示，连续下跌天数用负数表示，所以在第5行中，通过np.select将条件数组转换为[1, 0, -1]的序列，后面使用乘法就能得到正确的连续上涨（下跌）天数了。

## 中位数极值法去极值

在因子分析中，我们常常需要对数据进行去极值处理，以减少对异常值的影响。中位数极值法（Median Absolute Deviation，MAD）是一种常用的去极值方法，它通过计算数据中中位数（median）和绝对离差（absolute deviation）来确定异常值。

这里需要先介绍绝对中位差（median absolute deviation） 的概念：

$$MAD = median(|X_i - median(X)|)$$

为了能 MAD 当成与标准差$\sigma$估计相一致的估计量，即

---

$$\hat{\sigma} = k. MAD$$

这里 k 为比例因子常量，如果分布是正态分布，可以计算出：
$$
k = \frac{1}{(\Phi^{-1}(\frac{3}{4}))} \approx 1.4826
$$

基于这个 k 值，取 3 倍则近似于 5。

在对多个资产同时执行去极值时，我们可以使用下面的方法，以实现向量化并行操作：

```python
def mad_clip(df: Union[NDArray, pd.DataFrame], k: int = 3, axis=1):
    """使用 MAD 3 倍截断法去极值
    
    Args:
        df: 输入数据，要求索引为日期，资产名为列，单元格值为因子的宽表
        k: 截断倍数。
        axis: 截断方向
    """

    med = np.median(df, axis=axis).reshape(df.shape[0], -1)
    mad = np.median(np.abs(df - med), axis=axis)

    return np.clip(df.T, med.flatten() - k * 1.4826 * mad,
                   med.flatten() + k * mad).T
```

<!-- 
这篇文章是量化场景下的Numpy与Pandas中的一篇。这个系列既介绍基础的Numpy和Pandas，更介绍在量化场景下我们如何灵活运用Numpy和Pandas技巧，写出简洁、高效的代码。示例代码充分证明了这一点。
-->

<about/>

---

## 《因子投资与机器学习策略》开课啦！

![](https://images.jieyu.ai/images/hot/course/factor-ml/1.png)

---

## 目标清晰 获得感强

![](https://images.jieyu.ai/images/hot/course/factor-ml/2.png)

---

## 为什么你值得QuanTide的课程？

![](https://images.jieyu.ai/images/hot/course/factor-ml/3.png)

