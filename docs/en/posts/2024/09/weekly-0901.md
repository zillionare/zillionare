---
title: "FFT for Stock Prediction: Decoding Market Cycles"
date: 2024-09-01
slug: en/posts/uncategory/weekly-0901
tags: [Time Series Analysis, Fourier Transform, Market Cycles, Quantitative Research]
excerpt: "Decomposes stock price time series into frequency domains using FFT to identify dominant capital cycles. Demonstrates how to isolate main force trading patterns and predict short-term trends through signal energy analysis."
lang: en
translation_of: posts/uncategory/weekly-0901
auto_translated: true
source_sha: c93c5540f5d5c7914df3bd9aa244bd5c22779c42
cover: "stamp_width: 60%"
---

### This Week's Highlights

* Market rumors suggest a reduction in existing mortgage rates; real estate ETFs surged, but multiple stocks hit price limits before closing.
* China’s official manufacturing PMI for August stood at 49.1%, a 0.3 percentage point decline from the previous month.
* The State Administration for Market Regulation announced that Alibaba has completed its three-year rectification process.
* Tongkun Group released its first semi-annual report of the year, showing a 911.35% year-on-year increase, the highest net profit growth among companies that have already published their reports.

### Next Week's Focus
* Will the rumor about reducing existing mortgage rates materialize?
* Caixin Manufacturing PMI release on Monday.
* The 2024 Low-Altitude Economy Development Conference will be held in Wuhu from September 6 to 8.

### This Week's Selection

* Is the Main Force Entering? Research on Fast Fourier Transform and Stock Price Prediction
* Serialized! Essential Numpy Programming for Quants (1)

---

## This Week's Highlights

* Market rumors suggest that relevant authorities are considering further reducing existing mortgage rates, allowing up to 38 trillion RMB in existing mortgages to seek refinancing, thereby reducing residents' debt burden and boosting consumption.<remark>As of Saturday, these rumors have not been officially confirmed.</remark>
* In August, the PMI was **49.1%**, a 0.3 percentage point decline from the previous month. By enterprise size, the PMI for large enterprises was 50.4%, still above the critical point; the PMIs for medium and small enterprises were 48.7% and 46.4%, declining by **0.7** and 0.3 percentage points, respectively.<remark>The August PMI was influenced by high temperatures and did not significantly exceed expectations.</remark>
* On the afternoon of August 30, the State Administration for Market Regulation announced that Alibaba had completed its three-year rectification process with good results. Alibaba’s stock price has fallen by 70% from its peak in 2020.
* On Friday, Eastern Time, the three major US stock indices rose collectively. The Dow Jones Industrial Average rose 0.55% to 41,563.08 points, **setting a new record high**. The S&P 500 rose 1.01%, and the Nasdaq rose 1.13%. The Federal Reserve’s preferred July PCE inflation data basically met expectations. The market’s bet on a significant Fed rate cut in September decreased, but the market still expects a significant rate cut in November or December.
* E Fund’s Nasdaq 100 ETF released its 2024 interim report. Changzhou Investment Group holds a 5.92% share, becoming the largest holder. Despite a net value increase of 49.21%, the ETF still rose 14.91% this year. The ETF was issued in 2017 and currently has a net value of 3.16.
* Tongkun Group released its first semi-annual report of the year, achieving a net profit of 1.065 billion RMB, a 911.35% year-on-year increase, the highest net profit growth among companies that have already published their reports. During the reporting period, downstream demand for polyester filament industry improved significantly compared to the same period last year, with increased product sales and price spreads. **The industry is generally in a recovery state.** Overall, the electronics industry was the big winner, with revenue growth leading all sectors. The total revenue for the first half of the year was 1.59 trillion RMB, a 17.3% year-on-year increase.

<claimer>Information source: Eastmoney website</claimer>

---

## Next Week's Focus
* Market rumors on Friday suggested that reducing existing mortgage rates is under consideration. Real estate ETFs surged immediately, while bank stocks plummeted in response. However, prices fell back at the close, and many stocks hitting price limits failed to hold. Next week, will this rumor be confirmed or refuted? It could have a significant impact on the market.
* Caixin Manufacturing PMI release on Monday.
* The 2024 Low-Altitude Economy Development Conference will be held in Wuhu from September 6 to 8.
* US August unemployment rate and non-farm payrolls report released on Friday.

---

# Is the Main Force Entering? Research on Fast Fourier Transform and Stock Price Prediction

An undeniable fact: economic activity is cyclical. However, this fact seems to have been long ignored by the quantitative community. Whether in asset pricing theory or trend trading theory, we can hardly find a place for cycle research -- in the latter context, people prefer to use terms like "swing" rather than openly saying "cycle."

In this article, we will explore cycles in the stock market. We will use the Fast Fourier Transform (FFT) to decompose time series signals into frequency domain signals, identify main force capital through signal energy, and make some predictions based on their operational cycles. Finally, we present three hypotheses, one of which has been proven.

