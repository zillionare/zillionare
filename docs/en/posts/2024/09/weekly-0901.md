---
title: "QuanTide Weekly: FFT Stock Analysis & Numpy Basics"
date: 2024-09-01
slug: en/posts/uncategory/weekly-0901
tags: [Quantitative Investing, Factor Investing, Machine Learning, Technical Analysis]
excerpt: "Market rumors on mortgage rates spark real estate rallies. China's August PMI dips to 49.1%. Alibaba completes regulatory overhaul. This week: FFT for stock prediction and essential Numpy programming for quants."
lang: en
translation_of: posts/uncategory/weekly-0901
auto_translated: true
source_sha: c93c5540f5d5c7914df3bd9aa244bd5c22779c42
cover: "stamp_width: 60%"
---

### This Week's Highlights

* Market rumors of lower existing mortgage rates drive real estate ETFs higher, though several stocks hit price limits before closing.
* China's official August manufacturing PMI stands at 49.1%, down 0.3 percentage points from the previous month.
* State Administration for Market Regulation announces Alibaba has completed its three-year regulatory overhaul.
* First semi-annual report of the year! Tongkun Shares reports a 911.35% year-on-year growth, the highest net profit growth among companies that have released their semi-annual reports.

### Next Week's Watchlist
* Will rumors of lower existing mortgage rates materialize?
* Release of the Caixin Manufacturing PMI on Monday.
* The 2024 Low-Altitude Economy Development Conference will be held in Wuhu from September 6 to 8.

### This Week's Selection

* Are Main Force Funds Entering? Research on Fast Fourier Transform and Stock Price Prediction
* Series! Numpy Programming Essential for Quants (1)

---

## This Week's Highlights

* **Mortgage Rate Rumors:** Market speculation suggests authorities are considering further reductions in existing mortgage rates, allowing up to 38 trillion RMB in existing mortgages to be refinanced. The goal is to reduce household debt burdens and boost consumption.<remark>As of Saturday, these rumors have not been officially confirmed.</remark>
* **PMI Data:** August's PMI was **49.1%**, a 0.3 percentage point decline month-over-month. By enterprise size, large enterprises' PMI was 50.4%, remaining above the critical threshold; SMEs' PMIs were 48.7% and 46.4%, down **0.7** and 0.3 percentage points month-over-month, respectively.<remark>The August PMI was influenced by high temperatures and did not significantly exceed expectations.</remark>
* **Alibaba's Overhaul:** On the afternoon of August 30, the State Administration for Market Regulation announced that Alibaba had completed its three-year regulatory overhaul with positive results. Alibaba's stock price has fallen by 70% from its 2020 peak.
* **US Market Performance:** On Friday, US major indices rose collectively. The Dow Jones Industrial Average gained 0.55% to close at 41,563.08, **setting a new all-time high**. The S&P 500 rose 1.01%, and the Nasdaq Composite rose 1.13%. The July PCE inflation data, favored by the Federal Reserve, largely met expectations. Markets have reduced bets on a significant Fed rate cut in September but still anticipate substantial cuts in November or December.
* **Nasdaq 100 ETF Report:** E Fund's Nasdaq 100 ETF released its 2024 interim report. Changzhou Investment Group holds a 5.92% share, becoming the largest holder. Despite a net asset value (NAV) increase of 49.21%, the ETF still gained 14.91% year-to-date. Launched in 2017, its current NAV is 3.16.
* **Semi-Annual Report Leader:** Tongkun Shares released its semi-annual report, achieving a net profit of 1.065 billion RMB, a 911.35% year-on-year increase, the highest net profit growth among companies that have released their reports. During the reporting period, downstream demand for polyester filament showed significant marginal improvement compared to the previous year, with increased product sales and price spreads. **The industry is generally in a recovery phase.** Overall, the electronics sector emerged as the big winner, with revenue growth leading all sectors year-on-year. The sector's total revenue for the first half of the year was 1.59 trillion RMB, up 17.3% year-on-year.