## FFT - Time-Frequency Conversion

(Data acquisition part omitted).

We have obtained the Shanghai Composite Index over the past year. Obviously, it is a time series signal. The Fourier Transform is precisely designed to convert time series signals into frequency domain signals. In other words, the Fourier Transform can decompose the Shanghai Composite Index into a combination of several sine waves.

```python
# 应用傅里叶变换
fft_result = np.fft.fft(close)
freqs = np.fft.fftfreq(len(close))

# 逆傅里叶变换
filtered = fft_result.copy()
filtered[20:] = 0
inverse_fft = np.fft.ifft(filtered)
```

---

```python
# 绘制原始信号和分解后的信号
plt.figure(figsize=(14, 7))
plt.plot(close, label='Original Close')
plt.plot(np.real(inverse_fft), label='Reconstructed from Sine Waves')
plt.legend()
```

We obtained the following output:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/real-vs-synthetic.jpg)

In the field of digital signal processing, time series are called time-domain signals, and after the Fourier Transform, we obtain frequency-domain signals. Time-domain signals and frequency-domain signals can be converted into each other. The `fft` library in Numpy provides `fft` and `ifft` functions to help us implement these two conversions.

`np.fft.fft` converts time-domain signals into frequency-domain signals. The result is a complex array representing the amplitude (i.e., energy) of each frequency component decomposed from the signal. Frequencies are arranged from low to high, with the 0th element having a frequency of 0, which is the DC component, a linear function of the signal's mean.

`np.fft.ifft` is the inverse transform of `fft`, converting frequency-domain signals back into time-domain signals.

Converting time-domain signals to the frequency domain reveals basic characteristics such as signal periodicity. We can also perform some operations on the frequency-domain signals obtained from the `fft` and then transform them back, which is digital signal processing.

---

## High-Frequency Filtering and Compression

If we set the energy of high-frequency signals to zero and then inverse-transform the signal back, we will get a new sequence similar to the original sequence, but smoother -- this is what we often call low-pass filtering -- various moving averages you are familiar with are also low-pass filters.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml-promotion.png)

In the above code, we only retained the energy of the first 20 low-frequency signals, resulting in a new sequence similar to the original sequence. If this method is applied in the image field, it achieves lossy compression -- the compression ratio is 250/20.

In the 1990s, the most advanced image compression algorithms were based on such principles -- retaining the mid-to-low-frequency parts of the image and treating high-frequency parts as noise to be removed, thereby preserving the main features of the image while significantly reducing the amount of data to be saved.

---

People working on such compression algorithms at that time all knew this beautiful young lady -- Lena. This photo is a standard test sample for image algorithms. Through long-term evolution, under the pressure of survival, humans have evolved super strong abilities to recognize others' expressions. Therefore, compared to other samples, once compression causes a decline in image quality, the human eye is more likely to detect changes in faces and expressions, making face images the best test samples.

<div style='width:50%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/lena.jpg'>
<span style='font-size:0.6rem'>Lena </span>
</div>

Lena is a model for Playboy magazine. This photo is a small part of her seductive photo taken for the November 1972 issue of Playboy -- in the original photo, Lena boldly displayed her seductive buttocks curve, but those unorthodox scientists only shared her smile with us -- from a scientific perspective, this is also the part with the highest information ratio.

Coincidentally, before Lena became the standard test sample for digital image processing, scientists were always using another young lady's photo, also from Playboy.

Okay, back to the topic. We just shared a method to remove high-frequency noise from signals, making the meaning of the signal itself more prominent. We also hope to use similar techniques in securities analysis to reveal signals hidden in K-lines.

But if we simply copy this method from other fields, it hardly counts as research, and it is difficult to achieve good results. In fact, in securities signals, we should pay more attention to signal energy compared to frequency, after all, we want to stand on the side of the most powerful people.

---

<div style='text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/may-the-force-be-with-you.jpg'>
<span style='font-size:0.6rem'>May the Force be with you -- Star Wars</span>
</div>

So, let's change our approach and keep the parts with the strongest energy in the decomposed frequency-domain signals to see what they look like.

## Filtering Low-Energy Signals

```python
# 保留能量最强的前 5 个信号
amp_threshold = np.sort(np.abs(fft_result))[-11]

# 绘制各个正弦波分量
plt.figure(figsize=(14, 7))

theforce = []
for freq in freqs:
    if freq == 0:  # 处理直流分量
        continue
    elif freq < 0:
        continue
    else:
        amp = np.abs(fft_result[np.where(freqs == freq)])
        if amp < amp_threshold:
            continue
```

---

```python

        sine_wave = amp * np.sin(2 * np.pi * freq * np.arange(len(close)))
        theforce.append(sine_wave)
        plt.plot(dates, sine_wave, label=f'Frequency={freq:.2f}')

plt.legend()
plt.title('Individual Sine Wave Components')
ticks = np.arange(0, len(dates), 20)
labels_to_show = [dates[i] for i in ticks]
plt.xticks(ticks=ticks, labels=labels_to_show, rotation=45)
plt.show()
```

The FFT gives frequencies in pairs of positive and negative. We can simply consider that negative frequencies are meaningless to us; they are a kind of dark energy we cannot see and need not care about. Therefore, in the code, we ignored this part.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/individual-sine-wave.jpg)

We see that the wave (orange) with the strongest impact on the Shanghai Composite Index trend has a cycle of about 7 months: it takes 3.5 months from peak to trough, and 3.5 months from trough to peak. Since its energy is almost double that of other waves, it dominates the trend of the entire superimposed wave: if other waves are in phase with it, the superimposed result will strengthen the trend; otherwise, it will offset the trend. The energies of other waves are similar, but their frequencies differ.

---

What exactly are these waves? They can be economic cycles, but ultimately, economic cycles are driven by people or reflect people's judgments. Therefore, we can view the cycle of fluctuations as the **operational cycle of capital**.

From this decomposition chart, we can hypothesize that there is long-term capital (corresponding to the blue wave) that rebalances once a year or so. There is medium-term capital (corresponding to the orange wave) that rebalances about every six months. Other capital is short-term, changing positions about every three months. There are countless high-frequency waves we filtered out, which operate frequently, possibly corresponding to retail investors, but their energy is small and can generally be ignored; only in extremely rare cases can they form superimposed effects in the same direction, thereby affecting the trend.

Now, let's synthesize the operations of these capital flows and compare them with the actual trend to see how it goes:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/real-vs-5-waves-synthetic.jpg)

The major cycles basically match, meaning these capital flows basically control the market trend. Moreover, we seem to be able to assert that during the period from March 15 to May 17, there was a divergence trend between stock prices and main force capital: main force capital was retreating, but retail investors were still operating. Thus, although stock prices were still rising, the final direction was determined by main force capital.

---

!!! tip
    The black line is synthesized from the main force capital waves (predictive for the future). Before the market undergoes fundamental changes, the main force's operational style is relatively fixed, so it may have some short-term predictive ability. If we accept this conclusion, we should note that there is another divergence at the end -- retail investors are still leaving, but main force capital is entering. Of course, please do not take this too seriously.

## Explanation of the DC Component

I used to think that the DC component indicates the trend of asset prices, but in fact, all waves are horizontal -- but only commodity markets are horizontal, while stock markets are essentially upward. Therefore, the DC component cannot indicate the trend of asset prices.

Until today, a sudden idea struck me: if you segment a longer time series signal and perform FFT decomposition, you will obtain several DC components. The regression line of these DC components is the trend of asset prices.

Here are three hypotheses:

1. If the energy distribution at various frequencies does not change significantly after segmented decomposition, it indicates that the composition of investors and their operational styles have not changed significantly. We can use FFT to predict short-term future trends until the conditions no longer hold.
   

2. The DC component of the Shanghai Composite Index over the past 30 years should be able to perfectly fit a trend line, and its slope equals the slope of the 20-year regression line of the Shanghai Composite Index.
3. Securities prices are a combination of the trend line of the DC component and a series of sine waves.

---

Next, we will prove the second hypothesis (process omitted). Finally, we plot the DC component and trend line as follows:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/dc-regression.jpg)

And the A-share annual lines and trend lines since 2005 are as follows:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/a-share-yearly.jpg)

It cannot be said to be very similar, but almost completely consistent.

The p-value for trend line fitting is around 0.055, which basically meets the 0.05 confidence level requirement.

---

This article is part of our "Factor Investing and Machine Learning Strategies," appearing in the section on exploring new factor methodologies. Some important results obtained from FFT transformation will become features used to train machine learning strategies. See you in class for more content!

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml-promotion.png)

<!-- If I hadn't read Ray Dalio's "Principles," I would almost believe that stock price fluctuations are unrelated to economic cycles. But there has always been a faint belief that since economic activity exists in cycles, the fluctuations in securities prices must also exist in cycles. -->

---

# Essential NUMPY Programming for Quants (1) - Core Syntax

## 1. Basic Data Structures

The core data structure of NumPy is `ndarray` (n-dimensional array). This is an object representing multi-dimensional, homogeneous, and fixed-size arrays.

`ndarray` can only store homogeneous array objects, making it unable to express record-type data. Therefore, NumPy has extended to a data structure called `structured array`. It uses a `void` type tuple to represent a record, allowing NumPy to also express record-type data. Therefore, in NumPy, there are actually two main data types related to arrays.

The former array format is well-known, and we will use it as an example to introduce most NumPy operations. The latter data format is also commonly used in quantitative finance, such as market data obtained through Juheshi's [^Juheshi] `jqdatasdk`, which allows returning this type of data. Compared to `DataFrame`, it has many conveniences in storage and access. We will introduce it in a separate chapter later.