<claimer>Source: East Money Website</claimer>

---

## Next Week's Watchlist
* **Mortgage Rate Rumors:** Friday's market rumors suggested authorities were considering lowering existing mortgage rates, causing real estate ETFs to surge and bank stocks to drop sharply in response. However, prices fell back near the close, with many stocks hitting price limits breaking open. Next week, will this rumor be confirmed or debunked? It could significantly impact the market.
* **Caixin PMI:** Release of the Caixin Manufacturing PMI on Monday.
* **Low-Altitude Economy Conference:** The 2024 Low-Altitude Economy Development Conference will be held in Wuhu from September 6 to 8.
* **US Economic Data:** Release of US August unemployment rate and non-farm payrolls reports on Friday.

---

# Are Main Force Funds Entering? Research on Fast Fourier Transform and Stock Price Prediction

An undeniable fact: economic activity is cyclical. However, this fact seems to have been long ignored by the quantitative community. Whether in asset pricing theory or trend trading theory, we rarely find a place for cyclical research -- in the latter context, people prefer terms like "oscillation" rather than explicitly stating "cycle."

In this article, we explore cycles in the stock market. We will use the Fast Fourier Transform (FFT) to decompose time-series signals into frequency-domain signals, identify main force funds through signal energy, and make some predictions based on their operational cycles. Finally, we present three hypotheses, one of which has been proven.

## FFT - Time-Frequency Conversion

(Data acquisition part omitted).

We have obtained the Shanghai Composite Index data for the past year. Clearly, it is a time-series signal. The Fourier Transform is precisely designed to convert time-series signals into frequency-domain signals. In other words, the Fourier Transform can decompose the Shanghai Composite Index into a combination of several sine waves.

```python
# Apply Fourier Transform
fft_result = np.fft.fft(close)
freqs = np.fft.fftfreq(len(close))

# Inverse Fourier Transform
filtered = fft_result.copy()
filtered[20:] = 0
inverse_fft = np.fft.ifft(filtered)
```

---

```python
# Plot original signal and reconstructed signal
plt.figure(figsize=(14, 7))
plt.plot(close, label='Original Close')
plt.plot(np.real(inverse_fft), label='Reconstructed from Sine Waves')
plt.legend()
```

The output we obtained is as follows:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/real-vs-synthetic.jpg)

In the field of digital signal processing, time-series are called time-domain signals, and after Fourier Transform, we obtain frequency-domain signals. Time-domain and frequency-domain signals can be converted into each other. The `fft` library in Numpy provides `fft` and `ifft` functions to help us implement these conversions.

`np.fft.fft` transforms time-domain signals into frequency-domain signals. The result is a complex array representing the amplitude (i.e., energy) of each frequency component decomposed from the signal. Frequencies are arranged from low to high, with the 0th element having a frequency of 0, which is the DC component, a linear function of the signal's mean.

`np.fft.ifft` is the inverse transform of `fft`, converting frequency-domain signals back into time-domain signals.

Transforming time-domain signals into the frequency domain reveals basic characteristics such as signal periodicity. We can also perform operations on the frequency-domain signals obtained from the FFT and then transform them back, which is the essence of digital signal processing.

---

## High-Frequency Filtering and Compression

If we set the energy of high-frequency signals to zero and then inverse-transform the signal, we obtain a new sequence similar to the original but smoother -- this is what we commonly refer to as low-pass filtering. Various moving averages you are familiar with are also low-pass filters.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml-promotion.png)

In the code above, we only retained the energy of the first 20 low-frequency signals, resulting in a new sequence similar to the original. If this method were applied to the image field, it would achieve lossy compression -- with a compression ratio of 250/20.