Before using NumPy, we must first install and import the NumPy library:

```bash
# 安装 NUMPY
pip install numpy
```

---

Generally, we import and use NumPy via the alias `np`:

```python
import numpy as np
```

To make the results more prominent when running these examples in a Notebook, we first define a `cprint` function that outputs prompts as-is but uses red font for variables to distinguish them:

```python
from termcolor import colored

def cprint(formatter: str, *args):
    colorful = [colored(f"{item}", 'red') for item in args]
    print(formatter.format(*colorful))

# 测试一下 CPRINT
cprint("这是提示信息，后接红色字体输出的变量值：{}", "hello!")
```

Next, we will introduce basic add, delete, modify, and query operations.

### 1.1. Creating Arrays

#### 1.1.1. Creating via Python List
We can create a simple array via the `np.array` syntax:

```python
arr = np.array([1, 2, 3])
cprint("create a simple numpy array: {}", arr)
```

In this syntax, we can provide a Python list or any object with an `Iterable` interface, such as a tuple.

#### 1.1.2. Pre-set Special Arrays
Often, we hope NumPy will create arrays with special values. NumPy indeed provides such support, for example:

---

| Function              | Description                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| zeros<br>zeros_like   | Create an array of all 0s. `zeros_like` accepts another array and generates a zeros array of the same shape and data type. Commonly used for initialization. The following *_like functions are similar. |
| ones<br>ones_like     | Create an array of all 1s.                                                                                              |
| full<br>full_like     | Create an array where all elements are filled with `n`.                                                                 |
| empty<br>empty_like   | Create an empty array.                                                                                                  |
| eye<br>identity       | Create an identity matrix.                                                                                              |
| random.random         | Create a random array.                                                                                                  |
| random.normal         | Create a random array following a normal distribution.                                                                  |
| random.dirichlet      | Create a random array following a Dirichlet distribution.                                                               |
| arange                | Create an incrementing array.                                                                                           |
| linspace              | Create a linearly growing array. The difference from `arange` is that this method generates a fully closed interval array by default. Also, the interval between its elements can be floating-point numbers. |

<!-- There are some less common pre-set functions, such as np.indices -->

```python
# 创建特殊类型的数组
cprint("全 0 数组：\n{}", np.zeros(3))
cprint("全 1 数组：\n{}", np.ones((2, 3)))
cprint("单位矩阵：\n{}", np.eye(3))
cprint("由数字 5 填充的矩阵：\n{}", np.full((3,2), 5))

cprint("空矩阵：\n{}", np.empty((2, 3)))
cprint("随机矩阵：\n{}",np.random.random(10))
cprint("正态分布的数组：\n{}",np.random.normal(10))
cprint("狄利克雷分布的数组：\n{}",np.random.dirichlet(np.ones(10)))
cprint("顺序增长的数组：\n{}", np.arange(10))
cprint("线性增长数组：\n{}", np.linspace(0, 2, 9))
```

!!! warning
    Although the name of the `empty` function implies it should generate an empty array, the generated array actually has values for each element. These values are neither `np.nan` nor `None`, but random values. Before using an array generated by `empty`, we must initialize it and handle these random values.
<!--
    Here, note that the empty array has values when printed, and these values are random. NumPy provides the `empty` function mainly for performance reasons. It allows us to quickly build an array, but we can fill its values later. However, since the data created by `empty` contains random values, we must be careful when using `empty`. In many cases, we would rather use `zeros` than `empty`.
-->

---

Generating normal distribution arrays is very useful. When conducting research, we often need to generate price sequences satisfying certain conditions to further study and compare their characteristics.

For example, if we want to study certain indicators under upward and downward trends, we need the ability to first construct price sequences that conform to trends. The following example demonstrates how to generate such sequences and plot them:

```python
import numpy as np
import matplotlib.pyplot as plt

returns = np.random.normal(0, 0.02, size=100)

fig, axes = plt.subplots(1, 3, figsize=(12,4))
c0 = np.random.randint(5, 50)

for i, alpha in enumerate((-0.01, 0, 0.01)):
    r = returns + alpha
    close = np.cumprod(1 + r) * c0
    axes[i].plot(close)
```

The plotted graph is as follows:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/04/same-vol-different-trend.jpg)

<!--
    In many cases, we need to generate normal distribution arrays. For example, if we want to study the relationship between stock price changes and volatility, such as whether continuous stock price increases and decreases have the same volatility, we can create several return sequences from a decrease of -0.1 to an increase of 0.1, with 0.05 as the step, and then calculate their volatility. At this point, we can use:

    ```python
import numpy as np
import matplotlib.pyplot as plt

returns = np.random.normal(0, 0.02, size=100)

fig, axes = plt.subplots(1, 3, figsize=(12,4))
c0 = np.random.randint(5, 50)

for i, alpha in enumerate((-0.01, 0, 0.01)):
    r = returns + alpha
    close = np.cumprod(1 + r) * c0
    vol = round(np.std(r), 3)
    axes[i].set_title(f"vol={vol}")
    axes[i].plot(close)
```

    This example demonstrates how to generate price sequences from return arrays.

    The conclusion is that sequences of continuous increases, continuous decreases, and sideways consolidation can have the same volatility. What is its significance? We know that high-quality stocks often have low volatility. This gives us a good starting point, and combined with other indicators, we can screen out high-quality stocks. Of course, knowing the relationship between volatility and price changes, we know that conversely, low volatility does not necessarily mean high-quality stocks.
-->

The example also mentions Dirichlet distribution arrays. These arrays have the characteristic that the sum of all their elements equals 1. For example, in the efficient frontier optimization of modern portfolio theory, we first need to initialize the weights of various assets (random values) and satisfy the constraint that the sum of asset weights equals 1 (obviously!). At this point, we can use the Dirichlet[^Dirichlet] distribution.

---

!!! info
    Dirichlet, a German mathematician. He made outstanding contributions to number theory, Fourier series theory, and other fields of mathematical analysis and is considered one of the earliest mathematicians to give the modern definition of a function and one of the founders of analytic number theory.
<!-- Of course, we can also use Gaussian distribution and then regularize it. -->
<!--
    `arange` arrays are similar to `range` syntax, generating an integer array, while `linspace` generates an array with floating-point steps. Additionally, one is a left-closed, right-open interval, and the other is a fully closed interval. What is the use of `linspace`?

    Here is an example: judging moving average trends. Assuming the moving average array is `ma`, with 10 data points, `linspace(ma[0], ma[-1], 10)` is the chord connecting the two ends. Subtract the chord array from the `ma` array. If the value is positive, the moving average is turning downward; otherwise, the moving average is a concave curve, turning upward, and accelerating upwards.
-->
#### 1.1.3. Conversion from Existing Arrays

We can also create new arrays from existing arrays through copying, slicing, repeating, etc.

```python
# 复制一个数组
cprint("通过 np.copy 创建：{}", np.copy(np.arange(5)))

# 复制数组的另一种方法
cprint("通过 arr.copy: {}", np.arange(5).copy())

# 使用切片，提取原数组的一部分
cprint("通过切片：{}", np.arange(5)[:2])

# 合并两个数组
arr = np.concatenate((np.arange(3), np.arange(2)))
cprint("通过 concatenate 合并：{}", arr)

# 重复一个数组
arr = np.repeat(np.arange(3), 2)
cprint("通过 repeat 重复原数组：{}", arr)

# 重复一个数组，注意与 NP.REPEAT 的差异
# NP.TILE 的语义类似于 PYTHON 的 LIST 乘法
arr = np.tile(np.arange(3), 2)
cprint("通过 tile 重复原数组：{}", arr)
```

!!! question
    What is the difference between `np.copy` and `arr.copy`? What other similar function pairs exist in NumPy, and what are their patterns?

<!--
    In array copying, we used two methods: one is `np.copy`, and the other is the `copy` method of the array object itself. What is the difference between these two methods?
-->
---

Note the role of `axis` in the `concatenate` function:

```python
arr = np.arange(6).reshape((3,2))

# 在 ROW 方向上拼接，相当于增加行，默认行为
cprint("按 axis=0 拼接：\n{}", np.concatenate((arr, arr), axis=0))
# 在 COL 方向上拼接，相当于扩展列
cprint("按 axis=1 拼接：\n{}", np.concatenate((arr, arr), axis=1))
```

### 1.2. Adding/Deleting and Modifying Elements
NumPy arrays are of fixed size, and we generally do not recommend frequently adding or deleting elements from arrays. But if there is indeed such a need, we can use the following methods to achieve adding or deleting:
<!--
    If we frequently perform operations that change the size of the array, such as adding and deleting array elements, we generally use Python's `list` as the data structure instead of NumPy's `array`.
-->

| Function | Description                                                                                |
| -------- | ------------------------------------------------------------------------------------------ |
| append   | Add `values` to the end of `arr`.                                                          |
| insert   | Insert value `value` (can be a scalar or an array) at the position specified by `obj` (can be an index, slicing). |
| delete   | Delete elements at specified indices.                                                      |

Examples are as follows:

```python
arr = np.arange(6).reshape((3,2))
np.append(arr, [[7,8]], axis=0)
cprint("指定在行的方向上操作、n{}", arr)

arr = np.arange(6).reshape((3,2))
arr = np.insert(arr.reshape((3,2)), 1, -10)
cprint("不指定 axis，数组被扁平化：\n{}", arr)

arr = np.arange(6).reshape((3,2))
arr = np.insert(arr, 1, (-10, -10), axis=0)
cprint("np.insert:\n{}", arr)

arr = np.delete(arr, [1], axis=1)
cprint("deleting col 1:\n{}", arr)
```