In the 1990s, the most advanced image compression algorithms were based on this principle -- retaining the mid-to-low frequency parts of the image and treating high-frequency parts as noise to be removed. This preserves the image's main features while significantly reducing the amount of data to be stored.

---

Those who worked on such compression algorithms at the time would recognize this beautiful young lady -- Lena. This photo is the standard test sample for image algorithms. Through long-term evolution, under survival pressure, humans have developed superhuman abilities to recognize others' expressions. Therefore, compared to other samples, once compression causes a decline in image quality, the human eye is more likely to detect changes in faces and expressions. Thus, face images became the best test samples.

<div style='width:50%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/lena.jpg'>
<span style='font-size:0.6rem'>Lena </span>
</div>

Lena was a model for *Playboy* magazine. This photo is a small part of her seductive photo shoot for the November 1972 issue of *Playboy* -- in the original photo, Lena boldly displayed her seductive hip curves, but those unorthodox scientists only shared her smile with us -- from a research perspective, this is also the part with the highest information ratio.

Coincidentally, before Lena became the standard test sample for digital image processing, scientists used photos of another young lady, also from *Playboy*.

Well, back to the topic. We just shared a method to remove high-frequency noise from signals, making the signal's meaning more prominent. We also hope to use similar techniques in securities analysis to reveal signals hidden in K-line charts.

But if we simply copy methods from other fields, it hardly counts as research, and it's difficult to achieve good results. In fact, for securities signals, we should focus more on signal energy than frequency, after all, we want to stand on the side of the most powerful players.

---

<div style='text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/may-the-force-be-with-you.jpg'>
<span style='font-size:0.6rem'>May the Force be with you -- Star Wars</span>
</div>

So, let's change our approach. Let's retain the most energetic parts of the decomposed frequency-domain signals and see what they look like.

## Filtering Low-Energy Signals