<!--
    `append` operates in the row direction by default, so `axis=0` can be omitted here.
-->

---

!!! tip
    Please definitely run the code here, especially the part about `insert`, to understand what flattening means.
<!--
    Lines 5~11 compare the different behaviors of `insert` with and without specifying `axis`. Pay special attention that if `axis` is not specified, after performing this operation, the array will be flattened into a one-dimensional array, regardless of the dimension of the array before.
-->

<!--
    Line 13 demonstrates how to delete an array element. Note that the second parameter is the coordinate of the element to be deleted, which can be a scalar, a coordinate array, or a slice.
-->

<!--
    Note that in NumPy, most operations do not directly modify the original array but return a new array.
-->

Sometimes we need to modify the values of individual elements. We should operate as follows:

```python
arr = np.arange(6).reshape(2,3)

arr[0,2] = 3
```

This involves how to locate an array element, which is the content of our next section.

<!--
    !!! warning
        In NumPy, most operations do not execute on the original array but copy and return a new array. The following example reminds us to pay attention to the problems that may arise from this:

        ```python
        data = np.array([("aaron", "label")], 
                        dtype=[("name", "O"), ("label", "O")])
        filter = data["name"] == "aaron"

        # AFTER THIS: AARON -> 100
        data["label"][filter] = 100

        # THIS WON'T CHANGE
        data[filter]["label"] = "blogger"
        ```
-->
### 1.3. Locating, Reading, and Searching

#### 1.3.1. Indexing and Slicing

The indexing and slicing syntax in NumPy is roughly similar to Python, with the main difference being support for multi-dimensional arrays:

```python
arr = np.arange(6).reshape((3,2))
cprint("原始数组：\n{}", arr)

# 切片语法
cprint("按行切片：{}", arr[1, :])
cprint("按列切片：{}", arr[:, -1])
cprint("逆排数组：\n {}", arr[: : -1])

# FANCY INDEXING
cprint("fancy index: 使用下标数组：\n {}", arr[[2, 1, 0]])

```

The above slicing syntax also exists in Python, but it only supports up to one dimension. Therefore, for the following Python array, similar operations will fail:

---

```python
arr = np.arange(6).reshape((3,2)).tolist()

arr[1, :]
```

Prompt: `list indices must be integers or slices, not tuple`.

<!--
    In the above code, we also converted the NumPy array to a Python list via `tolist()`. Conversion between NumPy objects and Python objects often occurs, especially conversion between time objects, which needs to be mastered proficiently.
-->

#### 1.3.2. Finding, Filtering, and Replacing

In the previous section, we located an array element via indexing. But often, we first need to find the indices that meet the requirements through conditional operations. This section will introduce related methods.

| Function          | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| np.searchsorted | Search for specified values in an ordered array and return the index. |
| np.nonzero      | Return the indices of non-zero elements, used to find elements in the array that meet the conditions. |
| np.flatnonzero  | Same as `nonzero`, but returns the indices of non-zero elements in the flattened version of the input array. |
| np.argwhere     | Return the indices of elements that meet the conditions, equivalent to the transpose version of `nonzero`. |
| np.argmin       | Return the index of the smallest element in the array (note: not the smallest index that meets the conditions). |
| np.argmax       | Return the index of the largest element in the array.         |

```python

# 查找
arr = [0, 2, 2, 2, 3]
pos = np.searchsorted(arr, 2, 'right')
cprint("在数组 {} 中寻找等于 2 的位置，返回 {}, 数值是 {}", 
        arr, pos, arr[pos - 1])

arr = np.arange(6).reshape((2, 3))
cprint("arr[arr > 1]: {}", arr[arr > 1])

# NONZERO 的用法
mask = np.nonzero(arr > 1)
cprint("nonzero 返回结果是：{}", mask)
cprint("筛选后的数组是：{}", arr[mask])

# ARGWHERE 的用法
mask = np.argwhere(arr > 1)
cprint("argwere 返回的结果是：{}", mask)
```

---

```python
# 多维数组不能直接使用 ARGWHERE 结果来筛选
# 下面的语句不能得到正确结果，一般会出现 INDEXERROR
arr[mask]

# 但对一维数组筛选我们可以用：
arr = np.arange(6)
mask = np.argwhere(arr > 1)
arr[mask.flatten()[0]]

# 寻找最大值的索引
arr = [1, 2, 2, 1, 0]
cprint("最大值索引是：{}", np.argmax(arr))
```

When using `searchsorted`, note that the array itself must be ordered; otherwise, it will not yield correct results.
<!--
    Why do we talk about this function? After becoming familiar with NumPy, everyone might want to represent all data using NumPy arrays. We remind everyone through this example that searching in NumPy, due to the lack of indexing, is actually slower. It can only speed up when the data is already ordered. Therefore, we cannot represent all data using NumPy.