```python
# Retain the top 5 signals with the strongest energy
amp_threshold = np.sort(np.abs(fft_result))[-11]

# Plot each sine wave component
plt.figure(figsize=(14, 7))

theforce = []
for freq in freqs:
    if freq == 0:  # Handle DC component
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

The frequencies given by FFT always come in positive and negative pairs. We can simply consider that negative frequencies are meaningless to us -- they are a form of dark energy we cannot see and need not care about. Therefore, in the code, we ignore this part.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/individual-sine-wave.jpg)

We see that the wave (orange) with the strongest impact on the Shanghai Composite Index has a cycle of about 7 months: it takes 3.5 months from peak to trough and another 3.5 months from trough to peak. Since its energy is almost double that of other waves, it dominates the trend of the entire superimposed wave: if other waves are in phase with it, the superposition result will strengthen the trend; conversely, it will offset the trend. The energies of other waves are similar, but their frequencies differ.

---

What exactly are these waves? They can be economic cycles, but ultimately, economic cycles are driven by people or reflect human judgment. Therefore, we can view the cycle of fluctuations as the **operational cycle of capital**.

From this decomposition chart, we can hypothesize that there is long-term capital (corresponding to the blue wave) that rebalances its portfolio once a year or so. There is medium-term capital (corresponding to the orange wave) that rebalances every half year or so. Other capital is short-term, changing positions about every three months. There are countless high-frequency waves we have filtered out, which trade frequently, possibly corresponding to retail investors, but their energy is small and can generally be ignored; only in extremely rare cases can they form same-direction superpositions, thereby affecting the trend.

Now, let's synthesize the operations of these capital flows and compare them with the actual trend to see how it goes:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/real-vs-5-waves-synthetic.jpg)

The large cycles basically match, meaning these capital flows basically dictate the market trend. Moreover, we seem to be able to assert that between March 15 and May 17, there was a divergence trend between stock prices and main force funds: main force funds were withdrawing, but retail investors were still trading. Thus, although stock prices were still rising, the final direction was determined by main force funds.

---

!!! tip
    The black line is synthesized from main force fund waves (predictive for the future). Before fundamental changes in the market, main force funds' operational style is relatively fixed, so it may have some short-term predictive capability. If we accept this conclusion, we should note that there is another divergence at the end -- retail investors are still leaving, but main force funds are entering. Of course, please do not take this too seriously.

## Explanation of the DC Component

I used to think the DC component indicated the trend of asset prices, but in fact, all waves are horizontal -- but only commodity markets are horizontal, while stock markets are essentially upward. Therefore, the DC component cannot indicate the trend of asset prices.

Until today, a sudden idea struck me: if you segment a longer time-series signal and perform FFT decomposition, you will obtain several DC components. The regression line of these DC components is the trend of asset prices.

Here are three hypotheses:

1. If the energy distribution across various frequencies does not change significantly after segmented decomposition, it indicates that the composition of investors and their operational styles have not changed significantly. We can use FFT to predict short-term future trends until the conditions are no longer met.
   

2. The DC components of the Shanghai Composite Index over the past 30 years should be able to perfectly fit a trend line, and its slope equals the slope of the 20-year regression line of the Shanghai Composite Index.
3. Securities prices are a combination of the DC component trend line and a series of sine waves.

---

Below, we prove the second hypothesis (process omitted). Finally, we plot the DC components and trend line as shown below:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/dc-regression.jpg)

And the annual lines and trend lines of China A-shares since 2005 are as follows:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/a-share-yearly.jpg)

It's not just similar; it's almost exactly the same.

The p-value for the trend line fit is around 0.055, which basically meets the 0.05 confidence level requirement.

---

This article is from our *Factor Investing and Machine Learning Strategies* course, appearing in the section on how to explore new factor methodologies. Some important results obtained from FFT transformations will serve as features for training machine learning strategies. More content will be covered in our classes!

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml-promotion.png)

<!-- If I hadn't read Ray Dalio's *Principles*, I would almost believe that stock price fluctuations have nothing to do with economic cycles. But there has always been a faint belief that since economic activity has cycles, stock price fluctuations must also have cycles. -->

---

# Numpy Programming Essential for Quants (1) - Core Syntax

# Mastering NumPy for Quantitative Finance: Data Structures & Operations

This guide covers essential NumPy data structures, array creation, manipulation, and indexing techniques critical for quantitative finance research and factor modeling.

## 1. Fundamental Data Structures

The core data structure of NumPy is the `ndarray` (n-dimensional array). This object represents a fixed-size, homogeneous, multi-dimensional array.

Because `ndarray` can only store homogeneous objects, it cannot natively express record-type data. To address this, NumPy introduced the `structured array`. It uses a `void`-type tuple to represent a single record, enabling NumPy to handle record-based data. Thus, there are primarily two array-related data types in NumPy:

1.  The standard `ndarray`, which is widely known and used for most NumPy operations.
2.  The `structured array`, frequently used in quantitative finance. For instance, market data obtained via JQData’s `jqdatasdk` [^JQData] can return this data type. Compared to Pandas DataFrames, it offers certain conveniences in data access. We will dedicate a separate section to this later.

Before using NumPy, install and import the library:

```bash
# Install NUMPY
pip install numpy
```

---

Typically, we import and use NumPy under the alias `np`:

```python
import numpy as np
```

To make result displays more prominent in Jupyter Notebooks, we first define a `cprint` function. It outputs提示信息 (prompts) verbatim but renders variable values in red text for distinction:

```python
from termcolor import colored

def cprint(formatter: str, *args):
    colorful = [colored(f"{item}", 'red') for item in args]
    print(formatter.format(*colorful))