-->

Lines 10 to 21 show how to find data in an array that meets the conditions and return its index.

<!--
    In many scenarios, we care about the position of data that meets the conditions, not its value. For example, in Tongda Xin company, there is a `barssince` function that requires calculating how many bars have passed since the condition was met. This is an example where we only care about the index position.
-->

The return value of `argwhere` is equivalent to the transpose of `nonzero`. In the case of multi-dimensional arrays, it cannot be directly used as an array index. Please compare the usage of `nonzero` and `argwhere` yourself.

<!--
    Functions starting with `arg` are not entirely for returning index values. For example, `argsort` is used for sorting, but it returns the sorted indices, similar to `rank`. But `rank` returns the ranking, while `argsort` returns the index.

    ```python
import numpy as np

# 创建一个数组
arr = np.array([3, 1, 2])

# 使用 ARGSORT 获取排序后的索引
sorted_indices = np.argsort(arr)

# 再次使用 ARGSORT 获取排名
ranks = np.argsort(sorted_indices) + 1

print("Ranks:", ranks)
```
-->

In quantitative finance, there are many situations requiring filtering functionality. For example, when calculating upper and lower shadows, we use the formula $(high - max(open, close))/(high - low)$ for calculation. If we want to calculate the upper shadows for the past $n$ periods all at once without using loops, we must use filtering functions like `np.where` and `np.select`.

<!-- There are more efficient implementations for this function alone -->

The following example shows how to use `np.select` to calculate upper shadows:

```python
import pandas as pd
import numpy as np

bars = pd.DataFrame({
    "open": [10, 10.2, 10.1],
    "high": [11, 10.5, 9.3],
    "low": [9.8, 9.8, 9.25],
    "close": [10.1, 10.2, 10.05]
})
```

---

```python
max_oc = np.select([bars.close > bars.open, 
                    bars.close <= bars.open], 
                    [bars.close, bars.open])
print(max_oc)

shadow = (bars.high - max_oc)/(bars.high - bars.low)
print(shadow)

```

`np.where` is a function similar to `np.select`, but it only accepts one condition.

```python
arr = np.arange(6)
cprint("np.where: {}", np.where(arr > 3, 3, arr))
```

This code implements the function of clipping numbers above 3 to 3. This function is called `clip`, a very common technique in factor preprocessing used to handle outliers.

But it cannot achieve clipping at both ends. At this point, `np.select` can do it, which is the main difference between `np.where` and `np.select`:

```python
arr = np.arange(6)
cprint("np.select: {}", np.select([arr<2, arr>4], [2, 4], arr))
```
The result is that in the generated array, values less than 2 are replaced with 2, values greater than 4 are replaced with 4, and others remain unchanged.

<!--
    There is another type of filtering: randomly selecting several samples from a set, which we will discuss in the random number section.
-->

<!--
    The methods introduced above, whether indexing or slicing, ultimately lead us to locate the elements of the array. Obviously, with this location, we can modify array elements. However, we must also emphasize the concepts of view and copy here. Because depending on how we locate elements, the result we get may be a view of the original array or a copy of the original array. The former can modify the original array elements, while the latter can only modify the copy.

    #### Views and Copies

    NumPy arrays are actually composed of two parts: one is the continuous data buffer containing the actual data elements; the other is the metadata about the array. Metadata includes data type, strides, and other important information that makes it easier to operate on `ndarray`, such as `shape`.

    This organization brings a benefit: it is possible to access and operate on the original array in different ways by only changing certain metadata (such as data type and `shape`) without changing the data buffer, but it looks like a new array. These new arrays are called views.

    Most positioning operations in NumPy return views, but some return a copy of the original array. The rule is that basic indexing always creates views. So, we can modify an array as follows:

    ```python
x = np.arange(10)

# 创建了一个视图
y = x[1:3]
x[1:3] = [10, 11]
```

    Now `y` and `x[1:3]` hold the same values. Therefore, the modification is made on the original data buffer.

    On the other hand, advanced indexing always creates copies, for example:

    ```python
x = np.arange(9).reshape(3,3)
cprint("原始数组、n{}", x)

y = x[[1, 2]]
cprint("高级索引创建了副本、n{}", y)

# 现在我们修改高级索引副本值
x[[1,2]] = [[10, 11, 12], [13, 14, 15]]
cprint("就地赋值改变了 x\n{}", x)

cprint("但 y 是副本、n{}", y)
cprint("副本的 base 属性{}", y.base)
cprint("视图的 base 属性{}", x[1:2].base)
```

    The most difficult part to understand in the above example is line 8. We must remember that this is a case of so-called in-place assignment, where no view or copy is created at this time.

    The example also gives the standard for determining whether an array is a copy or a view. If an array is a view, its `base` will point to the original array. The `base` of a copy will point to `None`.

    We will introduce another common but error-prone example after introducing Structured arrays.