# Test CPRINT
cprint("This is a prompt, followed by red-text variable values: {}", "hello!")
```

Next, we introduce basic CRUD (Create, Read, Update, Delete) operations.

### 1.1. Creating Arrays

#### 1.1.1. Creating from Python Lists
We can create a simple array using the `np.array` syntax:

```python
arr = np.array([1, 2, 3])
cprint("create a simple numpy array: {}", arr)
```

In this syntax, we can provide a Python list or any object implementing the `Iterable` interface, such as a tuple.

#### 1.1.2. Pre-defined Special Arrays
Often, we want NumPy to create arrays with specific values. NumPy provides support for this, as shown in the table below:

| Function | Description |
| :--- | :--- |
| `zeros`<br>`zeros_like` | Creates an array of all zeros. `zeros_like` accepts another array and generates a zeros array with the same shape and data type. Commonly used for initialization. The `_like` suffix applies to other functions below. |
| `ones`<br>`ones_like` | Creates an array of all ones. |
| `full`<br>`full_like` | Creates an array where all elements are filled with `n`. |
| `empty`<br>`empty_like` | Creates an empty array. |
| `eye`<br>`identity` | Creates an identity matrix. |
| `random.random` | Creates a random array. |
| `random.normal` | Creates a random array following a normal distribution. |
| `random.dirichlet` | Creates a random array following a Dirichlet distribution. |
| `arange` | Creates an incrementing array. |
| `linspace` | Creates a linearly increasing array. Unlike `arange`, this method defaults to a closed interval. Additionally, the interval between elements can be floating-point numbers. |

<!--Some less common pre-defined functions exist, such as np.indices-->

```python
# Create special types of arrays
cprint("Array of all zeros:\n{}", np.zeros(3))
cprint("Array of all ones:\n{}", np.ones((2, 3)))
cprint("Identity matrix:\n{}", np.eye(3))
cprint("Matrix filled with number 5:\n{}", np.full((3,2), 5))

cprint("Empty matrix:\n{}", np.empty((2, 3)))
cprint("Random matrix:\n{}",np.random.random(10))
cprint("Normal distribution array:\n{}",np.random.normal(10))
cprint("Dirichlet distribution array:\n{}",np.random.dirichlet(np.ones(10)))
cprint("Sequentially increasing array:\n{}", np.arange(10))
cprint("Linearly increasing array:\n{}", np.linspace(0, 2, 9))
```

!!! warning
    Although the name `empty` suggests it generates an empty array, the generated array actually contains values. These values are neither `np.nan` nor `None`, but random garbage values. Before using an array generated by `empty`, you must initialize it to handle these random values.
<!--
Note here that empty arrays display values when printed; these values are random. NumPy provides the `empty` function primarily for performance reasons. It allows us to quickly build an array, which we can then populate with values later. However, since `empty` creates data with random values, we must be cautious when using it. In many cases, we prefer using `zeros` over `empty`.
-->

---

Generating normal distribution arrays is highly useful. In research, we often need to generate price sequences satisfying specific conditions to further study and compare their characteristics.

For example, if we want to study indicators under upward and downward trends, we must first be able to construct price sequences that fit these trends. The following example demonstrates how to generate such sequences and plot them:

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
In many cases, we need to generate normal distribution arrays. For instance, if we want to study the relationship between stock price changes and volatility, such as whether continuous price increases and decreases yield the same volatility, we can create return sequences ranging from -0.1 to 0.1 in steps of 0.05, and then calculate their volatility. At this point, we can use:

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

The conclusion is that continuously rising, continuously falling, and sideways sequences can have the same volatility. What is the significance of this? We know that high-quality stocks often exhibit low volatility. This gives us a good starting point. Combined with other indicators, we can screen for high-quality stocks. Of course, knowing the relationship between volatility and price direction, we understand that low volatility does not necessarily imply high-quality stocks.
-->

The example also mentions Dirichlet distribution arrays. These arrays have the characteristic that all their elements sum to 1. For example, in the efficient frontier optimization of Modern Portfolio Theory, we first need to initialize the weights of various assets (random values) while satisfying the constraint that the sum of asset weights equals 1 (obviously!). In such cases, we can use the Dirichlet[^Dirichlet] distribution.

---

!!! info
    Dirichlet, a German mathematician. He made outstanding contributions to number theory, Fourier series theory, and other fields of mathematical analysis, and is considered one of the earliest mathematicians to provide the modern definition of a function and one of the founders of analytic number theory.
<!--We can also use Gaussian distribution and then regularize it.-->

<!--
The `arange` array is similar to the `range` syntax, generating an integer array, while `linspace` generates an array with floating-point steps. Additionally, one is a left-closed, right-open interval, while the other is a fully closed interval. What is the use of `linspace`?

Here is an example: judging moving average trends. Assume the moving average array is `ma`, with 10 data points. Then `linspace(ma[0], ma[-1], 10)` represents the chord connecting the two ends. Subtracting the chord array from the `ma` array: if the value is positive, the moving average is turning downward; otherwise, it is a concave curve, turning upward, indicating accelerating growth.
-->

#### 1.1.3. Converting from Existing Arrays

We can also create new arrays from existing ones through copying, slicing, repeating, and other methods:

```python
# Copy an array
cprint("Created via np.copy: {}", np.copy(np.arange(5)))

# Another method to copy an array
cprint("Via arr.copy: {}", np.arange(5).copy())

# Use slicing to extract a portion of the original array
cprint("Via slicing: {}", np.arange(5)[:2])

# Merge two arrays
arr = np.concatenate((np.arange(3), np.arange(2)))
cprint("Merged via concatenate: {}", arr)

# Repeat an array
arr = np.repeat(np.arange(3), 2)
cprint("Repeated original array via repeat: {}", arr)

# Repeat an array. Note the difference with NP.REPEAT.
# The semantics of NP.TILE are similar to Python's list multiplication.
arr = np.tile(np.arange(3), 2)
cprint("Repeated original array via tile: {}", arr)
```

!!! question
    What is the difference between `np.copy` and `arr.copy`? What other similar function pairs exist in NumPy, and what are their patterns?

<!--
When copying arrays, we used two methods: `np.copy` and the array object's own `copy`. What is the difference between these two methods?
-->

---

Note the role of `axis` in the `concatenate` function:

```python
arr = np.arange(6).reshape((3,2))

# Concatenate along ROWS, equivalent to adding rows (default behavior)
cprint("Concatenated via axis=0:\n{}", np.concatenate((arr, arr), axis=0))
# Concatenate along COLS, equivalent to expanding columns
cprint("Concatenated via axis=1:\n{}", np.concatenate((arr, arr), axis=1))
```

### 1.2. Adding/Deleting and Modifying Elements

NumPy arrays are fixed-size. Generally, we do not recommend frequently adding or deleting elements from an array. However, if such a need arises, we can use the following methods:
<!--
If we frequently perform operations that change the array size, such as adding or deleting elements, we generally use Python's `list` as the data structure instead of NumPy's `array`.
-->

| Function | Description |
| :--- | :--- |
| `append` | Adds `values` to the end of `arr`. |
| `insert` | Inserts value `value` (scalar or array) at the position specified by `obj` (index or slicing). |
| `delete` | Deletes elements at specified indices. |

Examples are as follows:

```python
arr = np.arange(6).reshape((3,2))
np.append(arr, [[7,8]], axis=0)
cprint("Operation specified along rows, n{}", arr)

arr = np.arange(6).reshape((3,2))
arr = np.insert(arr.reshape((3,2)), 1, -10)
cprint("Without specifying axis, array is flattened:\n{}", arr)

arr = np.arange(6).reshape((3,2))
arr = np.insert(arr, 1, (-10, -10), axis=0)
cprint("np.insert:\n{}", arr)