-->

### 1.4. Inspecting Arrays
<!-- Understand the usage of numpy's dtype, shape, ndim, size, and len. -->

When calling other people's libraries, we often need to exchange data with them. At this time, there may be data format incompatibility issues. To be able to troubleshoot, we must master some methods for viewing the characteristics of NumPy arrays.

We first generate a simple array as follows, and then view its various characteristics:

```python

arr = np.ones((3,2))
cprint("dtype is: {}", arr.dtype)
cprint("shape is: {}", arr.shape)
cprint("ndim is: {}", arr.ndim)
```

---

```python
cprint("size is: {}", arr.size)
cprint("'len' is also available: {}", len(arr))

# DTYPE
dt = np.dtype('>i4')
cprint("byteorder is: {}", dt.byteorder)
cprint("name of the type is: {}", dt.name)
cprint('is ">i4" a np.int32?: {}', dt.type is np.int32)

# 复杂的 DTYPE
complex = np.dtype([('name', 'U8'), ('score', 'f4')])
arr = np.array([('Aaron', 85), ('Zoe', 90)], dtype=complex)
cprint("A structured Array: {}", arr)
cprint("Dtype of structured array: {}", arr.dtype)
```

Just as Python objects have their own data types, NumPy arrays also have their own data types. We can view the data type of the array via `arr.dtype`.

<!--
    Here, we generated the array via `np.ones`, and all elements of the array are 1. Note that the dtype we obtained is `np.float64`, which is also the most common data type in NumPy.
-->

From line 3 to line 6, we output the array's `shape`, `ndim`, `size`, and `len` attributes, respectively. `ndim` tells us the dimension of the array. `shape` tells us the size of each dimension. `shape` itself is a tuple, and the size of this tuple equals `ndim`.

`size` returns the product of the values of each element in `shape` when no parameters are passed. `len` returns the length of the first dimension.

### 1.5. Array Operations
<!-- Introduce related operations that change the shape, size, etc., of the array -->

We have already seen some examples in the previous sections that cause changes in array shape. For example, to generate a $3×2$ array, we first use `np.arange(6)` to generate a one-dimensional array, and then change its shape to (2, 3).

Another example is using `np.concatenate`, which changes the rows or columns of the array.

#### 1.5.1. Dimension Increasing
We can change the dimension of the array via `reshape`, `hstack`, `vstack`:

---

```python

cprint("increase ndim with reshape:\n{}", 
        np.arange(6).reshape((3,2)))

# 将两个一维数组，堆叠为 2*3 的二维数组
cprint("createing from stack: {}", 
        np.vstack((np.arange(3), np.arange(4,7))))

# 将两个 （3，1）数组，堆叠为（3，2）数组
np.hstack((np.array([[1],[2],[3]]), np.array([[4], [5], [6]])))
```

#### 1.5.2. Dimension Decreasing

Perform dimension reduction on the array via `ravel`, `flatten`, `reshape`, `*split` operations.
<!-- Many operations, such as `argwhere`, will return dimension-increasing results, at which point we may need to reduce the dimension before use -->

```python

cprint("ravel: {}", arr.ravel())

cprint("flatten: {}", arr.flatten())

# RESHAPE 也可以用做扁平化
cprint("flatten by reshape: {}", arr.reshape(-1,))

# 使用 HSPLIT, VSPLIT 进行降维
x = np.arange(6).reshape((3, 2))
cprint("split:\n{}", np.hsplit(x, 2))

# RAVEL 与 FLATTEN 的区别：RAVEL 可以操作 PYTHON 的 LIST
np.ravel([[1,2,3],[4, 5, 6]])
```

This introduces a total of 4 methods. `ravel` and `flatten` have similar usage. The behavior of `ravel` is similar to `flatten`, except that `ravel` is a function of `np` and can act on `ArrayLike` arrays.

Flattening via `reshape` is also a common operation. Additionally, `vsplit` and `hsplit` functions are introduced, whose functions are exactly opposite to `vstack` and `hstack`.

#### 1.5.3. Transposition

Additionally, transposing the array is also one such example.

---

For example, earlier we mentioned that the result of `np.argwhere` is actually the transpose of `np.nonzero`. Let's verify this:

```python
x = np.arange(6).reshape(2,3)
cprint("argwhere: {}", np.argwhere(x > 1))

# 我们再来看 NP.NONZERO 的转置
cprint("nonzero: {}", np.array(np.nonzero(x > 1)).T)
```

The two output results are exactly the same. Here, we achieved transposition via `.T`, which is a syntax sugar. The formal function is `transpose`.

Of course, due to the extreme power of the `reshape` function, we can also use it to complete transposition:

```python
cprint("transposing array from \n{} to \n{}", 
    np.arange(6).reshape((2,3)),
    np.arange(6).reshape((3,2)))
```

<about/>