arr = np.delete(arr, [1], axis=1)
cprint("deleting col 1:\n{}", arr)
```

<!--
`append` defaults to operating along rows; here, `axis=0` can be omitted.
-->

---

!!! tip
    Please definitely run the code here, especially the parts regarding `insert`, to understand what "flattening" means.
<!--
Lines 5–11 compare the behavior of `insert` with and without specifying `axis`. Pay special attention: if `axis` is not specified, the array will be flattened into a one-dimensional array after this operation, regardless of the original array's dimensions.
-->

<!--
Line 13 demonstrates how to delete an array element. Note that the second parameter is the coordinate of the element to be deleted; it can be a scalar, a coordinate array, or a slice.
-->

<!--
Note that in NumPy, most operations do not modify the original array in place but return a new array.
-->

Sometimes we need to modify the values of individual elements. This is how to do it:

```python
arr = np.arange(6).reshape(2,3)

arr[0,2] = 3
```

This involves how to locate an array element, which is the content of our next section.

<!--
!!! warning
    In NumPy, most operations do not execute on the original array but copy and return a new array. The following example reminds us of potential issues arising from this:

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
cprint("Original array:\n{}", arr)

# Slicing syntax
cprint("Slice by row: {}", arr[1, :])
cprint("Slice by column: {}", arr[:, -1])
cprint("Reversed array:\n {}", arr[: : -1])

# FANCY INDEXING
cprint("fancy index: using index array:\n {}", arr[[2, 1, 0]])

```

The above slicing syntax exists in Python but only supports one dimension. Therefore, similar operations on the following Python array will fail:

---

```python
arr = np.arange(6).reshape((3,2)).tolist()

arr[1, :]
```

This raises the error: `list indices must be integers or slices, not tuple`.

<!--
In the above code, we also converted the NumPy array to a Python list via `tolist()`. Conversions between NumPy objects and Python objects occur frequently, especially conversions involving time objects, which require mastery.
-->

#### 1.3.2. Searching, Filtering, and Replacing

In the previous section, we located array elements via indexing. However, in many cases, we must first find the indices that meet specific conditions through conditional operations. This section introduces related methods.

| Function | Description |
| :--- | :--- |
| `np.searchsorted` | Searches for a specified value in a sorted array and returns the index. |
| `np.nonzero` | Returns the indices of non-zero elements, used to find elements in an array that meet conditions. |
| `np.flatnonzero` | Same as `nonzero`, but returns the indices of non-zero elements in the flattened version of the input array. |
| `np.argwhere` | Returns the indices of elements that meet conditions, equivalent to the transposed version of `nonzero`. |
| `np.argmin` | Returns the index of the smallest element in the array (note: not the smallest index that meets a condition). |
| `np.argmax` | Returns the index of the largest element in the array. |

```python

# Search
arr = [0, 2, 2, 2, 3]
pos = np.searchsorted(arr, 2, 'right')
cprint("Searching for position equal to 2 in array {}, returns {}, value is {}", 
        arr, pos, arr[pos - 1])

arr = np.arange(6).reshape((2, 3))
cprint("arr[arr > 1]: {}", arr[arr > 1])

# Usage of NONZERO
mask = np.nonzero(arr > 1)
cprint("nonzero returns: {}", mask)
cprint("Filtered array is: {}", arr[mask])

# Usage of ARGWHERE
mask = np.argwhere(arr > 1)
cprint("argwhere returns: {}", mask)
```

---

```python
# Multi-dimensional arrays cannot directly use ARGWHERE results for filtering
# The following statement will not yield correct results and usually raises an INDEXERROR
arr[mask]

# But for one-dimensional array filtering, we can use:
arr = np.arange(6)
mask = np.argwhere(arr > 1)
arr[mask.flatten()[0]]

# Find the index of the maximum value
arr = [1, 2, 2, 1, 0]
cprint("Index of maximum value is: {}", np.argmax(arr))
```

When using `searchsorted`, note that the array itself must be sorted; otherwise, correct results will not be obtained.
<!--
Why do we discuss this function? After becoming familiar with NumPy, users might
